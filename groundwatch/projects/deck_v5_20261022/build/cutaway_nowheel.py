# 배치도 원본에서 바퀴만 지운다(휠하우스는 어두운 빈 공간으로), 바닥 아래 GPR 배열은 그대로 둔다.
from PIL import Image, ImageDraw, ImageFilter
import numpy as np
im = Image.open("../../images/final_concept/cutaway_side.png").convert("RGBA"); W, H = im.size
FC, SILL = (170, 665), 704
a = np.asarray(im).copy()
yy, xx = np.ogrid[:H, :W]
disk = ((xx - FC[0]) ** 2 + (yy - FC[1]) ** 2) <= 106 ** 2
# 차체 하단선 아래 바퀴 부분 + 바퀴 바닥 그림자: 투명
a[disk & (yy >= SILL)] = 0
# 앞쪽 하부 그림자·잔여물: 차체 하단선 아래, 앞바퀴~차체 중간까지 알파를 부드럽게 0으로
ramp = np.clip((xx - 470) / 140.0, 0, 1)            # x 470 이하 완전 제거, 610까지 서서히
below = (yy > SILL + 2) & (yy < 860)
alpha = a[..., 3].astype(float)
alpha = np.where(below, alpha * np.broadcast_to(ramp, alpha.shape), alpha)
a[..., 3] = alpha.astype(np.uint8)
# 차체 안쪽 휠하우스: 어두운 빈 공간
well = disk & (yy < SILL)
a[well, 0], a[well, 1], a[well, 2], a[well, 3] = 30, 31, 35, 255
im = Image.fromarray(a)
bg = Image.new("RGBA", (W, H), (240, 242, 245, 255))
out = Image.alpha_composite(bg, im).convert("RGB")
out.save("images/cutaway_nowheel.png"); print(out.size)
