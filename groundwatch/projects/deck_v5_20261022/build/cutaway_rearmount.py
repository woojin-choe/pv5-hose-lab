# 컷어웨이 보정: 차체 아랫선 밑을 깨끗한 배경·그림자로 다시 깔고, 앞·뒷바퀴와 후방 하부 GPR만 올린다.
# (원본은 뒷바퀴가 없고 GPR 배열이 배터리 구간 아래에 있어 설명과 어긋났음)
import sys
from PIL import Image, ImageDraw, ImageFilter, ImageChops
BG = (240, 242, 245, 255)
src = Image.open("../../images/final_concept/cutaway_side.png").convert("RGBA")
W, H = src.size
flat = Image.new("RGBA", (W, H), BG); flat.alpha_composite(src)
RCX = int(sys.argv[1]) if len(sys.argv) > 1 else 1195
dst = sys.argv[2] if len(sys.argv) > 2 else "images/cutaway_rearmount.png"
FLOOR, CUT = 606, 690

# GPR 두 모듈+지지대(배경·그림자는 테두리에서 채워 걷어 냄)
gc = flat.crop((1160, 686, 1470, 800)).convert("RGB")
key = (255, 0, 255)
for x in range(gc.size[0]):
    ImageDraw.floodfill(gc, (x, gc.size[1] - 1), key, thresh=28)
for y in range(gc.size[1]):
    for x in (0, gc.size[0] - 1):
        if gc.getpixel((x, y)) != key:
            ImageDraw.floodfill(gc, (x, y), key, thresh=28)
gpr = gc.convert("RGBA")
gpr.putalpha(ImageChops.difference(gc, Image.new("RGB", gc.size, key)).convert("L").point(lambda v: 255 if v > 8 else 0).filter(ImageFilter.MinFilter(3)))

# 바퀴(앞바퀴 원형 크롭)
FC, R = (167, 662), 101
def wheel(top_clip):
    m = Image.new("L", (2 * R, 2 * R), 0)
    ImageDraw.Draw(m).ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
    if top_clip:
        ImageDraw.Draw(m).rectangle((0, 0, 2 * R, top_clip), fill=0)
    w = flat.crop((FC[0] - R, FC[1] - R, FC[0] + R, FC[1] + R)); w.putalpha(m.filter(ImageFilter.GaussianBlur(0.8))); return w

# 1) 차체 아랫선 밑을 배경으로
out = flat.copy()
ImageDraw.Draw(out).rectangle((0, CUT, W, H), fill=BG)
out.paste(flat.crop((1480, CUT, W, 714)), (1480, CUT))   # 뒷범퍼 아랫입술 복원
ImageDraw.Draw(out).rectangle((1480, 714, W, H), fill=BG)
# 2) 그림자: 차체 아래 넓게 + 바퀴 접지
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
d.rectangle((60, CUT, 1620, CUT + 34), fill=(0, 0, 0, 70))
d.ellipse((40, 735, 1650, 795), fill=(0, 0, 0, 60))
for cx in (FC[0], RCX):
    d.ellipse((cx - 105, 750, cx + 105, 776), fill=(0, 0, 0, 140))
out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)))
# 3) 바퀴·GPR 올리기
out.alpha_composite(wheel(0), (FC[0] - R, FC[1] - R))
out.alpha_composite(Image.new("RGBA", (2 * R + 24, 16), (22, 24, 28, 255)), (RCX - R - 12, FLOOR - 4))
out.alpha_composite(wheel(FLOOR - (662 - R)), (RCX - R, 662 - R))
# 모듈 바닥이 접지선(약 763)보다 위에 오도록 줄여서 범퍼 아래에 단다
bb = gpr.getbbox(); gpr = gpr.crop(bb)
SC = 0.62
gpr = gpr.resize((int(gpr.size[0] * SC), int(gpr.size[1] * SC)), Image.LANCZOS)
gx, gy = RCX + R + 22, 692
sh2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(sh2).ellipse((gx - 10, 752, gx + gpr.size[0] + 10, 772), fill=(0, 0, 0, 90))
out.alpha_composite(sh2.filter(ImageFilter.GaussianBlur(6)))
out.alpha_composite(gpr, (gx, gy))
print("gpr bottom", gy + gpr.size[1])
out.convert("RGB").save(dst)
print("ok", RCX, gx, gx + gpr.size[0])
