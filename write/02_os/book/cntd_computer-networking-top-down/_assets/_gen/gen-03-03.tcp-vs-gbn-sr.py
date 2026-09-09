# 03-03 §6 — 같은 사고에서 순수 GBN 과 TCP 가 실제로 몇 개를 다시 보내는가.
# 옆의 gbn-sr-hybrid.svg 는 두 방식의 성질을 집합으로 견주는 분류 축이고, 이 도식은 기법 축이다.
# 본문 근거 그대로: "세그먼트 1부터 N 까지 다 도착했는데 ACK n 하나만 유실되고 나머지가 제때 왔다고 해 봅니다.
#   GBN 은 n 부터 N 까지 전부 다시 보냅니다. TCP 는 많아야 한 개, 즉 n 만 다시 보냅니다.
#   게다가 n+1 의 ACK 가 n 의 타임아웃 전에 오면 n 조차 다시 보내지 않습니다."
#   n = 3, N = 5 로 두고 셋을 나란히 놓은 것이다.
# 타입 스펙: type-swimlane — 같은 사건 열을 세 주체가 각자 어떻게 처리하는지 나란히 놓는다.
#   축약: 손실은 ACK 3 하나뿐이고 데이터 세그먼트는 다 도착한 경우다. 데이터가 사라진 경우는 §5 가 다룬다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 660
CX0, CW, NC = 216, 188, 4
LY, LH = [172, 288, 404], 104
COLS = ["1~5 를 보냅니다", "다섯 다 도착합니다", "ACK 3 만 유실됩니다", "그래서 다시 보내는 것은"]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §6",
      "같은 사고인데 다시 보내는 양이 셋으로 갈립니다",
      "데이터는 다섯 다 도착했고 ACK 3 하나만 사라진 상황. 순수 GBN 이라면 셋을 다시 보내고 "
      "TCP 는 많아야 하나이며, 뒤 ACK 가 제때 오면 하나도 안 보낸다.",
      "누적 ACK 는 GBN 쪽인데 재전송 양은 SR 쪽입니다")

for i, c in enumerate(COLS):
    x = CX0 + i * CW
    d.t(x + CW / 2, 160, c, 11, SOFT, KR, "middle", 600)
    if i:
        d.line(x, 172, x, LY[2] + LH, RULE, 0.7, "3 6")

ROWS = [
    ("순수 GBN 이라면", "누적 ACK · 타이머 하나", WARN,
     [("보냅니다", "창이 5 입니다", MUTED), ("받는 쪽은 다 받았습니다", "ACK 1~5 를 보냅니다", MUTED),
      ("송신자는 3 에서 막힙니다", "SendBase 가 3 에 멈춥니다", WARN),
      ("3 · 4 · 5 를 전부", "이미 도착한 둘까지 다시", BAD)]),
    ("TCP — 뒤 ACK 가 늦으면", "타임아웃을 일으킨 것만", INFO,
     [("같습니다", "", SOFT), ("같습니다", "", SOFT),
      ("같습니다", "SendBase 가 3 에 멈춥니다", WARN),
      ("3 하나만", "많아야 한 개입니다", ACC)]),
    ("TCP — 뒤 ACK 가 제때 오면", "누적 ACK 가 앞을 덮습니다", OK,
     [("같습니다", "", SOFT), ("같습니다", "", SOFT),
      ("ACK 4 가 도착합니다", "4까지 다 받았다는 뜻입니다", OK),
      ("하나도 안 보냅니다", "SendBase 가 그냥 넘어갑니다", OK)]),
]
for r, (name, sub, col, cells) in enumerate(ROWS):
    y = LY[r]
    d.tone(24, y, W - 48, LH, col, 6, "0A", 1.1)
    d.t(40, y + 30, name, 12, col, KR, "start", 600)
    d.t(40, y + 50, sub, 11, SOFT, KR, "start")
    for i, (head, body, c) in enumerate(cells):
        x = CX0 + i * CW
        d.t(x + CW / 2, y + 40, head, 11, c, KR, "middle", 600)
        if body:
            d.t(x + CW / 2, y + 62, body, 11, MUTED, KR)

d.box(24, 526, W - 48, 82, PAPER2, RULE, 0.9, 6)
d.t(44, 552, "그래서 어느 이름도 안 맞습니다", 12, INK, KR, "start", 600)
d.t(44, 574, "확인 응답이 누적이고 순서 밖 세그먼트를 개별 확인하지 않는 것은 GBN 쪽입니다. 그런데 재전송이 「많아야 한 개」인 것은 SR 쪽입니다.",
    11, MUTED, KR, "start")
d.t(44, 594, "여기에 SACK 을 켜면 받는 쪽이 순서 밖 세그먼트를 골라서 확인해 주므로 SR 쪽으로 더 갑니다. 결론이 혼종인 이유입니다.",
    11, ACC, KR, "start")

d.legend(H - 44, [("막히는 자리", WARN), ("낭비", BAD), ("TCP 가 아끼는 자리", ACC), ("아무 일도 안 하는 자리", OK)])
d.save("03-03.tcp-vs-gbn-sr.svg")
print("ok tcp-vs-gbn-sr")
