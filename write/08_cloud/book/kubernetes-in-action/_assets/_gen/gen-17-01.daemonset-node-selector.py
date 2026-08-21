# 17-01 §3 — 좁히는 일도 노드 쪽에서 한다
# replicas 로 개수를 줄이는 것이 아니라 대상 노드를 고르는 것이 요점이다. 그러니 라벨 유무로
# 노드가 갈리는 장면이어야 하고, 제외된 노드에 파드가 없다는 사실이 함께 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 17-01",
      "라벨이 대상 노드를 정한다",
      "nodeSelector 를 적으면 그 라벨을 가진 노드에만 파드가 놓인다. 개수를 줄이는 것이 아니라 "
      "대상 집합을 좁히는 일이다.",
      "nodeSelector: gpu=cuda")

NODES = [("노드 A", "gpu=cuda", True), ("노드 B", "gpu=cuda", True), ("노드 C", "라벨 없음", False)]
for i, (nm, lab, on) in enumerate(NODES):
    x0 = 90 + i * 350
    c = OK if on else SOFT
    d.box(x0, 200, 300, 220, PAPER, RULE, 0.9, 8)
    d.t(x0 + 150, 228, nm, 11, SOFT, KR)
    d.t(x0 + 150, 254, lab, 11, c, MONO)
    if on:
        ddx.node(d, x0 + 150, 330, "데몬 파드", "여기 놓인다", 240, 62, OK)
    else:
        d.t(x0 + 150, 330, "파드가 놓이지 않는다", 11, SOFT, KR)
        d.t(x0 + 150, 356, "selector 에 안 맞는다", 10, SOFT, KR)

ddx.focal_tag(d, 600, 466, "라벨을 붙이면 그 노드에도 곧 뜬다", 340)

d.t(24, 520, "노드에 라벨을 새로 붙이면 컨트롤러가 그것을 감지해 파드를 만든다. 라벨을 떼면 그 노드의 파드를 지운다. "
             "노드 집합의 변화가 곧 파드 집합의 변화다.", 11, MUTED, KR, "start")
d.t(24, 542, "반대로 파드 수를 직접 조절하는 길은 없다 — replicas 필드가 없으니 kubectl scale 도 쓰지 못한다.",
     11, MUTED, KR, "start")
d.legend(568, [("대상 노드", OK), ("라벨이 바꾸는 것", ACC)])
d.save("17-01-daemonset-node-selector.svg")
print("ok")
