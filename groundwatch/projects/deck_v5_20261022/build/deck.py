# PV5 GroundWatch v5 덱 생성기: 장마다 "한 문장 제목 + 그것을 증명하는 그림 하나" 원칙으로 SVG를 쓴다.
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "svg_output")
for _f in os.listdir(OUT):
    if _f.endswith(".svg"):
        os.remove(os.path.join(OUT, _f))
N = 13
NAVY, INK, SUB, MUTE, LINE, PALE = "#0B1E3C", "#111827", "#374151", "#4B5563", "#E2E6EC", "#F3F5F8"
YEL, AMB, RED = "#F5B700", "#B45309", "#C62828"
STEPS = ["문제", "해법", "PV5", "검증", "사업"]


def head(step, label):
    """왼쪽: 브랜드 칩 + 장 이름. 오른쪽: 이야기 진행 표시(현재 단계만 진하게)."""
    s = f'''  <g id="header" data-pptx-role="header" data-pptx-bounds="56 24 1168 40">
    <rect x="56" y="28" width="140" height="24" fill="{NAVY}" />
    <text x="126" y="45" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PV5 GroundWatch</text>
    <text x="210" y="45" font-size="14" fill="{SUB}">{label}</text>
'''
    x = 900
    for i, name in enumerate(STEPS):
        on = name == step
        s += f'    <text x="{x}" y="45" font-size="14" font-weight="{"bold" if on else "normal"}" fill="{NAVY if on else "#9AA3AF"}" text-anchor="middle">{name}</text>\n'
        if on:
            s += f'    <rect x="{x - 24}" y="54" width="48" height="3" fill="{YEL}" />\n'
        if i < len(STEPS) - 1:
            s += f'    <text x="{x + 33}" y="45" font-size="12" fill="#C3CCD9" text-anchor="middle">›</text>\n'
        x += 66
    s += f'    <line x1="56" y1="62" x2="1224" y2="62" stroke="{NAVY}" stroke-width="1" />\n  </g>\n'
    return s


def title(t, sub=None):
    s = f'  <g id="title" data-pptx-bounds="56 80 1168 56" letter-spacing="-1">\n    <text x="56" y="120" font-size="40" font-weight="bold" fill="{NAVY}">{t}</text>\n  </g>\n'
    if sub:
        s += f'  <g id="lead" data-pptx-bounds="56 138 1168 28">\n    <text x="56" y="160" font-size="19" fill="{SUB}">{sub}</text>\n  </g>\n'
    return s


def foot(no, src):
    return f'''  <g id="source" data-pptx-bounds="56 668 1168 20">
    <text x="56" y="682" font-size="12" fill="{MUTE}">{src}</text>
  </g>
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="56 692 1168 22" fill="{MUTE}" font-size="12">
    <text x="56" y="706">한 명이라도 살릴 수 있다면</text>
    <text x="1224" y="706" text-anchor="end">{no:02d} / {N}</text>
  </g>
'''


def band(y, text):
    """결론 한 줄: 남색 상자 대신 노란 막대 + 진한 글씨."""
    return f'''  <g id="conclusion" data-pptx-bounds="56 {y} 1168 44">
    <rect x="56" y="{y}" width="4" height="44" fill="{YEL}" />
    <text x="76" y="{y + 30}" font-size="21" font-weight="bold" fill="{NAVY}">{text}</text>
  </g>
'''


def svg(name, body, role="content"):
    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" lang="ko-KR" data-pptx-page-role="{role}" font-family="Pretendard, 'Malgun Gothic', sans-serif">
  <rect id="bg" x="0" y="0" width="1280" height="720" fill="#FFFFFF" />
{body}</svg>
'''
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(doc)


# ---------------------------------------------------------------- 01 표지
svg("01_cover.svg", f'''  <defs>
    <linearGradient id="coverFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="0.94" />
      <stop offset="42%" stop-color="{NAVY}" stop-opacity="0.72" />
      <stop offset="70%" stop-color="{NAVY}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <image id="cover-photo" data-pptx-role="background" href="../images/cover_hangang.jpg" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" />
  <rect id="cover-scrim" data-pptx-role="decoration" x="0" y="0" width="1280" height="720" fill="url(#coverFade)" />
  <g id="cover-kicker" data-pptx-bounds="64 196 440 30">
    <text x="64" y="218" font-size="17" font-weight="bold" fill="{YEL}">제5회 기아 PBV 아이디어 공모전 · 일반 부문</text>
  </g>
  <g id="cover-title" data-pptx-bounds="64 238 450 156" fill="#FFFFFF" font-weight="bold" letter-spacing="-1.5">
    <text x="64" y="302" font-size="68">PV5</text>
    <text x="64" y="372" font-size="56">GroundWatch</text>
  </g>
  <g id="cover-subtitle" data-pptx-bounds="64 396 440 44">
    <text x="64" y="428" font-size="30" font-weight="bold" fill="#D7DEE8">PV5 지하안전 순찰차</text>
  </g>
  <g id="cover-tagline" data-pptx-bounds="64 456 440 92">
    <rect x="64" y="460" width="48" height="3" fill="{YEL}" />
    <text x="64" y="502" font-size="21" fill="#D7DEE8">같은 길을 반복해서 보고,<tspan x="64" dy="32">구멍이 되기 전의 변화를 찾습니다.</tspan></text>
  </g>
  <g id="cover-team" data-pptx-bounds="64 600 440 72" font-weight="bold">
    <text x="64" y="622" font-size="14" fill="{YEL}">TEAM</text>
    <text x="64" y="656" font-size="22" fill="#FFFFFF">한 명이라도 살릴 수 있다면</text>
  </g>
  <g id="cover-date" data-pptx-bounds="1080 674 160 24">
    <text x="1232" y="692" font-size="13" fill="#C3CCD9" text-anchor="end">2026. 10</text>
  </g>
