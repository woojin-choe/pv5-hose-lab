# PPTX 안의 큰 불투명 PNG를 JPEG(화질 85)로 바꾸고, 슬라이드에 비해 과하게 큰 이미지는 가로 2000px로 줄인다.
# 투명도가 있는 PNG(아이콘 등)는 그대로 둔다. 사용: python optimize_media.py in.pptx out.pptx
import io, re, sys, zipfile
from PIL import Image

SRC, DST = sys.argv[1:3]
MAX_W, MIN_BYTES, Q = 2000, 200_000, 85

zin = zipfile.ZipFile(SRC)
files = {n: zin.read(n) for n in zin.namelist()}
rename, saved = {}, 0
for name, data in list(files.items()):
    if not (name.startswith("ppt/media/") and name.lower().endswith(".png")) or len(data) < MIN_BYTES:
        continue
    im = Image.open(io.BytesIO(data))
    if im.mode in ("RGBA", "LA", "P"):
        a = im.convert("RGBA").getchannel("A")
        if a.getextrema()[0] < 250:      # 실제로 투명한 픽셀이 있으면 유지
            continue
    im = im.convert("RGB")
    if im.width > MAX_W:
        im = im.resize((MAX_W, round(im.height * MAX_W / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=Q, optimize=True, progressive=True)
    if buf.tell() >= len(data):
        continue
    new = name[:-4] + ".jpg"
    while new in files: new = new[:-4] + "_j.jpg"
    files[new] = buf.getvalue(); del files[name]
    rename[name.split("/")[-1]] = new.split("/")[-1]
    saved += len(data) - buf.tell()

for name in list(files):
    if name.endswith(".rels"):
        t = files[name].decode("utf-8")
        for old, new in rename.items():
            t = t.replace(f"media/{old}\"", f"media/{new}\"")
        files[name] = t.encode("utf-8")
ct = files["[Content_Types].xml"].decode("utf-8")
if 'Extension="jpg"' not in ct:
    ct = ct.replace("<Types ", "<Types ", 1).replace(">", '><Default Extension="jpg" ContentType="image/jpeg"/>', 1) \
        if False else re.sub(r"(<Types[^>]*>)", r'\1<Default Extension="jpg" ContentType="image/jpeg"/>', ct, count=1)
files["[Content_Types].xml"] = ct.encode("utf-8")

with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in zin.namelist():                      # 원래 순서 유지([Content_Types].xml 먼저)
        tgt = n
        if n.startswith("ppt/media/") and n.split("/")[-1] in rename:
            tgt = "ppt/media/" + rename[n.split("/")[-1]]
        zout.writestr(tgt, files[tgt])
print(f"converted {len(rename)} images, saved {saved / 1048576:.1f} MB")
