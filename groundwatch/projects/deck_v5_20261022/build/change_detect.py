# GroundWatch 변화 감지: ① 직접파·배경 제거 ② 회차 간 위치 정합(교차상관) ③ 차분 ④ 잡음 대비 임계값.
# 입력은 fdtd_change.py가 만든 두 회차 B-scan. 결과 그림과 수치를 저장한다.
import numpy as np, sys, json
from PIL import Image, ImageDraw, ImageFont

src, outdir, fonts = sys.argv[1:4]
d = np.load(src)
prev, cur, dt, dx = d["prev"], d["cur"], float(d["dt"]), float(d["dx"])
xp, xc = d["xp"], d["xc"]


def prep(b):
    b = b - np.median(b, axis=0, keepdims=True)          # 배경(직접파·수평 반사) 제거
    t = np.arange(b.shape[1]) * dt
    g = (1 + (t / 5e-9)) ** 1.6                          # 시간 증폭(깊이 보정)
    b = b * g[None, :]
    return b / np.abs(b).max()


P, Q, K = prep(prev), prep(cur), prep(d["ctrl"])
n = min(len(P), len(Q), len(K))
P, Q, K = P[:n], Q[:n], K[:n]

# ② 위치 정합: 트레이스 축으로 ±3 트레이스 이동시켜 공통 구간(관 아래 깊은 반사 제외한 얕은층) 상관 최대
win = slice(int(4e-9 / dt), int(14e-9 / dt))
best, bs = -1, 0
for s in range(-3, 4):
    a = P[max(0, s):n + min(0, s), win]; b = Q[max(0, -s):n - max(0, s), win]
    c = np.sum(a * b) / np.sqrt(np.sum(a * a) * np.sum(b * b))
    if c > best: best, bs = c, s
Qa = np.roll(Q, -bs, axis=0)

# ③ 차분, ④ 임계값(차분 하위 90% 분포의 5σ)
D = Qa - P
env = np.abs(D)
thr = np.percentile(env, 90) + 5 * env[env < np.percentile(env, 90)].std()
mask = env > thr
ix, it = np.where(mask)
eps_soil = 9.0
v = 299792458.0 / np.sqrt(eps_soil)
res = {"align_shift_traces": int(bs), "align_corr": round(float(best), 3), "flag_cells": int(mask.sum())}
if len(ix):
    trace_step = float(np.median(np.diff(xp))) * dx
    res["x_center_m"] = round(float(xp[0] * dx + ix.mean() * trace_step), 2)
    res["depth_top_m"] = round(float((it.min() * dt) * v / 2), 2)
    res["width_m"] = round(float((ix.max() - ix.min() + 1) * trace_step), 2)
# 핵심 영역: 차분 에너지 상위(최대의 50%) 셀로 위치·깊이 산출
core = env > 0.5 * env.max()
cx, ct = np.where(core)
trace_step = float(np.median(np.diff(xp))) * dx
res["x_center_m"] = round(float(xp[0] * dx + cx.mean() * trace_step), 2)
res["depth_top_m"] = round(float(ct.min() * dt * v / 2), 2)
res["true_x_m"], res["true_top_prev_m"], res["true_top_cur_m"] = 4.0, 1.18, 0.88
# 대조군: 공동은 그대로, 함수비·잡음만 다른 회차와 비교했을 때 같은 임계값을 넘는 셀 수
Dk = np.abs(K - P)
res["flag_cells_change"] = int(mask.sum())
res["flag_cells_control"] = int((Dk > thr).sum())
res["energy_ratio_change_vs_control"] = round(float(np.sum(env ** 2) / np.sum(Dk ** 2)), 1)
json.dump(res, open(f"{outdir}/result.json", "w"), ensure_ascii=False, indent=1)
print(res)


def img(b, w, h, clip=0.25):
    a = np.clip(b.T / clip, -1, 1)
    g = ((a + 1) * 127.5).astype(np.uint8)
    return Image.fromarray(g).resize((w, h), Image.BICUBIC).convert("RGB")


W, H = 900, 420
top = int(H * 0)
ims = [img(P, W, H), img(Qa, W, H)]
dif = np.clip(env.T / (thr * 3), 0, 1)
dimg = Image.fromarray((dif * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
heat = Image.merge("RGB", [dimg, dimg.point(lambda v: int(v * 0.72)), dimg.point(lambda v: 0)])
base = img(Qa, W, H, 0.4).point(lambda v: int(v * 0.35))
heat = Image.composite(heat, base, dimg.point(lambda v: 255 if v > 30 else 0))
d2 = ImageDraw.Draw(heat)
if len(cx):
    x0 = cx.min() / n * W; x1 = (cx.max() + 1) / n * W
    y0 = ct.min() / P.shape[1] * H; y1 = (ct.max() + 1) / P.shape[1] * H
    d2.rectangle((x0 - 8, y0 - 8, x1 + 8, y1 + 8), outline=(245, 183, 0), width=4)
ctl = np.clip(Dk.T / (thr * 3), 0, 1)
cimg = Image.fromarray((ctl * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)
cheat = Image.composite(Image.merge("RGB", [cimg, cimg.point(lambda v: int(v * 0.72)), cimg.point(lambda v: 0)]), img(K, W, H, 0.4).point(lambda v: int(v * 0.35)), cimg.point(lambda v: 255 if v > 30 else 0))
for name, im in [("sim_prev.png", ims[0]), ("sim_cur.png", ims[1]), ("sim_diff.png", heat), ("sim_ctrl.png", cheat)]:
    im.save(f"{outdir}/{name}")
