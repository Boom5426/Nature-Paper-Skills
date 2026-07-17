#!/usr/bin/env bash
# Nature-Paper-Skills installer.
#
# Remote (no clone needed):
#   curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash
#   curl -fsSL https://raw.githubusercontent.com/Boom5426/Nature-Paper-Skills/main/install.sh | bash -s -- --agent codex --figure
#
# From a clone:
#   ./install.sh --agent claude
#
# Environment overrides: NPS_REPO, NPS_REF (either one forces a download even from a clone).

set -euo pipefail

REPO="${NPS_REPO:-Boom5426/Nature-Paper-Skills}"
REF="${NPS_REF:-main}"

# An explicitly requested repo or ref must not be silently satisfied by whatever
# happens to be in the local working tree.
SOURCE_PINNED=0
[ -n "${NPS_REPO:-}" ] && SOURCE_PINNED=1
[ -n "${NPS_REF:-}" ] && SOURCE_PINNED=1

RECOMMENDED_SKILLS=(
  core/paper-workflow
  core/paper-bootstrap
  core/scientific-writing
  core/manuscript-optimizer
  core/results-section-revision
  core/figure-planner
  core/citation-verifier
  core/data-availability
  core/submission-audit
  core/rebuttal-response
  core/stats-reporting-audit
  core/scientific-prose-style
  venue/nature-portfolio-playbook
)

FIGURE_SKILLS=(
  figure/nature-figure
  figure/figure-style
)

AGENT=""
DEST_OVERRIDE=""
DEST_SET=0
SKILL_SET="recommended"
WITH_FIGURE=0
PROJECT_LOCAL=0
DRY_RUN=0
LIST_ONLY=0
SOURCE_DIR=""
SOURCE_LABEL=""
TMP_DIR=""
PROMPTED_AGENT=""
DESTS=()
STAGING=""

# stdout and stderr are redirected independently, so they need separate gates.
if [ -t 1 ]; then
  C_BOLD=$'\033[1m'; C_DIM=$'\033[2m'; C_GREEN=$'\033[32m'; C_RESET=$'\033[0m'
else
  C_BOLD=""; C_DIM=""; C_GREEN=""; C_RESET=""
fi
if [ -t 2 ]; then
  E_DIM=$'\033[2m'; E_RED=$'\033[31m'; E_RESET=$'\033[0m'
else
  E_DIM=""; E_RED=""; E_RESET=""
fi

info() { printf '%s\n' "$*"; }
# Diagnostics go to stderr: resolve_source runs before the caller knows anything,
# and --list must keep stdout free of prose.
note() { printf '%s\n' "${E_DIM}$*${E_RESET}" >&2; }
die()  { printf '%s\n' "${E_RED}error:${E_RESET} $*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Nature-Paper-Skills installer

Usage:
  install.sh [options]

Options:
  --agent <claude|codex|both>  Target agent. Default: auto-detect from ~/.claude and ~/.codex.
  --local                      Install into ./.claude/skills (current project only; Claude Code only).
  --dest <dir>                 Install into an explicit directory. Overrides --agent; conflicts with --local.
  --set <recommended|all>      Which skills to install. Default: recommended (13 skills).
  --figure                     Add the figure stack (nature-figure, figure-style) to --set recommended.
                               Needs a plotting backend: Python matplotlib/seaborn or R ggplot2.
  --ref <branch|tag|sha>       Download and install from this ref. Forces a download even from a clone.
                               Default: install from your clone, or from main when there is no clone.
  --list                       Print the skills that would be installed, then exit.
  --dry-run                    Show what would happen without writing anything.
  -h, --help                   Show this help.

Both `--flag value` and `--flag=value` are accepted.

Examples:
  ./install.sh                                   # auto-detect agent, recommended set
  ./install.sh --agent codex --figure            # Codex, recommended set plus figure stack
  ./install.sh --agent claude --local            # this project only
  ./install.sh --dest ~/somewhere/skills --set all
EOF
}

cleanup() {
  if [ -n "$TMP_DIR" ] && [ -d "$TMP_DIR" ]; then
    rm -rf "$TMP_DIR"
  fi
  # A half-copied skill must never be left where an agent would load it.
  if [ -n "$STAGING" ] && [ -d "$STAGING" ]; then
    rm -rf "$STAGING"
  fi
}
trap cleanup EXIT

# Reject an empty value and a bare option accidentally consumed as one. Without this,
# `--dest ""` looks the same as "no --dest" downstream and `--dest --figure` would
# install into a directory named "--figure".
require_value() {
  local flag="$1" value="$2" what="$3"
  [ -n "$value" ] || die "$flag needs $what"
  case "$value" in
    --*) die "$flag needs $what (got an option: $value)" ;;
  esac
}

