# PV5 GroundWatch v5 덱 생성기: 장마다 "한 문장 제목 + 그것을 증명하는 그림 하나" 원칙으로 SVG를 쓴다.
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import vec

OUT = os.path.join(os.path.dirname(__file__), "..", "svg_output")
for _f in os.listdir(OUT):
    if _f.endswith(".svg"):
        os.remove(os.path.join(OUT, _f))
N = 13
NAVY, INK, SUB, MUTE, LINE, PALE = "#0B1E3C", "#111827", "#374151", "#4B5563", "#E2E6EC", "#F3F5F8"
YEL, AMB, RED = "#F5B700", "#B45309", "#C62828"
STEPS = ["문제", "해법", "PV5", "검증", "사업"]


def head(step, label, nav=True):
    """왼쪽: 브랜드 칩 + 장 이름. 오른쪽: 이야기 진행 표시(현재 단계만 진하게)."""
    s = f'''  <g id="header" data-pptx-role="header" data-pptx-bounds="56 24 1168 40">
    <rect x="56" y="28" width="140" height="24" fill="{NAVY}" />
    <text x="126" y="45" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">PV5 GroundWatch</text>
    <text x="210" y="45" font-size="14" fill="{SUB}">{label}</text>
'''
    x = 900
    for i, name in enumerate(STEPS if nav else []):
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
    <text x="56" y="682" font-size="13" fill="{MUTE}">{src}</text>
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
  <rect id="cover-bg" x="0" y="0" width="1280" height="720" fill="{NAVY}" />
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
  <g id="cover-tagline" data-pptx-bounds="64 456 560 92">
    <rect x="64" y="460" width="48" height="3" fill="{YEL}" />
    <text x="64" y="502" font-size="21" fill="#D7DEE8">지표투과레이더(GPR)로 같은 길을 반복해서 보고,<tspan x="64" dy="32">구멍이 되기 전의 변화를 찾습니다.</tspan></text>
  </g>
  <g id="cover-team" data-pptx-bounds="64 600 440 72" font-weight="bold">
    <text x="64" y="622" font-size="14" fill="{YEL}">TEAM</text>
    <text x="64" y="656" font-size="22" fill="#FFFFFF">한 명이라도 살릴 수 있다면</text>
  </g>
  <g id="cover-date" data-pptx-bounds="980 658 260 40">
    <text x="1232" y="672" font-size="11" fill="#C3CCD9" text-anchor="end">PV5 기반 콘셉트 이미지</text>
    <text x="1232" y="692" font-size="13" fill="#C3CCD9" text-anchor="end">2026. 10</text>
  </g>
''', role="cover")

# ---------------------------------------------------------------- 02 사고
svg("02_incident.svg", head("문제", "실제로 일어난 일", nav=False) + f'''  <defs>
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
    <rect x="86" y="399" width="540" height="10" fill="{YEL}" fill-opacity="0.28" />
    <line x1="86" y1="404" x2="626" y2="404" stroke="#C3CCD9" stroke-width="2" />
    <circle cx="86" cy="404" r="10" fill="{NAVY}" stroke="#FFFFFF" stroke-width="3" />
    <circle cx="626" cy="404" r="10" fill="{RED}" stroke="#FFFFFF" stroke-width="3" />
    <text x="76" y="358" font-size="16" font-weight="bold" fill="{NAVY}">2024. 5. 7~16</text>
    <text x="76" y="380" font-size="15" fill="{SUB}">정기 GPR 탐사 · 공동 없음</text>
    <text x="636" y="358" font-size="16" font-weight="bold" fill="{RED}" text-anchor="end">2024. 8. 29</text>
    <text x="636" y="380" font-size="15" fill="{RED}" text-anchor="end">도로 함몰</text>
    <text x="356" y="444" font-size="16" fill="{SUB}" text-anchor="middle">그 사이 지하에서 무슨 일이 있었는지는 기록이 없습니다</text>
  </g>
  <g id="facts" data-pptx-bounds="56 488 600 110">
    <line x1="56" y1="492" x2="636" y2="492" stroke="{LINE}" stroke-width="1" />
    <text x="56" y="548" font-size="40" font-weight="bold" fill="{INK}">6×4m</text>
    <text x="56" y="576" font-size="15" fill="{SUB}">함몰 규모</text>
    <text x="250" y="548" font-size="40" font-weight="bold" fill="{INK}">2.5m</text>
    <text x="250" y="576" font-size="15" fill="{SUB}">함몰 깊이</text>
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
    <text x="56" y="256" font-size="18" fill="{INK}">법정 공동조사 주기 <tspan font-size="15" fill="{SUB}">(하수관 등 관리자)</tspan></text>
    <rect x="56" y="270" width="600" height="34" fill="#9AA3AF" />
    <text x="668" y="296" font-size="26" font-weight="bold" fill="{INK}">5년</text>
    <text x="56" y="356" font-size="18" fill="{INK}">서울시가 줄인 정기점검 주기 <tspan font-size="15" fill="{SUB}">(2025.4)</tspan></text>
    <rect x="56" y="370" width="120" height="34" fill="{NAVY}" />
    <text x="188" y="396" font-size="26" font-weight="bold" fill="{NAVY}">1년</text>
    <text x="56" y="456" font-size="18" font-weight="bold" fill="{RED}">연희동: 탐사 ‘이상 없음’에서 함몰까지</text>
    <rect x="56" y="470" width="35" height="34" fill="{RED}" />
    <text x="103" y="496" font-size="26" font-weight="bold" fill="{RED}">100여 일</text>
  </g>
  <g id="evidence" data-pptx-bounds="784 168 440 384">
    <rect x="784" y="168" width="440" height="3" fill="{NAVY}" />
    <text x="784" y="204" font-size="15" font-weight="bold" fill="{AMB}">그 사이 공동은 자랍니다</text>
    <text x="784" y="250" font-size="26" font-weight="bold" fill="{NAVY}">“예상보다 단기간에</text>
    <text x="784" y="286" font-size="26" font-weight="bold" fill="{NAVY}">공동이 성장할 수 있다”</text>
    <text x="784" y="330" font-size="16" fill="{SUB}">일본 국토교통성 위탁연구</text>
    <text x="784" y="352" font-size="16" fill="{SUB}">(도쿄대·지오서치, 2018~2020 · 원문 번역)</text>
    <line x1="784" y1="380" x2="1224" y2="380" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="414" font-size="16" fill="{INK}">같은 도로를 반복 모니터링하자</text>
    <text x="784" y="438" font-size="16" fill="{INK}">지하 1.64m 하수관 위 공동이</text>
    <text x="784" y="462" font-size="16" fill="{INK}">급격히 자란 것이 확인됐습니다.</text>
    <line x1="784" y1="486" x2="1224" y2="486" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="518" font-size="16" fill="{INK}">연희동 공동을 놓쳤는지, 그 뒤 생겼는지는</text>
    <text x="784" y="542" font-size="16" font-weight="bold" fill="{NAVY}">한 번의 탐사로는 구분할 수 없습니다.</text>
  </g>
  {band(566, "한 번의 탐사는 그 시점만 말해 줍니다. 그 사이의 ‘변화’를 봐야 합니다.").strip()}
''' + foot(3, "출처: 지하안전법(지하시설물관리자 공동조사 5년 1회 이상) · 이투데이(2025.4.23) · 뉴시스(2024.8.30) · 일본 국토교통성 도로정책 연구 30-5(2021)"))

# ---------------------------------------------------------------- 04 대상
svg("04_target.svg", head("문제", "우리가 막을 대상") + title("땅꺼짐 원인 1위는 하수관 손상, 그 위 2m가 탐사 대상입니다") + f'''  <g id="section" data-pptx-bounds="56 160 640 420">
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
    <text x="744" y="404" font-size="16" fill="{SUB}">공동이 먼저 생겨 자람 → 반복 측정으로 잡을 수 있음</text>
    <rect x="744" y="440" width="480" height="3" fill="#C3CCD9" />
    <text x="744" y="478" font-size="19" font-weight="bold" fill="{MUTE}">심부 붕괴형 · 예: 명일동 16m → 대상 아님</text>
    <text x="744" y="504" font-size="16" fill="{SUB}">깊은 지층·터널 공사 영역은 공사장 계측이 맡음</text>
  </g>
  {band(600, "차량형 GPR이 보는 깊이(약 2m)에, 가장 흔한 원인이 있습니다.").strip()}
