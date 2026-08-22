# 17-01 §1 — 세 가지를 감시해 하나를 보장한다
# 14-02 의 reconciliation 고리와 같은 골격이되 감시 대상에 노드가 들어간다는 점이 다르다.
# 그 차이가 "노드가 늘면 파드가 따라 는다"의 기전이므로 노드를 따로 세워 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 17-01",
      "노드까지 감시하기 때문에 따라 늘어난다",
      "ReplicaSet 컨트롤러는 ReplicaSet 과 Pod 를 본다. DaemonSet 컨트롤러는 거기에 Node 를 더 본다 — "
      "그래서 노드 목록이 바뀌면 그 변화가 곧 파드 변화가 된다.",
      "보장하는 것: 대상 노드마다 파드 하나")

WATCH = [("DaemonSet", "template · nodeSelector", 200),
         ("Pod", "지금 몇 개가 어디에", 300),
         ("Node", "노드가 늘었나 줄었나", 400)]
for t, s, cy in WATCH:
    ddx.node(d, 190, cy, t, s, 280, 76, INFO)
    d.path(f"M 332 {cy} L 424 {cy}", INFO, 1.3)
# 셋을 줄기(x=424)로 모아 비교 상자에는 한 번만 들어간다 — 비스듬한 수렴을 없앤다.
d.path("M 424 200 L 424 400", INFO, 1.3)
d.path("M 424 300 L 476 300", INFO, 1.3, m="info")

ddx.node(d, 610, 300, "비교한다", "대상 노드 : 파드", 260, 88, ACC)
d.path("M 742 300 L 830 300", ACC, 1.5, m="acc")
d.box(870, 232, 270, 136, PAPER, RULE, 0.9, 8)
d.t(1005, 258, "다르면", 11, SOFT, KR)
ddx.node(d, 1005, 300, "없는 노드에 만든다", "", 230, 44, OK)
ddx.node(d, 1005, 348, "빠진 노드 것을 지운다", "", 230, 44, OK)
d.path("M 1005 380 L 1005 470 L 190 470 L 190 442", INFO, 1.4, m="info", dash="6 5")
d.t(600, 440, "바뀐 결과를 다시 관찰한다", 10, SOFT, KR)

d.t(24, 500, "노드에 taint 가 있으면 그 노드는 대상에서 빠진다. 다만 DaemonSet 컨트롤러는 일부 taint 를 "
             "알아서 tolerate 해, 노드가 셋인데 파드가 둘인 상황이 그 때문에 생긴다.", 11, MUTED, KR, "start")
d.t(24, 522, "14-02 에서 본 level-triggered 성질은 여기서도 같다 — 무슨 일이 있었는지가 아니라 지금 노드 목록만 본다.",
     11, MUTED, KR, "start")
d.legend(548, [("감시 대상", INFO), ("비교하는 자리", ACC), ("조정", OK)])
d.save("17-01-daemonset-reconciliation.svg")
print("ok")
