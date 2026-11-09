# 10-01 §3 — 만드는 쪽과 붙이는 쪽이 다른 자리에 있다
# CSI 드라이버를 한 상자로 그리면 "왜 둘인가"가 안 보인다. 클러스터 어디서 도는지가 다르고
# 그래서 하는 일이 갈린다는 것이 요점이다.
# 타입 스펙: type-deployment.md — 밴드 둘이 "클러스터에 하나(Deployment)" 와 "노드마다 하나(DaemonSet)" 라는 배치 자체를
#           말한다 — 정본이 요구하는 존과 복제 수가 여기 있다. 하는 일이 갈리는 이유가 도는 자리이므로
#           배치가 곧 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(920, 670, "KUBERNETES IN ACTION · 10-01",
      "만드는 일과 붙이는 일은 자리가 다르다",
      "볼륨 생성은 컨트롤 플레인에서 한 번 수행하고, 노드 attach(ControllerPublishVolume)는 볼륨을 쓸 노드마다 컨트롤 플레인이 호출한다. "
      "노드 포맷과 컨테이너 마운트(NodeStage/NodePublishVolume)는 볼륨을 쓰는 노드에서 수행한다.",
      "CSI — 스토리지 벤더가 구현하는 표준 인터페이스")

ddx.band(d, 96, 326, "컨트롤러 — 클러스터에 하나(Deployment)", x=20, w=880)
ddx.node(d, 160, 210, "CSI 컨트롤러", "어느 노드에 있어도 된다", 240, 88, ACC)
for i, (t, s) in enumerate((("CreateVolume", "스토리지에 볼륨을 만든다"),
                            ("DeleteVolume", "볼륨을 지운다"),
                            ("ControllerPublish", "노드에 attach 한다"))):
    d.box(310, 154 + i * 52, 570, 44, PAPER2, RULE, 1.0, 5)
    d.t(330, 182 + i * 52, t, 13, INK, MONO, "start", 600)
    d.t(540, 182 + i * 52, s, 12, MUTED, KR, "start")

ddx.band(d, 344, 574, "노드 에이전트 — 노드마다 하나(DaemonSet)", x=20, w=880)
ddx.node(d, 160, 458, "CSI 노드 플러그인", "그 볼륨이 필요한 노드에서", 240, 88, OK)
for i, (t, s) in enumerate((("NodeStageVolume", "노드에 포맷·마운트"),
                            ("NodePublishVolume", "컨테이너 경로에 마운트"),
                            ("NodeGetInfo", "이 노드의 위상을 알린다"))):
    d.box(310, 402 + i * 52, 570, 44, PAPER2, RULE, 1.0, 5)
    d.t(330, 430 + i * 52, t, 13, INK, MONO, "start", 600)
    d.t(540, 430 + i * 52, s, 12, MUTED, KR, "start")

d.t(24, 596, "컨트롤러는 Deployment 로 하나 · 노드 플러그인은 DaemonSet 으로 노드마다 하나 (17 장 '노드마다 하나')", 12, MUTED, KR, "start")
d.legend(618, [("컨트롤 플레인에서 하는 일", ACC), ("그 볼륨을 쓰는 노드에서 하는 일", OK)])
d.save("10-01-csi-two-components.svg")
print("ok")
