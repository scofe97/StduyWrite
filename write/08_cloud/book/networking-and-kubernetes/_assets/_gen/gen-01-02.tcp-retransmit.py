# 01-02.tcp-retransmit — 조각 하나가 빠지면 재전송과 순서 재조립이 함께 일어난다
# 본문 요구(01-02 §2 "조각이 빠질 때"): "가운데 줄에서 화살표가 이어지지 않는 자리가 유실"이라고
#           본문이 그림의 규격을 못 박는다 — 그래서 유실 세그먼트만 화살표가 중간에서 끊기고 X 로
#           끝난다. 그리고 "두 가지가 함께 일어난다" — 빠진 조각만 다시 오고(재전송), 그 사이 뒤에
#           도착한 것은 앱으로 못 올라간다(순서 재조립). 오른쪽 세로 막대가 그 붙들린 구간이라
#           본문의 "받는 쪽 막대가 그 붙들고 있는 구간입니다"와 짝이 맞는다.
#           ACK 101 이 세 번 되풀이되는 것도 본문이 짚는 대목이라 (중복 1)(중복 2) 를 라벨에 적었다.
# 타입 스펙: type-sequence.md — 주체 둘 사이의 시간순 메시지. 세로가 시간, 가로가 주체다.
#           상태가 아니라 오간 것 자체가 논지라 state 칩 대신 메시지 부제로 의미를 실었다.
# 이력: 2026-08-28 신설. 생성기 없이 손으로 만들어진 SVG 였다. 값·좌표를 그대로 옮겼다.
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 980, 752
Y0, STRIDE, RAIL_BOT = 196, 52, 682

d = Seq(W, H, "SEQUENCE · 01-02 TCP RETRANSMIT",
        "조각 하나가 빠지면 — 재전송과 순서 재조립",
        "TCP 재전송과 순서 재조립. seq=101 세그먼트가 유실되면 이후 세그먼트가 도착해도 ACK는 "
        "101에 머물고, 같은 ACK가 세 번 쌓이면 송신 측은 타임아웃을 기다리지 않고 곧바로 재전송한다. "
        "받는 쪽은 앞이 채워질 때까지 뒤 데이터를 앱으로 올리지 못하고 버퍼에 붙들고 있다.",
        lead="화살표가 이어지지 않는 자리가 유실입니다 — 그동안 뒤엣것은 앱으로 못 올라갑니다.")

LX, RX = d.lanes([("보내는 쪽", "sender"), ("받는 쪽", "receiver")]).values()
d.rails(RAIL_BOT)
MID = (LX + RX) / 2

# 유실 화살표는 절반쯤에서 끊고 X 로 닫는다 — 나머지는 레인에서 레인으로 잇는다.
LOST_END, XA, XB = 518.0, 524.0, 540.0

MSGS = [(1, "seq=1  (100B)",    "정상 도착",                            OK,   "ok",   1.5, None),
        (0, "ACK 101",          "1~100 받았다 · 101부터 기다린다",       INFO, "info", 1.3, "4 4"),
        (1, "seq=101 (100B)",   "유실 — 도착하지 않는다",                BAD,  None,   1.6, "7 5"),
        (1, "seq=201 (100B)",   "도착했지만 앞이 비었다",                WARN, "warn", 1.5, None),
        (0, "ACK 101  (중복 1)", "번호가 바뀌지 않는다",                  INFO, "info", 1.3, "4 4"),
        (1, "seq=301 (100B)",   "도착했지만 앞이 비었다",                WARN, "warn", 1.5, None),
        (0, "ACK 101  (중복 2)", "셋째가 쌓이면 즉시 재전송",             INFO, "info", 1.3, "4 4"),
        (1, "seq=101  재전송",   "타임아웃을 기다리지 않는다 (fast retransmit)", ACC, "acc", 1.6, None),
        (0, "ACK 401",          "201·301 까지 한꺼번에 확인된다",        OK,   "ok",   1.3, "4 4")]

for i, (fwd, label, sub, c, mk, sw, dash) in enumerate(MSGS):
    y = Y0 + STRIDE * i
    if mk is None:                      # 유실 — 중간에서 끊고 X
        d.path(f"M {LX+10} {y} L {LOST_END} {y}", c, sw, dash=dash)
        d.line(XA, y - 11, XB, y + 11, c, 2.2)
        d.line(XB, y - 11, XA, y + 11, c, 2.2)
    elif fwd:
        d.path(f"M {LX+10} {y} L {RX-12} {y}", c, sw, m=mk, dash=dash)
    else:
        d.path(f"M {RX-10} {y} L {LX+12} {y}", c, sw, m=mk, dash=dash)
    d.t(MID, y - 9, label, 11, c, MONO, "middle", 600)
    d.t(MID, y + 15, sub, 9, MUTED)

# 붙들린 구간 — seq=201 이 도착한 줄부터 재전송이 도착할 때까지
HOLD_Y0, HOLD_H = 316, 228
d.o.append(f'<rect x="{RX+26}" y="{HOLD_Y0}" width="20" height="{HOLD_H}" rx="10" '
           f'fill="{WARN}2E" stroke="{WARN}" stroke-width="1.3"/>')
d.t(RX + 58, HOLD_Y0 + HOLD_H / 2 - 6, "버퍼에 붙들린 구간", 10, WARN, KR, "start")
d.t(RX + 58, HOLD_Y0 + HOLD_H / 2 + 10, "앱으로 못 올라간다", 9, MUTED, KR, "start")

d.legend(708, [("정상 도착", OK), ("유실", BAD), ("순서 대기", WARN),
               ("중복 ACK", INFO), ("재전송", ACC)])
d.save("01-02.tcp-retransmit.svg")
print("ok tcp-retransmit")
