# PV5 카고룸 이동식 탐사 연구실 상세 모델 (Blender Cycles). 카고룸 2,255 x 1,565 x 1,520mm(기아 공식) 기준.
import bpy, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT, VIEW = argv[0], argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
mm = lambda v: v / 1000.0
L, Wd, H = 2255, 1565, 1520          # 카고룸
Y0 = -Wd / 2
def mat(n, c, r=0.4, m=0.0, e=None, s=0.0, tex=None):
    M = bpy.data.materials.new(n); M.use_nodes = True; nt = M.node_tree; b = nt.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m
    if e: b.inputs["Emission Color"].default_value = (*e, 1); b.inputs["Emission Strength"].default_value = s
    if tex == "wood":
        w = nt.nodes.new("ShaderNodeTexWave"); w.inputs["Scale"].default_value = 3; w.inputs["Distortion"].default_value = 6; w.inputs["Detail"].default_value = 4
        cr = nt.nodes.new("ShaderNodeValToRGB"); cr.color_ramp.elements[0].color = (0.36, 0.25, 0.14, 1); cr.color_ramp.elements[1].color = (0.55, 0.4, 0.24, 1)
        nt.links.new(w.outputs["Fac"], cr.inputs["Fac"]); nt.links.new(cr.outputs["Color"], b.inputs["Base Color"])
    if tex == "rubber":
        n = nt.nodes.new("ShaderNodeTexChecker"); n.inputs["Scale"].default_value = 120
        n.inputs["Color1"].default_value = (0.03, 0.032, 0.035, 1); n.inputs["Color2"].default_value = (0.06, 0.062, 0.066, 1)
        nt.links.new(n.outputs["Color"], b.inputs["Base Color"])
    return M
WOOD = mat("ply", (0.7, 0.55, 0.38), 0.6, tex="wood")
FLOOR = mat("floor", (0.04, 0.04, 0.045), 0.75, tex="rubber")
ALU = mat("alu", (0.78, 0.8, 0.82), 0.25, 1.0)
ALUB = mat("alub", (0.55, 0.57, 0.6), 0.35, 1.0)
BLACK = mat("black", (0.02, 0.022, 0.025), 0.4, 0.2)
DARK = mat("dark", (0.08, 0.085, 0.095), 0.45, 0.3)
GREY = mat("grey", (0.32, 0.34, 0.37), 0.4, 0.4)
WHITE = mat("white", (0.85, 0.86, 0.87), 0.3)
ORANGE = mat("orange", (0.95, 0.35, 0.03), 0.45)
YEL = mat("yel", (0.95, 0.65, 0.05), 0.35)
RED = mat("red", (0.7, 0.03, 0.02), 0.35)
BLUEC = mat("bluecase", (0.06, 0.18, 0.35), 0.45)
SCR = mat("scr", (0.01, 0.02, 0.04), 0.1, e=(0.25, 0.5, 1.0), s=3.5)
SCR2 = mat("scr2", (0.01, 0.02, 0.04), 0.1, e=(0.15, 0.85, 0.55), s=3)
LEDG = mat("ledg", (0, 0.2, 0.05), 0.3, e=(0.1, 1, 0.3), s=25)
LEDB = mat("ledb", (0, 0.1, 0.3), 0.3, e=(0.2, 0.5, 1), s=25)
LEDA = mat("leda", (0.3, 0.2, 0), 0.3, e=(1, 0.6, 0.1), s=25)
STRIP = mat("strip", (1, 1, 1), 0.2, e=(1, 0.95, 0.88), s=20)
PAINT = mat("paint", (0.82, 0.83, 0.82), 0.22)
GLASS = mat("glass", (0.01, 0.012, 0.016), 0.03)
def box(n, x, y, z, sx, sy, sz, m, bev=0.002):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(mm(x), mm(y), mm(z))); o = bpy.context.active_object
    o.name = n; o.scale = (mm(sx), mm(sy), mm(sz)); bpy.ops.object.transform_apply(scale=True); o.data.materials.append(m)
    if bev: d = o.modifiers.new("b", "BEVEL"); d.width = bev; d.segments = 3
    return o
def cyl(n, x, y, z, r, d, m, rot=(0, 0, 0), v=48):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=mm(r), depth=mm(d), location=(mm(x), mm(y), mm(z)), rotation=rot)
    o = bpy.context.active_object; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o
