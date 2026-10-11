# images/gen/의 선별 원본(FLUX.2 klein 편집, 실차 사진 기반)을 슬라이드 칸 비율로 잘라 images/f_*.jpg로 저장
# 형식: 출력 이름: (원본, 칸 가로/세로 비율, 초점 x, 초점 y, 확대)
import os, sys
from PIL import Image, ImageEnhance
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images")
JOBS = {
    "f_front_n": ("front_dawn.png", 6.433 / 5.1, 0.0, 0.5, 1.0),   # 1 표지
    "f_front":   ("front_day.png", 4.1 / 2.85, 0.5, 0.5, 1.0),      # 5 솔루션 개요
    "f_int6":    ("lab_open_b.png", 5.933 / 5.1, 0.5, 0.5, 1.12),   # 6 구분장
    "f_rear_n":  ("rear_dawn.png", 7.48 / 4.99, 0.5, 0.5, 1.0),     # 7 새벽 순찰
    "f_int":     ("lab_open.png", 5.4 / 3.04, 0.5, 0.45, 1.0),      # 8 이동형 탐사실
    "f_gpr":     ("gpr_close.png", 2.05 / 3.04, 0.6, 0.6, 1.0),     # 8 후방 하부 GPR
    "f_rear":    ("rear_day.png", 5.933 / 5.1, 0.5, 0.5, 1.0),      # 18 구분장
    "f_front2":  ("street_dawn.png", 6.433 / 5.1, 0.0, 0.5, 1.0),  # 23 맺음말
}
for name in (sys.argv[1:] or JOBS):
    src, ar, fx, fy, z = JOBS[name]
    p = os.path.join(R, "gen", src)
    if not os.path.exists(p): print("skip", name, "(no", src + ")"); continue
    im = Image.open(p).convert("RGB"); W, H = im.size
    h = min(H, W / ar) / z; w = h * ar
    x0 = min(max(fx * W - w / 2, 0), W - w); y0 = min(max(fy * H - h / 2, 0), H - h)
    out = im.crop((round(x0), round(y0), round(x0 + w), round(y0 + h)))
    if out.width < 1400: out = out.resize((1400, round(1400 / ar)), Image.LANCZOS)
    out = ImageEnhance.Sharpness(out).enhance(1.15)
    out.save(os.path.join(R, name + ".jpg"), quality=93); print("saved", name, out.size)
