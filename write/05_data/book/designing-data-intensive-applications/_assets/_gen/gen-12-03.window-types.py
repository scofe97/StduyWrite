# 12-03 세부 도식 — 윈도우 유형별 시간축 구간 비교
# 사실 출처: 12-03 본문 §3(L46~L65), 원서 p.44~45(10:03:39·10:08:12 예시, 호핑 10:03:00~10:07:59/10:04:00~10:08:59, 세션 30분)
# 원서: DDIA 2nd Edition Ch. 12 "Types of windows" (p.44~45)
# 타입 스펙: type-gantt
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 540

d = D(W, H, "12-03 · SECTION 3", "윈도우 유형별 시간축 구간 비교",
      "동일한 시간축(10:03~10:09)과 두 이벤트(e1, e2)에 대한 4가지 윈도우 분할 메커니즘",
      "텀블링 고정 분할 · 호핑 중첩 평활화 · 슬라이딩 간격 버퍼 · 세션 비활동 감지")

# 시간축 파라미터
AXIS_Y = 120
T_START_X = 232
PITCH = 100  # 1분 = 100px
TICKS = [
    ("10:03", T_START_X),
    ("10:04", T_START_X + 100),
    ("10:05", T_START_X + 200),
    ("10:06", T_START_X + 300),
    ("10:07", T_START_X + 400),
    ("10:08", T_START_X + 500),
    ("10:09", T_START_X + 600),
]

# 시간축 눈금선 및 라벨
d.line(T_START_X - 12, AXIS_Y, T_START_X + 612, AXIS_Y, RULE, 1.0)
for lab, tx in TICKS:
    d.line(tx, AXIS_Y - 4, tx, AXIS_Y + 4, SOFT, 1.0)
    d.t(tx, AXIS_Y - 8, lab, 11, SOFT, MONO, "middle")

# 원서 예시 이벤트 좌표 (DDIA p.45)
# e1: 10:03:39 -> 39/60 = 0.65 -> x = 232 + 65 = 297
# e2: 10:08:12 -> 12/60 = 0.20 -> x = 732 + 20 = 752
E1_X = 297
E2_X = 752

# 이벤트 수직 가이드선 (점선)
for ex, elab, ec in [(E1_X, "e1: 10:03:39", INFO), (E2_X, "e2: 10:08:12", OK)]:
    d.line(ex, AXIS_Y + 6, ex, 388, RULE, 1.0, "3,3")
    d.chip(ex, AXIS_Y + 12, elab, ec, 11)

# 두 이벤트 간 시간 차이 표시 (4분 33초 < 5분) - 텍스트와 선 간격 8px 확보
d.t((E1_X + E2_X) / 2, AXIS_Y + 24, "이벤트 간격 4분 33초 (< 5분)", 11, ACC, KR, "middle", 600)
d.line(E1_X + 16, AXIS_Y + 32, E2_X - 16, AXIS_Y + 32, ACC, 1.0)

ROWS = [
    ("텀블링 윈도우", "1분 고정 · 비중첩", INFO, 156),
    ("호핑 윈도우", "5분 고정 · 1분 hop", OK, 216),
    ("슬라이딩 윈도우", "5분 간격 버퍼 (focal)", ACC, 276),
    ("세션 윈도우", "30분 비활동 감지", WARN, 336),
]

for name, sub, c, ry in ROWS:
    # 좌측 라벨 칼럼
    d.box(24, ry, 188, 48, PAPER2, RULE, 0.8)
    d.t(36, ry + 20, name, 12, c, KR, "start", 600)
    d.t(36, ry + 38, sub, 11, MUTED, KR, "start")

# Row 0: 텀블링 1분 윈도우 6개
RY0 = 156
for i in range(6):
    bx = T_START_X + i * 100
    is_e1_or_e2 = (i == 0 or i == 5)
    c_win = INFO if is_e1_or_e2 else SOFT
    d.box(bx + 2, RY0 + 8, 96, 32, PAPER2, c_win, 0.9 if is_e1_or_e2 else 0.6)
    d.t(bx + 50, RY0 + 28, f"W{i+1} (1분)", 11, INK if is_e1_or_e2 else MUTED, MONO, "middle")

