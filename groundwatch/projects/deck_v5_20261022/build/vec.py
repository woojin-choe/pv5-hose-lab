# 벡터 도면 모음: 지하 단면, PV5 측면 도면, 후방 장착 상세, 현장 화면 예시.
# 모든 도면은 같은 팔레트(남색 선, 회색 면, 노랑 강조)를 쓴다. 치수는 기아 공식 제원만 표기한다.
NAVY, INK, SUB, MUTE, LINE, PALE = "#0B1E3C", "#111827", "#374151", "#4B5563", "#E2E6EC", "#F3F5F8"
YEL, AMB, RED = "#F5B700", "#B45309", "#C62828"
ASPH, BASE, SOIL, DEEP = "#2B3036", "#8B9099", "#CDBB9F", "#A8957A"


# ---------------------------------------------------------------- 지하 단면
def section(x, y, w, h, cav=0.0, depth_m=2.6, ghost=0.0, labels=True, uid="s"):
    """도로 단면. cav: 공동 반지름(m), ghost: 이전 회차 공동 반지름(점선)."""
    k = h / depth_m                     # 1m 당 px
    gx = lambda m: x + w * m            # 가로 비율
    gy = lambda m: y + m * k            # 깊이(m) → y
    s = f'<clipPath id="clip{uid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" /></clipPath>\n'
    s += f'<g clip-path="url(#clip{uid})">\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SOIL}" />\n'
    s += f'<rect x="{x}" y="{gy(1.9)}" width="{w}" height="{h}" fill="{DEEP}" />\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{0.12 * k:.1f}" fill="{ASPH}" />\n'
    s += f'<rect x="{x}" y="{gy(0.12)}" width="{w}" height="{0.25 * k:.1f}" fill="{BASE}" />\n'
    # 하수관 Ø0.8m, 관 상단 1.6m
    pc, pr = (gx(0.5), gy(2.0)), 0.4 * k
    s += f'<circle cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" r="{pr:.1f}" fill="#E5E7EB" stroke="#6B7280" stroke-width="3" />\n'
    s += f'<circle cx="{pc[0]:.1f}" cy="{pc[1]:.1f}" r="{pr * 0.78:.1f}" fill="#4B5563" />\n'
    top = 1.6
    if ghost:
        gr = ghost * k
        s += f'<ellipse cx="{pc[0]:.1f}" cy="{gy(top) - gr * 0.55:.1f}" rx="{gr * 1.5:.1f}" ry="{gr:.1f}" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="6,4" />\n'
    if cav:
        cr = cav * k
        s += f'<ellipse cx="{pc[0]:.1f}" cy="{gy(top) - cr * 0.55:.1f}" rx="{cr * 1.5:.1f}" ry="{cr:.1f}" fill="#1E2228" />\n'
    s += '</g>\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NAVY}" stroke-width="1" />\n'
    return s, pc, k


def target_figure():
    """5장: 깊이 축 + GPR 탐사 범위 + 하수관 공동 + 심부 붕괴(범위 밖)."""
    x, y, w, h = 120, 170, 520, 330
    s, pc, k = section(x, y, w, h, cav=0.32, uid="t")
    # GPR 탐사 범위(약 2m)
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{2.0 * k:.1f}" fill="{YEL}" fill-opacity="0.16" />\n'
    s += f'<line x1="{x}" y1="{y + 2.0 * k:.1f}" x2="{x + w}" y2="{y + 2.0 * k:.1f}" stroke="{YEL}" stroke-width="3" />\n'
    s += f'<text x="{x + w - 12}" y="{y + 2.0 * k - 10:.1f}" font-size="15" font-weight="bold" fill="{NAVY}" text-anchor="end">차량형 GPR 탐사 깊이 약 2m</text>\n'
    # 깊이 축
    for m in (0, 1, 2):
        yy = y + m * k
        s += f'<line x1="{x - 10}" y1="{yy:.1f}" x2="{x}" y2="{yy:.1f}" stroke="{NAVY}" stroke-width="1.5" />\n'
        s += f'<text x="{x - 16}" y="{yy + 5:.1f}" font-size="14" fill="{SUB}" text-anchor="end">{m}m</text>\n'
    # 과정 라벨
    lab = [("1", "하수관 누수", pc[0] + 0.42 * k + 20, pc[1] + 6), ("2", "흙이 쓸려 공동", pc[0] + 0.62 * k + 20, y + 1.25 * k),
           ("3", "노면 침하", pc[0] + 30, y + 0.06 * k - 18)]
    for n, t, lx, ly in lab:
        s += f'<circle cx="{lx:.1f}" cy="{ly - 5:.1f}" r="11" fill="{NAVY}" />\n<text x="{lx:.1f}" y="{ly:.1f}" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">{n}</text>\n'
        s += f'<text x="{lx + 18:.1f}" y="{ly:.1f}" font-size="15" font-weight="bold" fill="{INK}">{t}</text>\n'
    # 심부(범위 밖) 표시
    s += f'<text x="{x + w / 2:.1f}" y="{y + h + 30}" font-size="16" fill="{MUTE}" text-anchor="middle">≈ 16m · 명일동 같은 심부 붕괴는 탐사 범위 밖(공사장 계측의 영역)</text>\n'
    return s


