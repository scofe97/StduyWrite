# 타입 스펙: type-process
# 01-01 §2 Canary — 가중치 90/10 -> 70/30 -> 50/50 -> 0/100 단계 진행, pause·analysis 관문, 실패 시 abort 100/0 복귀.
# 본문 근거: 01-01.배포 전략 비교 L151-L173 (Canary 소절) + 공통 브리프 01-02/01-03 연동 용어.
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO  # noqa: E402

W = 960
LABEL_COL_W = 136
COL_X0 = 156
NODE_W = 152
COL_STRIDE = 200  # gutter = 48 (308..356, 508..556, 708..756)

# Vertical layout (all multiples of 4)
CHIP_Y = 92
STEP_HDR_Y = 144
LANE0_Y = 160
LANE0_H = 100   # 160..260 (router nodes: 172..248, h=76, mid=210)
LANE1_Y = 260
LANE1_H = 96    # 260..356 (gate nodes: 276..340, h=64, mid=308)
LANE2_Y = 356
LANE2_H = 100   # 356..456 (abort node: 372..444, h=72, mid=408)

LEGEND_Y = LANE2_Y + LANE2_H + 16  # 472
H = LEGEND_Y + 44  # 516 (margin = 516 - (472 + 24) = 20 >= 16)

d = D(
    W,
    H,
    "PROCESS · CANARY WEIGHT STEPS",
    "Canary 단계별 가중치 확대와 pause · analysis 관문",
    "트래픽 라우터가 v1/v2 가중치를 90/10, 70/30, 50/50, 0/100 으로 단계 진행하며 "
    "단계마다 pause 와 analysis 관문을 거친다. 관문 실패 시 abort 점선으로 100/0 으로 즉시 복귀하며, "
    "정확한 가중치 분할에는 NGINX 나 Istio 같은 trafficRouting 이 필요하다.",
    lead="단계마다 v1/v2 가중치를 높이며 pause · analysis 관문을 통과하고, 실패하면 abort 로 100/0 에 즉시 복귀합니다",
)


def nx(j):
    return COL_X0 + j * COL_STRIDE


def cx(j):
    return nx(j) + NODE_W // 2


# ── 1. Background grid & lane structure ──────────────────────────────────
# Subtle alternating lane wash (Lane 0 & Lane 2)
d.o.append(f'<rect x="{LABEL_COL_W}" y="{LANE0_Y}" width="{W - LABEL_COL_W - 24}" height="{LANE0_H}" fill="{PAPER2}" opacity="0.45"/>')
d.o.append(f'<rect x="{LABEL_COL_W}" y="{LANE2_Y}" width="{W - LABEL_COL_W - 24}" height="{LANE2_H}" fill="{PAPER2}" opacity="0.45"/>')

# Horizontal lane dividers & vertical label divider
for ly in (LANE0_Y, LANE1_Y, LANE2_Y, LANE2_Y + LANE2_H):
    d.line(16, ly, W - 24, ly, RULE, 0.9)
d.line(LABEL_COL_W, LANE0_Y, LABEL_COL_W, LANE2_Y + LANE2_H, RULE, 1.0)