# Row 1: 호핑 5분 윈도우 2개 (1분 hop 중첩)
RY1 = 216
# Hop 1: 10:03~10:08 (w=500, e1 포함, e2 미포함)
d.box(T_START_X + 2, RY1 + 4, 500 - 4, 20, PAPER2, OK, 0.9)
d.t(T_START_X + 250, RY1 + 18, "호핑 W1: 10:03:00 ~ 10:07:59 (5분, e1 포함 · e2 제외)", 11, INK, KR, "middle")
# Hop 2: 10:04~10:09 (w=500, e1 미포함, e2 포함)
d.box(T_START_X + 100 + 2, RY1 + 26, 500 - 4, 20, PAPER2, OK, 0.9)
d.t(T_START_X + 100 + 250, RY1 + 40, "호핑 W2: 10:04:00 ~ 10:08:59 (5분, e1 제외 · e2 포함)", 11, INK, KR, "middle")

# Row 2: 슬라이딩 5분 윈도우 (FOCAL!)
# e1 기준 5분 구간: 10:03:39 ~ 10:08:39 (x = 297 to 797)
RY2 = 276
d.tone(E1_X, RY2 + 6, 500, 36, ACC, 4, "22", 1.4)
d.t(E1_X + 250, RY2 + 24, "슬라이딩 5분 버퍼: e1과 e2 동시 포함 (간격 4분 33초 < 5분)", 12, ACC, KR, "middle", 600)
d.t(E1_X + 250, RY2 + 38, "10:03:39 ~ 10:08:39 시간 간격 버퍼 유지", 11, INK, KR, "middle")

# Row 3: 세션 윈도우
RY3 = 336
# e1 ~ e2 활성 세션 구간
d.tone(E1_X, RY3 + 6, E2_X - E1_X, 36, WARN, 4, "16", 1.0)
d.t((E1_X + E2_X) / 2, RY3 + 24, "사용자 활성 세션 (e1 ~ e2 연속 활동)", 11, WARN, KR, "middle", 600)
# e2 이후 30분 비활동 대기 구간 (폭 104px 확보로 글자 넘침 방지)
d.box(E2_X, RY3 + 6, 104, 36, PAPER, RULE, 0.8)
d.t(E2_X + 52, RY3 + 24, "30분 비활동 대기", 11, MUTED, KR, "middle")

# 하단 비교 요약 패널
PANEL_Y = 404
d.tone(24, PANEL_Y, W - 48, 48, INFO, 4, "10", 0.9)
d.t(W / 2, PANEL_Y + 20, "원서 대목 (p.45): 고정 경계(텀블링·호핑)는 e1·e2를 분리하나, 슬라이딩 윈도우는 두 이벤트를 동일 창에 포섭", 11, INK, KR, "middle", 600)
d.t(W / 2, PANEL_Y + 38, "구현 특성: 텀블링(분 내림) · 호핑(1분 텀블링 집계 결합) · 슬라이딩(정렬 버퍼 만료) · 세션(비활동 타임아웃)", 11, MUTED, KR, "middle")

# 범례
LEG = 472
legend_items = [
    ("텀블링 (비중첩 고정)", INFO),
    ("호핑 (중첩 평활화)", OK),
    ("슬라이딩 (간격 버퍼, focal)", ACC),
    ("세션 (비활동 종료)", WARN),
]
d.line(24, LEG, W - 24, LEG, RULE, 0.8)
d.t(24, LEG + 22, "LEGEND", 8, SOFT, MONO, "start")
lx = 80
for lab, c in legend_items:
    d.o.append(f'<rect x="{lx}" y="{LEG + 12}" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    d.t(lx + 20, LEG + 22, lab, 11, MUTED, KR, "start")
    w_text = sum(11 if "가" <= ch <= "힣" else 7 for ch in lab)
    lx += 26 + w_text + 16

d.save("12-03.window-types.svg")