''', role="cover")

# ---------------------------------------------------------------- 02 사고
svg("02_incident.svg", head("문제", "실제로 일어난 일") + f'''  <defs>
    <linearGradient id="mapFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="#05070B" stop-opacity="0" />
      <stop offset="100%" stop-color="#05070B" stop-opacity="0.88" />
    </linearGradient>
  </defs>
  <g id="incident-map" data-pptx-bounds="680 0 600 720">
    <image href="../images/yeonhui_crop.png" x="680" y="0" width="600" height="720" preserveAspectRatio="xMidYMid slice" />
    <rect x="680" y="430" width="600" height="290" fill="url(#mapFade)" />
    <rect x="700" y="150" width="226" height="56" rx="4" fill="{NAVY}" fill-opacity="0.92" />
    <text x="714" y="174" font-size="16" font-weight="bold" fill="#FFFFFF">2024. 8. 29 사고 구간</text>
    <text x="714" y="195" font-size="14" fill="#D6DDE8">서대문구 연희동 성산로</text>
    <text x="712" y="590" font-size="28" font-weight="bold" fill="#FFFFFF">평범한 도로가<tspan x="712" dy="42">한 사람의 마지막 길이 되었습니다.</tspan></text>
    <text x="712" y="690" font-size="12" fill="#C3CCD9">지도 © OpenStreetMap contributors · 정확한 지점은 보도되지 않아 구간으로 표시</text>
  </g>
  <g id="kicker" data-pptx-bounds="56 132 600 28">
    <text x="56" y="154" font-size="18" font-weight="bold" fill="{RED}">2024. 8. 29 · 서울 서대문구 연희동</text>
  </g>
  <g id="title" data-pptx-bounds="56 168 623 136" letter-spacing="-1.5" font-weight="bold">
    <text x="56" y="222" font-size="40" fill="{NAVY}">‘이상 없음’ 판정</text>
    <text x="56" y="278" font-size="40" fill="{RED}">100여 일 뒤, 도로가 무너졌습니다</text>
  </g>
  <g id="timeline" data-pptx-bounds="56 330 600 150">
    <line x1="76" y1="404" x2="636" y2="404" stroke="#C3CCD9" stroke-width="3" />
    <rect x="76" y="398" width="560" height="12" fill="{YEL}" fill-opacity="0.25" />
    <circle cx="96" cy="404" r="11" fill="{NAVY}" />
    <text x="76" y="364" font-size="16" font-weight="bold" fill="{NAVY}">2024. 5. 7~16</text>
    <text x="76" y="386" font-size="15" fill="{SUB}">정기 GPR 탐사 · 공동 없음</text>
    <circle cx="616" cy="404" r="16" fill="{RED}" />
    <text x="636" y="364" font-size="16" font-weight="bold" fill="{RED}" text-anchor="end">2024. 8. 29</text>
    <text x="636" y="386" font-size="15" fill="{RED}" text-anchor="end">도로 함몰</text>
    <text x="356" y="444" font-size="16" fill="{SUB}" text-anchor="middle">이 사이의 변화는 아무도 보지 못했습니다</text>
  </g>
  <g id="facts" data-pptx-bounds="56 488 600 110">
    <line x1="56" y1="492" x2="636" y2="492" stroke="{LINE}" stroke-width="1" />
    <text x="56" y="548" font-size="40" font-weight="bold" fill="{INK}">6×4m</text>
    <text x="56" y="576" font-size="15" fill="{SUB}">함몰 규모</text>
    <text x="250" y="548" font-size="40" font-weight="bold" fill="{INK}">2.5m</text>
    <text x="250" y="576" font-size="15" fill="{SUB}">깊이 · 얕은 함몰</text>
    <text x="440" y="548" font-size="40" font-weight="bold" fill="{RED}">사망 1</text>
    <text x="440" y="576" font-size="15" fill="{SUB}">차량 추락 · 동승자</text>
  </g>
  <g id="source" data-pptx-bounds="56 640 600 20">
    <text x="56" y="652" font-size="12" fill="{MUTE}">출처: 뉴시스·아시아경제(2024.8.30), 세계일보(2025.9.25)</text>
  </g>
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="56 692 600 22" fill="{MUTE}" font-size="12">
    <text x="56" y="706">한 명이라도 살릴 수 있다면</text>
    <text x="636" y="706" text-anchor="end">02 / {N}</text>
  </g>
