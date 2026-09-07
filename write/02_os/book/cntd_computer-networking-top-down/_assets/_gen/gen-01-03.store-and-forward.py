# 01-03 §1 — 저장 후 전달이 만드는 시간표. 패킷 3개가 링크 2개를 지나면 4L/R 이 걸린다.
# 값 출처: 원문 1.3.1 의 서술과 식 (1.1). 시간 단위는 L/R(패킷 하나를 링크에 밀어 넣는 시간).
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 시간 축 + 행마다 막대 하나, 국면별 zone 묶음.
#           축약: 행이 작업이 아니라 (패킷 × 링크) 점유 구간이고 축 단위가 주가 아니라 L/R 이다.
#           문법(행 × 시간축 × 막대 하나)은 그대로 쓰고 의미만 갈아 끼운다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 980, 500
LX, TX0, TX1 = 20, 200, 930
ROW_H, BAR_H, Y0 = 40, 24, 136
UNITS = 4
PITCH = (TX1 - TX0) / UNITS

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 01-03 §1",
      "저장 후 전달이 만드는 시간표",
      "패킷 세 개가 라우터 하나를 거쳐 목적지로 간다. 라우터는 패킷 전체를 받아야 첫 비트를 내보낼 수 있으므로 링크마다 L/R 씩 밀린다. 마지막 패킷이 도착하는 시각이 4L/R 이다.",
      "가로 한 칸이 L/R 입니다 — 길이 L 비트를 속도 R 인 링크에 밀어 넣는 시간")

# 시간 축
for i in range(UNITS + 1):
    x = TX0 + i * PITCH
    d.line(x, 120, x, Y0 + 6 * ROW_H, RULE, 0.8)
    lab = "0" if i == 0 else ("L/R" if i == 1 else f"{i}L/R")
    d.t(x, 112, lab, 11, MUTED, MONO)
d.line(TX0, 120, TX1, 120, RULE, 1.0)

ZONES = [("링크 1 · 출발지 → 라우터", 0, 3), ("링크 2 · 라우터 → 목적지", 3, 3)]
for name, start, n in ZONES:
    zy = Y0 + start * ROW_H
    d.box(TX0 - 188, zy - 4, W - 40 - (TX0 - 188), n * ROW_H, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, zy + 14, name, 11, SOFT, KR, "start", 600)

ROWS = [
    ("패킷 1", 0, 1, 0, False), ("패킷 2", 1, 2, 1, False), ("패킷 3", 2, 3, 2, False),
    ("패킷 1", 1, 2, 3, False), ("패킷 2", 2, 3, 4, False), ("패킷 3", 3, 4, 5, True),
]
for name, s, e, i, focal in ROWS:
    y = Y0 + i * ROW_H
    d.t(LX + 4, y + 32, name, 11, INK, KR, "start", 600)
    x, w = TX0 + s * PITCH, (e - s) * PITCH
    if focal: d.tone(x, y + 12, w, BAR_H, ACC, 4)
    else: d.box(x, y + 12, w, BAR_H, PAPER, MUTED, 1.0, 4)
    d.t(x + w / 2, y + 28, f"{s}L/R → {e}L/R" if s else "0 → L/R", 11, ACC if focal else MUTED, MONO)

BOT = Y0 + 6 * ROW_H
d.t(LX, BOT + 32, "링크 N 개를 지나는 패킷 하나는 N·L/R 이 걸립니다(식 1.1). 패킷 P 개라면 (N + P − 1)·L/R 이고, 여기서는 N=2·P=3 이라 4L/R 입니다",
     11, MUTED, KR, "start")

d.legend(H - 60, [("마지막 패킷이 도착하는 구간", ACC), ("나머지 점유 구간", MUTED)])
d.save("01-03.store-and-forward.svg")