# Lane labels (left column)
lane_labels = [
    (LANE0_Y + LANE0_H // 2 + 4, "트래픽 라우터"),
    (LANE1_Y + LANE1_H // 2 + 4, "관문 검증"),
    (LANE2_Y + LANE2_H // 2 + 4, "롤백 복구"),
]
for ly, txt in lane_labels:
    d.t(LABEL_COL_W // 2 + 8, ly, txt, 13, MUTED, KR, "middle", 600)

# trafficRouting requirement chip (open top-right strip above Step headers)
CHIP_X, CHIP_W, CHIP_H = 548, 380, 26
d.o.append(
    f'<rect x="{CHIP_X}" y="{CHIP_Y}" width="{CHIP_W}" height="{CHIP_H}" rx="4" '
    f'fill="{INFO}18" stroke="{INFO}" stroke-width="1.0"/>'
)
d.t(
    CHIP_X + CHIP_W // 2,
    CHIP_Y + 18,
    "정밀 가중치 필수 · trafficRouting (NGINX · Istio)",
    13,
    INFO,
    KR,
    "middle",
    600,
)

# Step column headers
step_headers = [
    ("STEP 1", ACC),
    ("STEP 2", MUTED),
    ("STEP 3", MUTED),
    ("STEP 4", OK),
]
for j, (stxt, scol) in enumerate(step_headers):
    d.t(cx(j), STEP_HDR_Y, stxt, 11, scol, MONO, "middle", 600)

# ── 2. Connectors (z-order: before nodes) ────────────────────────────────
R_TOP, R_H = 172, 76   # 172..248, mid=210
G_TOP, G_H = 276, 64   # 276..340, mid=308
A_TOP, A_H = 372, 72   # 372..444, mid=408

# (a) Router j -> Gate j (vertical down, 28px)
for j in range(3):
    col, mk = (ACC, "acc") if j == 0 else (MUTED, "ar")
    d.arrow([(cx(j), R_TOP + R_H), (cx(j), G_TOP)], c=col, m=mk, sw=1.4)

# (b) Gate j -> Router j+1 (orthogonal right -> up -> right, pass path)
for j in range(3):
    gx_right = nx(j) + NODE_W
    corridor_x = gx_right + 12  # 320, 520, 720
    next_left = nx(j + 1)       # 356, 556, 756
    col, mk = (ACC, "acc") if j == 0 else (OK, "ok")
    d.arrow(
        [(gx_right, 308), (corridor_x, 308), (corridor_x, 210), (next_left, 210)],
        c=col,
        m=mk,
        sw=1.5,
    )
    d.t(corridor_x + 6, 246, "통과", 13, col, KR, "start", 600)

# (c) Gate failure -> abort 100/0 (dashed BAD return bus)
# Gate 1 drops straight into top of abort box (32px)
d.arrow([(cx(0), G_TOP + G_H), (cx(0), A_TOP)], c=BAD, m="bad", sw=1.5, dash="5 4")
# Gate 3 drops to bus y=408 and runs left into right edge of abort box
d.arrow(
    [(cx(2), G_TOP + G_H), (cx(2), 408), (nx(0) + NODE_W, 408)],
    c=BAD,
    m="bad",
    sw=1.5,
    dash="5 4",
)
# Gate 2 drops down to join the horizontal abort bus cleanly at (cx(1), 408)
d.line(cx(1), G_TOP + G_H, cx(1), 408, BAD, 1.5, dash="5 4")
d.t(532, 396, "실패 · abort", 13, BAD, KR, "middle", 600)


# ── 3. Nodes ─────────────────────────────────────────────────────────────
def draw_split_bar(x, y, total_w, h, v1_pct, v2_col):
    """v1/v2 가중치 비율을 막대 길이로 시각화한다."""
    if v1_pct == 100:
        d.o.append(f'<rect x="{x}" y="{y}" width="{total_w}" height="{h}" rx="3" fill="{INFO}"/>')
    elif v1_pct == 0:
        d.o.append(f'<rect x="{x}" y="{y}" width="{total_w}" height="{h}" rx="3" fill="{v2_col}"/>')
    else:
        gap = 2
        usable = total_w - gap
        w1 = round(usable * v1_pct / 100)
        w2 = usable - w1
        d.o.append(f'<rect x="{x}" y="{y}" width="{w1}" height="{h}" rx="3" fill="{INFO}"/>')
        d.o.append(f'<rect x="{x + w1 + gap}" y="{y}" width="{w2}" height="{h}" rx="3" fill="{v2_col}"/>')


# Lane 0: Router weight steps
router_steps = [
    (90, 10, "소량 노출", WARN),
    (70, 30, "비율 확대", WARN),
    (50, 50, "절반 전환", WARN),
    (0, 100, "v2 승격", OK),
]
for j, (v1, v2, sub, v2_col) in enumerate(router_steps):
    x = nx(j)
    border_c = OK if v2 == 100 else WARN
    d.tone(x, R_TOP, NODE_W, R_H, border_c, r=6, op="10", sw=1.2)
    d.t(cx(j), R_TOP + 22, f"v1 {v1} / v2 {v2}", 13, INK, MONO, "middle", 600)
    draw_split_bar(x + 12, R_TOP + 32, NODE_W - 24, 12, v1, v2_col)
    sub_col = OK if v2 == 100 else MUTED
    d.t(cx(j), R_TOP + 64, sub, 13, sub_col, KR, "middle", 600 if v2 == 100 else 400)

# Lane 1: pause · analysis gates (Col 0 is focal ACC)
for j in range(3):
    x = nx(j)
    if j == 0:
        d.tone(x, G_TOP, NODE_W, G_H, ACC, r=6, op="12", sw=1.4)
        title_col = ACC
    else:
        d.box(x, G_TOP, NODE_W, G_H, fill=PAPER2, stroke=RULE, sw=1.1, r=6)
        title_col = INK
    d.t(cx(j), G_TOP + 24, "pause · analysis", 12, title_col, MONO, "middle", 600)
    d.t(cx(j), G_TOP + 48, "오류율 · 지연", 13, MUTED, KR, "middle")

# Lane 2: abort 100/0 recovery node (Col 0)
ax = nx(0)
d.tone(ax, A_TOP, NODE_W, A_H, BAD, r=6, op="14", sw=1.2)
d.t(cx(0), A_TOP + 22, "abort · 100 / 0", 13, BAD, MONO, "middle", 600)
draw_split_bar(ax + 12, A_TOP + 32, NODE_W - 24, 12, 100, INFO)
d.t(cx(0), A_TOP + 62, "v1 즉시 복구", 13, MUTED, KR, "middle")

# ── 4. Legend ────────────────────────────────────────────────────────────
d.legend(
    LEGEND_Y,
    [
        ("v1 트래픽", INFO),
        ("v2 카나리", WARN),
        ("관문 검증", ACC),
        ("통과 · 승격", OK),
        ("abort 복구", BAD),
    ],
)

out_path = (
    sys.argv[1]
    if len(sys.argv) > 1
    else str(pathlib.Path(__file__).resolve().parent.parent / "01-01.canary-weight-steps.svg")
)
d.save(out_path)
print(f"ok {pathlib.Path(out_path).name}")
