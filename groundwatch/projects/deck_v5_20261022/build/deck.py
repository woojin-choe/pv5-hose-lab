# PV5 GroundWatch v5 덱 생성기: 장마다 "한 문장 제목 + 그것을 증명하는 그림 하나" 원칙으로 SVG를 쓴다.
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "svg_output")
N = 12
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
    <text x="56" y="222" font-size="44" fill="{NAVY}">‘이상 없음’ 판정</text>
    <text x="56" y="282" font-size="44" fill="{RED}">3개월 뒤, 도로가 무너졌습니다</text>
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
    <text x="103" y="496" font-size="26" font-weight="bold" fill="{RED}">약 3.5개월</text>
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
svg("04_target.svg", head("문제", "우리가 막을 대상") + title("그 사이 자라는 ‘얕은 공동’이 땅꺼짐 원인 1위입니다") + f'''  <g id="section" data-pptx-bounds="56 160 640 420">
    <image href="../images/ug_section_cut.png" x="56" y="166" width="640" height="407" preserveAspectRatio="xMidYMid meet" />
    <g font-size="15" font-weight="bold">
      <rect x="290" y="214" width="112" height="28" rx="14" fill="{NAVY}" />
      <text x="346" y="233" fill="#FFFFFF" text-anchor="middle">③ 노면 침하</text>
      <rect x="114" y="282" width="112" height="28" rx="14" fill="{NAVY}" />
      <text x="170" y="301" fill="#FFFFFF" text-anchor="middle">② 공동 형성</text>
      <rect x="406" y="340" width="124" height="28" rx="14" fill="{NAVY}" />
      <text x="468" y="359" fill="#FFFFFF" text-anchor="middle">① 하수관 누수</text>
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
svg("05_solution.svg", head("해법", "GroundWatch의 핵심") + title("같은 길을 반복해서 찍고, 달라진 곳만 다시 봅니다") + f'''  <g id="compare" data-pptx-bounds="56 160 680 400">
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
    <text x="808" y="224" font-size="17" fill="{SUB}">PV5가 새벽마다 같은 경로를 주행</text>
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
''' + foot(5, "B-scan 비교 화면은 설명용 예시입니다."))

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
''' + foot(7, "출처: 기아 PV5 카고 가격표·제원·액세서리 · 오토뷰(2026, 공식 컨버전 파트너) · V2L 3.6kW는 해외 제원 · 배치도는 PV5 기반 콘셉트 · 실증 필요: 총중량·전자파"))

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


def port(src, dst, no, step, label, new_title, drops=(), edits=()):
    s = open(os.path.join(V4, src), encoding="utf-8").read()
    s = re.sub(r'  <g id="header".*?\n  </g>\n', head(step, label), s, count=1, flags=re.S)
    s = re.sub(r'(<g id="title"[^>]*>\s*<text [^>]*>)[^<]*(</text>)', lambda m: m.group(1) + new_title + m.group(2), s, count=1)
    for gid in drops:
        s, n = re.subn(r'\n  <g id="%s"[^>]*>.*?\n  </g>' % re.escape(gid), "", s, count=1, flags=re.S)
        assert n == 1, (src, gid)
    for a, b in edits:
        assert a in s, (src, a[:50])
        s = s.replace(a, b)
    s = re.sub(r'\d\d / \d\d<', f"{no:02d} / {N}<", s)
    open(os.path.join(OUT, dst), "w", encoding="utf-8").write(s)


port("08_app_ar.svg", "06_field.svg", 6, "해법", "현장 재확인", "차가 찾은 지점을, 작업자가 현장에서 바로 확인합니다")
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
port("10_validation.svg", "09_verify.svg", 9, "검증", "기술 실증 계획", "남은 질문은 4가지, 4단계로 실증합니다", drops=("evidence",),
     edits=[('<g id="matrix"', '<g id="lead" data-pptx-bounds="56 138 1168 60">\n    <text x="56" y="164" font-size="19" fill="#374151">반복 탐사가 공동 성장을 잡는다는 것은 연구로 확인됐습니다(3장).</text>\n    <text x="56" y="192" font-size="19" font-weight="bold" fill="#0B1E3C">남은 질문은 하나, PV5에 실었을 때도 정확한가입니다.</text>\n  </g>\n  <g id="matrix"')])
port("13_economics.svg", "10_economics.svg", 10, "사업", "시장과 수지", "차량 1대가 자치구 2곳만 맡아도 흑자입니다")
port("14_go_to_market.svg", "11_entry.svg", 11, "사업", "첫 고객과 확장", "이미 GPR 예산을 쓰는 지자체에서 시작합니다")
print("ok")
