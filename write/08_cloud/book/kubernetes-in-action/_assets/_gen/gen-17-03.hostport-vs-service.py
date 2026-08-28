# 17-03 §1 — 같은 노드 IP 인데 목적지가 갈린다
# 캡션이 "규칙을 만든 주체가 달라 목적지가 갈린다"로 원인을 지목한다. 그러니 경로 둘을
# 같은 입구에서 출발시키고, 갈리는 지점에 주체 이름을 붙여야 한다.
# 타입 스펙: type-flowchart.md — 같은 노드 IP 라는 입구 하나에서 어느 규칙에 걸리느냐로 목적지가 두 갈래로 갈린다.
#           마름모를 쓰지 않았지만 판정 하나가 두 결말을 만드는 구조라 flowchart 계약에 맞는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 620, "KUBERNETES IN ACTION · 17-03",
      "규칙을 만든 주체가 목적지를 정한다",
      "노드 A 의 같은 IP 로 들어와도 어느 규칙에 걸리느냐에 따라 목적지가 갈린다. 하나는 클러스터 "
      "전역에서 고르고, 하나는 이 노드의 컨테이너로 고정한다.",
      "kube-proxy 의 규칙과 CNI portmap 의 규칙")

ddx.node(d, 160, 320, "노드 A IP", "패킷이 들어온다", 220, 84, INFO)

d.path("M 272 296 L 326 296 L 326 220 L 380 220", INFO, 1.5, m="info")
ddx.node(d, 540, 220, "kube-proxy 의 규칙", "NodePort Service", 300, 76, INFO)
d.path("M 692 220 L 800 220", INFO, 1.4, m="info")
ddx.node(d, 990, 220, "클러스터 전역 엔드포인트", "어느 노드의 파드든", 340, 76, INFO)

d.path("M 272 344 L 326 344 L 326 420 L 380 420", ACC, 1.5, m="acc")
ddx.node(d, 540, 420, "CNI portmap 의 규칙", "hostPort", 300, 76, ACC)
d.path("M 692 420 L 800 420", ACC, 1.4, m="acc")
ddx.node(d, 990, 420, "노드 A 의 로컬 컨테이너", "이 노드로 고정", 340, 76, ACC)

d.t(620, 320, "같은 입구, 다른 규칙", 11, SOFT, KR)

d.t(24, 512, "그래서 hostPort 와 NodePort 는 겉으로 비슷해 보여도 쓰임이 다르다. 하나는 어느 파드든 "
             "괜찮을 때, 하나는 이 노드의 것이어야 할 때다.", 11, MUTED, KR, "start")
d.t(24, 534, "둘 다 노드 IP 로 들어오므로, 무엇이 걸릴지는 포트 번호와 심어 둔 규칙이 정한다.",
     11, MUTED, KR, "start")
d.legend(560, [("전역에서 고른다", INFO), ("이 노드로 고정", ACC)])
d.save("17-03-hostport-vs-service.svg")
print("ok")
