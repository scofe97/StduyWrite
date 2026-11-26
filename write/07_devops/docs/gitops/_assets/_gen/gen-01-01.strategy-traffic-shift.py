# 타입 스펙: type-line
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import ACC, BAD, D, INK, KR, MONO, MUTED, OK, PAPER, RULE, SOFT, WARN

# 4px 그리드 고정 상수 (W=920 -> 12px 한글 1.304% >= 1.3% 목표)
W = 920
PLOT_X0 = 232
PLOT_W = 640
PLOT_X1 = PLOT_X0 + PLOT_W  # 872 (= W - 48, 범례 구분선 끝과 정렬)
SLOTS = 5
SLOT_W = PLOT_W // SLOTS  # 128

ROW_Y0 = 120
PLOT_H = 72
ROW_STRIDE = 100
N_ROWS = 6

X_TICK_Y = ROW_Y0 + (N_ROWS - 1) * ROW_STRIDE + PLOT_H + 24  # 716
X_CAP_Y = X_TICK_Y + 20  # 736
LEGEND_Y = X_CAP_Y + 20  # 756
H = LEGEND_Y + 44  # 800 (margin = 800 - (756 + 24) = 20 >= 16)


def sx(i):
    return PLOT_X0 + i * SLOT_W


def sc(i):
    return PLOT_X0 + i * SLOT_W + SLOT_W // 2


def py(y_bot, pct):
    return round(y_bot - PLOT_H * pct / 100.0)


def step_path(pts):
    return " ".join(("M" if i == 0 else "L") + f" {x} {y}" for i, (x, y) in enumerate(pts))


def area_poly(d, pts, y_bot, color, alpha="14"):
    poly = [(pts[0][0], y_bot)] + pts + [(pts[-1][0], y_bot)]
    pstr = " ".join(f"{x},{y}" for x, y in poly)
    d.o.append(f'<polygon points="{pstr}" fill="{color}{alpha}" stroke="none"/>')


def dot(d, cx, cy, color, r=3.5):
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>')


