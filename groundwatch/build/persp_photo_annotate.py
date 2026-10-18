# 생성 AI로 실사화한 3점 투시 절개도 위에 번호 지시선·부품표·표제를 얹는다.
# 사용: python persp_photo_annotate.py render.png anchors.json fonts_dir out.png
# anchors.json 은 GW_CLEAN=1 drawing_persp.py 가 내보낸 SVG 좌표(2400x1350 캔버스)이며,
# 실사화 입력은 그 PNG(1.5배)에서 CROP 영역을 잘라 쓴 것이다(sd_gen.py 와 동일해야 함).
import json, sys
from PIL import Image, ImageDraw, ImageFont

RENDER, ANCH, FONTS, OUT = sys.argv[1:5]
CROP = (1000, 470, 3400, 1820)
im = Image.open(RENDER).convert("RGB")
im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS)
W, H = im.size
d = ImageDraw.Draw(im, "RGBA")
F = lambda s, w="Regular": ImageFont.truetype(f"{FONTS}/Pretendard-{w}.otf", s)


def to_img(x, y):
    return ((x * 1.5 - CROP[0]) / (CROP[2] - CROP[0]) * W, (y * 1.5 - CROP[1]) / (CROP[3] - CROP[1]) * H)


anch = json.load(open(ANCH))
# 라벨 위치(최종 이미지 px). 차체를 가리지 않는 빈 배경 쪽으로 뺀다.
LABEL = {"1": (760, 90), "2": (1500, 70), "3": (2050, 210), "4": (330, 470), "5": (1500, 300),
         "6": (1250, 1230), "7": (2330, 520), "8": (2330, 1260), "9": (1720, 1290)}
INK, WHITE, AMBER = (16, 24, 40), (255, 255, 255), (245, 180, 0)
for n, (x, y, name) in anch.items():
    ax, ay = to_img(x, y)
    lx, ly = LABEL[n]
    d.line([(ax, ay), (lx, ly)], fill=(255, 255, 255, 235), width=7)
    d.line([(ax, ay), (lx, ly)], fill=INK + (255,), width=3)
    d.ellipse((ax - 9, ay - 9, ax + 9, ay + 9), fill=AMBER, outline=INK, width=3)
    r = 34
    d.ellipse((lx - r, ly - r, lx + r, ly + r), fill=INK, outline=WHITE, width=4)
    d.text((lx, ly + 1), n, font=F(40, "Bold"), fill=WHITE, anchor="mm")

# 부품표(좌하단, 반투명 흰 패널)
rows = [(n, v[2]) for n, v in sorted(anch.items(), key=lambda kv: int(kv[0]))]
rh, tw = 50, 470
tx, ty = 36, H - 36 - rh * (len(rows) + 1)
d.rectangle((tx, ty, tx + tw, ty + rh * (len(rows) + 1)), fill=(255, 255, 255, 228), outline=INK, width=2)
d.rectangle((tx, ty, tx + tw, ty + rh), fill=INK)
d.text((tx + 22, ty + rh / 2), "탑재 장비", font=F(26, "Bold"), fill=WHITE, anchor="lm")
for i, (n, name) in enumerate(rows):
    y = ty + rh * (i + 1)
    if i: d.line((tx + 10, y, tx + tw - 10, y), fill=(200, 205, 212), width=1)
    cx = tx + 40
    d.ellipse((cx - 17, y + rh / 2 - 17, cx + 17, y + rh / 2 + 17), fill=INK)
    d.text((cx, y + rh / 2 + 1), n, font=F(22, "Bold"), fill=WHITE, anchor="mm")
    d.text((tx + 74, y + rh / 2), name, font=F(25), fill=INK, anchor="lm")

# 표제(좌상단)
d.text((40, 44), "PV5 GroundWatch 장비 배치도", font=F(40, "ExtraBold"), fill=WHITE, anchor="la")
d.text((40, 100), "3점 투시 · 화물실 우측 절개 · 실사 렌더(제안 이미지)", font=F(26), fill=(225, 230, 236), anchor="la")
im.save(OUT, quality=92)
print("saved", OUT, im.size)
