# 타입 스펙: type-gantt — 면접 네 단계의 걸리는 분을 막대 길이로 그린다. 진한 구간이 하한, 옅은 구간이 하한에서 상한까지 늘어나는 폭이다.
# 사실 출처: 추출본 v2.txt 849~852행(범위 확정 3~10분 · 개략 설계 10~15분 · 상세 설계 10~25분 · 마무리 3~5분, 45분 면접 기준 러프한 안내)
# Layout conventions: 라벨 열 x=24~200, 타임라인 x=220~920(분당 28px, 0~25분), 행 stride 80(y=152·232·312·392), 막대 높이 32(행 +16), 눈금 y=120, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 520
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 03-01",
      "네 단계가 45분 면접에서 걸리는 분",
      "범위 확정은 3~10분, 개략 설계는 10~15분, 상세 설계는 10~25분, 마무리는 3~5분이다. 상세 설계의 폭이 가장 넓다.",
      "진한 막대는 하한, 옅은 막대는 상한까지 늘어나는 폭")

X0, PITCH = 220, 28
ROWS = (152, 232, 312, 392)
BH = 32

# 눈금
for m in range(0, 26, 5):
    x = X0 + m * PITCH
    d.line(x, 128, x, 440, RULE, 0.8, "3 6")
    d.t(x, 116, f"{m}분", 13, SOFT, MONO)

PHASES = (
    ("범위 확정", "질문 · 가정 기록", 3, 10, INFO),
    ("개략 설계", "박스 · 어림셈 · 합의", 10, 15, INFO),
    ("상세 설계", "고른 구성 요소", 10, 25, ACC),
    ("마무리", "병목 · 장애 · 확장", 3, 5, INFO),
)
for y, (name, sub, lo, hi, c) in zip(ROWS, PHASES):
    d.t(24, y + 14, name, 14, INK, KR, "start", 600)
    d.t(24, y + 34, sub, 13, MUTED, KR, "start")
    by = y + 8
    d.tone(X0, by, hi * PITCH, BH, c, 4, "10", 1.0)
    d.tone(X0, by, lo * PITCH, BH, c, 4, "40", 1.2)
    d.t(X0 + lo * PITCH - 8, by + 21, f"{lo}분", 13, INK, MONO, "end", 600)
    d.t(X0 + hi * PITCH - 8, by + 21, f"{hi}분", 13, c, MONO, "end", 600)

d.legend(H - 56, [("단계별 분 범위", INFO), ("가장 넓은 단계", ACC)])
d.save("03-01.chapter-overview.svg")