def change_figure(x0=56, y0=156):
    """6장: 지난 회차 / 약 2개월 뒤 / 자동 선별된 차이."""
    s = ""
    w, h = 340, 200
    panels = [("지난 회차", 0.18, 0, False), ("약 2개월 뒤", 0.34, 0, False), ("자동 선별된 차이", 0.34, 0.18, True)]
    for i, (lab, cav, ghost, diff) in enumerate(panels):
        x = x0 + i * 414
        sec, pc, k = section(x, y0, w, h, cav=0 if diff else cav, ghost=0, uid=f"c{i}")
        s += sec
        if diff:
            s += f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" fill="#0B1E3C" fill-opacity="0.72" />\n'
            cr, gr = cav * k, ghost * k
            cy, gy_ = y0 + 1.6 * k - cr * 0.55, y0 + 1.6 * k - gr * 0.55
            s += f'<ellipse cx="{pc[0]:.1f}" cy="{cy:.1f}" rx="{cr * 1.5:.1f}" ry="{cr:.1f}" fill="{YEL}" fill-opacity="0.85" />\n'
            s += f'<ellipse cx="{pc[0]:.1f}" cy="{gy_:.1f}" rx="{gr * 1.5:.1f}" ry="{gr:.1f}" fill="#0B1E3C" />\n'
            s += f'<text x="{pc[0] + cr * 1.5 + 12:.1f}" y="{cy + 5:.1f}" font-size="15" font-weight="bold" fill="#FFFFFF">커진 만큼만</text>\n'
        s += f'<rect x="{x + 8}" y="{y0 + 8}" width="{len(lab) * 15 + 22}" height="26" rx="3" fill="{NAVY}" fill-opacity="0.92" />\n'
        s += f'<text x="{x + 19}" y="{y0 + 26}" font-size="15" font-weight="bold" fill="#FFFFFF">{lab}</text>\n'
        if i < 2:
            s += f'<text x="{x + w + 37}" y="{y0 + h / 2 + 12:.1f}" font-size="34" font-weight="bold" fill="{NAVY}" text-anchor="middle">{"→" if i == 0 else "="}</text>\n'
    return s


