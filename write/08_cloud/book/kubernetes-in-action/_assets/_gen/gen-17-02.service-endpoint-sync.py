# 17-02 §3 — 목록을 받고 규칙을 심는 왕복
# 캡션이 "목록과 변경 이벤트를 받아 커널 규칙을 동기화하는 왕복"이라 한다. 그러니 한 방향
# 화살표가 아니라 초기 목록과 이후 이벤트가 갈라져 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 17-02",
      "한 번 받아 두고, 그 뒤로는 변경만 받는다",
      "kube-proxy 는 시작할 때 EndpointSlice 목록을 통째로 받아 규칙을 심고, 그 뒤로는 변경 이벤트만 "
      "받아 해당 부분을 고친다. 매번 전체를 다시 세지 않는다.",
      "11-03 의 조각 단위 전송이 여기서 값한다")

ddx.node(d, 200, 300, "API 서버", "EndpointSlice 를 담는다", 260, 88, INFO)
ddx.node(d, 640, 300, "kube-proxy", "노드마다 하나(DaemonSet)", 260, 88, ACC)
ddx.node(d, 1040, 300, "커널 규칙", "iptables · IPVS · nftables", 240, 88, OK)

d.path("M 332 268 L 508 268", INFO, 1.5, m="info")
d.t(420, 250, "① 처음 — 목록 전체", 11, INFO, KR)
d.path("M 332 332 L 508 332", ACC, 1.5, m="acc", dash="6 5")
d.t(420, 356, "② 그 뒤 — 변경 이벤트만", 11, ACC, KR)
d.path("M 772 300 L 918 300", OK, 1.5, m="ok")
d.t(845, 280, "심고 고친다", 11, OK, KR)

d.t(610, 434, "그래서 파드 하나가 죽고 사는 사건이 규칙 한 줄만 건드린다", 11, SOFT, KR)

d.t(24, 496, "kube-proxy 도 DaemonSet 으로 도는 노드 에이전트다 — 노드마다 자기 커널 규칙을 손봐야 하기 때문이다. "
             "이 편이 다루는 격리 개방이 그 일을 가능하게 한다.", 11, MUTED, KR, "start")
d.t(24, 518, "11-03 에서 EndpointSlice 가 조각으로 나뉜 이유가 여기서 값한다 — 변경 하나가 실어 나르는 양이 조각 하나로 좁혀진다.",
     11, MUTED, KR, "start")
d.legend(548, [("목록의 출처", INFO), ("받아서 옮기는 자", ACC), ("실제 규칙", OK)])
d.save("17-02-service-endpoint-sync.svg")
print("ok")
