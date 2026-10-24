# v7 근거 장 단순화: "한 장 = 한 메시지 + 그림 또는 큰 숫자 하나". 덜어 낸 세부 수치는 발표자 노트(notes/total.md)에 있다.
# deck.py가 만든 15장(01_cover~15_closing 이름) 중 근거 장을 덮어쓴다. 장 번호는 deck7.py가 다시 매긴다.
import os, re

NAVY, INK, SUB, MUTE, LINE = "#0B1E3C", "#111827", "#374151", "#4B5563", "#E2E6EC"
YEL, AMB, RED = "#F5B700", "#B45309", "#C62828"


def run(G, OUT):
    head, title, band, svg = G["head"], G["title"], G["band"], G["svg"]
    path = lambda f: os.path.join(OUT, f)
    read = lambda f: open(path(f), encoding="utf-8").read()

    def src_group(f):
        """기존 장의 출처·쪽번호 묶음을 그대로 가져온다(출처는 지우지 않는다)."""
        t = read(f)
        s = re.search(r'  <g id="source".*?\n  </g>\n', t, re.S).group(0)
        ft = re.search(r'  <g id="footer".*?\n  </g>\n', t, re.S).group(0)
        return s + ft

    def big(x, y, value, label, size=60, color=NAVY, label2=""):
        s = f'    <text x="{x}" y="{y}" font-size="{size}" font-weight="bold" fill="{color}" letter-spacing="-2">{value}</text>\n'
        s += f'    <text x="{x}" y="{y + 34}" font-size="19" font-weight="bold" fill="{INK}">{label}</text>\n'
        if label2:
            s += f'    <text x="{x}" y="{y + 60}" font-size="16" fill="{MUTE}">{label2}</text>\n'
        return s

    # ---- 3 지금의 탐사: 사진 + 큰 숫자 둘 + 한 문장
    f = "04_current.svg"; tail = src_group(f)
    b = f'''  <g id="photo" data-pptx-bounds="56 160 600 430">
    <image href="../images/gpr_handheld_road.jpg" x="56" y="160" width="600" height="400" preserveAspectRatio="xMidYMid slice" />
    <text x="56" y="584" font-size="13" fill="{MUTE}">수동형 GPR 탐사 장비 · 사진: The Charles Machine Works, CC BY-SA 2.0(배경 편집)</text>
  </g>
  <g id="stats" data-pptx-bounds="712 160 512 420">
{big(712, 236, "33,129km", "서울 누적 GPR 탐사", 64, NAVY, "2014~2025.9")}{big(712, 396, "7,760개", "같은 기간 찾은 공동", 64, NAVY)}    <line x1="712" y1="478" x2="1224" y2="478" stroke="{LINE}" stroke-width="1" />
    <text x="712" y="522" font-size="22" font-weight="bold" fill="{INK}">그런데 같은 길은</text>
    <text x="712" y="556" font-size="22" font-weight="bold" fill="{INK}"><tspan fill="{RED}">다음 정기점검 때</tspan> 다시 봅니다.</text>
  </g>
'''
    svg(f, head("문제", "지금의 탐사") + title("GPR 탐사는 이미 합니다. 한 번 보고 끝날 뿐입니다") + b + tail)

    # ---- 4 맹점: 막대 셋 + 큰 결론 하나
    f = "05_blindspot.svg"; tail = src_group(f)
    b = f'''  <g id="gap-chart" data-pptx-bounds="56 168 700 380">
    <text x="56" y="204" font-size="19" fill="{INK}">법정 공동조사 주기</text>
    <rect x="56" y="218" width="600" height="44" fill="#9AA3AF" />
    <text x="672" y="250" font-size="32" font-weight="bold" fill="{INK}">5년</text>
    <text x="56" y="322" font-size="19" fill="{INK}">서울시가 줄이기로 한 주기 <tspan font-size="15" fill="{MUTE}">(2025.4 발표)</tspan></text>
    <rect x="56" y="336" width="120" height="44" fill="{NAVY}" />
    <text x="192" y="368" font-size="32" font-weight="bold" fill="{NAVY}">1년</text>
    <text x="56" y="440" font-size="19" font-weight="bold" fill="{RED}">연희동: ‘이상 없음’에서 함몰까지</text>
    <rect x="56" y="454" width="35" height="44" fill="{RED}" />
    <text x="107" y="486" font-size="32" font-weight="bold" fill="{RED}">100여 일</text>
  </g>
  <g id="evidence" data-pptx-bounds="792 168 432 380">
    <rect x="792" y="168" width="432" height="3" fill="{NAVY}" />
    <text x="792" y="210" font-size="17" font-weight="bold" fill="{AMB}">같은 공동을 다시 재 보니</text>
    <text x="792" y="300" font-size="76" font-weight="bold" fill="{NAVY}" letter-spacing="-3">21곳 모두</text>
    <text x="792" y="346" font-size="24" font-weight="bold" fill="{INK}">크기가 변해 있었습니다</text>
    <text x="792" y="390" font-size="16" fill="{MUTE}">서울 공동 30곳을 209~989일 뒤 재탐사,</text>
    <text x="792" y="414" font-size="16" fill="{MUTE}">그사이 복구된 9곳 제외 · 인천대 연구(2020)</text>
  </g>
{band(560, "한 번의 탐사는 그 시점만 말해 줍니다. 그 사이의 ‘변화’를 봐야 합니다.")}'''
    svg(f, head("문제", "지금 체계의 맹점") + title("맹점은 탐사가 아니라, 탐사와 탐사 ‘사이’입니다") + b + tail)

    # ---- 5 원인: 단면도 + 45.4% + 대상 한 줄
    f = "06_target.svg"; t = read(f)
    t = re.sub(r'  <g id="scope".*?\n  </g>\n', f'''  <g id="scope" data-pptx-bounds="744 340 480 160">
    <rect x="744" y="352" width="480" height="3" fill="{YEL}" />
    <text x="744" y="396" font-size="24" font-weight="bold" fill="{NAVY}">GroundWatch 대상</text>
    <text x="744" y="436" font-size="24" font-weight="bold" fill="{NAVY}">약 2m 이내의 얕은 공동</text>
    <text x="744" y="474" font-size="17" fill="{MUTE}">깊은 굴착·터널 공사장은 계측이 맡습니다</text>
  </g>
''', t, count=1, flags=re.S)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 9 요약: 칸마다 헤드라인 한 줄 + 숫자 셋
    f = "02_summary.svg"; t = read(f)
    t = re.sub(r'\n    <text x="\d+" y="282" font-size="17" fill="#374151">.*?</text>', "", t)
    t = t.replace('font-size="23" font-weight="bold" fill="#0B1E3C">', 'font-size="24" font-weight="bold" fill="#0B1E3C">')
    t = re.sub(r'(<g id="col\d" data-pptx-bounds="\d+ 168 274) 180"', r'\1 100"', t)
    # 숫자 줄을 위로 당기고 숫자를 키운다, 결론 띠도 함께 올린다
    k = re.search(r'  <g id="keynum".*?\n  </g>\n', t, re.S).group(0)
    k2 = (k.replace('data-pptx-bounds="56 398 1168 120"', 'data-pptx-bounds="56 296 1168 160"').replace('y="420"', 'y="318"')
          .replace('y="434"', 'y="332"').replace('y="480" font-size="32"', 'y="400" font-size="52"').replace('y="508"', 'y="438"'))
    t = t.replace(k, k2)
    t = t.replace('data-pptx-bounds="56 590 1168 44">\n    <rect x="56" y="590"', 'data-pptx-bounds="56 520 1168 44">\n    <rect x="56" y="520"').replace('<text x="76" y="620"', '<text x="76" y="550"')
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 10 해법: B-scan 셋 + 2.4배
    f = "07_solution.svg"; t = read(f)
    t = re.sub(r'  <g id="(diff|proof)".*?\n  </g>\n', "", t, flags=re.S)
    t = re.sub(r'  <g id="conclusion".*?\n  </g>\n', "", t, flags=re.S)
    t = t.replace("  <g id=\"source\"", f'''  <g id="hero" data-pptx-bounds="56 420 1168 170">
    <rect x="56" y="420" width="1168" height="3" fill="{NAVY}" />
    <text x="56" y="526" font-size="88" font-weight="bold" fill="{NAVY}" letter-spacing="-3">2.4배</text>
    <text x="336" y="486" font-size="24" font-weight="bold" fill="{INK}">10cm 자란 공동의 변화 신호가</text>
    <text x="336" y="522" font-size="24" font-weight="bold" fill="{INK}">가장 큰 오탐 요인보다 2.4배 뚜렷합니다</text>
    <text x="336" y="558" font-size="16" fill="{MUTE}">전자기 시뮬레이션 결과이며 현장 정확도가 아닙니다 · 판정은 전문가, 확정은 천공</text>
  </g>
  <g id="source"''', 1)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 11 현장: 5단계 줄을 한 문장으로, 설명 둘째 줄 삭제
    f = "08_field.svg"; t = read(f)
    t = re.sub(r'  <g id="system-chain".*?\n  </g>\n', f'''  <g id="lead" data-pptx-bounds="56 150 1168 70">
    <text x="56" y="196" font-size="24" fill="{SUB}">판독자가 승인한 지점만, <tspan font-weight="bold" fill="{NAVY}">2인 1조가 현장에서 바로</tspan> 다시 확인합니다.</text>
  </g>
''', t, count=1, flags=re.S)
    t = re.sub(r'\n    <text x="(56|640)" y="634" font-size="16" fill="#4B5563">.*?</text>', "", t)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 12 탐사실: 사양 표 → 동사 셋
    f = "09_pv5_lab.svg"; t = read(f)
    rows = [("싣는다", "4,420L · 550kg", "장비 약 300kg [가설]"), ("켠다", "V2L 최대 3.6kW", "장비 1.5kW · 배터리의 14%/일 [가설]"),
            ("연결한다", "PIM · Pleos", "재확인 지점 안내 · 장비 제어 · 여러 대 관제")]
    g = '  <g id="spec" data-pptx-bounds="720 160 504 400">\n'
    y = 200
    for k, v, u in rows:
        g += f'    <rect x="720" y="{y - 40}" width="504" height="3" fill="{NAVY}" />\n'
        g += f'    <text x="720" y="{y}" font-size="18" font-weight="bold" fill="{AMB}">{k}</text>\n'
        g += f'    <text x="720" y="{y + 46}" font-size="34" font-weight="bold" fill="{NAVY}" letter-spacing="-1">{v}</text>\n'
        g += f'    <text x="720" y="{y + 76}" font-size="16" fill="{MUTE}">{u}</text>\n'
        y += 136
    g += "  </g>\n"
    t = re.sub(r'  <g id="spec".*?\n  </g>\n', g, t, count=1, flags=re.S)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 13 왜 PV5: 기능 한 줄씩, 기본 조건·불리한 점은 노트로
    f = "10_why_pv5.svg"; t = read(f)
    feats = [("PBV 컨버전 포털", "모든 차에 같은 위치 장착"), ("PIM · 조인트 블록", "차가 장비 전원·기록을 제어"),
             ("Pleos Fleet", "단말기 없이 여러 도시 관제"), ("적재고 419mm", "카트를 바로 내려 현장 재확인")]
    g = '  <g id="compare" data-pptx-bounds="56 410 1168 110">\n'
    for k, (n, d) in enumerate(feats):
        x = 56 + 298 * k
        g += f'    <rect x="{x}" y="414" width="274" height="3" fill="{NAVY}" />\n'
        g += f'    <text x="{x}" y="452" font-size="21" font-weight="bold" fill="{NAVY}">{n}</text>\n'
        g += f'    <text x="{x}" y="484" font-size="18" fill="{INK}">{d}</text>\n'
    g += "  </g>\n"
    t = re.sub(r'  <g id="compare".*?\n  </g>\n', g, t, count=1, flags=re.S)
    t = re.sub(r'  <g id="kit".*?\n  </g>\n', "", t, count=1, flags=re.S)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 14 검증: 질문 표 삭제, 4단계 상자만 크게
    f = "11_verify.svg"; tail = src_group(f)
    stages = [("1단계", "폐쇄 시험장", "EV와 GPR 전자파 간섭", "차량에서 측정 가능"),
              ("2단계", "통제된 시험 구간", "회차마다 같은 자리를 찍는가", "회차 비교 가능"),
              ("3단계", "실제 도로 위험구간", "AI 선별 · 야간 AR 정확도", "실증확인서"),
              ("4단계", "실제 운영", "운영 지표", "연간 관제 계약")]
    b = '  <g id="stages" data-pptx-bounds="56 170 1168 330">\n'
    for k, (n, place, q, ok) in enumerate(stages):
        x = 56 + 298 * k
        b += f'    <rect x="{x}" y="176" width="274" height="300" fill="#F3F5F8" />\n'
        b += f'    <rect x="{x}" y="176" width="274" height="5" fill="{YEL if k == 3 else NAVY}" />\n'
        b += f'    <text x="{x + 22}" y="226" font-size="18" font-weight="bold" fill="{AMB}">{n}</text>\n'
        b += f'    <text x="{x + 22}" y="270" font-size="26" font-weight="bold" fill="{NAVY}">{place}</text>\n'
        b += f'    <text x="{x + 22}" y="340" font-size="15" font-weight="bold" fill="{MUTE}">확인할 것</text>\n'
        b += f'    <text x="{x + 22}" y="368" font-size="18" fill="{INK}">{q}</text>\n'
        b += f'    <text x="{x + 22}" y="420" font-size="15" font-weight="bold" fill="{MUTE}">통과하면</text>\n'
        b += f'    <text x="{x + 22}" y="448" font-size="18" font-weight="bold" fill="{NAVY}">→ {ok}</text>\n'
    b += "  </g>\n" + band(530, "정확도 숫자를 미리 약속하지 않고, 단계마다 통과 조건을 둡니다.")
    svg(f, head("검증", "기술 실증 계획") + title("남은 질문은 4단계로 확인합니다") + b + tail)

    # ---- 15 원가: 막대 비교 + 4.7만 원
    f = "12_economics.svg"; tail = src_group(f)
    b = f'''  <g id="hero" data-pptx-bounds="56 160 520 260">
    <text x="56" y="200" font-size="17" font-weight="bold" fill="{AMB}">반복 탐사 1회 원가 [가설]</text>
    <text x="56" y="300" font-size="96" font-weight="bold" fill="{NAVY}" letter-spacing="-4">4.7만 원</text>
    <text x="56" y="344" font-size="22" font-weight="bold" fill="{INK}">탐사 연장 1km당</text>
    <text x="56" y="380" font-size="16" fill="{MUTE}">차량 1대 연 3.09억 원 ÷ 6,600km(하루 30km × 220일)</text>
  </g>
  <g id="bars" data-pptx-bounds="640 160 584 300">
    <text x="640" y="200" font-size="17" font-weight="bold" fill="{AMB}">같은 길 1km를 1년 동안</text>
    <text x="640" y="250" font-size="18" fill="{INK}">지금 · 전체 공정 1회</text>
    <rect x="640" y="262" width="360" height="44" fill="#9AA3AF" />
    <text x="1016" y="294" font-size="26" font-weight="bold" fill="{INK}">92만 원</text>
    <text x="640" y="360" font-size="18" fill="{INK}">GroundWatch · 여기에 반복 6회</text>
    <rect x="640" y="372" width="360" height="44" fill="#9AA3AF" />
    <rect x="1000" y="372" width="110" height="44" fill="{NAVY}" />
    <text x="1122" y="404" font-size="26" font-weight="bold" fill="{NAVY}">+28만</text>
  </g>
{band(500, "현행 비용에 약 30%를 더하면, 1년에 한 번 보던 길을 6번 봅니다.")}'''
    svg(f, head("사업", "단가와 수지") + title("반복 탐사는 km당 약 4.7만 원이면 원가가 맞습니다") + b + tail)

    # ---- 16 기아 몫: 위 3칸 설명 줄 삭제
    f = "13_players.svg"; t = read(f)
    t = re.sub(r'\n    <text x="\d+" y="(268|292)" font-size="16" fill="#374151">.*?</text>', "", t)
    t = re.sub(r'(<g id="who\d" data-pptx-bounds="\d+ 168 368) 140"', r'\1 90"', t)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 17 진입: 로드맵 세 줄만
    f = "14_entry.svg"; t = read(f)
    road = [("1~2년", "조사기관과 시·군 용역 공동 수주"), ("2~3년", "혁신제품 지정 → 연간 관제 계약"), ("3년~", "권역별 PV5 플릿 · 상하수도 기관")]
    g = f'''  <g id="next" data-pptx-bounds="736 272 488 300">
    <text x="736" y="294" font-size="15" font-weight="bold" fill="{AMB}">그다음</text>
    <rect x="736" y="304" width="488" height="3" fill="{NAVY}" />
'''
    y = 350
    for k, (when, what) in enumerate(road):
        g += f'    <text x="736" y="{y}" font-size="22" font-weight="bold" fill="{NAVY}">{when}</text>\n'
        g += f'    <text x="836" y="{y}" font-size="19" fill="{INK}">{what}</text>\n'
        y += 64
    g += "  </g>\n"
    t = re.sub(r'  <g id="next".*?\n  </g>\n', g, t, count=1, flags=re.S)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 2 사고: 세부 한 줄(다음 날 30m) 삭제
    f = "03_incident.svg"; t = read(f)
    t = re.sub(r'\n    <text [^>]*>다음 날, 약 30m 옆에서도[^<]*</text>', "", t)
    open(path(f), "w", encoding="utf-8").write(t)


