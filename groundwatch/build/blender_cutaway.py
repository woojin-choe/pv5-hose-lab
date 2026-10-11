# PV5 GroundWatch 3D 절개 배치도 (Blender, Cycles). 차체 치수 = 기아 공식 제원(PV5 카고 롱), 형상은 실차 사진 기준 근사.
import bpy, bmesh, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
OUT = argv[0] if argv else "/tmp/cutaway.png"
VIEW = argv[1] if len(argv) > 1 else "cutaway"
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
mm = lambda v: v / 1000.0

def mat(name, col, rough=0.4, metal=0.0, emit=None, strength=0.0, alpha=1.0, trans=0.0):
    m = bpy.data.materials.new(name); m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*col, 1); b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    if emit: b.inputs["Emission Color"].default_value = (*emit, 1); b.inputs["Emission Strength"].default_value = strength
    if trans: b.inputs["Transmission Weight"].default_value = trans
    if alpha < 1: b.inputs["Alpha"].default_value = alpha; m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m
WHITE = mat("paint", (0.86, 0.87, 0.88), 0.25, 0.0)
CLAD = mat("clad", (0.035, 0.038, 0.042), 0.55)
GLASS = mat("glass", (0.02, 0.03, 0.045), 0.05, 0.0)
INNER = mat("inner", (0.62, 0.64, 0.66), 0.7)
FLOOR = mat("floor", (0.12, 0.13, 0.14), 0.8)
TIRE = mat("tire", (0.02, 0.02, 0.022), 0.85)
RIM = mat("rim", (0.05, 0.055, 0.06), 0.35, 0.3)
RED = mat("tail", (0.4, 0.0, 0.0), 0.3, emit=(1, 0.05, 0.03), strength=6)
DRL = mat("drl", (0.9, 0.9, 0.9), 0.2, emit=(1, 0.97, 0.9), strength=8)
AMBER = mat("amber", (0.9, 0.5, 0.0), 0.25, emit=(1, 0.55, 0.05), strength=10 if VIEW != "day" else 2)
DOME = mat("dome", (0.92, 0.92, 0.9), 0.35)
EQUIP = mat("equip", (0.11, 0.13, 0.16), 0.45, 0.2)
EQUIP2 = mat("equip2", (0.18, 0.2, 0.24), 0.5, 0.1)
YELLOW = mat("yellow", (0.85, 0.55, 0.05), 0.4)
LED_G = mat("ledg", (0, 0.4, 0.1), 0.3, emit=(0.1, 1, 0.3), strength=12)
LED_B = mat("ledb", (0, 0.2, 0.5), 0.3, emit=(0.2, 0.55, 1), strength=12)
SCREEN = mat("screen", (0.01, 0.02, 0.04), 0.2, emit=(0.15, 0.4, 0.8), strength=3)
ALU = mat("alu", (0.7, 0.72, 0.74), 0.3, 1.0)
GROUND = mat("ground", (0.5, 0.52, 0.55), 0.9)

def prism(name, prof, y0, y1, m, bevel=0.0):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    vs = [bm.verts.new((mm(x), y0, mm(z))) for x, z in prof]
    f = bm.faces.new(vs); bmesh.ops.recalc_face_normals(bm, faces=[f])
    r = bmesh.ops.extrude_face_region(bm, geom=[f]); top = [v for v in r["geom"] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0, y1 - y0, 0)); bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new(name, me); sc.collection.objects.link(ob); ob.data.materials.append(m)
    if bevel:
        md = ob.modifiers.new("bev", "BEVEL"); md.width = bevel; md.segments = 4; md.limit_method = "ANGLE"
    return ob
def box(name, x, y, z, sx, sy, sz, m, bevel=0.004):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(mm(x), mm(y), mm(z))); ob = bpy.context.active_object
    ob.name = name; ob.scale = (mm(sx), mm(sy), mm(sz)); bpy.ops.object.transform_apply(scale=True)
    ob.data.materials.append(m)
    if bevel: md = ob.modifiers.new("b", "BEVEL"); md.width = bevel; md.segments = 3
    return ob
def cyl(name, x, y, z, r, d, m, rot=(math.pi / 2, 0, 0), verts=64):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=mm(r), depth=mm(d), location=(mm(x), mm(y), mm(z)), rotation=rot)
    ob = bpy.context.active_object; ob.name = name; ob.data.materials.append(m); bpy.ops.object.shade_smooth(); return ob

W2 = 0.9475
# ---- 차체 프로파일(측면, x=후→전, z=높이) ----
prof = [(0, 420), (0, 1780), (35, 1870), (150, 1905), (3250, 1905), (3380, 1888), (3470, 1838), (4230, 1205), (4520, 1110), (4640, 1060), (4690, 980), (4695, 420), (4660, 340), (4380, 300),
        (4370, 300), (4360, 560), (4300, 690), (3390, 690), (3330, 560), (3320, 300), (1375, 300), (1365, 560), (1305, 690), (395, 690), (335, 560), (325, 300), (40, 330)]
