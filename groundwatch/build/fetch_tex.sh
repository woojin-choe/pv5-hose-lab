#!/bin/bash
# underground.py가 쓰는 Poly Haven CC0 스캔 텍스처(2K)를 tex/에 받는다
cd "$(dirname "$0")" && mkdir -p tex && cd tex
for a in asphalt_02 rocky_gravel excavated_soil_wall coast_sand_05 brown_mud_02 concrete_floor_02 concrete_slab_wall concrete_pavement; do
  curl -s "https://api.polyhaven.com/files/$a" | python3 -c "
import json,sys;d=json.load(sys.stdin)
for k,n in [('Diffuse','diff'),('nor_gl','nor'),('Rough','rough')]: print(d[k]['2k']['jpg']['url'], '$a'+'_'+n+'.jpg')" |
  while read u f; do [ -f "$f" ] || curl -s -o "$f" "$u"; done
done
