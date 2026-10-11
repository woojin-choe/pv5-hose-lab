#!/bin/bash
cd "$(dirname "$0")"
export GW_FONT=$PWD/../fonts/Pretendard-Bold.otf SAMPLES=${SAMPLES:-160}
for v in ${@:-front night rear interior cutaway}; do
  /Applications/Blender.app/Contents/MacOS/Blender -b -P pv5_scene.py -- $PWD/../images/3d/$v.png $v 2>&1 | grep -E "RENDERED|Error|Traceback|glare"
done
