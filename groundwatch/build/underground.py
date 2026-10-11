# 도로 지하 단면 실사 렌더 (Blender Cycles). view: mech(사고 원인 단면) / twin(지상 지도 + 지하 블록)
import bpy, bmesh, math, sys, os, json
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT, VIEW = argv[0], argv[1]
MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "map", "gangdong_z16.png")
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene

def nodes(M):
    M.use_nodes = True; nt = M.node_tree; return nt, nt.nodes["Principled BSDF"]

def ramp(nt, stops):
    r = nt.nodes.new("ShaderNodeValToRGB"); e = r.color_ramp.elements
    e[0].position, e[0].color = stops[0][0], (*stops[0][1], 1)
    e[1].position, e[1].color = stops[-1][0], (*stops[-1][1], 1)
    for p, c in stops[1:-1]: x = e.new(p); x.color = (*c, 1)
    return r

def bump(nt, b, src, strength, dist=0.02):
    bp = nt.nodes.new("ShaderNodeBump"); bp.inputs["Strength"].default_value = strength; bp.inputs["Distance"].default_value = dist
    nt.links.new(src, bp.inputs["Height"]); nt.links.new(bp.outputs["Normal"], b.inputs["Normal"])

def earth(name, stops, scale=3.0, pebbles=0.0, peb_scale=40, rough=0.95, bstr=0.6, stretch=(1, 1, 1), stones=0.0, st_scale=8, wet=None):
    """흙·자갈 재질: 층리 방향으로 늘린 노이즈 + 미세 입자 + 자갈 + (선택) 젖은 영역"""
    M = bpy.data.materials.new(name); nt, b = nodes(M)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping"); mp.inputs["Scale"].default_value = stretch
    nt.links.new(tc.outputs["Object"], mp.inputs["Vector"]); V = mp.outputs["Vector"]
    def noise(sc_, det=12, rgh=0.62):
        n = nt.nodes.new("ShaderNodeTexNoise"); n.inputs["Scale"].default_value = sc_; n.inputs["Detail"].default_value = det; n.inputs["Roughness"].default_value = rgh
        nt.links.new(V, n.inputs["Vector"]); return n.outputs["Fac"]
    def mixc(A, B, f, mode="MIX"):
        m = nt.nodes.new("ShaderNodeMix"); m.data_type = "RGBA"; m.blend_type = mode
        if isinstance(f, float): m.inputs["Factor"].default_value = f
        else: nt.links.new(f, m.inputs["Factor"])
        nt.links.new(A, m.inputs["A"])
        if isinstance(B, tuple): m.inputs["B"].default_value = (*B, 1)
        else: nt.links.new(B, m.inputs["B"])
        return m.outputs["Result"]
    h1 = noise(scale); r = ramp(nt, stops); nt.links.new(h1, r.inputs["Fac"]); col = r.outputs["Color"]
    g = noise(scale * 14, 6, 0.75); gr = ramp(nt, [(0.3, (0.55, 0.55, 0.55)), (0.7, (1, 1, 1))]); nt.links.new(g, gr.inputs["Fac"])
    col = mixc(col, gr.outputs["Color"], 0.55, "MULTIPLY")
    hm = nt.nodes.new("ShaderNodeMath"); hm.operation = "ADD"; nt.links.new(h1, hm.inputs[0]); nt.links.new(g, hm.inputs[1]); height = hm.outputs[0]
    if pebbles:
        v = nt.nodes.new("ShaderNodeTexVoronoi"); v.feature = "DISTANCE_TO_EDGE"; v.inputs["Scale"].default_value = peb_scale
        nt.links.new(tc.outputs["Object"], v.inputs["Vector"])
        pr = ramp(nt, [(0.0, (0, 0, 0)), (0.06, (1, 1, 1))]); nt.links.new(v.outputs["Distance"], pr.inputs["Fac"])
        col = mixc(col, pr.outputs["Color"], pebbles, "MULTIPLY")
        h2 = nt.nodes.new("ShaderNodeMath"); h2.operation = "ADD"; nt.links.new(height, h2.inputs[0]); nt.links.new(pr.outputs["Color"], h2.inputs[1]); height = h2.outputs[0]
    if stones:  # 흩어진 돌: 보로노이 셀 중심 근처만, 셀마다 다른 회색
        v = nt.nodes.new("ShaderNodeTexVoronoi"); v.inputs["Scale"].default_value = st_scale; v.inputs["Randomness"].default_value = 1.0
        nt.links.new(tc.outputs["Object"], v.inputs["Vector"])
        mk = ramp(nt, [(0.0, (1, 1, 1)), (stones, (1, 1, 1)), (stones + 0.04, (0, 0, 0)), (1.0, (0, 0, 0))]); nt.links.new(v.outputs["Distance"], mk.inputs["Fac"])
        sv = nt.nodes.new("ShaderNodeSeparateColor"); nt.links.new(v.outputs["Color"], sv.inputs["Color"])
        stc = ramp(nt, [(0, (0.18, 0.17, 0.16)), (0.5, (0.42, 0.4, 0.37)), (1, (0.66, 0.63, 0.58))]); nt.links.new(sv.outputs["Red"], stc.inputs["Fac"])
        stc2 = mixc(stc.outputs["Color"], gr.outputs["Color"], 0.4, "MULTIPLY")
        col = mixc(col, stc2, mk.outputs["Color"])
        h3 = nt.nodes.new("ShaderNodeMath"); h3.operation = "MULTIPLY_ADD"; nt.links.new(mk.outputs["Color"], h3.inputs[0]); h3.inputs[1].default_value = 0.8; nt.links.new(height, h3.inputs[2]); height = h3.outputs[0]
    rough_out = None
    if wet:  # 젖은 영역: 중심점에서 거리 기반으로 어둡게, 덜 거칠게
        (cx, cy, cz), rad = wet
        d = nt.nodes.new("ShaderNodeVectorMath"); d.operation = "DISTANCE"; nt.links.new(tc.outputs["Object"], d.inputs[0]); d.inputs[1].default_value = (cx, cy, cz)
        wn = noise(scale * 3, 8, 0.6); wd = nt.nodes.new("ShaderNodeMath"); wd.operation = "MULTIPLY_ADD"; nt.links.new(wn, wd.inputs[0]); wd.inputs[1].default_value = rad * 0.6; nt.links.new(d.outputs["Value"], wd.inputs[2])
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = rad * 0.55; mr.inputs["From Max"].default_value = rad * 1.25; mr.inputs["To Min"].default_value = 1; mr.inputs["To Max"].default_value = 0
        nt.links.new(wd.outputs[0], mr.inputs["Value"])
        col = mixc(col, (0.16, 0.12, 0.09), mr.outputs["Result"], "MULTIPLY")
        rr = nt.nodes.new("ShaderNodeMath"); rr.operation = "MULTIPLY_ADD"; nt.links.new(mr.outputs["Result"], rr.inputs[0]); rr.inputs[1].default_value = -0.45; rr.inputs[2].default_value = rough
        rough_out = rr.outputs[0]
    nt.links.new(col, b.inputs["Base Color"]); b.inputs["Roughness"].default_value = rough
    if rough_out: nt.links.new(rough_out, b.inputs["Roughness"])
    bump(nt, b, height, bstr)
    return M

