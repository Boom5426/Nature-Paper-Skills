# Installation, updates and recovery

The installer requires Bash and Python 3.9+ with its standard library. Remote installation also requires curl and tar. It does not install an agent, plotting packages or API credentials.

## Choose scope

| Agent | User-level default | `--local` in current project |
|---|---|---|
| Codex | `~/.agents/skills` | `./.agents/skills` |
| Claude Code | `~/.claude/skills` | `./.claude/skills` |

Use `--agent both` for both locations, including with `--local`. `--dest <directory>` overrides agent selection and cannot be combined with `--local`. The current working directory determines the project-local target; run from the intended project.

For an older Codex setup using `~/.codex/skills`, first inspect its actual discovery behavior. You can retain that target explicitly with `--dest ~/.codex/skills`. Installing into a new path does not migrate or delete old copies. Avoid keeping conflicting versions with the same name in multiple discovered locations. The [current official Codex guide](https://developers.openai.com/codex/build-skills) describes `.agents/skills`; this project does not claim every historical client behaves identically.

### Manual layout: one canonical copy, linked into the agent directory

This is a manual layout for one installed version shared by several agents. The installer manages the canonical directory; the links in the agent directories are yours to create, check and repair. Run updates, `--doctor` and restores against the canonical directory.

```bash
CANONICAL=~/skill-store/nature-paper-skills
bash install.sh --dest "$CANONICAL" --set all

AGENT_DIR=~/.claude/skills   # Codex: ~/.agents/skills
mkdir -p "$AGENT_DIR"
conflicts=0
for d in "$CANONICAL"/*/; do
  [ -f "${d}SKILL.md" ] || continue
  name=$(basename "$d")
  target="$AGENT_DIR/$name"
  if [ -L "$target" ]; then
    [ "$(readlink "$target")" = "${d%/}" ] && continue
    echo "conflict: $target points to $(readlink "$target")" >&2
    conflicts=$((conflicts + 1))
    continue
  fi
  if [ -e "$target" ]; then
    echo "conflict: $target exists and is not a link to the canonical copy" >&2
    conflicts=$((conflicts + 1))
    continue
  fi
  ln -s "${d%/}" "$target"
done
if [ "$conflicts" -gt 0 ]; then
  echo "$conflicts entry or entries left untouched; resolve them yourself" >&2
  exit 1
fi
```

The loop creates missing entries, skips a link that already points at the canonical copy, and reports anything else instead of replacing it, so it is safe on a fresh and on an existing agent directory. Targets are absolute, so a link keeps resolving when its entry is moved, and updating the canonical directory does not require recreating the links. An earlier copy-based install leaves real directories in the agent directory; the loop reports those as conflicts rather than replacing them.

Ownership and limits:

- Run `--doctor` against the canonical directory. Pointed at an agent directory, it reports each linked entry as `LINKED` or `INVALID_LINK`, says it is not verified there, and exits 1; that describes the installation record of the directory you pointed it at, not the state of the canonical installation.
- An installer run aimed at a directory that holds these links stops during preflight unless `--on-conflict keep` is set, and a restore refuses per-skill symlinks in targets and backup entries. See the notes under Local changes and conflicts and Restore.
- One canonical copy can serve several agents, but the layout does not resolve a name collision between packs: when two packs provide the same skill name, the agent still discovers only one of them.

## Inspect and update

From a clone:

```bash
bash install.sh --agent codex --list
bash install.sh --agent codex --dry-run
bash install.sh --agent codex --doctor
bash install.sh --agent codex --on-conflict backup
```

Re-running the installer updates the selected set. Keep using `--figure` or `--set all` when updating those sets; unselected skills remain installed at their previous versions. Doctor lists all recorded skills so mixed versions are visible.

Each destination stores `.nature-paper-skills/installed.json`: ownership, component versions, source ref/commit, and hashes of installed files. A local checkout records its commit and whether it has uncommitted changes. Remote installation resolves a ref to a commit when GitHub's API is available; if lookup fails, the requested ref and file hashes remain recorded, and the installer reports that the commit was not resolved. Do not treat an unresolved branch name as an immutable version.

Metadata writes exclusively create a new temporary sibling and atomically replace the record. Existing predictable `.tmp` paths are not followed. See [helper input and failure boundaries](helper-script-boundaries.md) for file-write and scan behavior.

### Local changes and conflicts

- Default `--on-conflict backup`: preserve the existing directory, including local changes, then install the selected version.
- `--on-conflict keep`: keep modified or untracked skills. Unchanged managed skills can still update. Kept skills may remain on an older version.
- `--on-conflict error`: stop before replacing any skills if a local conflict exists.

A directory without `SKILL.md` is never replaced. Managed metadata cannot be a symlink. Install payloads are staged before replacement; ordinary copy/replace errors roll back replaced skills. Backups are not automatically expired. This is not a guarantee against a machine crash or concurrent installers: run one installer per destination at a time.

During installation, per-skill symlinks are not converted into copies. The default `backup` policy and `error` stop during preflight if a selected skill entry is a symlink; no selected destination is changed. Use `--on-conflict keep` to leave linked entries untouched, including broken links, while updating other selected skills. Kept links are not adopted into the installation record. Update the canonical installation directory instead of its links. A symlink used for the entire `--dest` directory is still resolved as before.

## Restore

`--doctor` lists backup IDs, and updates print the IDs containing replaced copies. Use the ID exactly as shown:

```bash
bash install.sh --agent codex --restore <backup-id> --dry-run
bash install.sh --agent codex --restore <backup-id>
```

Restore puts back the skills present in that backup and preserves the current copies in a new backup. It does not remove skills first installed later. An old unmanaged copy remains unmanaged after restoration; doctor reports it as untracked. An intentionally restored modified copy may still be reported as modified relative to its old recorded baseline.

Restore refuses per-skill symlinks in both current targets and backup entries before changing any selected destination. Relative links cannot safely be moved into a rescue backup. Restore real directories at their canonical destination; symlinked destination roots remain supported.

## Pinning a version

`VERSION` and [CHANGELOG](../CHANGELOG.md) identify behavior changes. For reproducible installation, use a full commit SHA from [history](https://github.com/Boom5426/Nature-Paper-Skills/commits/main):

```bash
bash install.sh --agent codex --ref <full-commit-sha>
```

The remote script also accepts this flag. To reproduce a version predating the management helper, run the `install.sh` from that same old commit. A version label in `VERSION` is not itself a Git tag.

## Troubleshooting

| Symptom | Next action |
|---|---|
| `bash` not recognized in Windows | Check whether the app uses the native or WSL2 agent; use the corresponding [Windows installation route](installation-codex.md#windows-desktop-app) |
| GitHub skill installation reports missing path or `SKILL.md` | Select individual skill directories under `skills/<category>/<name>`; the repository root is a collection |
| ChatGPT Work on the web cannot import the repository | Check the [workspace/plugin distribution requirements](installation-codex.md#chatgpt-work-on-the-web); a local install and a source archive do not supply marketplace metadata |
| Python requirement error | Make Python 3.9+ available as `python3` or `python` in that environment |
| Installer cannot identify an agent | Set `--agent codex`, `--agent claude`, or an explicit `--dest` |
| Doctor reports missing/untracked/modified | Read the reported path; reinstall, retain your local edit, or restore the intended copy |
| Installer refuses a linked skill, or doctor reports `LINKED`/`INVALID_LINK` | Inspect the displayed target; update/check its canonical installation directory, or use `--on-conflict keep` to retain the entry. A broken link must be repaired manually; doctor does not verify or adopt the target |
| Agent cannot see a skill despite doctor succeeding | Open its skill selector; explicitly invoke `$paper-workflow` in Codex CLI/IDE or `/paper-workflow` in Claude Code. Refresh/reopen the session and verify the agent uses the same machine and scope |
| Skill sends you to an unavailable figure/research tool | Add `--figure` or `--set all`; the default supports prose and reviewer replies |
| A helper mentions the wrong path | Use the directory the installer printed; replace global example paths with your project-local or custom root |
| Figure checks cannot run | Install the chosen plotting/checking dependencies; report unavailable checks, never a PASS |

Doctor exit codes: **0** recorded selected/all managed files match; **1** missing, untracked, modified or unverified linked skills; **2** usage, malformed metadata or I/O errors. Optional dependency discovery is informational; it does not render a figure, check R package versions, test API access or prove the current agent has loaded a skill.
