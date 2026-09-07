# 03-01 §4 — 포트는 하나인데 소켓은 연결 수만큼이다.
# 원문 3.2: "the Web server has a different socket for each connection" · 최초 연결 요청만 환영 소켓으로
#       가고 그 뒤로 만들어진 연결 소켓이 4튜플로 식별된다.
# 노트의 읽기: 2026-09-07 학습 세션에서 학습자가 "듣는 소켓과 연결된 소켓이 따로 있다고?" 라고 되물어
#       추가한 도식. 원문은 이름만 대고 넘어가고 02-01 은 소켓 API 축으로 보였으므로, 이 도식은
#       *역다중화 축* 으로 그린다 — 도착한 세그먼트가 어느 소켓으로 갈라지는가.
#   listen(2): "marks the socket referred to by sockfd as a passive socket, that is, as a socket that
#       will be used to accept incoming connection requests using accept(2)."
#   accept(2): "extracts the first connection request on the queue of pending connections for the
#       listening socket, sockfd, creates a new connected socket ... The original socket sockfd is
#       unaffected by this call."
#   recvfrom(2): "If src_addr is not NULL ... that source address is placed in the buffer pointed to
#       by src_addr." / recv(2): "equivalent to the call: recvfrom(fd, buf, size, flags, NULL, NULL)"
# 타입 스펙: type-architecture — 구성 요소(소켓)와 그 사이로 흐르는 관계를 zone 둘로 갈라 놓는다.
#       같은 노트의 03-01.mux-demux 도 이 타입이지만 그쪽은 *층과 포트* 를 그리고 이쪽은
#       *소켓 인스턴스와 그 4튜플* 을 그린다 — 대상이 다르다.
#       accent 는 하나뿐이며 학습자가 있는 줄 몰랐던 그 소켓, 곧 데이터를 나르지 않는 듣는 소켓이다.
#       축약: 3-way 핸드셰이크의 순서는 03-04 의 몫이라 여기서는 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 712
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-01 §4",
      "포트는 하나인데 소켓은 연결 수만큼이다",
      "TCP 서버는 듣는 소켓 하나로 연결 요청만 받고, 연결마다 따로 만든 소켓에서 데이터를 주고받는다. "
      "UDP 는 소켓 하나가 전부 받는다.",
      "넷이 안 섞이는 근거가 4튜플입니다")

ZY, ZH = 148, 396
TX, TW = 24, 600
UX, UW = 640, 336
for x, w, name, sub in ((TX, TW, "TCP", "소켓이 연결 수만큼"), (UX, UW, "UDP", "소켓 하나가 다 받는다")):
    d.box(x, ZY, w, ZH, "rgba(245,245,245,0.02)", RULE, 1.0, 8)
    d.t(x + 20, ZY + 30, name, 15, INK, MONO, "start", 600)
    d.t(x + 20 + (34 if name == "TCP" else 38), ZY + 30, sub, 12, MUTED, KR, "start")

# ── TCP — 듣는 소켓 하나 + 연결된 소켓 셋 ───────────────────────
LSX, LSW = 300, 300
d.tone(LSX, ZY + 52, LSW, 60, ACC, 8, "12", 1.5)
d.t(LSX + 16, ZY + 78, "듣는 소켓", 13, ACC, KR, "start", 600)
d.t(LSX + LSW - 16, ZY + 78, "*:80  LISTEN", 12, ACC, MONO, "end")
d.t(LSX + 16, ZY + 100, "새 연결 요청만 받는다 — 데이터는 나르지 않는다", 11.5, MUTED, KR, "start")

d.arrow([(LSX + LSW / 2, ZY + 116), (LSX + LSW / 2, ZY + 146)], SOFT, "soft", 1.4, dash="4 4")
d.t(LSX + LSW / 2 - 14, ZY + 138, "accept() 가 연결마다 하나씩", 11.5, SOFT, KR, "end")

conns = [
    ("클라이언트 A", "1.1.1.1:26145"),
    ("클라이언트 B", "2.2.2.2:7532"),
    ("클라이언트 C", "3.3.3.3:26145"),
]
CY, CH, CGAP = ZY + 154, 46, 12
for i, (who, src) in enumerate(conns):
    y = CY + i * (CH + CGAP)
    d.box(44, y, 200, CH, PAPER2, RULE, 1.0, 6)
    d.t(58, y + 20, who, 11.5, MUTED, KR, "start")
    d.t(58, y + 37, src, 11.5, INK, MONO, "start")
    d.box(LSX, y, LSW, CH, PAPER2, OK, 1.2, 6)
    d.t(LSX + 16, y + 20, "연결된 소켓", 11.5, OK, KR, "start", 600)
    d.t(LSX + LSW - 16, y + 20, f"fd={5 + i * 2}", 11, MUTED, MONO, "end")
    d.t(LSX + 16, y + 37, f"{src} → *:80", 11.5, INK, MONO, "start")
    d.arrow([(246, y + CH / 2), (LSX - 4, y + CH / 2)], OK, "ok", 1.4)

d.t(44, ZY + ZH - 24, "목적지는 셋 다 :80 으로 같습니다. 갈라 주는 것은 출발지입니다 — 그것이 4튜플입니다.",
    12, MUTED, KR, "start")

# ── UDP — 소켓 하나로 모인다 ────────────────────────────────────
USX, USW = 790, 170
d.box(USX, ZY + 176, USW, 58, PAPER2, INFO, 1.2, 6)
d.t(USX + 16, ZY + 202, "소켓 하나", 12.5, INFO, KR, "start", 600)
d.t(USX + 16, ZY + 222, "*:12000", 12, INK, MONO, "start")
for i, src in enumerate(("A 57418", "B 49530", "C 51002")):
    y = ZY + 96 + i * 56
    d.box(660, y, 90, 40, PAPER2, RULE, 1.0, 6)
    d.t(705, y + 25, src, 11.5, MUTED, MONO)
    # 세 화살표가 x=768 한 줄기로 모였다 내려간다. 대각선은 lint 가 막으므로 직교로 꺾는다.
    d.arrow([(752, y + 20), (768, y + 20), (768, ZY + 205), (USX - 4, ZY + 205)], INFO, "info", 1.3)

d.t(660, ZY + ZH - 44, "출발지가 달라도 같은 소켓입니다.", 12, MUTED, KR, "start")
d.t(660, ZY + ZH - 24, "그래서 recvfrom() 이 출발지를 함께 줍니다.", 12, MUTED, KR, "start")

BY = ZY + ZH + 22
d.tone(24, BY, W - 48, 78, ACC)
d.t(44, BY + 28, "튜플의 개수가 API 를 정합니다", 13, INK, KR, "start", 600)
d.t(44, BY + 50, "TCP 의 연결된 소켓은 4튜플로 상대를 이미 알아서 recv() 로 충분합니다.", 12, MUTED, KR, "start")
d.t(44, BY + 70, "UDP 소켓은 2튜플뿐이라 상대를 모릅니다 — 답장하려면 recvfrom() 이 준 출발지를 써야 합니다.",
    12, MUTED, KR, "start")

d.legend(BY + 100, [("데이터를 안 나르는 소켓", ACC), ("연결마다 하나씩", OK), ("전부 한 소켓으로", INFO)])
d.save("03-01.listen-vs-connected.svg")
print("ok 03-01.listen-vs-connected")
