# proposal-final 6p 측면 절개 콘셉트 이미지(투명 PNG)에 번호 지시선과 장비 사이드바를 얹어 부록 '장비 배치' 이미지로 만든다.
# 사용: python compose_cutaway.py cutaway.png fonts_dir out.jpg
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, FONTS, OUT = sys.argv[1:4]
F = lambda s, w="Regular": ImageFont.truetype(f"{FONTS}/Pretendard-{w}.otf", s)
CW, CH, SB = 2432, 1360, 400                   # 캔버스, 사이드바 폭
NAVY, INK, WHITE, AMBER, MUTED = (18, 26, 45), (16, 24, 40), (255, 255, 255), (245, 180, 0), (150, 162, 180)

canvas = Image.new("RGB", (CW, CH), (238, 241, 245))
d = ImageDraw.Draw(canvas)
# 바닥 그라데이션
for y in range(CH):
    t = y / CH
    d.line([(SB, y), (CW, y)], fill=tuple(int(a + (b - a) * t) for a, b in zip((246, 248, 250), (222, 226, 232))))
car = Image.open(SRC).convert("RGBA")
k = (CW - SB - 60) / car.width
car = car.resize((round(car.width * k), round(car.height * k)), Image.LANCZOS)
ox, oy = SB + 30, (CH - car.height) // 2 + 40
canvas.paste(car, (ox, oy), car)
P = lambda x, y: (ox + x * k, oy + y * k)      # 원본(1672x941) 좌표 → 캔버스

ITEMS = [  # 번호, 이름, 원본 좌표, 라벨 위치(캔버스)
    (1, "루프 카메라(전·후방)", (622, 157), (1010, 150)),
    (2, "RTK-GNSS 안테나", (997, 112), (1500, 70)),
    (3, "Patrol 업무 앱(운전석)", (404, 380), (640, 330)),
    (4, "Edge Gateway 랙", (720, 320), (1420, 330)),
    (5, "AR 글래스 · RTK 이동국", (1125, 320), (1700, 190)),
    (6, "수동 GPR 카트", (1150, 540), (2050, 1230)),
    (7, "내시경 · 작업 조명", (1365, 290), (2140, 160)),
    (8, "안전장비(조끼·라바콘)", (1395, 440), (2330, 640)),
    (9, "차량형 다채널 GPR(하부)", (1100, 752), (1460, 1270)),
]
for n, _name, (x, y), (lx, ly) in ITEMS:
    ax, ay = P(x, y)
    d.line([(ax, ay), (lx, ly)], fill=WHITE, width=7)
    d.line([(ax, ay), (lx, ly)], fill=INK, width=3)
    d.ellipse((ax - 9, ay - 9, ax + 9, ay + 9), fill=AMBER, outline=INK, width=3)
    d.ellipse((lx - 33, ly - 33, lx + 33, ly + 33), fill=INK, outline=WHITE, width=4)
    d.text((lx, ly + 1), str(n), font=F(38, "Bold"), fill=WHITE, anchor="mm")

# 사이드바
d.rectangle((0, 0, SB, CH), fill=NAVY)
d.text((34, 44), "PV5 GroundWatch", font=F(30, "Bold"), fill=WHITE)
d.text((34, 84), "장비 배치도", font=F(40, "ExtraBold"), fill=WHITE)
d.text((34, 138), "측면 절개 · 콘셉트 이미지", font=F(20), fill=MUTED)
d.line((34, 182, SB - 34, 182), fill=(60, 72, 96), width=2)
d.text((34, 206), "탑재 장비", font=F(24, "Bold"), fill=AMBER)
rh = 112
for i, (n, name, *_r) in enumerate(ITEMS):
    y = 262 + i * rh
    d.ellipse((34, y, 34 + 46, y + 46), outline=(200, 208, 220), width=3)
    d.text((57, y + 24), str(n), font=F(26, "Bold"), fill=WHITE, anchor="mm")
    d.text((96, y + 23), name, font=F(27, "Medium"), fill=(244, 246, 249), anchor="lm")
    if i < len(ITEMS) - 1:
        d.line((34, y + rh - 32, SB - 34, y + rh - 32), fill=(44, 56, 80), width=1)
canvas.save(OUT, quality=92)
print("saved", OUT, canvas.size)
