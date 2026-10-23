# 배치도 원본(cutaway_side.png)은 뒷바퀴 자리에 GPR 배열이 그려져 있다.
# 뒷바퀴를 차체 비율 위치에 휠하우스와 함께 넣고, GPR 배열은 앞뒤 바퀴 사이 바닥 아래로 옮긴다.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
SRC = "../../images/final_concept/cutaway_side.png"
im = Image.open(SRC).convert("RGBA"); W, H = im.size
FC, R = (170, 665), 101              # 앞바퀴 중심·타이어 반지름(측정값)
RC = (1205, 665)                     # 뒷바퀴: 앞바퀴 + 휠베이스(차체 길이 비율 2,995/4,695)
SILL = 704                           # 차체 하단선
array = im.crop((880, 648, 1500, 800))            # GPR 배열 원본
# 1) 원래 배열·그림자 지우기(차체 하단선 아래만)
a = np.asarray(im).copy()
a[SILL:860, 860:1520, 3] = 0
im = Image.fromarray(a)
# 2) 휠하우스: 차체에 파인 어두운 아치 + 검은 휀더 테두리
well = Image.new("L", (W, H), 0); d = ImageDraw.Draw(well)
d.ellipse((RC[0] - 128, RC[1] - 128, RC[0] + 128, RC[1] + 128), fill=255)
d.rectangle((0, SILL + 2, W, H), fill=0)
body = Image.fromarray((np.asarray(im)[..., 3] > 200).astype(np.uint8) * 255)
flare = Image.composite(well, Image.new("L", (W, H), 0), body)
im = Image.composite(Image.new("RGBA", (W, H), (44, 45, 48, 255)), im, flare.filter(ImageFilter.GaussianBlur(0.8)))
inner = Image.new("L", (W, H), 0); di = ImageDraw.Draw(inner)
di.ellipse((RC[0] - 112, RC[1] - 112, RC[0] + 112, RC[1] + 112), fill=255); di.rectangle((0, SILL + 2, W, H), fill=0)
im = Image.composite(Image.new("RGBA", (W, H), (20, 21, 24, 255)), im, inner.filter(ImageFilter.GaussianBlur(1.2)))
# 3) 바닥 그림자
sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
ds.ellipse((RC[0] - 120, RC[1] + R - 14, RC[0] + 120, RC[1] + R + 14), fill=(0, 0, 0, 120))
ds.ellipse((560, 800, 1100, 830), fill=(0, 0, 0, 70))
im = Image.alpha_composite(sh.filter(ImageFilter.GaussianBlur(10)), im)
# 4) 앞바퀴를 그대로 복제해 뒷바퀴로
tire = im.crop((FC[0] - R, FC[1] - R, FC[0] + R, FC[1] + R))
m = Image.new("L", tire.size, 0); ImageDraw.Draw(m).ellipse((1, 1, 2 * R - 1, 2 * R - 1), fill=255)
im.paste(tire, (RC[0] - R, RC[1] - R), m.filter(ImageFilter.GaussianBlur(0.7)))
# 5) GPR 배열을 바퀴 사이로(뒷바퀴 앞 30px까지)
s = 0.86
arr = array.resize((int(array.width * s), int(array.height * s)), Image.LANCZOS)
x1 = RC[0] - 128 - 30; x0 = x1 - arr.width
im.alpha_composite(arr, (x0, SILL - int(56 * s)))
# 6) 밝은 배경에 합성
bg = Image.new("RGBA", (W, H), (240, 242, 245, 255))
out = Image.alpha_composite(bg, im).convert("RGB")
out.save("images/cutaway_pv5.png"); print("ok", x0, x1)