TEX = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tex")
def pbr(name, tex, tile=1.0, tint=None, bstr=1.0, wet=None, stretch=(1, 1, 1)):
    """Poly Haven CC0 스캔 텍스처 박스 투영 재질. tile = 텍스처 한 장이 덮는 길이(m)"""
    M = bpy.data.materials.new(name); nt, b = nodes(M)
    tc = nt.nodes.new("ShaderNodeTexCoord"); mp = nt.nodes.new("ShaderNodeMapping")
    mp.inputs["Scale"].default_value = (stretch[0] / tile, stretch[1] / tile, stretch[2] / tile); nt.links.new(tc.outputs["Object"], mp.inputs["Vector"])
    def im(kind, colorspace):
        t = nt.nodes.new("ShaderNodeTexImage"); t.image = bpy.data.images.load(os.path.join(TEX, f"{tex}_{kind}.jpg")); t.image.colorspace_settings.name = colorspace
        t.projection = "BOX"; t.projection_blend = 0.25; nt.links.new(mp.outputs["Vector"], t.inputs["Vector"]); return t
    d = im("diff", "sRGB"); r = im("rough", "Non-Color"); n = im("nor", "Non-Color")
    col = d.outputs["Color"]
    if tint:
        h = nt.nodes.new("ShaderNodeHueSaturation"); h.inputs["Saturation"].default_value = tint[0]; h.inputs["Value"].default_value = tint[1]
        nt.links.new(col, h.inputs["Color"]); col = h.outputs["Color"]
    rough = r.outputs["Color"]
    if wet:
        (cx, cy, cz), rad = wet
        dd = nt.nodes.new("ShaderNodeVectorMath"); dd.operation = "DISTANCE"; nt.links.new(tc.outputs["Object"], dd.inputs[0]); dd.inputs[1].default_value = (cx, cy, cz)
        nz = nt.nodes.new("ShaderNodeTexNoise"); nz.inputs["Scale"].default_value = 3; nz.inputs["Detail"].default_value = 8; nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
        wd = nt.nodes.new("ShaderNodeMath"); wd.operation = "MULTIPLY_ADD"; nt.links.new(nz.outputs["Fac"], wd.inputs[0]); wd.inputs[1].default_value = rad * 0.7; nt.links.new(dd.outputs["Value"], wd.inputs[2])
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.inputs["From Min"].default_value = rad * 0.6; mr.inputs["From Max"].default_value = rad * 1.3; mr.inputs["To Min"].default_value = 1; mr.inputs["To Max"].default_value = 0
        nt.links.new(wd.outputs[0], mr.inputs["Value"])
        mx = nt.nodes.new("ShaderNodeMix"); mx.data_type = "RGBA"; mx.blend_type = "MULTIPLY"; nt.links.new(mr.outputs["Result"], mx.inputs["Factor"])
        nt.links.new(col, mx.inputs["A"]); mx.inputs["B"].default_value = (0.22, 0.2, 0.2, 1); col = mx.outputs["Result"]
        rm = nt.nodes.new("ShaderNodeMix"); rm.data_type = "RGBA"; nt.links.new(mr.outputs["Result"], rm.inputs["Factor"]); nt.links.new(rough, rm.inputs["A"]); rm.inputs["B"].default_value = (0.35, 0.35, 0.35, 1); rough = rm.outputs["Result"]
    nt.links.new(col, b.inputs["Base Color"]); nt.links.new(rough, b.inputs["Roughness"])
    nm = nt.nodes.new("ShaderNodeNormalMap"); nm.inputs["Strength"].default_value = bstr; nt.links.new(n.outputs["Color"], nm.inputs["Color"]); nt.links.new(nm.outputs["Normal"], b.inputs["Normal"])
    return M

