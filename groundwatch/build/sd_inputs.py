# Stable Diffusion 입력: 실차 사진 + 장비 레이어(글자 없음) → 초기 이미지(낮/새벽)와 Canny 윤곽
import os, numpy as np, cv2
from PIL import Image
import compose as C
OUTD = os.path.join(C.IMG, "sd"); os.makedirs(OUTD, exist_ok=True)
def make(name, src, eq, glow, band_quad):
    base = Image.open(os.path.join(C.PH, src)).convert("RGB").resize((C.W, C.H), Image.LANCZOS)
    base = C.multiply(base, C.warp(C.band_art(1600, 60), band_quad))
    day = Image.alpha_composite(base.convert("RGBA"), Image.open(os.path.join(C.LY, eq)).convert("RGBA")).convert("RGB")
    nt = Image.alpha_composite(C.night(day).convert("RGBA"), Image.open(os.path.join(C.LY, glow)).convert("RGBA")).convert("RGB")
    day.save(os.path.join(OUTD, name + "_day.png")); nt.save(os.path.join(OUTD, name + "_night.png"))
    g = cv2.cvtColor(np.asarray(day), cv2.COLOR_RGB2GRAY); g = cv2.bilateralFilter(g, 9, 50, 50)
    e = cv2.Canny(g, 60, 140); cv2.imwrite(os.path.join(OUTD, name + "_canny.png"), e)
make("front", "pv5_cargo_c.jpg", "eq_front.png", "eq_front_glow.png", [(1004, 692), (1834, 642), (1834, 672), (1004, 724)])
make("rear", "pv5_cargo_d.jpg", "eq_rear.png", "eq_rear_glow.png", [(112, 844), (892, 844), (892, 876), (112, 876)])
print("inputs ok")
