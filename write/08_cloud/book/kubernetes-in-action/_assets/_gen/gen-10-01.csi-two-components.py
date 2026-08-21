# 10-01 §3 — 만드는 쪽과 붙이는 쪽이 다른 자리에 있다
# CSI 드라이버를 한 상자로 그리면 "왜 둘인가"가 안 보인다. 클러스터 어디서 도는지가 다르고
# 그래서 하는 일이 갈린다는 것이 요점이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 676, "KUBERNETES IN ACTION · 10-01",
      "만드는 일과 붙이는 일은 자리가 다르다",
      "볼륨을 만들고 지우는 일은 클러스터 어디서 한 번만 하면 된다. 그것을 노드에 붙여 마운트하는 일은 "
      "그 볼륨이 필요한 노드에서 해야 한다.",
      "CSI — 스토리지 벤더가 구현하는 표준 인터페이스")

ddx.band(d, 100, 336, "컨트롤러 — 클러스터에 하나(Deployment)", x=24, w=1172)
ddx.node(d, 220, 240, "CSI 컨트롤러", "어느 노드에 있어도 된다", 280, 88, ACC)
for i, (t, s) in enumerate((("CreateVolume", "스토리지에 볼륨을 만든다"),
                            ("DeleteVolume", "지운다"),
                            ("ControllerPublish", "노드에 attach 한다"))):
    d.box(560, 190 + i * 52, 560, 44, PAPER2, RULE, 1.0, 5)
    d.t(584, 218 + i * 52, t, 11, INK, MONO, "start", 600)
    d.t(800, 218 + i * 52, s, 10, MUTED, KR, "start")

ddx.band(d, 360, 596, "노드 에이전트 — 노드마다 하나(DaemonSet)", x=24, w=1172)
ddx.node(d, 220, 500, "CSI 노드 플러그인", "그 볼륨이 필요한 노드에서", 280, 88, OK)
for i, (t, s) in enumerate((("NodeStageVolume", "노드에 포맷·마운트"),
                            ("NodePublishVolume", "컨테이너 경로에 붙인다"),
                            ("NodeGetInfo", "이 노드의 위상을 알린다"))):
    d.box(560, 450 + i * 52, 560, 44, PAPER2, RULE, 1.0, 5)
    d.t(584, 478 + i * 52, t, 11, INK, MONO, "start", 600)
    d.t(800, 478 + i * 52, s, 10, MUTED, KR, "start")

d.t(24, 632 - 8, "그래서 컨트롤러는 Deployment 로 하나만 띄우고, 노드 플러그인은 DaemonSet 으로 노드마다 띄운다. "
                 "17 장의 '노드마다 하나'가 여기서 쓰인다.", 11, MUTED, KR, "start")
d.legend(628, [("한 번만 하면 되는 일", ACC), ("그 노드에서 해야 하는 일", OK)])
d.save("10-01-csi-two-components.svg")
print("ok")