def plain(name, c, r=0.5, m=0.0, e=None, s=0.0, alpha=1.0, trans=0.0):
    M = bpy.data.materials.new(name); nt, b = nodes(M)
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m
    if e: b.inputs["Emission Color"].default_value = (*e, 1); b.inputs["Emission Strength"].default_value = s
    if alpha < 1: b.inputs["Alpha"].default_value = alpha; M.blend_method = "BLEND" if hasattr(M, "blend_method") else None
    if trans: b.inputs["Transmission Weight"].default_value = trans
    return M

ASPH = pbr("asphalt", "asphalt_02", 3.5, (0.6, 0.75))
BASE = pbr("base", "rocky_gravel", 0.9, (0.7, 0.9), 1.4)
FILL = pbr("fill", "excavated_soil_wall", 2.8, (0.8, 0.9), 1.3, wet=((0.9, -2.2, -1.45), 1.1))
SAND = pbr("sand", "coast_sand_05", 1.6, (0.9, 1.35), 1.6)
CLAY = pbr("clay", "brown_mud_02", 2.0, (0.7, 0.55), 1.0)
VOID = pbr("void", "excavated_soil_wall", 1.0, (0.9, 0.38), 2.0)
CONC = pbr("concrete", "concrete_floor_02", 1.5, (0.6, 0.85), 1.0)
CONC_IN = pbr("conc_in", "concrete_slab_wall", 1.5, (0.4, 0.35), 1.0)
PAINT_W = plain("lane_w", (0.85, 0.85, 0.82), 0.6)
PAINT_Y = plain("lane_y", (0.85, 0.62, 0.08), 0.6)
CURB = pbr("curb", "concrete_pavement", 1.2, (0.5, 0.95), 0.8)
WATER = plain("water", (0.1, 0.35, 0.8), 0.05, e=(0.2, 0.5, 1.0), s=0.3)
GW = plain("gw", (0.2, 0.45, 0.9), 0.3, alpha=0.32)
AMBER = plain("amber", (1.0, 0.62, 0.1), 0.4, e=(1.0, 0.55, 0.08), s=12)
CAST = plain("cast", (0.2, 0.21, 0.22), 0.45, 0.6)

def box(name, x0, x1, y0, y1, z0, z1, m, bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))
    o = bpy.context.active_object; o.name = name; o.scale = (x1 - x0, y1 - y0, z1 - z0); bpy.ops.object.transform_apply(scale=True)
    o.data.materials.append(m)
    if bev: d = o.modifiers.new("b", "BEVEL"); d.width = bev; d.segments = 3
    return o

