# PV5 GroundWatch 장비 배치도: 3점 투시 선화(뒤-오른쪽 위에서 내려다본 시점, 화물실 우측 절개)
# 차량 치수 = 기아 공식 제원(PV5 카고 롱: 전장 4,695 / 전폭 1,895 / 전고 1,905 / 휠베이스 2,995). 형상은 실차 사진 기준 근사.
# 좌표계(mm): x = 후단 0 → 전단 4,695, y = 차량 중심 0(+는 차량 오른쪽), z = 지면 0 → 위.
# 사용: python3 drawing_persp.py out.png fonts_dir
import math, os, subprocess, sys, tempfile

OUT, FONTS = sys.argv[1], sys.argv[2]
CLEAN = os.environ.get("GW_CLEAN") == "1"   # 1이면 주석 없이 실사 생성용 베이스 이미지만
CW, CH = 2400, 1350
K, G, L, P, ACC, BLUE = "#1B1F24", "#6E7680", "#B8BEC6", "#9AA3AE", "#C9861A", "#2C5A8C"
EQ, EQ_SIDE, EQ_TOP = "#E4EDF7", "#D3E0EE", "#EEF4FA"

# ---------------------------------------------------------------- 카메라(아래로 기울여 세로선도 소실 → 3점 투시)
CAM = (-3400.0, 9400.0, 5600.0)
TGT = (2200.0, 0.0, 800.0)
FOCAL = 1.0