parse_args() {
  while [ $# -gt 0 ]; do
    case "$1" in
      --agent)
        [ $# -ge 2 ] || die "--agent needs a value (claude, codex, or both)"
        require_value --agent "$2" "a value (claude, codex, or both)"
        AGENT="$2"; shift 2 ;;
      --agent=*)
        AGENT="${1#*=}"
        require_value --agent "$AGENT" "a value (claude, codex, or both)"
        shift ;;
      --dest)
        [ $# -ge 2 ] || die "--dest needs a directory"
        require_value --dest "$2" "a directory"
        DEST_OVERRIDE="$2"; DEST_SET=1; shift 2 ;;
      --dest=*)
        DEST_OVERRIDE="${1#*=}"
        require_value --dest "$DEST_OVERRIDE" "a directory"
        DEST_SET=1; shift ;;
      --set)
        [ $# -ge 2 ] || die "--set needs a value (recommended or all)"
        require_value --set "$2" "a value (recommended or all)"
        SKILL_SET="$2"; shift 2 ;;
      --set=*)
        SKILL_SET="${1#*=}"
        require_value --set "$SKILL_SET" "a value (recommended or all)"
        shift ;;
      --ref)
        [ $# -ge 2 ] || die "--ref needs a value"
        require_value --ref "$2" "a branch, tag, or commit"
        REF="$2"; SOURCE_PINNED=1; shift 2 ;;
      --ref=*)
        REF="${1#*=}"
        require_value --ref "$REF" "a branch, tag, or commit"
        SOURCE_PINNED=1; shift ;;
      --figure) WITH_FIGURE=1; shift ;;
      --local) PROJECT_LOCAL=1; shift ;;
      --list) LIST_ONLY=1; shift ;;
      --dry-run) DRY_RUN=1; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "unknown option: $1 (try --help)" ;;
    esac
  done

  case "$AGENT" in
    ""|claude|codex|both) ;;
    *) die "--agent must be claude, codex, or both (got: $AGENT)" ;;
  esac
  case "$SKILL_SET" in
    recommended|all) ;;
    *) die "--set must be recommended or all (got: $SKILL_SET)" ;;
  esac
  if [ "$PROJECT_LOCAL" -eq 1 ] && [ "$DEST_SET" -eq 1 ]; then
    die "--local and --dest are mutually exclusive"
  fi
  if [ "$PROJECT_LOCAL" -eq 1 ] && { [ "$AGENT" = "codex" ] || [ "$AGENT" = "both" ]; }; then
    die "Codex reads only ~/.codex/skills, so --local cannot cover it; use --agent claude with --local, or drop --local"
  fi
}

# Locate a checkout that contains skills/. Prefer the directory this script lives in
# (the clone case); otherwise download the repository tarball (the curl | bash case).
resolve_source() {
  local script_dir="" self="${BASH_SOURCE[0]:-}"

  # Under `curl | bash` the script has no path: bash sets BASH_SOURCE[0] to the
  # interpreter name, which must not be resolved against the current directory.
  case "$self" in
    ""|bash|-bash|sh|-sh) self="" ;;
  esac

  # Follow symlinks by hand (readlink -f is GNU-only): a symlinked install.sh must
  # still find the clone it lives in rather than quietly downloading instead.
  local hops=0 target
  while [ -n "$self" ] && [ -L "$self" ] && [ "$hops" -lt 20 ]; do
    target="$(readlink "$self")"
    case "$target" in
      /*) self="$target" ;;
      *)  self="$(dirname "$self")/$target" ;;
    esac
    hops=$((hops + 1))
  done

  if [ "$SOURCE_PINNED" -eq 0 ] && [ -n "$self" ] && [ -f "$self" ]; then
    script_dir="$(cd "$(dirname "$self")" && pwd)"
    if [ -d "$script_dir/skills" ]; then
      SOURCE_DIR="$script_dir"
      SOURCE_LABEL="local checkout at $SOURCE_DIR"
      note "source: $SOURCE_LABEL"
      return
    fi
  fi

  command -v curl >/dev/null 2>&1 || die "curl is required to download the repository"
  command -v tar  >/dev/null 2>&1 || die "tar is required to unpack the repository"

  # Pass an explicit template: BSD/macOS mktemp rejects a bare `mktemp -d`, which
  # would abort the headline `curl | bash` install on every Mac.
  TMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/nature-paper-skills.XXXXXXXX")" \
    || die "could not create a temporary directory"
  local url="https://codeload.github.com/${REPO}/tar.gz/${REF}"
  local tarball="$TMP_DIR/source.tar.gz"
  SOURCE_LABEL="${REPO}@${REF}"
  note "source: downloading ${SOURCE_LABEL}"

  # Fetch to a file rather than piping into tar: a bad ref would otherwise make tar
  # fail on an empty stream and print decoder noise ahead of the real message.
  curl -fsSL -o "$tarball" "$url" 2>/dev/null \
    || die "could not download ${REPO}@${REF}; check the ref name and your network (tried ${url})"
  tar -xzf "$tarball" --strip-components=1 -C "$TMP_DIR" 2>/dev/null \
    || die "could not unpack the archive downloaded from ${url}"
  [ -d "$TMP_DIR/skills" ] || die "downloaded archive has no skills/ directory"
  SOURCE_DIR="$TMP_DIR"
}

selected_skills() {
  if [ "$SKILL_SET" = "all" ]; then
    local d
    for d in "$SOURCE_DIR"/skills/*/*/; do
      [ -f "${d}SKILL.md" ] || continue
      d="${d%/}"
      printf '%s/%s\n' "$(basename "$(dirname "$d")")" "$(basename "$d")"
    done | sort
    return
  fi

  printf '%s\n' "${RECOMMENDED_SKILLS[@]}"
  if [ "$WITH_FIGURE" -eq 1 ]; then
    printf '%s\n' "${FIGURE_SKILLS[@]}"
  fi
}