cab = [(2430, 1905), (3250, 1905), (3380, 1888), (3470, 1838), (4230, 1205), (4520, 1110), (4640, 1060), (4690, 980), (4695, 420), (4660, 340), (4380, 300), (4370, 300), (4360, 560), (4300, 690), (3390, 690), (3330, 560), (3320, 300), (2430, 300)]
cargo = [(0, 420), (0, 1780), (35, 1870), (150, 1905), (2430, 1905), (2430, 300), (1375, 300), (1365, 560), (1305, 690), (395, 690), (335, 560), (325, 300), (40, 330)]
def bevel(ob, w=0.025):
    b = ob.modifiers.new("bev", "BEVEL"); b.width = w; b.segments = 5; b.limit_method = "ANGLE"; b.angle_limit = math.radians(35)
bevel(prism("cab", cab, -W2, W2, WHITE))
CUT = VIEW == "cutaway"
if not CUT:
    bevel(prism("cargo", cargo, -W2, W2, WHITE))
else:
    bevel(prism("wall_far", cargo, W2 - 0.03, W2, WHITE), 0.01)
    near = prism("wall_near", cargo, -W2, -W2 + 0.03, WHITE)
    c = box("cutter", 1300, -947, 1290, 2160, 200, 1120, INNER, 0); c.hide_render = True
    bo = near.modifiers.new("cut", "BOOLEAN"); bo.object = c; bo.operation = "DIFFERENCE"
    box("rear_wall", 15, 0, 1100, 30, 1895, 1400, WHITE, 0.01)
    box("wall_in_far", 1215, 900, 1150, 2400, 10, 1450, INNER, 0)
    box("sill", 1215, 0, 365, 2430, 1895, 130, CLAD, 0.01)
    # 절개 단면(남색 테두리)
    for (x, z, sx, sz) in [(1300, 730, 2160, 16), (1300, 1850, 2160, 16), (220, 1290, 16, 1120), (2380, 1290, 16, 1120)]:
        box("cutedge", x, -947, z, sx, 40, sz, mat("cutedge", (0.04, 0.12, 0.25), 0.5), 0)
# 클래딩(하단 띠)
clad = [(0, 420), (0, 560), (335, 560), (325, 300), (40, 330)]
for pr in (clad, [(1365, 560), (3330, 560), (3320, 300), (1375, 300)], [(4360, 560), (4695, 560), (4695, 420), (4660, 340), (4380, 300), (4370, 300)]):
    for y0 in (-W2 - 0.012, W2 - 0.03): prism("clad", pr, y0, y0 + 0.042, CLAD, 0.006)
for cx in (850, 3845):  # 휠아치 몰딩
    arch = [(cx - 520, 560), (cx - 455, 700), (cx + 455, 700), (cx + 520, 560), (cx + 470, 560), (cx + 410, 660), (cx - 410, 660), (cx - 470, 560)]
    for y0 in (-W2 - 0.015, W2 - 0.03): prism("arch", arch, y0, y0 + 0.045, CLAD, 0.004)
# 블랙 루프 앞단 + 글라스(윈드실드·1열 창)
prism("roofblk", [(3060, 1905), (3250, 1905), (3380, 1888), (3470, 1838), (3420, 1800), (3060, 1800)], -W2 - 0.004, W2 + 0.004, CLAD)
prism("glass_side", [(3060, 1190), (3060, 1790), (3380, 1822), (3455, 1792), (4200, 1215)], -W2 - 0.006, W2 + 0.006, GLASS)
ws = [(3470, 1838), (4230, 1205), (4205, 1195), (3445, 1825)]
prism("windshield", ws, -W2 + 0.06, W2 - 0.06, GLASS)
prism("hoodblk", [(4230, 1205), (4520, 1110), (4640, 1060), (4660, 1010), (4500, 1060), (4230, 1160)], -W2 + 0.03, W2 - 0.03, CLAD)
# 주간주행등(ㄱ자), 리어램프(세로)
for y in (-W2 + 0.04, W2 - 0.04):
    prism("drl", [(4230, 1200), (4520, 1105), (4645, 1055), (4645, 1040), (4520, 1090), (4230, 1185)], y - 0.01, y + 0.01, DRL)
for y in (-W2 + 0.05, W2 - 0.08):
    box("tail", -8, mm(0) or y * 1000, 1230, 20, 30, 840, RED, 0)
