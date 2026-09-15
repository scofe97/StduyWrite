# 02-02 §2 — 비지속 연결과 지속 연결이 쓰는 왕복 수. 값은 원문 2.2.2 의 회계 그대로다.
# 원문 예는 객체 11개지만 행이 22개가 되어 읽히지 않으므로 기반 HTML + 이미지 2장으로 줄였다.
# 객체당 2 RTT 라는 규칙은 그대로이므로 11개로 늘리면 22 RTT 대 3 RTT 가 된다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대 하나, 국면별 zone 묶음.
#           축약: 행이 작업이 아니라 왕복 점유 구간이고, 축 단위가 주가 아니라 RTT 다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 812
LX, TX0, TX1 = 20, 258, 952
ROW_H, BAR_H = 48, 24        # 행 48 · 막대 24 — 위아래로 12px 씩 숨 쉴 자리를 둔다
ZONE_HEAD, ZONE_GAP = 40, 20  # zone 제목이 첫 행 라벨과 붙지 않도록 머리 밴드를 따로 둔다
Y0 = 156
UNITS = 6
PITCH = (TX1 - TX0) / UNITS

ZONES = [("비지속 연결 — 객체마다 새 TCP 연결", 6), ("지속 연결 — 연결 하나를 계속", 3)]
Z1_Y = Y0
Z1_H = ZONE_HEAD + 6 * ROW_H                      # 328
Z2_Y = Z1_Y + Z1_H + ZONE_GAP                     # 504
Z2_H = ZONE_HEAD + 3 * ROW_H                      # 184
BOT = Z2_Y + Z2_H                                 # 688

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 02-02 §2",
      "왕복을 세어 보면",
      "기반 HTML 하나와 이미지 두 장을 받을 때 두 방식이 쓰는 왕복 수. 비지속 연결은 객체마다 연결을 새로 세우고, 지속 연결은 한 번 세운 연결을 계속 쓴다.",
      "가로 한 칸이 1 RTT 입니다 — 작은 패킷이 갔다 돌아오는 시간")

for i in range(UNITS + 1):
    x = TX0 + i * PITCH
    d.line(x, 126, x, BOT, RULE, 0.8)
    d.t(x, 118, "0" if i == 0 else f"{i} RTT", 13, MUTED, MONO)
d.line(TX0, 126, TX1, 126, RULE, 1.0)
d.t(20, 118, "왕복 점유 구간", 13, SOFT, KR, "start")

for (name, n), zy, zh in ((ZONES[0], Z1_Y, Z1_H), (ZONES[1], Z2_Y, Z2_H)):
    d.box(20, zy, W - 44, zh, PAPER2, RULE, 0.8, 6)
    d.t(LX + 8, zy + 26, name, 13, SOFT, KR, "start", 600)

# (라벨, 시작 RTT, 끝 RTT, zone 안 행 번호, 색, focal)
ROWS = [
    (Z1_Y, "TCP 연결 · HTML",      0, 1, 0, INFO, False),
    (Z1_Y, "요청·응답 · HTML",     1, 2, 1, MUTED, False),
    (Z1_Y, "TCP 연결 · 이미지 1",  2, 3, 2, INFO, False),
    (Z1_Y, "요청·응답 · 이미지 1", 3, 4, 3, MUTED, False),
    (Z1_Y, "TCP 연결 · 이미지 2",  4, 5, 4, INFO, False),
    (Z1_Y, "요청·응답 · 이미지 2", 5, 6, 5, MUTED, True),
    (Z2_Y, "TCP 연결 · 한 번만",   0, 1, 0, INFO, False),
    (Z2_Y, "요청·응답 · HTML",     1, 2, 1, MUTED, False),
    (Z2_Y, "요청·응답 · 이미지 둘", 2, 3, 2, MUTED, True),
]
for zy, name, s, e, i, col, focal in ROWS:
    y = zy + ZONE_HEAD + i * ROW_H
    d.t(LX + 8, y + 32, name, 13, INK, KR, "start", 600)
    x, w = TX0 + s * PITCH, (e - s) * PITCH
    if focal:
        d.tone(x, y + 12, w, BAR_H, ACC, 4)
    else:
        d.box(x, y + 12, w, BAR_H, PAPER, col, 1.0, 4)
    d.t(x + w / 2, y + 29, f"{s} → {e}", 13, ACC if focal else col, MONO)

d.t(LX, BOT + 32, "객체당 2 RTT 는 연결 수립 1 회와 요청·응답 1 회 · 원문의 객체 11개 예에서는 22 RTT 대 3 RTT 가 됨",
    13, MUTED, KR, "start")
d.t(LX, BOT + 56, "마지막 줄이 파이프라이닝입니다 — 앞 답을 기다리지 않고 두 요청을 연달아 보냄",
    13, MUTED, KR, "start")

d.legend(H - 48, [("마지막 객체가 도착하는 구간", ACC), ("연결 수립", INFO), ("요청·응답", MUTED)])
d.save("02-02.rtt-accounting.svg")
