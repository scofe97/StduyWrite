# 17-02 §3 — 일반 파드가 받는 경로
# 짝 도식(hostnetwork-node)과 나란히 읽히도록 같은 골격으로 그린다. 이쪽에는 DNAT 와 veth 와
# 파드 전용 netns 가 있고, 저쪽에는 그 셋이 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 600, "KUBERNETES IN ACTION · 17-02",
      "일반 파드 — 변환과 건널목을 거친다",
      "노드 IP 로 들어온 패킷이 커널 규칙에서 목적지를 파드 IP 로 바꾼 뒤, veth 를 건너 그 파드만의 "
      "네트워크 네임스페이스 안에 있는 컨테이너에 닿는다.",
      "파드가 자기 IP 를 가진다")

d.box(60, 176, 1100, 244, PAPER, RULE, 0.9, 8)
d.t(610, 204, "노드", 11, SOFT, KR)
ddx.node(d, 190, 300, "노드 IP:30080", "패킷이 들어온다", 220, 76, INFO)
ddx.node(d, 540, 300, "커널 규칙", "DNAT — 목적지를 바꾼다", 240, 76, ACC)
# 통로 300~420 · 칩 308~412 — 양쪽 8px
d.path("M 302 300 L 416 300", MUTED, 1.5, m="ar")
d.chip(360, 272, "dst 노드 IP", SOFT, 9)

d.box(780, 236, 360, 152, PAPER2, OK, 1.0, 8)
d.t(960, 262, "파드 전용 netns", 11, OK, KR)
ddx.node(d, 960, 320, "컨테이너", "10.244.1.7:8080", 300, 62, OK)
# 통로 660~780 · 칩 668~772 — 양쪽 8px
d.path("M 662 300 L 776 300", OK, 1.5, m="ok")
d.chip(720, 272, "dst 파드 IP", ACC, 9)
d.t(720, 348, "veth", 10, SOFT, MONO)

d.t(24, 470, "파드가 자기 IP 와 자기 네임스페이스를 가지므로, 같은 포트를 쓰는 파드가 한 노드에 여럿 있어도 "
             "서로 충돌하지 않는다.", 11, MUTED, KR, "start")
d.t(24, 492, "대가는 홉 하나와 변환 한 번이다. 그것을 없애려는 것이 hostNetwork 다.", 11, MUTED, KR, "start")
d.legend(520, [("들어오는 자리", INFO), ("바꾸는 자리", ACC), ("파드의 영역", OK)])
d.save("17-02-hostnetwork-normal.svg")
print("ok")