''')

# ---------------------------------------------------------------- 03 맹점
svg("03_blindspot.svg", head("문제", "지금 체계의 맹점") + title("맹점은 탐사가 아니라, 탐사와 탐사 ‘사이’입니다") + f'''  <g id="gap-chart" data-pptx-bounds="56 168 680 360">
    <text x="56" y="196" font-size="18" font-weight="bold" fill="{NAVY}">한 번 탐사한 도로를 다시 보기까지</text>
    <line x1="56" y1="210" x2="736" y2="210" stroke="{NAVY}" stroke-width="1.5" />
    <text x="56" y="256" font-size="18" fill="{INK}">법이 정한 공동조사 주기</text>
    <rect x="56" y="270" width="600" height="34" fill="#9AA3AF" />
    <text x="668" y="296" font-size="26" font-weight="bold" fill="{INK}">5년</text>
    <text x="56" y="356" font-size="18" fill="{INK}">서울시가 줄인 정기점검 주기 <tspan font-size="15" fill="{SUB}">(2025.4)</tspan></text>
    <rect x="56" y="370" width="120" height="34" fill="{NAVY}" />
    <text x="188" y="396" font-size="26" font-weight="bold" fill="{NAVY}">1년</text>
    <text x="56" y="456" font-size="18" font-weight="bold" fill="{RED}">연희동: 탐사 ‘이상 없음’에서 함몰까지</text>
    <rect x="56" y="470" width="35" height="34" fill="{RED}" />
    <text x="103" y="496" font-size="26" font-weight="bold" fill="{RED}">100여 일</text>
  </g>
  <g id="evidence" data-pptx-bounds="784 168 440 360">
    <rect x="784" y="168" width="440" height="3" fill="{NAVY}" />
    <text x="784" y="204" font-size="15" font-weight="bold" fill="{AMB}">그 사이 공동은 자랍니다</text>
    <text x="784" y="250" font-size="26" font-weight="bold" fill="{NAVY}">“예상보다 단기간에</text>
    <text x="784" y="286" font-size="26" font-weight="bold" fill="{NAVY}">공동이 성장할 수 있다”</text>
    <text x="784" y="330" font-size="16" fill="{SUB}">일본 국토교통성 위탁연구</text>
    <text x="784" y="352" font-size="16" fill="{SUB}">(도쿄대·지오서치, 2018~2020)</text>
    <line x1="784" y1="380" x2="1224" y2="380" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="414" font-size="16" fill="{INK}">같은 도로를 반복 모니터링하자</text>
    <text x="784" y="438" font-size="16" fill="{INK}">지하 1.64m 하수관 위 공동이</text>
    <text x="784" y="462" font-size="16" fill="{INK}">급격히 자란 것이 확인됐습니다.</text>
  </g>
  {band(566, "한 번의 탐사는 그 시점만 말해 줍니다. 그 사이의 ‘변화’를 봐야 합니다.").strip()}
''' + foot(3, "출처: 지하안전법(지하시설물관리자 공동조사 5년 1회 이상) · 이투데이(2025.4.23) · 뉴시스(2024.8.30) · 일본 국토교통성 도로정책 연구 30-5(2021)"))

# ---------------------------------------------------------------- 04 대상
svg("04_target.svg", head("문제", "우리가 막을 대상") + title("원인 1위 하수관 손상은 ‘얕은 공동’부터 만듭니다") + f'''  <g id="section" data-pptx-bounds="56 160 640 420">
    <image href="../images/ug_section_cut.png" x="56" y="166" width="640" height="407" preserveAspectRatio="xMidYMid meet" />
    <g font-size="15" font-weight="bold">
      <rect x="290" y="214" width="112" height="28" rx="14" fill="{NAVY}" />
      <text x="346" y="233" fill="#FFFFFF" text-anchor="middle">3  노면 침하</text>
      <rect x="114" y="282" width="112" height="28" rx="14" fill="{NAVY}" />
      <text x="170" y="301" fill="#FFFFFF" text-anchor="middle">2  공동 형성</text>
      <rect x="406" y="340" width="124" height="28" rx="14" fill="{NAVY}" />
      <text x="468" y="359" fill="#FFFFFF" text-anchor="middle">1  하수관 누수</text>
      <rect x="138" y="524" width="160" height="28" rx="14" fill="#FFFFFF" stroke="#9AA3AF" stroke-width="1" />
      <text x="218" y="543" fill="{SUB}" text-anchor="middle">깊은 층 · 대상 아님</text>
    </g>
  </g>
  <g id="stat" data-pptx-bounds="744 160 480 162">
    <text x="744" y="250" font-size="88" font-weight="bold" fill="{NAVY}" letter-spacing="-3">45.4%</text>
    <text x="744" y="286" font-size="20" font-weight="bold" fill="{INK}">지반침하 원인 1위 · 하수관 손상</text>
    <text x="744" y="312" font-size="16" fill="{SUB}">전국 867건 중 394건 (2020~2024)</text>
  </g>
  <g id="scope" data-pptx-bounds="744 340 480 220">
    <rect x="744" y="340" width="480" height="3" fill="{YEL}" />
    <text x="744" y="378" font-size="19" font-weight="bold" fill="{NAVY}">얕은 공동형 · 약 2m 이내 → GroundWatch 대상</text>
    <text x="744" y="404" font-size="16" fill="{SUB}">공동이 먼저 생겨 함몰 전에 GPR로 찾을 수 있음</text>
    <rect x="744" y="440" width="480" height="3" fill="#C3CCD9" />
    <text x="744" y="478" font-size="19" font-weight="bold" fill="{MUTE}">심부 붕괴형 · 예: 명일동 16m → 대상 아님</text>
    <text x="744" y="504" font-size="16" fill="{SUB}">깊은 지층·터널 공사 영역은 공사장 계측이 맡음</text>
  </g>
  {band(600, "차량형 GPR이 보는 깊이(약 2m)에, 가장 흔한 원인이 있습니다.").strip()}
