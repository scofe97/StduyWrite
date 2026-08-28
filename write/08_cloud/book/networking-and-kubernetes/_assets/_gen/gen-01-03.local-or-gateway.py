# 01-03.local-or-gateway — 안이냐 밖이냐, 누구의 MAC 을 물을지가 갈린다
# 본문 요구(00-03 §6): 마스크 대조 결과가 곧바로 "누구의 MAC 을 물을지"로 이어진다. 같으면 그
#           기계의 MAC 을 ARP 로 직접 알아내고, 다르면 기본 게이트웨이의 MAC 을 적는다. 그리고
#           "밖으로 판정되면 목적지 기계의 MAC 은 아예 묻지 않는다 — 물을 방법이 없기 때문"이라는
#           대목이 이 도식의 초점이다. 그래서 각 갈래 아래에 "브로드캐스트가 닿는가"를 한 칸 더 뒀다.
#           맨 아래 한 줄은 IP 목적지가 안 바뀐다는 사실 — 바뀌는 것은 겉봉의 MAC 뿐이다.
# 타입 스펙: type-flowchart.md — 조건 하나(내 서브넷 안인가)에서 두 갈래로 갈리는 판단 논리.
#           갈래마다 결론(겉봉 MAC)과 그 결론이 가능한 이유(브로드캐스트 도달 여부)가 붙는다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, PAPER2, KR

W, H = 1000, 620
X0, X1, GAP = 12, 970, 30       # 오른쪽 여백이 왼쪽보다 넓다 — 원본 좌표를 그대로 옮겼다
COLW = (X1 - X0 - GAP) / 2      # 갈래 둘이 그 안을 반씩 쓴다
CX = W / 2
LEFT, RIGHT = X0, X0 + COLW + GAP

d = D(W, H, "BRANCH · 01-03 ARP TARGET",
      "안이냐 밖이냐 — 누구의 MAC 을 물을지가 갈린다",
      "마스크 대조 결과에 따라 목적지 MAC 을 누구에게 물을지가 갈린다. 같은 서브넷이면 그 기계의 "
      "MAC 을 직접 알아내고, 다른 서브넷이면 기본 게이트웨이의 MAC 을 적는다. 바깥 기계의 MAC 은 "
      "알아낼 방법이 아예 없다 — 브로드캐스트가 로컬을 벗어나지 못하기 때문이다.",
      lead="바깥 기계의 MAC 은 물어볼 방법 자체가 없습니다.")

d.tone(CX - 160, 118, 320, 64, ACC, 6, "14", 1.4)
d.t(CX, 145, "마스크로 대조", 12, ACC, KR, "middle", 600)
d.t(CX, 166, "목적지가 내 서브넷 안인가?", 11, INK)

BRANCHES = [
    (LEFT,  OK,   "ok",   "안 — 같은 서브넷", "직접 묻는다",
     "목적지 기계의 MAC",     "ARP 브로드캐스트가 닿는다"),
    (RIGHT, WARN, "warn", "밖 — 다른 서브넷", "게이트웨이에게",
     "기본 게이트웨이의 MAC", "브로드캐스트는 로컬을 못 벗어난다"),
]

for x, c, mk, head, how, mac, why in BRANCHES:
    cx = x + COLW / 2
    d.arrow([(CX, 184), (CX, 210), (cx, 210), (cx, 233)], c, mk, 1.5)
    d.tone(x, 236, COLW, 62, c, 6, "14", 1.3)
    d.t(cx, 262, head, 12, c, KR, "middle", 600)
    d.t(cx, 283, how, 11, INK)
    d.box(x, 316, COLW, 58, PAPER2, RULE, 0.9)
    d.t(cx, 342, "겉봉에 적는 목적지 MAC", 10, SOFT)
    d.t(cx, 362, mac, 12, c, KR, "middle", 600)
    d.box(x, 386, COLW, 52, PAPER2, RULE, 0.9)
    d.t(cx, 417, why, 10, MUTED)

d.t(CX, 466, "IP 목적지는 어느 쪽이든 바뀌지 않습니다 — 바뀌는 것은 겉봉의 MAC 뿐입니다.", 10, ACC)
d.legend(486, [("같은 서브넷 — 직접", OK), ("다른 서브넷 — 게이트웨이", WARN)])
d.save("01-03.local-or-gateway.svg")
print("ok local-or-gateway")
