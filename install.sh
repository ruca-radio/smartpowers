#!/usr/bin/env bash
# SmartPowers installer
#
# Installs the full skills suite into a harness skills directory, makes helper
# scripts executable, installs the session-start preamble (the portable
# equivalent of a session-start hook), and verifies the result.
#
# Usage:
#   ./install.sh [--kimi|--claude|--cursor] [--target DIR] [--link] [--uninstall]
#
#   --kimi       Install for Kimi Code / Moonshot harnesses (default)
#                skills -> ~/.agents/skills, preamble -> ~/.agents/AGENTS.md
#   --claude     Install for Claude Code
#                skills -> ~/.claude/skills, preamble -> ~/.claude/CLAUDE.md
#   --cursor     Install for Cursor (skills -> ~/.cursor/skills, preamble printed)
#   --target DIR Install skills to an explicit directory (overrides harness default)
#   --link       Symlink skills instead of copying (development mode)
#   --uninstall  Remove everything this script installed
#
# Idempotent: re-running upgrades in place. Requires bash + git for full
# functionality; python3 enables the skill-lint verification step.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HARNESS="kimi"
TARGET=""
GLOBAL_MD=""
MODE="copy"
UNINSTALL=0

while [ $# -gt 0 ]; do
  case "$1" in
    --kimi)      HARNESS="kimi" ;;
    --claude)    HARNESS="claude" ;;
    --cursor)    HARNESS="cursor" ;;
    --target)    TARGET="${2:?install.sh: --target needs a directory}"; shift ;;
    --link)      MODE="link" ;;
    --uninstall) UNINSTALL=1 ;;
    -h|--help)   sed -n '2,20p' "$0" | sed 's/^#\{1,2\} \{0,1\}//'; exit 0 ;;
    *) echo "install.sh: unknown option '$1' (see --help)" >&2; exit 1 ;;
  esac
  shift
done

case "$HARNESS" in
  kimi)   : "${TARGET:=$HOME/.agents/skills}"; GLOBAL_MD="$HOME/.agents/AGENTS.md" ;;
  claude) : "${TARGET:=$HOME/.claude/skills}"; GLOBAL_MD="$HOME/.claude/CLAUDE.md" ;;
  cursor) : "${TARGET:=$HOME/.cursor/skills}"; GLOBAL_MD="" ;;
esac

MANIFEST="$TARGET/.smartpowers-manifest"
MARK_BEGIN="# >>> smartpowers >>>"
MARK_END="# <<< smartpowers <<<"

strip_preamble() {
  # Remove the managed smartpowers block from a global-instructions file.
  local file="$1"
  [ -f "$file" ] || return 0
  awk -v b="$MARK_BEGIN" -v e="$MARK_END" '
    $0 == b { skip = 1; next }
    $0 == e { skip = 0; next }
    !skip { print }
  ' "$file" > "$file.smartpowers-tmp"
  mv "$file.smartpowers-tmp" "$file"
}

install_preamble() {
  if [ -z "$GLOBAL_MD" ]; then
    echo "note: no known global-instructions file for this harness." >&2
    echo "      paste preamble/AGENTS.snippet.md into your harness's global instructions." >&2
    return 0
  fi
  mkdir -p "$(dirname "$GLOBAL_MD")"
  touch "$GLOBAL_MD"
  strip_preamble "$GLOBAL_MD"
  {
    echo ""
    echo "$MARK_BEGIN"
    sed "s|__SKILLS_DIR__|$TARGET|g" "$REPO_ROOT/preamble/AGENTS.snippet.md"
    echo "$MARK_END"
  } >> "$GLOBAL_MD"
  echo "preamble installed: $GLOBAL_MD"
}

if [ "$UNINSTALL" -eq 1 ]; then
  if [ -f "$MANIFEST" ]; then
    while IFS= read -r name; do
      [ -n "$name" ] && rm -rf "${TARGET:?}/$name"
    done < "$MANIFEST"
    rm -f "$MANIFEST"
  fi
  strip_preamble "$GLOBAL_MD"
  echo "SmartPowers uninstalled from $TARGET"
  exit 0
fi

# Pre-flight: lint the repo's own skills before installing anything.
if command -v python3 >/dev/null 2>&1; then
  echo "== pre-flight: skill-lint =="
  python3 "$REPO_ROOT/skills/writing-skills/scripts/skill-lint" "$REPO_ROOT/skills"
else
  echo "warning: python3 not found - skipping skill-lint pre-flight" >&2
fi

# Install skills.
mkdir -p "$TARGET"
: > "$MANIFEST"
count=0
for d in "$REPO_ROOT"/skills/*/; do
  name="$(basename "$d")"
  dest="$TARGET/$name"
  if [ "$MODE" = "link" ]; then
    ln -sfn "$d" "$dest"
  else
    rm -rf "$dest"
    cp -R "$d" "$dest"
  fi
  if [ -d "$dest/scripts" ]; then
    find -L "$dest/scripts" -type f -exec chmod +x {} +
  fi
  echo "$name" >> "$MANIFEST"
  count=$((count + 1))
done

install_preamble

# Post-install verification.
missing=0
while IFS= read -r name; do
  [ -n "$name" ] || continue
  [ -e "$TARGET/$name/SKILL.md" ] || { echo "verify: MISSING $TARGET/$name/SKILL.md" >&2; missing=1; }
done < "$MANIFEST"
[ "$missing" -eq 0 ] || { echo "install.sh: verification failed" >&2; exit 2; }

echo ""
echo "SmartPowers installed: $count skills -> $TARGET"
echo "next step: restart your agent session so the preamble and skills load."
