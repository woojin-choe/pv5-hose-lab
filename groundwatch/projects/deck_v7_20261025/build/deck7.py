# PV5 GroundWatch v7 합본: 최우진 1차 수정본의 이야기 흐름(어두운 풀화면 질문 장) + v6 근거 장.
# deck.py로 15장을 만든 뒤, 표지·마지막 장을 이야기 장으로 바꾸고 18장 순서로 다시 번호를 매긴다.
import os, re, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
G = runpy.run_path(os.path.join(HERE, "deck.py"), run_name="__main__")
OUT = os.path.join(HERE, "..", "svg_output")
import sys; sys.path.insert(0, HERE)
import simplify7
simplify7.run(G, OUT)  # 근거 장: 한 장 = 한 메시지
NAVY, YEL = "#0B1E3C", "#F5B700"
LIGHT, DIM = "#FFFFFF", "#D6DDE8"

# 옛 장 번호(v6 15장) → 새 장 번호(v7 18장): 화면·노트의 "N장" 참조를 맞춘다
REMAP = {2: 9, 3: 2, 4: 3, 5: 4, 6: 5, 7: 10, 8: 11, 9: 12, 10: 13, 11: 14, 12: 15, 13: 16, 14: 17}


def remap_refs(t):
    return re.sub(r"(?<![0-9])(\d{1,2})장", lambda m: f"{REMAP.get(int(m.group(1)), int(m.group(1)))}장", t)


def story(img, lines, foot_left="", credit="", fade=0.9):
    """어두운 풀화면 장: 사진 + 왼쪽 남색 스크림 + 큰 문장. lines = [(y, size, weight, color, text)]"""
    s = f'''  <defs>
    <linearGradient id="storyFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="{fade}" />
      <stop offset="45%" stop-color="{NAVY}" stop-opacity="{fade * 0.7:.2f}" />
      <stop offset="78%" stop-color="{NAVY}" stop-opacity="0.15" />
    </linearGradient>
    <linearGradient id="storyFoot" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{NAVY}" stop-opacity="0" />
      <stop offset="100%" stop-color="{NAVY}" stop-opacity="0.85" />
    </linearGradient>
  </defs>
  <rect id="story-bg" x="0" y="0" width="1280" height="720" fill="{NAVY}" />
  <image id="story-photo" data-pptx-role="background" href="../images/{img}" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" />
  <rect id="story-scrim" data-pptx-role="decoration" x="0" y="0" width="1280" height="720" fill="url(#storyFade)" />
  <rect id="story-foot-scrim" data-pptx-role="decoration" x="0" y="600" width="1280" height="120" fill="url(#storyFoot)" />
  <g id="story-brand" data-pptx-bounds="64 32 400 24">
    <text x="64" y="50" font-size="14" font-weight="bold" fill="{DIM}">PV5 GroundWatch</text>
  </g>
  <g id="story-text" data-pptx-bounds="64 150 700 440">
'''
    for y, size, w, col, txt in lines:
        s += f'    <text x="64" y="{y}" font-size="{size}" font-weight="{w}" fill="{col}" letter-spacing="{-1 if size >= 36 else 0}">{txt}</text>\n'
    s += "  </g>\n"
    s += f'''  <g id="footer" data-pptx-role="footer" data-pptx-bounds="64 676 1160 28">
    <text x="64" y="696" font-size="14" font-weight="bold" fill="{YEL}">{foot_left}</text>
    <text x="1224" y="696" font-size="13" fill="{DIM}" text-anchor="end">{credit}{"  ·  " if credit else ""}00 / 18</text>
  </g>
'''
    return s


