# 02-02 §2 — 비지속 연결과 지속 연결이 쓰는 왕복 수. 값은 원문 2.2.2 의 회계 그대로다.
# 원문 예는 객체 11개지만 행이 22개가 되어 읽히지 않으므로 기반 HTML + 이미지 2장으로 줄였다.
# 객체당 2 RTT 라는 규칙은 그대로이므로 11개로 늘리면 22 RTT 대 3 RTT 가 된다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대 하나, 국면별 zone 묶음.
#           축약: 행이 작업이 아니라 왕복 점유 구간이고, 축 단위가 주가 아니라 RTT 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 664
LX, TX0, TX1 = 20, 258, 952
ROW_H, BAR_H, Y0 = 38, 22, 156
UNITS = 6
PITCH = (TX1 - TX0) / UNITS

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §2",
      "왕복을 세어 보면",
      "기반 HTML 하나와 이미지 두 장을 받을 때 두 방식이 쓰는 왕복 수. 비지속 연결은 객체마다 연결을 새로 세우고, 지속 연결은 한 번 세운 연결을 계속 쓴다.",
      "가로 한 칸이 1 RTT 입니다 — 작은 패킷이 갔다 돌아오는 시간")

for i in range(UNITS + 1):
    x = TX0 + i * PITCH
    d.line(x, 126, x, Y0 + 9 * ROW_H, RULE, 0.8)
    d.t(x, 118, "0" if i == 0 else f"{i} RTT", 11, MUTED, MONO)
d.line(TX0, 126, TX1, 126, RULE, 1.0)

ZONES = [("비지속 연결 — 객체마다 새 TCP 연결", 0, 6), ("지속 연결 — 연결 하나를 계속", 6, 3)]
for name, start, n in ZONES:
    zy = Y0 + start * ROW_H
    d.box(20, zy - 4, W - 44, n * ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LX + 8, zy + 14, name, 11, SOFT, KR, "start", 600)

ROWS = [
    ("TCP 연결 · HTML",      0, 1, 0, INFO, False),
    ("요청·응답 · HTML",     1, 2, 1, MUTED, False),
    ("TCP 연결 · 이미지 1",  2, 3, 2, INFO, False),
    ("요청·응답 · 이미지 1", 3, 4, 3, MUTED, False),
    ("TCP 연결 · 이미지 2",  4, 5, 4, INFO, False),
    ("요청·응답 · 이미지 2", 5, 6, 5, MUTED, True),
    ("TCP 연결 · 한 번만",   0, 1, 6, INFO, False),
    ("요청·응답 · HTML",     1, 2, 7, MUTED, False),
    ("요청·응답 · 이미지 둘", 2, 3, 8, MUTED, True),
]
for name, s, e, i, col, focal in ROWS:
    y = Y0 + i * ROW_H
    d.t(LX + 8, y + 30, name, 11, INK, KR, "start", 600)
    x, w = TX0 + s * PITCH, (e - s) * PITCH
    if focal:
        d.tone(x, y + 12, w, BAR_H, ACC, 4)
    else:
        d.box(x, y + 12, w, BAR_H, PAPER, col, 1.0, 4)
    d.t(x + w / 2, y + 27, f"{s} → {e}", 11, ACC if focal else col, MONO)

BOT = Y0 + 9 * ROW_H
d.t(LX, BOT + 30, "객체 하나에 2 RTT 가 드는 것은 연결 수립 1 회와 요청·응답 1 회이기 때문입니다. 객체가 11개인 원문 예에서는 22 RTT 대 3 RTT 가 됩니다",
     11, MUTED, KR, "start")
d.t(LX, BOT + 52, "지속 연결의 마지막 줄은 파이프라이닝입니다 — 앞 요청의 답을 기다리지 않고 두 요청을 연달아 보냅니다",
     11, MUTED, KR, "start")

d.legend(H - 48, [("마지막 객체가 도착하는 구간", ACC), ("연결 수립", INFO), ("요청·응답", MUTED)])
d.save("02-02.rtt-accounting.svg")