def draw_frame(d, y_top, name, layer, focal=False):
    y_bot = y_top + PLOT_H
    if focal:
        d.o.append(f'<rect x="{PLOT_X0}" y="{y_top}" width="{PLOT_W}" height="{PLOT_H}" rx="4" fill="{ACC}0E" stroke="none"/>')
        d.o.append(f'<rect x="12" y="{y_top + 4}" width="4" height="{PLOT_H - 8}" rx="2" fill="{ACC}"/>')

    # 좌측 전략명 + 트래픽 분할 계층
    d.t(24 if focal else 16, y_top + 32, name, size=13, fill=INK, fam=KR, anchor="start", weight=600)
    layer_fam = KR if any("가" <= ch <= "힣" for ch in layer) else MONO
    d.t(24 if focal else 16, y_top + 52, layer, size=12, fill=MUTED, fam=layer_fam, anchor="start", weight=400)

    # y축 눈금 (100 / 50 tick / 0)
    d.t(PLOT_X0 - 12, y_top + 4, "100", size=11, fill=MUTED, fam=MONO, anchor="end")
    d.t(PLOT_X0 - 12, y_bot + 4, "0", size=11, fill=MUTED, fam=MONO, anchor="end")
    d.line(PLOT_X0 - 6, y_top + PLOT_H // 2, PLOT_X0, y_top + PLOT_H // 2, RULE, 0.8)

    # 공통 격자: 100% 상한 점선, 0% 기준선, 세로 시간 경계
    d.line(PLOT_X0, y_top, PLOT_X1, y_top, RULE, 0.7, dash="2 4")
    d.line(PLOT_X0, y_bot, PLOT_X1, y_bot, RULE, 1.0)
    d.line(PLOT_X0, y_top, PLOT_X0, y_bot, RULE, 1.0)
    for i in range(1, SLOTS):
        d.line(sx(i), y_top, sx(i), y_bot, RULE, 0.7, dash="2 4")
    return y_bot


d = D(
    W,
    H,
    "LINE SMALL MULTIPLES · DEPLOYMENT TRAFFIC SHIFT",
    "여섯 배포 전략의 v2 트래픽 전환 추이",
    "공통 시간축 t0~t4에서 여섯 배포 전략의 사용자 트래픽 중 v2 비율 0~100% 변화와 Shadow 복제 흐름을 비교합니다.",
    lead="공통 시간축(t0→t4)에서 사용자 트래픽 중 v2 비율(0~100%) — Rolling은 replicas 4·maxSurge 1·maxUnavailable 0 기준",
)

# y축 단위 헤더
d.t(PLOT_X0 - 12, ROW_Y0 - 12, "v2 %", size=11, fill=MUTED, fam=MONO, anchor="end", weight=600)

# 1. RollingUpdate: 0 -> 25 -> 50 -> 75 -> 100
y0 = ROW_Y0 + 0 * ROW_STRIDE
yb = draw_frame(d, y0, "RollingUpdate", "Deployment")
roll_vals = [0, 25, 50, 75, 100]
roll_pts = []
for i, v in enumerate(roll_vals):
    yv = py(yb, v)
    roll_pts.append((sx(i), yv))
    roll_pts.append((sx(i + 1), yv))
area_poly(d, roll_pts, yb, OK, "14")
d.path(step_path(roll_pts), OK, 2.2)
d.t(sx(0) + 12, y0 + 20, "4 Pod · surge 1", size=11, fill=MUTED, fam=MONO, anchor="start")
d.t(sc(0), py(yb, 0) - 10, "0", size=11, fill=MUTED, fam=MONO)
d.t(sc(1), py(yb, 25) - 10, "25", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(2), py(yb, 50) - 10, "50", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(3), py(yb, 75) + 18, "75", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(4), py(yb, 100) + 18, "100%", size=11, fill=OK, fam=MONO, weight=600)

# 2. Recreate: v1 100 -> 다운타임 0/0 -> v2 100
y1 = ROW_Y0 + 1 * ROW_STRIDE
yb = draw_frame(d, y1, "Recreate", "Deployment")
# t0: v1 100% (v2 0%)
d.path(step_path([(sx(0), py(yb, 0)), (sx(1), py(yb, 0))]), OK, 2.2)
dot(d, sx(1), py(yb, 0), MUTED, 3.0)
d.t(sc(0), py(yb, 0) - 12, "v1 100%", size=11, fill=MUTED, fam=MONO, weight=600)
# t1..t2: 다운타임 띠 (v1·v2 모두 없음, 불연속 구간)
d.o.append(
    f'<rect x="{sx(1)}" y="{y1}" width="{SLOT_W * 2}" height="{PLOT_H}" '
    f'fill="{BAD}1C" stroke="{BAD}" stroke-width="1.1" stroke-dasharray="4 3"/>'
)
d.t(sx(2), y1 + 40, "다운타임 · 0/0", size=12, fill=BAD, fam=KR, weight=600)
# t3..t4: v2 100%
rec_pts = [(sx(3), py(yb, 100)), (sx(5), py(yb, 100))]
area_poly(d, rec_pts, yb, OK, "14")
d.path(step_path(rec_pts), OK, 2.2)
dot(d, sx(3), py(yb, 100), OK, 3.5)
d.t(sx(4), py(yb, 100) + 20, "v2 100%", size=11, fill=OK, fam=MONO, weight=600)

# 3. Blue-Green: Green 준비 0 -> selector 전환 수직 100 -> 점선 복귀 0
y2 = ROW_Y0 + 2 * ROW_STRIDE
yb = draw_frame(d, y2, "Blue-Green", "Service")
bg_pts = [
    (sx(0), py(yb, 0)),
    (sx(2), py(yb, 0)),
    (sx(2), py(yb, 100)),
    (sx(5), py(yb, 100)),
]
area_poly(d, [(sx(2), py(yb, 100)), (sx(5), py(yb, 100))], yb, OK, "14")
d.path(step_path(bg_pts), OK, 2.2)
d.t(sx(1), py(yb, 0) - 12, "Green 준비", size=12, fill=MUTED, fam=KR)
d.t(sx(2) + 12, y2 + 40, "selector=green", size=11, fill=OK, fam=MONO, anchor="start", weight=600)
# 되돌리기 점선 (t3 중간에서 100 -> 0 복귀)
rb_x = sc(3)
d.path(step_path([(rb_x, py(yb, 100)), (rb_x, py(yb, 0)), (PLOT_X1 - 4, py(yb, 0))]), BAD, 2.0, m="bad", dash="5 4")
d.t(sc(4) - 8, py(yb, 0) - 12, "복귀 0%", size=12, fill=BAD, fam=KR, weight=600)

# 4. Canary: 10 -> (pause) -> 30 -> 50 -> 100, analysis 실패 시 abort 점선 0
y3 = ROW_Y0 + 3 * ROW_STRIDE
yb = draw_frame(d, y3, "Canary", "Gateway·Mesh")
can_pts = [
    (sx(0), py(yb, 10)),
    (sx(2), py(yb, 10)),
    (sx(2), py(yb, 30)),
    (sx(3), py(yb, 30)),
    (sx(3), py(yb, 50)),
    (sx(4), py(yb, 50)),
    (sx(4), py(yb, 100)),
    (sx(5), py(yb, 100)),
]
area_poly(d, can_pts, yb, OK, "14")
d.path(step_path(can_pts), OK, 2.2)
# pause 구간 강조선 + 칩
d.path(step_path([(sx(1), py(yb, 10)), (sx(2), py(yb, 10))]), WARN, 2.6)
d.chip(sc(1), y3 + 32, "pause", WARN, size=11, pad=8)
d.t(sc(0), py(yb, 10) - 10, "10%", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(2), py(yb, 30) - 10, "30%", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(3), py(yb, 50) - 10, "50%", size=11, fill=OK, fam=MONO, weight=600)
d.t(sc(4), py(yb, 100) + 18, "100%", size=11, fill=OK, fam=MONO, weight=600)
# analysis 실패 시 abort 점선 (30% -> 0%)
d.path(step_path([(sx(3), py(yb, 30)), (sx(3), py(yb, 0)), (PLOT_X1 - 4, py(yb, 0))]), BAD, 2.0, m="bad", dash="5 4")
d.t(sc(4), py(yb, 0) - 12, "abort 0%", size=11, fill=BAD, fam=MONO, weight=600)

# 5. A/B Testing: 시간 무관 그룹 B 50% 수평선 + 헤더·쿠키 기준 칩
y4 = ROW_Y0 + 4 * ROW_STRIDE
yb = draw_frame(d, y4, "A/B Testing", "Ingress·앱")
ab_pts = [(sx(0), py(yb, 50)), (sx(5), py(yb, 50))]
area_poly(d, ab_pts, yb, WARN, "12")
d.path(step_path(ab_pts), WARN, 2.2)
d.t(sc(0), py(yb, 50) - 12, "그룹 B 50%", size=12, fill=WARN, fam=KR, weight=600)
d.chip(sc(2), y4 + 18, "헤더·쿠키 기준", WARN, size=12, pad=8)

# 6. Shadow (FOCAL): 사용자 v2 0% 실선 + 복제 요청 100% 점선 (응답 폐기)
y5 = ROW_Y0 + 5 * ROW_STRIDE
yb = draw_frame(d, y5, "Shadow", "Gateway·Mesh", focal=True)
# 실트래픽 v2 = 0%
d.path(step_path([(sx(0), py(yb, 0)), (sx(5), py(yb, 0))]), OK, 2.2)
d.t(sc(2), py(yb, 0) - 12, "실트래픽 0%", size=12, fill=OK, fam=KR, weight=600)
# 복제 요청 100% (focal accent 점선 + 꼭짓점 점)
d.path(step_path([(sx(0), py(yb, 100)), (sx(5), py(yb, 100))]), ACC, 2.4, dash="7 4")
for i in range(SLOTS):
    dot(d, sc(i), py(yb, 100), ACC, 3.5)
d.t(sc(2), py(yb, 100) + 22, "복제 100% · 응답 폐기", size=12, fill=ACC, fam=KR, weight=600)

# 공통 x축 눈금 (t0 -> t4)
for i in range(SLOTS):
    d.t(sc(i), X_TICK_Y, f"t{i}", size=11, fill=MUTED, fam=MONO, weight=600)
d.t(PLOT_X0 + PLOT_W // 2, X_CAP_Y, "배포 경과", size=12, fill=MUTED, fam=KR)

d.legend(
    LEGEND_Y,
    [
        ("v2 실트래픽", OK),
        ("중단 · 롤백/abort", BAD),
        ("조건 분기 · 대기", WARN),
        ("복제 100% (응답 폐기)", ACC),
    ],
)

d.save("01-01.strategy-traffic-shift.svg")
