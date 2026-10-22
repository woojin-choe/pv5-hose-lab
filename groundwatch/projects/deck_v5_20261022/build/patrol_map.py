# 실제 명일동 OSM 지도(myeongil_dark.png) 위 실제 도로에 위험도별 순찰 주기 색을 칠한다. 주기는 예시.
from PIL import Image, ImageDraw
base = Image.open("myeongil_dark.png").convert("RGB")
x0, y0, x1, y1 = 300, 580, 1240, 1110   # 940x530 ≈ 1.774
S = 2
im = base.crop((x0, y0, x1, y1)).resize(((x1 - x0) * S, (y1 - y0) * S), Image.LANCZOS)
im = Image.blend(im, Image.new("RGB", im.size, (8, 14, 28)), 0.18)
d = ImageDraw.Draw(im)
P = lambda pts: [((x - x0) * S, (y - y0) * S) for x, y in pts]
roads = [
    ((224, 49, 49),  [(1056, 746), (1052, 900), (1046, 1030), (1040, 1078), (860, 1062), (700, 1045)]),  # 동남로·상암로 사고 인근: 집중관리
    ((240, 140, 0),  [(430, 744), (745, 745), (1050, 746)]),                                              # 구천면로: 노후 하수관·공사장
    ((78, 143, 217), [(1058, 600), (1056, 746)]),                                                         # 동남로 북측(고덕역 방향): 역세권
    ((59, 165, 92),  [(440, 600), (430, 744), (418, 880), (410, 1018), (560, 1030), (700, 1045)]),        # 명일로·상암로 서측: 일반 관리
    ((139, 92, 246), [(745, 745), (742, 900), (740, 1040)]),                                              # 상암로61길: 집중호우 후
]
for col, pts in roads:
    d.line(P(pts), fill=(255, 255, 255), width=13, joint="curve")
    d.line(P(pts), fill=col, width=9, joint="curve")
im.save("patrol_map_real.png")
print(im.size)
