#!/usr/bin/env python3
"""Install, inspect and restore NPS skills using only the Python standard library."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile
from datetime import datetime, timezone
import uuid

OWNER = "Nature-Paper-Skills"
STATE = ".nature-paper-skills"


def read_manifest(dest):
    path = dest / STATE / "installed.json"
    if not path.exists():
        return {"owner": OWNER, "schema": 1, "skills": {}}
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("owner") != OWNER or value.get("schema") != 1 or not isinstance(value.get("skills"), dict):
        raise ValueError(f"Unrecognized installation record: {path}")
    return value


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusively create a fresh sibling; never open a pre-existing .tmp link.
    fd, name = tempfile.mkstemp(prefix=f".{path.name}-", suffix=".tmp", dir=path.parent)
    temp = Path(name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            handle.write(json.dumps(value, indent=2, ensure_ascii=False) + "\n")
        os.replace(temp, path)
    finally:
        temp.unlink(missing_ok=True)


def fingerprint(root):
    """Include paths, bytes, executable bits and symlink targets; ignore bytecode."""
    if root.is_symlink():
        return {".": "symlink:" + os.readlink(root)}
    result = {}
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(dirs + files):
            path = Path(parent) / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink():
                result[rel] = "symlink:" + os.readlink(path)
            elif path.is_file() and path.suffix not in {".pyc", ".pyo"}:
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                result[rel] = digest + (":x" if path.stat().st_mode & 0o111 else "")
    return result


def safe_name(name):
    if not name or name in {".", ".."} or any(c not in "abcdefghijklmnopqrstuvwxyz0123456789-" for c in name):
        raise ValueError(f"Invalid skill name: {name!r}")
    return name


def destination(raw):
    dest = Path(raw).expanduser().absolute()
    # Resolve the destination itself, but reject links used as our management area.
    dest = dest.resolve()
    for path in (dest / STATE, dest / STATE / "backups", dest / STATE / "installed.json"):
        if path.is_symlink():
            raise ValueError(f"Management path must not be a symlink: {path}")
    return dest


def copy_skill(src, target):
    shutil.copytree(src, target, symlinks=True, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo"))


def remove(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def install(args, dests):
    source = Path(args.source)
    selected = [(rel, safe_name(Path(rel).name)) for rel in args.skill]
    if len({name for _, name in selected}) != len(selected):
        raise ValueError("Duplicate skill names in selection")
    version = (source / "VERSION").read_text().strip() if (source / "VERSION").exists() else "unversioned"
    plans = []
    # Check all destinations before replacing any skill.
    for dest in dests:
        manifest = read_manifest(dest)
        for rel, name in selected:
            src = source / "skills" / rel
            if not src.is_dir() or not (src / "SKILL.md").is_file():
                raise ValueError(f"Missing source skill: {src}")
            if rel in args.apache:
                for license_name in ("LICENSE-APACHE", "NOTICE"):
                    if not (source / license_name).is_file():
                        raise ValueError(f"Missing license: {license_name}")
            target = dest / name
            exists = target.exists() or target.is_symlink()
            if exists and not (target / "SKILL.md").is_file():
                raise ValueError(f"Target is not a skill; nothing replaced: {target}")
            old = manifest["skills"].get(name)
            conflict = exists and (not old or fingerprint(target) != old.get("files"))
            if conflict and args.on_conflict == "error":
                raise ValueError(f"Unmanaged or locally modified skill: {target}; use --on-conflict backup or keep")
            plans.append((dest, manifest, rel, name, conflict))
    if args.dry_run:
        for dest, _, _, name, conflict in plans:
            action = "keep" if conflict and args.on_conflict == "keep" else "install (back up any existing copy)"
            print(f"Would {action}: {dest / name}")
        return 0

    batch_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    # Stage complete payloads before touching installed files. A failed copy leaves old skills intact.
    stages, changed, old_manifests, manifests = [], [], {}, {}
    try:
        for dest in dests:
            old_manifests[dest] = read_manifest(dest)
            manifests[dest] = json.loads(json.dumps(old_manifests[dest]))
        for dest, _, rel, name, conflict in plans:
            if conflict and args.on_conflict == "keep":
                print(f"Kept locally modified/unmanaged skill: {dest / name}")
                continue
            state = dest / STATE
            state.mkdir(parents=True, exist_ok=True)
            stage = Path(tempfile.mkdtemp(prefix="stage-", dir=state))
            stages.append(stage)
            payload = stage / name
            copy_skill(source / "skills" / rel, payload)
            if rel in args.apache:
                for license_name in ("LICENSE-APACHE", "NOTICE"):
                    shutil.copy2(source / license_name, payload / license_name)
            files = fingerprint(payload)
            target = dest / name
            prior = manifests[dest]["skills"].get(name)
            record = {"repo": args.repo, "requested_ref": args.source_ref, "commit": args.commit or None,
                      "version": version, "files": files}
            if target.exists() and prior == record and fingerprint(target) == files:
                print(f"Unchanged: {target}")
                continue
            stages[-1] = (stage, dest, name, payload, record, conflict)
        for item in stages:
            if not isinstance(item, tuple):
                continue
            stage, dest, name, payload, record, conflict = item
            target = dest / name
            backup_dir = dest / STATE / "backups" / batch_id
            backup = backup_dir / name
            existed = target.exists() or target.is_symlink()
            if existed:
                backup_dir.mkdir(parents=True, exist_ok=True)
                if not (backup_dir / "before.json").exists():
                    write_json(backup_dir / "before.json", old_manifests[dest])
                os.replace(target, backup)
            changed.append((dest, name, existed, backup))
            os.replace(payload, target)
            manifests[dest]["skills"][name] = record
            print(f"Installed: {target}" + (" (local changes backed up)" if conflict else ""))
        for dest in dests:
            write_json(dest / STATE / "installed.json", manifests[dest])
        for dest in dests:
            replaced = [name for d, name, existed, _ in changed if d == dest and existed]
            if replaced:
                print(f"Backup {batch_id}: {', '.join(replaced)}")
                print(f"Restore: bash install.sh --dest '{dest}' --restore {batch_id}")
        print("Installation files are ready. In your agent, invoke paper-workflow using the quickstart example.")
        print("If it is not visible, refresh the skill list or reopen the session. File checks do not prove session loading.")
        return 0
    except BaseException:
        for dest, name, existed, backup in reversed(changed):
            remove(dest / name)
            if existed:
                os.replace(backup, dest / name)
        for dest in old_manifests:
            if changed:
                write_json(dest / STATE / "installed.json", old_manifests[dest])
        raise
    finally:
        for item in stages:
            remove(item[0] if isinstance(item, tuple) else item)


def doctor(args, dests):
    failed = False
    for dest in dests:
        manifest = read_manifest(dest)
        names = sorted(set(safe_name(Path(s).name) for s in args.skill) | set(manifest["skills"]))
        print(f"Checking {dest}")
        for name in names:
            safe_name(name)
            target, record = dest / name, manifest["skills"].get(name)
            if not (target / "SKILL.md").is_file():
                status = "MISSING"
            elif not record:
                status = "UNTRACKED (installed without an NPS record)"
            elif fingerprint(target) != record.get("files"):
                status = "MODIFIED"
            else:
                print(f"OK {name}: {record.get('version')} @ {record.get('commit') or record.get('requested_ref')}")
                continue
            print(f"{status}: {name}")
            failed = True
        backups = dest / STATE / "backups"
        print("Backups: " + (", ".join(p.name for p in sorted(backups.iterdir()) if p.is_dir()) if backups.exists() else "none"))
        if (dest / "nature-figure").exists():
            print("Figure dependencies: matplotlib=" + str(importlib.util.find_spec("matplotlib") is not None)
                  + "; Rscript=" + str(shutil.which("Rscript") is not None)
                  + ". No figure was rendered; R packages and optional APIs were not tested.")
    print("This checks files and installation records, not agent discovery or manuscript quality.")
    return 1 if failed else 0


def restore(args, dests):
    backup_id = args.restore
    if not backup_id or any(c not in "0123456789TZ-abcdef" for c in backup_id):
        raise ValueError("Use a backup ID printed by --doctor")
    plans = []
    for dest in dests:
        backup_dir = dest / STATE / "backups" / backup_id
        if backup_dir.is_symlink() or not backup_dir.is_dir():
            raise ValueError(f"Backup not found: {backup_dir}")
        before = json.loads((backup_dir / "before.json").read_text())
        current = read_manifest(dest)
        for backup in sorted(backup_dir.iterdir()):
            if backup.name == "before.json":
                continue
            name = safe_name(backup.name)
            if not (backup / "SKILL.md").is_file():
                raise ValueError(f"Backup is not a skill: {backup}")
            target = dest / name
            if (target.exists() or target.is_symlink()) and not (target / "SKILL.md").is_file():
                raise ValueError(f"Current target is not a skill: {target}")
            plans.append((dest, name, backup, before, current))
    if not plans:
        raise ValueError("Backup contains no replaced skills to restore")
    if args.dry_run:
        for dest, name, *_ in plans:
            print(f"Would restore {dest / name}; preserve its current version in a new backup")
        return 0
    rescue_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    staged, changed, original, manifests = [], [], {}, {}
    try:
        for dest in dests:
            original[dest] = read_manifest(dest)
            manifests[dest] = json.loads(json.dumps(original[dest]))
        for dest, name, backup, before, _ in plans:
            stage = Path(tempfile.mkdtemp(prefix="restore-", dir=dest / STATE))
            staged.append(stage)
            copy_skill(backup, stage / name) if not backup.is_symlink() else (stage / name).symlink_to(os.readlink(backup), target_is_directory=True)
        for (dest, name, backup, before, _), stage in zip(plans, staged):
            rescue = dest / STATE / "backups" / rescue_id
            rescue.mkdir(parents=True, exist_ok=True)
            write_json(rescue / "before.json", original[dest])
            target = dest / name
            existed = target.exists() or target.is_symlink()
            if existed:
                os.replace(target, rescue / name)
            changed.append((dest, name, existed, rescue / name))
            os.replace(stage / name, target)
            if name in before["skills"]:
                manifests[dest]["skills"][name] = before["skills"][name]
            else:
                manifests[dest]["skills"].pop(name, None)
            print(f"Restored: {target}; previous version saved in {rescue_id}")
        for dest in dests:
            write_json(dest / STATE / "installed.json", manifests[dest])
        return 0
    except BaseException:
        for dest, name, existed, rescue in reversed(changed):
            remove(dest / name)
            if existed:
                os.replace(rescue, dest / name)
        for dest in original:
            write_json(dest / STATE / "installed.json", original[dest])
        raise
    finally:
        for path in staged:
            remove(path)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--source", required=True)
    p.add_argument("--repo", default="Boom5426/Nature-Paper-Skills")
    p.add_argument("--source-ref", default="local")
    p.add_argument("--commit", default="")
    p.add_argument("--dest", action="append", required=True)
    p.add_argument("--skill", action="append", default=[])
    p.add_argument("--apache", action="append", default=[])
    p.add_argument("--on-conflict", choices=["backup", "keep", "error"], default="backup")
    p.add_argument("--doctor", action="store_true")
    p.add_argument("--restore")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()
    try:
        dests = list(dict.fromkeys(destination(raw) for raw in args.dest))
        if args.doctor:
            return doctor(args, dests)
        if args.restore:
            return restore(args, dests)
        return install(args, dests)
    except (ValueError, OSError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
