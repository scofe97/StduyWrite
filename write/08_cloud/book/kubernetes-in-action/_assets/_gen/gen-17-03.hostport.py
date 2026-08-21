# 17-03 §1 — 각 노드가 자기 것으로만 보낸다
# NodePort 와 헷갈리기 쉬운 자리라, 캡션도 "NodePort Service 처럼 무작위 파드로 가지 않는다"로
# 대비를 건다. 그러니 노드 둘을 그려 각자 자기 것으로만 가는 것이 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 600, "KUBERNETES IN ACTION · 17-03",
      "각 노드가 자기 위의 파드로만 보낸다",
      "hostPort 는 그 노드에 온 트래픽을 그 노드의 컨테이너로 포워딩한다. 규칙을 만든 주체가 "
      "그 노드의 CNI 라, 다른 노드로 넘길 길 자체가 없다.",
      "NodePort Service 와 겉모습은 비슷하지만 목적지가 다르다")

for i, nm in enumerate(("노드 A", "노드 B")):
    x0 = 90 + i * 540
    d.box(x0, 200, 460, 220, PAPER, RULE, 0.9, 8)
    d.t(x0 + 230, 228, nm, 11, SOFT, KR)
    ddx.node(d, x0 + 130, 300, f"{nm} IP:9090", "hostPort", 200, 62, INFO)
    ddx.node(d, x0 + 340, 300, "로컬 에이전트", "이 노드의 것", 190, 62, OK)
    d.path(f"M {x0+232} 300 L {x0+242} 300", OK, 1.5, m="ok")
    d.t(x0 + 230, 380, "노드 밖으로 나가지 않는다", 11, OK, KR)

ddx.focal_tag(d, 600, 466, "규칙을 만든 주체가 그 노드의 CNI 다", 380)

d.t(24, 520, "그래서 NodePort 처럼 무작위 파드로 가지 않는다. 노드 IP 를 알아야 부를 수 있다는 점이 "
             "대가이고, 그 노드 IP 는 Downward API 로 받는다.", 11, MUTED, KR, "start")
d.legend(548, [("들어오는 자리", INFO), ("로컬 목적지", OK), ("규칙의 주인", ACC)])
d.save("17-03-hostport.svg")
print("ok")