def cyl(name, r, depth, loc, rot, m, v=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object; o.name = name; o.data.materials.append(m); bpy.ops.object.shade_smooth(); return o

def cut(target, cutter, keep_mat=None):
    md = target.modifiers.new("cut", "BOOLEAN"); md.operation = "DIFFERENCE"; md.object = cutter; md.solver = "EXACT"
    if keep_mat:  # 절단면에 다른 재질
        target.data.materials.append(keep_mat); cutter.data.materials.clear(); cutter.data.materials.append(keep_mat)
        md.material_mode = "TRANSFER"
    bpy.context.view_layer.objects.active = target; bpy.ops.object.modifier_apply(modifier="cut")

def blob(name, loc, size, seed=0):
    """울퉁불퉁한 공동(void) 커터"""
    bpy.ops.mesh.primitive_uv_sphere_add(segments=96, ring_count=48, location=loc)
    o = bpy.context.active_object; o.name = name; o.scale = size; bpy.ops.object.transform_apply(scale=True)
    tx = bpy.data.textures.new(name + "t", "CLOUDS"); tx.noise_scale = 0.35; tx.noise_depth = 3
    d = o.modifiers.new("d", "DISPLACE"); d.texture = tx; d.strength = 0.22; d.mid_level = 0.5
    bpy.ops.object.modifier_apply(modifier="d"); return o

L0, L1, Y0, Y1, BOT = -5.0, 5.0, -2.2, 2.2, -5.0
TOP = 0.0
if VIEW == "mech":
    asph = box("asph", L0, L1, Y0, Y1, -0.22, TOP, ASPH)
    base = box("base", L0, L1, Y0, Y1, -0.6, -0.22, BASE)
    fill = box("fill", L0, L1, Y0, Y1, -2.9, -0.6, FILL)
    sand = box("sand", L0, L1, Y0, Y1, -3.9, -2.9, SAND)
    clay = box("clay", L0, L1, Y0, Y1, BOT, -3.9, CLAY)
    # 노후 하수관(단면이 보이도록 y축 방향), 누수 이음부
    px, pz, pr = 1.3, -1.75, 0.55
    pipe = cyl("pipe", pr, Y1 - Y0, (px, 0, pz), (math.pi / 2, 0, 0), CONC)
    hole = cyl("pipe_hole", pr - 0.08, Y1 - Y0 + 0.2, (px, 0, pz), (math.pi / 2, 0, 0), CONC_IN)
    for t in (fill,): cut(t, cyl("pc", pr, Y1 - Y0 + 0.2, (px, 0, pz), (math.pi / 2, 0, 0), CONC))
    cut(pipe, hole, CONC_IN); bpy.data.objects.remove(hole)
    for o in list(bpy.data.objects):
        if o.name.startswith("pc"): bpy.data.objects.remove(o)
    # 공동: 포장 바로 아래 기층·성토층을 파고 들어간 빈 공간
    cav = blob("cav", (0.2, -1.4, -1.0), (1.5, 1.6, 0.62))
    cav.data.materials.append(VOID)
    for t in (base, fill): cut(t, cav, VOID)
    bpy.data.objects.remove(cav)
    # 하부 지하철/터널(라이닝)
    tz, tr = -4.25, 0.95
    tun = cyl("tunnel", tr + 0.18, Y1 - Y0, (-2.6, 0, tz), (math.pi / 2, 0, 0), CONC)
    th = cyl("th", tr, Y1 - Y0 + 0.2, (-2.6, 0, tz), (math.pi / 2, 0, 0), CONC_IN)
    for t in (sand, clay): cut(t, cyl("tc", tr + 0.18, Y1 - Y0 + 0.2, (-2.6, 0, tz), (math.pi / 2, 0, 0), CONC))
    cut(tun, th, CONC_IN); bpy.data.objects.remove(th)
    for o in list(bpy.data.objects):
        if o.name.startswith("tc"): bpy.data.objects.remove(o)
    box("tun_floor", -3.45, -1.75, Y0, Y1, tz - 0.62, tz - 0.55, CONC)
    # 노면: 차선, 연석·보도
    for x in range(-5, 5, 2): box("lane", x + 0.2, x + 1.3, -0.06, 0.06, TOP, TOP + 0.004, PAINT_W)
    for dy in (-1.95, -1.85): box("lane_y", L0, L1, dy - 0.03, dy + 0.03, TOP, TOP + 0.004, PAINT_Y)
    box("curb", L0, L1, 1.7, 1.86, -0.22, 0.15, CURB); box("walk", L0, L1, 1.86, Y1, -0.22, 0.12, CURB)
    # 맨홀
    mh = cyl("manhole", 0.33, 0.012, (3.4, 0.7, TOP + 0.003), (0, 0, 0), CAST, 64)
    cam_loc, cam_tgt, lens = (9.4, -16.8, 4.2), (0.1, 0.0, -2.75), 40
elif VIEW == "freq":  # 주파수별 탐사 깊이: 단면 블록 + 노면 위 안테나 3종
    box("asph", L0, L1, Y0, Y1, -0.22, TOP, ASPH); box("base", L0, L1, Y0, Y1, -0.6, -0.22, BASE)
    fill = box("fill", L0, L1, Y0, Y1, -2.9, -0.6, FILL); box("sand", L0, L1, Y0, Y1, -3.9, -2.9, SAND); box("clay", L0, L1, Y0, Y1, BOT, -3.9, CLAY)
    for i, (x, z, r) in enumerate([(-1.7, -1.3, 0.35), (2.2, -2.4, 0.25)]):
        p_ = cyl("p%d" % i, r, Y1 - Y0, (x, 0, z), (math.pi / 2, 0, 0), CONC); cut(fill, cyl("pc%d" % i, r, Y1 - Y0 + 0.2, (x, 0, z), (math.pi / 2, 0, 0), CONC))
        h_ = cyl("ph", r - 0.06, Y1 - Y0 + 0.2, (x, 0, z), (math.pi / 2, 0, 0), CONC_IN); cut(p_, h_, CONC_IN); bpy.data.objects.remove(h_)
    for o in list(bpy.data.objects):
        if o.name.startswith("pc"): bpy.data.objects.remove(o)
    ANT = plain("ant", (0.1, 0.11, 0.12), 0.45, 0.3); STR = plain("stripe", (0.95, 0.68, 0.05), 0.4)
    for x in (-3.3, 0.0, 3.3):
        box("ant", x - 0.55, x + 0.55, Y0 + 0.05, Y0 + 0.75, 0.0, 0.16, ANT, 0.015); box("st", x - 0.55, x + 0.55, Y0 + 0.04, Y0 + 0.05, 0.1, 0.13, STR, 0)
    for x in range(-5, 5, 2): box("lane", x + 0.2, x + 1.3, 0.9, 1.02, TOP, TOP + 0.004, PAINT_W)
    cam_loc, cam_tgt, lens = (5.5, -17.5, 3.4), (0.0, 0.0, -2.35), 40
elif VIEW == "road":  # 교차검증: 비스듬히 내려다본 실제 도로면
    RL0, RL1, RY0, RY1 = -16.0, 16.0, -9.0, 9.0
    box("asph", RL0, RL1, RY0, RY1, -0.2, 0.0, pbr("asph2", "asphalt_02", 3.0, (0.55, 0.8)), 0)
    for x in [i * 3.0 - 16 for i in range(11)]: box("lane", x + 0.5, x + 2.3, -0.07, 0.07, 0, 0.004, PAINT_W, 0)
    for dy in (3.55, 3.7): box("ly", RL0, RL1, dy - 0.05, dy + 0.05, 0, 0.004, PAINT_Y, 0)
    box("edge", RL0, RL1, -3.62, -3.52, 0, 0.004, PAINT_W, 0)
    box("curb", RL0, RL1, -4.3, -4.0, -0.2, 0.14, CURB, 0); box("walk", RL0, RL1, -9.0, -4.3, -0.2, 0.12, CURB, 0)
    for dy in (-1.55, 1.55): pass
    mh = cyl("manhole", 0.36, 0.01, (-5.6, -2.0, 0.003), (0, 0, 0), CAST, 64); bpy.ops.object.shade_flat()
    Y0, Y1, L0, L1, BOT = RY0, RY1, -13.0, 13.0, -0.2
    cam_loc, cam_tgt, lens = (0.6, -7.5, 13.5), (0.6, -0.4, 0.0), 30
elif VIEW == "layers":  # 데이터 레이어 분해 스택: 지도 기반 판 7장 + 같은 좌표를 관통하는 기준선
    IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "3d")
    PW, PD, GAP = 8.0, 5.0, 0.95
    for i in range(7):
        z = (6 - i) * GAP
        bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, z)); o = bpy.context.active_object; o.scale = (PW, PD, 1); bpy.ops.object.transform_apply(scale=True)
        sl = o.modifiers.new("s", "SOLIDIFY"); sl.thickness = 0.06; bv = o.modifiers.new("b", "BEVEL"); bv.width = 0.02; bv.segments = 2
        M = bpy.data.materials.new(f"lt{i}"); nt, b = nodes(M); it = nt.nodes.new("ShaderNodeTexImage"); it.image = bpy.data.images.load(os.path.join(IMG, f"lt_{i}.png"))
        nt.links.new(it.outputs["Color"], b.inputs["Base Color"]); nt.links.new(it.outputs["Color"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 0.55
        b.inputs["Roughness"].default_value = 0.22; b.inputs["Coat Weight"].default_value = 0.6
        o.data.materials.append(M)
        box("edge", -PW / 2, PW / 2, -PD / 2 - 0.004, -PD / 2, z - 0.03, z + 0.03, plain(f"ed{i}", (0.55, 0.62, 0.72), 0.3, 0.8), 0)
    BEAM = plain("bm", (1, 0.6, 0.1), 0.4, e=(1.0, 0.55, 0.08), s=10)
    bx, by = -0.6, -0.15
    cyl("beam", 0.016, 6 * GAP + 0.6, (bx, by, 3 * GAP), (0, 0, 0), BEAM, 16)
    for i in range(7):
        bpy.ops.mesh.primitive_torus_add(major_radius=0.14, minor_radius=0.014, location=(bx, by, (6 - i) * GAP + 0.04)); bpy.context.active_object.data.materials.append(BEAM)
    Y0, Y1, L0, L1, BOT = -PD / 2, PD / 2, -PW / 2, PW / 2, -0.3
    cam_loc, cam_tgt, lens = (12.5, -20.0, 10.5), (1.2, 0.0, 2.9), 44  # L
elif VIEW == "patrol":  # 위험도별 순찰망: 기울인 어두운 지도 위에 빛나는 경로 튜브
    IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "3d")
    PR = json.load(open(os.path.join(IMG, "patrol_routes.json"))); MW, MH = 24.0, 15.0
    def mxy(px, py): u = px * PR["k"] / 2048; v = py * PR["k"] / 1280; return ((u - 0.5) * MW, (0.5 - v) * MH)
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 0)); mp = bpy.context.active_object; mp.scale = (MW, MH, 1); bpy.ops.object.transform_apply(scale=True)
    M = bpy.data.materials.new("mapd"); nt, b = nodes(M); it = nt.nodes.new("ShaderNodeTexImage"); it.image = bpy.data.images.load(os.path.join(IMG, "map_dark.png"))
    tn = nt.nodes.new("ShaderNodeMix"); tn.data_type = "RGBA"; tn.blend_type = "MULTIPLY"; tn.inputs["Factor"].default_value = 1.0; tn.inputs["B"].default_value = (0.45, 0.65, 1.0, 1)
    nt.links.new(it.outputs["Color"], tn.inputs["A"]); nt.links.new(tn.outputs["Result"], b.inputs["Base Color"]); nt.links.new(tn.outputs["Result"], b.inputs["Emission Color"]); b.inputs["Emission Strength"].default_value = 0.6; b.inputs["Roughness"].default_value = 0.5
    mp.data.materials.append(M)
    box("under", -60, 60, -60, 60, -0.03, -0.01, plain("und", (0.035, 0.045, 0.065), 0.6))
    def hx(c): c = c.lstrip("#"); return tuple(int(c[i:i + 2], 16) / 255 for i in (0, 2, 4))
    for r in PR["routes"]:
        cu = bpy.data.curves.new(r["n"], "CURVE"); cu.dimensions = "3D"; sp = cu.splines.new("POLY"); sp.points.add(len(r["pts"]) - 1)
        for i, (px, py) in enumerate(r["pts"]): x, y = mxy(px, py); sp.points[i].co = (x, y, 0.05, 1)
        cu.bevel_depth = 0.07 if r["n"] != "B2" else 0.1; cu.bevel_resolution = 4
        o = bpy.data.objects.new(r["n"], cu); sc.collection.objects.link(o)
        col = hx(r["c"]); col = tuple(v ** 2.2 for v in col); o.data.materials.append(plain("r" + r["n"], col, 0.3, e=col, s=0.9 if r["n"] != "B2" else 1.3))
    sx, sy = mxy(*PR["station"])
    cyl("st", 0.22, 0.12, (sx, sy, 0.08), (0, 0, 0), plain("stw", (0.95, 0.95, 0.97), 0.3), 48)
    cyl("st2", 0.14, 0.14, (sx, sy, 0.1), (0, 0, 0), plain("stn", (0.04, 0.12, 0.23), 0.3), 48)
    Y0, Y1, L0, L1, BOT = -MH / 2, MH / 2, -MW / 2, MW / 2, -0.01
    cam_loc, cam_tgt, lens = (sx + 3.5, sy - 13.0, 9.5), (sx + 0.6, sy - 0.4, 0.0), 32
    PATROL_ST = (sx, sy, 0.1)
