# 타입 스펙: type-process — 이동하는 1분이 이전 창과 현재 창에 걸친 비율을 위에 보이고, 아래 두 줄에서 같은 슬롯(이전 × 겹침 · 현재 · 추정 · 내림 · 한도)의 값이 요청 하나 전후로 바뀌는 것을 계산 칸으로 보인다.
# 사실 출처: 추출본 v2.txt 1105~1114행(분당 7건 · 이전 분 5건 · 현재 분 3건 · 현재 분의 30% 지점 · 3 + 5 × 0.7 = 6.5 · 내림 6 · 한도 7 이므로 통과), PDF 쪽 61 그림(이동 1분 = 이전 70% + 현재 30%).
#   통과 뒤 장면(현재 4건 → 4 + 5 × 0.7 = 7.5 → 내림 7)은 같은 식으로 계산했다. 원문 그림의 "5 requests/min" 표기는 본문의 7건과 달라 본문 값을 따른다.
# Layout conventions: 분 상자 폭 416(이전 x=64 · 현재 x=480) y=104 높이 60, 이동 1분 띠 x=188~604 y=176 높이 36(30% = 124 → 4의 배수 근사), 계산 칸 폭 140 · 간격 48(x=36 부터 stride 188), 줄 y=304·412 높이 64. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 04-01 §7",
      "근사식은 이전 창의 겹친 비율만큼만 센다",
      "한도 분당 7건에서 이전 분 5건 · 현재 분 3건 · 현재 분의 30% 지점이면 이동하는 1분이 이전 분의 70% 를 덮어 3 + 5 × 0.7 = 6.5 이고, 내림한 6 은 한도 7 보다 작아 통과하며 통과 뒤에는 4 + 3.5 = 7.5 로 한도에 닿는다.",
      "한도 분당 7건 · 현재 분의 30% 지점에 도착")

# 분 상자 둘
d.tone(64, 104, 416, 60, INFO, 6, "12", 1.2)
d.t(272, 140, "이전 1분 · 5건", 14, INFO, KR, "middle", 600)
d.tone(480, 104, 416, 60, INFO, 6, "12", 1.2)
d.t(688, 140, "현재 1분 · 3건", 14, INFO, KR, "middle", 600)

# 이동하는 1분 — focal
d.tone(188, 176, 416, 36, ACC, 6, "14", 1.4)
d.t(334, 200, "겹침 70%", 13, ACC, KR, "middle", 600)
d.t(542, 200, "30%", 13, ACC, KR, "middle", 600)
d.line(480, 104, 480, 212, SOFT, 1.0, "4 4")
d.arrow([(604, 244), (604, 216)], MUTED, "ar", 1.4)
d.chip(604, 256, "요청 도착", MUTED, 13)

CW, CH, X0, STRIDE = 140, 64, 36, 188
ROWS = (304, 412)


def cell(x, y, top, val, c, focal=False):
    d.tone(x, y, CW, CH, c, 6, "14" if focal else "12", 1.4 if focal else 1.2)
    d.t(x + CW / 2, y + 24, top, 13, MUTED, KR)
    d.t(x + CW / 2, y + 50, val, 20, c, MONO, "middle", 600)


def op(i, y, sym):
    d.t(X0 + STRIDE * i + CW + 24, y + 40, sym, 18, MUTED, MONO, "middle", 600)


d.t(36, ROWS[0] - 12, "이 요청이 도착했을 때", 13, SOFT, KR, "start", 600)
cell(X0, ROWS[0], "이전 5 × 0.7", "3.5", INFO)
op(0, ROWS[0], "+")
cell(X0 + STRIDE, ROWS[0], "현재", "3", INFO)
op(1, ROWS[0], "=")
cell(X0 + STRIDE * 2, ROWS[0], "추정", "6.5", ACC, True)
op(2, ROWS[0], "→")
cell(X0 + STRIDE * 3, ROWS[0], "내림", "6", INFO)
op(3, ROWS[0], "<")
cell(X0 + STRIDE * 4, ROWS[0], "한도 7", "통과", OK)

d.t(36, ROWS[1] - 12, "통과한 뒤 같은 지점", 13, SOFT, KR, "start", 600)
cell(X0, ROWS[1], "이전 5 × 0.7", "3.5", INFO)
op(0, ROWS[1], "+")
cell(X0 + STRIDE, ROWS[1], "현재", "4", INFO)
op(1, ROWS[1], "=")
cell(X0 + STRIDE * 2, ROWS[1], "추정", "7.5", WARN)
op(2, ROWS[1], "→")
cell(X0 + STRIDE * 3, ROWS[1], "내림", "7", WARN)
op(3, ROWS[1], "=")
cell(X0 + STRIDE * 4, ROWS[1], "한도 7", "도달", WARN)

d.legend(H - 56, [("창 카운터", INFO), ("이동하는 1분", ACC), ("통과", OK), ("한도 도달", WARN)])
d.save("04-01.sliding-counter-calc.svg")
