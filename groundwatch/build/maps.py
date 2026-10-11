# CARTO Positron 타일(© OpenStreetMap contributors )로 실제 서울 지도 바탕 생성
import math, os, time, urllib.request, io
from PIL import Image
OUT = os.path.join(os.path.dirname(__file__), "..", "images", "map")
def tile(lat, lon, z):
    n = 2 ** z; x = (lon + 180) / 360 * n
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n
    return x, y
def stitch(name, lat, lon, z, cols, rows, style="light_all"):
    cx, cy = tile(lat, lon, z); x0, y0 = int(cx - cols / 2), int(cy - rows / 2)
    im = Image.new("RGB", (cols * 256, rows * 256))
    for i in range(cols):
        for j in range(rows):
            url = f"https://tile.openstreetmap.org/{z}/{x0 + i}/{y0 + j}.png"
            data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "GroundWatchDeck/1.0 (contest proposal)"})).read()
            im.paste(Image.open(io.BytesIO(data)).convert("RGB"), (i * 256, j * 256)); time.sleep(0.2)
    im.save(os.path.join(OUT, name + ".png")); print(name, im.size)
stitch("gangdong_z16", 37.5480, 127.1440, 16, 8, 5)
stitch("gangdong_z15", 37.5450, 127.1350, 15, 8, 5)
