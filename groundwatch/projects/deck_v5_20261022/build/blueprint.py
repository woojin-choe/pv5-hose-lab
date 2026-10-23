# PV5 실루엣(배치도 원본 외곽)으로 도면용 이미지 2종을 만든다.
#  1) pv5_blueprint.png : 밝은 면 + 남색 외곽선 실루엣(바퀴 자리는 비움, 바퀴는 SVG에서 제원대로 그림)
#  2) cargo_interior.png : 화물칸 내부만 잘라낸 배치 그림(차체 하부·바퀴 제외)
from PIL import Image, ImageFilter, ImageChops
import numpy as np
SRC = "../../images/final_concept/cutaway_side.png"
im = Image.open(SRC).convert("RGBA"); W, H = im.size
SILL = 704
a = np.asarray(im).copy()
mask = (a[..., 3] > 200)
mask[SILL:, :] = False
# 앞바퀴 위쪽 일부가 실루엣에 남지 않도록 휠아치 영역 제거(바퀴는 SVG에서 다시 그림)
yy, xx = np.ogrid[:H, :W]
for cx in (170, 1205):
    mask &= ~(((xx - cx) ** 2 + (yy - 665) ** 2) <= 125 ** 2)
m = Image.fromarray((mask * 255).astype(np.uint8)).filter(ImageFilter.MinFilter(9)).filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(1.0)).point(lambda v: 255 if v > 127 else 0)
# 가장 큰 덩어리만 남김(하부 잔조각 제거): 바닥선(y 690) 아래는 바퀴 사이 차체만 유지
_a = np.asarray(m).copy()
_a[690:, :] = 0
m = Image.fromarray(_a)
edge = ImageChops.subtract(m.filter(ImageFilter.MaxFilter(7)), m)
out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
out.paste((247, 248, 250, 255), (0, 0), m)
out.paste((11, 30, 60, 255), (0, 0), edge)
out.save("images/pv5_blueprint.png")
# 화물칸 내부(랙·장비) 크롭: 원본을 밝은 배경에 합성 후 바닥선 위만
bg = Image.new("RGBA", (W, H), (240, 242, 245, 255))
comp = Image.alpha_composite(bg, im).convert("RGB")
comp.crop((330, 70, 1660, 676)).save("images/cargo_interior.png")
print(comp.crop((330, 70, 1660, 676)).size)
