# 05-04 실습 — 흐름 표를 한 줄 바꿀 때마다 같은 패킷의 운명이 달라진다.
# 2026-09-14 신설: 손으로 쓴 SVG 만 있어 타입 선택 절차를 거치지 않은 장이었다.
#   여섯 줄이 모두 ns1 → br0 → ns2 라는 같은 경로를 쓰고, 달라지는 것은 br0 에서 무슨 일이 나는가뿐이다.
#   그래서 경로를 여섯 번 다시 그리되 패킷이 어디까지 가는지를 칸마다 달리 그린다 — 표가 아니라 흐름이다.
# 타입 스펙: type-swimlane — 레인(ns1 · br0 · ns2)은 고정이고 행마다 그 위를 지나는 결과가 바뀐다.
#   축약: 시간축 대신 실습 회차를 세로로 쌓았다. 한 행 안에서는 왼→오가 시간 순서다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 604

d = D(W, H, "SECTION 5.3 LAB · FLOW TABLE STATES",
      "표를 한 줄 바꿀 때마다 패킷의 운명이 바뀝니다",
      "같은 경로(ns1 → br0 → ns2)에 같은 패킷을 여섯 번 흘려보내고, 흐름 표만 한 줄씩 바꾼다. br0 에 깔린 줄이 무엇이냐에 따라 패킷은 끝까지 가기도 하고, 다리에서 버려지기도 하고, 세어지기만 하기도 한다.",
      "왼쪽이 표에 든 줄, 오른쪽이 그 패킷이 어디까지 갔는가")

LANE_X = (352, 470, 588)          # ns1 · br0 · ns2
ROW_Y0, ROW_STRIDE = 126, 74
PW, PH = 22, 16

# (회차, 표에 든 줄, 부연, br0 에서의 결말, 끝까지 가는가, 결말색)
ROWS = [
    ("1", "priority=0 actions=NORMAL", "fail_mode 기본값이 깔아 둔 줄", None, True, OK, "도착 — 옛 L2 경로"),
    ("2", "(비어 있음)", "del-flows 로 비운 뒤", "폐기", False, BAD, "폐기 — 올려보낼 컨트롤러 없음"),
    ("3", "in_port=1 → output:2", "한 방향만 넣었을 때", "응답 폐기", False, BAD, "ARP 응답이 죽어 시작 못 함"),
    ("4", "arp,in_port=2 → drop", "돌아오는 ARP 만 세어 버림", "세고 버림", False, WARN, "84 바이트 세어짐 — 답은 옴"),
    ("5", "in_port=1 → CONTROLLER", "Packet-in 으로 올려보냄", "올라감 · 답 없음", False, INFO, "올라가지만 답이 없어 끝"),
    ("6", "tcp,tp_dst=9090 → drop", "TCP 포트로 일치", "9090 만 차단", False, WARN, "8080 도착 · 9090 침묵"),
]

# 레인 머리
for x, name in zip(LANE_X, ("ns1", "br0", "ns2")):
    d.t(x, 112, name, 12, SOFT, MONO)
d.t(24, 112, "흐름 표에 든 줄", 12, SOFT, KR, "start", 600)
d.t(700, 112, "어디까지 갔나", 12, SOFT, KR, "start", 600)

for i, (num, rule, note, halt, through, c, verdict) in enumerate(ROWS):
    y = ROW_Y0 + i * ROW_STRIDE
    mid = y + PH / 2

    d.t(24, y + 8, num, 11, SOFT, MONO, "start")
    d.t(40, y + 8, rule, 12, INK, MONO, "start")
    d.t(40, y + 26, note, 11, MUTED, KR, "start")

    # 레인 — 세 점은 고정, 달라지는 것은 패킷이 어디서 멈추는가
    for x in LANE_X:
        d.line(x - 16, mid, x + 16, mid, RULE, 1.0)

    # ns1 에서 출발
    d.tone(LANE_X[0] - PW / 2, y, PW, PH, MUTED, 3, "22", 1.0)
    d.path(f"M {LANE_X[0] + 16} {mid} L {LANE_X[1] - 20} {mid}", MUTED, 1.2, m="ar")

    if through:
        # br0 을 지나 ns2 까지
        d.tone(LANE_X[1] - PW / 2, y, PW, PH, c, 3, "22", 1.1)
        d.path(f"M {LANE_X[1] + 16} {mid} L {LANE_X[2] - 20} {mid}", c, 1.3, m="ok")
        d.tone(LANE_X[2] - PW / 2, y, PW, PH, c, 3, "22", 1.1)
    else:
        # br0 에서 멈춘다 — 멈춘 자리에 X 를 둔다
        d.tone(LANE_X[1] - PW / 2, y, PW, PH, c, 3, "22", 1.1)
        d.t(LANE_X[1], y + 30, f"✕ {halt}", 11, c, KR)
        d.line(LANE_X[2] - 16, mid, LANE_X[2] + 16, mid, RULE, 1.0, "3 3")

    d.t(700, y + 12, verdict, 12, c, KR, "start")

d.legend(H - 44, [("끝까지 도착", OK), ("다리에서 폐기", BAD),
                  ("세어지거나 일부만", WARN), ("컨트롤러로 올라감", INFO)])
d.save("05-04.flow-table-states.svg")
print("ok flow-table-states")
