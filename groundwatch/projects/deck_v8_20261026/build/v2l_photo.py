# PV5 실내 사진(Alexander Migl, CC BY-SA 4.0)의 디스플레이에 한국어 '장비 전원(V2L)' 화면을 합성한다.
# 원근 좌표(QUAD)와 화면 톤은 groundwatch/build/ivi_photo.py 와 같다. 수치는 [화면 예시].
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import numpy as np

PHOTO, FONTS, OUT = sys.argv[1:4]
AMBER, GREEN, BLUE = (245, 180, 0), (90, 210, 122), (78, 155, 234)
INK, ROW, MUTE = (12, 21, 36), (19, 34, 56), (138, 151, 171)


def F(size, w="Regular"):
    return ImageFont.truetype(f"{FONTS}/Pretendard-{w}.otf", size)


def screen():
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), (5, 8, 13))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, W - 14, H - 14), 18, fill=INK)
    d.text((46, 62), "장비 전원 · V2L", font=F(34, "Bold"), fill=(255, 255, 255), anchor="ls")
    d.text((W - 46, 62), "04:42   배터리 86%", font=F(24), fill=MUTE, anchor="rs")
    # 왼쪽: 출력 게이지
    d.rounded_rectangle((38, 90, 760, 862), 16, fill=ROW)
    d.text((80, 170), "실내 V2L 출력 중", font=F(32), fill=GREEN, anchor="ls")
    d.text((80, 330), "1.2", font=F(170, "ExtraBold"), fill=(255, 255, 255), anchor="ls")
    d.text((330, 330), "kW", font=F(60, "Bold"), fill=MUTE, anchor="ls")
    d.text((80, 390), "최대 출력 대비 사용량", font=F(26), fill=MUTE, anchor="ls")
    bx0, by0, bx1, by1 = 80, 420, 718, 470
    d.rounded_rectangle((bx0, by0, bx1, by1), 25, fill=(36, 52, 78))
    d.rounded_rectangle((bx0, by0, bx0 + (bx1 - bx0) * 1.2 / 3.6, by1), 25, fill=AMBER)
    d.text((bx1, by1 + 44), "3.6 kW", font=F(26), fill=MUTE, anchor="rs")
    d.line((80, 560, 718, 560), fill=(36, 52, 78), width=2)
    d.text((80, 625), "배터리 하한", font=F(28), fill=MUTE, anchor="ls")
    d.text((718, 625), "30 %에서 자동 차단", font=F(30, "Bold"), fill=(255, 255, 255), anchor="rs")
    d.text((80, 700), "남은 순찰 가능", font=F(28), fill=MUTE, anchor="ls")
    d.text((718, 700), "약 12시간", font=F(30, "Bold"), fill=(255, 255, 255), anchor="rs")
    d.rounded_rectangle((80, 750, 718, 830), 14, fill=(28, 45, 30))
    d.text((399, 790), "시동 없이 장비 운용 · 공회전 0", font=F(28, "Bold"), fill=GREEN, anchor="mm")
    # 오른쪽: 장비별 전력
    px, pw = 790, 772
    items = [("GPR 제어부", "0.45 kW"), ("엣지 AI 컴퓨터", "0.38 kW"), ("작업 조명", "0.20 kW"),
             ("수동 GPR 충전", "0.12 kW"), ("AR 글래스 충전", "0.06 kW")]
    for i, (k, v) in enumerate(items):
        y = 90 + i * 124
        d.rounded_rectangle((px, y, px + pw, y + 108), 12, fill=ROW)
        d.ellipse((px + 28, y + 44, px + 48, y + 64), fill=GREEN)
        d.text((px + 70, y + 54), k, font=F(30), fill=(225, 232, 242), anchor="lm")
        d.text((px + pw - 28, y + 54), v, font=F(34, "Bold"), fill=(255, 255, 255), anchor="rm")
    d.rounded_rectangle((px, 722, px + pw, 862), 16, fill=AMBER)
    d.text((px + pw / 2, 792), "작업 모드 전원 유지", font=F(44, "ExtraBold"), fill=INK, anchor="mm")
    return im


QUAD = [(1341, 482), (1895, 477), (1893, 803), (1322, 794)]  # ivi_photo.py 와 같은 유리면(2400px 기준)


def coeffs(src, dst):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


ph = Image.open(PHOTO).convert("RGB")
if ph.width != 2400:
    ph = ph.resize((2400, round(ph.height * 2400 / ph.width)), Image.LANCZOS)
sc = screen()
c = coeffs([(0, 0), (sc.width, 0), (sc.width, sc.height), (0, sc.height)], QUAD)
warped = sc.transform(ph.size, Image.PERSPECTIVE, c, Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.6))
mask = Image.new("L", sc.size, 255).transform(ph.size, Image.PERSPECTIVE, c, Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8))
glass = ImageChops.screen(warped, ph.point(lambda v: int(v * 0.35)))
out = ph.copy()
out.paste(glass, (0, 0), mask)
# 6장 칸(3:2)에 맞춰 화면 중심으로 자르기
cx, cy, w = 1610, 640, 900
out.crop((cx - w // 2, cy - w // 3, cx + w // 2, cy + w // 3)).save(OUT, quality=93)
print("ok", ph.size)
