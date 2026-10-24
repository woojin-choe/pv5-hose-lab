# v8 테마: 흰 배경 템플릿을 어두운 시네마틱·에디토리얼 톤으로 바꾼다(최우진 수정본의 어두운 화면 + v7 근거 장).
# deck7.py가 만든 18장 SVG를 후처리한다. 상단 메뉴 줄 대신 노란 장 표시, 큰 제목, 장 번호 워터마크.
import os, re, runpy
HERE = os.path.dirname(os.path.abspath(__file__))
runpy.run_path(os.path.join(HERE, "deck7.py"), run_name="__main__")
OUT = os.path.join(HERE, "..", "svg_output")
BG0, BG1, CARD, YEL = "#0A0F19", "#101A2B", "#131D2E", "#F5B700"
TEXT = {"#0B1E3C": "#FFFFFF", "#111827": "#E8ECF2", "#374151": "#C3CBD8", "#4B5563": "#8E9AAB",
        "#C62828": "#FF6B5E", "#B45309": "#F5B700", "#9AA3AF": "#6B7789"}
SHAPE = {"#F3F5F8": CARD, "#9AA3AF": "#3B4557", "#C62828": "#FF6B5E", "#E2E6EC": "#273147", "#C3CCD9": "#3B4557"}


def recolor_text(m):
    tag = m.group(0)
    if re.search(r'>[A-D]</text>', tag):  # 배치도 노란 동그라미 안 글자
        return tag
    return re.sub(r'fill="(#[0-9A-F]{6})"', lambda k: f'fill="{TEXT.get(k.group(1), k.group(1))}"', tag)


def recolor_shape(m):
    tag = m.group(0)
    if "fill-opacity" in tag:
        return tag
    h = re.search(r'height="([\d.]+)"', tag)
    h = float(h.group(1)) if h else 0
    def f(k):
        c = k.group(1)
        if c == "#0B1E3C":
            if tag.startswith("<rect") and 18 <= h <= 30:   # 사진 위 이름표 칩
                return f'fill="{c}"'
            if tag.startswith("<rect") and h > 120:          # 큰 남색 패널 → 카드
                return f'fill="{CARD}"'
            return 'fill="#FFFFFF"'
        return f'fill="{SHAPE.get(c, c)}"'
    tag = re.sub(r'fill="(#[0-9A-F]{6})"', f, tag)
    tag = re.sub(r'stroke="(#0B1E3C|#E2E6EC)"', lambda k: 'stroke="#2E3A50"' if not tag.startswith("<circle") else k.group(0), tag)
    return tag


for f in sorted(os.listdir(OUT)):
    p = os.path.join(OUT, f)
    t = open(p, encoding="utf-8").read()
    no = int(f[:2])
    hm = re.search(r'  <g id="header".*?\n  </g>\n', t, re.S)
    if not hm:  # 이야기 장(이미 어두움)
        continue
    hdr = hm.group(0)
    label = re.search(r'<text x="210"[^>]*>([^<]*)</text>', hdr).group(1)
    step = re.search(r'font-weight="bold" fill="#0B1E3C" text-anchor="middle">([^<]*)</text>', hdr)
    chap = step.group(1) if step else ("문제" if no == 2 else "요약")
    kicker = f'''  <g id="chapter" data-pptx-bounds="56 36 600 30">
    <rect x="56" y="44" width="28" height="4" fill="{YEL}" />
    <text x="96" y="52" font-size="16" font-weight="bold" fill="{YEL}">{chap}<tspan fill="#8E9AAB" font-weight="normal">   {label}</tspan></text>
  </g>
'''
    t = t.replace(hdr, kicker)
    # 배경: 어두운 세로 그라데이션 + 장 번호 워터마크
    bg = f'''  <defs><linearGradient id="bg8" x1="0" y1="0" x2="0.4" y2="1"><stop offset="0%" stop-color="{BG1}" /><stop offset="100%" stop-color="{BG0}" /></linearGradient></defs>
  <rect id="bg" x="0" y="0" width="1280" height="720" fill="url(#bg8)" />
  <g id="watermark" data-pptx-role="decoration" data-pptx-bounds="900 440 332 278">
    <text x="1232" y="636" font-size="200" font-weight="bold" fill="#121B2B" text-anchor="end" letter-spacing="-12">{no:02d}</text>
  </g>
'''
    if no == 2:  # 지도 장은 워터마크 없이
        bg = re.sub(r'  <g id="watermark".*?</g>\n', '', bg, flags=re.S)
    t = re.sub(r'  <rect id="bg"[^>]*/>\n', bg, t, count=1)
    body_start = t.index('<g id="chapter"')
    head_part, body = t[:body_start], t[body_start:]
    body = re.sub(r'<(text|tspan|g)\b[^>]*>(?:[^<]*</text>)?', recolor_text, body)
    body = re.sub(r'<(rect|circle|polygon|line|ellipse)\b[^>]*/>', recolor_shape, body)
    # 제목 크게
    body = body.replace('font-size="44" font-weight="bold" fill="#FFFFFF">', 'font-size="48" font-weight="bold" fill="#FFFFFF">')
    # 사업 장: 최우진 수정본의 야간 현장 사진을 어둡게 깐다(사진 장과 도표 장을 섞어 단조로움을 줄임)
    photo = {15: "story_nightvan.jpg", 16: "story_field.jpg", 17: "story_nightvan.jpg"}.get(no)
    if photo:
        layer = f'''  <defs><linearGradient id="ph8" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="{BG0}" stop-opacity="0.95" /><stop offset="55%" stop-color="{BG0}" stop-opacity="0.82" /><stop offset="100%" stop-color="{BG0}" stop-opacity="0.55" /></linearGradient></defs>
  <image id="photo8" data-pptx-role="background" href="../images/{photo}" x="0" y="0" width="1280" height="720" preserveAspectRatio="xMidYMid slice" />
  <rect id="photo8-scrim" data-pptx-role="decoration" x="0" y="0" width="1280" height="720" fill="url(#ph8)" />
'''
        head_part = head_part.replace('  <g id="watermark"', layer + '  <g id="watermark"', 1)
    if no == 5:  # 단면도 위 흰 이름표는 어두운 글씨 유지
        body = body.replace('fill="#C3CBD8" text-anchor="middle">깊은 층', 'fill="#374151" text-anchor="middle">깊은 층')
    open(p, "w", encoding="utf-8").write(head_part + body)
print("theme8 ok")