def write(name, body, role="content"):
    doc = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1280 720" lang="ko-KR" data-pptx-page-role="{role}" font-family="Pretendard, 'Malgun Gothic', sans-serif">
  <rect id="bg" x="0" y="0" width="1280" height="720" fill="{NAVY}" />
{body}</svg>
'''
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(doc)


TEAM = "TEAM 한 명이라도 살릴 수 있다면"
write("s_open.svg", story("story_trip.jpg", [
    (300, 30, "normal", DIM, "가족과 여행을 가는 길,"),
    (372, 54, "bold", LIGHT, "지금, 도로가 꺼진다면."),
    (470, 17, "bold", YEL, "제5회 기아 PBV 아이디어 공모전 · 일반 부문"),
    (504, 22, "bold", LIGHT, "PV5 GroundWatch · PV5 지하안전 순찰차"),
], TEAM, "연출 이미지"), role="cover")

write("s_q_more.svg", story("story_traffic.jpg", [
    (220, 44, "bold", LIGHT, "그렇다면,"),
    (280, 44, "bold", LIGHT, "더 자주 검사하면 되지 않을까요?"),
    (372, 18, "normal", DIM, "지금의 1회 공정 · 서울시 2024 공동조사용역"),
    (446, 72, "bold", LIGHT, "km당 약 92만 원"),
    (490, 20, "normal", DIM, "1·2차 탐사, 천공 499곳, 공동 채움 285곳까지 묶인 가격입니다."),
    (522, 20, "bold", LIGHT, "이 공정을 그대로 여러 번 돌리면, 예산과 인력이 그만큼 늘어납니다."),
    (584, 13, "normal", DIM, "출처: 서울시 「지반침하 특별점검 공동조사용역 최종보고서」(2024.10) · 17억 8,090만 원 ÷ 조사연장 1,930.6km"),
], "", "사진: Immanuelle, CC BY 4.0"))

write("s_q_diff.svg", story("story_jongno.jpg", [
    (250, 28, "normal", DIM, "매번 전체 공정을 반복하지 않고,"),
    (322, 50, "bold", LIGHT, "달라진 곳부터"),
    (386, 50, "bold", LIGHT, "찾아볼 수 있다면요?"),
    (466, 20, "normal", DIM, "같은 길을 반복해서 재고, 지난 기록과 달라진 곳만 골라"),
    (498, 20, "normal", DIM, "전문가가 검토한 지점만 현장에서 다시 확인합니다."),
], "", "사진: 서울연구원, CC BY 4.0"))

write("s_reveal.svg", story("cover_hangang.jpg", [
    (214, 26, "normal", DIM, "그래서, 같은 길을 다시 달립니다."),
    (316, 76, "bold", LIGHT, "PV5"),
    (396, 64, "bold", LIGHT, "GroundWatch"),
    (452, 30, "bold", "#D7DEE8", "PV5 지하안전 순찰차"),
    (512, 21, "normal", DIM, "약 2개월마다 도로 아래를 다시 재고,"),
    (544, 21, "normal", DIM, "지난 기록과 달라진 곳을 찾습니다."),
], TEAM, "PV5 기반 콘셉트 이미지", fade=0.94))

write("s_close.svg", story("story_trip.jpg", [
    (300, 30, "normal", DIM, "가족과 떠난 길,"),
    (372, 54, "bold", LIGHT, "무사히 돌아올 수 있도록."),
    (470, 22, "bold", LIGHT, "PV5 GroundWatch"),
    (506, 20, "normal", DIM, "같은 길을 다시 보는 일이, 한 사람의 무사 귀가가 되도록."),
], TEAM, "연출 이미지"), role="ending")

# 18장 순서
ORDER = ["s_open", "03_incident", "04_current", "05_blindspot", "06_target", "s_q_more", "s_q_diff", "s_reveal",
         "02_summary", "07_solution", "08_field", "09_pv5_lab", "10_why_pv5", "11_verify", "12_economics",
         "13_players", "14_entry", "s_close"]
files = {f[:-4]: f for f in os.listdir(OUT) if f.endswith(".svg")}
for drop in ("01_cover", "15_closing"):
    os.remove(os.path.join(OUT, files.pop(drop)))
assert set(files) == set(ORDER), sorted(set(files) ^ set(ORDER))
texts = []
for i, key in enumerate(ORDER, 1):
    t = open(os.path.join(OUT, files[key]), encoding="utf-8").read()
    t = re.sub(r"\d\d / \d\d<", f"{i:02d} / 18<", t)
    if not key.startswith("s_"):
        t = remap_refs(t)
    os.remove(os.path.join(OUT, files[key]))
    name = key[2:] if key.startswith("s_") else key.split("_", 1)[1]
    texts.append((f"{i:02d}_{name}.svg", t))
for f, t in texts:
    open(os.path.join(OUT, f), "w", encoding="utf-8").write(t)
assert len(os.listdir(OUT)) == 18
print("v7 ok", [f for f, _ in texts])
