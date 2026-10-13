# 타입 스펙: type-timeline — 2:00:00~2:02:00 시각 축에 요청 묶음을 올리고, 창 경계 2:01:00 양쪽 30초에 몰린 5건씩이 한 분 구간 안에서 10건이 되는 것을 보인다.
# 사실 출처: 추출본 v2.txt 1048~1052행(분당 5건 · 2:00:00~2:01:00 5건 · 2:01:00~2:02:00 5건 · 2:00:30~2:01:30 구간 10건), PDF 쪽 59 그림(요청 묶음이 2:00:30~2:01:30 구간 안 양쪽에 5건씩).
# Layout conventions: 시각 축 y=272, 30초 = 208px(2:00:00 x=64 · 2:00:30 x=272 · 2:01:00 x=480 · 2:01:30 x=688 · 2:02:00 x=896), 요청 칸 20 · 간격 24, 창 띠 y=316 높이 40. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 440
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §5",
      "창 경계에서 한 분 안에 10건이 통과한다",
      "분당 5건 한도의 고정 윈도에서 2:00:30~2:01:00 에 5건, 2:01:00~2:01:30 에 5건이 오면 두 창의 카운터는 모두 한도 안이지만 2:00:30~2:01:30 한 분에는 10건이 통과한다.",
      "한도 분당 5건 · 창은 2:01:00 에 초기화")

AX = 272
TICKS = ((64, "2:00:00"), (272, "2:00:30"), (480, "2:01:00"), (688, "2:01:30"), (896, "2:02:00"))

# 두 배 구간 — focal
d.o.append(f'<rect x="272" y="112" width="416" height="168" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 4"/>')
d.chip(480, 96, "10건 · 한도 5건의 2배", ACC, 13)

# 창 경계
d.line(480, 116, 480, 264, SOFT, 1.0, "4 4")
d.line(480, 316, 480, 356, SOFT, 1.0, "4 4")

# 시각 축
d.line(64, AX, 896, AX, MUTED, 1.3)
for x, lab in TICKS:
    d.line(x, AX - 8, x, AX + 8, MUTED, 1.3)
    d.t(x, AX + 28, lab, 12, INK, MONO, "middle")

# 요청 묶음 두 개
for cx in (376, 584):
    for k in range(5):
        d.tone(cx - 10, 244 - 24 * k, 20, 20, OK, 3, "33", 1.1)
    d.t(cx, 136, "5건", 13, OK, KR, "middle", 600)

# 창 띠
d.tone(64, 316, 412, 40, INFO, 6, "14", 1.2)
d.t(270, 341, "창 1 · 카운터 5", 13, INFO, KR, "middle", 600)
d.tone(484, 316, 412, 40, INFO, 6, "14", 1.2)
d.t(690, 341, "창 2 · 카운터 5", 13, INFO, KR, "middle", 600)

d.legend(H - 56, [("통과한 요청", OK), ("고정 윈도", INFO), ("두 배 통과 구간", ACC)])
d.save("04-01.fixed-window-edge.svg")
