# 04-01.l2-adjacency — ARP 가 닿는 범위는 CNI 방식에 달려 있다
# 본문 요구: "bridge 형 CNI 는 같은 노드의 Pod 를 한 브리지에 꽂아 ARP 로 상대 MAC 을 찾는다 / ptp 형 CNI(kindnet)는
#           Pod 마다 점대점 veth 라 Pod 가 ARP 로 묻는 이웃은 게이트웨이 하나다 / 어느 쪽이든 노드를 넘으면 ARP 는 멈추고
#           노드 라우팅 테이블이 IP 로 보낸다"
# 타입 스펙: type-nested — 논지가 "브로드캐스트 도메인이라는 범위가 어디까지인가"라서 포함 관계로 그린다.
#           왼쪽은 범위가 노드 안 전체, 가운데는 범위가 Pod 하나와 게이트웨이, 오른쪽은 범위 밖.
#           2026-11-08 kind(kindnet) 실측으로 가운데 패널을 더했다 — "같은 노드면 항상 ARP" 가 아니다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 464
d = D(W, H, "L2 ADJACENCY · WHERE ARP STOPS WORKING",
      "같은 노드여도 ARP 가 상대 Pod 에 닿는지는 CNI 방식이 정한다",
      "bridge 형 CNI 는 같은 노드의 Pod 를 한 브로드캐스트 도메인에 묶고, ptp 형 CNI 는 Pod 가 게이트웨이만 ARP 로 묻게 한다. "
      "노드를 넘으면 어느 쪽이든 ARP 는 멈추고 L3 라우팅이 맡는다.",
      lead="MAC 은 어느 Pod 에나 있다 — 갈리는 것은 ARP 가 누구에게 닿느냐")

PY, PH, PW = 104, 272, 308
PX = (24, 346, 668)
FY, POD_W, POD_H, POD_Y = 148, 104, 52, 176
BAR_Y, BAR_H = 256, 32


def panel(x, title, c):
    d.box(x, PY, PW, PH, PAPER2, c, 1.2, 8)
    d.t(x + 20, PY + 26, title, 14, c, KR, "start", 600)


def frame(x, w, name):
    d.o.append(f'<rect x="{x}" y="{FY}" width="{w}" height="154" rx="6" fill="none" '
               f'stroke="{RULE}" stroke-width="1.0" stroke-dasharray="5 5"/>')
    d.t(x + 12, FY + 20, name, 11, SOFT, MONO, "start")


def pod(cx, name, ip):
    d.box(cx - POD_W // 2, POD_Y, POD_W, POD_H, PAPER, RULE, 1.0, 6)
    d.t(cx, POD_Y + 22, name, 13, INK, KR, "middle", 600)
    d.t(cx, POD_Y + 42, ip, 12, MUTED, MONO)


def bar(x, w, txt, c):
    d.tone(x, BAR_Y, w, BAR_H, c, 6, "14", 1.1)
    d.t(x + w // 2, BAR_Y + 21, ddx.fit(txt, 12, w - 16, txt), 12, c, KR)


def caption(x, l1, l2, c):
    d.t(x + PW // 2, 332, ddx.fit(l1, 13, PW - 24, l1), 13, c, KR, "middle", 600)
    d.t(x + PW // 2, 356, l2, 12, MUTED, KR)


# 1. bridge 형 — 같은 노드 전체가 한 브로드캐스트 도메인
x0 = PX[0]
panel(x0, "bridge 형 · 같은 노드 (예시 값)", OK)
frame(x0 + 12, 284, "NODE 1")
A, B = x0 + 76, x0 + 232
pod(A, "Pod A", "10.1.3.7"); pod(B, "Pod B", "10.1.3.8")
bar(x0 + 24, 260, "브리지 · 브로드캐스트 도메인 하나", OK)
for cx in (A, B):
    d.line(cx, POD_Y + POD_H, cx, BAR_Y, OK, 1.2)
d.arrow([(A + POD_W // 2 + 4, POD_Y + 30), (B - POD_W // 2 - 8, POD_Y + 30)], OK, "ok", 1.5)
d.t((A + B) // 2, POD_Y + 20, "ARP", 12, OK, MONO, "middle", 600)
caption(x0, "ARP 응답 · Pod B 의 MAC", "상대 Pod 를 L2 에서 찾는다", OK)

# 2. ptp 형 — Pod 는 게이트웨이만 ARP 로 묻는다 (kindnet 실측)
x1 = PX[1]
panel(x1, "ptp 형 · 같은 노드", ACC)
frame(x1 + 12, 284, "NODE 1")
A2, B2 = x1 + 76, x1 + 232
pod(A2, "Pod A", "10.244.2.2"); pod(B2, "Pod B", "10.244.2.3")
bar(x1 + 24, 260, "노드 라우팅 · 게이트웨이 10.244.2.1", ACC)
d.arrow([(A2, POD_Y + POD_H + 2), (A2, BAR_Y - 8)], ACC, "acc", 1.5)
d.arrow([(B2, BAR_Y - 2), (B2, POD_Y + POD_H + 8)], ACC, "acc", 1.5)
d.t(x1 + PW // 2, POD_Y + 30, "ARP 없음", 11, SOFT, KR, "middle")
caption(x1, "ARP 는 게이트웨이에만", "Pod 사이는 노드가 라우팅한다", ACC)

# 3. 노드를 넘을 때 — ARP 경계
x2 = PX[2]
panel(x2, "노드를 넘을 때", INFO)
frame(x2 + 12, 136, "NODE 1")
frame(x2 + 160, 136, "NODE 2")
C1, C2 = x2 + 80, x2 + 228
pod(C1, "Pod A", "10.244.2.2"); pod(C2, "Pod C", "10.244.1.2")
BX = x2 + 154
d.line(BX, FY - 8, BX, 244, BAD, 1.6, "5 4")
d.chip(BX, FY - 16, "ARP 경계", BAD, 12)
bar(x2 + 20, 124, "라우팅 테이블", INFO)
bar(x2 + 168, 124, "라우팅 테이블", INFO)
d.arrow([(C1, POD_Y + POD_H + 4), (C1, BAR_Y - 8)], INFO, "info", 1.4)
d.arrow([(C2, BAR_Y - 2), (C2, POD_Y + POD_H + 8)], INFO, "info", 1.4)
caption(x2, "브로드캐스트 불통 · IP 로 라우팅", "L3 에서 해결", INFO)

d.legend(400, [("노드 안 전체가 L2", OK), ("게이트웨이로만 ARP", ACC), ("L3 라우팅 구간", INFO), ("ARP 가 멈추는 경계", BAD)])
d.save("04-01.l2-adjacency.svg")
print("ok l2-adjacency")