# ---------------------------------------------------------------- PV5 측면 도면 (기아 공식 제원: 전장 4,695 · 휠베이스 2,995 · 전고 1,905 · 215/65R16)
def pv5_side(x0, gy, L=560, zones=True, dims=True, rear_gpr=True):
    k = L / 4695                                  # px/mm
    X = lambda mm: x0 + mm * k
    Y = lambda mm: gy - mm * k
    r = 343 * k                                   # 215/65R16 외경 약 686mm
    fo = 800                                      # 앞 오버행(공식 수치 없음: 비율 근사)
    fx, rx = X(fo), X(fo + 2995)
    H = 1905
    body = (f'M{X(0):.1f},{Y(330):.1f} L{X(0):.1f},{Y(900):.1f} L{X(60):.1f},{Y(1000):.1f} L{X(420):.1f},{Y(1120):.1f} '
            f'L{X(900):.1f},{Y(H - 40):.1f} Q{X(960):.1f},{Y(H):.1f} {X(1080):.1f},{Y(H):.1f} L{X(4600):.1f},{Y(H):.1f} '
            f'Q{X(4695):.1f},{Y(H):.1f} {X(4695):.1f},{Y(H - 110):.1f} L{X(4695):.1f},{Y(330):.1f} Z')
    s = f'<path d="{body}" fill="#F7F8FA" stroke="{NAVY}" stroke-width="2" />\n'
    # 유리
    s += (f'<path d="M{X(120):.1f},{Y(1010):.1f} L{X(450):.1f},{Y(1130):.1f} L{X(930):.1f},{Y(H - 70):.1f} L{X(1650):.1f},{Y(H - 70):.1f} '
          f'L{X(1650):.1f},{Y(1150):.1f} L{X(500):.1f},{Y(1060):.1f} Z" fill="#C9D3E2" stroke="{NAVY}" stroke-width="1.2" />\n')
    s += f'<line x1="{X(1700):.1f}" y1="{Y(H):.1f}" x2="{X(1700):.1f}" y2="{Y(330):.1f}" stroke="{NAVY}" stroke-width="1" />\n'
    # 하부 검은 몰딩
    s += f'<rect x="{X(0):.1f}" y="{Y(560):.1f}" width="{4695 * k:.1f}" height="{230 * k:.1f}" fill="#3A3F47" />\n'
    # 휠하우스 + 바퀴
    for cx in (fx, rx):
        s += f'<circle cx="{cx:.1f}" cy="{gy - r:.1f}" r="{r + 9:.1f}" fill="#3A3F47" />\n'
        s += f'<circle cx="{cx:.1f}" cy="{gy - r:.1f}" r="{r:.1f}" fill="#1F2329" />\n'
        s += f'<circle cx="{cx:.1f}" cy="{gy - r:.1f}" r="{r * 0.58:.1f}" fill="#6B7280" />\n'
        s += f'<circle cx="{cx:.1f}" cy="{gy - r:.1f}" r="{r * 0.16:.1f}" fill="#1F2329" />\n'
    # 바닥 아래 배터리 팩
    s += f'<rect x="{fx + r + 14:.1f}" y="{Y(330):.1f}" width="{rx - fx - 2 * r - 28:.1f}" height="{120 * k:.1f}" fill="#6B7280" />\n'
    s += f'<text x="{(fx + rx) / 2:.1f}" y="{Y(330) + 120 * k + 18:.1f}" font-size="13" fill="{MUTE}" text-anchor="middle">배터리 팩 (바닥 아래)</text>\n'
    if zones:
        # 카고룸 2,255mm (뒤쪽부터)
        cx0, cx1 = X(4695 - 120 - 2255), X(4695 - 120)
        s += f'<rect x="{cx0:.1f}" y="{Y(H - 160):.1f}" width="{cx1 - cx0:.1f}" height="{(H - 160 - 600) * k:.1f}" fill="#FFFFFF" stroke="{MUTE}" stroke-width="1" stroke-dasharray="5,4" />\n'
        zw = (cx1 - cx0) / 3
        for i, z in enumerate("ABC"):
            zx = cx0 + i * zw
            s += f'<rect x="{zx + 6:.1f}" y="{Y(H - 220):.1f}" width="{zw - 12:.1f}" height="{(H - 220 - 640) * k:.1f}" fill="{PALE}" stroke="{NAVY}" stroke-width="1" />\n'
            s += f'<circle cx="{zx + zw / 2:.1f}" cy="{Y(1250):.1f}" r="15" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />\n'
            s += f'<text x="{zx + zw / 2:.1f}" y="{Y(1250) + 5:.1f}" font-size="15" font-weight="bold" fill="{NAVY}" text-anchor="middle">{z}</text>\n'
    if rear_gpr:
        gx0, gx1 = rx + r + 20, X(4695) + 10
        s += f'<rect x="{gx0:.1f}" y="{gy - 120 * k:.1f}" width="{gx1 - gx0:.1f}" height="{70 * k:.1f}" fill="{YEL}" stroke="{NAVY}" stroke-width="1.5" />\n'
        s += f'<line x1="{(gx0 + gx1) / 2:.1f}" y1="{gy - 120 * k:.1f}" x2="{(gx0 + gx1) / 2:.1f}" y2="{Y(330):.1f}" stroke="{NAVY}" stroke-width="2" />\n'
        s += f'<path d="M{X(4380):.1f},{Y(H):.1f} q12,-16 24,0 Z" fill="{NAVY}" />\n'   # RTK 안테나
    if dims:
        dy = gy + 34
        s += f'<line x1="{X(0):.1f}" y1="{dy}" x2="{X(4695):.1f}" y2="{dy}" stroke="{MUTE}" stroke-width="1" />\n'
        s += f'<text x="{X(2347):.1f}" y="{dy + 18}" font-size="14" fill="{SUB}" text-anchor="middle">전장 4,695mm</text>\n'
        s += f'<line x1="{fx:.1f}" y1="{gy + 12}" x2="{rx:.1f}" y2="{gy + 12}" stroke="{MUTE}" stroke-width="1" />\n'
        s += f'<text x="{(fx + rx) / 2:.1f}" y="{gy + 28}" font-size="13" fill="{SUB}" text-anchor="middle">휠베이스 2,995mm</text>\n'
        s += f'<line x1="{X(-60):.1f}" y1="{Y(0):.1f}" x2="{X(-60):.1f}" y2="{Y(H):.1f}" stroke="{MUTE}" stroke-width="1" />\n'
        s += f'<text x="{X(-80):.1f}" y="{Y(H / 2):.1f}" font-size="13" fill="{SUB}" text-anchor="end">전고</text>\n<text x="{X(-80):.1f}" y="{Y(H / 2) + 16:.1f}" font-size="13" fill="{SUB}" text-anchor="end">1,905</text>\n'
    s += f'<line x1="{X(-200):.1f}" y1="{gy}" x2="{X(4900):.1f}" y2="{gy}" stroke="{NAVY}" stroke-width="2" />\n'
    return s, dict(fx=fx, rx=rx, r=r, k=k, X=X, Y=Y)


