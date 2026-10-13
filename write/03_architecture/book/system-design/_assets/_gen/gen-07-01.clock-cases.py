# 타입 스펙: type-flowchart — nextId 의 분기를 네 줄(시계 후퇴 · 같은 밀리초 · 순번 가득 · 새 밀리초)로 펼치고 줄마다 조건 → 계산 → 결과를 실제 값으로 적는다.
# 사실 출처: twitter-archive/snowflake 태그 snowflake-2010 IdWorker.scala L74~L79(후퇴 시 예외, 메시지의 N 은 lastTimestamp − timestamp), L81~L85(같은 밀리초: (sequence + 1) & sequenceMask, 0 이면 tilNextMillis), L86~L88(새 밀리초: sequence = 0),
#   sequenceMask = 2^12 − 1 = 4095. 시각 값 1586451091222 · 1586451091225 는 §6 의 값에서 3 을 뺀 예시.
# Layout conventions: 줄 stride 88(y=116·204·292·380) 카드 높이 64, 열 x=24(폭 280) · 344(폭 280) · 664(폭 272). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, SOFT, INFO, KR, MONO

W, H = 960, 536
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 07-01 §7",
      "시계가 뒤로 가면 ID 를 만들지 않고 거절한다",
      "현재 시각이 마지막 발급 시각보다 3 ms 작으면 예외로 거절하고, 같은 밀리초에 순번이 4095 를 넘으면 다음 밀리초까지 기다린다.",
      "now 는 현재 시각 · last 는 마지막 발급 시각")

COLS = (24, 344, 664)
CW = (280, 280, 272)
for i, h in enumerate(("조건", "계산", "결과")):
    d.t(COLS[i] + 4, 104, h, 13, SOFT, KR, "start", 600)
ROWS = (
    (("now < last", "1586451091222 < 1586451091225", BAD), ("last − now", "= 3", BAD), ("발급 거절", "InvalidSystemClock", BAD), True),
    (("now = last", "순번 7", INFO), ("(7 + 1) & 4095", "= 8", INFO), ("ID 발급", "순번 8", OK), False),
    (("now = last", "순번 4095", INFO), ("(4095 + 1) & 4095", "= 0", INFO), ("다음 ms 까지 대기", "tilNextMillis", WARN), False),
    (("now > last", "새 밀리초", INFO), ("순번", "= 0", INFO), ("ID 발급", "순번 0", OK), False),
)
for r, row in enumerate(ROWS):
    y = 116 + 88 * r
    foc = row[3]
    for i in range(3):
        a, b, c = row[i]
        x = COLS[i]
        d.tone(x, y, CW[i], 64, ACC if foc and i == 0 else c, 6, "14" if foc and i == 0 else "12", 1.4 if foc and i == 0 else 1.0)
        d.t(x + 14, y + 26, a, 14, c if not (foc and i == 0) else ACC, MONO if i < 2 else KR, "start", 600)
        d.t(x + 14, y + 48, b, 12, MUTED, MONO, "start")
        if i < 2:
            d.arrow([(x + CW[i] + 2, y + 32), (COLS[i + 1] - 6, y + 32)], MUTED, "ar", 1.5)
d.legend(H - 56, [("후퇴 거절", BAD), ("같은 · 새 밀리초", INFO), ("발급", OK), ("대기", WARN)])
d.save("07-01.clock-cases.svg")
