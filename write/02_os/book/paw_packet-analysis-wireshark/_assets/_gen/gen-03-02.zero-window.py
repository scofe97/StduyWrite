# 03-02 §5 — ZeroWindow 가 어디서 생기는가. 수신 버퍼가 차는 지점을 파이프라인 위에 놓는다.
# 원문: "receiver's buffers are full. This condition arrives more rapidly for writes than reads."
# 타입 스펙: type-data-flow — 단계마다 *누가* 무엇을 하는지. 레인은 송신자·네트워크·수신자이고
#           칸 사이를 건너가는 것은 세그먼트다.
#           축약: §2 공식의 label_col_w 140 · right_pad 28 은 그대로, step_slot_w 는 112→184,
#           lane_h 는 80→108 로 올린다(한글 3줄 노드). 헤더 띠는 제목 블록 아래에서 시작한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, SLOT_W, RIGHT_PAD = 140, 184, 28
HEADER_TOP, HEADER_H, LANE_H, LEGEND_H = 96, 36, 108, 96
STEPS = [("01", "보냄"), ("02", "실려 감"), ("03", "버퍼에 쌓임"), ("04", "읽어 감")]
LANES = [("송신자", "SND"), ("네트워크", "NET"), ("수신자", "RCV")]
NODE_W, NODE_H = 164, 76

W = LABEL_W + len(STEPS) * SLOT_W + RIGHT_PAD
H = HEADER_TOP + HEADER_H + len(LANES) * LANE_H + LEGEND_H
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02 §5",
      "ZeroWindow 가 생기는 자리",
      "세그먼트가 수신 버퍼에 쌓이는 속도가 애플리케이션이 읽어 가는 속도보다 빠르면 버퍼가 찬다. 그때 수신자가 윈도우 0 을 광고하고 송신자는 멈춘다.",
      "막힌 곳은 네트워크가 아니라 수신자의 읽기 속도입니다")

def step_cx(j): return LABEL_W + 10 + j * SLOT_W + NODE_W / 2
def lane_top(k): return HEADER_TOP + HEADER_H + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for j, (num, label) in enumerate(STEPS):
    cx = step_cx(j)
    foc = (j == 2)
    d.o.append(f'<rect x="{cx - 52}" y="{HEADER_TOP + 6}" width="20" height="18" rx="9" '
               f'fill="{ACC if foc else PAPER2}" stroke="{ACC if foc else RULE}" stroke-width="1"/>')
    d.t(cx - 42, HEADER_TOP + 20, num, 9, PAPER if foc else SOFT, MONO)
    d.t(cx - 24, HEADER_TOP + 20, label, 12, ACC if foc else MUTED, KR, "start", 600)

for k, (name, key) in enumerate(LANES):
    d.line(0, lane_top(k), W - RIGHT_PAD, lane_top(k), RULE, 0.8)
    d.t(16, lane_mid(k) - 4, name, 12, SOFT, KR, "start", 600)
    d.t(16, lane_mid(k) + 14, key, 9, SOFT, MONO, "start")
d.line(0, lane_top(len(LANES)), W - RIGHT_PAD, lane_top(len(LANES)), RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(len(LANES)), RULE, 0.8)

def node(j, k, title, sub, tool, focal=False, c=None):
    x, y = step_cx(j) - NODE_W / 2, lane_mid(k) - NODE_H / 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NODE_W}" height="{NODE_H}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, NODE_W, NODE_H, c, 8)
    else:
        d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 1.0, 8)
    col = ACC if focal else (c if c else INK)
    d.t(x + NODE_W / 2, y + 24, title, 13, col, KR, "middle", 600)
    d.t(x + NODE_W / 2, y + 43, sub, 11, MUTED, KR)
    d.t(x + NODE_W / 2, y + 62, tool, 10, MUTED, MONO)

d.arrow([(step_cx(0), lane_mid(0) + NODE_H / 2), (step_cx(0), lane_mid(1)),
         (step_cx(1) - NODE_W / 2 - 4, lane_mid(1))], MUTED, "ar", 1.4)
d.arrow([(step_cx(1) + 44, lane_mid(1) + NODE_H / 2), (step_cx(1) + 44, lane_mid(2)),
         (step_cx(2) - NODE_W / 2 - 4, lane_mid(2))], MUTED, "ar", 1.4)
d.arrow([(step_cx(2) + NODE_W / 2, lane_mid(2)), (step_cx(3) - NODE_W / 2 - 4, lane_mid(2))],
        WARN, "warn", 1.4)
# 윈도우 0 광고가 거슬러 올라가 송신을 멈춘다
d.arrow([(step_cx(2), lane_mid(2) - NODE_H / 2), (step_cx(2), lane_mid(0) + 8),
         (step_cx(0) + NODE_W / 2 + 4, lane_mid(0) + 8)], BAD, "bad", 1.4, dash="4,3")
d.t(step_cx(1) + 20, lane_mid(0) - 4, "win=0 광고 · 송신이 멈춥니다", 11, BAD, KR)

node(0, 0, "세그먼트 송신", "윈도우가 허락하는 만큼", "tcp.len > 0")
node(1, 1, "선을 지나감", "여기는 대개 병목이 아닙니다", "RTT")
node(2, 2, "수신 버퍼", "쓰기가 읽기보다 빠르면 찹니다", "window_size=0", focal=True)
node(3, 2, "애플리케이션이 읽음", "이 속도가 상한을 정합니다", "read()", c=WARN)

d.legend(H - LEGEND_H + 24,
         [("버퍼가 차는 지점", ACC), ("실제 상한을 정하는 쪽", WARN), ("송신을 멈추는 신호", BAD)])
d.save("03-02.zero-window.svg")