else:  # twin: 지도 상판 + 지하 블록(층·관로·공동 신호)
    YA, YB, DB = -3.6, 3.6, -3.4
    box("asph", L0, L1, YA, YB, -0.2, 0.0, ASPH); box("base", L0, L1, YA, YB, -0.5, -0.2, BASE)
    fill = box("fill", L0, L1, YA, YB, -2.3, -0.5, FILL); sand = box("sand", L0, L1, YA, YB, DB, -2.3, SAND)
    WP = plain("wp", (0.12, 0.3, 0.62), 0.35, 0.3); GP = plain("gp", (0.85, 0.62, 0.08), 0.4, 0.2); TP = plain("tp", (0.85, 0.35, 0.08), 0.45)
    for i, (x, z, r, m) in enumerate([(-3.2, -1.5, 0.45, CONC), (-1.4, -1.1, 0.2, WP), (2.4, -0.9, 0.14, GP), (3.4, -0.85, 0.09, TP), (3.75, -0.85, 0.09, TP)]):
        p_ = cyl("p%d" % i, r, YB - YA, (x, 0, z), (math.pi / 2, 0, 0), m)
        if r > 0.3:
            h_ = cyl("ph", r - 0.07, YB - YA + 0.2, (x, 0, z), (math.pi / 2, 0, 0), CONC_IN); cut(p_, h_, CONC_IN); bpy.data.objects.remove(h_)
        for t in (fill,): cut(t, cyl("pc%d" % i, r, YB - YA + 0.2, (x, 0, z), (math.pi / 2, 0, 0), m))
    for o in list(bpy.data.objects):
        if o.name.startswith("pc"): bpy.data.objects.remove(o)
    cav = blob("cav", (0.6, YA + 0.5, -1.25), (1.0, 1.2, 0.5)); cut(fill, cav, VOID); bpy.data.objects.remove(cav)
    glow = blob("glow", (0.6, YA + 0.6, -1.25), (0.62, 0.7, 0.3)); glow.data.materials.append(plain("amb2", (0.9, 0.35, 0.02), 0.4, e=(1.0, 0.38, 0.02), s=0.45))
    # 지도 상판(띄움): 남색 계열로 반전해 디지털 지도 느낌
    bpy.ops.mesh.primitive_plane_add(size=1, location=(0, 0, 2.2)); mp = bpy.context.active_object
    mp.scale = (L1 - L0, YB - YA, 1); bpy.ops.object.transform_apply(scale=True)
    sl = mp.modifiers.new("s", "SOLIDIFY"); sl.thickness = 0.05
    M = bpy.data.materials.new("map"); nt, b = nodes(M); it = nt.nodes.new("ShaderNodeTexImage"); it.image = bpy.data.images.load(MAP)
    tcm = nt.nodes.new("ShaderNodeTexCoord"); mpp = nt.nodes.new("ShaderNodeMapping"); mpp.inputs["Scale"].default_value = (0.55, 0.55, 1); mpp.inputs["Location"].default_value = (0.12, 0.3, 0)
    nt.links.new(tcm.outputs["UV"], mpp.inputs["Vector"]); nt.links.new(mpp.outputs["Vector"], it.inputs["Vector"])
    bw = nt.nodes.new("ShaderNodeRGBToBW"); nt.links.new(it.outputs["Color"], bw.inputs["Color"])
    rp = ramp(nt, [(0.55, (0.32, 0.55, 0.85)), (0.8, (0.05, 0.1, 0.2)), (0.95, (0.025, 0.05, 0.1))]); nt.links.new(bw.outputs["Val"], rp.inputs["Fac"])
    nt.links.new(rp.outputs["Color"], b.inputs["Base Color"]); b.inputs["Roughness"].default_value = 0.35
    em = nt.nodes.new("ShaderNodeMath"); em.operation = "LESS_THAN"; em.inputs[1].default_value = 0.62; nt.links.new(bw.outputs["Val"], em.inputs[0])
    nt.links.new(rp.outputs["Color"], b.inputs["Emission Color"]); nt.links.new(em.outputs[0], b.inputs["Emission Strength"])
    mp.data.materials.append(M)
    cyl("beam", 0.014, 3.2, (0.6, YA + 0.6, 0.6), (0, 0, 0), plain("amb3", (1, 0.6, 0.1), 0.4, e=(1.0, 0.55, 0.08), s=6), 16)
    for r_, a_ in ((0.09, 1.0), (0.22, 0.35), (0.36, 0.15)):
        bpy.ops.mesh.primitive_torus_add(major_radius=r_, minor_radius=0.012, location=(0.6, YA + 0.6, 2.23)); bpy.context.active_object.data.materials.append(plain("ring", (1, 0.6, 0.1), 0.4, e=(1.0, 0.55, 0.08), s=8 * a_))
    Y0, Y1 = YA, YB
    cam_loc, cam_tgt, lens = (10.5, -19.5, 8.6), (0.0, 0.0, -0.85), 38
    BOT = DB