def finalize(G, OUT):
    """제목을 '이 장에서 말하고 싶은 한 문장'으로 짧게 바꾸고 44px로 키운다. 빽빽한 장은 다시 짠다."""
    head, svg, band = G["head"], G["svg"], G["band"]
    path = lambda f: os.path.join(OUT, f)
    read = lambda f: open(path(f), encoding="utf-8").read()

    def keep_tail(t):
        s = re.search(r'  <g id="source".*?\n  </g>\n', t, re.S).group(0)
        return s + re.search(r'  <g id="footer".*?\n  </g>\n', t, re.S).group(0)

    def title(t):
        return f'  <g id="title" data-pptx-bounds="56 78 1168 64" letter-spacing="-1.5">\n    <text x="56" y="128" font-size="44" font-weight="bold" fill="{NAVY}">{t}</text>\n  </g>\n'

    # ---- 9 요약 → 숫자 셋
    f = "02_summary.svg"; tail = keep_tail(read(f))
    nums = [("100여 일", "‘이상 없음’에서 함몰까지", "2024 연희동", RED),
            ("2.4배", "자란 공동이 오탐보다 뚜렷", "전자기 시뮬레이션", NAVY),
            ("최대 88대", "전국 지자체 탐사형 PV5", "차량 매출 약 40억 원", NAVY)]
    b = '  <g id="keynum" data-pptx-bounds="56 190 1168 260">\n'
    for k, (v, l1, l2, c) in enumerate(nums):
        x = 56 + 400 * k
        b += f'    <rect x="{x}" y="200" width="368" height="4" fill="{c}" />\n'
        b += f'    <text x="{x}" y="310" font-size="80" font-weight="bold" fill="{c}" letter-spacing="-3">{v}</text>\n'
        b += f'    <text x="{x}" y="362" font-size="24" font-weight="bold" fill="{INK}">{l1}</text>\n'
        b += f'    <text x="{x}" y="396" font-size="18" fill="{MUTE}">{l2}</text>\n'
    b += "  </g>\n" + band(500, "기아 PV5 AI 순찰차가 도로 위를 본다면, GroundWatch는 도로 아래를 봅니다.")
    svg(f, head("", "한 장 요약") + title("숫자 세 개로 보는 GroundWatch") + b + tail)

    # ---- 13 왜 PV5: 부제·각주 줄 삭제, 기능 글씨 키움
    f = "10_why_pv5.svg"; t = read(f)
    t = re.sub(r'  <g id="lead".*?\n  </g>\n', "", t, flags=re.S)
    t = re.sub(r'\n    <text x="56" y="384"[^\n]*</text>', "", t)
    t = t.replace('font-size="21" font-weight="bold" fill="#0B1E3C">', 'font-size="24" font-weight="bold" fill="#0B1E3C">')
    t = re.sub(r'(<text x="\d+" y="484") font-size="18"', r'\1 font-size="19"', t)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 14 검증: 상자 글씨 키움
    f = "11_verify.svg"; t = read(f)
    t = t.replace('font-size="26" font-weight="bold" fill="#0B1E3C">', 'font-size="28" font-weight="bold" fill="#0B1E3C">')
    t = re.sub(r'(y="(368|448)") font-size="18"', r'\1 font-size="20"', t)
    open(path(f), "w", encoding="utf-8").write(t)

    # ---- 17 진입: 큰 숫자 하나 + 단계 넷
    f = "14_entry.svg"; tail = keep_tail(read(f))
    b = f'''  <g id="hero" data-pptx-bounds="56 180 520 300">
    <text x="56" y="218" font-size="18" font-weight="bold" fill="{AMB}">지자체가 이미 쓰는 GPR 용역 예산 · 2026 낙찰</text>
    <text x="56" y="320" font-size="76" font-weight="bold" fill="{NAVY}" letter-spacing="-3">1~2억 원</text>
    <text x="56" y="366" font-size="22" font-weight="bold" fill="{INK}">안양·강동구·용인, 건당 0.85억~1.90억 원</text>
    <text x="56" y="400" font-size="18" fill="{MUTE}">경기도는 16개 시·군 탐사에 21.6억 원 지원(2025.9)</text>
  </g>
  <g id="road" data-pptx-bounds="640 180 584 320">
    <line x1="652" y1="210" x2="652" y2="437" stroke="{LINE}" stroke-width="2" />
'''
    steps = [("수상 후 6개월", "PV5 실물 대여로 폐쇄 시험장 실증", YEL), ("1~2년", "조사기관과 시·군 용역 공동 수주", NAVY),
             ("2~3년", "혁신제품 지정 → 연간 관제 계약", NAVY), ("3년~", "권역별 PV5 플릿 구매", NAVY)]
    y = 210
    for when, what, c in steps:
        b += f'    <circle cx="652" cy="{y - 7}" r="8" fill="{c}" />\n'
        b += f'    <text x="676" y="{y}" font-size="22" font-weight="bold" fill="{NAVY}">{when}</text>\n'
        b += f'    <text x="676" y="{y + 32}" font-size="19" fill="{INK}">{what}</text>\n'
        y += 78
    b += '  </g>\n'
    b += band(540, "새 예산이 아니라 이미 쓰는 탐사 예산에서, 기아와 함께 첫 실증을 만듭니다.")
    svg(f, head("사업", "첫 고객과 기아와 할 일") + title("지자체 예산에서 바로 시작합니다") + b + tail)

    # ---- 나머지 장: 제목만 짧고 크게
    titles = {"04_current.svg": "탐사는 이미 합니다. 한 번 보고 끝날 뿐입니다",
              "05_blindspot.svg": "문제는 탐사와 탐사 ‘사이’입니다",
              "06_target.svg": "원인 1위 하수관 손상, 땅속 2m 안에 있습니다",
              "07_solution.svg": "같은 길을 다시 찍고, 달라진 곳만 봅니다",
              "08_field.svg": "찾은 지점은 현장에서 바로 확인합니다",
              "09_pv5_lab.svg": "PV5 한 대가 이동형 탐사실이 됩니다",
              "10_why_pv5.svg": "어느 PV5가 재도, 같은 기준으로 잽니다",
              "11_verify.svg": "남은 질문은 4단계로 검증합니다",
              "12_economics.svg": "km당 4.7만 원이면 됩니다",
              "13_players.svg": "기아는 공공 PV5 시장을 엽니다"}
    for f, tt in titles.items():
        t = read(f)
        t, n = re.subn(r'  <g id="title".*?\n  </g>\n', lambda m: title(tt), t, count=1, flags=re.S)
        assert n == 1, f
        open(path(f), "w", encoding="utf-8").write(t)
