#!/bin/bash
# 에셋 → PPTX → (PowerPoint) PDF → 슬라이드 PNG
set -e
cd "$(dirname "$0")"
ROOT="$(cd .. && pwd)"
export PPTX_SKILL=${PPTX_SKILL:-$HOME/.claude/skills/synced/48cfeb08-ee00-46ed-b391-3f9cae2ee764_5d520355-d1f3-496b-b50b-f5a257054f70/pptx}
export NODE_PATH="$PWD/node_modules"
[ "$1" = "--skip-assets" ] || node assets.js
node deck.js
rm -f "$ROOT/PV5_GroundWatch.pdf"
osascript <<OSA
tell application "Microsoft PowerPoint"
  open POSIX file "$ROOT/PV5_GroundWatch.pptx"
  delay 3
  set p to active presentation
  save p in POSIX file "$ROOT/PV5_GroundWatch.pdf" as save as PDF
  close p saving no
end tell
OSA
rm -f "$ROOT"/renders/slide-*.png
${PY:-python3} - "$ROOT" <<'PYEOF'
import sys, pymupdf
root = sys.argv[1]
d = pymupdf.open(f"{root}/PV5_GroundWatch.pdf")
for i, p in enumerate(d):
    p.get_pixmap(dpi=144).save(f"{root}/renders/slide-{i+1:02d}.png")
print("pages", len(d))
PYEOF
