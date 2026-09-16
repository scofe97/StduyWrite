# 04-01.l2-adjacency — ARP 가 닿는 범위는 자기 노드의 브리지까지
# 본문 요구: "같은 노드의 Pod 둘은 한 브리지 … 하나의 브로드캐스트 도메인 … 다른 노드의 Pod 는 그 브리지에 없습니다.
#           ARP 는 노드 경계를 넘지 못하므로 … 노드가 라우팅 테이블을 보고 상대 노드로 보냅니다"
# 타입 스펙: type-nested — 논지가 "브로드캐스트 도메인이라는 범위가 어디까지인가"라서 포함 관계로 그린다.
#           왼쪽은 범위 안, 오른쪽은 범위 밖. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 468
d = D(W, H, "L2 ADJACENCY · WHERE ARP STOPS WORKING",
      "같은 노드면 ARP 로 찾고, 다른 노드면 라우팅으로 간다",
      "Pod 의 eth0 에는 MAC 이 있지만 노드 경계를 넘으면 같은 브로드캐스트 도메인이 아니어서 "
      "ARP 로 상대를 찾을 수 없고 L3 라우팅에 의존한다.",
      lead="MAC 은 있다 — 없는 것은 노드 사이의 L2 인접성")

PY, PH = 104, 288                       # 두 패널
PW = 456
PX = (32, 512)
FY = 144                                # 노드 틀 윗변
POD_W, POD_H, POD_Y = 148, 56, 176


def panel(x, title, c):
    d.box(x, PY, PW, PH, PAPER2, c, 1.2, 8)
    d.t(x + 20, PY + 26, title, 14, c, KR, "start", 600)


def frame(x, w, h, name):
    d.o.append(f'<rect x="{x}" y="{FY}" width="{w}" height="{h}" rx="6" fill="none" '
               f'stroke="{RULE}" stroke-width="1.0" stroke-dasharray="5 5"/>')
    d.t(x + 12, FY + 20, name, 11, SOFT, MONO, "start")


def pod(cx, name, ip):
    d.box(cx - POD_W // 2, POD_Y, POD_W, POD_H, PAPER, RULE, 1.0, 6)
    d.t(cx, POD_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(cx, POD_Y + 44, ip, 12, MUTED, MONO)


# 왼쪽 — 같은 노드 안: 브리지 하나가 브로드캐스트 도메인 하나
panel(PX[0], "같은 노드 안", OK)
frame(56, 408, 156, "NODE 1")
A, B = 160, 360
pod(A, "Pod A", "10.1.3.7"); pod(B, "Pod B", "10.1.3.8")
BR_Y, BR_H = 256, 32
d.tone(80, BR_Y, 360, BR_H, OK, 6, "14", 1.1)
d.t(260, BR_Y + 21, "브리지 · 브로드캐스트 도메인 하나", 12, OK, KR)
for cx in (A, B):
    d.line(cx, POD_Y + POD_H, cx, BR_Y, OK, 1.2)
d.arrow([(A + POD_W // 2 + 6, POD_Y + 28), (B - POD_W // 2 - 10, POD_Y + 28)], OK, "ok", 1.5)
d.t((A + B) // 2, POD_Y + 18, "ARP", 12, OK, MONO, "middle", 600)
d.t(PX[0] + PW // 2, 340, "ARP 응답 · Pod B 의 MAC", 13, OK, KR, "middle", 600)
d.t(PX[0] + PW // 2, 364, "L2 에서 해결", 12, MUTED, KR)

# 오른쪽 — 노드를 넘을 때: ARP 경계, 노드 라우팅 테이블
panel(PX[1], "노드를 넘을 때", INFO)
frame(536, 188, 96, "NODE 1")
frame(756, 188, 96, "NODE 2")
C1, C2 = 630, 850
pod(C1, "Pod A", "10.1.3.7"); pod(C2, "Pod C", "10.1.9.4")
BX = 740
d.line(BX, FY - 8, BX, 244, BAD, 1.6, "5 4")
d.chip(BX, FY - 16, "ARP 경계", BAD, 12)
RT_Y, RT_H = 256, 32
d.tone(552, RT_Y, 376, RT_H, INFO, 6, "14", 1.1)
d.t(740, RT_Y + 21, "노드 라우팅 테이블 · 목적지 IP", 12, INFO, KR)
d.arrow([(C1, POD_Y + POD_H + 4), (C1, RT_Y - 8)], INFO, "info", 1.4)
d.arrow([(C2, RT_Y - 2), (C2, POD_Y + POD_H + 8)], INFO, "info", 1.4)
d.t(PX[1] + PW // 2, 340, "브로드캐스트 불통 · IP 로 라우팅", 13, INFO, KR, "middle", 600)
d.t(PX[1] + PW // 2, 364, "L3 에서 해결", 12, MUTED, KR)

d.legend(420, [("L2 로 해결되는 범위", OK), ("L3 라우팅이 맡는 구간", INFO), ("ARP 가 멈추는 경계", BAD)])
d.save("04-01.l2-adjacency.svg")
print("ok l2-adjacency")