# Populates the DESTS array. Deliberately not a stdout-returning function: it can
# fail or prompt, and inside a command substitution `die` would only exit the
# subshell, leaving the caller to carry on with an empty target list.
resolve_dests() {
  DESTS=()

  if [ "$DEST_SET" -eq 1 ]; then
    # `--dest=~/x` reaches us unexpanded: bash expands a tilde after `=` only in a
    # real assignment, so do here what the caller's shell did for `--dest ~/x`.
    case "$DEST_OVERRIDE" in
      "~")   DEST_OVERRIDE="$(home_or_die)" ;;
      "~/"*) DEST_OVERRIDE="$(home_or_die)/${DEST_OVERRIDE#\~/}" ;;
      "~"*)  die "--dest does not support ~user paths; pass an absolute path" ;;
    esac
    DESTS=("$DEST_OVERRIDE")
    return
  fi

  if [ "$PROJECT_LOCAL" -eq 1 ]; then
    DESTS=("$PWD/.claude/skills")
    return
  fi

  local home
  home="$(home_or_die)"

  local agent="$AGENT"
  if [ -z "$agent" ]; then
    local has_claude=0 has_codex=0
    [ -d "$home/.claude" ] && has_claude=1
    [ -d "$home/.codex" ] && has_codex=1
    if [ "$has_claude" -eq 1 ] && [ "$has_codex" -eq 1 ]; then
      agent="both"
    elif [ "$has_claude" -eq 1 ]; then
      agent="claude"
    elif [ "$has_codex" -eq 1 ]; then
      agent="codex"
    fi

    if [ -n "$agent" ]; then
      note "agent: ${agent} (auto-detected; override with --agent)"
    else
      prompt_for_agent
      agent="$PROMPTED_AGENT"
      note "agent: ${agent}"
    fi
  fi

  case "$agent" in
    claude) DESTS=("$home/.claude/skills") ;;
    codex)  DESTS=("$home/.codex/skills") ;;
    both)   DESTS=("$home/.claude/skills" "$home/.codex/skills") ;;
    *) die "internal error: unresolved agent '$agent'" ;;
  esac
}

home_or_die() {
  [ -n "${HOME:-}" ] || die "HOME is not set, so ~/.claude and ~/.codex cannot be located; pass --dest <dir>"
  printf '%s\n' "$HOME"
}

# Reached only when neither agent directory exists. Ask on the terminal if there is
# one (stdin is the script itself under curl | bash), otherwise fail loudly.
# Sets PROMPTED_AGENT.
prompt_for_agent() {
  PROMPTED_AGENT=""
  # Probe in a subshell: with no controlling terminal /dev/tty passes a -r test but
  # fails to open, and the raw redirection error would replace this message.
  if ! (: < /dev/tty) 2>/dev/null; then
    die "found neither ~/.claude nor ~/.codex, and no terminal to ask; pass --agent claude|codex|both or --dest <dir>"
  fi
  local reply=""
  printf '%s\n' "Found neither ~/.claude nor ~/.codex. Install for which agent?" > /dev/tty
  printf '%s\n' "  1) Claude Code   2) Codex   3) both" > /dev/tty
  printf '%s' "Choice [1]: " > /dev/tty
  read -r reply < /dev/tty || true
  case "${reply:-1}" in
    1) PROMPTED_AGENT=claude ;;
    2) PROMPTED_AGENT=codex ;;
    3) PROMPTED_AGENT=both ;;
    *) die "invalid choice: $reply" ;;
  esac
}