# 그림자 받는 바닥 + 조명
bpy.ops.mesh.primitive_plane_add(size=80, location=(0, 0, BOT - 0.001)); g = bpy.context.active_object
g.is_shadow_catcher = True
sun = bpy.data.lights.new("sun", "SUN"); sun.energy = 1.6; sun.angle = math.radians(6); so = bpy.data.objects.new("sun", sun); sc.collection.objects.link(so)
so.rotation_euler = (math.radians(42), math.radians(-18), math.radians(28))
key = bpy.data.lights.new("key", "AREA"); key.energy = 900; key.size = 8; ko = bpy.data.objects.new("key", key); sc.collection.objects.link(ko)
ko.location = (2, -12, 4); ko.rotation_euler = (Vector((0, 0, -2)) - Vector(ko.location)).to_track_quat("-Z", "Y").to_euler()
if VIEW == "twin":
    pl = bpy.data.lights.new("glow", "POINT"); pl.energy = 120; pl.color = (1, 0.6, 0.15); po = bpy.data.objects.new("glow", pl); po.location = (0.6, -3.9, -1.25); sc.collection.objects.link(po)
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.8, 0.83, 0.88, 1); bg.inputs[1].default_value = 0.35
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam)
if VIEW == "patrol": bg.inputs[0].default_value = (0.01, 0.02, 0.04, 1); bg.inputs[1].default_value = 1.0; sun.energy = 0.3; key.energy = 150
if VIEW == "patrol": cam.dof.use_dof = True; cam.dof.focus_distance = (Vector(cam_loc) - Vector(PATROL_ST)).length; cam.dof.aperture_fstop = 2.2; sc.collection.objects.link(co); sc.camera = co
co.location = cam_loc; cam.lens = lens; co.rotation_euler = (Vector(cam_tgt) - Vector(cam_loc)).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"
try:
    p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices(); [setattr(d, "use", True) for d in p.devices]; sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = int(os.environ.get("SAMPLES", "256")); sc.cycles.use_denoising = True