''' + foot(4, "출처: 국토교통부 지반침하 원인 통계(2020~2024) · 국토교통부 명일동 사고조사(2025.12.3) · 서울시 차량형 GPR 탐사 깊이 약 2m · 단면도는 원리 설명용"))

# ---------------------------------------------------------------- 05 해법
svg("05_solution.svg", head("해법", "GroundWatch의 핵심") + title("같은 길을 약 2개월마다 다시 찍고, 달라진 곳만 다시 봅니다") + f'''  <g id="compare" data-pptx-bounds="56 160 680 400">
    <rect x="56" y="166" width="680" height="388" fill="#2A2E33" />
    <image href="../images/bscan_prev_band.png" x="56" y="166" width="680" height="192" preserveAspectRatio="xMidYMid slice" />
    <image href="../images/bscan_cur_band.png" x="56" y="362" width="680" height="192" preserveAspectRatio="xMidYMid slice" />
    <rect x="68" y="178" width="96" height="28" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="116" y="198" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">지난 회차</text>
    <rect x="68" y="374" width="96" height="28" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="116" y="394" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">이번 회차</text>
    <rect x="410" y="400" width="300" height="140" fill="none" stroke="{YEL}" stroke-width="4" />
    <rect x="410" y="370" width="150" height="28" fill="{YEL}" />
    <text x="485" y="390" font-size="16" font-weight="bold" fill="{NAVY}" text-anchor="middle">새로 커진 신호</text>
  </g>
  <g id="steps" data-pptx-bounds="784 166 440 388">
    <text x="784" y="196" font-size="15" font-weight="bold" fill="{MUTE}">1</text>
    <text x="808" y="196" font-size="22" font-weight="bold" fill="{NAVY}">반복 측정</text>
    <text x="808" y="224" font-size="17" fill="{SUB}">PV5가 새벽에 같은 경로를 약 2개월마다 주행</text>
    <line x1="784" y1="252" x2="1224" y2="252" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="292" font-size="15" font-weight="bold" fill="{MUTE}">2</text>
    <text x="808" y="292" font-size="22" font-weight="bold" fill="{NAVY}">변화만 선별</text>
    <text x="808" y="320" font-size="17" fill="{SUB}">AI가 지난 회차와 달라진 곳을 고르고</text>
    <text x="808" y="344" font-size="17" fill="{SUB}">전문가가 원시 데이터로 승인</text>
    <line x1="784" y1="372" x2="1224" y2="372" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="412" font-size="15" font-weight="bold" fill="{MUTE}">3</text>
    <text x="808" y="412" font-size="22" font-weight="bold" fill="{NAVY}">현장 재확인</text>
    <text x="808" y="440" font-size="17" fill="{SUB}">승인된 곳만 수동 GPR로 다시 보고</text>
    <text x="808" y="464" font-size="17" fill="{SUB}">필요하면 천공·내시경으로 확정</text>
    <line x1="784" y1="492" x2="1224" y2="492" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="530" font-size="17" fill="{INK}">결과는 다음 순찰 경로에 다시 반영됩니다.</text>
  </g>
  {band(590, "AI는 볼 순서를 정할 뿐, 판정은 전문가가 하고 확정은 천공이 합니다.").strip()}
''' + foot(5, "약 2개월 = 차량 1대가 연 6,600km를 달려 도로 약 1,000km를 연 6회 반복(11장, 가설) · B-scan 비교 화면은 설명용 예시"))

# ---------------------------------------------------------------- 07 PV5 탐사실 (6+7 통합)
svg("07_pv5_lab.svg", head("PV5", "PV5 이동형 탐사실") + title("PV5 한 대가 그대로 이동형 탐사실이 됩니다") + f'''  <g id="cutaway" data-pptx-bounds="56 150 680 440">
    <image href="../images/cutaway_fixed.png" x="56" y="150" width="680" height="453" preserveAspectRatio="xMidYMid meet" />
    <g font-size="16" font-weight="bold" text-anchor="middle">
      <circle cx="342" cy="372" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="342" y="378" fill="{NAVY}">A</text>
      <circle cx="460" cy="308" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="460" y="314" fill="{NAVY}">B</text>
      <circle cx="608" cy="326" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="608" y="332" fill="{NAVY}">C</text>
    </g>
  </g>
  <g id="features" data-pptx-bounds="776 160 448 420">
    <text x="776" y="190" font-size="20" font-weight="bold" fill="{NAVY}">싣는다 <tspan font-size="16" font-weight="normal" fill="{SUB}">카고룸 4,420L · 최대 적재 600kg</tspan></text>
    <text x="776" y="216" font-size="15" fill="{MUTE}">A 분석 장비 · B 수동 GPR·AR 글래스 · C 안전장비</text>
    <line x1="776" y1="236" x2="1224" y2="236" stroke="{LINE}" stroke-width="1" />
    <text x="776" y="276" font-size="20" font-weight="bold" fill="{NAVY}">켠다 <tspan font-size="16" font-weight="normal" fill="{SUB}">실내·실외 V2L · 최대 3.6kW</tspan></text>
    <text x="776" y="302" font-size="15" fill="{MUTE}">시동 없이 GPR·엣지 PC를 돌리고 장비를 충전</text>
    <line x1="776" y1="322" x2="1224" y2="322" stroke="{LINE}" stroke-width="1" />
    <text x="776" y="362" font-size="20" font-weight="bold" fill="{NAVY}">고정한다 <tspan font-size="16" font-weight="normal" fill="{SUB}">L-Track·몰리 패널</tspan></text>
    <text x="776" y="388" font-size="15" fill="{MUTE}">회차마다 같은 위치에 장착 → 같은 조건으로 비교</text>
    <line x1="776" y1="408" x2="1224" y2="408" stroke="{LINE}" stroke-width="1" />
    <text x="776" y="448" font-size="20" font-weight="bold" fill="{NAVY}">복제한다 <tspan font-size="16" font-weight="normal" fill="{SUB}">기아 공식 컨버전 체계</tspan></text>
    <text x="776" y="474" font-size="15" fill="{MUTE}">특장 파트너 10개사 · 3D CAD 제공 → 같은 사양 여러 대</text>
    <rect x="776" y="504" width="448" height="76" fill="{PALE}" />
    <text x="796" y="534" font-size="15" font-weight="bold" fill="{AMB}">그래도 여유 있습니다 <tspan font-weight="normal" fill="{MUTE}">[가설]</tspan></text>
    <text x="796" y="562" font-size="16" fill="{INK}">장비 약 300kg / 600kg · 전력 약 1.5kW / 3.6kW</text>
  </g>