''' + foot(4, "출처: 국토교통부 지반침하 원인 통계(2020~2024) · 국토교통부 명일동 사고조사(2025.12.3) · 서울시 차량형 GPR 탐사 깊이 약 2m · 단면도는 원리 설명용"))

# ---------------------------------------------------------------- 05 해법
svg("05_solution.svg", head("해법", "GroundWatch의 핵심") + title("같은 길을 약 2개월마다 다시 찍고, 달라진 곳만 다시 봅니다") + f'''  <g id="compare" data-pptx-bounds="56 160 680 400">
    <rect x="56" y="166" width="680" height="388" fill="#2A2E33" />
    <image href="../images/sim_prev.png" x="56" y="166" width="680" height="192" preserveAspectRatio="none" />
    <image href="../images/sim_cur.png" x="56" y="362" width="680" height="192" preserveAspectRatio="none" />
    <rect x="68" y="178" width="96" height="28" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="116" y="198" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">지난 회차</text>
    <rect x="68" y="374" width="96" height="28" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="116" y="394" font-size="16" font-weight="bold" fill="#FFFFFF" text-anchor="middle">이번 회차</text>
    <rect x="300" y="452" width="300" height="96" fill="none" stroke="{YEL}" stroke-width="4" />
    <rect x="300" y="424" width="150" height="28" fill="{YEL}" />
    <text x="375" y="444" font-size="16" font-weight="bold" fill="{NAVY}" text-anchor="middle">새로 커진 신호</text>
  </g>
  <g id="steps" data-pptx-bounds="784 166 440 388">
    <text x="784" y="196" font-size="15" font-weight="bold" fill="{MUTE}">1</text>
    <text x="808" y="196" font-size="22" font-weight="bold" fill="{NAVY}">반복 측정</text>
    <text x="808" y="224" font-size="17" fill="{SUB}">PV5가 새벽에 같은 경로를 약 2개월마다 주행</text>
    <line x1="784" y1="252" x2="1224" y2="252" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="292" font-size="15" font-weight="bold" fill="{MUTE}">2</text>
    <text x="808" y="292" font-size="22" font-weight="bold" fill="{NAVY}">변화만 선별</text>
    <text x="808" y="320" font-size="17" fill="{SUB}">회차 차분으로 달라진 곳을 고르고(7장)</text>
    <text x="808" y="344" font-size="17" fill="{SUB}">AI가 신호 유형을 분류, 전문가가 승인</text>
    <line x1="784" y1="372" x2="1224" y2="372" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="412" font-size="15" font-weight="bold" fill="{MUTE}">3</text>
    <text x="808" y="412" font-size="22" font-weight="bold" fill="{NAVY}">현장 재확인</text>
    <text x="808" y="440" font-size="17" fill="{SUB}">승인된 곳만 수동 GPR로 다시 보고</text>
    <text x="808" y="464" font-size="17" fill="{SUB}">필요하면 천공·내시경으로 확정</text>
    <line x1="784" y1="492" x2="1224" y2="492" stroke="{LINE}" stroke-width="1" />
    <text x="784" y="530" font-size="17" fill="{INK}">결과는 다음 순찰 경로에 다시 반영됩니다.</text>
  </g>
  {band(590, "자동 선별은 볼 순서만 정하고, 판정은 전문가가, 확정은 천공이 합니다.").strip()}
''' + foot(5, "약 2개월 = 차량 1대가 연 6,600km를 달려 도로 약 1,000km를 연 6회 반복(11장, 가설) · 회차 화면은 2D 전자기 시뮬레이션 결과(7장)"))

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
    <text x="776" y="474" font-size="15" fill="{MUTE}">컨버전 포털: 차량 3D 데이터·인증자료 → 같은 사양 여러 대</text>
    <rect x="776" y="504" width="448" height="76" fill="{PALE}" />
    <text x="796" y="534" font-size="15" font-weight="bold" fill="{AMB}">그래도 여유 있습니다 <tspan font-weight="normal" fill="{MUTE}">[가설]</tspan></text>
    <text x="796" y="562" font-size="16" fill="{INK}">장비 약 300kg / 600kg · 전력 약 1.5kW / 3.6kW</text>
  </g>
''' + foot(7, "차량형 GPR 장착(하부형·후방형)은 배터리 팩·지상고 간섭 시험 후 확정 · 출처: 기아 PV5 카고 제원·액세서리, 오토뷰(2026.1.28, 컨버전 포털) · V2L 3.6kW는 해외 제원 · 배치도는 콘셉트"))

