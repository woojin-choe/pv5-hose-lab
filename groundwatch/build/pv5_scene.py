# PV5 GroundWatch 3D 장면 (Blender Cycles). 차체 치수 = 기아 공식 제원(PV5 카고 롱), 형상은 실차 사진 기준 모델링.
# 사용: blender -b -P pv5_scene.py -- <out.png> <view>   view = front | night | rear | interior | cutaway
import bpy, bmesh, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT, VIEW = argv[0], argv[1]
FONT = os.environ.get("GW_FONT", "")
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
mm = lambda v: v / 1000.0
NIGHT = VIEW == "night"
SHELL = VIEW in ("interior", "cutaway", "interior_side")
CUTV = VIEW in ("cutaway", "interior_side")
W = 947.5

def mat(name, col, rough=0.4, metal=0.0, emit=None, strength=0.0, coat=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if coat: b.inputs["Coat Weight"].default_value = coat; b.inputs["Coat Roughness"].default_value = 0.05
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    return m
PAINT = mat("paint", (0.80, 0.81, 0.80), 0.22, coat=0.6)
BLACKG = mat("blackgloss", (0.01, 0.011, 0.013), 0.08, coat=1.0)
CLAD = mat("clad", (0.025, 0.027, 0.03), 0.6)
GLASS = mat("glass", (0.006, 0.008, 0.012), 0.03, coat=1.0)
BUMPER = mat("bumper", (0.28, 0.29, 0.30), 0.45, 0.4)
TIRE = mat("tire", (0.018, 0.018, 0.02), 0.8)
RIM = mat("rim", (0.03, 0.032, 0.036), 0.3, 0.5)
RIMH = mat("rimh", (0.55, 0.57, 0.6), 0.25, 1.0)
TAIL = mat("tail", (0.35, 0.0, 0.0), 0.2, emit=(1, 0.04, 0.02), strength=(25 if NIGHT else 3))
DRL = mat("drl", (0.95, 0.95, 0.95), 0.1, emit=(1, 0.97, 0.92), strength=(40 if NIGHT else 6))
AMBER = mat("amber", (1.0, 0.55, 0.0), 0.15, emit=(1, 0.5, 0.02), strength=(250 if NIGHT else 4))
EQ = mat("equip", (0.05, 0.055, 0.06), 0.4, 0.3)
EQ2 = mat("equip2", (0.14, 0.15, 0.17), 0.5, 0.2)
ALU = mat("alu", (0.75, 0.77, 0.8), 0.28, 1.0)
DOME = mat("dome", (0.93, 0.93, 0.92), 0.35)
LENS = mat("lens", (0.0, 0.02, 0.05), 0.02, coat=1.0)
NAVY = mat("navy", (0.012, 0.035, 0.09), 0.35, coat=0.4)
AMB2 = mat("amberpaint", (0.85, 0.48, 0.02), 0.35, coat=0.4)
INNER = mat("inner", (0.72, 0.73, 0.74), 0.6)
FLOOR = mat("floor", (0.05, 0.055, 0.06), 0.85)
YEL = mat("yellow", (0.92, 0.6, 0.03), 0.35, coat=0.3)
CONE = mat("cone", (0.95, 0.3, 0.03), 0.5)
LEDG = mat("ledg", (0, 0.3, 0.1), 0.3, emit=(0.1, 1, 0.35), strength=20)
LEDB = mat("ledb", (0, 0.1, 0.3), 0.3, emit=(0.25, 0.55, 1), strength=20)
SCREEN = mat("screen", (0.01, 0.02, 0.05), 0.15, emit=(0.18, 0.42, 0.9), strength=4)
LAMP = mat("lamp", (1, 1, 1), 0.2, emit=(1, 0.95, 0.88), strength=(12 if SHELL else 0))
PLATE = mat("plate", (0.9, 0.9, 0.9), 0.4)
STRAP = mat("strap", (0.95, 0.4, 0.05), 0.6)

def prism(name, prof, y0, y1, m, bev=0.0, seg=5, ang=40):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((mm(x), mm(y0), mm(z))) for x, z in prof]
    f = bm.faces.new(vs); bmesh.ops.recalc_face_normals(bm, faces=[f])
    r = bmesh.ops.extrude_face_region(bm, geom=[f]); top = [v for v in r["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0, mm(y1 - y0), 0)); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m)
    if bev:
        md = ob.modifiers.new("bev", "BEVEL"); md.width = bev; md.segments = seg; md.limit_method = "ANGLE"; md.angle_limit = math.radians(ang)
    for p in ob.data.polygons: p.use_smooth = True
    ob.data.shade_auto_smooth() if hasattr(ob.data, "shade_auto_smooth") else None
    return ob
def box(name, x, y, z, sx, sy, sz, m, bev=0.004, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(mm(x), mm(y), mm(z)), rotation=rot); ob = bpy.context.active_object
    ob.name = name; ob.scale = (mm(sx), mm(sy), mm(sz)); bpy.ops.object.transform_apply(scale=True); ob.data.materials.append(m)
    if bev: md = ob.modifiers.new("b", "BEVEL"); md.width = bev; md.segments = 3
    return ob
def cyl(name, x, y, z, r, d, m, rot=(math.pi / 2, 0, 0), v=64, bev=0.0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=mm(r), depth=mm(d), location=(mm(x), mm(y), mm(z)), rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.data.materials.append(m); bpy.ops.object.shade_smooth()
    if bev: md = ob.modifiers.new("b", "BEVEL"); md.width = bev; md.segments = 4
    return ob
def text(name, s, x, y, z, size, m, rotz=0, depth=0.0015, align="LEFT"):
    bpy.ops.object.text_add(location=(mm(x), mm(y), mm(z)), rotation=(math.pi / 2, 0, rotz))
    ob = bpy.context.active_object; ob.name = name; ob.data.body = s; ob.data.size = mm(size); ob.data.extrude = depth; ob.data.align_x = align
    if FONT and os.path.exists(FONT): ob.data.font = bpy.data.fonts.load(FONT)
    ob.data.materials.append(m); return ob

# ---------------- 차체 ----------------
cab = [(2430, 1905), (3250, 1905), (3385, 1888), (3480, 1835), (4235, 1205), (4520, 1110), (4645, 1058), (4700, 975), (4705, 420), (4670, 335), (4390, 300),
       (4375, 300), (4365, 560), (4300, 700), (3390, 700), (3325, 560), (3315, 300), (2430, 300)]
cargo = [(0, 420), (0, 1780), (40, 1872), (160, 1905), (2430, 1905), (2430, 300), (1380, 300), (1370, 560), (1305, 700), (395, 700), (330, 560), (320, 300), (45, 335)]
prism("cab", cab, -W, W, PAINT, 0.055, 6)
if not SHELL:
    prism("cargo", cargo, -W, W, PAINT, 0.055, 6)
else:
    prism("wall_far", cargo, W - 30, W, PAINT, 0.012)
    near = prism("wall_near", cargo, -W, -W + 30, PAINT, 0.012)
    if CUTV:
        c = box("cut", 1300, -W, 1290, 2160, 200, 1120, INNER, 0); c.hide_render = True
        bo = near.modifiers.new("cut", "BOOLEAN"); bo.object = c; bo.operation = "DIFFERENCE"
    else:
        box("roof", 1215, 0, 1890, 2430, 1895, 30, PAINT, 0.012)
    box("sill", 1215, 0, 365, 2430, 1895, 130, CLAD, 0.01)
    for yy in ((1,) if CUTV else (-1, 1)): box("liner", 1215, yy * (W - 45), 1150, 2380, 10, 1400, INNER, 0)
    box("bulkhead", 2415, 0, 1110, 30, 1830, 1400, INNER, 0)
    if False:
        for s_ in (-1, 1):   # 열린 뒷문(경첩 기준 약 100도)
            d = box("door", 0, 0, 1100, 30, W, 1450, PAINT, 0.012)
            d.location = (mm(-W * 0.5 * math.sin(math.radians(100)) + 0), mm(s_ * (W - (W * 0.5) * math.cos(math.radians(100)) * 1)), mm(1100))
            d.rotation_euler = (0, 0, -s_ * math.radians(100) + 0)
            d.location = (mm(-(W / 2) * math.sin(math.radians(100))), mm(s_ * W + s_ * (W / 2) * math.cos(math.radians(100)) * -1), mm(1100))
    elif VIEW != "interior":
        box("rear_wall", 15, 0, 1100, 30, 1895, 1450, PAINT, 0.01)
    if VIEW == "interior":   # 활짝 열린 뒷문(측면으로 접힘)
        for s_ in (-1, 1):
            box("door", -60, s_ * (W + 470), 1100, 30, 900, 1450, PAINT, 0.012)
            box("door_lamp", -78, s_ * (W + 860), 1240, 8, 30, 820, TAIL, 0)
# 하단 클래딩(측면 띠)·휠아치
for pr in ([(0, 420), (0, 560), (330, 560), (320, 300), (45, 335)], [(1370, 560), (3325, 560), (3315, 300), (1380, 300)], [(4365, 560), (4705, 560), (4705, 420), (4670, 335), (4390, 300), (4375, 300)]):
    for y0 in (-W - 10, W - 30): prism("clad", pr, y0, y0 + 40, CLAD, 0.008)
for cx in (850, 3845):
    arch = [(cx - 525, 560), (cx - 460, 712), (cx + 460, 712), (cx + 525, 560), (cx + 470, 560), (cx + 412, 668), (cx - 412, 668), (cx - 470, 560)]
    for y0 in (-W - 18, W - 28): prism("arch", arch, y0, y0 + 46, CLAD, 0.006)
box("rear_bumper", 40, 0, 400, 90, 1900, 220, CLAD, 0.02)
# 글라스 밴드(블랙 루프 끝·A필러·1열 창)·윈드실드
prism("roofblk", [(3050, 1905), (3250, 1905), (3385, 1888), (3480, 1835), (3430, 1800), (3050, 1800)], -W - 4, W + 4, BLACKG, 0.01)
prism("glass_side", [(3050, 1180), (3050, 1795), (3385, 1825), (3462, 1795), (4215, 1212)], -W - 6, W + 6, GLASS, 0.006)
prism("windshield", [(3480, 1835), (4235, 1205), (4212, 1192), (3458, 1822)], -W + 55, W - 55, GLASS)
# 전면 상단 블랙 밴드(후드 랩어라운드)
prism("hood_band", [(4228, 1212), (4522, 1116), (4648, 1064), (4712, 978), (4712, 880), (4560, 950), (4228, 1100)], -W + 25, W - 25, BLACKG, 0.01)
for s_ in (-1, 1): prism("hood_side", [(4228, 1212), (4522, 1116), (4648, 1064), (4712, 978), (4712, 880), (4560, 950), (4228, 1100)], s_ * W - 8 if s_ > 0 else -W - 8, (s_ * W - 8 if s_ > 0 else -W - 8) + 16, BLACKG)
# ㄱ자 주간주행등(후드 모서리 → 전면 하강), 전면 가로 라이트
for s_ in (-1, 1):
    y = s_ * (W - 12)
    prism("drl", [(4230, 1206), (4522, 1110), (4650, 1058), (4652, 1046), (4524, 1098), (4232, 1194)], y - 6, y + 6, DRL)
    box("drl_front", 4714, s_ * (W - 60), 960, 10, 90, 14, DRL, 0)
box("front_face", 4700, 0, 650, 26, 1840, 520, PAINT, 0.03)
box("front_lightbar", 4716, 0, 790, 8, 1560, 18, DRL, 0)
box("front_lower", 4712, 0, 470, 30, 1750, 300, BUMPER, 0.02)
box("grille", 4722, 0, 520, 10, 1100, 120, CLAD, 0.01)
box("plate", 4730, 0, 420, 6, 520, 110, PLATE, 0.003)
# 리어램프(세로)
for s_ in (-1, 1): box("tail", 4, s_ * (W - 40), 1240, 18, 34, 860, TAIL, 0.004)
# 미러
for s_ in (-1, 1):
    box("mirror_arm", 3470, s_ * (W + 40), 1215, 70, 90, 40, CLAD, 0.01)
    box("mirror", 3500, s_ * (W + 120), 1250, 110, 90, 230, CLAD, 0.02)
# 바퀴(에어로 휠)
for cx in (850, 3845):
    for s_ in (-1, 1):
        cyl("tire", cx, s_ * 805, 343, 343, 225, TIRE, bev=0.03)
        cyl("rim", cx, s_ * 915, 343, 225, 14, RIM)
        for k in range(5):
            a = math.radians(k * 72 + 18)
            box("spoke", cx + 135 * math.cos(a), s_ * 924, 343 + 135 * math.sin(a), 175, 6, 38, RIMH, 0.003, rot=(0, -a, 0))
        cyl("hub", cx, s_ * 924, 343, 45, 10, RIM)
# ---------------- 외부 장비 ----------------
for bx in (() if VIEW == "cutaway" else (700, 2050)):   # 루프 크로스바
    box("crossbar", bx, 0, 1935, 50, 1700, 30, ALU, 0.006)
    for s_ in (-1, 1): box("foot", bx, s_ * 820, 1915, 80, 60, 30, CLAD, 0.006)
box("beacon_base", 2800, 0, 1925, 260, 1280, 40, EQ, 0.006)
box("beacon", 2800, 0, 1965, 220, 1220, 55, AMBER, 0.015)
box("cam_pod", 3200, 0, 1940, 200, 300, 70, EQ, 0.015); cyl("cam_lens", 3302, 0, 1940, 22, 10, LENS, rot=(0, math.pi / 2, 0))
cyl("gnss_post", 2050, 560, 1985, 14, 70, EQ, rot=(0, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=mm(95), location=(mm(2050), mm(560), mm(2020))); d_ = bpy.context.active_object; d_.scale.z = 0.5; d_.data.materials.append(DOME); bpy.ops.object.shade_smooth()
cyl("mast", 450, 0, 2060, 18, 260, EQ, rot=(0, 0, 0))
bpy.ops.mesh.primitive_uv_sphere_add(radius=mm(60), location=(mm(450), 0, mm(2210))); c_ = bpy.context.active_object; c_.data.materials.append(LENS); bpy.ops.object.shade_smooth()
box("cam360_band", 450, 0, 2210, 125, 125, 40, EQ, 0.02)
for s_ in (-1, 1): box("side_cam", 3500, s_ * (W + 120), 1395, 90, 80, 55, EQ, 0.01)
box("rear_cam", 30, 0, 1850, 40, 220, 60, EQ, 0.01)
# 후방 하부 다채널 GPR 어레이
for by in (-760, 0, 760): box("gpr_bracket", 260, by, 235, 50, 50, 170, ALU, 0.004)
box("gpr", 260, 0, 120, 540, 1820, 90, EQ2, 0.015)
box("gpr_edge", -12, 0, 140, 6, 1825, 18, AMB2, 0.002)
box("encoder", 850, -W - 135, 343, 80, 50, 80, YEL, 0.01)
# 랩핑(측면 양쪽): 남색 띠 + 앰버 라인 + 워드마크
for s_ in (-1, 1):
    y = s_ * (W + 1.5)
    box("stripe_navy", 1700, y, 860, 3250, 3, 90, NAVY, 0)
    box("stripe_amber", 1700, y, 920, 3250, 3, 18, AMB2, 0)
    rz = 0 if s_ < 0 else math.pi
    xx = 330 if s_ < 0 else 2230
    if CUTV and s_ < 0: continue
    text("wm", "GroundWatch", xx, y + s_ * 1, 1430, 230, NAVY, rotz=rz)
    text("wm2", "지하안전 순찰 · GPR 탐사", xx + (0 if s_ < 0 else 0), y + s_ * 1, 1280, 105, mat("sub", (0.15, 0.17, 0.2), 0.4), rotz=rz)
text("rear_wm", "GroundWatch", -2, 0, 1500, 130, NAVY, rotz=-math.pi / 2, align="CENTER") if not SHELL else None
# ---------------- 실내 ----------------
if SHELL:
    box("cargo_floor", 1215, 0, 432, 2380, 1820, 24, FLOOR, 0)
    for yy in (-560, 560): box("wheelhouse", 850, yy, 560, 1000, 380, 260, INNER, 0.04)
    # Edge Gateway 랙 + 작업대
    box("rack", 2150, 650, 1000, 480, 480, 1120, EQ, 0.01)
    for k in range(7):
        z = 560 + k * 150
        box("ru", 2150, 408, z, 440, 6, 118, EQ2, 0.002); box("led", 1960, 404, z, 16, 4, 16, LEDG if k % 3 else LEDB, 0)
        for v in range(3): box("vent", 2120 + v * 60, 404, z, 40, 3, 70, EQ, 0)
    box("desk", 2190, -120, 900, 380, 560, 28, ALU, 0.004)
    box("monitor", 2330, -120, 1150, 30, 480, 290, EQ, 0.006); box("scr", 2313, -120, 1150, 4, 450, 260, SCREEN, 0)
    cyl("seat_post", 1960, -220, 640, 30, 380, ALU, rot=(0, 0, 0)); box("seat", 1960, -220, 845, 400, 400, 60, EQ2, 0.02)
    # 수동 GPR 카트(고정 스트랩)
    box("cart", 1500, 150, 565, 620, 460, 170, YEL, 0.02); box("cart_top", 1500, 150, 657, 600, 440, 14, EQ, 0.004)
    for cxw in (1270, 1730):
        for sg in (-1, 1): cyl("cw", cxw, 150 + sg * 255, 505, 65, 45, TIRE)
    bpy.ops.mesh.primitive_cylinder_add(radius=mm(15), depth=mm(800), location=(mm(1890), mm(150), mm(930)), rotation=(0, math.radians(-28), 0)); h_ = bpy.context.active_object; h_.data.materials.append(ALU)
    box("cart_ui", 2070, 150, 1280, 70, 260, 180, EQ, 0.006); box("cart_scr", 2035, 150, 1280, 4, 230, 150, SCREEN, 0)
    for k in range(2): box("strap", 1350 + k * 300, 150, 655, 40, 480, 8, STRAP, 0)
    # 선반: AR 글래스 충전함·케이스
    box("shelf", 1400, 760, 1450, 1100, 300, 24, ALU, 0.004)
    box("ar_case", 1180, 760, 1530, 380, 260, 140, EQ, 0.01); box("ar_led", 1180, 628, 1530, 30, 4, 12, LEDG, 0)
    box("pelican", 1620, 760, 1530, 420, 260, 140, mat("pel", (0.12, 0.28, 0.45), 0.5), 0.015)
    # 수납장·라바콘·내시경 케이스
    box("locker", 650, 640, 1150, 900, 420, 820, EQ2, 0.01); box("split", 650, 428, 1150, 6, 4, 780, EQ, 0)
    for hx in (610, 690): box("handle", hx, 424, 1150, 12, 10, 120, ALU, 0)
    for k in range(3):
        bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=mm(130), radius2=mm(18), depth=mm(450), location=(mm(330), mm(-560), mm(667 + k * 70)))
        cn = bpy.context.active_object; cn.data.materials.append(CONE); bpy.ops.object.shade_smooth()
    box("cone_base", 330, -560, 452, 300, 300, 30, CONE, 0.01)
    box("scope_case", 720, -420, 520, 520, 340, 160, EQ, 0.015)
    box("ceiling_light", 1215, 0, 1868, 1900, 70, 10, LAMP, 0)
    pl = bpy.data.lights.new("in", "POINT"); pl.energy = 60; pl.color = (1, 0.95, 0.88); po = bpy.data.objects.new("in", pl); po.location = (1.2, 0, 1.6); sc.collection.objects.link(po)
# ---------------- 지면·하늘·조명 ----------------
gm = bpy.data.materials.new("asphalt"); gm.use_nodes = True; nt = gm.node_tree; bsdf = nt.nodes["Principled BSDF"]
nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 180; nz.inputs["Detail"].default_value = 8
cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.035, 0.037, 0.04, 1); cr.color_ramp.elements[1].color = (0.11, 0.115, 0.12, 1)
nt.links.new(nz.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], bsdf.inputs["Base Color"])
bsdf.inputs["Roughness"].default_value = 0.35 if NIGHT else 0.75
bpy.ops.mesh.primitive_plane_add(size=60, location=(2, 0, 0)); g_ = bpy.context.active_object; g_.data.materials.append(gm)
for xx in range(-12, 16, 3): box("lane", xx * 1000, -2600, 1, 1500, 120, 2, mat("lane", (0.85, 0.85, 0.82), 0.6), 0)
box("curb", 2000, 2400, 75, 30000, 250, 150, mat("curb", (0.55, 0.56, 0.57), 0.8), 0.01)
box("sidewalk", 2000, 4200, 70, 30000, 3400, 140, mat("walk", (0.42, 0.43, 0.44), 0.85), 0)
# 도심 배경(건물·가로수·가로등)
import random
random.seed(5)
BLD = mat("bld", (0.55, 0.56, 0.58) if not NIGHT else (0.06, 0.065, 0.08), 0.85)
BLD2 = mat("bld2", (0.38, 0.40, 0.44) if not NIGHT else (0.04, 0.045, 0.06), 0.85)
WIN = mat("win", (0.05, 0.07, 0.1), 0.1, emit=((1, 0.8, 0.5) if NIGHT else None), strength=(0.6 if NIGHT else 0))
WIN_OFF = mat("winoff", (0.04, 0.05, 0.07), 0.15)
x = -60000
while x < 70000:
    w = random.randint(9000, 18000); h = random.randint(12000, 34000); d = 10000
    y0 = 16000 + d / 2
    box("bld", x + w / 2, y0, h / 2, w - 1200, d, h, random.choice([BLD, BLD2]), 0)
    wo = box("win", x + 1600, y0 - d / 2 - 8, 2500, 900, 10, 1300, WIN if (NIGHT and random.random() < 0.6) else WIN_OFF, 0)
    a1 = wo.modifiers.new("ax", "ARRAY"); a1.count = max(1, int((w - 3000) / 1800)); a1.relative_offset_displace = (2.0, 0, 0)
    a2 = wo.modifiers.new("az", "ARRAY"); a2.count = max(1, int((h - 4000) / 3200)); a2.relative_offset_displace = (0, 0, 2.4)
    x += w
for lx in range(-15000, 40000, 14000):
    cyl("pole", lx, 2900, 3800, 70, 7600, mat("pole", (0.2, 0.21, 0.22), 0.5, 0.6), rot=(0, 0, 0))
    box("arm", lx, 2300, 7550, 160, 1300, 80, mat("pole2", (0.2, 0.21, 0.22), 0.5, 0.6), 0.01)
    box("lamp", lx, 1750, 7480, 300, 500, 60, mat("lamph", (1, 0.9, 0.7), 0.2, emit=(1, 0.85, 0.6), strength=(30 if NIGHT else 0)), 0.01)

world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True; wn = world.node_tree
if NIGHT:
    wn.nodes["Background"].inputs["Color"].default_value = (0.012, 0.022, 0.05, 1)
else:
    sky = wn.nodes.new("ShaderNodeTexSky"); sky.sky_type = "MULTIPLE_SCATTERING"
    sky.sun_elevation = math.radians(28); sky.sun_rotation = math.radians(210); sky.altitude = 50
    wn.links.new(sky.outputs["Color"], wn.nodes["Background"].inputs["Color"])
wn.nodes["Background"].inputs["Strength"].default_value = 1.0 if NIGHT else 0.045
if NIGHT:
    for (x, y) in ((-1.5, -4.2), (7.5, -4.2)):
        L = bpy.data.lights.new("street", "SPOT"); L.energy = 2500; L.spot_size = math.radians(80); L.color = (1, 0.82, 0.55)
        o = bpy.data.objects.new("street", L); o.location = (x, y, 6.5); o.rotation_euler = (math.radians(20), 0, 0); sc.collection.objects.link(o)
    fill = bpy.data.lights.new("fill", "AREA"); fill.energy = 120; fill.size = 10; fill.color = (0.5, 0.62, 1.0)
    fo = bpy.data.objects.new("fill", fill); fo.location = (2.5, -8, 6); fo.rotation_euler = (math.radians(55), 0, 0); sc.collection.objects.link(fo)
    sun = bpy.data.lights.new("bl", "POINT"); sun.energy = 250; sun.color = (1, 0.55, 0.1); so = bpy.data.objects.new("bl", sun); so.location = (2.8, 0, 2.2); sc.collection.objects.link(so)
# ---------------- 카메라 ----------------
cam = bpy.data.cameras.new("cam"); co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
V = {
  "front": ((8.6, -6.4, 1.45), (2.35, 0, 0.95), 42),
  "night": ((8.9, -5.6, 1.15), (2.35, 0, 1.0), 38),
  "rear": ((-4.4, -5.0, 1.25), (1.2, 0, 0.75), 40),
  "interior": ((-2.1, -0.15, 1.3), (1.6, 0.05, 0.95), 24),
  "cutaway": ((4.3, -6.2, 6.2), (1.7, 0.1, 0.7), 50),
  "interior_side": ((1.25, -3.1, 1.3), (1.25, 0.7, 1.0), 20),
  "gpr": ((-1.9, -1.7, 0.45), (0.2, 0.0, 0.18), 45),
}[VIEW]
co.location = V[0]; cam.lens = V[2]; co.rotation_euler = (Vector(V[1]) - Vector(V[0])).to_track_quat("-Z", "Y").to_euler()
cam.dof.use_dof = VIEW in ("front", "night", "rear", "gpr"); cam.dof.focus_distance = (Vector(V[1]) - Vector(V[0])).length; cam.dof.aperture_fstop = 4.0
# ---------------- 렌더 ----------------
sc.render.engine = "CYCLES"
try:
    pr = bpy.context.preferences.addons["cycles"].preferences; pr.compute_device_type = "METAL"; pr.get_devices()
    for d in pr.devices: d.use = True
    sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = int(os.environ.get("SAMPLES", "192")); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.view_settings.exposure = 0.0
sc.use_nodes = True
try:
    ntc = sc.node_tree; rl = ntc.nodes.new("CompositorNodeRLayers"); gl = ntc.nodes.new("CompositorNodeGlare"); cp = ntc.nodes.new("CompositorNodeComposite")
    gl.glare_type = "FOG_GLOW"; gl.threshold = 1.2 if NIGHT else 3.0; gl.size = 8 if NIGHT else 6
    ntc.links.new(rl.outputs["Image"], gl.inputs["Image"]); ntc.links.new(gl.outputs["Image"], cp.inputs["Image"])
except Exception as e:
    print("glare skipped", e)
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print("RENDERED", OUT)
