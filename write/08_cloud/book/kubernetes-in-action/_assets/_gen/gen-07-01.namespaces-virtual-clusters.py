# 07-01 §namespace 로 물리 클러스터를 가상 분할
# 본문·옛 도식: 팀마다 자기 namespace 에 오브젝트를 만들고, namespace 는 이름과 권한의
#   스코프가 된다. 스코프가 갈리므로 서로 다른 팀이 같은 이름의 오브젝트를 만들 수 있다.
#   Alice 는 자기 namespace 와 B팀 namespace 양쪽에서 일할 수 있다.
# 타입 스펙: type-nested.md — 물리 클러스터 하나 안에 경계 셋이 그어지는 구조가 곧 답이다.
#           사람이 어느 경계에 닿는가가 권한 스코프이므로 접근선을 함께 그린다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 632
d = D(W, H, "KUBERNETES IN ACTION · 07-01",
      "물리 클러스터는 하나인데 이름 공간은 여럿이다",
      "namespace 는 이름과 권한의 스코프다. 스코프가 갈리므로 서로 다른 팀이 같은 이름의 "
      "오브젝트를 만들 수 있고, 사람은 자기가 닿는 namespace 에서만 일한다.",
      lead="Alice 는 자기 namespace 와 B팀 namespace 양쪽에 닿는다 — 권한이 곧 스코프다")

OUTER = (48, 200, 904, 216)
NS = [(200, 308), (500, 308), (800, 308)]
NW, NH = 240, 150
ACTORS = [(200, 500), (500, 500), (800, 500)]

ddx.band(d, 104, 576, "같은 이름의 오브젝트가 다른 namespace 에 있어도 부딪히지 않는다")

ox, oy, ow, oh = OUTER
d.o.append(f'<rect x="{ox}" y="{oy}" width="{ow}" height="{oh}" rx="8" '
           f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
ddx.ring_label(d, ox, oy, "Kubernetes cluster — 물리 클러스터는 하나", 11, INFO, off=16)

for (cx, cy), name, c in zip(NS, ["A팀의 namespace", "B팀의 namespace", "Alice 의 namespace"],
                             [OK, OK, ACC]):
    d.o.append(f'<rect x="{cx-NW//2}" y="{cy-NH//2}" width="{NW}" height="{NH}" rx="6" '
               f'fill="{c}0A" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - NH // 2 + 26, name, 12, c, KR, "middle", 600)
    for i, obj in enumerate(["Pods", "ConfigMaps", "그 밖의 오브젝트"]):
        d.t(cx, cy - 10 + i * 24, obj, 11, MUTED,
            MONO if all(ord(ch) < 128 for ch in obj) else KR)

for (cx, cy), name, c in zip(ACTORS, ["Team A", "Team B", "Alice"], [OK, OK, ACC]):
    d.box(cx - 90, cy - 30, 180, 60, PAPER2, c, 1.1, 6)
    d.t(cx, cy + 5, name, 13, c, MONO, "middle", 600)

d.path(f"M {ACTORS[0][0]} {ACTORS[0][1]-30-6} L {NS[0][0]} {NS[0][1]+NH//2+10}", OK, 1.6, m="ok")
d.path(f"M {ACTORS[1][0]} {ACTORS[1][1]-30-6} L {NS[1][0]} {NS[1][1]+NH//2+10}", OK, 1.6, m="ok")
d.path(f"M {ACTORS[2][0]} {ACTORS[2][1]-30-6} L {NS[2][0]} {NS[2][1]+NH//2+10}", ACC, 1.8, m="acc")
d.path(f"M {ACTORS[2][0]-90-6} {ACTORS[2][1]} L 620 {ACTORS[2][1]} L 620 {NS[1][1]+NH//2+10}",
       ACC, 1.8, m="acc")
# Alice 상자(710~890)와 회귀 열(620) 사이는 84px — 칩은 그 안에 드는 길이로
d.chip(662, ACTORS[2][1], "양쪽", ACC, 11)

d.t(36, 548, "namespace 는 이름의 스코프이자 권한의 스코프다 — 누가 어디에 닿는지가 곧 경계다.",
     12, MUTED, KR, "start")
d.legend(592, [("팀별 namespace", OK), ("두 곳에 닿는 사람", ACC), ("물리 클러스터", INFO)])
d.save("07-01-namespaces-virtual-clusters.svg")
print("ok namespaces-virtual-clusters")
