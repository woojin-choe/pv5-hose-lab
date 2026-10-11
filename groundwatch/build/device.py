# 차량 디스플레이(12.9인치급 가로형) 제품 렌더: 화면에 앱 UI 이미지를 넣고 비스듬히 촬영 (Blender Cycles)
import bpy, math, sys, os
from mathutils import Vector
argv = sys.argv[sys.argv.index("--") + 1:]
OUT, UI = argv[0], argv[1]
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
img = bpy.data.images.load(UI); AR = img.size[0] / img.size[1]
W = 1.0; H = W / AR; T = 0.035; BZ = 0.018

def mat(n, c, r, m=0.0):
    M = bpy.data.materials.new(n); M.use_nodes = True; b = M.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*c, 1); b.inputs["Roughness"].default_value = r; b.inputs["Metallic"].default_value = m; return M, b

# 본체(모서리 둥근 슬래브)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0)); body = bpy.context.active_object
body.scale = (W + 2 * BZ, T, H + 2 * BZ); bpy.ops.object.transform_apply(scale=True)
bv = body.modifiers.new("b", "BEVEL"); bv.width = 0.014; bv.segments = 8
body.data.materials.append(mat("body", (0.02, 0.022, 0.026), 0.35, 0.4)[0]); bpy.ops.object.shade_smooth()
# 화면(UI 발광 + 유리 코트)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -T / 2 - 0.0008, 0), rotation=(math.pi / 2, 0, 0)); scr = bpy.context.active_object
scr.scale = (W, H, 1); bpy.ops.object.transform_apply(scale=True)
M, b = mat("screen", (0, 0, 0), 0.05)
nt = M.node_tree; it = nt.nodes.new("ShaderNodeTexImage"); it.image = img
nt.links.new(it.outputs["Color"], b.inputs["Base Color"]); nt.links.new(it.outputs["Color"], b.inputs["Emission Color"])
b.inputs["Emission Strength"].default_value = 0.8; b.inputs["Coat Weight"].default_value = 1.0; b.inputs["Coat Roughness"].default_value = 0.03
scr.data.materials.append(M)
# 받침(대시보드 위 거치 스탠드)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, T * 1.6, -H / 2 - 0.05)); st = bpy.context.active_object
st.scale = (0.16, 0.05, 0.12); bpy.ops.object.transform_apply(scale=True); st.modifiers.new("b", "BEVEL").width = 0.01
st.data.materials.append(mat("stand", (0.05, 0.05, 0.055), 0.4, 0.6)[0])
# 대시보드 상판(어두운 소프트 소재)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.25, -H / 2 - 0.13)); dash = bpy.context.active_object
dash.scale = (3.2, 0.9, 0.04); bpy.ops.object.transform_apply(scale=True)
dash.data.materials.append(mat("dash", (0.03, 0.032, 0.036), 0.7)[0])
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.21, -H / 2 - 0.11)); trim = bpy.context.active_object
trim.scale = (3.2, 0.012, 0.012); bpy.ops.object.transform_apply(scale=True); trim.data.materials.append(mat("trim", (0.6, 0.62, 0.66), 0.25, 1.0)[0])
# 조명: 차갑고 낮은 새벽광 + 위쪽 소프트박스 반사
world = bpy.data.worlds.new("w"); sc.world = world; world.use_nodes = True
bg = world.node_tree.nodes["Background"]; bg.inputs[0].default_value = (0.02, 0.035, 0.07, 1); bg.inputs[1].default_value = 1.0
for loc, e, sz, col in (((-1.6, -1.8, 1.4), 120, 2.5, (0.55, 0.7, 1.0)), ((1.8, -1.2, 0.6), 50, 1.2, (1.0, 0.8, 0.55)), ((0, 1.5, 1.2), 80, 2.0, (0.6, 0.75, 1.0))):
    L = bpy.data.lights.new("l", "AREA"); L.energy = e; L.size = sz; L.color = col; o = bpy.data.objects.new("l", L); o.location = loc
    o.rotation_euler = (Vector((0, 0, 0)) - Vector(loc)).to_track_quat("-Z", "Y").to_euler(); sc.collection.objects.link(o)
cam = bpy.data.cameras.new("c"); co = bpy.data.objects.new("c", cam); sc.collection.objects.link(co); sc.camera = co
co.location = (0.62, -2.05, 0.2); cam.lens = 52; cam.dof.use_dof = True; cam.dof.focus_distance = 2.1; cam.dof.aperture_fstop = 2.8
co.rotation_euler = (Vector((0.06, 0, -0.035)) - Vector(co.location)).to_track_quat("-Z", "Y").to_euler()
sc.render.engine = "CYCLES"
try:
    p = bpy.context.preferences.addons["cycles"].preferences; p.compute_device_type = "METAL"; p.get_devices(); [setattr(d, "use", True) for d in p.devices]; sc.cycles.device = "GPU"
except Exception: pass
sc.cycles.samples = int(os.environ.get("SAMPLES", "200")); sc.cycles.use_denoising = True
sc.render.resolution_x, sc.render.resolution_y = 3200, 1240
sc.render.resolution_percentage = int(os.environ.get("PCT", "100"))
sc.view_settings.view_transform = "Standard"; sc.view_settings.look = "None"
sc.render.filepath = OUT; bpy.ops.render.render(write_still=True); print("RENDERED", OUT)