''' + foot(7, "차량형 GPR은 하부형(배치도)·후방형(표지) 중 배터리 팩·지상고 간섭 시험 후 확정 · 출처: 기아 PV5 카고 제원·액세서리, 오토뷰(2026) · V2L 3.6kW는 해외 제원 · 배치도는 콘셉트"))

# ---------------------------------------------------------------- 12 마무리
svg("12_closing.svg", f'''  <defs>
    <linearGradient id="closeFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="1" />
      <stop offset="55%" stop-color="{NAVY}" stop-opacity="0.85" />
      <stop offset="100%" stop-color="{NAVY}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1280" height="720" fill="{NAVY}" />
  <image href="../images/pv5_rear_dawn.jpg" x="560" y="0" width="720" height="720" preserveAspectRatio="xMidYMid slice" />
  <rect x="560" y="0" width="420" height="720" fill="url(#closeFade)" />
  <g id="recap" data-pptx-bounds="64 96 620 300">
    <text x="64" y="120" font-size="16" font-weight="bold" fill="{YEL}">GroundWatch가 바꾸는 것</text>
    <text x="64" y="176" font-size="22" fill="#9FB0C8">한 번 찍고 끝나는 탐사</text>
    <text x="64" y="212" font-size="26" font-weight="bold" fill="#FFFFFF">→ 같은 길의 ‘변화’를 보는 탐사</text>
    <text x="64" y="268" font-size="22" fill="#9FB0C8">사람이 다시 찾아야 하는 의심 지점</text>
    <text x="64" y="304" font-size="26" font-weight="bold" fill="#FFFFFF">→ 현장에서 바로 확인하는 재탐사</text>
    <text x="64" y="360" font-size="22" fill="#9FB0C8">장비를 실은 차</text>
    <text x="64" y="396" font-size="26" font-weight="bold" fill="#FFFFFF">→ 복제 가능한 PV5 탐사실</text>
  </g>
  <g id="closing" data-pptx-bounds="64 470 620 150">
    <rect x="64" y="470" width="48" height="3" fill="{YEL}" />
    <text x="64" y="530" font-size="38" font-weight="bold" fill="#FFFFFF">한 번의 조기 발견이,<tspan x="64" dy="52">한 사람의 무사 귀가가 되도록.</tspan></text>
  </g>
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="64 670 1172 40">
    <text x="64" y="700" font-size="14" font-weight="bold" fill="{YEL}">TEAM 한 명이라도 살릴 수 있다면</text>
    <text x="1232" y="684" font-size="11" fill="#D6DDE8" text-anchor="end">사진: Alexander Migl, CC BY-SA 4.0(편집)</text>
    <text x="1232" y="704" font-size="13" font-weight="bold" fill="{YEL}" text-anchor="end">12 / {N}</text>
  </g>