# Every check here is a pure read, so run them all against every destination before
# the first write. The recommended list is hard-coded in this script while --ref can
# swap the source tree underneath it, and checking inside the copy loop would abort
# partway through, leaving some skills upgraded and the rest at their old version.
preflight() {
  local dest="$1"; shift
  local skills=("$@")
  local rel name src
  local missing=""

  for rel in "${skills[@]}"; do
    src="$SOURCE_DIR/skills/$rel"
    if [ ! -d "$src" ] || [ ! -f "$src/SKILL.md" ]; then
      missing="${missing}  skills/${rel}"$'\n'
      continue
    fi
    name="${rel##*/}"
    # We would delete this path, so make sure it is a skill and not something of the
    # user's that happens to share the name.
    if [ -e "$dest/$name" ] && { [ ! -d "$dest/$name" ] || [ ! -f "$dest/$name/SKILL.md" ]; }; then
      die "$dest/$name exists and is not a skill (no SKILL.md); move it aside first (nothing was written)"
    fi
  done

  if [ -n "$missing" ]; then
    printf '%s\n' "${E_RED}error:${E_RESET} source (${SOURCE_LABEL}) is missing selected skills (nothing was written):" >&2
    printf '%s' "$missing" >&2
    exit 1
  fi
}

install_into() {
  local dest="$1"; shift
  local skills=("$@")
  local rel name src verb installed=0 replaced=0

  info ""
  info "${C_BOLD}→ ${dest}${C_RESET}"

  if [ "$DRY_RUN" -eq 0 ]; then
    mkdir -p "$dest"
  fi

  for rel in "${skills[@]}"; do
    name="${rel##*/}"
    src="$SOURCE_DIR/skills/$rel"

    verb="install"
    [ -e "$dest/$name" ] && verb="replace"

    if [ "$DRY_RUN" -eq 1 ]; then
      info "  would ${verb}  $name"
      installed=$((installed + 1))
      [ "$verb" = "replace" ] && replaced=$((replaced + 1))
      continue
    fi

    # Copy to a staging directory first, then swap. Replacing in place would leave a
    # half-copied skill loadable if the run is interrupted mid-copy; this way the
    # only exposed window is the rename.
    STAGING="$dest/.nps-staging-$name"
    rm -rf "$STAGING"
    cp -R "$src" "$STAGING"
    rm -rf "${dest:?}/$name"
    mv "$STAGING" "$dest/$name"
    STAGING=""

    if [ "$verb" = "replace" ]; then
      info "  ${C_GREEN}✓${C_RESET} $name ${C_DIM}(replaced)${C_RESET}"
      replaced=$((replaced + 1))
    else
      info "  ${C_GREEN}✓${C_RESET} $name"
    fi
    installed=$((installed + 1))
  done

  if [ "$replaced" -gt 0 ]; then
    info "  ${C_DIM}${installed} skills, ${replaced} replaced${C_RESET}"
  else
    info "  ${C_DIM}${installed} skills${C_RESET}"
  fi
}

# True when every figure skill is already present in every destination.
figure_stack_present() {
  local dest rel
  for dest in "${DESTS[@]}"; do
    for rel in "${FIGURE_SKILLS[@]}"; do
      [ -f "$dest/${rel##*/}/SKILL.md" ] || return 1
    done
  done
  return 0
}

main() {
  parse_args "$@"
  resolve_source

  local skills=() line
  while IFS= read -r line; do
    [ -n "$line" ] && skills+=("$line")
  done < <(selected_skills)
  [ "${#skills[@]}" -gt 0 ] || die "no skills selected"

  if [ "$LIST_ONLY" -eq 1 ]; then
    printf '%s\n' "${skills[@]}"
    exit 0
  fi

  resolve_dests
  [ "${#DESTS[@]}" -gt 0 ] || die "could not determine an install directory"

  # Validate every destination before writing to any of them, so `--agent both`
  # cannot fail on the second one after the first is already rewritten.
  local dest
  for dest in "${DESTS[@]}"; do
    preflight "$dest" "${skills[@]}"
  done
  for dest in "${DESTS[@]}"; do
    install_into "$dest" "${skills[@]}"
  done

  info ""
  if [ "$DRY_RUN" -eq 1 ]; then
    info "${C_BOLD}Dry run: nothing was written.${C_RESET}"
    return
  fi

  info "${C_BOLD}Done.${C_RESET} Fully restart your agent so it picks up the new skills"
  info "(quit and relaunch Claude Code or Codex, not just /clear), then paste:"
  info ""
  info "  Use paper-workflow to tell me which skill I should use next for this manuscript."
  # Only offer the figure stack where it is actually absent: it survives a re-run
  # without --figure, and claiming otherwise would contradict what is on disk.
  if [ "$WITH_FIGURE" -eq 0 ] && [ "$SKILL_SET" = "recommended" ] && ! figure_stack_present; then
    info ""
    info "${C_DIM}The figure stack (nature-figure, figure-style) was not installed."
    info "Add it with: --figure   (needs Python matplotlib/seaborn or R ggplot2)${C_RESET}"
  fi
}

main "$@"
