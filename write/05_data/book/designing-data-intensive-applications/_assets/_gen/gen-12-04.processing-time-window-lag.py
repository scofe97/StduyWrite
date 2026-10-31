# 12-04 §1 — 이벤트 시간 vs 처리 시간: 스트림 프로세서 재시작에 따른 처리 시간 윈도우의 집계 왜곡.
# 사실 출처: 12-04 본문 §1(L26~L42), DDIA 2판 Ch.12 "Event time versus processing time" (PDF p.41~42) 및 Figure 12-8.
# Figure 12-8 의 세로축 눈금은 10 하나뿐이다. rates_pt 의 급등 높이는 그림에서 읽은 모양이고 수치 라벨로 쓰지 않는다.
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO, BAD

W = 880
BANNER_Y = 104
BANNER_H = 36
Y0 = 156
LEG = 512
H = LEG + 52

d = D(W, H, "12-04 · §1 REASONING ABOUT TIME", "처리 시간 기준 윈도우의 처리율 왜곡",
      "DDIA 2판 Figure 12-8: 웹 서버의 실제 요청률은 초당 10건으로 일정하지만, 스트림 프로세서 재시작 시 처리 시간 기준 윈도우가 인위적 급등 스파이크를 발생시키는 구조를 보인다.",
      "프로세서 1분 재시작 · 누적 백로그 일시 처리 · 인위적 스파이크 왜곡 · 이벤트 시간 결정론성")

# 상단 배경 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "원서 Figure 12-8 대조: 실제 요청률은 일정하나 프로세서 재시작 후 백로그 처리가 인위적 스파이크 왜곡을 유발", 11.5, INK, KR, "middle", 600)

# 타임라인 좌표계 정의
T_X0 = 240
T_W = 600
N_SLOTS = 7
DX = T_W / N_SLOTS

# 시간축 눈금선 (t0 ~ t7)
time_labels = ["t0", "t1", "t2", "t3 (재시작)", "t4", "t5 (급속처리)", "t6", "t7"]
for idx, lab in enumerate(time_labels):
    gx = T_X0 + idx * DX
    d.line(gx, Y0, gx, Y0 + 268, RULE, 0.8, "3 4")
    d.t(gx, Y0 + 282, lab, 11, MUTED, MONO, "middle")

# 1. 웹 서버 트랙 (요청 생성)
y_ws = Y0 + 8
d.box(28, y_ws - 4, 196, 44, PAPER2, RULE, 1.0)
d.t(126, y_ws + 16, "웹 서버 (요청 생성)", 12, INK, KR, "middle", 600)
d.t(126, y_ws + 33, "초당 10건 일정 속도 발생", 11, OK, KR, "middle")

for idx in range(N_SLOTS):
    sx = T_X0 + idx * DX
    for k in range(5):
        rx = sx + 8 + k * 14
        d.box(rx, y_ws + 4, 9, 28, PAPER, OK, 0.8, 2)

# 2. 스트림 프로세서 트랙 (처리 진행)
y_sp = Y0 + 64
d.box(28, y_sp - 4, 196, 48, PAPER2, RULE, 1.0)
d.t(126, y_sp + 18, "스트림 프로세서 (처리)", 12, INK, KR, "middle", 600)
d.t(126, y_sp + 36, "큐 소비 및 윈도우 집계", 11, MUTED, KR, "middle")

# t0 ~ t2: 정상 처리
for idx in [0, 1]:
    sx = T_X0 + idx * DX
    for k in range(5):
        rx = sx + 8 + k * 14
        d.box(rx, y_sp + 6, 9, 28, PAPER, INFO, 0.8, 2)

# t2 일부 처리 후 재시작 돌입
sx2 = T_X0 + 2 * DX
for k in range(2):
    rx = sx2 + 8 + k * 14
    d.box(rx, y_sp + 6, 9, 28, PAPER, INFO, 0.8, 2)

# t3: 1분 재시작 구간 (Restart)
restart_x = T_X0 + 2.5 * DX
restart_w = DX * 1.35
d.tone(restart_x, y_sp + 4, restart_w, 32, WARN, 4, "22", 1.2)
d.t(restart_x + restart_w / 2, y_sp + 24, "1분 재시작", 11, WARN, KR, "middle", 600)