''', role="ending")


# ---------------------------------------------------------------- v4 장을 가져와 머리말·제목·쪽번호를 새 흐름에 맞춘다
import re
V4 = os.path.join(os.path.dirname(__file__), "..", "..", "deck_v4_20261022", "svg_output")


def port(src, dst, no, step, label, new_title, drops=(), edits=(), regex_drop=None):
    s = open(os.path.join(V4, src), encoding="utf-8").read()
    s = re.sub(r'  <g id="header".*?\n  </g>\n', head(step, label), s, count=1, flags=re.S)
    s = re.sub(r'(<g id="title"[^>]*>\s*<text [^>]*>)[^<]*(</text>)', lambda m: m.group(1) + new_title + m.group(2), s, count=1)
    for gid in drops:
        s, n = re.subn(r'\n  <g id="%s"[^>]*>.*?\n  </g>' % re.escape(gid), "", s, count=1, flags=re.S)
        assert n == 1, (src, gid)
    for a, b in edits:
        assert a in s, (src, a[:50])
        s = s.replace(a, b)
    if regex_drop:
        s, n = re.subn(regex_drop, "", s, count=1, flags=re.S)
        assert n == 1, (src, "regex_drop")
    s = re.sub(r'\d\d / \d\d<', f"{no:02d} / {N}<", s)
    open(os.path.join(OUT, dst), "w", encoding="utf-8").write(s)


port("08_app_ar.svg", "06_field.svg", 6, "해법", "현장 재확인", "차가 찾은 지점을, 작업자가 현장에서 바로 확인합니다", regex_drop=r'\n      <g font-size="13" fill="#4B5563">.*?</g>')
port("09_why_pv5.svg", "08_why_pv5.svg", 8, "PV5", "왜 PV5인가", "가격이 아니라 구조 때문에 PV5입니다",
     edits=[('<rect x="452" y="446" width="376" height="134" fill="#F3F5F8" />', ''),
            ('<text x="472" y="474" font-size="15" font-weight="bold" fill="#0B1E3C">PV5 공식 컨버전 체계</text>', ''),
            ('<text x="472" y="500" font-size="15" fill="#111827">국내 특장 파트너 10개사 선정<tspan x="472" dy="21">PBV 컨버전 포털: 3D CAD·기술 가이드</tspan><tspan x="472" dy="21">12V 전력 연결 블록·PIM 기본 적용</tspan><tspan x="472" dy="21">→ GPR 키트 표준화의 바탕</tspan></text>', ''),
            ('<rect x="848" y="446" width="376" height="134" fill="#F3F5F8" />', '<rect x="652" y="446" width="572" height="134" fill="#F3F5F8" />'),
            ('<rect x="56" y="446" width="376" height="134" fill="#F3F5F8" />', '<rect x="56" y="446" width="572" height="134" fill="#F3F5F8" />'),
            ('<text x="868" y="474"', '<text x="672" y="474"'),
            ('<text x="868" y="500" font-size="15" fill="#111827">주행거리는 스타리아보다 10km 짧고,<tspan x="868" dy="21">전폭은 포터·봉고보다 155mm 넓습니다.</tspan><tspan x="868" dy="21">→ 하루 순찰 약 30km <tspan fill="#4B5563">[가설]</tspan>에는</tspan><tspan x="868" dy="21">377km로 충분합니다.</tspan></text>',
             '<text x="672" y="500" font-size="16" fill="#111827">주행거리는 스타리아보다 10km 짧고, 전폭은 포터·봉고보다<tspan x="672" dy="24">155mm 넓습니다. 하루 순찰 약 30km <tspan fill="#4B5563">[가설]</tspan>에는</tspan><tspan x="672" dy="24">377km로 충분합니다.</tspan></text>'),
            ('<text x="76" y="500" font-size="15" fill="#111827">차값 차이는 최대 1,354만 원,<tspan x="76" dy="21">차량형 GPR은 대당 <tspan font-weight="bold">2억~8억 원</tspan>.</tspan><tspan x="76" dy="21">차이를 가르는 건 구조와</tspan><tspan x="76" dy="21">지원 체계입니다.</tspan></text>',
             '<text x="76" y="500" font-size="16" fill="#111827">차값 차이는 최대 1,354만 원인데, 차량형 GPR은<tspan x="76" dy="24">대당 <tspan font-weight="bold">2억~8억 원</tspan>입니다. 차이를 가르는 건</tspan><tspan x="76" dy="24">전원·고정 구조와 공식 컨버전 체계입니다.</tspan></text>')])
port("14_go_to_market.svg", "11_entry.svg", 11, "사업", "첫 고객과 확장", "이미 GPR 예산을 쓰는 지자체에서 시작합니다",
     edits=[(">0.46~1.77억 원<", ">0.85~1.90억 원<"),
            (">보령·안양·용인(기흥구) 낙찰, 이미 집행 중<", ">안양·강동구·용인 등 낙찰, 이미 집행 중<"),
            ("자치구 2곳 연간 계약", "지자체 2곳 연간 계약"),
            ("출처: 나라장터 2026 GPR 용역 낙찰(보령·안양·용인 기흥구)", "출처: 나라장터 2026 GPR 용역(안양 R26BK01572949 · 강동구 R26BK01599467 · 용인 R26BK01517362)")])
print("ok")


# ---------------------------------------------------------------- 09 실증: 질문 4개 + 단계 4개
def verify():
    rows = [("EV 구동계와 GPR의 전자파 간섭", "차량에서 측정 자체가 불가", "주행·정차·V2L 상태별 잡음 비교"),
            ("회차마다 같은 자리를 찍는가", "변화 비교가 불가", "RTK·IMU·휠 인코더로 위치 정합"),
            ("AI가 변화를 맞게 고르는가", "재확인 출동이 과다", "공동 모사체 구간 · 계절 보정"),
            ("밤에 AR이 정확히 맞는가", "현장 탐색 범위가 커짐", "맨홀·경계석 기준점 오차 측정")]
    b = f'''  <g id="lead" data-pptx-bounds="56 138 1168 28">
    <text x="56" y="160" font-size="19" fill="{SUB}">반복 탐사의 효과는 연구로 확인됐습니다(4장). 남은 건 <tspan font-weight="bold" fill="{NAVY}">PV5에 실었을 때도 정확한가</tspan>입니다.</text>
  </g>
  <g id="questions" data-pptx-bounds="56 186 1168 236">
    <g font-size="14" font-weight="bold" fill="{MUTE}">
      <text x="56" y="206">확인할 질문</text>
      <text x="520" y="206">안 되면</text>
      <text x="820" y="206">어떻게 확인하나</text>
    </g>
    <line x1="56" y1="216" x2="1224" y2="216" stroke="{NAVY}" stroke-width="1.5" />