def sub(a, b): return (a[0] - b[0], a[1] - b[1], a[2] - b[2])
def dot(a, b): return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
def cross(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def norm(a):
    l = math.sqrt(dot(a, a)); return (a[0] / l, a[1] / l, a[2] / l)


FWD = norm(sub(TGT, CAM))
RIGHT = norm(cross(FWD, (0, 0, 1)))
UP = cross(RIGHT, FWD)


def cam(p):
    d = sub(p, CAM)
    return dot(d, RIGHT), dot(d, UP), dot(d, FWD)


def proj_raw(p):
    x, y, z = cam(p)
    return (FOCAL * x / z, -FOCAL * y / z)


# ---------------------------------------------------------------- 모델
W2 = 947.5
PROFILE = [(30, 330), (0, 420), (0, 1800), (40, 1880), (140, 1905), (3260, 1905), (3380, 1890), (3470, 1840), (4230, 1205), (4520, 1110),
           (4640, 1060), (4690, 980), (4695, 420), (4660, 330), (4380, 300), (4370, 300), (4360, 560), (4300, 690), (3390, 690), (3330, 560),
           (3320, 300), (1375, 300), (1365, 560), (1305, 690), (395, 690), (335, 560), (325, 300)]
area = sum(PROFILE[i][0] * PROFILE[(i + 1) % len(PROFILE)][1] - PROFILE[(i + 1) % len(PROFILE)][0] * PROFILE[i][1] for i in range(len(PROFILE))) / 2
CCW = area > 0

faces = []   # dict(pts3d, normal, fill, stroke, w, kind, dash, extra)


def face(pts, n, fill="#fff", stroke=K, w=1.6, kind="body", dash=None):
    if CLEAN: stroke, w = ("#4A4F57" if stroke == K else stroke), w * 0.45
    faces.append(dict(pts=pts, n=n, fill=fill, stroke=stroke, w=w, kind=kind, dash=dash))


LIGHT = norm((-0.35, 0.55, 0.75))


def shade(n, base=(255, 255, 255), lo=0.86):
    k = lo + (1 - lo) * max(0.0, dot(n, LIGHT))
    return "#%02X%02X%02X" % tuple(int(c * k) for c in base)


# 차체 측면 2장
face([(x, W2, z) for x, z in PROFILE], (0, 1, 0), kind="side_r")
face([(x, -W2, z) for x, z in PROFILE], (0, -1, 0), kind="side_l")
# 차체 둘레 띠(프로필 외곽선을 전폭으로 밀어낸 면)
for i in range(len(PROFILE)):
    (x0, z0), (x1, z1) = PROFILE[i], PROFILE[(i + 1) % len(PROFILE)]
    dx, dz = x1 - x0, z1 - z0
    n = (dz, 0, -dx) if CCW else (-dz, 0, dx)
    ln = math.hypot(n[0], n[2]) or 1
    n = (n[0] / ln, 0, n[2] / ln)
    glass = 3470 <= x0 <= 4230 and 3470 <= x1 <= 4230
    face([(x0, -W2, z0), (x1, -W2, z1), (x1, W2, z1), (x0, W2, z0)], n,
         fill=("#2B3440" if CLEAN else "url(#hatch)") if glass else shade(n), kind="strip")


def box(x0, x1, y0, y1, z0, z1, fill=EQ, stroke=BLUE, w=1.3, kind="eq", dash=None, shaded=True):
    cols = {(-1, 0, 0): fill, (1, 0, 0): fill, (0, -1, 0): fill, (0, 1, 0): fill, (0, 0, -1): fill, (0, 0, 1): fill}
    if shaded and fill.startswith("#"):
        base = tuple(int(fill[i:i + 2], 16) for i in (1, 3, 5))
        cols = {n: shade(n, base, 0.8) for n in cols}
    face([(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)], (-1, 0, 0), cols[(-1, 0, 0)], stroke, w, kind, dash)
    face([(x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)], (1, 0, 0), cols[(1, 0, 0)], stroke, w, kind, dash)
    face([(x0, y0, z0), (x0, y0, z1), (x1, y0, z1), (x1, y0, z0)], (0, -1, 0), cols[(0, -1, 0)], stroke, w, kind, dash)
    face([(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)], (0, 1, 0), cols[(0, 1, 0)], stroke, w, kind, dash)
    face([(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)], (0, 0, -1), cols[(0, 0, -1)], stroke, w, kind, dash)
    face([(x0, y0, z1), (x0, y1, z1), (x1, y1, z1), (x1, y0, z1)], (0, 0, 1), cols[(0, 0, 1)], stroke, w, kind, dash)


def wheel(cx, side):
    r, n = 343, 28
    yo, yi = (side * 965, side * 745)
    ring = [(cx + r * math.cos(2 * math.pi * k / n), r * math.sin(2 * math.pi * k / n) + 343) for k in range(n)]
    face([(x, yo, z) for x, z in ring], (0, side, 0), fill="#2A2F36", stroke=K, w=1.6, kind="wheel")
    for k in range(n):
        (xa, za), (xb, zb) = ring[k], ring[(k + 1) % n]
        mx, mz = (xa + xb) / 2 - cx, (za + zb) / 2 - 343
        ln = math.hypot(mx, mz)
        face([(xa, yi, za), (xb, yi, zb), (xb, yo, zb), (xa, yo, za)], (mx / ln, 0, mz / ln), fill="#3A4048", stroke="#1B1F24", w=0.6, kind="wheel")
    rim = [(cx + 215 * math.cos(2 * math.pi * k / n), 215 * math.sin(2 * math.pi * k / n) + 343) for k in range(n)]
    face([(x, yo + side * 2, z) for x, z in rim], (0, side, 0), fill="#E9ECF0", stroke=K, w=1.2, kind="rim")


for cx in (850, 3845):
    for sd in (1, -1):
        n0 = len(faces); wheel(cx, sd)
        for f in faces[n0:]: f["layer"] = "wheel_near" if sd == 1 else "wheel_far"

# 외부 장비
_n_ext = len(faces)
box(3150, 3340, -95, 95, 1905, 1975, fill="#2A2E33" if CLEAN else EQ, kind="eq_ext")                                        # 1 전방 카메라 포드
box(2320, 2570, -600, 600, 1905, 1945, fill="#FFFFFF", stroke=K, kind="eq_ext")             # 2 경광등 베이스
box(2340, 2550, -580, 580, 1945, 1995, fill="#F2A41C" if CLEAN else "#F6E3BE", stroke=ACC, kind="eq_ext")           #   렌즈
box(560, 590, 560, 590, 1905, 1960, fill="#FFFFFF", stroke=K, kind="eq_ext")                # 3 GNSS 마스트
box(3480, 3570, 1040, 1100, 1310, 1370, fill="#2A2E33" if CLEAN else EQ, kind="eq_ext")                                     # 4 측면 카메라(오른쪽)
box(3440, 3560, W2, 1100, 1130, 1310, fill="#FFFFFF", stroke=K, kind="eq_ext")              #   미러
box(3440, 3560, -1100, -W2, 1130, 1310, fill="#FFFFFF", stroke=K, kind="eq_ext")
box(-40, 600, -900, 900, 80, 160, fill="#3A3E44" if CLEAN else EQ, kind="eq_ext", stroke=K, w=1.5)                           # 8 후방 하부 GPR 어레이
for bx in (80, 520):
    for by in (-700, 640):
        box(bx, bx + 30, by, by + 60, 160, 330, fill="#FFFFFF", stroke=K, w=1, kind="eq_ext")
box(800, 900, 955, 990, 293, 393, fill="#FFFFFF", stroke=K, w=1.2, kind="eq_ext")           # 9 휠 인코더
for f in faces[_n_ext:]:
    zs = [p[2] for p in f["pts"]]; ys = [p[1] for p in f["pts"]]
    if max(zs) <= 335: f["layer"] = "under"          # GPR 어레이·브래킷
    elif max(ys) <= -W2 + 1: f["layer"] = "wheel_far"   # 반대편 미러: 차체 뒤로
    elif min(ys) >= W2 - 1: f["layer"] = "outside"   # 미러·측면 카메라·인코더
    else: f["layer"] = "roof"
for f in faces:
    f.setdefault("layer", "body")

# 내부(절개부로 보이는 것)
interior = []


def ibox(*a, **k):
    n0 = len(faces); box(*a, **k)
    interior.extend(faces[n0:]); del faces[n0:]


ibox(2120, 2400, -760, -420, 419, 1560, fill="#1F2328" if CLEAN else EQ)                                                   # 5 Edge Gateway 랙
ibox(1450, 1970, 220, 700, 419, 560, fill="#E2661C" if CLEAN else EQ)                                                      # 6 수동 GPR 카트 본체
ibox(1880, 1940, 400, 520, 560, 1100, fill="#2A2E33" if CLEAN else EQ)                                                     #   손잡이
ibox(200, 1250, -760, -420, 760, 1300, fill="#8E949B" if CLEAN else EQ)                                                    # 7 후방 장비 수납장
ibox(200, 1250, -782, -430, 419, 690, fill="#F1F2F4", stroke=P, w=1, shaded=False)        #   휠하우스

CUT = (240, 2330, 600, 1760)   # 화물실 우측 절개창 x0, x1, z0, z1

# ---------------------------------------------------------------- 투영 및 화면 맞춤
allp = [p for f in faces for p in f["pts"]] + [p for f in interior for p in f["pts"]]
raw = [proj_raw(p) for p in allp]
minx, maxx = min(p[0] for p in raw), max(p[0] for p in raw)
miny, maxy = min(p[1] for p in raw), max(p[1] for p in raw)
AX0, AX1, AY0, AY1 = 640, 2300, 300, 1170       # 그림이 들어갈 영역
sc = min((AX1 - AX0) / (maxx - minx), (AY1 - AY0) / (maxy - miny))
ox = AX0 + ((AX1 - AX0) - (maxx - minx) * sc) / 2 - minx * sc
oy = AY0 + ((AY1 - AY0) - (maxy - miny) * sc) / 2 - miny * sc


def PJ(p):
    u, v = proj_raw(p)
    return (ox + u * sc, oy + v * sc)


def depth(f):
    return sum(cam(p)[2] for p in f["pts"]) / len(f["pts"])


def visible(f):
    c = tuple(sum(p[i] for p in f["pts"]) / len(f["pts"]) for i in range(3))
    return dot(f["n"], sub(CAM, c)) > 0


svg = []
add = svg.append


def pts_str(pts): return " ".join(f"{x:.1f},{y:.1f}" for x, y in (PJ(p) for p in pts))


def draw_face(f, extra=""):
    dash = f' stroke-dasharray="{f["dash"]}"' if f["dash"] else ""
    add(f'<polygon points="{pts_str(f["pts"])}" fill="{f["fill"]}" stroke="{f["stroke"]}" stroke-width="{f["w"]}" stroke-linejoin="round"{dash} {extra}/>')


def pline(pts3, stroke=K, w=1.0, dash=None, close=False, fill="none"):
    tag = "polygon" if close else "polyline"
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<{tag} points="{pts_str(pts3)}" fill="{fill}" stroke="{stroke}" stroke-width="{w}" stroke-linejoin="round" stroke-linecap="round"{d}/>')


def text(x, y, t, size=14, w=400, c=K, a="start"):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="Pretendard" font-size="{size}" font-weight="{w}" fill="{c}" text-anchor="{a}">{t}</text>')


add('<defs><pattern id="hatch" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#AEB9C6" stroke-width="1"/></pattern>'
    '<pattern id="scan" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="8" stroke="#E2B65C" stroke-width="1.2"/></pattern>'
    f'<clipPath id="cut"><polygon points="{pts_str([(CUT[0], W2, CUT[2]), (CUT[1], W2, CUT[2]), (CUT[1], W2, CUT[3]), (CUT[0], W2, CUT[3])])}"/></clipPath></defs>')
add(f'<rect width="{CW}" height="{CH}" fill="{"#7D8187" if CLEAN else "#fff"}"/>')
if not CLEAN:
    add(f'<rect x="24" y="24" width="{CW - 48}" height="{CH - 48}" fill="none" stroke="{K}" stroke-width="1.6"/>')

# 소실점 보조선(옅게): 차체 모서리 연장
def vp_guides():
    edges = [((0, W2, 1905), (3260, W2, 1905)), ((0, W2, 330), (4695, W2, 330)),
             ((0, -W2, 1905), (0, W2, 1905)), ((0, -W2, 420), (0, W2, 420)),
             ((0, W2, 420), (0, W2, 1800)), ((3260, W2, 690), (3260, W2, 1905))]
    for a, b in edges:
        pa, pb = PJ(a), PJ(b)
        dx, dy = pb[0] - pa[0], pb[1] - pa[1]
        ln = math.hypot(dx, dy)
        ext = 260
        add(f'<line x1="{pa[0] - dx / ln * ext:.1f}" y1="{pa[1] - dy / ln * ext:.1f}" x2="{pb[0] + dx / ln * ext:.1f}" y2="{pb[1] + dy / ln * ext:.1f}" stroke="#E3E6EA" stroke-width="1" stroke-dasharray="3 6"/>')


if not CLEAN:
    vp_guides()

# 지면 그림자, GPR 탐사 폭
pline([(-150, -1050, 0), (4800, -1050, 0), (4800, 1050, 0), (-150, 1050, 0)], stroke="none", close=True, fill="#55595F" if CLEAN else "#F2F3F5")
pline([(-40, -900, 0), (600, -900, 0), (600, 900, 0), (-40, 900, 0)], stroke=ACC, w=1, dash="6 4", close=True, fill="url(#scan)")

# 그리는 순서 고정: 먼 바퀴 → 하부 장비 → 차체 둘레 → (절개 내부 + 오른쪽 측면) → 가까운 바퀴 → 외측 장비 → 루프 장비
ORDER = {"wheel_far": 0, "under": 1, "body": 2, "side": 3, "wheel_near": 4, "outside": 5, "roof": 6}
def rank(f):
    if f["kind"] == "side_r": return 3
    if f["kind"] == "rim" and f["layer"] == "wheel_near": return 4.5
    return ORDER[f["layer"]]
vis = sorted([f for f in faces if visible(f)], key=lambda f: (rank(f), -depth(f)))
for f in vis:
    if f["kind"] == "side_r":
        # 절개창 안쪽: 바닥, 왼쪽 벽, 격벽, 내부 장비(절개창으로 클립)
        add('<g clip-path="url(#cut)">')
        pline([(160, -782, 419), (2415, -782, 419), (2415, -782, 1820), (160, -782, 1820)], stroke=P, w=1, close=True, fill="#C8AE84" if CLEAN else "#F4F5F7")
        pline([(160, -782, 419), (2415, -782, 419), (2415, W2, 419), (160, W2, 419)], stroke=P, w=1, close=True, fill="#9C7A4E" if CLEAN else "#E9EBEE")
        pline([(2415, -782, 419), (2415, W2, 419), (2415, W2, 1820), (2415, -782, 1820)], stroke=P, w=1, close=True, fill="#BFA47A" if CLEAN else "#EDEFF2")
        for x in range(400, 2415, 300):
            pline([(x, -782, 419), (x, W2, 419)], stroke="#D8DBE0", w=0.8)
        for g in sorted([q for q in interior if visible(q)], key=depth, reverse=True):
            draw_face(g)
        for wx in (1520, 1900):   # 카트 바퀴(원근 반지름 = 투영된 50mm)
            c = PJ((wx, 700, 470)); r_ = abs(PJ((wx + 50, 700, 470))[0] - c[0]) + abs(PJ((wx, 700, 520))[1] - c[1])
            add(f'<circle cx="{c[0]:.1f}" cy="{c[1]:.1f}" r="{max(4, r_ * 0.7):.1f}" fill="#fff" stroke="{BLUE}" stroke-width="1.2"/>')
        add('</g>')
        # 측면 패널(절개창 구멍)
        outer = pts_str(f["pts"])
        hole = pts_str([(CUT[0], W2, CUT[2]), (CUT[0], W2, CUT[3]), (CUT[1], W2, CUT[3]), (CUT[1], W2, CUT[2])])
        def to_path(s):
            ps = s.split(" "); return "M " + " L ".join(ps) + " Z"
        add(f'<path d="{to_path(outer)} {to_path(hole)}" fill="#FFFFFF" fill-rule="evenodd" stroke="{K}" stroke-width="{1.0 if CLEAN else 2.2}" stroke-linejoin="round"/>')
        # 측면 디테일: 클래딩, 도어선, 창, 손잡이, 캐릭터 라인
        pline([(1365, W2, 560), (3330, W2, 560)], w=1.2); pline([(0, W2, 560), (335, W2, 560)], w=1.2); pline([(4360, W2, 560), (4695, W2, 560)], w=1.2)
        pline([(1375, W2, 300), (3320, W2, 300), (3330, W2, 560), (1365, W2, 560)], stroke="none", close=True, fill="#3A3F46" if CLEAN else "url(#hatch)")
        pline([(3060, W2, 1190), (3060, W2, 1790), (3380, W2, 1820), (3460, W2, 1790), (4200, W2, 1215)], w=1.3, close=True, fill="#2B3440" if CLEAN else "url(#hatch)")
        pline([(3330, W2, 1810), (3330, W2, 1195)], w=2.2)
        pline([(2010, W2, 1860), (2010, W2, 560)], w=1); pline([(3040, W2, 1860), (3040, W2, 560)], w=1)
        pline([(2700, W2, 1190), (2860, W2, 1100), (3060, W2, 1100)], stroke=L)
        pline([(2830, W2, 1130), (2970, W2, 1130), (2970, W2, 1158), (2830, W2, 1158)], close=True)
        # 절개면 테두리(두께)
        pline([(CUT[0], W2, CUT[2]), (CUT[1], W2, CUT[2]), (CUT[1], W2, CUT[3]), (CUT[0], W2, CUT[3])], stroke=K, w=2.6, close=True)
        pline([(CUT[0], W2 - 40, CUT[2]), (CUT[1], W2 - 40, CUT[2]), (CUT[1], W2 - 40, CUT[3]), (CUT[0], W2 - 40, CUT[3])], stroke=P, w=1, close=True)
    else:
        draw_face(f)

# 뒷면 디테일(보이는 경우): 테일램프, 도어 분할선
if dot((-1, 0, 0), sub(CAM, (0, 0, 1000))) > 0:
    pline([(0, 0, 1850), (0, 0, 560)], w=1)
    for ly in (-930, 905):
        pline([(0, ly, 1700), (0, ly + 25, 1700), (0, ly + 25, 850), (0, ly, 850)], close=True, w=1.2, fill="#F6D7D3")
    pline([(0, -720, 1260), (0, -160, 1260), (0, -160, 1010), (0, -720, 1010)], stroke=L, close=True)
# GNSS 돔(마스트 위 타원)
c = PJ((575, 575, 1985)); rx_ = abs(PJ((680, 575, 1985))[0] - PJ((470, 575, 1985))[0]) / 2 + 6
add(f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="{rx_:.1f}" ry="{rx_ * 0.62:.1f}" fill="#FFFFFF" stroke="{K}" stroke-width="1.5"/>')

svg_keep = list(svg)
# ---------------------------------------------------------------- 번호 지시선
EQUIP = [(1, "전방 카메라 포드", (3245, 0, 1975), (110, -150)), (2, "경광등(루프)", (2445, 300, 1995), (60, -170)),
         (3, "RTK-GNSS 안테나", (575, 575, 2020), (-60, -150)), (4, "측면 카메라(미러)", (3525, 1100, 1340), (150, 40)),
         (5, "Edge Gateway 랙", (2260, -420, 1000), (260, -330)), (6, "수동 GPR 카트", (1700, 700, 520), (-40, 330)),
         (7, "후방 장비 수납장", (1000, -420, 1030), (170, -300)), (8, "후방 하부 GPR 어레이", (100, 900, 120), (60, 150)),
         (9, "휠 인코더(뒷바퀴)", (850, 990, 343), (-140, 200))]
for n, name, p, (dx, dy) in EQUIP:
    a = PJ(p); b = (a[0] + dx, a[1] + dy)
    add(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{K}" stroke-width="0.9"/>')
    add(f'<circle cx="{a[0]:.1f}" cy="{a[1]:.1f}" r="3" fill="{K}"/>')
    add(f'<circle cx="{b[0]:.1f}" cy="{b[1]:.1f}" r="22" fill="#fff" stroke="{K}" stroke-width="1.8"/>')
    text(b[0], b[1] + 8, str(n), 24, 700, a="middle")

# 원근 치수(차체 모서리를 따라)
def dim3(a, b, off, label):
    pa, pb = PJ(tuple(a[i] + off[i] for i in range(3))), PJ(tuple(b[i] + off[i] for i in range(3)))
    for p0, p1 in ((PJ(a), pa), (PJ(b), pb)):
        add(f'<line x1="{p0[0]:.1f}" y1="{p0[1]:.1f}" x2="{p1[0]:.1f}" y2="{p1[1]:.1f}" stroke="{G}" stroke-width="0.7"/>')
    add(f'<line x1="{pa[0]:.1f}" y1="{pa[1]:.1f}" x2="{pb[0]:.1f}" y2="{pb[1]:.1f}" stroke="{G}" stroke-width="1"/>')
    ang = math.atan2(pb[1] - pa[1], pb[0] - pa[0])
    for (q, s_) in ((pa, 1), (pb, -1)):
        x1, y1 = q[0] + s_ * 10 * math.cos(ang - 0.3), q[1] + s_ * 10 * math.sin(ang - 0.3)
        x2, y2 = q[0] + s_ * 10 * math.cos(ang + 0.3), q[1] + s_ * 10 * math.sin(ang + 0.3)
        add(f'<path d="M {q[0]:.1f} {q[1]:.1f} L {x1:.1f} {y1:.1f} L {x2:.1f} {y2:.1f} Z" fill="{G}"/>')
    m = ((pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2)
    deg = math.degrees(ang)
    if deg > 90: deg -= 180
    if deg < -90: deg += 180
    w = len(label) * 8.6 + 12
    add(f'<g transform="translate({m[0]:.1f} {m[1]:.1f}) rotate({deg:.1f})"><rect x="{-w / 2:.1f}" y="-11" width="{w:.1f}" height="22" fill="#fff"/>'
        f'<text x="0" y="5" font-family="Pretendard" font-size="14" fill="{G}" text-anchor="middle">{label}</text></g>')


dim3((0, W2, 0), (4695, W2, 0), (0, 420, 0), "전장 4,695")
dim3((0, -W2, 0), (0, W2, 0), (-450, 0, 0), "전폭 1,895")
dim3((4695, W2, 0), (4695, W2, 1905), (0, 330, 0), "전고 1,905")
text(*PJ((300, 0, -10))[:1], PJ((300, 0, -10))[1] + 70, "", 1)

# 탐사 폭 라벨
q = PJ((-40, 0, 0))


# ---------------------------------------------------------------- 부품표(좌하단, 슬라이드에서 읽히는 크기)
RH, FS = 54, 23
bx, bw = 50, 560
by = CH - 90 - RH * 10
add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{RH * 10}" fill="#fff" stroke="{K}" stroke-width="1.5"/>')
add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{RH}" fill="#F1F3F6" stroke="{K}" stroke-width="1.5"/>')
text(bx + 34, by + RH * 0.66, "번호", FS, 700, a="middle"); text(bx + 82, by + RH * 0.66, "장비", FS, 700)
add(f'<line x1="{bx + 68}" y1="{by}" x2="{bx + 68}" y2="{by + RH * 10}" stroke="{K}"/>')
for i, (n, name, *_r) in enumerate(EQUIP):
    y = by + RH + i * RH
    add(f'<line x1="{bx}" y1="{y}" x2="{bx + bw}" y2="{y}" stroke="{L}"/>')
    text(bx + 34, y + RH * 0.66, str(n), FS, 700, a="middle"); text(bx + 82, y + RH * 0.66, name, FS)

# ---------------------------------------------------------------- 표제란(우하단)
tx, ty_, tw, th = 1720, 56, 624, 200
add(f'<rect x="{tx}" y="{ty_}" width="{tw}" height="{th}" fill="#fff" stroke="{K}" stroke-width="1.6"/>')
for yy in (ty_ + 70, ty_ + 115, ty_ + 160):
    add(f'<line x1="{tx}" y1="{yy}" x2="{tx + tw}" y2="{yy}" stroke="{K}"/>')
add(f'<line x1="{tx + 150}" y1="{ty_ + 70}" x2="{tx + 150}" y2="{ty_ + th}" stroke="{K}"/>')
text(tx + 20, ty_ + 32, "PV5 GroundWatch 장비 배치도", 22, 800)
text(tx + 20, ty_ + 58, "PV5 카고 롱 기반 지하안전 순찰차 · 제안안", 14, c=G)
for i, (k, v) in enumerate([("투시", "3점 투시 · 뒤-오른쪽 위 시점, 화물실 우측 절개"), ("단위", "mm · 차량 치수: 기아 공식 제원"), ("비고", "장비 형상·위치는 제안 예시 · 팀 제작 도면")]):
    y = ty_ + 70 + i * 45
    text(tx + 75, y + 29, k, 15, 700, a="middle"); text(tx + 168, y + 29, v, 14)

# 범례(좌하단)
ly = CH - 52
add(f'<rect x="72" y="{ly - 10}" width="30" height="20" fill="{EQ}" stroke="{BLUE}" stroke-width="1.3"/>'); text(112, ly + 5, "탑재 장비", 15, c=G)
add(f'<rect x="230" y="{ly - 10}" width="30" height="20" fill="url(#scan)" stroke="{ACC}" stroke-dasharray="6 4"/>'); text(270, ly + 5, "GPR 탐사 범위(폭 약 1.8m, 제안 예시)", 15, c=G)
add(f'<line x1="600" y1="{ly}" x2="660" y2="{ly}" stroke="#C9CDD3" stroke-dasharray="3 6"/>'); text(670, ly + 5, "소실점 보조선", 15, c=G)

if CLEAN:
    svg[:] = svg_keep
    import json
    json.dump({str(n): [*PJ(p), name] for n, name, p, _o in EQUIP}, open(os.path.splitext(OUT)[0] + "_anchors.json", "w"), ensure_ascii=False)
body_svg = "\n".join(svg)
fonts = "".join(f"@font-face{{font-family:'Pretendard';src:url('file://{FONTS}/Pretendard-{n}.otf');font-weight:{w};}}"
                for n, w in [("Regular", 400), ("Medium", 500), ("SemiBold", 600), ("Bold", 700), ("ExtraBold", 800)])
html = f"""<!doctype html><html><head><meta charset="utf-8"><style>{fonts} html,body{{margin:0;padding:0;background:#fff}}</style></head>
<body><svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}">{body_svg}</svg></body></html>"""
with tempfile.TemporaryDirectory() as td:
    hp = os.path.join(td, "d.html")
    open(hp, "w", encoding="utf-8").write(html)
    subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=1.5", f"--window-size={CW},{CH}",
                    "--virtual-time-budget=5000", f"--screenshot={OUT}", "file://" + hp], check=True, capture_output=True)
print("saved", OUT)
