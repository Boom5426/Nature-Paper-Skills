#!/usr/bin/env python3
"""Build a skills-only plugin ZIP and GitHub marketplace using Python 3.9+."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import unicodedata
import zipfile

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = Path("packaging/chatgpt-work")
SKIP_NAMES = {"__pycache__", ".git", ".DS_Store"}
SKIP_SUFFIXES = {".pyc", ".pyo"}


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def installer_array(root, name):
    text = (root / "install.sh").read_text(encoding="utf-8")
    match = re.search(rf"^{name}=\((.*?)^\)", text, re.M | re.S)
    if match is None:
        raise ValueError(f"Missing installer profile: {name}")
    return [line.strip() for line in match.group(1).splitlines() if line.strip()]


def selected_skills(root, profile, figure):
    if profile == "all":
        selected = [p.parent.relative_to(root / "skills").as_posix()
                    for p in sorted((root / "skills").glob("*/*/SKILL.md"))]
    else:
        selected = installer_array(root, "RECOMMENDED_SKILLS")
        if figure:
            selected += installer_array(root, "FIGURE_SKILLS")
    if not selected:
        raise ValueError("The selected profile has no skills")
    names = [PurePosixPath(rel).name for rel in selected]
    if len(names) != len(set(names)):
        raise ValueError("Duplicate skill names in profile")
    for rel in selected:
        parts = PurePosixPath(rel).parts
        if len(parts) != 2 or any(not re.fullmatch(r"[a-z0-9-]+", p) for p in parts):
            raise ValueError(f"Invalid source skill path: {rel}")
    return selected


def resource_files(folder):
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError(f"Expected a real directory: {folder}")
    for path in sorted(folder.rglob("*")):
        rel = path.relative_to(folder)
        if any(part in SKIP_NAMES for part in rel.parts) or path.suffix in SKIP_SUFFIXES:
            continue
        if path.is_symlink():
            raise ValueError(f"Plugin resources must not be symlinks: {path}")
        if path.is_file():
            yield path, rel.as_posix()
        elif not path.is_dir():
            raise ValueError(f"Unsupported plugin resource: {path}")


def check_skill(folder, plugin_name):
    path = folder / "SKILL.md"
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing regular SKILL.md: {folder}")
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    if len(parts) != 3 or parts[0].strip() or not parts[2].strip():
        raise ValueError(f"Invalid skill frontmatter or empty body: {path}")
    name = re.search(r"^name:\s*([a-z0-9-]+)\s*$", parts[1], re.M)
    if name is None or name.group(1) != folder.name:
        raise ValueError(f"Skill name does not match its directory: {path}")
    if not re.search(r"^description:\s*\S", parts[1], re.M):
        raise ValueError(f"Missing skill description: {path}")
    if len(f"{plugin_name}:{folder.name}") > 64:
        raise ValueError(f"Plugin/skill identity exceeds 64 characters: {folder.name}")


def source_state(root):
    def git(*args):
        try:
            return subprocess.check_output(
                ["git", "-C", str(root), *args], text=True, stderr=subprocess.DEVNULL).strip()
        except (OSError, subprocess.CalledProcessError):
            return None
    commit = git("rev-parse", "HEAD")
    status = git("status", "--porcelain")
    return {"commit": commit, "dirty": bool(status) if status is not None else None}


def package_plan(root, profile="recommended", figure=False, version=None):
    manifest = json.loads((root / TEMPLATE / "plugin.json").read_text(encoding="utf-8"))
    name = manifest["name"]
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
        raise ValueError("Invalid plugin name")
    if version is not None:
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[a-zA-Z0-9.-]+)?(?:\+[a-zA-Z0-9.-]+)?", version):
            raise ValueError("Plugin version must be a semantic version, such as 0.1.1")
        manifest["version"] = version
    interface = manifest["extensions"]["com.openai"]["interface"]
    payload = {"plugin.json": (json_bytes(manifest), 0o644)}
    # The compatibility manifest is also accepted by GitHub workspace import.
    compatibility = {k: v for k, v in manifest.items() if k not in {"$schema", "extensions"}}
    compatibility.update(skills="./skills/", interface=interface)
    payload[".codex-plugin/plugin.json"] = (json_bytes(compatibility), 0o644)
    for path, rel in resource_files(root / TEMPLATE / "assets"):
        payload[f"assets/{rel}"] = (path.read_bytes(), 0o644)
    for field in ("composerIcon", "logo"):
        asset = interface[field]
        if not asset.startswith("./") or asset[2:] not in payload:
            raise ValueError(f"Missing or unsafe {field}: {asset}")
    selected = selected_skills(root, profile, figure)
    apache = set(installer_array(root, "APACHE_SKILLS"))
    for rel in selected:
        source = root / "skills" / rel
        check_skill(source, name)
        prefix = f"skills/{source.name}/"
        for path, resource in resource_files(source):
            mode = 0o755 if path.stat().st_mode & 0o111 else 0o644
            payload[prefix + resource] = (path.read_bytes(), mode)
        if rel in apache:
            for license_name in ("LICENSE-APACHE", "NOTICE"):
                payload[prefix + license_name] = ((root / license_name).read_bytes(), 0o644)
    for filename in ("LICENSE", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md", "VERSION"):
        payload[filename] = ((root / filename).read_bytes(), 0o644)
    payload["CREATOR-PROMPT.txt"] = ((root / TEMPLATE / "creator-prompt.txt").read_bytes(), 0o644)
    readme = (
        "# Nature Paper Skills\n\n"
        f"This skills-only plugin contains {len(selected)} skills. Start with paper-workflow "
        "and supply your manuscript and supporting evidence.\n\n"
        "In ChatGPT Work, use Plugin Creator to create a private plugin from this package, "
        "or ask your workspace administrator to import its generated GitHub marketplace. "
        "Attaching this ZIP to an ordinary chat alone does not install it.\n\n"
        "Scripts require the execution tools and packages documented in each skill. "
        "The plugin supplies instructions and resources; it does not provision these tools.\n"
    )
    payload["README.md"] = (readme.encode("utf-8"), 0o644)
    info = {
        "repository": manifest["repository"],
        "source": source_state(root),
        "profile": profile,
        "figure_addon": figure and profile != "all",
        "skills": selected,
        "files": {rel: hashlib.sha256(data).hexdigest()
                  for rel, (data, _) in sorted(payload.items())},
    }
    payload["build-info.json"] = (json_bytes(info), 0o644)
    normalized = set()
    for rel, (data, _) in payload.items():
        parts = PurePosixPath(rel).parts
        if (rel != rel.strip() or "\\" in rel or rel.startswith("/")
                or any(p in {"", ".", ".."} for p in rel.split("/")) or len(parts) > 20):
            raise ValueError(f"Unsafe package path: {rel}")
        key = unicodedata.normalize("NFKC", rel).casefold()
        if key in normalized:
            raise ValueError(f"Case/Unicode collision in package: {rel}")
        normalized.add(key)
        if len(data) > 100 * 1024 * 1024:
            raise ValueError(f"Package file exceeds 100 MiB: {rel}")
    if len(payload) > 5000 or sum(len(data) for data, _ in payload.values()) > 512 * 1024 * 1024:
        raise ValueError("Package exceeds archive entry or extracted-size limits")
    return manifest, payload, selected


def archive_bytes(payload):
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for rel, (data, mode) in sorted(payload.items()):
            entry = zipfile.ZipInfo(rel, date_time=(2020, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = (stat.S_IFREG | mode) << 16
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, data)
    data = buffer.getvalue()
    if len(data) > 100_000_000:
        raise ValueError("Compressed plugin ZIP exceeds 100 MB")
    return data


def web_skill_plan(root, payload, selected):
    """One web creator entry, with specialist directories retained as resources."""
    bundled = {"SKILL.md": ((root / TEMPLATE / "skill" / "SKILL.md").read_bytes(), 0o644)}
    for rel, value in payload.items():
        if rel.startswith("skills/"):
            bundled["resources/" + rel[len("skills/"):]] = value
        elif rel in {"LICENSE", "LICENSE-APACHE", "NOTICE", "ATTRIBUTION.md", "VERSION"}:
            bundled[rel] = value
    index = "# Bundled specialists\n\n" + "\n".join(
        f"- [{PurePosixPath(rel).name}](../resources/{PurePosixPath(rel).name}/SKILL.md)"
        for rel in selected) + "\n"
    bundled["references/bundled-skills.md"] = (index.encode("utf-8"), 0o644)
    info = json.loads(payload["build-info.json"][0])
    info.update(kind="single-skill-source", entry_skill="nature-paper-workflow")
    info["files"] = {rel: hashlib.sha256(data).hexdigest()
                     for rel, (data, _) in sorted(bundled.items())}
    bundled["build-info.json"] = (json_bytes(info), 0o644)
    prompt = (
        "Use the attached nature-paper-workflow skill source ZIP to create and save "
        "a reusable skill named nature-paper-workflow in this ChatGPT Work environment.\n"
        "Preserve the root SKILL.md and every resources/, references/, script, template, "
        "asset and license file. Keep the specialist workflows as resources within this "
        "one skill, rather than creating separate menu entries.\n"
        "Finish the supported save/install flow. Show where it was saved and how I can "
        "select it from @ in a new conversation. A ZIP attachment alone is not installation.\n"
    )
    return bundled, prompt


def build(root, output, profile="recommended", figure=False, version=None):
    output = Path(output).expanduser().absolute()
    if output.exists() or output.is_symlink():
        raise ValueError(f"Output already exists; choose a new directory: {output}")
    manifest, payload, selected = package_plan(root, profile, figure, version)
    archive = archive_bytes(payload)
    web_payload, skill_prompt = web_skill_plan(root, payload, selected)
    web_archive = archive_bytes(web_payload)
    name = manifest["name"]
    zip_name = f"{name}-{manifest['version']}-{profile}"
    if figure and profile != "all":
        zip_name += "-figure"
    zip_name += ".zip"
    catalog = {
        "name": "nature-paper-skills",
        "interface": {"displayName": "Nature Paper Skills"},
        "plugins": [{"name": name, "source": {"source": "local", "path": f"./plugins/{name}"}}],
    }
    # All reads and structural checks finish before creating a fresh destination.
    output.mkdir(parents=True, exist_ok=False)
    plugin = output / "plugins" / name
    for rel, (data, mode) in sorted(payload.items()):
        path = plugin / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
        path.chmod(mode)
    marketplace = output / ".agents" / "plugins" / "marketplace.json"
    marketplace.parent.mkdir(parents=True, exist_ok=True)
    with marketplace.open("xb") as handle:
        handle.write(json_bytes(catalog))
    zip_path = output / zip_name
    with zip_path.open("xb") as handle:
        handle.write(archive)
    web_skill = output / "skills" / "nature-paper-workflow"
    for rel, (data, mode) in sorted(web_payload.items()):
        path = web_skill / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("xb") as handle:
            handle.write(data)
        path.chmod(mode)
    skill_zip = output / f"nature-paper-workflow-{manifest['version']}-{profile}.zip"
    if figure and profile != "all":
        skill_zip = output / f"nature-paper-workflow-{manifest['version']}-{profile}-figure.zip"
    with skill_zip.open("xb") as handle:
        handle.write(web_archive)
    with (output / "SKILL-CREATOR-PROMPT.txt").open("x", encoding="utf-8") as handle:
        handle.write(skill_prompt)
    return {"zip": str(zip_path), "marketplace_root": str(output),
            "plugin": str(plugin), "skill_count": len(selected),
            "zip_sha256": hashlib.sha256(archive).hexdigest(),
            "web_skill": str(web_skill),
            "web_skill_zip": str(skill_zip),
            "web_skill_zip_sha256": hashlib.sha256(web_archive).hexdigest()}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", required=True, type=Path,
                        help="New directory for the plugin ZIP and marketplace; existing paths are refused")
    parser.add_argument("--set", dest="profile", choices=("recommended", "all"), default="recommended")
    parser.add_argument("--figure", action="store_true", help="Add the two figure skills to the recommended profile")
    parser.add_argument("--version", help="Override the plugin semantic version for a release")
    args = parser.parse_args(argv)
    try:
        result = build(ROOT, args.output_dir, args.profile, args.figure, args.version)
    except (OSError, ValueError, KeyError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
