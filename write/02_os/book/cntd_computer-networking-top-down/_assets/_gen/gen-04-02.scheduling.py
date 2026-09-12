# 04-02 §4 — 원문 Figure 4.12·4.14·4.15. 같은 도착 순서에 규율만 바꾸면 나가는 순서가 달라진다.
# 도착 시각과 클래스 배정, 전송에 세 단위가 걸린다는 가정은 원문 예 그대로다.
#   우선순위: 1·3·4 가 높은 클래스, 2·5 가 낮은 클래스 · 비선점
#   라운드 로빈: 1·2·4 가 클래스 1, 3·5 가 클래스 2
# 타입 스펙: type-timeline — 시간 축 위의 사건. 세 규율을 같은 축에 나란히 놓아 순서 차이를 본다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 600
TX0, TX1, TMAX = 190, 950, 18
ROWS = [("도착", 168), ("FIFO", 240), ("우선순위", 322), ("라운드 로빈", 404)]

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §4",
      "규율만 바꾸면 순서가 달라집니다",
      "원문의 세 그림을 같은 시간 축에 얹은 것. 도착 순서는 같고 나가는 순서만 규율에 따라 갈린다.",
      "전송에 세 단위가 걸리고 도착은 1·2·3·4·5 순입니다")

def xp(t): return TX0 + t / TMAX * (TX1 - TX0)

for g in range(0, TMAX + 1, 3):
    d.line(xp(g), 140, xp(g), 448, RULE, 0.7)
    d.t(xp(g), 132, str(g), 12, MUTED, MONO)
d.line(TX0, 140, TX1, 140, RULE, 1.0)
for name, y in ROWS:
    d.t(20, y + 22, name, 12, INK, KR, "start", 600)

ARRIVE = [(0, "1"), (1, "2"), (2, "3"), (5, "4"), (14, "5")]
for t, lab in ARRIVE:
    d.path(f"M {xp(t)} {ROWS[0][1] + 34} L {xp(t)} {ROWS[0][1] + 8}", MUTED, 1.3, m="ar")
    d.t(xp(t), ROWS[0][1] + 48, lab, 12, INK, MONO)

def bar(row_y, s, lab, c, focal=False):
    x, w = xp(s), xp(3) - xp(0)
    if focal: d.tone(x + 2, row_y + 6, w - 4, 30, c, 4)
    else: d.box(x + 2, row_y + 6, w - 4, 30, PAPER2, c, 1.0, 4)
    d.t(x + w / 2, row_y + 26, lab, 12, c if focal else INK, MONO, "middle", 600)

for s, lab in [(0, "1"), (3, "2"), (6, "3"), (9, "4"), (14, "5")]:
    bar(ROWS[1][1], s, lab, MUTED)
d.t(xp(12) + 8, ROWS[1][1] + 26, "링크가 놉니다", 12, SOFT, KR, "start")

for s, lab, hi in [(0, "1", True), (3, "3", True), (6, "2", False), (9, "4", True), (14, "5", False)]:
    bar(ROWS[2][1], s, lab, ACC if hi else MUTED, hi)
d.t(xp(9) + 4, ROWS[2][1] - 6, "높은 우선순위인 4 가 2 를 끊지 못합니다 — 비선점", 12, SOFT, KR, "start")

for s, lab, c1 in [(0, "1", True), (3, "3", False), (6, "2", True), (9, "4", True), (14, "5", False)]:
    bar(ROWS[3][1], s, lab, INFO if c1 else OK, True)
d.t(xp(3) + 4, ROWS[3][1] + 52, "클래스를 번갈아 — 3 이 2 보다 먼저 나갑니다", 12, SOFT, KR, "start")

d.t(20, 492, "WFQ 는 라운드 로빈을 일반화해 클래스마다 가중치를 줍니다. 클래스 i 는 최소한 R × w_i / Σw_j 를 받습니다.",
     11, MUTED, KR, "start")
d.t(20, 514, "넷 다 일 보존 규율이라 보낼 패킷이 있는 한 링크를 놀리지 않습니다. FIFO 의 빈 구간은 보낼 것이 없어서입니다.",
     11, MUTED, KR, "start")

d.legend(H - 44, [("높은 우선순위", ACC), ("클래스 1", INFO), ("클래스 2", OK), ("구분 없음", MUTED)])
d.save("04-02.scheduling.svg")
