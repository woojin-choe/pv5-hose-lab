# 실제 GPR B-scan처럼 보이는 단면 영상 합성: 반사계수 → 리커 웨이블릿 합성곱 → 잡음·이득·회색조
# prev(이전 회차)·cur(현재 회차) 두 장. 같은 관로 쌍곡선 + 현재 회차에만 커진 공동 반사
import os, numpy as np
from PIL import Image
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "images", "3d")
NX, NZ, DMAX = 1100, 520, 2.0           # 트레이스 수, 샘플 수, 최대 깊이(m)
dz = DMAX / NZ; xs = np.linspace(0, 11.0, NX)  # 수평 거리(m)

def ricker(f=0.09, n=61):  # 샘플 단위 주파수
    t = np.arange(n) - n // 2; a = (np.pi * f * t) ** 2; return (1 - 2 * a) * np.exp(-a)

def section(seed, cavity):
    rng = np.random.default_rng(seed); R = np.zeros((NZ, NX))
    def layer(depth, amp, wav=0.0, ph=0.0):
        z = ((depth + wav * np.sin(xs * 1.3 + ph) + 0.004 * rng.standard_normal(NX).cumsum() / 8) / dz).astype(int)
        for i in range(NX):
            if 0 <= z[i] < NZ: R[z[i], i] += amp * (1 + 0.15 * rng.standard_normal())
    layer(0.02, 1.6); layer(0.24, -0.55, 0.01); layer(0.58, 0.35, 0.03, 1.0); layer(1.45, 0.16, 0.035, 2.3)
    def hyper(x0, d0, amp, v=0.11, w=2.2):  # 점 반사체의 쌍곡선
        for i, x in enumerate(xs):
            dx = x - x0
            if abs(dx) > w: continue
            z = int(np.sqrt(d0 ** 2 + (dx * v * 4.5) ** 2) / dz)
            if z < NZ: R[z, i] += amp * np.exp(-(dx / (w * 0.6)) ** 2)
    hyper(2.4, 0.9, 1.2, w=2.0)                                    # 관로
    for _ in range(14): hyper(rng.uniform(0, 11), rng.uniform(0.35, 1.9), rng.uniform(0.05, 0.14), w=0.8)  # 자갈·잡산란
    if cavity:  # 공동: 강한 반사 + 극성 반전 + 하부 다중반사
        hyper(7.2, 0.95, 1.9 * cavity, w=1.8 + cavity)
        for k, a in ((0.09, -1.2), (0.18, 0.7), (0.27, -0.4)): hyper(7.2, 0.95 + k, a * cavity, w=1.4 + cavity)
    # 리커 합성곱(깊이 방향)
    w = ricker(); D = np.apply_along_axis(lambda c: np.convolve(c, w, mode="same"), 0, R)
    D += 0.035 * rng.standard_normal(D.shape)                          # 백색 잡음
    D += 0.012 * np.sin(np.arange(NZ) / 3.1)[:, None] * rng.uniform(0.5, 1, NX)[None, :]  # 링잉 잔류
    gain = np.exp(np.linspace(0, 1.6, NZ))[:, None]; D *= gain        # 깊이 이득
    D[: int(0.06 / dz)] *= 0.5
    D = np.tanh(D * 1.4)
    img = ((D * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8)
    return Image.fromarray(img).resize((1600, 760), Image.LANCZOS)

section(11, 0.45).save(os.path.join(OUT, "bscan_prev.png"))
section(11, 1.0).save(os.path.join(OUT, "bscan_cur.png"))
print("bscan done")
