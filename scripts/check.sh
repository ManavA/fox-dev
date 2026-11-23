#!/usr/bin/env bash
# Pre-release checks for fox-dev. Run from anywhere: bash scripts/check.sh
set -euo pipefail
cd "$(dirname "$0")/.."
fail=0
for f in .claude-plugin/marketplace.json plugin/.claude-plugin/plugin.json plugin/.codex-plugin/plugin.json; do
  python3 -I -m json.tool "$f" >/dev/null || { echo "invalid JSON: $f"; fail=1; }
done
cmp -s NOTICE.md plugin/NOTICE.md || { echo "plugin/NOTICE.md differs from NOTICE.md"; fail=1; }
cmp -s LICENSE plugin/LICENSE || { echo "plugin/LICENSE differs from LICENSE"; fail=1; }
v1=$(python3 -I -c 'import json;print(json.load(open("plugin/.claude-plugin/plugin.json"))["version"])')
v2=$(python3 -I -c 'import json;print(json.load(open("plugin/.codex-plugin/plugin.json"))["version"])')
v3=$(python3 -I -c 'import json;print(json.load(open(".claude-plugin/marketplace.json"))["plugins"][0]["version"])')
[ "$v1" = "$v2" ] && [ "$v1" = "$v3" ] || { echo "version mismatch: $v1 $v2 $v3"; fail=1; }
grep -q "^## $v1" CHANGELOG.md || { echo "CHANGELOG.md has no entry for $v1"; fail=1; }
for s in plugin/skills/*/SKILL.md; do
  head -5 "$s" | grep -q '^name: ' && head -5 "$s" | grep -q '^description: ' || { echo "missing name or description: $s"; fail=1; }
done
# Machine paths must not ship. Keep any private-name pattern out of this public file; pass it in
# FOXDEV_PRIVATE_RE (an extended regex) to check for those too.
re='/(ho''me|Us''ers)/[A-Za-z]'"${FOXDEV_PRIVATE_RE:+|$FOXDEV_PRIVATE_RE}"
if git grep -nIiE "$re" -- .; then echo "machine paths or private names found"; fail=1; fi
if command -v claude >/dev/null; then
  claude plugin validate . >/dev/null 2>&1 || { echo "claude plugin validate . failed"; fail=1; }
  claude plugin validate ./plugin >/dev/null 2>&1 || { echo "claude plugin validate ./plugin failed"; fail=1; }
fi
[ "$fail" = 0 ] && echo "all checks passed"
exit "$fail"