# ---- 쉘: 바닥·합판 벽·천장·격벽 (x=0 뒷문, x=L 격벽) ----
box("floor", L / 2, 0, -10, L, Wd, 20, FLOOR, 0)
for s in (-1, 1): box("wall", L / 2, s * (Wd / 2 + 9), H / 2, L, 18, H, WOOD, 0)
box("ceil", L / 2, 0, H + 9, L, Wd, 18, WHITE, 0)
box("bulk", L + 9, 0, H / 2, 18, Wd, H, WOOD, 0)
for s in (-1, 1): box("wh", 760, s * (Wd / 2 - 160), 140, 900, 320, 280, WOOD, 0.01)   # 휠하우스(합판 커버)
for x in (300, 900, 1500, 2100):                                                        # 바닥 고정 레일
    box("rail", x, 0, 2, 30, Wd - 60, 4, ALUB, 0)
for s in (-1, 1): box("led", L / 2, s * (Wd / 2 - 120), H - 6, L - 200, 30, 8, STRIP, 0)  # 천장 LED 스트립
box("tray", L / 2, -Wd / 2 + 60, H - 80, L - 300, 100, 40, ALUB, 0.002)                    # 케이블 트레이
# ---- 우측(+y) 격벽 쪽: 19인치 랙 2개 ----
for k, rx in enumerate((L - 330, L - 330 - 620)):
    box("rack", rx, Wd / 2 - 330, 650, 600, 600, 1300, BLACK, 0.006)
    fy = Wd / 2 - 330 - 302
    for u in range(9):
        z = 120 + u * 130
        box("unit", rx, fy, z + 50, 520, 6, 110, DARK if u % 2 else GREY, 0.002)
        for v in range(3): box("vent", rx - 120 + v * 40, fy - 4, z + 50, 25, 3, 80, BLACK, 0)
        box("led1", rx + 200, fy - 4, z + 70, 14, 3, 10, LEDG if (u + k) % 3 else LEDB, 0)
        box("led2", rx + 230, fy - 4, z + 70, 14, 3, 10, LEDA if u % 4 == 0 else LEDG, 0)
    box("rack_scr", rx, fy - 4, 1180, 300, 3, 120, SCR2, 0)
# ---- 좌측(-y) 격벽 쪽: 운영자 작업대(듀얼 모니터) ----
dx = L - 450
box("desk", dx, -Wd / 2 + 280, 760, 820, 520, 30, ALU, 0.004)
box("desk_leg", dx - 360, -Wd / 2 + 280, 380, 40, 480, 740, ALUB, 0.002)
box("drawers", dx + 250, -Wd / 2 + 280, 380, 320, 480, 740, ALUB, 0.004)
for d in range(3): box("dr", dx + 250, -Wd / 2 + 520, 150 + d * 240, 300, 6, 200, ALU, 0.002); box("dh", dx + 250, -Wd / 2 + 526, 220 + d * 240, 120, 10, 14, BLACK, 0)
for k, a in ((-1, 12), (1, -12)):
    mx = dx + k * 210
    box("mon", mx, -Wd / 2 + 110, 1080, 520, 30, 320, BLACK, 0.006).rotation_euler = (0, 0, math.radians(a))
    s_ = box("monscr", mx, -Wd / 2 + 128, 1085, 490, 4, 285, SCR, 0); s_.rotation_euler = (0, 0, math.radians(a))
    box("arm", mx, -Wd / 2 + 60, 920, 30, 80, 300, ALUB, 0)
box("kb", dx, -Wd / 2 + 380, 782, 420, 140, 16, BLACK, 0.003)
box("mouse", dx + 300, -Wd / 2 + 380, 782, 60, 100, 20, BLACK, 0.01)
cyl("seat_post", dx - 40, -Wd / 2 + 650, 260, 25, 520, ALUB)
box("seat", dx - 40, -Wd / 2 + 650, 540, 440, 420, 80, BLACK, 0.03)
box("back", dx - 40, -Wd / 2 + 840, 700, 380, 50, 260, BLACK, 0.03)
# ---- 좌측 벽 상부: 알루미늄 선반 + 케이스 ----
for z in (1250,):
    box("shelf", 900, -Wd / 2 + 180, z, 1300, 340, 20, ALU, 0.002)
    box("lip", 900, -Wd / 2 + 345, z + 40, 1300, 10, 80, ALU, 0)
    box("peli1", 520, -Wd / 2 + 180, z + 110, 380, 300, 200, BLUEC, 0.02)
    box("peli2", 930, -Wd / 2 + 180, z + 110, 380, 300, 200, DARK, 0.02)
    box("arcase", 1320, -Wd / 2 + 180, z + 90, 300, 280, 160, BLACK, 0.02); box("arled", 1320, -Wd / 2 + 322, z + 120, 40, 3, 12, LEDG, 0)
