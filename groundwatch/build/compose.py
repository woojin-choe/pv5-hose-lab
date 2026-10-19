# PV5 실차 사진 + 원근 랩핑(곱하기 합성) + 장비 레이어 + 새벽 그레이딩 → 장착 예상도
import os, numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.join(os.path.dirname(__file__), "..")
IMG = os.path.join(ROOT, "images"); PH = os.path.join(IMG, "photos"); LY = os.path.join(IMG, "layers")
FB = os.path.join(ROOT, "fonts", "Pretendard-Bold.otf"); FM = os.path.join(ROOT, "fonts", "Pretendard-Medium.otf")
W, H = 1920, 1278
PORT = {"gw_front": 330, "gw_rear": 60}
NAVY, AMBER = (16, 38, 74), (232, 168, 20)

def coeffs(dst, src):
    # dst 사변형 → src 직사각형 역변환 계수(PIL PERSPECTIVE)
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]; B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()

def warp(art, quad):
    w, h = art.size
    return art.transform((W, H), Image.PERSPECTIVE, coeffs(quad, [(0, 0), (w, 0), (w, h), (0, h)]), Image.BICUBIC)

def text_art(title, sub, w, h, tsize, ssize):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.text((0, 0), title, font=ImageFont.truetype(FB, tsize), fill=NAVY + (255,))
    d.text((4, int(tsize * 1.18)), sub, font=ImageFont.truetype(FM, ssize), fill=(60, 72, 92, 255))
    return im

def band_art(w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    a = int(h * 0.22); d.rectangle([0, 0, w, a], fill=AMBER + (255,)); d.rectangle([0, a + int(h * 0.08), w, h], fill=NAVY + (255,))
    return im

def sign_art(w, h, text):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=8, fill=(255, 236, 170, 255), outline=AMBER + (255,), width=5)
    f = ImageFont.truetype(FB, int(h * 0.48)); tw = d.textlength(text, font=f)
    d.text(((w - tw) / 2, h * 0.2), text, font=f, fill=(70, 50, 0, 255))
    return im

def multiply(base, layer):
    # 차체 음영·반사가 랩핑 위로 비치도록 곱하기 합성 + 미세 블러
    layer = layer.filter(ImageFilter.GaussianBlur(0.7))
    b = np.asarray(base, float) / 255; l = np.asarray(layer, float) / 255
    a = l[..., 3:4]; col = l[..., :3]
    lum = b.mean(axis=2, keepdims=True)
    shade = np.clip(lum / 0.86, 0, 1.08)          # 흰 차체 기준 음영 비율
    mixed = col * shade + 0.06 * b                # 반사 일부 유지
    a = a * np.clip((lum - 0.42) / 0.16, 0, 1)   # 흰 차체 위에만(검은 클래딩·유리 제외)
    out = b * (1 - a) + np.clip(mixed, 0, 1) * a
    return Image.fromarray((out * 255).astype(np.uint8))

def night(img):
    a = np.asarray(img, float) / 255
    g = a.mean(axis=2, keepdims=True)
    a = a * 0.4 + g * 0.6
    a = a * 0.42 * np.array([0.78, 0.9, 1.25])
    y = np.linspace(0, 1, H)[:, None, None]
    a = a * (0.55 + 0.45 * np.clip((y - 0.05) / 0.5, 0, 1)) * (1 - 0.3 * np.clip((y - 0.8) / 0.2, 0, 1))
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))

def build(name, src, livery, eq, glow, crop_top):
    base = Image.open(os.path.join(PH, src)).convert("RGB").resize((W, H), Image.LANCZOS)
    for art, quad in livery: base = multiply(base, warp(art, quad))
    eqL = Image.open(os.path.join(LY, eq)).convert("RGBA")
    day = base.copy(); day.alpha_composite if False else None
    day = Image.alpha_composite(base.convert("RGBA"), eqL).convert("RGB")
    nt = night(day).convert("RGBA")
    nt = Image.alpha_composite(nt, Image.open(os.path.join(LY, glow)).convert("RGBA")).convert("RGB")
    for img, suf in [(day, ""), (nt, "_n")]:
        img.save(os.path.join(IMG, f"{name}{suf}.jpg"), quality=92)
        img.crop((0, crop_top, W, crop_top + 1080)).save(os.path.join(IMG, f"{name}{suf}_169.jpg"), quality=92)
        img.crop((PORT[name], 0, PORT[name] + 1180, H)).save(os.path.join(IMG, f"{name}{suf}_port.jpg"), quality=92)

# 차체 측면 'GroundWatch' 문구는 넣지 않음(2026-10-18 결정). 띠 래핑만 유지
front_liv = [
    (band_art(1600, 60), [(1004, 692), (1834, 642), (1834, 672), (1004, 724)]),
]
rear_liv = [
    (band_art(1600, 60), [(112, 844), (892, 844), (892, 876), (112, 876)]),
    (sign_art(460, 84, "저속 탐사 차량"), [(522, 734), (750, 734), (750, 778), (522, 778)]),
]
if __name__ == "__main__": build("gw_front", "pv5_cargo_c.jpg", front_liv, "eq_front.png", "eq_front_glow.png", 120)
if __name__ == "__main__": build("gw_rear", "pv5_cargo_d.jpg", rear_liv, "eq_rear.png", "eq_rear_glow.png", 190)
if __name__ == "__main__": print("composed")