# ================================================================ 개선판
def section2(x, y, w, h, cav=0.0, ghost=0.0, uid="s", depth_m=2.8):
    """도로 단면(개선): 관 중심 1.6m(Ø0.8m, 상단 1.2m), 공동은 관 위로 솟는 아치형."""
    k = h / depth_m
    gy = lambda m: y + m * k
    px, pyc, pr = x + w * 0.5, gy(1.6), 0.4 * k
    s = '<g>\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{SOIL}" />\n'
    s += f'<rect x="{x}" y="{gy(2.3):.1f}" width="{w}" height="{y + h - gy(2.3):.1f}" fill="{DEEP}" />\n'
    s += f'<rect x="{x}" y="{gy(0.12):.1f}" width="{w}" height="{0.25 * k:.1f}" fill="{BASE}" />\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{0.12 * k:.1f}" fill="{ASPH}" />\n'

    def arch(r):          # 관 상단에서 위로 솟는 공동(아치)
        top = pyc - pr - r * k
        hw = (r * 1.7 + 0.25) * k
        base = pyc - pr * 0.35
        return (f'M{px - hw:.1f},{base:.1f} C{px - hw:.1f},{top + r * k * 0.2:.1f} {px - hw * 0.45:.1f},{top:.1f} {px:.1f},{top:.1f} '
                f'C{px + hw * 0.5:.1f},{top:.1f} {px + hw:.1f},{top + r * k * 0.25:.1f} {px + hw:.1f},{base:.1f} Z')
    if cav:
        s += f'<path d="{arch(cav)}" fill="#24282F" />\n'
    if ghost:
        s += f'<path d="{arch(ghost)}" fill="none" stroke="#FFFFFF" stroke-width="2" stroke-dasharray="6,4" />\n'
    s += f'<circle cx="{px:.1f}" cy="{pyc:.1f}" r="{pr:.1f}" fill="#E5E7EB" stroke="#6B7280" stroke-width="3" />\n'
    s += f'<circle cx="{px:.1f}" cy="{pyc:.1f}" r="{pr * 0.78:.1f}" fill="#4B5563" />\n'
    s += '</g>\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{NAVY}" stroke-width="1" />\n'
    return s, (px, pyc, pr), k, arch


