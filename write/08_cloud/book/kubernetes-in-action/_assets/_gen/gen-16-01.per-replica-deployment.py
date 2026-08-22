# 16-01 §1 — 되기는 되는데 운영이 daunting 하다
# 본문이 "가능은 하지만"이라고 열어 두고 복잡도로 닫는다. 그러니 불가능을 그리면 안 되고,
# replica 하나 늘릴 때 무엇이 몇 개 늘어나는지가 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 660, "KUBERNETES IN ACTION · 16-01",
      "replica 마다 오브젝트 세 벌을 손으로 만든다",
      "각 파드가 자기 볼륨과 자기 주소를 가지고, 교체돼도 같은 것을 되받아야 한다. "
      "단일 Deployment·Service 로는 이 셋을 줄 수 없다.",
      "MongoDB 리플리카 셋 세 멤버를 Deployment 로 세우려면")

ddx.band(d, 100, 464, "Deployment 로 하면 — replica 마다 세 벌", x=24, w=760)
for i in range(3):
    x0 = 60 + i * 240
    d.box(x0, 156, 200, 268, PAPER, RULE, 0.9, 8)
    d.t(x0 + 100, 182, f"멤버 {i}", 11, SOFT, KR)
    for j, (nm, c) in enumerate((("Deployment", INFO), ("Service", INFO), ("PVC", INFO))):
        ddx.node(d, x0 + 100, 226 + j * 62, nm, f"quiz-{i}", 168, 50, c)
d.t(404, 444, "오브젝트 9 개 — 멤버 셋에", 11, MUTED, KR)

ddx.band(d, 100, 464, "StatefulSet 으로 하면", x=808, w=388)
ddx.node(d, 1002, 200, "headless Service", "quiz-pods", 320, 62, OK)
ddx.node(d, 1002, 286, "StatefulSet", "replicas: 3", 320, 62, OK)
d.t(1002, 344, "PVC 는 volumeClaimTemplates 가", 11, MUTED, KR)
d.t(1002, 364, "번호마다 알아서 만든다", 11, MUTED, KR)
d.t(1002, 404, "오브젝트 2 개", 11, OK, KR)

ddx.focal_tag(d, 610, 500, "replica 를 늘리려면 kubectl scale 도 못 쓴다", 400)
d.t(610, 534, "왼쪽에서는 오브젝트 3 종을 더 만들어야 한다", 11, ACC, KR)

d.t(24, 588, "보장해야 할 것은 셋이다 — 각 파드가 자기 PersistentVolume 을 가지고, 자기 고유 주소로 접근되며, "
             "교체되면 새 파드가 같은 주소와 볼륨을 되받는 것.", 11, MUTED, KR, "start")
d.legend(610, [("손으로 만드는 것", INFO), ("맡기는 것", OK), ("운영 비용", ACC)])
d.save("16-01-per-replica-deployment.svg")
print("ok")
