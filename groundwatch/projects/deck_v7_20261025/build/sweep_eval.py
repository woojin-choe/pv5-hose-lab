# 강화 시뮬레이션 평가: 같은 처리(배경 제거·위치 정합·차분)로 성장 3종과 오탐 요인 4종을 비교한다.
# 임계값은 '변화 없음' 대조군 4종의 최대 차분 에너지로 정한다(대조군을 모두 정상으로 판정하는 가장 낮은 선).
import numpy as np, sys, json

d = np.load(sys.argv[1]); dt = float(d["dt"])


def prep(b):
    b = b - np.median(b, axis=0, keepdims=True)
    t = np.arange(b.shape[1]) * dt
    b = b * ((1 + t / 5e-9) ** 1.6)[None, :]
    return b


base = prep(d["base"])
scale = np.abs(base).max()
base /= scale
win = slice(int(4e-9 / dt), int(14e-9 / dt))


def diff_energy(name):
    q = prep(d[name]) / scale
    n = min(len(base), len(q)); p, q = base[:n], q[:n]
    best, bs = -1, 0
    for s in range(-3, 4):
        a = p[max(0, s):n + min(0, s), win]; b = q[max(0, -s):n - max(0, s), win]
        c = np.sum(a * b) / np.sqrt(np.sum(a * a) * np.sum(b * b))
        if c > best: best, bs = c, s
    q = np.roll(q, -bs, axis=0)
    D = q - p
    # 공동 주변 창(x 3~5m, 0.5~2m 깊이 해당 시간)만 본다: 위치가 알려진 회차 비교
    return float(np.sum(D[:, int(6e-9 / dt):int(30e-9 / dt)] ** 2)), int(bs)


res = {k: diff_energy(k) for k in ["grow5", "grow10", "grow20", "ctl_noise", "ctl_moist", "ctl_repave", "ctl_offset8"]}
ctl = max(v[0] for k, v in res.items() if k.startswith("ctl"))
out = {k: {"energy": round(v[0], 3), "ratio_to_worst_control": round(v[0] / ctl, 2), "shift": v[1]} for k, v in res.items()}
json.dump(out, open(sys.argv[2], "w"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, v)
