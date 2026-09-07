# 03-02 §3·§4 — 같은 사고(1~5 를 보냈고 3 이 사라짐)에서 GBN 과 SR 이 어떻게 갈리는지.
# 본문 근거: GBN 수신자는 "그 밖의 모든 경우에는 패킷을 버리고 가장 최근에 순서대로 받은 패킷의
#   ACK 를 다시 보냅니다", 타임아웃 시 "보냈지만 확인되지 않은 패킷을 전부 다시 보냅니다".
#   SR 수신자는 "순서에서 벗어난 패킷은 빠진 것이 채워질 때까지 버퍼에 둡니다".
# 논점은 재전송 양이 아니라 "받는 쪽이 무엇을 들고 있어야 하는가" 다 — 숫자 하나 대 버퍼·표시·로직.
# 타입 스펙: type-swimlane — 같은 사건 열을 두 주체가 각자 어떻게 처리하는지 나란히 놓는다.
#            축약: 창 크기는 5 로 고정하고 창 미끄러짐은 그리지 않는다(gbn-window.svg 가 그 축이다).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 1000, 604
d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-02 §3·§4",
      "3 만 사라졌는데 넷과 다섯의 운명이 갈립니다",
      "창 5 로 1~5 를 보냈고 3 이 망에서 사라진 같은 상황. 두 방식이 4·5 를 다르게 다루고, "
      "그 차이가 재전송 양이 아니라 수신자가 들고 있어야 하는 것에서 나온다.",
      "고른다는 것은 수신자를 얼마나 복잡하게 할지를 고르는 일입니다")

CX0, CW, NC = 170, 160, 5
LY = [156, 288]
LH = 112
COLS = ["1~5 를 보냄", "3 이 사라짐", "4 가 도착", "5 가 도착", "타임아웃"]

for i, c in enumerate(COLS):
    x = CX0 + i * CW
    d.t(x + CW / 2, 144, c, 11, SOFT, KR, "middle", 600)
    if i:
        d.line(x, 156, x, LY[1] + LH, RULE, 0.7, "3 6")

ROWS = [
    ("Go-Back-N", "누적 ACK · 타이머 하나", WARN, [
        ("보냅니다", "창이 5 라 다섯이\n동시에 떠 있습니다", MUTED),
        ("모릅니다", "송신자에게는\n아무 일도 없습니다", SOFT),
        ("버립니다", "기대는 3 인데 4 라\nACK 2 를 다시 보냅니다", WARN),
        ("또 버립니다", "이미 온 데이터인데도\nACK 2 를 또 보냅니다", WARN),
        ("셋을 다시", "3·4·5 를 전부\n재전송합니다", BAD),
    ]),
    ("Selective Repeat", "개별 ACK · 패킷마다 타이머", OK, [
        ("보냅니다", "같습니다", MUTED),
        ("모릅니다", "같습니다", SOFT),
        ("버퍼에 둡니다", "ACK 4 를 보내고\n3 자리를 비워 둡니다", OK),
        ("버퍼에 둡니다", "ACK 5 를 보내고\n그대로 기다립니다", OK),
        ("하나만 다시", "3 만 재전송하고\n오면 셋을 함께 올립니다", ACC),
    ]),
]

for r, (name, sub, col, cells) in enumerate(ROWS):
    y = LY[r]
    d.tone(24, y, W - 48, LH, col, 6, "0A", 1.1)
    d.t(40, y + 30, name, 13, col, KR, "start", 600)
    d.t(40, y + 50, sub, 11, SOFT, MONO, "start")
    for i, (head, body, c) in enumerate(cells):
        x = CX0 + i * CW
        d.t(x + CW / 2, y + 34, head, 11, c, KR, "middle", 600)
        for j, ln in enumerate(body.split("\n")):
            d.t(x + CW / 2, y + 60 + j * 18, ln, 11, MUTED, KR)

d.box(24, 424, W - 48, 92, PAPER2, RULE, 0.9, 6)
d.t(44, 450, "값은 재전송 양이 아니라 수신자가 드는 무게입니다", 12, INK, KR, "start", 600)
d.t(44, 474, "GBN 의 수신자가 들고 있는 것은 '다음에 기대하는 번호' 하나뿐입니다. SR 의 수신자는 버퍼와 받음 표시와 창 로직을 함께 듭니다.",
    11, MUTED, KR, "start")
d.t(44, 494, "그래서 손실이 잦으면 SR 이 이기고, 수신자가 단순해야 하면 GBN 이 이깁니다. TCP 는 누적 ACK 위에 SACK 을 얹어 사이에 섭니다.",
    11, MUTED, KR, "start")

d.legend(H - 44, [("낭비가 생기는 자리", WARN), ("아낀 자리", OK), ("한 번에 다시 보내는 양", BAD), ("SR 이 얻는 것", ACC)])
d.save("03-02.gbn-vs-sr.svg")
print("ok gbn-vs-sr")