'''
    y = 254
    for i, (q, f, h) in enumerate(rows):
        b += f'''    <text x="56" y="{y}" font-size="15" font-weight="bold" fill="{MUTE}">{i + 1}</text>
    <text x="80" y="{y}" font-size="19" font-weight="bold" fill="{NAVY}">{q}</text>
    <text x="520" y="{y}" font-size="17" fill="{RED}">{f}</text>
    <text x="820" y="{y}" font-size="17" fill="{INK}">{h}</text>
'''
        if i < 3:
            b += f'    <line x1="56" y1="{y + 18}" x2="1224" y2="{y + 18}" stroke="{LINE}" stroke-width="1" />\n'
        y += 48
    b += '  </g>\n'
    stages = [("1단계", "폐쇄 시험장", "질문 1", "통과 → 차량 측정 가능"),
              ("2단계", "통제된 시험 구간", "질문 2·3", "통과 → 회차 비교 가능"),
              ("3단계", "실제 도로 위험구간", "질문 3·4", "통과 → 실증확인서"),
              ("4단계", "실제 운영", "소요시간·재방문", "통과 → 연간 관제 계약")]
    b += f'  <g id="stages" data-pptx-bounds="56 446 1168 130">\n    <text x="56" y="466" font-size="15" font-weight="bold" fill="{MUTE}">실증 순서</text>\n'
    x = 56
    for i, (n, place, q, ok) in enumerate(stages):
        fill = NAVY if i == 3 else PALE
        t1, t2 = ("#FFFFFF", YEL) if i == 3 else (NAVY, AMB)
        b += f'''    <rect x="{x}" y="480" width="278" height="94" fill="{fill}" />
    <text x="{x + 18}" y="508" font-size="14" font-weight="bold" fill="{t2}">{n} · {q}</text>
    <text x="{x + 18}" y="536" font-size="20" font-weight="bold" fill="{t1}">{place}</text>
    <text x="{x + 18}" y="562" font-size="15" fill="{t1}">{ok}</text>
'''
        if i < 3:
            b += f'    <text x="{x + 286}" y="534" font-size="18" fill="{MUTE}">›</text>\n'
        x += 297
    b += '  </g>\n'
    b += band(600, "정확도 숫자를 미리 약속하지 않고, 단계마다 통과 조건을 둡니다.")
    return head("검증", "기술 실증 계획") + title("남은 질문은 4가지, 4단계로 실증합니다") + b + foot(
        9, "인허가: 도로 영상은 개인정보보호법 제25조의2(2023.9)대로 차량 외부 표시 · GPR 전파 적합성평가·튜닝 승인은 사업화 전 확인 · 출처: 일본 국토교통성 연구(2021)")


svg("09_verify.svg", verify())


# ---------------------------------------------------------------- 10 수지: 막대 하나로 비용 vs 수입
def econ():
    X0, K = 330, 110  # 0억 위치, 1억당 px
    b = f'''  <g id="market" data-pptx-bounds="56 138 1168 74">
    <text x="56" y="176" font-size="30" font-weight="bold" fill="{NAVY}">96,712km</text>
    <text x="56" y="202" font-size="15" fill="{SUB}">지자체가 관리하는 도로 (전국의 83%)</text>
    <text x="452" y="176" font-size="30" font-weight="bold" fill="{NAVY}">2,308 → 11,380km</text>
    <text x="452" y="202" font-size="15" fill="{SUB}">정부 지반탐사 2024 → 2026 (약 5배)</text>
    <text x="900" y="176" font-size="30" font-weight="bold" fill="{NAVY}">44억 원</text>
    <text x="900" y="202" font-size="15" fill="{SUB}">2026 국비 · 지자체 지반탐사 지원</text>
  </g>
  <g id="bars" data-pptx-bounds="56 232 1168 300">
    <line x1="56" y1="234" x2="1224" y2="234" stroke="{NAVY}" stroke-width="1.5" />
    <text x="56" y="262" font-size="15" font-weight="bold" fill="{MUTE}">연간 금액 (억 원)</text>
'''
    rows = [("차량 1대 연간 비용", "[가설]", 1.8, 2.4, "#9AA3AF", "1.8~2.4억"),
            ("지자체 1곳 연간 GPR 용역", "강동구·용인급", 1.4, 1.8, "#C9D3E2", "1.4~1.8억"),
            ("지자체 2곳을 맡으면", "", 2.8, 3.5, NAVY, "2.8~3.5억"),
            ("지자체 3곳을 맡으면", "", 4.2, 5.3, NAVY, "4.2~5.3억")]
    y = 290
    for name, tag, lo, hi, col, lab in rows:
        b += f'''    <text x="56" y="{y + 24}" font-size="18" font-weight="bold" fill="{INK}">{name} <tspan font-size="14" font-weight="normal" fill="{MUTE}">{tag}</tspan></text>
    <rect x="{X0}" y="{y}" width="{lo * K:.0f}" height="36" fill="{col}" />
    <rect x="{X0 + lo * K:.0f}" y="{y}" width="{(hi - lo) * K:.0f}" height="36" fill="{col}" fill-opacity="0.45" />
    <text x="{X0 + max(hi, 2.4) * K + 14:.0f}" y="{y + 25}" font-size="20" font-weight="bold" fill="{NAVY}">{lab}</text>