# t4 ~ t6: 누적 백로그 급속 처리 (Catch-up)
for idx in [4, 5]:
    sx = T_X0 + idx * DX
    for k in range(8):
        rx = sx + 4 + k * 10
        d.box(rx, y_sp + 6, 7, 28, PAPER, ACC, 0.8, 2)

# t6 ~ t7: 정상화
sx6 = T_X0 + 6 * DX
for k in range(5):
    rx = sx6 + 8 + k * 14
    d.box(rx, y_sp + 6, 9, 28, PAPER, INFO, 0.8, 2)

# 3. 처리 시간 기준 측정율 트랙 (인위적 왜곡)
y_pt = Y0 + 126
d.box(28, y_pt - 4, 196, 64, PAPER2, WARN, 1.0)
d.t(126, y_pt + 18, "처리 시간 기준 측정율", 12, WARN, KR, "middle", 600)
d.t(126, y_pt + 36, "초당 처리 건수 윈도우 집계", 11, MUTED, KR, "middle")
d.t(126, y_pt + 53, "재시작 직후 인위적 급등", 11, WARN, KR, "middle")

rates_pt = [10, 10, 7, 0, 5, 18, 18, 12]
base_y = y_pt + 54
scale = 2.1

pts_pt = []
for idx, r in enumerate(rates_pt):
    px = T_X0 + idx * DX
    py = base_y - r * scale
    pts_pt.append((px, py))

# 왜곡 곡선 그리기
for i in range(len(pts_pt) - 1):
    c_line = WARN if i in [3, 4, 5] else INFO
    d.line(pts_pt[i][0], pts_pt[i][1], pts_pt[i+1][0], pts_pt[i+1][1], c_line, 1.8)

for px, py in pts_pt:
    d.o.append(f'<circle cx="{px}" cy="{py}" r="3.5" fill="{PAPER}" stroke="{WARN}" stroke-width="1.5"/>')

# 스파이크 라벨 콜아웃
d.chip(T_X0 + 3.8 * DX, y_pt + 2, "백로그 처리 중 인위적 급등", WARN, 11)

# 4. 실제 요청률 트랙 (이벤트 시간 기준)
y_et = Y0 + 204
d.box(28, y_et - 4, 196, 52, PAPER2, OK, 1.0)
d.t(126, y_et + 20, "실제 요청률 (이벤트 시간)", 12, OK, KR, "middle", 600)
d.t(126, y_et + 39, "페이로드 타임스탬프 집계", 11, MUTED, KR, "middle")

pts_et = [(T_X0 + idx * DX, y_et + 28) for idx in range(N_SLOTS + 1)]
for i in range(len(pts_et) - 1):
    d.line(pts_et[i][0], pts_et[i][1], pts_et[i+1][0], pts_et[i+1][1], OK, 2.0)
for px, py in pts_et:
    d.o.append(f'<circle cx="{px}" cy="{py}" r="3.5" fill="{PAPER}" stroke="{OK}" stroke-width="1.5"/>')

d.chip(T_X0 + 3.5 * DX, y_et + 10, "실제 요청률 불변 (초당 10건 유지)", OK, 11)

# 하단 비교 패널
PANEL_Y = Y0 + 296
PANEL_W = (W - 56 - 16) / 2
d.box(28, PANEL_Y, PANEL_W, 48, PAPER2, RULE, 1.0)
d.t(28 + PANEL_W / 2, PANEL_Y + 19, "처리 시간 윈도우 한계", 11.5, WARN, KR, "middle", 600)
d.t(28 + PANEL_W / 2, PANEL_Y + 36, "큐 백로그 일시 처리로 인한 인위적 스파이크 왜곡 유발", 11, MUTED, KR, "middle")

d.box(28 + PANEL_W + 16, PANEL_Y, PANEL_W, 48, PAPER2, RULE, 1.0)
d.t(28 + PANEL_W + 16 + PANEL_W / 2, PANEL_Y + 19, "이벤트 시간 윈도우 해결", 11.5, OK, KR, "middle", 600)
d.t(28 + PANEL_W + 16 + PANEL_W / 2, PANEL_Y + 36, "페이로드 타임스탬프로 발생 시점 버킷 집계 및 결정론성 보장", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("실제 요청률", OK),
    ("스파이크 왜곡", WARN),
    ("백로그 처리", ACC),
    ("정상 처리", INFO)
])

d.save("12-04.processing-time-window-lag.svg")
