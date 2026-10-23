# 2D FDTD(TM) GPR 시뮬레이션: 같은 도로를 두 회차 측정하고, 하수관 위 공동이 자랐을 때
# GroundWatch 변화 감지(위치 정합 → 회차 차분 → 임계값)가 그 변화를 잡는지 확인한다.
# 단위: m, s. 토양 εr=9, σ=5 mS/m, 공기 공동 εr=1, 콘크리트 하수관(εr=6) Ø0.8m.
import numpy as np, json, sys

C0, EPS0, MU0 = 299792458.0, 8.854e-12, 4e-7 * np.pi
DX = 0.02                      # 2cm 격자
NX, NZ = 360, 160              # 7.2m × 3.2m (위 0.2m는 공기)
AIR = 10                       # 공기층 셀 수
DT = 0.99 * DX / (C0 * np.sqrt(2))
F0 = 400e6                     # 400MHz 안테나
NT = int(60e-9 / DT)           # 60ns 기록
PML = 20


def model(cavity_r, rng):
    eps = np.full((NX, NZ), 9.0); sig = np.full((NX, NZ), 0.005)
    eps[:, :AIR] = 1.0; sig[:, :AIR] = 0.0
    # 포장층 0.25m
    eps[:, AIR:AIR + 12] = 6.0
    # 토양 불균질(두 회차 공통) + 회차별 함수비 미세 변화는 rng로
    base = np.random.default_rng(7).normal(0, 0.6, (NX, NZ))
    eps[:, AIR + 12:] += base[:, AIR + 12:] * 0.5 + rng.normal(0, 0.15, (NX, NZ))[:, AIR + 12:]
    x = np.arange(NX)[:, None] * DX; z = (np.arange(NZ)[None, :] - AIR) * DX
    pipe = (x - 4.0) ** 2 + (z - 1.9) ** 2 <= 0.4 ** 2
    eps[pipe] = 6.0
    if cavity_r > 0:            # 관 위로 자라는 공동(타원, 위쪽으로 성장)
        cav = ((x - 4.0) / (cavity_r * 1.6)) ** 2 + ((z - (1.45 - cavity_r * 0.5)) / cavity_r) ** 2 <= 1
        eps[cav & ~pipe] = 1.0; sig[cav & ~pipe] = 0.0
    return eps, sig


def run_trace(eps, sig, sx):
    ca = (1 - sig * DT / (2 * EPS0 * eps)) / (1 + sig * DT / (2 * EPS0 * eps))
    cb = (DT / (EPS0 * eps * DX)) / (1 + sig * DT / (2 * EPS0 * eps))
    # 간단한 흡수층: 가장자리 감쇠 계수
    damp = np.ones((NX, NZ))
    for i in range(PML):
        f = 1 - 0.02 * ((PML - i) / PML) ** 2
        damp[i, :] *= f; damp[-1 - i, :] *= f; damp[:, -1 - i] *= f; damp[:, i] *= f
    ez = np.zeros((NX, NZ)); hx = np.zeros((NX, NZ)); hy = np.zeros((NX, NZ))
    k = DT / (MU0 * DX)
    sz = AIR - 1; rx = sx + 5
    out = np.zeros(NT)
    t0 = 1.2 / F0
    for n in range(NT):
        hx[:, :-1] -= k * (ez[:, 1:] - ez[:, :-1])
        hy[:-1, :] += k * (ez[1:, :] - ez[:-1, :])
        ez[1:, 1:] = ca[1:, 1:] * ez[1:, 1:] + cb[1:, 1:] * ((hy[1:, 1:] - hy[:-1, 1:]) - (hx[1:, 1:] - hx[1:, :-1]))
        t = n * DT; a = (np.pi * F0 * (t - t0)) ** 2
        ez[sx, sz] += (1 - 2 * a) * np.exp(-a)
        ez *= damp
        out[n] = ez[rx, sz]
    return out


def bscan(cavity_r, seed, shift_cells):
    rng = np.random.default_rng(seed)
    eps, sig = model(cavity_r, rng)
    xs = list(range(PML + 10 + shift_cells, NX - PML - 15, 4))
    tr = np.array([run_trace(eps, sig, x) for x in xs])
    tr += np.random.default_rng(seed + 100).normal(0, 2e-3 * np.abs(tr).max(), tr.shape)
    return tr, xs


if __name__ == "__main__":
    out = sys.argv[1]
    prev, xp = bscan(0.18, 1, 0)        # 지난 회차: 공동 반경 18cm
    cur, xc = bscan(0.38, 2, 1)         # 이번 회차: 38cm, 주행선이 2cm 어긋남
    ctrl, _ = bscan(0.18, 3, 1)         # 대조군: 공동 변화 없음, 함수비·잡음·주행선만 다름
    np.savez_compressed(out, prev=prev, cur=cur, ctrl=ctrl, xp=np.array(xp), xc=np.array(xc), dt=DT, dx=DX)
    print("saved", prev.shape, cur.shape, NT, DT)
