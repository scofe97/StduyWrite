# 타입 스펙: type-data-flow
# 14-01.middleware-value — 미들웨어가 쿠키에서 사용자를 꺼내 context 에 담고 핸들러가 꺼내 업무 로직에 명시적 인자로 넘기는 데이터 흐름
# 본문 요구(14-01 §2 「미들웨어가 담고 핸들러가 꺼내 명시적 인자로 넘깁니다」): 미들웨어가 값을 context 에 담음 → 핸들러가
#           FromContext 로 꺼냄 → 업무 로직에는 명시적 인자로 넘김. 값·함수 이름은 212·241행 블록의 것만 쓴다.
# 타입 스펙: type-data-flow — 레인 3개(Middleware · Controller · BusinessLogic), 단계 4개(EXTRACT · INJECT · RESOLVE · DELEGATE).
#           focal 은 BusinessLogic 노드와 Controller → BusinessLogic 간의 명시적 인자(user) 전달 화살표.
# 사실 출처: Learning Go 2판 14장 「Values」 context_user 예제(212·241행), go1.25.1 / go1.27.1 로컬 실행 대조.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 984, 432
LABEL_W = 144
N_STEPS = 4
STEP_W = 196
N_LANES = 3
LANE_H = 74
Y_START = 104
HEADER_H = 34
Y_LANES = Y_START + HEADER_H
LEGEND_Y = Y_LANES + N_LANES * LANE_H + 16


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "DATA FLOW · 14-01 §2",
      "미들웨어가 담은 값을 핸들러가 꺼내 명시적 인자로 넘깁니다",
      "미들웨어는 extractUser 로 쿠키에서 사용자를 꺼내 ContextWithUser 로 context 에 담는다. "
      "컨트롤러는 UserFromContext 로 context 에서 사용자를 복원하고, "
      "업무 로직 BusinessLogic 에는 context 와 함께 user 를 명시적 인자로 직접 넘긴다.",
      lead="단계마다 데이터가 변환됩니다. 업무 로직에는 context 대신 명시적 인자로 전달합니다.")

# 1. Header (Steps)
steps = [
    ("01", "EXTRACT", False),
    ("02", "INJECT", False),
    ("03", "RESOLVE", False),
    ("04", "DELEGATE", True),
]

for j, (num, lab, focal) in enumerate(steps):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    c = ACC if focal else SOFT
    d.o.append(f'<rect x="{cx - 18}" y="{Y_START + 2}" width="36" height="16" rx="8" fill="{c}22" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, Y_START + 14, num, 9, c, MONO, "middle", 600)
    d.t(cx, Y_START + 28, lab, 9, ACC if focal else MUTED, MONO, "middle", 600)

# 2. Lanes
lanes = [
    "Middleware",
    "Controller",
    "Logic",
]

for k, name in enumerate(lanes):
    ly = Y_LANES + k * LANE_H
    if k % 2 == 1:
        d.o.append(f'<rect x="{LABEL_W}" y="{ly}" width="{W - LABEL_W - 24}" height="{LANE_H}" fill="#161B22" opacity="0.6"/>')
    d.line(16, ly, W - 24, ly, RULE, 0.8)
    d.t(LABEL_W // 2, ly + LANE_H // 2 + 4, name, 11, INK, kr(name), "middle", 600)

d.line(16, Y_LANES + N_LANES * LANE_H, W - 24, Y_LANES + N_LANES * LANE_H, RULE, 0.8)
d.line(LABEL_W, Y_START, LABEL_W, Y_LANES + N_LANES * LANE_H, RULE, 0.8)

# 3. Nodes and Data Chips
NODE_W, NODE_H = 148, 50


def draw_node(j, k, title, sub, tool, focal=False):
    cx = LABEL_W + j * STEP_W + STEP_W // 2
    x = cx - NODE_W // 2
    y = Y_LANES + k * LANE_H + (LANE_H - NODE_H) // 2

    # Container
    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, r=6, op="18", sw=1.3)
    else:
        d.box(x, y, NODE_W, NODE_H, fill=PAPER2, stroke=RULE, sw=0.9, r=6)

    # Title & Sub
    d.t(cx, y + 17, title, 11, ACC if focal else INK, MONO, "middle", 600)
    d.t(cx, y + 31, sub, 9, MUTED, MONO, "middle")
    d.t(cx, y + 43, tool, 8.5, SOFT, MONO, "middle")


# Nodes configuration
nodes = [
    # j, k, title, sub, tool, focal
    (0, 0, "extractUser", "Cookie(\"identity\")", "user", False),
    (1, 0, "ContextWithUser", "WithValue(ctx, ...)", "req.WithContext", False),
    (2, 1, "UserFromContext", "Value(key).(string)", "user, ok", False),
    (3, 2, "BusinessLogic", "Logic.BusinessLogic", "(ctx, user, data)", True),
]

# 4. Arrows
cx0 = LABEL_W + 0 * STEP_W + STEP_W // 2
cx1 = LABEL_W + 1 * STEP_W + STEP_W // 2
cx2 = LABEL_W + 2 * STEP_W + STEP_W // 2
cx3 = LABEL_W + 3 * STEP_W + STEP_W // 2

x0_r = cx0 + NODE_W // 2
x1_l = cx1 - NODE_W // 2
y_mw = Y_LANES + 0 * LANE_H + LANE_H // 2
d.arrow([(x0_r + 2, y_mw), (x1_l - 4, y_mw)], SOFT, "soft", 1.2)
d.t((x0_r + x1_l) // 2, y_mw - 6, "user", 9, MUTED, MONO, "middle")

# Arrow 2: Node 1 bottom -> Node 2 left
y1_bot = Y_LANES + 0 * LANE_H + (LANE_H + NODE_H) // 2
y_ctl = Y_LANES + 1 * LANE_H + LANE_H // 2
x2_l = cx2 - NODE_W // 2
d.path(f"M {cx1} {y1_bot + 2} L {cx1} {y_ctl - 8} Q {cx1} {y_ctl} {cx1 + 8} {y_ctl} L {x2_l - 4} {y_ctl}",
       INFO, 1.2, m="info")
d.t((cx1 + x2_l) // 2, y_ctl - 6, "req (ctx)", 9, MUTED, MONO, "middle")

# Arrow 3: Node 2 bottom -> Node 3 left (focal)
y2_bot = Y_LANES + 1 * LANE_H + (LANE_H + NODE_H) // 2
y_log = Y_LANES + 2 * LANE_H + LANE_H // 2
x3_l = cx3 - NODE_W // 2
d.path(f"M {cx2} {y2_bot + 2} L {cx2} {y_log - 8} Q {cx2} {y_log} {cx2 + 8} {y_log} L {x3_l - 4} {y_log}",
       ACC, 1.4, m="acc")
d.t((cx2 + x3_l) // 2, y_log - 6, "user (명시적 인자)", 11, ACC, kr("user (명시적 인자)"), "middle", 600)

# Draw all nodes
for n in nodes:
    draw_node(*n)

# 5. Legend
d.legend(LEGEND_Y, [("쿠키 추출", SOFT), ("context 주입", INFO), ("명시적 인자 (핵심)", ACC)])

out_path = str(pathlib.Path(__file__).resolve().parent.parent / "14-01.middleware-value.svg")
d.save(out_path)
print("ok 14-01 middleware-value")
