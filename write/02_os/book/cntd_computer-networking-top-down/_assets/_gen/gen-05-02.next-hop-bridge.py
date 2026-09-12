# 05-02 §4 — NEXT-HOP 이 BGP 와 OSPF 를 잇는 다리인 이유.
# 원문 5.4.2: NEXT-HOP 은 "the IP address of the router interface that begins the AS-PATH" 이고,
#       그 주소는 광고를 받은 AS 에 속하지 않지만 그 주소를 담은 서브넷은 직접 붙어 있다.
# 노트의 읽기: 10.0.0.0/30 · 10.0.0.1 · 10.0.0.2 는 원문에 없는 예시 주소다. 원문은 "2a 의 가장
#       왼쪽 인터페이스 주소" 라고만 적어, 학습자가 "그래서 그게 어느 주소냐" 에서 막혔다.
# 타입 스펙: type-architecture — 구성요소와 연결. AS 경계를 존으로 두르고 직각 연결선만 쓴다.
#       축약: AS3 방향과 iBGP 전파는 §3 의 몫이라 그리지 않는다. AS 경계는 실선 존으로 둘렀다.
import sys; sys.path.insert(0, ".")
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

W, H = 920, 560
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 05-02 §4",
      "NEXT-HOP 은 두 프로토콜을 잇는 다리입니다",
      "1b 가 받은 경로의 NEXT-HOP 은 AS2 라우터 2a 의 인터페이스 주소다. 그 주소가 든 서브넷은 "
      "AS1 에 직접 붙어 있어, 1b 는 OSPF 만으로 거기까지 가는 길을 안다.",
      "주소의 주인은 남의 AS 이고, 그 주소가 든 서브넷은 내 AS 에 붙어 있습니다")

# 1b 의 BGP 표에 실린 경로 하나
d.box(160, 112, 560, 68, PAPER2, RULE, 1.0, 8)
d.t(440, 140, "1b 의 BGP 표에 실린 경로 하나", 13, INK, KR, "middle", 600)
d.t(236, 164, "접두어 x", 13, MUTED, MONO)
d.t(424, 164, "AS-PATH  AS2 AS3", 13, MUTED, MONO)
d.t(624, 164, "NEXT-HOP  10.0.0.2", 13, ACC, MONO, "middle", 600)

# AS 경계
d.box(120, 256, 440, 144, "none", INFO, 1.2, 10)
d.box(680, 256, 200, 144, "none", INFO, 1.2, 10)
d.t(132, 278, "AS1", 13, INFO, MONO, "start", 600)
d.t(692, 278, "AS2", 13, INFO, MONO, "start", 600)

NODES = [(160, "1b", "AS1 내부 라우터"), (400, "1c", "AS1 경계 라우터"), (700, "2a", "AS2 경계 라우터")]
for x, name, sub in NODES:
    d.box(x, 288, 140, 56, PAPER2, RULE, 1.0, 7)
    d.t(x + 70, 312, name, 16, INK, MONO, "middle", 600)
    d.t(x + 70, 332, sub, 12, MUTED, KR)

# 직각 연결선만 — 세 요소가 한 행에 있어 모두 수평이다
d.path("M 230 180 L 230 288", MUTED, 1.2, m="ar")
d.t(246, 238, "BGP 가 어느 출구인지 알려줍니다", 12, MUTED, KR, "start")

d.path("M 300 316 L 400 316", MUTED, 1.4, m="ar")
d.t(350, 300, "OSPF", 12, MUTED, MONO)

d.path("M 540 316 L 700 316", ACC, 1.6)
d.chip(620, 296, "10.0.0.0/30", ACC, 13, 7)

d.t(536, 368, "10.0.0.1", 13, SOFT, MONO, "end")
d.t(704, 368, "10.0.0.2", 13, ACC, MONO, "start", 600)

d.t(12, 440, "1c 와 2a 를 잇는 링크의 서브넷은 AS1 에 직접 붙어 있습니다. "
             "그래서 1b 의 OSPF 가 10.0.0.0/30 을 이미 압니다.", 13, MUTED, KR, "start")
d.t(12, 462, "BGP 는 어느 출구로 나가나를 답하고, OSPF 는 그 출구까지 어떻게 가나를 답합니다. "
             "두 답이 NEXT-HOP 주소 하나에서 만납니다.", 13, MUTED, KR, "start")

d.legend(496, [("NEXT-HOP 과 그 서브넷", ACC), ("AS 경계", INFO), ("AS 안에서 아는 길", MUTED)])
d.t(W - 12, 540, "KUROSE-ROSS 9E FIG 5.10", 8, SOFT, MONO, "end")

d.save("05-02.next-hop-bridge.svg")
print("ok 05-02.next-hop-bridge")
