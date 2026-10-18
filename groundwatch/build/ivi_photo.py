# PV5 실내 사진(Alexander Migl, CC BY-SA 4.0)의 꺼진 디스플레이에 GroundWatch Patrol 화면을 합성한다.
# 화면 UI 구성은 assets.js의 iviScreen()과 같고, 지도만 실제 OSM 타일(map4d와 같은 다크 처리)로 바꿨다.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageFilter, ImageChops
import numpy as np

PHOTO, MAP, FONTS, OUT = sys.argv[1:5]

AMBER, RED, GREEN, BLUE = (245, 180, 0), (217, 48, 37), (90, 210, 122), (78, 155, 234)
INK, PANEL, ROW, MUTE = (12, 21, 36), (22, 36, 58), (19, 34, 56), (138, 151, 171)


def F(size, w="Regular"):
    return ImageFont.truetype(f"{FONTS}/Pretendard-{w}.otf", size)


# ---------------------------------------------------------------- dark map (map4d 와 같은 톤)
def dark_map():
    m = Image.open(MAP).convert("RGBA")
    bg = Image.new("RGBA", m.size, (255, 255, 255, 255))
    g = Image.alpha_composite(bg, m).convert("L")
    a = np.asarray(g).astype(np.float32) * 2.2 - 470
    g = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return ImageOps.colorize(g, black=(18, 22, 30), white=(165, 180, 205))


ROADS = {  # assets.js ROADS (1300px 썸네일 기준 좌표)
    "A": [(235, 268), (560, 268), (800, 270), (1160, 250)],
    "B": [(800, 95), (797, 250), (790, 380)], "B2": [(790, 380), (775, 480)], "B3": [(775, 480), (755, 600), (725, 760)],
    "C1": [(600, 430), (700, 420), (790, 440)], "C2": [(790, 440), (950, 470), (1160, 470)],
    "D": [(560, 600), (760, 600), (980, 568), (1150, 575)], "F": [(300, 280), (290, 500), (275, 700)],
}


def map_panel(w, h, mode):
    dm = dark_map()
    k = dm.width / 1300
    # 경로가 들어오는 영역(썸네일 좌표)을 패널 비율로 잘라 확대
    x0, x1 = 250, 980
    span_y = (x1 - x0) * h / w
    y0 = 360 - span_y / 2
    crop = dm.crop((int(x0 * k), int(y0 * k), int(x1 * k), int((y0 + span_y) * k))).resize((w, h), Image.LANCZOS)
    s = w / (x1 - x0)
    P = lambda p: ((p[0] - x0) * s, (p[1] - y0) * s)
    d = ImageDraw.Draw(crop)
    lw = max(6, int(w / 110))
    # 배경 도로망: 회색(미조사)으로 옅게
    for key in ROADS:
        d.line([P(p) for p in ROADS[key]], fill=(84, 92, 104), width=lw - 2, joint="curve")
    plan = [(300, 268), (560, 268), (800, 270), (797, 330), (790, 380), (782, 430), (775, 480)]
    done_upto = {"pre": 1, "drive": 3, "stop": 4}[mode]
    d.line([P(p) for p in plan], fill=(255, 255, 255), width=lw + 6, joint="curve")
    d.line([P(p) for p in plan], fill=BLUE, width=lw, joint="curve")
    d.line([P(p) for p in plan[:done_upto + 1]], fill=(59, 165, 92), width=lw, joint="curve")
    pts = [((660, 269), AMBER, "1"), ((798, 300), AMBER, "2"), ((782, 430), RED, "3")]
    r = int(w / 42)
    for (pt, col, lab) in pts:
        x, y = P(pt)
        d.ellipse((x - r, y - r, x + r, y + r), fill=col, outline=INK, width=4)
        d.text((x, y), lab, font=F(int(r * 1.15), "ExtraBold"), fill=(255, 255, 255) if col == RED else INK, anchor="mm")
    vx, vy = P(plan[done_upto])
    d.ellipse((vx - r * 0.75, vy - r * 0.75, vx + r * 0.75, vy + r * 0.75), fill=(255, 255, 255), outline=BLUE, width=5)
    d.text((w - 12, h - 10), "© OpenStreetMap contributors", font=F(14), fill=(120, 128, 140), anchor="rd")
    return crop