# ---------------------------------------------------------------- 12 마무리
svg("12_closing.svg", f'''  <defs>
    <linearGradient id="closeFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="1" />
      <stop offset="55%" stop-color="{NAVY}" stop-opacity="0.85" />
      <stop offset="100%" stop-color="{NAVY}" stop-opacity="0" />
    </linearGradient>
  </defs>
  <rect x="0" y="0" width="1280" height="720" fill="{NAVY}" />
  <image href="../images/close_pv5_rear_b.jpg" x="560" y="0" width="720" height="720" preserveAspectRatio="xMidYMid slice" />
  <rect x="560" y="0" width="420" height="720" fill="url(#closeFade)" />
  <g id="recap" data-pptx-bounds="64 80 620 360">
    <text x="64" y="104" font-size="16" font-weight="bold" fill="{YEL}">GroundWatch가 바꾸는 것</text>
    <text x="64" y="150" font-size="20" fill="#9FB0C8">회차마다 따로 보는 탐사</text>
    <text x="64" y="182" font-size="25" font-weight="bold" fill="#FFFFFF">→ 같은 길의 ‘변화’를 보는 탐사</text>
    <text x="64" y="228" font-size="20" fill="#9FB0C8">다시 찾아가야 하는 의심 지점</text>
    <text x="64" y="260" font-size="25" font-weight="bold" fill="#FFFFFF">→ 같은 차에서 바로 재탐사</text>
    <text x="64" y="306" font-size="20" fill="#9FB0C8">장비를 실은 차</text>
    <text x="64" y="338" font-size="25" font-weight="bold" fill="#FFFFFF">→ 업무에 연동된 PV5 탐사실</text>
    <text x="64" y="384" font-size="20" fill="#9FB0C8">기아에게</text>
    <text x="64" y="416" font-size="25" font-weight="bold" fill="#FFFFFF">→ 공공 탐사용 PV5 플릿 (최대 약 97대)</text>
  </g>
  <g id="closing" data-pptx-bounds="64 474 620 150">
    <rect x="64" y="480" width="48" height="3" fill="{YEL}" />
    <text x="64" y="540" font-size="38" font-weight="bold" fill="#FFFFFF">한 번의 조기 발견이,<tspan x="64" dy="52">한 사람의 무사 귀가가 되도록.</tspan></text>
  </g>
  <g id="footer" data-pptx-role="footer" data-pptx-bounds="64 662 1172 48">
    <text x="64" y="700" font-size="14" font-weight="bold" fill="{YEL}">TEAM 한 명이라도 살릴 수 있다면</text>
    <text x="64" y="676" font-size="11" fill="#9FB0C8">사진: Alexander Migl, CC BY-SA 4.0(편집)</text>
    <text x="1232" y="700" font-size="13" font-weight="bold" fill="{YEL}" text-anchor="end">12 / {N}</text>
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
    s = re.sub(r'(<g id="source"[^>]*>\s*<text [^>]*?)font-size="12"', r'\1font-size="13"', s)
    open(os.path.join(OUT, dst), "w", encoding="utf-8").write(s)


port("08_app_ar.svg", "06_field.svg", 6, "해법", "현장 재확인", "차가 찾은 지점을, 작업자가 현장에서 바로 확인합니다", regex_drop=r'\n      <g font-size="13" fill="#4B5563">.*?</g>',
     edits=[('추정 깊이 0.9~1.3m · AI 신뢰도 84%', '추정 깊이 0.9~1.3m · 지난 회차 대비 신규'),
            ('rx="8" fill="#0B1E3C" />', 'rx="8" fill="#FFFFFF" stroke="#0B1E3C" stroke-width="2" />'),
            ('font-weight="bold" fill="#FFFFFF">GroundWatch Cloud', 'font-weight="bold" fill="#0B1E3C">GroundWatch Cloud'),
            ('font-weight="bold" fill="#FFFFFF">Patrol 차량 앱', 'font-weight="bold" fill="#0B1E3C">Patrol 차량 앱'),
            ('font-weight="bold" fill="#FFFFFF">Edge Gateway', 'font-weight="bold" fill="#0B1E3C">Edge Gateway'),
            ('font-size="14" fill="#D6DDE8">4D', 'font-size="14" fill="#374151">4D'),
            ('font-size="14" fill="#D6DDE8">업무', 'font-size="14" fill="#374151">업무'),
            ('font-size="14" fill="#D6DDE8">센서', 'font-size="14" fill="#374151">센서')])
port("09_why_pv5.svg", "08_why_pv5.svg", 8, "PV5", "왜 PV5인가", "가격이 아니라 구조 때문에 PV5입니다",
     regex_drop=None,
     edits=[('<text x="232" y="362" font-size="24" font-weight="bold" fill="#0B1E3C">4,520만 원</text>', '<text x="232" y="362" font-size="21" fill="#0B1E3C">4,520만 원</text>'),
            ('<text x="232" y="414" font-size="24" font-weight="bold" fill="#0B1E3C">377km</text>', '<text x="232" y="414" font-size="21" fill="#0B1E3C">377km</text>'),
            ("오토뷰(2026, PV5 공식 컨버전 파트너·포털)", "오토뷰(2026.1.28, PV5 컨버전 포털)"),
            ('<rect x="452" y="446" width="376" height="134" fill="#F3F5F8" />', ''),
            ('<text x="472" y="474" font-size="15" font-weight="bold" fill="#0B1E3C">PV5 공식 컨버전 체계</text>', ''),
            ('<text x="472" y="500" font-size="15" fill="#111827">국내 특장 파트너 10개사 선정<tspan x="472" dy="21">PBV 컨버전 포털: 3D CAD·기술 가이드</tspan><tspan x="472" dy="21">12V 전력 연결 블록·PIM 기본 적용</tspan><tspan x="472" dy="21">→ GPR 키트 표준화의 바탕</tspan></text>', ''),
            ('<rect x="848" y="446" width="376" height="134" fill="#F3F5F8" />', '<rect x="652" y="446" width="572" height="134" fill="#F3F5F8" />'),
            ('<rect x="56" y="446" width="376" height="134" fill="#F3F5F8" />', '<rect x="56" y="446" width="572" height="134" fill="#F3F5F8" />'),
            ('<text x="868" y="474"', '<text x="672" y="474"'),
            ('<text x="868" y="500" font-size="15" fill="#111827">주행거리는 스타리아보다 10km 짧고,<tspan x="868" dy="21">전폭은 포터·봉고보다 155mm 넓습니다.</tspan><tspan x="868" dy="21">→ 하루 순찰 약 30km <tspan fill="#4B5563">[가설]</tspan>에는</tspan><tspan x="868" dy="21">377km로 충분합니다.</tspan></text>',
             '<text x="672" y="500" font-size="16" fill="#111827">주행거리는 스타리아보다 10km 짧고, 전폭은 포터·봉고보다<tspan x="672" dy="24">155mm 넓습니다. 하루 순찰 약 30km <tspan fill="#4B5563">[가설]</tspan>에는</tspan><tspan x="672" dy="24">377km로 충분합니다.</tspan></text>'),
            ('<text x="76" y="500" font-size="15" fill="#111827">차값 차이는 최대 1,354만 원,<tspan x="76" dy="21">차량형 GPR은 대당 <tspan font-weight="bold">2억~8억 원</tspan>.</tspan><tspan x="76" dy="21">차이를 가르는 건 구조와</tspan><tspan x="76" dy="21">지원 체계입니다.</tspan></text>',
             '<text x="76" y="500" font-size="16" fill="#111827">차값 차이는 최대 1,354만 원인데, 차량형 GPR은<tspan x="76" dy="24">대당 <tspan font-weight="bold">2억~8억 원</tspan>(서울시 약 5억)입니다.</tspan><tspan x="76" dy="24">차이를 가르는 건 전원·고정 구조와 컨버전 체계입니다.</tspan></text>')])
port("14_go_to_market.svg", "11_entry.svg", 11, "사업", "첫 고객과 확장", "이미 GPR 예산을 쓰는 지자체에서 시작합니다",
     edits=[(">0.46~1.77억 원<", ">0.85~1.90억 원<"),
            (">보령·안양·용인(기흥구) 낙찰, 이미 집행 중<", ">안양·강동구·용인 등 낙찰, 이미 집행 중<"),
            ("자치구 2곳 연간 계약", "지자체 2곳 연간 계약"),
            ("출처: 나라장터 2026 GPR 용역 낙찰(보령·안양·용인 기흥구)", "출처: 나라장터 2026 GPR 용역(안양 R26BK01572949 · 강동구 R26BK01599467 · 용인 R26BK01517362)")])
print("ok")


# ---------------------------------------------------------------- 09 실증: 질문 4개 + 단계 4개
def verify():
    rows = [("EV 구동계와 GPR의 전자파 간섭", "차량에서 측정 자체가 불가", "주행·정차·V2L 상태별 잡음 비교"),
            ("회차마다 같은 자리를 찍는가", "변화 비교가 불가", "8cm 어긋남이 최대 오탐(6장) → RTK·IMU 정합"),
            ("AI가 변화를 맞게 고르는가", "재확인 출동이 과다", "시뮬레이션 통과(6장) → 공동 모사체 실측"),
            ("밤에 AR이 정확히 맞는가", "현장 탐색 범위가 커짐", "맨홀·경계석 기준점 오차 측정")]
    b = f'''  <g id="lead" data-pptx-bounds="56 138 1168 28">
    <text x="56" y="160" font-size="19" fill="{SUB}">공동이 단기간에 자랄 수 있다는 것은 연구로 확인됐습니다(4장). 남은 건 <tspan font-weight="bold" fill="{NAVY}">PV5에 실었을 때도 정확한가</tspan>입니다.</text>
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
        t1, t2 = NAVY, AMB
        b += f'''    <rect x="{x}" y="480" width="278" height="94" fill="{PALE}" />
    <rect x="{x}" y="480" width="278" height="4" fill="{YEL if i == 3 else NAVY}" />
    <text x="{x + 18}" y="508" font-size="14" font-weight="bold" fill="{t2}">{n} · {q}</text>
    <text x="{x + 18}" y="536" font-size="20" font-weight="bold" fill="{t1}">{place}</text>
    <text x="{x + 18}" y="562" font-size="15" fill="{t1}">{ok}</text>
'''
        if i < 3:
            b += f'    <text x="{x + 286}" y="536" font-size="18" fill="{MUTE}">›</text>\n'
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
    <text x="56" y="552" font-size="15" fill="{SUB}">비용 = PV5·GPR(2억~5억, 서울시 대당 약 5억) 5년 감가 + 2인 인건비 1억 + 유지 0.3억 · 하루 30km×220일 → 도로 1,000km를 약 2개월마다</text>
    <text x="56" y="576" font-size="15" fill="{SUB}"><tspan font-weight="bold" fill="{RED}">핵심 가설</tspan> 지자체는 지금 예산 그대로, 우리는 차이만 판독해 같은 돈으로 연 1회 → 연 6회 → 실증 3·4단계</text>
  </g>
'''
    b += band(600, "비용은 연 약 2억 원. 지자체 2곳부터 수입이 비용을 넘습니다.")
    return head("사업", "시장과 수지") + title("차량 1대가 지자체 2곳만 맡아도 흑자입니다") + b + foot(
        10, "출처: e-나라지표 · 머니투데이(2025.12.23) · 뉴스서울(2025.12.3) · 시사저널(2025.4.25) · 나라장터 개찰 · 헤럴드경제(2025.9.7) · 첫 해는 조사기관과 공동 수행 · 비용은 가설")


svg("10_economics.svg", econ())


# ---------------------------------------------------------------- 02 한 장 요약 + 심사 기준별 근거 위치
def summary():
    cols = [("문제", "탐사 100여 일 뒤 함몰", "법정 점검 5년, 서울 1년.<tspan x='{x}' dy='22'>그 사이 자라는 얕은 공동을</tspan><tspan x='{x}' dy='22'>아무도 보지 못합니다.</tspan>", "3~5장"),
            ("해법", "같은 길을 약 2개월마다", "PV5가 GPR로 다시 찍고,<tspan x='{x}' dy='22'>달라진 곳만 골라</tspan><tspan x='{x}' dy='22'>현장에서 재확인합니다.</tspan>", "6~7장"),
            ("왜 PV5", "차가 업무의 일부가 됨", "차량 내비·화면과 연동하고,<tspan x='{x}' dy='22'>V2L·L-Track으로 싣고 고정,</tspan><tspan x='{x}' dy='22'>공식 컨버전으로 복제.</tspan>", "8~9장"),
            ("사업", "같은 길을 6번, 1회의 1/3", "현행 km당 92만 원 vs<tspan x='{x}' dy='22'>반복 탐사 원가 4.7만 원.</tspan><tspan x='{x}' dy='22'>실증은 4단계로.</tspan>", "10~12장")]
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
    keyn = [("100여 일", "‘이상 없음’ 탐사에서 함몰까지 (연희동)"), ("2.4배", "10cm 자란 공동 vs 가장 큰 오탐 요인 (시뮬레이션)"), ("92만 → 28만 원", "도로 1km·1년: 현행 1회 vs 반복 6회")]
    b += f'''  <g id="keynum" data-pptx-bounds="56 440 1168 120">
    <text x="56" y="462" font-size="15" font-weight="bold" fill="{MUTE}">숫자 셋으로 보면</text>
'''
    x = 56
    for v, k in keyn:
        b += f'''    <rect x="{x}" y="476" width="376" height="3" fill="{NAVY}" />
    <text x="{x}" y="522" font-size="32" font-weight="bold" fill="{NAVY}">{v}</text>
    <text x="{x}" y="550" font-size="15" fill="{SUB}">{k}</text>
'''
        x += 396
    b += "  </g>\n" + band(590, "한 번의 조기 발견이, 한 사람의 무사 귀가가 되도록.")
    return head("", "한 장 요약") + title("GroundWatch는 탐사와 탐사 ‘사이’의 공백을 메웁니다") + b + foot(2, "근거: 3장 뉴시스·세계일보 · 6장 GPR 전자기 시뮬레이션 · 11장 서울시 2024 공동조사용역 최종보고서")


svg("01b_summary.svg", summary())

# ---------------------------------------------------------------- 07 혁신+증거: 기존 모니터링과의 차이, 시뮬레이션 검증
def innovation():
    b = f"""  <g id="compare" data-pptx-bounds="56 160 560 420">
    <text x="56" y="186" font-size="15" font-weight="bold" fill="{MUTE}">기존 모니터링 (후지사와시·연구)</text>
    <text x="330" y="186" font-size="15" font-weight="bold" fill="{NAVY}">GroundWatch</text>
    <line x1="56" y1="198" x2="616" y2="198" stroke="{NAVY}" stroke-width="1.5" />
"""
    rows = [("다시 보는 곳", "이미 발견한 공동만", "‘이상 없음’ 구간까지 전체"),
            ("판정 방식", "회차마다 따로 판독", "지난 회차와 맞춰 뺀 차이만"),
            ("주기", "연구 노선 3개월 · 시 5년 계획", "업무 노선 약 2개월 [가설]"),
            ("현장 확인", "별도 정밀조사 발주", "같은 차에서 바로 재탐사")]
    y = 236
    for k, a, g in rows:
        b += f"""    <text x="56" y="{y - 22}" font-size="13" font-weight="bold" fill="{MUTE}">{k}</text>
    <text x="56" y="{y + 4}" font-size="17" fill="{SUB}">{a}</text>
    <text x="330" y="{y + 4}" font-size="17" font-weight="bold" fill="{NAVY}">{g}</text>
    <line x1="56" y1="{y + 22}" x2="616" y2="{y + 22}" stroke="{LINE}" stroke-width="1" />
"""
        y += 84
    b += "  </g>\n"
    b += f"""  <g id="evidence" data-pptx-bounds="656 160 568 420">
    <text x="656" y="186" font-size="15" font-weight="bold" fill="{AMB}">검증 · GPR 전자기 시뮬레이션 (실측 아님)</text>
    <image href="../images/sim_diff.png" x="656" y="200" width="274" height="196" preserveAspectRatio="xMidYMid slice" />
    <image href="../images/sim_ctrl.png" x="950" y="200" width="274" height="196" preserveAspectRatio="xMidYMid slice" />
    <rect x="662" y="206" width="132" height="24" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="728" y="223" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">공동이 자란 회차</text>
    <rect x="956" y="206" width="154" height="24" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="1033" y="223" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">변화 없는 회차(대조군)</text>
    <text x="656" y="446" font-size="34" font-weight="bold" fill="{NAVY}">2,831</text>
    <text x="656" y="470" font-size="15" fill="{SUB}">변화로 표시된 화소</text>
    <text x="950" y="446" font-size="34" font-weight="bold" fill="{MUTE}">25</text>
    <text x="950" y="470" font-size="15" fill="{SUB}">같은 기준의 오탐 화소 (약 1/113)</text>
    <line x1="656" y1="490" x2="1224" y2="490" stroke="{LINE}" stroke-width="1" />
    <text x="656" y="520" font-size="17" fill="{INK}">위치 오차 <tspan font-weight="bold" fill="{NAVY}">3cm</tspan> (추정 3.97m · 실제 4.00m)</text>
    <text x="656" y="548" font-size="17" fill="{INK}">깊이 오차 <tspan font-weight="bold" fill="{RED}">17cm</tspan> (추정 1.05m · 실제 0.88m) → 실측 보정 과제</text>
  </g>
"""
    b += band(596, "연구로 효과가 확인된 반복 모니터링을, 도로 전체의 상시 업무로 만듭니다.")
    return head("해법", "무엇이 새로운가") + title("새 장비가 아니라 ‘변화를 판정하는 방법’이 새롭습니다") + b + foot(
        7, "시뮬레이션: 2D 전자기 파동 계산(FDTD) · 400MHz · 토양 εr 9 · Ø0.8m 하수관 위 공동 반경 18→38cm · 함수비·잡음 변화 포함 · 출처: 후지사와시·지오서치 모니터링 보고(2025) · 일본 국토교통성 30-5")


svg("05b_innovation.svg", innovation())


# ---------------------------------------------------------------- 10 PV5 연동: 기아가 공개한 기능에만 근거
def pv5link():
    b = f"""  <g id="lead" data-pptx-bounds="56 138 1168 28">
    <text x="56" y="160" font-size="18" fill="{SUB}">기아가 공개한 PV5 기능만 썼습니다. 실제 권한·범위는 기아 PBV 파트너 승인 후 확정합니다.</text>
  </g>
  <g id="photo" data-pptx-bounds="56 182 520 380">
    <image href="../images/pv5_v2l_kr.jpg" x="56" y="182" width="520" height="380" preserveAspectRatio="xMidYMid slice" />
    <rect x="66" y="192" width="214" height="26" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="173" y="210" font-size="14" font-weight="bold" fill="#FFFFFF" text-anchor="middle">[화면 예시] 장비 전원 · PIM 제어</text>
  </g>
  <g id="links" data-pptx-bounds="616 182 608 380">
"""
    rows = [("Navihelper", "내비 목적지·경로 연계", "재확인 지점·순찰 경로를 차량 내비로 바로 안내"),
            ("Vehicle API", "충전 상태·도어 등 차량 정보", "배터리 하한에서 장비 전원 정리, 문 열면 현장 모드"),
            ("Gleo AI", "음성 명령·음성 인식", "운전자는 손 떼지 않고 ‘침하 의심’ 음성 기록"),
            ("PIM 제어기·12V 블록", "IVI로 외부 전장 장비 제어", "차량 화면에서 GPR·작업등을 켜고 끔"),
            ("Pleos App Market", "검증 후 지원 차종에 배포", "다른 지자체 PV5에 같은 앱을 설치")]
    y = 204
    for i, (k, f, u) in enumerate(rows):
        b += f"""    <text x="616" y="{y}" font-size="19" font-weight="bold" fill="{NAVY}">{k} <tspan font-size="14" font-weight="normal" fill="{MUTE}">{f}</tspan></text>
    <text x="616" y="{y + 26}" font-size="16" fill="{INK}">→ {u}</text>
"""
        if i < 4:
            b += f'    <line x1="616" y1="{y + 44}" x2="1224" y2="{y + 44}" stroke="{LINE}" stroke-width="1" />\n'
        y += 76
    b += "  </g>\n" + band(590, "장비를 싣는 것을 넘어, PV5에서는 차가 탐사 업무의 일부가 됩니다.")
    return head("PV5", "PV5와 연결되는 지점") + title("GroundWatch는 PV5의 소프트웨어·전장 구조에 꽂힙니다") + b + foot(
        10, "출처: 기아 PBV 아이디어 공모전 솔루션 부문 안내(Pleos Connect SDK·Vehicle API·Navihelper·Gleo AI·App Market) · 오토뷰(2026.1.28, PIM 제어기·12V 조인트 블록)")


svg("07b_pv5link.svg", pv5link())

# ---------------------------------------------------------------- 14b 기아와 함께: 수요 대수 추정 + 요청 사항
def withkia():
    b = f"""  <g id="volume" data-pptx-bounds="56 160 540 400">
    <text x="56" y="186" font-size="15" font-weight="bold" fill="{AMB}">기아에게 생기는 수요 (계산)</text>
    <rect x="56" y="200" width="540" height="3" fill="{NAVY}" />
    <text x="56" y="268" font-size="64" font-weight="bold" fill="{NAVY}" letter-spacing="-2">약 97대</text>
    <text x="56" y="300" font-size="17" fill="{INK}">지자체 관리 도로 전 구간을 약 2개월마다 볼 때(최대치)</text>
    <text x="56" y="324" font-size="15" fill="{SUB}">96,712km ÷ 차량 1대 담당 약 1,000km</text>
    <line x1="56" y1="352" x2="596" y2="352" stroke="{LINE}" stroke-width="1" />
    <text x="56" y="400" font-size="34" font-weight="bold" fill="{NAVY}">약 8대</text>
    <text x="230" y="392" font-size="17" fill="{INK}">서울 도로 8,342km만 맡을 때</text>
    <text x="56" y="452" font-size="34" font-weight="bold" fill="{NAVY}">2.5억~5.5억</text>
    <text x="300" y="444" font-size="17" fill="{INK}">장비 포함 PV5 1대<tspan x="300" dy="22" font-size="15" fill="{SUB}">GPR 2억~5억 + 차량</tspan></text>
    <text x="56" y="500" font-size="15" fill="{SUB}">대수는 많지 않지만, 대당 가격이 높고 공공 레퍼런스가 되는</text>
    <text x="56" y="522" font-size="15" fill="{SUB}">‘PV5 + 업무 앱’ 패키지의 첫 사례입니다.</text>
  </g>
  <g id="ask" data-pptx-bounds="656 160 568 400">
    <text x="656" y="186" font-size="15" font-weight="bold" fill="{AMB}">수상 후 기아와 함께 할 첫 6개월</text>
    <rect x="656" y="200" width="568" height="3" fill="{NAVY}" />
"""
    asks = [("PV5 실물 1대", "1단계 폐쇄 시험장 실증", "공모전 혜택: 우수작 PV5 대여 검토"),
            ("Pleos Playground·SDK", "Navihelper·Vehicle API 연동 시제품", "Pleos Playground: 공개 개발자 환경(SDK 문서·도구)"),
            ("컨버전 포털·PIM 기술 지원", "GPR 장착 위치·전원 간섭 검토", "기아 컨버전 포털(3D 데이터·인증자료)"),
            ("지자체 파일럿 연결", "2단계 통제 구간 → 3단계 실제 도로", "공모전 혜택: PoC·사업화 연계, 전문가 멘토링")]
    y = 236
    for i, (k, d, src) in enumerate(asks):
        b += f"""    <text x="656" y="{y}" font-size="15" font-weight="bold" fill="{MUTE}">{i + 1}</text>
    <text x="680" y="{y}" font-size="20" font-weight="bold" fill="{NAVY}">{k}</text>
    <text x="680" y="{y + 26}" font-size="16" fill="{INK}">→ {d}</text>
    <text x="680" y="{y + 50}" font-size="13" fill="{MUTE}">{src}</text>
"""
        if i < 3:
            b += f'    <line x1="656" y1="{y + 66}" x2="1224" y2="{y + 66}" stroke="{LINE}" stroke-width="1" />\n'
        y += 84
    b += "  </g>\n" + band(590, "기아가 이미 약속한 혜택만으로, 6개월 안에 1단계 실증 결과를 가져옵니다.")
    return head("사업", "기아와 함께 할 일") + title("기아가 지원하면, 6개월 안에 첫 실증을 보여드립니다") + b + foot(
        15, "대수는 계산값(차량 1대 연 6,600km 가설 기준) · 지원 항목 출처: 기아 PBV 아이디어 공모전 안내(PoC·사업화 연계, PV5 대여 검토, 멘토링) · 일정은 목표 [가설]")


svg("11b_withkia.svg", withkia())





# ================================================================ 압축본: 같은 이야기를 하는 장을 합친다
def solution2():
    b = f"""  <g id="scans" data-pptx-bounds="56 150 1168 250">
"""
    imgs = [("sim_prev.png", "지난 회차"), ("sim_cur.png", "이번 회차"), ("sim_diff.png", "자동 선별된 차이")]
    x = 56
    for i, (f, lab) in enumerate(imgs):
        b += f"""    <image href="../images/{f}" x="{x}" y="156" width="360" height="200" preserveAspectRatio="none" />
    <rect x="{x + 8}" y="164" width="{len(lab) * 15 + 20}" height="26" rx="3" fill="{NAVY}" fill-opacity="0.9" />
    <text x="{x + 18}" y="182" font-size="15" font-weight="bold" fill="#FFFFFF">{lab}</text>
"""
        if i < 2:
            b += f'    <text x="{x + 385}" y="268" font-size="34" font-weight="bold" fill="{NAVY}" text-anchor="middle">{"−" if i == 0 else "="}</text>\n'
        x += 404
    b += f"""    <text x="56" y="382" font-size="16" fill="{SUB}"><tspan font-weight="bold" fill="{NAVY}">1 반복 측정</tspan> 새벽에 같은 경로를 약 2개월마다   <tspan font-weight="bold" fill="{NAVY}">2 변화만 선별</tspan> 위치를 맞춰 빼고, AI가 신호 유형 분류   <tspan font-weight="bold" fill="{NAVY}">3 현장 재확인</tspan> 승인된 곳만 수동 GPR</text>
  </g>
  <g id="diff" data-pptx-bounds="56 410 560 170">
    <rect x="56" y="412" width="560" height="3" fill="{NAVY}" />
    <text x="56" y="442" font-size="15" font-weight="bold" fill="{AMB}">무엇이 새로운가 <tspan font-weight="normal" fill="{MUTE}">기존 → GroundWatch</tspan></text>
    <text x="56" y="474" font-size="16" fill="{SUB}">다시 보는 곳</text>
    <text x="196" y="474" font-size="16" fill="{MUTE}">발견한 공동만 →</text>
    <text x="340" y="474" font-size="17" font-weight="bold" fill="{NAVY}">‘이상 없음’ 구간까지</text>
    <text x="56" y="508" font-size="16" fill="{SUB}">판정 방식</text>
    <text x="196" y="508" font-size="16" fill="{MUTE}">회차마다 판독 →</text>
    <text x="340" y="508" font-size="17" font-weight="bold" fill="{NAVY}">지난 회차와의 차이만</text>
    <text x="56" y="542" font-size="16" fill="{SUB}">현장 확인</text>
    <text x="196" y="542" font-size="16" fill="{MUTE}">별도 발주 →</text>
    <text x="340" y="542" font-size="17" font-weight="bold" fill="{NAVY}">같은 차에서 바로</text>
    <text x="56" y="570" font-size="13" fill="{MUTE}">기존: 일본 후지사와시·지오서치 경과관찰, 국토교통성 연구(3개월 주기)</text>
  </g>
  <g id="proof" data-pptx-bounds="664 410 560 176">
    <rect x="664" y="412" width="560" height="3" fill="{NAVY}" />
    <text x="664" y="438" font-size="15" font-weight="bold" fill="{AMB}">검증 · 전자기 시뮬레이션 (실측 아님) <tspan font-weight="normal" fill="{MUTE}">변화 신호 세기</tspan></text>
    <text x="664" y="466" font-size="14" fill="{SUB}">공동 20cm 성장</text>
    <rect x="808" y="454" width="343" height="15" fill="{NAVY}" />
    <text x="1159" y="466" font-size="14" font-weight="bold" fill="{INK}">2.9</text>
    <text x="664" y="487" font-size="14" fill="{SUB}">공동 10cm 성장</text>
    <rect x="808" y="475" width="293" height="15" fill="{NAVY}" />
    <text x="1109" y="487" font-size="14" font-weight="bold" fill="{INK}">2.4</text>
    <text x="664" y="508" font-size="14" fill="{SUB}">공동 5cm 성장</text>
    <rect x="808" y="496" width="163" height="15" fill="{AMB}" />
    <text x="979" y="508" font-size="14" font-weight="bold" fill="{INK}">1.4</text>
    <text x="664" y="529" font-size="14" fill="{SUB}">주행선 8cm 어긋남</text>
    <rect x="808" y="517" width="120" height="15" fill="{RED}" />
    <text x="936" y="529" font-size="14" font-weight="bold" fill="{INK}">1.0</text>
    <text x="664" y="550" font-size="14" fill="{SUB}">함수비 변화</text>
    <rect x="808" y="538" width="97" height="15" fill="{MUTE}" />
    <text x="936" y="550" font-size="14" font-weight="bold" fill="{INK}">0.8</text>
    <text x="664" y="571" font-size="14" fill="{SUB}">재포장</text>
    <rect x="808" y="559" width="40" height="15" fill="{MUTE}" />
    <text x="936" y="571" font-size="14" font-weight="bold" fill="{INK}">0.3</text>
    <line x1="928" y1="450" x2="928" y2="580" stroke="{RED}" stroke-width="1.5" stroke-dasharray="4,3" />
  </g>
"""
    b += band(596, "10cm 이상 자란 공동은 오탐 요인의 2배 넘는 신호, 5cm는 경계 — 주행선 정합이 관건입니다.")
    return head("해법", "GroundWatch의 핵심") + title("같은 길을 약 2개월마다 다시 찍고, 달라진 곳만 봅니다") + b + foot(
        6, "시뮬레이션: 2D 전자기 파동 계산(FDTD) · 400MHz · Ø0.8m 하수관 위 공동 반경 18cm 기준 · 세기 = 회차 차분 에너지 ÷ 가장 큰 오탐 요인 · 판정은 전문가, 확정은 천공")


_S = 620 / 1672
CA, CB, CC = (56 + _S * 545, 150 + _S * 418), (56 + _S * 1060, 150 + _S * 330), (56 + _S * 1390, 150 + _S * 330)
CD = (56 + _S * 1195, 150 + _S * 795)
CA, CB, CC = [tuple(round(v) for v in c) for c in (CA, CB, CC)]


def pv5lab2():
    b = f"""  <g id="cutaway" data-pptx-bounds="56 160 640 420">
    <image href="../images/cutaway_nowheel.png" x="56" y="150" width="620" height="349" preserveAspectRatio="xMidYMid meet" />
    <g font-size="16" font-weight="bold" text-anchor="middle">
      <circle cx="{CA[0]}" cy="{CA[1]}" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="{CA[0]}" y="{CA[1] + 6}" fill="{NAVY}">A</text>
      <circle cx="{CB[0]}" cy="{CB[1]}" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="{CB[0]}" y="{CB[1] + 6}" fill="{NAVY}">B</text>
      <circle cx="{CC[0]}" cy="{CC[1]}" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="{CC[0]}" y="{CC[1] + 6}" fill="{NAVY}">C</text>
      <circle cx="{CD[0]}" cy="{CD[1]}" r="17" fill="{YEL}" stroke="{NAVY}" stroke-width="2" />
      <text x="{CD[0]}" y="{CD[1] + 6}" fill="{NAVY}">D</text>
    </g>
    <text x="56" y="522" font-size="15" fill="{INK}"><tspan font-weight="bold" fill="{NAVY}">A</tspan> 분석 장비 랙 (엣지 컴퓨터·GPR 제어)   <tspan font-weight="bold" fill="{NAVY}">B</tspan> 수동 GPR·AR 글래스</text>
    <text x="56" y="546" font-size="15" fill="{INK}"><tspan font-weight="bold" fill="{NAVY}">C</tspan> 내시경·안전장비   <tspan font-weight="bold" fill="{NAVY}">D</tspan> 바닥 아래 차량형 다채널 GPR</text>
    <text x="56" y="572" font-size="13" fill="{MUTE}">콘셉트 이미지 · GPR 장착 위치는 배터리 팩 간섭 시험 후 확정</text>
  </g>
  <g id="spec" data-pptx-bounds="696 150 528 430">
    <g font-size="13" font-weight="bold" fill="{MUTE}">
      <text x="696" y="166">탐사실에 필요한 것</text>
      <text x="866" y="166">PV5에서 확인된 사양</text>
    </g>
    <line x1="696" y1="178" x2="1224" y2="178" stroke="{NAVY}" stroke-width="1.5" />
"""
    rows = [("장비 적재", "카고룸 4,420L · 최대 적재 600kg", "장비 약 300kg + 2인 약 150kg [가설]"),
            ("장비 전원", "실내·실외 V2L (최대 3.6kW, 해외 제원)", "시동 없이 GPR·컴퓨터 운용"),
            ("같은 위치 고정", "L-Track·몰리 패널 (순정 액세서리)", "회차마다 같은 자리에 장착"),
            ("차량과 연동", "PIM 제어기 · Pleos Connect 내비 API", "재확인 지점 안내, 화면에서 장비 제어"),
            ("여러 대 복제", "컨버전 포털 (차량 3D 데이터·인증자료)", "같은 사양의 탐사실을 지자체별로")]
    y = 214
    for i, (k, v, u) in enumerate(rows):
        b += f"""    <text x="696" y="{y}" font-size="17" font-weight="bold" fill="{NAVY}">{k}</text>
    <text x="866" y="{y}" font-size="16" fill="{INK}">{v}</text>
    <text x="866" y="{y + 24}" font-size="14" fill="{SUB}">{u}</text>
"""
        if i < 4:
            b += f'    <line x1="696" y1="{y + 44}" x2="1224" y2="{y + 44}" stroke="{LINE}" stroke-width="1" />\n'
        y += 76
    b += "  </g>\n" + band(598, "장비를 싣는 것을 넘어, PV5에서는 차가 탐사 업무의 일부가 됩니다.")
    return head("PV5", "PV5 이동형 탐사실") + title("PV5 한 대에 탐사실이 들어가고, 차량과 연결됩니다") + b + foot(
        8, "출처: 기아 PV5 카고 제원·액세서리 · 공모전 솔루션 부문 안내(Pleos Connect) · 오토뷰(2026.1.28) · V2L 3.6kW 해외 제원 · 내부 배치는 콘셉트")


def entry2():
    b = f"""  <g id="facts" data-pptx-bounds="56 146 1168 104">
"""
    facts = [("0.85~1.90억 원", "2026 지자체 GPR 용역 낙찰액", "안양·강동구·용인, 이미 집행 중"),
             ("21.6억 원", "경기도 16개 시·군 탐사 지원", "장비 대신 용역으로 1,080km (2025.9)"),
             ("최대 약 97대", "기아 PV5 수요 (계산)", "차량 매출 최대 약 44억 원 · 서울만 약 8대")]
    x = 56
    for v, k, d in facts:
        b += f"""    <rect x="{x}" y="148" width="376" height="3" fill="{NAVY}" />
    <text x="{x}" y="196" font-size="30" font-weight="bold" fill="{AMB}">{v}</text>
    <text x="{x}" y="222" font-size="16" font-weight="bold" fill="{NAVY}">{k}</text>
    <text x="{x}" y="244" font-size="14" fill="{SUB}">{d}</text>
"""
        x += 396
    b += "  </g>\n"
    b += f"""  <g id="ask" data-pptx-bounds="56 272 640 300">
    <text x="56" y="294" font-size="15" font-weight="bold" fill="{AMB}">수상 후 첫 6개월 · 기아가 안내한 혜택으로</text>
    <rect x="56" y="304" width="640" height="3" fill="{NAVY}" />
"""
    asks = [("PV5 실물 대여", "1단계 폐쇄 시험장 실증"), ("Pleos Playground·SDK", "내비·차량 연동 시제품"),
            ("컨버전 포털·PIM 기술 지원", "GPR 장착·전원 간섭 검토"), ("PoC·사업화 연계, 멘토링", "지자체 1곳 파일럿 연결")]
    y = 340
    for i, (k, d) in enumerate(asks):
        b += f"""    <text x="56" y="{y}" font-size="15" font-weight="bold" fill="{MUTE}">{i + 1}</text>
    <text x="80" y="{y}" font-size="19" font-weight="bold" fill="{NAVY}">{k}</text>
    <text x="380" y="{y}" font-size="17" fill="{INK}">→ {d}</text>
"""
        if i < 3:
            b += f'    <line x1="56" y1="{y + 22}" x2="696" y2="{y + 22}" stroke="{LINE}" stroke-width="1" />\n'
        y += 56
    b += f"""  </g>
  <g id="next" data-pptx-bounds="736 272 488 300">
    <text x="736" y="294" font-size="15" font-weight="bold" fill="{AMB}">그다음</text>
    <rect x="736" y="304" width="488" height="3" fill="{NAVY}" />
    <text x="736" y="340" font-size="19" font-weight="bold" fill="{NAVY}">1~2년 <tspan font-weight="normal" fill="{INK}">조사기관과 시·군 용역 공동 수주</tspan></text>
    <text x="736" y="396" font-size="19" font-weight="bold" fill="{NAVY}">2~3년 <tspan font-weight="normal" fill="{INK}">혁신제품 지정 → 연간 관제 계약</tspan></text>
    <text x="736" y="452" font-size="19" font-weight="bold" fill="{NAVY}">3년~ <tspan font-weight="normal" fill="{INK}">권역별 PV5 플릿 · 상하수도 기관</tspan></text>
    <text x="736" y="508" font-size="15" fill="{SUB}">조달청 혁신제품: 지정 시 최대 6년 수의계약</text>
    <text x="736" y="530" font-size="15" fill="{SUB}">테스트베드서울: 과제당 최대 2억 원 실증</text>
  </g>
"""
    b += band(596, "새 예산이 아니라 지자체가 이미 쓰는 탐사 예산에서, 기아와 함께 첫 실증을 만듭니다.")
    return head("사업", "첫 고객과 기아와 할 일") + title("지자체 예산에서 시작해, 6개월 안에 1단계 실증을 마칩니다") + b + foot(
        12, "출처: 나라장터 2026(R26BK01572949 · R26BK01599467 · R26BK01517362) · 헤럴드경제(2025.9.7) · 조달청 · 테스트베드서울 · 공모전 안내 · 일정은 목표")


for _f in ["05b_innovation.svg", "07b_pv5link.svg", "11b_withkia.svg"]:
    _p = os.path.join(OUT, _f)
    if os.path.exists(_p):
        os.remove(_p)


def econ3():
    b = f"""  <g id="now" data-pptx-bounds="56 146 1168 96">
    <rect x="56" y="148" width="1168" height="3" fill="{NAVY}" />
    <text x="56" y="182" font-size="15" font-weight="bold" fill="{AMB}">지금의 실제 단가 · 서울시 2024 지반침하 특별점검 공동조사용역</text>
    <text x="56" y="226" font-size="36" font-weight="bold" fill="{NAVY}">17.8억 원 ÷ 1,930.6km = km당 약 92만 원</text>
    <text x="900" y="214" font-size="15" fill="{SUB}">1·2차 탐사, 천공 499곳,</text>
    <text x="900" y="236" font-size="15" fill="{SUB}">공동 복구 285곳 포함 · 1회</text>
  </g>
  <g id="cost" data-pptx-bounds="56 262 560 300">
    <text x="56" y="286" font-size="16" font-weight="bold" fill="{NAVY}">GroundWatch 차량 1대 연간 원가 <tspan font-weight="normal" fill="{MUTE}">[가설]</tspan></text>
    <line x1="56" y1="298" x2="616" y2="298" stroke="{NAVY}" stroke-width="1.5" />
"""
    rows = [("PV5 카고 4,520만 원 · 5년", "0.09억"), ("차량형 GPR 5억 원(서울시 구매가) · 5년", "1.00억"),
            ("현장 2인 (운전·안전 / 탐사)", "1.20억"), ("판독 전문가 0.5인", "0.40억"), ("수동 GPR·AR·클라우드·보험·유지", "0.40억")]
    y = 326
    for k, v in rows:
        b += f"""    <text x="56" y="{y}" font-size="16" fill="{INK}">{k}</text>
    <text x="616" y="{y}" font-size="16" font-weight="bold" fill="{INK}" text-anchor="end">{v}</text>
    <line x1="56" y1="{y + 12}" x2="616" y2="{y + 12}" stroke="{LINE}" stroke-width="1" />
"""
        y += 36
    b += f"""    <text x="56" y="{y + 10}" font-size="18" font-weight="bold" fill="{NAVY}">합계 약 3.1억 원 ÷ 연 6,600km</text>
    <text x="616" y="{y + 10}" font-size="22" font-weight="bold" fill="{NAVY}" text-anchor="end">km당 약 4.7만 원</text>
    <text x="56" y="{y + 36}" font-size="14" fill="{MUTE}">6,600km = 하루 30km × 220일 (실제 장비 탐사 속도는 20~30km/h)</text>
  </g>
  <g id="compare" data-pptx-bounds="664 262 560 300">
    <text x="664" y="286" font-size="16" font-weight="bold" fill="{NAVY}">같은 도로 1km를 1년 동안</text>
    <line x1="664" y1="298" x2="1224" y2="298" stroke="{NAVY}" stroke-width="1.5" />
    <text x="664" y="334" font-size="16" fill="{INK}">현행 전체 공정 1회</text>
    <rect x="664" y="344" width="460" height="34" fill="#9AA3AF" />
    <text x="1134" y="368" font-size="18" font-weight="bold" fill="{INK}">92만</text>
    <text x="664" y="412" font-size="16" fill="{INK}">GroundWatch 반복 탐사 6회 (약 2개월마다)</text>
    <rect x="664" y="422" width="141" height="34" fill="{NAVY}" />
    <text x="815" y="446" font-size="18" font-weight="bold" fill="{NAVY}">28만 <tspan font-size="14" font-weight="normal" fill="{MUTE}">(4.7만 × 6)</tspan></text>
    <text x="664" y="490" font-size="16" fill="{INK}">천공·복구 같은 2차 조사는</text>
    <text x="664" y="514" font-size="16" font-weight="bold" fill="{NAVY}">변화가 나온 곳에만, 지금 단가대로</text>
  </g>
"""
    b += band(596, "현행 1회 전체 탐사비의 약 3분의 1로, 같은 길을 1년에 6번 봅니다.")
    return head("사업", "단가와 수지") + title("반복 탐사는 km당 약 5만 원이면 원가가 맞습니다") + b + foot(
        11, "출처: 서울시 「지반침하 특별점검 공동조사용역 최종보고서」(2024.10, 사업비 1,780,900,000원·수행 1,930.6km) · 이투데이(2025.4.23, 차량형 GPR 3대 15억 원) · 원가는 가설")


svg("10_economics.svg", econ3())

svg("05_solution.svg", solution2())

# ================================================================ 현장 사양(장착 상세) — 현장 실무자용
def mount():
    sc = 0.40
    fig, an = vec.mount_figure(70, 146, sc)
    b = f"""  <g id="drawing" data-pptx-bounds="56 150 720 420">
{fig}"""
    calls = [("RTK 안테나", an["rtk"], (640, 168)), ("다채널 GPR (후방)", an["gpr"], (680, 560)),
             ("배터리 팩 (바닥 아래)", an["battery"], (200, 560)), ("휠 인코더", an["enc"], (470, 560))]
    for t, (ax, ay), (lx, ly) in calls:
        b += f'    <line x1="{ax:.1f}" y1="{ay:.1f}" x2="{lx:.1f}" y2="{ly - 6:.1f}" stroke="{NAVY}" stroke-width="1" />\n'
        b += f'    <text x="{lx:.1f}" y="{ly + 10 if ly > 300 else ly - 10:.1f}" font-size="14" font-weight="bold" fill="{NAVY}" text-anchor="middle">{t}</text>\n'
    b += "  </g>\n"
    b += f"""  <g id="spec" data-pptx-bounds="800 150 424 430">
    <line x1="800" y1="160" x2="1224" y2="160" stroke="{NAVY}" stroke-width="1.5" />
"""
    rows = [("GPR 장비", "다채널 400MHz · 탐사 깊이 약 2m", "서울시 2024 용역 장비 기준, 폭은 차폭 1,895mm 안으로 [설계]"),
            ("장착 위치", "바닥 아래 배터리 팩을 피해 뒤 차축 뒤", "구조변경은 기아 컨버전 파트너를 거쳐 진행"),
            ("탐사 속도", "시속 20~30km", "서울시 2024 용역 장비의 적정 탐사 속도"),
            ("위치 정합", "RTK 수평 8mm+1ppm + IMU·휠 인코더", "RTK를 GPR 바로 위에 두어 위치 오차 최소화"),
            ("정합 목표", "회차 간 주행선 어긋남 8cm 이내", "6장: 8cm 어긋남이 가장 큰 오탐 요인")]
    y = 192
    for i, (k, v, u) in enumerate(rows):
        b += f"""    <text x="800" y="{y}" font-size="14" font-weight="bold" fill="{AMB}">{k}</text>
    <text x="800" y="{y + 24}" font-size="17" font-weight="bold" fill="{NAVY}">{v}</text>
    <text x="800" y="{y + 46}" font-size="14" fill="{SUB}">{u}</text>
"""
        if i < 4:
            b += f'    <line x1="800" y1="{y + 60}" x2="1224" y2="{y + 60}" stroke="{LINE}" stroke-width="1" />\n'
        y += 78
    b += "  </g>\n" + band(598, "배터리 팩을 피해 뒤에 달고, 위치 기준인 RTK를 GPR 바로 위에 둡니다.")
    return head("PV5", "현장 사양 · 장착 상세") + title("현장 사양: 배터리를 피해 뒤에 달고, GPR 위에 RTK를 둡니다") + b + foot(
        9, "치수: 기아 PV5 카고 롱 공식 제원 · 배터리 바닥 장착(Autocar) · GPR: 서울시 2024 용역 보고서 · RTK: 측량용 수신기 제조사 사양 · 실루엣 비율 근사")




# ================================================================ 현장 재확인 — 같은 톤의 벡터 화면 예시
def app_screen(x, y, w=560, h=300):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="#0F1A2B" />\n'
    mx, my, mw, mh = x + 16, y + 44, 320, h - 60
    s += f'<text x="{x + 18}" y="{y + 28}" font-size="15" font-weight="bold" fill="#FFFFFF">GroundWatch Patrol</text>\n'
    s += f'<text x="{x + w - 18}" y="{y + 28}" font-size="13" fill="#9FB0C8" text-anchor="end">04:42 · 배터리 86%</text>\n'
    s += f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="8" fill="#1B2638" />\n'
    for i in range(1, 6):
        s += f'<line x1="{mx}" y1="{my + i * mh / 6:.1f}" x2="{mx + mw}" y2="{my + i * mh / 6 + 8:.1f}" stroke="#2C3A52" stroke-width="5" />\n'
        s += f'<line x1="{mx + i * mw / 6:.1f}" y1="{my}" x2="{mx + i * mw / 6 - 10:.1f}" y2="{my + mh}" stroke="#2C3A52" stroke-width="5" />\n'
    pts = [(mx + 30, my + 200), (mx + 110, my + 168), (mx + 190, my + 140), (mx + 230, my + 80), (mx + 290, my + 40)]
    s += '<polyline points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts) + '" fill="none" stroke="#4E9BEA" stroke-width="6" stroke-linejoin="round" />\n'
    s += '<polyline points="' + " ".join(f"{a:.0f},{b:.0f}" for a, b in pts[:3]) + '" fill="none" stroke="#3BA55C" stroke-width="6" stroke-linejoin="round" />\n'
    for (a, b2), c, n in [(pts[1], YEL, "1"), (pts[3], YEL, "2"), (pts[4], RED, "3")]:
        s += f'<circle cx="{a}" cy="{b2}" r="11" fill="{c}" stroke="#0F1A2B" stroke-width="2" />\n<text x="{a}" y="{b2 + 5}" font-size="13" font-weight="bold" fill="#0F1A2B" text-anchor="middle">{n}</text>\n'
    rx0 = mx + mw + 14; rw = w - (rx0 - x) - 16
    rows = [("오늘 순찰", "38.4km"), ("재확인 지점", "3곳"), ("GPR·게이트웨이", "연결됨")]
    for i, (k, v) in enumerate(rows):
        ry = my + i * 48
        s += f'<rect x="{rx0}" y="{ry}" width="{rw}" height="40" rx="6" fill="#1B2638" />\n'
        s += f'<text x="{rx0 + 10}" y="{ry + 25}" font-size="13" fill="#9FB0C8">{k}</text>\n<text x="{rx0 + rw - 10}" y="{ry + 25}" font-size="14" font-weight="bold" fill="{"#5AD27A" if i == 2 else "#FFFFFF"}" text-anchor="end">{v}</text>\n'
    s += f'<rect x="{rx0}" y="{my + 150}" width="{rw}" height="{mh - 150}" rx="8" fill="{YEL}" />\n'
    s += f'<text x="{rx0 + rw / 2:.0f}" y="{my + 150 + (mh - 150) / 2 + 7:.0f}" font-size="18" font-weight="bold" fill="#0F1A2B" text-anchor="middle">순찰 시작</text>\n'
    return s


def ar_view(x, y, w=560, h=300):
    s = '<g>\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#1B2433" />\n'
    hz = y + 92
    s += f'<rect x="{x}" y="{y}" width="{w}" height="{hz - y}" fill="#263247" />\n'
    for i in range(6):
        bx = x + 14 + i * 50
        s += f'<rect x="{bx}" y="{hz - 30 - (i % 3) * 14}" width="40" height="{30 + (i % 3) * 14}" fill="#33405A" />\n'
        s += f'<rect x="{x + w - 54 - i * 48}" y="{hz - 26 - (i % 2) * 16}" width="38" height="{26 + (i % 2) * 16}" fill="#33405A" />\n'
    cxh = x + w / 2
    s += f'<path d="M{cxh - 40},{hz} L{cxh + 40},{hz} L{x + w},{y + h - 30} L{x + w},{y + h} L{x},{y + h} L{x},{y + h - 30} Z" fill="#3A3F47" />\n'
    s += f'<path d="M{cxh - 3},{hz} L{cxh + 3},{hz} L{cxh + 9},{y + h} L{cxh - 9},{y + h} Z" fill="{YEL}" />\n'
    s += f'<line x1="{cxh - 40}" y1="{hz}" x2="{x}" y2="{y + h - 30}" stroke="#D9DDE3" stroke-width="3" />\n'
    sx0, sy0, sy1 = cxh + 30, y + 170, y + 240
    s += f'<path d="M{sx0},{sy0} L{sx0 + 90},{sy0} L{sx0 + 140},{sy1} L{sx0 - 10},{sy1} Z" fill="{YEL}" fill-opacity="0.28" stroke="{YEL}" stroke-width="2.5" />\n'
    for t in (0.33, 0.66):
        yy = sy0 + (sy1 - sy0) * t
        s += f'<line x1="{sx0 - 10 * t:.0f}" y1="{yy:.0f}" x2="{sx0 + 90 + 50 * t:.0f}" y2="{yy:.0f}" stroke="{YEL}" stroke-width="1.2" stroke-dasharray="5,4" />\n'
    s += f'<ellipse cx="{cxh - 70}" cy="{y + 262}" rx="48" ry="14" fill="#4B5563" stroke="#FFFFFF" stroke-width="2.5" />\n'
    s += '</g>\n'
    s += f'<rect x="{x}" y="{y}" width="{w}" height="24" fill="{RED}" fill-opacity="0.92" />\n'
    s += f'<text x="{x + w / 2:.0f}" y="{y + 17}" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">GPR 기반 추정 위치 · 굴착 전 정밀조사와 승인 필요</text>\n'
    s += f'<rect x="{x + 14}" y="{y + 36}" width="236" height="52" rx="6" fill="#0B1E3C" fill-opacity="0.9" />\n'
    s += f'<text x="{x + 26}" y="{y + 58}" font-size="14" font-weight="bold" fill="#FFFFFF">재확인 R-0427 · 재탐사 3/4회</text>\n'
    s += f'<text x="{x + 26}" y="{y + 78}" font-size="13" fill="#D6DDE8">추정 깊이 0.9~1.3m · 신규 변화</text>\n'
    s += f'<text x="{cxh - 70}" y="{y + h - 8}" font-size="13" font-weight="bold" fill="#FFFFFF" text-anchor="middle">기준점 · 맨홀</text>\n'
    s += f'<text x="{sx0 + 64}" y="{sy0 - 10}" font-size="14" font-weight="bold" fill="{YEL}" text-anchor="middle">재탐사 범위</text>\n'
    return s


def field2():
    b = f"""  <g id="chain" data-pptx-bounds="56 146 1168 56">
"""
    chain = ["클라우드 · 4D 지도", "PV5 차량 앱", "엣지 게이트웨이", "AR 글래스", "수동 GPR"]
    x = 56
    for i, c in enumerate(chain):
        b += f'    <rect x="{x}" y="150" width="204" height="44" rx="6" fill="#FFFFFF" stroke="{NAVY}" stroke-width="1.5" />\n'
        b += f'    <text x="{x + 102}" y="178" font-size="16" font-weight="bold" fill="{NAVY}" text-anchor="middle">{c}</text>\n'
        if i < 4:
            b += f'    <text x="{x + 218}" y="180" font-size="18" fill="{NAVY}" text-anchor="middle">→</text>\n'
        x += 241
    b += "  </g>\n"
    b += f"""  <g id="screens" data-pptx-bounds="56 216 1168 370">
{app_screen(56, 222)}
{ar_view(664, 222)}
    <text x="56" y="552" font-size="18" font-weight="bold" fill="{INK}">운전석 · PV5 화면의 Patrol 앱 <tspan font-size="14" font-weight="normal" fill="{MUTE}">[화면 예시]</tspan></text>
    <text x="56" y="578" font-size="15" fill="{SUB}">오늘의 순찰 경로와 재확인 지점, 장비 연결 상태</text>
    <text x="664" y="552" font-size="18" font-weight="bold" fill="{INK}">차 밖 · 작업자 AR 글래스 <tspan font-size="14" font-weight="normal" fill="{MUTE}">[화면 예시]</tspan></text>
    <text x="664" y="578" font-size="15" fill="{SUB}">두 손으로 수동 GPR을 미는 동안 재탐사 범위를 표시</text>
  </g>
"""
    b += band(600, "2인 1조로, 운전자는 주행 중 AR을 쓰지 않고, 정차 후 작업자만 씁니다.")
    return head("해법", "현장 재확인") + title("차가 찾은 지점을, 작업자가 현장에서 바로 확인합니다") + b + foot(
        7, "AR은 공동의 실제 모양이 아니라 재탐사 범위만 안내 · 앱 배포와 차량 데이터 접근은 기아 PBV 파트너 승인 필요 · 화면은 예시")



svg("07_pv5_lab.svg", pv5lab2())
svg("11_entry.svg", entry2())

# ---------------------------------------------------------------- 파일명·쪽번호를 최종 순서로
names = sorted(f for f in os.listdir(OUT) if f.endswith(".svg"))
tmp = []
for i, f in enumerate(names, 1):
    t = open(os.path.join(OUT, f), encoding="utf-8").read()
    t = re.sub(r"\d\d / \d\d<", f"{i:02d} / {N}<", t)
    t = t.replace('<text x="56" y="708">', '<text x="56" y="706">').replace('<text x="1224" y="708" text-anchor="end">', '<text x="1224" y="706" text-anchor="end">')
    t = t.replace('<text x="56" y="280">차체 성격</text>', '<text x="56" y="278">차체 성격</text>')
    t = re.sub(r'<text x="56" y="70[68]">한 명이라도 살릴 수 있다면</text>', '<text x="56" y="706">PV5 GroundWatch</text>', t)
    os.remove(os.path.join(OUT, f))
    tmp.append((f"{i:02d}_" + f.split("_", 1)[1], t))
for f, t in tmp:
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(t)
print("ok", [f for f, _ in tmp])
