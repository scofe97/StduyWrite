# 11-01 §1 — 파드끼리는 NAT 없이 통신한다
# 본문의 요지는 '홉을 지나도 주소가 그대로'다. 물리 토폴로지와 파드가 보는 층을 위아래로 놓고,
# 홉마다 같은 목적지 칩을 반복해 불변을 눈으로 세게 한다. type-layers 의 두 층 관례.
# 타입 스펙: type-layers.md — 물리 토폴로지와 파드가 보는 층을 위아래로 놓은 두 층. 같은 목적지 칩을 홉마다 반복해
#           주소 불변을 눈으로 세게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1000, 596, "KUBERNETES IN ACTION · 11-01",
      "파드끼리는 NAT 없이 통신한다",
      "노드가 여러 라우터를 사이에 두고 떨어져 있어도, 파드가 보내는 패킷의 출발지·목적지 주소는 "
      "홉을 지나며 바뀌지 않는다. 받는 파드는 보낸 파드의 진짜 IP를 출발지로 본다.",
      "물리 토폴로지는 파드에게 보이지 않는다")

PA, PB = 200, 800

# 위 — 파드가 보는 것
ddx.band(d, 100, 288, "파드가 보는 것 — 하나의 flat 네트워크")
ddx.node(d, PA, 208, "파드 A", "10.244.1.5", 152, 56, INFO)
ddx.node(d, PB, 208, "파드 B", "10.244.2.9", 152, 56, INFO)
d.path(f"M {PA+84} 208 L {PB-88} 208", MUTED, 1.5, m="ar")
d.chip(500, 178, "src 10.244.1.5  ·  dst 10.244.2.9", MUTED, 9)
ddx.focal_tag(d, 500, 244, "출발지도 목적지도 바꾸지 않는다", 268)

# 아래 — 실제 네트워크
ddx.band(d, 316, 528, "실제 네트워크 — 노드는 라우터를 사이에 두고 떨어져 있다")
for cx, nm in ((PA, "노드 1"), (PB, "노드 2")):
    d.box(cx - 100, 356, 200, 112, PAPER, RULE, 0.9, 8)
    d.t(cx, 378, nm, 11, SOFT, KR)
ddx.node(d, PA, 424, "파드 A", "10.244.1.5", 152, 52, INFO)
ddx.node(d, PB, 424, "파드 B", "10.244.2.9", 152, 52, INFO)
for cx in (400, 600):
    ddx.node(d, cx, 424, "라우터", "L3 홉", 96, 52)

for a, b in ((PA + 76, 400 - 48), (400 + 48, 600 - 48), (600 + 48, PB - 76)):
    d.path(f"M {a+8} 424 L {b-10} 424", MUTED, 1.4, m="ar")
d.t(120, 500, "홉마다 본 목적지", 10, SOFT, KR, "start")
for cx in (314, 500, 686):
    d.chip(cx, 496, "dst 10.244.2.9", SOFT, 9)

# 대응
for cx in (PA, PB):
    d.line(cx, 236, cx, 356, RULE, 0.9, "3 6")

d.legend(548, [("파드 주소", INFO), ("변하지 않는다", ACC)])
d.save("11-01-pod-flat-network.svg")
print("ok")