# ---------------------------------------------------------------- screen (1600x900, UI 구성은 iviScreen 과 동일)
def screen(mode):
    W, H = 1600, 900
    im = Image.new("RGB", (W, H), (5, 8, 13))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((14, 14, W - 14, H - 14), 18, fill=INK)
    d.text((46, 62), "GroundWatch Patrol", font=F(30, "Bold"), fill=(255, 255, 255), anchor="ls")
    d.text((W - 46, 62), "04:42   배터리 86%", font=F(24), fill=MUTE, anchor="rs")
    mx, my, mw, mh = 38, 90, 900, 772
    mp = map_panel(mw, mh, mode)
    mask = Image.new("L", (mw, mh), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, mw - 1, mh - 1), 14, fill=255)
    im.paste(mp, (mx, my), mask)
    px, pw = 962, 600

    def row(y, k, v, col=(255, 255, 255), h=92):
        d.rounded_rectangle((px, y, px + pw, y + h), 12, fill=ROW)
        d.text((px + 26, y + h / 2), k, font=F(25), fill=MUTE, anchor="lm")
        d.text((px + pw - 26, y + h / 2), v, font=F(32, "Bold"), fill=col, anchor="rm")

    if mode == "pre":
        for i, (k, v, c) in enumerate([("오늘의 기본 순찰거리", "38.4 km", None), ("재확인 포인트", "3곳", AMBER),
                                       ("예상 소요시간", "3시간 10분", None), ("GPR · Edge Gateway", "연결됨", GREEN),
                                       ("AR 글래스 · 저장공간", "92% · 71%", GREEN)]):
            row(90 + i * 106, k, v, c or (255, 255, 255))
        d.rounded_rectangle((px, 632, px + pw, 862), 18, fill=AMBER)
        d.text((px + pw / 2, 747), "순찰 시작", font=F(52, "ExtraBold"), fill=INK, anchor="mm")
    elif mode == "drive":
        for i, (k, v) in enumerate([("스캔 상태", "수집 중"), ("데이터 품질", "양호"), ("GNSS · IMU", "RTK 고정")]):
            row(90 + i * 106, k, v, GREEN)
        d.rounded_rectangle((px, 420, px + pw, 862), 18, fill=ROW)
        d.text((px + 34, 490), "다음 재확인 지점까지", font=F(30), fill=MUTE, anchor="ls")
        d.text((px + 34, 700), "420 m", font=F(150, "ExtraBold"), fill=AMBER, anchor="ls")
        d.text((px + 34, 800), "주행 중에는 화면 조작이 잠깁니다", font=F(24), fill=MUTE, anchor="ls")
    else:
        d.rounded_rectangle((px, 90, px + pw, 250), 14, fill=(58, 18, 22))
        d.text((px + 28, 140), "위험등급", font=F(26), fill=(255, 179, 179), anchor="ls")
        d.text((px + 28, 212), "정밀 재탐사 필요", font=F(50, "ExtraBold"), fill=(255, 255, 255), anchor="ls")
        for i, (k, v, c) in enumerate([("이전 회차 대비", "신규 확대", None), ("변화량 [예시]", "+17%", AMBER), ("추정 깊이 [예시]", "0.9–1.3 m", None)]):
            row(266 + i * 100, k, v, c or (255, 255, 255), h=88)
        d.rounded_rectangle((px, 572, px + 292, 862), 18, fill=ROW)
        d.text((px + 146, 670), "안전 정차 위치", font=F(26), fill=MUTE, anchor="mm")
        d.text((px + 146, 750), "우측 40 m", font=F(40, "ExtraBold"), fill=(255, 255, 255), anchor="mm")
        d.rounded_rectangle((px + 308, 572, px + pw, 862), 18, fill=AMBER)
        d.text((px + 454, 690), "현장 점검 시작", font=F(36, "ExtraBold"), fill=INK, anchor="mm")
        d.text((px + 454, 760), "AR 글래스 연결", font=F(26), fill=(74, 55, 0), anchor="mm")
    return im


# ---------------------------------------------------------------- perspective composite
QUAD = [(1341, 482), (1895, 477), (1893, 803), (1322, 794)]  # TL TR BR BL (2400px 기준 유리면)


def coeffs(src, dst):
    A, B = [], []
    for (x, y), (u, v) in zip(dst, src):
        A += [[x, y, 1, 0, 0, 0, -u * x, -u * y], [0, 0, 0, x, y, 1, -v * x, -v * y]]
        B += [u, v]
    return np.linalg.solve(np.array(A, float), np.array(B, float)).tolist()


def composite(mode):
    ph = Image.open(PHOTO).convert("RGB")
    sc = screen(mode)
    sw, sh = sc.size
    c = coeffs([(0, 0), (sw, 0), (sw, sh), (0, sh)], QUAD)
    warped = sc.transform(ph.size, Image.PERSPECTIVE, c, Image.BICUBIC)
    mask = Image.new("L", (sw, sh), 255).transform(ph.size, Image.PERSPECTIVE, c, Image.BICUBIC).filter(ImageFilter.GaussianBlur(0.8))
    # 실제 화면처럼: 약간 부드럽게, 유리 반사를 옅게 남김
    warped = warped.filter(ImageFilter.GaussianBlur(0.6))
    glass = ImageChops.screen(warped, ph.point(lambda v: int(v * 0.35)))
    out = ph.copy()
    out.paste(glass, (0, 0), mask)
    return out


for mode in ["pre", "drive", "stop"]:
    im = composite(mode)
    im.save(f"{OUT}/ivi_car_{mode}.jpg", quality=92)
    screen(mode).save(f"{OUT}/ivi_screen_{mode}.png")
print("ok")
