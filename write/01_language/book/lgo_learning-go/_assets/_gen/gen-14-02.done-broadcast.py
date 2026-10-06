# 타입 스펙: type-data-flow — cancelFunc() 한 번으로 Done 채널이 닫혀 대기하던 고루틴 여럿이 동시에 깨어나는 흐름
# 본문 요구(14-02 §1 「취소는 Done 채널이 닫히는 것으로 전해집니다」):
#           cancelFunc() 호출 한 번으로 Done 채널(chan struct{})이 닫히고,
#           select 로 Done 채널을 기다리던 고루틴 여럿이 동시에 깨어난다.
# 사실 출처: Learning Go 2판 14장 「Cancellation」
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 960, 580
LABEL_W, SLOT_W, RIGHT_PAD = 120, 260, 40
HEADER_TOP, HEADER_H = 96, 36
LANE_H = 72
LEGEND_Y = 516

STEPS = [("01", "취소 호출"), ("02", "채널 닫힘"), ("03", "동시 수신")]
LANES = [
    ("호출자", "cancelFunc"),
    ("context", "chan struct{}"),
    ("고루틴 1", "select"),
    ("고루틴 2", "select"),
    ("고루틴 3", "select"),
]
NODE_W, NODE_H = 156, 44


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def step_cx(j):
    return LABEL_W + 20 + j * SLOT_W + SLOT_W // 2


def lane_top(k):
    return HEADER_TOP + HEADER_H + k * LANE_H


def lane_mid(k):
    return lane_top(k) + LANE_H // 2


d = D(W, H, "DATA FLOW · 14-02 §1",
      "Done 채널 닫힘으로 여러 고루틴이 동시에 깨어납니다",
      "cancelFunc() 호출 한 번으로 context 의 Done 채널이 닫히고, select 로 대기하던 여러 고루틴이 동시에 깨어나는 전파 과정.",
      lead="취소는 채널 닫힘으로 전파되어 select 로 대기 중인 모든 고루틴을 깨웁니다.")

# 상단 단계 칩
for j, (num, label) in enumerate(STEPS):
    cx = step_cx(j)
    is_focal = (j == 1)
    c = ACC if is_focal else (INFO if j == 0 else OK)
    d.o.append(f'<rect x="{cx - 52}" y="{HEADER_TOP + 6}" width="28" height="20" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="1"/>')
    d.t(cx - 38, HEADER_TOP + 20, num, 10, c, MONO, "middle", 600)
    d.t(cx - 16, HEADER_TOP + 20, label, 12, INK, KR, "start", 600)

# 레인 배경 구분선과 라벨
for k, (name, key) in enumerate(LANES):
    yt = lane_top(k)
    ym = lane_mid(k)
    d.line(16, yt, W - RIGHT_PAD, yt, RULE, 0.8)
    d.t(24, ym - 4, name, 13, INK, KR, "start", 600)
    d.t(24, ym + 14, key, 10, MUTED, MONO, "start")

d.line(16, lane_top(len(LANES)), W - RIGHT_PAD, lane_top(len(LANES)), RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(len(LANES)), RULE, 0.8)


def node(j, k, title, sub, c=None, focal=False):
    cx = step_cx(j)
    ym = lane_mid(k)
    x = cx - NODE_W // 2
    y = ym - NODE_H // 2
    if focal:
        d.tone(x, y, NODE_W, NODE_H, ACC, 6, "18", 1.4)
    elif c:
        d.tone(x, y, NODE_W, NODE_H, c, 6, "14", 1.1)
    else:
        d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 1.0, 6)
    tc = ACC if focal else (c if c else INK)
    d.t(cx, ym - 3, title, 13, tc, kr(title), "middle", 600)
    d.t(cx, ym + 14, sub, 11, MUTED, kr(sub), "middle")


# ── 노드 배치 ─────────────────────────────────────────────────────────────
# Step 01: 호출자가 cancelFunc() 호출
node(0, 0, "cancelFunc()", "취소 함수 호출", INFO)

# Step 02: context 의 Done 채널 닫힘 (FOCAL)
node(1, 1, "close(Done)", "chan struct{} 닫힘", ACC, focal=True)

# Step 03: 고루틴 셋이 select 에서 동시 수신
node(2, 2, "case <-ctx.Done():", "고루틴 1 깨어남", OK)
node(2, 3, "case <-ctx.Done():", "고루틴 2 깨어남", OK)
node(2, 4, "case <-ctx.Done():", "고루틴 3 깨어남", OK)

# ── 연결선 배치 (직각만 사용) ─────────────────────────────────────────────
# Step 01 -> Step 02: cancelFunc -> close(Done)
x1 = step_cx(0) + NODE_W // 2
y1 = lane_mid(0)
x2 = step_cx(1) - NODE_W // 2 - 4
y2 = lane_mid(1)
cx1 = 406
d.arrow([(x1, y1), (cx1, y1), (cx1, y2), (x2, y2)], INFO, "info", 1.4)
d.t(cx1, y1 - 8, "cancelFunc()", 11, INFO, MONO, "middle", 600)

# Step 02 -> Step 03: close(Done) -> 3개 고루틴으로 브로드캐스트
bx1 = step_cx(1) + NODE_W // 2
by1 = lane_mid(1)
bx2 = step_cx(2) - NODE_W // 2 - 4
bcx = (bx1 + bx2) // 2

# 주간선: context 에서 분기 축까지
d.line(bx1, by1, bcx, by1, OK, 1.4)
d.t(bcx, by1 - 8, "Done 닫힘", 11, OK, KR, "middle", 600)

# 수직 분기선
d.line(bcx, lane_mid(2), bcx, lane_mid(4), OK, 1.4)

# 각 고루틴으로 진입하는 화살표 셋
d.arrow([(bcx, lane_mid(2)), (bx2, lane_mid(2))], OK, "ok", 1.4)
d.arrow([(bcx, lane_mid(3)), (bx2, lane_mid(3))], OK, "ok", 1.4)
d.arrow([(bcx, lane_mid(4)), (bx2, lane_mid(4))], OK, "ok", 1.4)

# 범례
d.legend(LEGEND_Y, [("취소 호출", INFO), ("채널 닫힘 (focal)", ACC), ("동시 수신", OK)])

out_path = str(pathlib.Path(__file__).resolve().parent.parent / "14-02.done-broadcast.svg")
d.save(out_path)
print("ok 14-02 done-broadcast")
