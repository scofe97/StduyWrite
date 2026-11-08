# 04-01.pod-routing-table — Pod 의 테이블은 한 곳으로 올리고, 갈래는 노드가 고른다
# 본문 요구: "Pod 의 ip route 는 세 줄이고 다음 홉이 전부 게이트웨이다 / 노드의 테이블에는 게이트웨이·다른 노드·로컬 veth 가
#           함께 들어 있다 — 판단은 노드가 한다" (kind v1.37.0 + kindnet 실측 값, 2026-11-08)
# 타입 스펙: type-swimlane.md — 레인은 Pod 와 노드, 두 레인을 건너는 하나의 핸드오프(default via)가 요점이라
#           그 화살표에만 focal 을 건다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 520
d = D(W, H, "POD ROUTING TABLE · WHERE THE DECISION IS MADE",
      "Pod 의 테이블은 한 곳으로 올리고, 갈래는 노드가 고른다",
      "Pod 의 ip route 는 세 줄이고 다음 홉이 전부 게이트웨이 10.244.2.1 이다. 노드의 테이블에는 게이트웨이와 다른 노드와 로컬 veth 가 함께 들어 있어서 목적지별 판단은 노드가 한다.",
      lead="Pod 는 목적지를 가르지 않고 올려 보낸다 — 판단은 인터페이스를 여럿 가진 노드가 한다")

ddx.band(d, 104, 252, "Pod · bb (10.244.2.2)")
ddx.band(d, 264, 452, "노드 · ntk0401-worker")

POD = [("default via 10.244.2.1 dev eth0"),
       ("10.244.2.0/24 via 10.244.2.1 dev eth0 src 10.244.2.2"),
       ("10.244.2.1 dev eth0 scope link src 10.244.2.2")]
NODE = [("default via 192.168.148.1 dev eth0"),
        ("10.244.0.0/24 via 192.168.148.5 dev eth0"),
        ("10.244.1.0/24 via 192.168.148.6 dev eth0"),
        ("10.244.2.2 dev veth61175e6c scope host"),
        ("192.168.148.0/24 dev eth0 proto kernel scope link src 192.168.148.4")]


def table(x, y, w, title, rows):
    h = 40 + len(rows) * 20
    d.box(x, y, w, h, PAPER, RULE, 1.0, 6)
    d.t(x + 16, y + 24, title, 12, INK, KR, "start", 600)
    for i, r in enumerate(rows):
        d.t(x + 16, y + 48 + i * 20, ddx.fit(r, 11, w - 32, r), 11, MUTED, MONO, "start")
    return h


table(200, 124, 420, "Pod 안 ip route · 3줄", POD)
table(200, 292, 520, "노드 ip route · 5줄", NODE)

d.path("M 410 232 L 410 288", ACC, 1.6, m="acc")
d.t(424, 244, "목적지가 무엇이든 default 로 노드에 올린다", 11, ACC, KR, "start", 600)

d.t(652, 172, "다음 홉이 전부", 12, INK, KR, "start", 600)
d.t(652, 194, "게이트웨이 10.244.2.1", 12, MUTED, KR, "start")
d.t(652, 216, "Pod 안에서는 판단하지 않음", 12, MUTED, KR, "start")
d.t(748, 340, "다음 홉이 셋", 12, INK, KR, "start", 600)
d.t(748, 364, "게이트웨이", 12, MUTED, KR, "start")
d.t(748, 386, "다른 노드 .5 · .6", 12, MUTED, KR, "start")
d.t(748, 408, "로컬 veth", 12, MUTED, KR, "start")

d.legend(468, [("레인을 건너는 핸드오프", ACC)])
d.save("04-01.pod-routing-table.svg")
print("ok pod-routing-table")