box("front_lower", 4690, 0, 520, 30, 1700, 380, CLAD, 0.01)
box("front_bar", 4693, 0, 760, 12, 1500, 22, DRL, 0)
box("plate", 4706, 0, 560, 6, 520, 110, mat("plate", (0.05, 0.05, 0.05), 0.5), 0)
# 미러
for s in (-1, 1): box("mirror", 3480, s * (W2 * 1000 + 70), 1240, 120, 110, 190, CLAD)
# 바퀴
for cx in (850, 3845):
    for s in (-1, 1):
        cyl("tire", cx, s * 790, 343, 343, 225, TIRE); cyl("rim", cx, s * 905, 343, 215, 12, RIM)
        for k in range(5):
            a = k * 72
            bpy.ops.mesh.primitive_cube_add(size=1, location=(mm(cx + 120 * math.cos(math.radians(a))), mm(s * 912), mm(343 + 120 * math.sin(math.radians(a)))), rotation=(0, -math.radians(a), 0))
            sp = bpy.context.active_object; sp.scale = (0.17, 0.006, 0.04); sp.data.materials.append(ALU if VIEW != "night" else RIM)
# ---- 외부 장비 ----
box("beacon_base", 2800, 0, 1925, 300, 1240, 40, EQUIP)
box("beacon", 2800, 0, 1965, 240, 1180, 50, AMBER, 0.012)
cyl("gnss_post", 2560, 560, 1935, 15, 60, EQUIP, rot=(0, 0, 0)); bpy.ops.mesh.primitive_uv_sphere_add(radius=mm(95), location=(mm(2560), mm(560), mm(1965))); d = bpy.context.active_object; d.scale.z = 0.55; d.data.materials.append(DOME); bpy.ops.object.shade_smooth()
box("cam_pod", 3200, 0, 1935, 190, 260, 60, EQUIP); cyl("cam_lens", 3300, 0, 1935, 18, 10, GLASS, rot=(0, math.pi / 2, 0))
for s in (-1, 1): box("side_cam", 3480, s * (W2 * 1000 + 70), 1360, 90, 70, 50, EQUIP)
# 후방 하부 다채널 GPR 어레이 + 브래킷
for bx in (-760, 0, 760):
    box("bracket", 250, bx, 230, 40, 40, 160, ALU)
box("gpr", 250, 0, 120, 520, 1800, 80, EQUIP2, 0.01)
for k in range(16): box("gpr_ch", 250, -850 + k * 113, 78, 420, 90, 6, EQUIP, 0)
box("encoder", 850, -W2 * 1000 - 130, 343, 70, 40, 70, YELLOW)
# ---- 카고룸 내부 ----
box("cargo_floor", 1290, 0, 430, 2250, 1820, 24, FLOOR, 0)
for yy in (-560, 560): box("wheelhouse", 850, yy, 560, 1000, 380, 260, INNER, 0.04)
box("bulkhead", 2415, 0, 1110, 30, 1830, 1360, INNER, 0)
# 5 Edge Gateway 랙: 격벽 쪽 원거리 벽에 붙이고 앞면이 통로(-y)를 향함
box("rack", 2150, 650, 1000, 480, 480, 1120, EQUIP, 0.01)
for k in range(7):
    box("rack_unit", 2150, 408, 520 + k * 150 + 40, 440, 6, 118, EQUIP2, 0.002)
    box("led", 1960, 404, 520 + k * 150 + 40, 16, 4, 16, LED_G if k % 3 else LED_B, 0)
    for v in range(3): box("vent", 2120 + v * 60, 404, 520 + k * 150 + 40, 40, 3, 70, EQUIP, 0)
# 작업대 + 모니터 + 좌석(통로 쪽)
box("desk", 2190, -120, 900, 380, 520, 28, ALU, 0.004)
box("monitor", 2330, -120, 1150, 30, 460, 280, EQUIP, 0.006); box("monitor_scr", 2313, -120, 1150, 4, 430, 250, SCREEN, 0)
cyl("seat_post", 1960, -200, 640, 30, 380, ALU, rot=(0, 0, 0)); box("seat", 1960, -200, 840, 400, 400, 60, EQUIP2, 0.02)
# 6 수동 GPR 카트(바닥 고정)
box("cart_body", 1500, 150, 560, 620, 460, 170, YELLOW, 0.02)
box("cart_top", 1500, 150, 652, 600, 440, 14, EQUIP, 0.004)
for cxw in (1270, 1730):
    for sgn in (-1, 1): cyl("cart_wheel", cxw, 150 + sgn * 255, 500, 65, 45, TIRE)
