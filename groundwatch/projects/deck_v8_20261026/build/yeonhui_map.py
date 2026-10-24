# OSM 표준 타일(© OpenStreetMap contributors)로 연희동 성산로 일대 지도를 받아 명일동 지도와 같은 어두운 톤으로 만든다.
import math, time, urllib.request, io
from PIL import Image, ImageOps, ImageEnhance
def tile(lat, lon, z):
    n = 2 ** z
    return (lon + 180) / 360 * n, (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
lat, lon, z, cols, rows = 37.5650, 126.9300, 17, 5, 6
cx, cy = tile(lat, lon, z); x0, y0 = int(cx - cols / 2), int(cy - rows / 2)
im = Image.new("RGB", (cols * 256, rows * 256))
for i in range(cols):
    for j in range(rows):
        url = f"https://tile.openstreetmap.org/{z}/{x0 + i}/{y0 + j}.png"
        for k in range(4):
            try:
                data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "GroundWatchDeck/1.0 (contest proposal)"}), timeout=20).read(); break
            except Exception:
                time.sleep(2)
        im.paste(Image.open(io.BytesIO(data)).convert("RGB"), (i * 256, j * 256)); time.sleep(0.25)
im.save("images/yeonhui_osm.png")
g = ImageOps.invert(ImageOps.grayscale(im))
g = ImageEnhance.Contrast(g).enhance(0.9)
dark = ImageOps.colorize(g, black=(10, 18, 34), white=(150, 168, 196))
dark.save("images/yeonhui_dark.png")
print("origin tile", x0, y0, "size", im.size)
def px(la, lo):
    X, Y = tile(la, lo, z); return round((X - x0) * 256), round((Y - y0) * 256)
for name, la, lo in [("사러가", 37.5672711, 126.9299935), ("연희교차로", 37.5657194, 126.9301737), ("성산로A", 37.5640163, 126.9297658), ("성산로B", 37.5664502, 126.9266927), ("성산로C", 37.5614728, 126.9327106)]:
    print(name, px(la, lo))

# 성산로 연희동 구간 강조(정확한 사고 지점은 보도되지 않아 구간으로 표시) 후 2장 오른쪽 칸 비율로 자르기
from PIL import ImageDraw, ImageFilter
base = dark.convert("RGBA")
seg = [(40, 757), (200, 763), (360, 785), (470, 820), (560, 868), (630, 950), (700, 1062)]
glow = Image.new("RGBA", base.size, (0, 0, 0, 0))
ImageDraw.Draw(glow).line(seg, fill=(229, 72, 77, 150), width=46, joint="curve")
base = Image.alpha_composite(base, glow.filter(ImageFilter.GaussianBlur(10)))
ImageDraw.Draw(base).line(seg, fill=(255, 90, 95, 255), width=9, joint="curve")
base.convert("RGB").crop((80, 380, 1000, 1415)).save("images/yeonhui_crop.png")
