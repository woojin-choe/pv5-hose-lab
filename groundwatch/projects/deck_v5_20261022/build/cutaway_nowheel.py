# 배치도 원본(앞바퀴·바닥 아래 GPR 배열 포함)을 밝은 배경에 그대로 합성한다.
from PIL import Image
im = Image.open("../../images/final_concept/cutaway_side.png").convert("RGBA")
bg = Image.new("RGBA", im.size, (240, 242, 245, 255))
Image.alpha_composite(bg, im).convert("RGB").save("images/cutaway_nowheel.png")
print(im.size)