bpy.ops.mesh.primitive_cylinder_add(radius=mm(15), depth=mm(800), location=(mm(1890), mm(150), mm(930)), rotation=(0, math.radians(-28), 0)); hd = bpy.context.active_object; hd.data.materials.append(ALU); bpy.ops.object.shade_smooth()
box("cart_ui", 2070, 150, 1280, 70, 260, 180, EQUIP, 0.006); box("cart_scr", 2035, 150, 1280, 4, 230, 150, SCREEN, 0)
for k in range(2): box("strap", 1350 + k * 300, 150, 650, 40, 480, 8, mat("strap", (0.9, 0.4, 0.05), 0.6), 0)
# AR 글래스 충전함·선반(원거리 벽 상단)
box("shelf", 1400, 760, 1450, 1100, 300, 24, ALU, 0.004)
box("ar_case", 1180, 760, 1530, 380, 260, 140, EQUIP, 0.01); box("ar_led", 1180, 628, 1530, 30, 4, 12, LED_G, 0)
box("pelican", 1620, 760, 1530, 420, 260, 140, mat("pelican", (0.12, 0.28, 0.45), 0.5), 0.015)
# 7 후방 수납장(휠하우스 위)과 라바콘
box("locker", 650, 640, 1150, 900, 420, 820, EQUIP2, 0.01)
box("locker_split", 650, 428, 1150, 6, 4, 780, EQUIP, 0)
for hx in (610, 690): box("handle", hx, 424, 1150, 12, 10, 120, ALU, 0)
for k in range(3):
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=mm(130), radius2=mm(18), depth=mm(450), location=(mm(330), mm(-560 + k * 20), mm(667 + k * 70)))
    cn_ = bpy.context.active_object; cn_.data.materials.append(mat("cone", (0.95, 0.33, 0.04), 0.5)); bpy.ops.object.shade_smooth()
box("cone_base", 330, -560, 452, 300, 300, 30, mat("cone", (0.95, 0.33, 0.04), 0.5), 0.01)
box("scope_case", 720, -420, 520, 520, 340, 160, EQUIP, 0.015)
# 작업 조명
box("cargo_light", 1290, 900, 1870, 1800, 60, 12, mat("lamp", (1, 1, 1), 0.2, emit=(1, 0.96, 0.9), strength=6 if VIEW == "cutaway" else 0), 0)
# 지면
bpy.ops.mesh.primitive_plane_add(size=40, location=(2, 0, 0)); gp = bpy.context.active_object; gp.data.materials.append(GROUND)
# ---- 조명·카메라 ----
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]
if VIEW == "night":
    bg.inputs[0].default_value = (0.012, 0.02, 0.045, 1); bg.inputs[1].default_value = 1.0
else:
    bg.inputs[0].default_value = (0.82, 0.85, 0.9, 1); bg.inputs[1].default_value = 0.9
def light(kind, loc, energy, size=4, rot=(0, 0, 0), col=(1, 1, 1)):
    d = bpy.data.lights.new(kind + "L", kind); d.energy = energy; d.color = col
    if kind == "AREA": d.size = size
    o = bpy.data.objects.new(kind, d); o.location = loc; o.rotation_euler = rot; sc.collection.objects.link(o); return o
if VIEW == "night":
    light("AREA", (2.5, -6, 6), 300, 6, (math.radians(50), 0, 0), (0.6, 0.7, 1.0)); light("AREA", (8, 2, 3), 200, 4, (0, math.radians(70), 0), (1, 0.8, 0.6))
else:
    light("SUN", (0, 0, 10), 3.5, rot=(math.radians(45), math.radians(10), math.radians(-35)))
    light("AREA", (2.3, -7, 4), 900, 8, (math.radians(65), 0, 0)); light("AREA", (-4, -3, 3), 300, 5, (math.radians(60), 0, math.radians(-60)))
cam = bpy.data.cameras.new("cam"); co = bpy.data.objects.new("cam", cam); sc.collection.objects.link(co); sc.camera = co
cam.lens = 50
if VIEW == "cutaway": co.location = (mm(4300), mm(-6200), mm(6200)); tgt = Vector((mm(1700), mm(100), mm(700)))
elif VIEW == "rear": co.location = (mm(-4200), mm(-5200), mm(1500)); tgt = Vector((mm(900), 0, mm(800)))
else: co.location = (mm(8800), mm(-6200), mm(1600)); tgt = Vector((mm(2300), 0, mm(900)))
co.rotation_euler = (tgt - co.location).to_track_quat("-Z", "Y").to_euler()
# ---- 렌더 ----
sc.render.engine = "CYCLES"
prefs = bpy.context.preferences.addons["cycles"].preferences
try:
    prefs.compute_device_type = "METAL"; prefs.get_devices(); [setattr(d, "use", True) for d in prefs.devices]; sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = int(os.environ.get("SAMPLES", "160")); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True)
print("RENDERED", OUT)