sc.render.film_transparent = VIEW != "patrol"
sc.render.resolution_x, sc.render.resolution_y = {"mech": (3200, 1640), "twin": (3400, 1800), "freq": (2800, 1400), "road": (3200, 1440), "layers": (3200, 1760), "patrol": (3200, 1800)}[VIEW]
sc.render.resolution_percentage = int(os.environ.get("PCT", "100"))
sc.view_settings.view_transform = "AgX"; sc.view_settings.look = "AgX - Medium High Contrast"
if VIEW == "patrol": sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "Medium High Contrast"; sc.render.use_compositing = True
sc.render.image_settings.color_mode = "RGBA"
import json
from bpy_extras.object_utils import world_to_camera_view
bpy.context.view_layer.update()
def proj(p):
    v = world_to_camera_view(sc, co, Vector(p)); return [round(v.x, 4), round(1 - v.y, 4)]
A = {"mech": {"asph": (-4.2, Y0, -0.11), "base": (-4.2, Y0, -0.41), "fill": (-4.2, Y0, -1.6), "pipe": (1.3, Y0, -1.75), "cav": (0.2, Y0, -1.0),
              "gw_l": (L0, Y0, -3.4), "gw_r": (L1, Y0, -3.4), "gw_rb": (L1, Y1, -3.4), "tun": (-2.6, Y0, -4.25), "road": (2.0, 0.0, 0.0), "w1": (-0.95, Y0, -0.6), "w2": (1.75, Y0, -0.6), "wa": (-2.35, Y0, -3.1), "tl": (L0, Y0, 0.0), "br": (L1, Y1, BOT), "bl": (L0, Y0, BOT)},
     "freq": dict([(f"a{i}{s_}", (x + s_ * 0.5, Y0, 0.0)) for i, x in enumerate((-3.3, 0.0, 3.3)) for s_ in (-1, 1)] + [(f"b{i}{s_}", (x + s_ * w, Y0, -d)) for i, (x, w, d) in enumerate(((-3.3, 1.45, 4.3), (0.0, 0.95, 2.4), (3.3, 0.6, 0.85))) for s_ in (-1, 1)] + [("dl", (L0, Y0, -2.0)), ("dr", (L1, Y0, -2.0)), ("drb", (L1, Y1, -2.0))]),
     "road": dict([(f"s{k}{e}", (L0 if e == "l" else L1, -3.2 + k * 0.92 + o, 0.0)) for k in range(8) for e in ("l", "r") for o in (0,)] + [(f"t{k}{e}", (L0 if e == "l" else L1, -3.2 + k * 0.92 + 0.62, 0.0)) for k in range(8) for e in ("l", "r")] +
                   [("r00", (0.6, -2.4, 0)), ("r10", (4.6, -2.4, 0)), ("r11", (4.6, 1.6, 0)), ("r01", (0.6, 1.6, 0))] + [(f"v{k}{e}", (0.95 + k * 0.66, -2.25 if e == "a" else 1.45, 0)) for k in range(6) for e in ("a", "b")] + [(f"h{k}{e}", (0.75 if e == "a" else 4.45, -1.8 + k * 0.95, 0)) for k in range(4) for e in ("a", "b")] + [("dir", (-7.5, -3.6, 0))]),
     "layers": dict([(f"l{i}", (4.0, -2.5, (6 - i) * 0.95)) for i in range(7)] + [("beam", (-0.6, -0.15, 6 * 0.95 + 0.3))]),
     "patrol": {"st": PATROL_ST} if VIEW == "patrol" else {},
     "twin": {"map": (-4.6, -3.6, 2.2), "dot": (0.6, -3.0, 2.23), "glow": (0.6, -3.6, -1.25), "sewer": (-3.2, -3.6, -1.5), "water": (-1.4, -3.6, -1.1), "gas": (2.4, -3.6, -0.9), "tel": (3.55, -3.6, -0.85), "asph": (-4.6, -3.6, -0.1)}}[VIEW]
json.dump({k: proj(v) for k, v in A.items()}, open(OUT.rsplit(".", 1)[0] + ".json", "w"))
sc.render.filepath = OUT
if os.environ.get("JSON_ONLY"): sys.exit(0)
bpy.ops.render.render(write_still=True); print("RENDERED", OUT)
