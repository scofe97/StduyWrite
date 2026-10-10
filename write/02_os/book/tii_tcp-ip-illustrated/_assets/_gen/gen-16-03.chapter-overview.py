# 타입 스펙: type-timeline — 100초 업로드 동안 일어난 11개 혼잡 사건의 발생 시각과 상태.
# 사실 출처: ch16.txt 1077~2040행 — 사건 1~11의 발생 시각, 상태 전이, cwnd·ssthresh 수치.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-03",
      "100초 업로드 동안 일어난 11개 혼잡 사건",
      "2.5MB 파일 전송 중 로컬 큐 포화, 망 손실 복구, 헛 타임아웃 되돌리기가 다섯 상태를 가로지릅니다.",
      "100초 동안 11번의 혼잡 조절을 겪으며 전송을 마칩니다")

L1_Y = 165
L2_Y = 345
X_START, X_END = 54, W - 54
SPAN = X_END - X_START

# 레일
d.line(X_START, L1_Y, X_END, L1_Y, RULE, 1.5)
d.line(X_START, L2_Y, X_END, L2_Y, RULE, 1.5)

d.t(X_START, L1_Y - 14, "0.0s 시작", 11, SOFT, MONO, "start")
d.t(X_END, L1_Y - 14, "50.0s", 11, SOFT, MONO, "end")
d.t(X_START, L2_Y - 14, "50.0s", 11, SOFT, MONO, "start")
d.t(X_END, L2_Y - 14, "100.5s 종료", 11, SOFT, MONO, "end")

EVENTS_L1 = [
    (6.2, "사건 1 (6.2s)", "CWR", "로컬 큐 포화", WARN, 1),
    (21.2, "사건 2 (21.2s)", "Recovery", "첫 빠른 재전송", BAD, -1),
    (30.7, "사건 3 (30.7s)", "CWR", "로컬 혼잡 재발", WARN, 1),
    (36.9, "사건 4 (36.9s)", "Recovery", "2차 빠른 재전송", BAD, -1),
    (43.4, "사건 5 (43.4s)", "CWR", "로컬 전송 실패", WARN, 1),
]

EVENTS_L2 = [
    (59.7, "사건 6 (59.7s)", "CWR", "CWR 중 RTO", WARN, -1),
    (62.5, "사건 7 (62.5s)", "Loss→Undo", "헛 RTO 되돌리기", OK, 1),
    (67.5, "사건 8 (67.5s)", "Recovery", "3차 빠른 재전송", BAD, -1),
    (77.1, "사건 9 (77.1s)", "CWR", "로컬 혼잡 발생", WARN, 1),
    (78.5, "사건 10 (78.5s)", "Loss→Undo", "완화 후 되돌리기", OK, -1),
    (88.9, "사건 11 (88.9s)", "Loss", "실제 손실 타임아웃", BAD, 1),
]

def draw_event(t, title, state, desc, color, rail_y, side, x_calc):
    x = x_calc(t)
    box_w, box_h = 108, 54
    box_x = x - box_w / 2
    box_y = rail_y - 12 - box_h if side < 0 else rail_y + 12
    d.line(x, rail_y, x, rail_y - 12 if side < 0 else rail_y + 12, color, 1.2)
    d.o.append(f'<circle cx="{x}" cy="{rail_y}" r="3.5" fill="{color}"/>')
    d.box(box_x, box_y, box_w, box_h, PAPER2, color, 1.0, 6)
    d.t(x, box_y + 18, title, 11, INK, KR, "middle", 600)
    d.t(x, box_y + 34, state, 11, color, MONO, "middle", 600)
    d.t(x, box_y + 48, desc, 11, MUTED, KR, "middle")

for t, title, state, desc, color, side in EVENTS_L1:
    draw_event(t, title, state, desc, color, L1_Y, side, lambda v: X_START + (v / 50.0) * SPAN)

for t, title, state, desc, color, side in EVENTS_L2:
    draw_event(t, title, state, desc, color, L2_Y, side, lambda v: X_START + ((v - 50.0) / 50.5) * SPAN)

d.legend(H - 44, [
    ("정상·되돌리기", OK),
    ("로컬 제동 (CWR)", WARN),
    ("손실 복구 (Recovery)", BAD),
])

d.save("16-03.chapter-overview.svg")
