# 시뮬레이션 강화: 작은 성장과 오탐 요인(함수비 변화·재포장·주행선 오차)을 넣어 탐지/오탐을 비교한다.
import numpy as np, json, sys, os
sys.path.insert(0, os.path.dirname(__file__))
import fdtd_change as F

def bscan2(cavity_r, seed, shift_cells, moist=0.15, pave=0.0):
    rng = np.random.default_rng(seed)
    eps, sig = F.model(cavity_r, rng)
    if moist > 0.15:  # 회차 전체 함수비 증가(유전율 상승)
        eps[:, F.AIR + 12:] += (moist - 0.15) * 4
    if pave:          # 재포장: 포장층 유전율·두께 변화
        eps[:, F.AIR:F.AIR + 14] = 6.0 + pave
    xs = list(range(F.PML + 10 + shift_cells, F.NX - F.PML - 15, 4))
    tr = np.array([F.run_trace(eps, sig, x) for x in xs])
    tr += np.random.default_rng(seed + 100).normal(0, 2e-3 * np.abs(tr).max(), tr.shape)
    return tr

cases = {
 "base": dict(cavity_r=0.18, seed=1, shift_cells=0),
 "grow5": dict(cavity_r=0.23, seed=2, shift_cells=1),
 "grow10": dict(cavity_r=0.28, seed=4, shift_cells=1),
 "grow20": dict(cavity_r=0.38, seed=2, shift_cells=1),
 "ctl_noise": dict(cavity_r=0.18, seed=3, shift_cells=1),
 "ctl_moist": dict(cavity_r=0.18, seed=5, shift_cells=1, moist=0.6),
 "ctl_repave": dict(cavity_r=0.18, seed=6, shift_cells=1, pave=1.0),
 "ctl_offset8": dict(cavity_r=0.18, seed=7, shift_cells=4),
}
out = {}
for k, c in cases.items():
    out[k] = bscan2(**c); print(k, flush=True)
np.savez_compressed(sys.argv[1], dt=F.DT, dx=F.DX, **out)
