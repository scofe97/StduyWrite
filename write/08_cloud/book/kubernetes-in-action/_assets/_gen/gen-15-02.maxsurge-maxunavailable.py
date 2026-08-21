# 15-02 §4 — 두 값이 정하는 것은 상한과 하한이다
# 본문이 "값이 원하는 복제본 수에 상대적"이라고 못박는다. 그러니 단계별 개수만 나열하면
# 안 되고, 총합의 천장과 가용의 바닥이 선으로 그어져 있어야 그 상대성이 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 640, "KUBERNETES IN ACTION · 15-02",
      "천장과 바닥 사이에서만 움직인다",
      "maxSurge 는 원하는 수를 얼마나 넘어설 수 있는지를, maxUnavailable 은 얼마나 모자랄 수 있는지를 "
      "정한다. 두 값 모두 원하는 복제본 수에 상대적이다.",
      "replicas 3 · maxSurge 1 · maxUnavailable 1 → 총합 ≤ 4 · 가용 ≥ 2")

STEP = [("시작", 3, 0, 3, 3), ("새 +1 · 옛 −1", 2, 2, 4, 2),
        ("교체 진행", 1, 3, 4, 3), ("옛 −1", 0, 3, 3, 3)]
BW, GP = 220, 40
X0 = (1220 - (4 * BW + 3 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(4)]

d.line(60, 200, 1160, 200, WARN, 1.2, "6 5")
d.t(1150, 192, "총합 천장 4 = replicas + maxSurge", 10, WARN, KR, "end")
d.line(60, 396, 1160, 396, OK, 1.2, "6 5")
d.t(1150, 388, "가용 바닥 2 = replicas − maxUnavailable", 10, OK, KR, "end")

for cx, (t, old, new, total, avail) in zip(CX, STEP):
    d.t(cx, 168, t, 11, SOFT, KR)
    d.box(cx - BW // 2, 216, BW, 100, PAPER2, RULE, 1.0, 6)
    d.t(cx, 244, f"옛 0.5 × {old}", 11, MUTED, MONO)
    d.t(cx, 268, f"새 0.6 × {new}", 11, MUTED, MONO)
    ddx.tag(d, cx, 300, f"총합 {total}", WARN if total == 4 else SOFT, 130)
    ddx.tag(d, cx, 364, f"가용 {avail}", ACC if avail == 2 else OK, 130)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+6} 266 L {b-BW//2-10} 266", MUTED, 1.4, m="ar")

d.t(24, 460, "핵심은 값이 원하는 수에 상대적이라는 것이다 — replicas 3 · maxUnavailable 1 인데 현재 5 개면, "
             "가용해야 할 수는 2 개(=3−1)이지 4 개가 아니다.", 11, MUTED, KR, "start")
d.t(24, 482, "maxSurge 0 · maxUnavailable 1 이면 천장이 3 이라 옛 파드를 먼저 지워야 자리가 나고, "
             "maxSurge 1 · maxUnavailable 0 이면 바닥이 3 이라 새 파드를 먼저 띄워야 한다 — 순서가 강제된다.",
     11, MUTED, KR, "start")
d.legend(516, [("천장에 닿은 단계", WARN), ("가용 파드", OK), ("바닥에 닿은 단계", ACC)])
d.save("15-02-maxsurge-maxunavailable.svg")
print("ok")
