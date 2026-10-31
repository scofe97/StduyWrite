# 09-02 §1 — 경과 시간 측정용 단조 시계와 달력 시각 표현용 벽시계의 속성·용도 비교 격자.
# 사실 출처: 09-02 §1(L23~L35), 원서 Ch.9 Monotonic Versus Time-of-Day Clocks
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LX, LW = 24, 140
CX0, CW, GAP = 180, 330, 16
HY, HH = 104, 54
RY0, RSTR, RH = 174, 54, 46
FOCAL = 1

cols = [
    ("벽시계 (Time-of-Day)", "CLOCK_REALTIME · currentTimeMillis", WARN),
    ("단조 시계 (Monotonic)", "CLOCK_MONOTONIC · nanoTime", ACC),
]

rows = [
    ("기준 시각과 의미",
     [("1970-01-01 UTC 기점 에포크 시각", "달력 시각 표현", INFO),
      ("임의 시작점(부팅 후) 나노초", "절댓값 자체는 무의미", INFO)]),
    ("시간 진행과 단조성",
     [("강제 뒤로 점프 가능", "NTP 동기화·윤초·DST 영향", WARN),
      ("항상 앞으로만 단조 증가", "뒤로 되돌려지지 않음", OK)]),
    ("주요 적합 용도",
     [("달력 시각 표현", "직관적인 현재 시각", INFO),
      ("경과 시간 측정 · 타임아웃 · 지연", "두 시점 간의 차이 계산", ACC)]),
    ("시스템 표준 API",
     [("CLOCK_REALTIME / currentTimeMillis", "리눅스 · 자바", INFO),
      ("CLOCK_MONOTONIC / nanoTime", "리눅스 · 자바", INFO)]),
    ("머신 간 비교",
     [("NTP 동기화 필요 (스큐 잔존)", "노드 간 수 ms~수 초 오차", WARN),
      ("다른 컴퓨터와 비교 불가", "단일 로컬 머신 내부 한정", OK)]),
    ("NTP 시간 조정",
     [("강제 리셋 (뒤로 점프)", "서버보다 앞서면 뒤로 이동", WARN),
      ("슬루잉 (slewing) 가감", "진행 주파수 미세 가감만 허용", OK)]),
]

LEG = RY0 + len(rows) * RSTR + 24
H = LEG + 56

d = D(W, H, "09-02 · §1 TWO TYPES OF CLOCKS", "단조 시계와 벽시계의 특성 및 용도 비교",
      "달력 시각 표현을 위한 벽시계와 경과 시간 측정을 위한 단조 시계의 기준점, 단조성, 주요 용도, 표준 API 비교.",
      "단조 시계 vs 벽시계 · 경과 시간 측정 · 불연속 점프 · 단조성 보장 · 로컬 측정 전용")

# 컬럼 헤더
for k, (name, sub, col_c) in enumerate(cols):
    x = CX0 + k * (CW + GAP)
    is_focal = (k == FOCAL)
    d.box(x, HY, CW, HH, PAPER2, ACC if is_focal else RULE, 1.4 if is_focal else 1.0)
    d.t(x + CW / 2, HY + 24, name, 13.5, INK, KR, "middle", 600)
    d.t(x + CW / 2, HY + 42, sub, 11, col_c, MONO)

# 행 데이터
for r, (label, vals) in enumerate(rows):
    y = RY0 + r * RSTR
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.8)
    d.t(LX + LW / 2, y + 27, label, 12, INK, KR, "middle", 600)
    for k, (main_v, sub_v, cell_c) in enumerate(vals):
        x = CX0 + k * (CW + GAP)
        is_focal = (k == FOCAL)
        d.box(x, y, CW, RH, PAPER, ACC if is_focal and cell_c == ACC else RULE, 1.0 if is_focal and cell_c == ACC else 0.7)
        d.t(x + 20, y + 20, main_v, 12, INK, MONO if main_v.isascii() else KR, "start", 600)
        d.t(x + 20, y + 36, sub_v, 11, cell_c, KR, "start")

# 단조 시계 강조 외곽선
fx = CX0 + FOCAL * (CW + GAP)
total_table_h = (RY0 + len(rows) * RSTR) - HY
d.o.append(f'<rect x="{fx - 4}" y="{HY - 4}" width="{CW + 8}" height="{total_table_h + 4}" rx="8" fill="none" stroke="{ACC}" stroke-width="1.6"/>')

d.legend(LEG, [
    ("경과 측정 표준 (focal)", ACC),
    ("안전 단조성", OK),
    ("위험 및 불연속", WARN),
    ("표준 및 용도", INFO),
])

d.save("09-02.monotonic-vs-wall-clock.svg")