'''
        y += 58
    xb = X0 + 2.4 * K
    b += f'''    <line x1="{xb:.0f}" y1="278" x2="{xb:.0f}" y2="{y - 10}" stroke="{RED}" stroke-width="2" stroke-dasharray="6,5" />
    <text x="{xb + 8:.0f}" y="282" font-size="14" font-weight="bold" fill="{RED}">비용 상한 2.4억</text>
  </g>
  <g id="basis" data-pptx-bounds="56 532 1168 50">
    <text x="56" y="552" font-size="15" fill="{SUB}">비용 = PV5·차량형 GPR(2억~5억) 5년 감가 + 2인 1조 인건비 1억 + 장비·유지 0.3억 · 처리량 = 하루 30km × 220일 = 연 6,600km → 도로 약 1,000km를 약 2개월마다</text>
    <text x="56" y="576" font-size="15" fill="{SUB}"><tspan font-weight="bold" fill="{NAVY}">기아에게</tspan> 장비 포함 대당 2억 원 이상의 고부가 컨버전 PV5 · 시·군·구 226곳의 권역별 플릿 수요</text>
  </g>
'''
    b += band(600, "비용은 연 약 2억 원. 지자체 2곳부터 수입이 비용을 넘습니다.")
    return head("사업", "시장과 수지") + title("차량 1대가 지자체 2곳만 맡아도 흑자입니다") + b + foot(
        10, "출처: e-나라지표(2025.12) · 머니투데이(2025.12.23) · 뉴스서울(2025.12.3) · 시사저널(2025.4.25) · 나라장터 개찰(강동구·용인 기흥구) · 비용은 가설")


svg("10_economics.svg", econ())


# ---------------------------------------------------------------- 02 한 장 요약 + 심사 기준별 근거 위치
def summary():
    cols = [("문제", "검사 100여 일 뒤 함몰", "법정 점검 5년, 서울 1년.<tspan x='{x}' dy='22'>그 사이 자라는 얕은 공동을</tspan><tspan x='{x}' dy='22'>아무도 보지 못합니다.</tspan>", "3~5장"),
            ("해법", "같은 길을 약 2개월마다", "PV5가 GPR로 다시 찍고,<tspan x='{x}' dy='22'>달라진 곳만 골라</tspan><tspan x='{x}' dy='22'>현장에서 재확인합니다.</tspan>", "6~7장"),
            ("왜 PV5", "싣고·켜고·고정·복제", "카고룸 4,420L · V2L ·<tspan x='{x}' dy='22'>L-Track · 공식 컨버전 체계로</tspan><tspan x='{x}' dy='22'>같은 탐사실을 여러 대로.</tspan>", "8~9장"),
            ("사업", "이미 있는 예산에서", "큰 지자체 GPR 용역 연 1.4~1.8억.<tspan x='{x}' dy='22'>차량 1대가 2곳을 맡으면</tspan><tspan x='{x}' dy='22'>흑자, 실증은 4단계로.</tspan>", "10~12장")]
    b = ""
    x = 56
    for i, (k, h, d, ref) in enumerate(cols):
        b += f'''  <g id="col{i}" data-pptx-bounds="{x} 168 274 260">
    <rect x="{x}" y="168" width="274" height="3" fill="{NAVY if i else RED}" />
    <text x="{x}" y="202" font-size="16" font-weight="bold" fill="{RED if i == 0 else AMB}">{k}</text>
    <text x="{x}" y="240" font-size="23" font-weight="bold" fill="{NAVY}">{h}</text>
    <text x="{x}" y="282" font-size="17" fill="{SUB}">{d.format(x=x)}</text>
    <text x="{x}" y="372" font-size="14" fill="{MUTE}">자세히 → {ref}</text>
  </g>
'''
        x += 298
    crit = [("기술적 완성도", "30", "6·7·10장"), ("시장 실현성", "25", "11·12장"), ("혁신성", "20", "4·6장"), ("PV5 연계성", "15", "8·9장"), ("사회적 가치", "10", "3·5장")]
    b += f'''  <g id="criteria" data-pptx-bounds="56 440 1168 120">
    <text x="56" y="462" font-size="15" font-weight="bold" fill="{MUTE}">심사 기준별 근거 위치</text>
'''
    x = 56
    for name, pt, ref in crit:
        b += f'''    <rect x="{x}" y="476" width="222" height="76" fill="{PALE}" />
    <text x="{x + 16}" y="506" font-size="17" font-weight="bold" fill="{NAVY}">{name} <tspan font-size="14" font-weight="normal" fill="{MUTE}">{pt}점</tspan></text>
    <text x="{x + 16}" y="536" font-size="16" fill="{SUB}">{ref}</text>
'''
        x += 236
    b += "  </g>\n" + band(590, "한 번의 조기 발견이, 한 사람의 무사 귀가가 되도록.")
    return head("", "한 장 요약") + title("GroundWatch는 탐사와 탐사 ‘사이’의 공백을 메웁니다") + b + foot(2, "심사 배점: 기아 PBV 아이디어 공모전 공식 안내(기술적 완성도 30 · 시장 실현성 25 · 혁신성 20 · PV5 연계성 15 · 사회적 가치 10)")


svg("01b_summary.svg", summary())

# ---------------------------------------------------------------- 파일명·쪽번호를 최종 순서로
names = sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))
tmp = []
for i, f in enumerate(names, 1):
    t = open(os.path.join(OUT, f), encoding="utf-8").read()
    t = re.sub(r"\d\d / \d\d<", f"{i:02d} / {N}<", t)
    os.remove(os.path.join(OUT, f))
    tmp.append((f"{i:02d}_" + f.split("_", 1)[1], t))
for f, t in tmp:
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(t)
print("ok", [f for f, _ in tmp])
