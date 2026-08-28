# 17-01 §1 — 무엇을 세느냐가 다르다
# 배치 결과만 그리면 우연처럼 보인다. 각자 무엇을 맞추려 하는지를 함께 적어야 "노드가 늘면
# 파드가 따라 는다"가 결과가 아니라 정의에서 나온 것임이 읽힌다.
# 타입 스펙: type-deployment.md — 두 밴드가 같은 노드 셋 위에 서로 다른 배치를 그린다. 노드 상자가 존, 그 안의 칩이 파드이고
#           칸마다 개수(2·1·0 대 1·1·1)가 적히므로 type-deployment 정본이 요구하는 replica 수와
#           배치 결정이 둘 다 있다. 격자로 읽을 값이 아니라 배치 그 자체가 값이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 676, "KUBERNETES IN ACTION · 17-01",
      "replica 를 세느냐 노드를 세느냐",
      "ReplicaSet 은 정해진 개수를 맞추므로 어느 노드에 몇 개가 가든 상관하지 않는다. "
      "DaemonSet 은 노드마다 하나를 맞추므로 노드가 늘면 파드가 따라 는다.",
      "노드 셋 · replicas 3")

def scene(y0, label, rule, pods, c, note):
    ddx.band(d, y0, y0 + 224, label, x=24, w=1172)
    d.t(160, y0 + 60, rule, 11, c, KR)
    for i, (nm, n) in enumerate(pods):
        x0 = 330 + i * 290
        d.box(x0, y0 + 60, 260, 136, PAPER, RULE, 0.9, 8)
        d.t(x0 + 130, y0 + 86, nm, 11, SOFT, KR)
        for j in range(n):
            ddx.tag(d, x0 + 130, y0 + 124 + j * 40, "파드", c, 180)
        if n == 0:
            d.t(x0 + 130, y0 + 130, "없다", 11, SOFT, KR)
    d.t(160, y0 + 168, note, 11, SOFT, KR)

scene(100, "ReplicaSet — 개수를 맞춘다", "합이 3 이면 된다",
      [("노드 A", 2), ("노드 B", 1), ("노드 C", 0)], INFO,
      "어디에 몇 개든 상관없다")
scene(348, "DaemonSet — 노드마다 하나", "노드 수가 곧 파드 수",
      [("노드 A", 1), ("노드 B", 1), ("노드 C", 1)], ACC,
      "노드가 늘면 따라 는다")

d.t(24, 604, "그래서 DaemonSet 에는 replicas 필드가 없다. 개수를 적을 자리가 아니라 어느 노드에 놓을지를 "
             "적는 자리(nodeSelector)가 있다.", 11, MUTED, KR, "start")
d.legend(628, [("개수를 맞춘다", INFO), ("노드를 맞춘다", ACC)])
d.save("17-01-daemonset-vs-replicaset.svg")
print("ok")