# 좌측 벽 하부: 서랍식 수납 랙(휠하우스 뒤)
box("cab", 260, -Wd / 2 + 230, 420, 420, 440, 840, ALUB, 0.004)
for d in range(4): box("cdr", 260, -Wd / 2 + 452, 140 + d * 190, 400, 6, 170, ALU, 0.002); box("cdh", 260, -Wd / 2 + 458, 200 + d * 190, 140, 10, 14, BLACK, 0)
# ---- 바닥 중앙: 수동 GPR 카트(스트랩 고정) ----
cx, cy = 1250, 120
box("cart", cx, cy, 160, 700, 480, 200, YEL, 0.02); box("cart_top", cx, cy, 266, 680, 460, 12, DARK, 0.004)
for ox in (-280, 280):
    for oy in (-260, 260): cyl("wheel", cx + ox, cy + oy, 70, 70, 50, BLACK, rot=(math.pi / 2, 0, 0))
for oy in (-150, 150): cyl("handle", cx + 120, cy + oy, 300, 14, 820, ALU, rot=(0, math.pi / 2, 0))   # 접힌 손잡이(적재 상태)
box("cart_ui", cx - 120, cy, 300, 260, 200, 50, DARK, 0.006); box("cart_scr", cx - 120, cy, 326, 230, 170, 4, SCR, 0)
for ox in (-200, 200): box("strap", cx + ox, cy, 276, 50, 560, 6, ORANGE, 0)
# ---- 우측 뒤쪽: 라바콘·소화기·응급함 ----
for k in range(3):
    bpy.ops.mesh.primitive_cone_add(vertices=48, radius1=mm(140), radius2=mm(20), depth=mm(480), location=(mm(250), mm(Wd / 2 - 260), mm(250 + k * 60)))
    o = bpy.context.active_object; o.data.materials.append(ORANGE); bpy.ops.object.shade_smooth()
box("cone_base", 250, Wd / 2 - 260, 15, 320, 320, 30, ORANGE, 0.01)
cyl("ext", 600, Wd / 2 - 70, 330, 75, 520, RED); cyl("ext_top", 600, Wd / 2 - 70, 610, 30, 60, BLACK)
box("aid", 600, Wd / 2 - 20, 900, 260, 30, 200, WHITE, 0.01); box("aidx", 600, Wd / 2 - 38, 900, 30, 4, 120, RED, 0); box("aidy", 600, Wd / 2 - 38, 900, 120, 4, 30, RED, 0)
box("scope", 600, Wd / 2 - 260, 120, 500, 300, 240, DARK, 0.015)
# ---- 차체 외곽(문틀·도어) : 실사화 시 PV5 실차 느낌 ----
if VIEW == "rear":
    for s in (-1, 1):
        box("frame", -20, s * (Wd / 2 + 60), H / 2 + 40, 60, 110, H + 160, PAINT, 0.01)
        d = box("door", -460, s * (Wd / 2 + 520), H / 2 + 40, 40, 860, H + 120, PAINT, 0.01)
        box("door_in", -440, s * (Wd / 2 + 520), H / 2 + 40, 6, 780, H - 40, WOOD, 0)
        box("tail", -20, s * (Wd / 2 + 95), H / 2 + 120, 40, 40, 900, mat("tail", (0.5, 0.02, 0.02), 0.2, e=(1, 0.05, 0.03), s=4), 0.004)
    box("sill", -20, 0, -60, 60, Wd + 220, 120, BLACK, 0.01)
    box("roofedge", -20, 0, H + 70, 60, Wd + 220, 80, PAINT, 0.01)
# ---- 조명·카메라 ----
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
world.node_tree.nodes["Background"].inputs[0].default_value = (0.55, 0.6, 0.68, 1); world.node_tree.nodes["Background"].inputs[1].default_value = 0.6
for s in (-1, 1):
    l = bpy.data.lights.new("a", "AREA"); l.energy = 45; l.size = 1.8; l.color = (1, 0.96, 0.9)
    o = bpy.data.objects.new("a", l); o.location = (mm(L / 2), mm(s * 450), mm(H - 30)); sc.collection.objects.link(o)
fl = bpy.data.lights.new("f", "AREA"); fl.energy = 150; fl.size = 3; fo = bpy.data.objects.new("f", fl); fo.location = (-2.5, 0, 1.4); fo.rotation_euler = (0, math.radians(-90), 0); sc.collection.objects.link(fo)
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); sc.collection.objects.link(co); sc.camera = co
V = {"rear": ((-2.25, -0.05, 1.05), (1.4, 0.05, 0.75), 20), "work": ((0.35, -0.05, 1.3), (2.0, -0.55, 0.95), 18), "racks": ((0.6, -0.45, 1.15), (2.0, 0.5, 0.75), 16)}[VIEW]
co.location = V[0]; cam.lens = V[2]; co.rotation_euler = (Vector(V[1]) - Vector(V[0])).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"
try:
    p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices(); [setattr(d, "use", True) for d in p.devices]; sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = int(os.environ.get("SAMPLES", "200")); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"; sc.view_settings.exposure = -0.4
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print("RENDERED", OUT)