def target_figure2(x=110, y=168, w=420, h=360):
    s, (px, pyc, pr), k, arch = section2(x, y, w, h, cav=0.28, uid="t2")
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{2.0 * k:.1f}" fill="{YEL}" fill-opacity="0.18" />\n'
    s += f'<line x1="{x}" y1="{y + 2.0 * k:.1f}" x2="{x + w}" y2="{y + 2.0 * k:.1f}" stroke="{YEL}" stroke-width="3" />\n'
    for m in (0, 1, 2):
        yy = y + m * k
        s += f'<line x1="{x - 10}" y1="{yy:.1f}" x2="{x}" y2="{yy:.1f}" stroke="{NAVY}" stroke-width="1.5" />\n'
        s += f'<text x="{x - 16}" y="{yy + 5:.1f}" font-size="14" fill="{SUB}" text-anchor="end">{m}m</text>\n'
    # 오른쪽 바깥 라벨 + 지시선
    lx = x + w + 24
    items = [("노면 침하", y + 0.06 * k, px + 40, y + 0.06 * k),
             ("흙이 쓸려 생긴 공동", pyc - pr - 0.18 * k, px + 0.35 * k, pyc - pr - 0.18 * k),
             ("하수관 누수", pyc, px + pr, pyc),
             ("GPR 탐사 깊이 약 2m", y + 2.0 * k, x + w, y + 2.0 * k)]
    for i, (t, ly, ax, ay) in enumerate(items):
        col = AMB if i == 3 else NAVY
        s += f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{lx - 6:.1f}" y2="{ly:.1f}" stroke="{col}" stroke-width="1.2" />\n'
        s += f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="3.5" fill="{col}" />\n'
        s += f'<text x="{lx:.1f}" y="{ly + 5:.1f}" font-size="15" font-weight="bold" fill="{col}">{t}</text>\n'
    s += f'<text x="{x}" y="{y + h + 28}" font-size="15" fill="{MUTE}">≈ 16m · 명일동 같은 심부 붕괴는 이 깊이 밖(공사장 계측의 영역)</text>\n'
    return s


def change_figure2(x0=56, y0=152, w=340, h=210):
    s = ""
    panels = [("지난 회차", 0.16, 0, False), ("약 2개월 뒤", 0.30, 0, False), ("자동 선별된 차이", 0.30, 0.16, True)]
    for i, (lab, cav, ghost, diff) in enumerate(panels):
        x = x0 + i * 414
        sec, (px, pyc, pr), k, arch = section2(x, y0, w, h, cav=0 if diff else cav, uid=f"cc{i}")
        s += sec
        if diff:
            s += f'<rect x="{x}" y="{y0}" width="{w}" height="{h}" fill="{NAVY}" fill-opacity="0.75" />\n'
            s += f'<path d="{arch(cav)}" fill="{YEL}" />\n<path d="{arch(ghost)}" fill="{NAVY}" />\n'
            s += f'<circle cx="{px:.1f}" cy="{pyc:.1f}" r="{pr:.1f}" fill="none" stroke="#9AA3AF" stroke-width="2" />\n'
            s += f'<text x="{x + w - 14}" y="{y0 + h - 16}" font-size="15" font-weight="bold" fill="#FFFFFF" text-anchor="end">커진 부분만 남음</text>\n'
        s += f'<rect x="{x + 8}" y="{y0 + 8}" width="{len(lab) * 15 + 22}" height="26" rx="3" fill="{NAVY}" fill-opacity="0.92" />\n'
        s += f'<text x="{x + 19}" y="{y0 + 26}" font-size="15" font-weight="bold" fill="#FFFFFF">{lab}</text>\n'
        if i < 2:
            s += f'<text x="{x + w + 37}" y="{y0 + h / 2 + 12:.1f}" font-size="34" font-weight="bold" fill="{NAVY}" text-anchor="middle">{"→" if i == 0 else "="}</text>\n'
    return s


# ---------------------------------------------------------------- 장착 상세: PV5 실루엣 + 공식 제원 기반 바퀴·치수
KMM = 1622 / 4695            # 실루엣 이미지 px/mm (전장 4,695mm = 1,622px)
FRONT_X, FWX, GROUND = 24, 170, 765


def mount_figure(ix, iy, sc):
    P = lambda x, y: (ix + x * sc, iy + y * sc)
    r = 343 * KMM                                    # 215/65R16 외경 약 686mm
    fx, rx = FWX, FWX + 2995 * KMM                   # 휠베이스 2,995mm
    wy = GROUND - r
    s = f'<image href="../images/pv5_blueprint.png" x="{ix}" y="{iy}" width="{1672 * sc:.1f}" height="{941 * sc:.1f}" />\n'
    for cx in (fx, rx):
        X, Y = P(cx, wy)
        s += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{(r + 6) * sc:.1f}" fill="#3A3F47" />\n'
        s += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r * sc:.1f}" fill="#1F2329" />\n'
        s += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r * 0.58 * sc:.1f}" fill="#8B9099" />\n'
        s += f'<circle cx="{X:.1f}" cy="{Y:.1f}" r="{r * 0.15 * sc:.1f}" fill="#1F2329" />\n'
    # 배터리 팩(바닥 아래)
    bx0, bx1 = P(fx + r + 18, 0)[0], P(rx - r - 18, 0)[0]
    s += f'<rect x="{bx0:.1f}" y="{P(0, 676)[1]:.1f}" width="{bx1 - bx0:.1f}" height="{28 * sc:.1f}" fill="#8B9099" stroke="{NAVY}" stroke-width="1" />\n'
    # 후방 GPR 배열 + 브래킷
    g0, g1 = P(rx + r + 16, 0)[0], P(1662, 0)[0]
    gt, gb = P(0, GROUND - 52)[1], P(0, GROUND - 12)[1]
    s += f'<rect x="{g0:.1f}" y="{gt:.1f}" width="{g1 - g0:.1f}" height="{gb - gt:.1f}" fill="{YEL}" stroke="{NAVY}" stroke-width="1.5" />\n'
    for bxp in (g0 + 10, g1 - 14):
        s += f'<line x1="{bxp:.1f}" y1="{gt:.1f}" x2="{bxp:.1f}" y2="{P(0, 700)[1]:.1f}" stroke="{NAVY}" stroke-width="2.5" />\n'
    # RTK 안테나(지붕, GPR 바로 위) + 기준선
    ax = (g0 + g1) / 2
    ry = P(0, 150)[1]
    s += f'<rect x="{ax - 10:.1f}" y="{ry - 18:.1f}" width="20" height="10" rx="5" fill="{NAVY}" />\n<line x1="{ax:.1f}" y1="{ry - 8:.1f}" x2="{ax:.1f}" y2="{ry + 2:.1f}" stroke="{NAVY}" stroke-width="2" />\n'
    s += f'<line x1="{ax:.1f}" y1="{ry + 4:.1f}" x2="{ax:.1f}" y2="{gt - 4:.1f}" stroke="{AMB}" stroke-width="1.5" stroke-dasharray="5,4" />\n'
    # 휠 인코더(뒷바퀴 허브)
    hx, hy = P(rx, wy)
    s += f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="6" fill="{YEL}" stroke="{NAVY}" stroke-width="1.5" />\n'
    # 치수(공식 제원)
    gyp = P(0, GROUND)[1]
    s += f'<line x1="{P(-120, 0)[0]:.1f}" y1="{gyp:.1f}" x2="{P(1700, 0)[0]:.1f}" y2="{gyp:.1f}" stroke="{NAVY}" stroke-width="2" />\n'
    d1 = gyp + 22
    s += f'<line x1="{P(fx, 0)[0]:.1f}" y1="{d1:.1f}" x2="{P(rx, 0)[0]:.1f}" y2="{d1:.1f}" stroke="{MUTE}" stroke-width="1" />\n'
    for xx in (fx, rx):
        s += f'<line x1="{P(xx, 0)[0]:.1f}" y1="{d1 - 6:.1f}" x2="{P(xx, 0)[0]:.1f}" y2="{d1 + 6:.1f}" stroke="{MUTE}" stroke-width="1" />\n'
    s += f'<text x="{P(fx, 0)[0] + 6:.1f}" y="{d1 + 18:.1f}" font-size="13" fill="{SUB}">휠베이스 2,995mm</text>\n'
    d2 = d1 + 34
    s += f'<line x1="{P(FRONT_X, 0)[0]:.1f}" y1="{d2:.1f}" x2="{P(1646, 0)[0]:.1f}" y2="{d2:.1f}" stroke="{MUTE}" stroke-width="1" />\n'
    for xx in (FRONT_X, 1646):
        s += f'<line x1="{P(xx, 0)[0]:.1f}" y1="{d2 - 6:.1f}" x2="{P(xx, 0)[0]:.1f}" y2="{d2 + 6:.1f}" stroke="{MUTE}" stroke-width="1" />\n'
    s += f'<text x="{P(FRONT_X, 0)[0] + 6:.1f}" y="{d2 + 18:.1f}" font-size="13" fill="{SUB}">전장 4,695mm</text>\n'
    anchors = dict(rtk=(ax, ry - 18), gpr=((g0 + g1) / 2, gb), battery=((bx0 + bx1) / 2, P(0, 704)[1]), enc=(hx, hy))
    return s, anchors
