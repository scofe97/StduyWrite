# 07-01 §5 — DrDoS 는 공격자가 피해자를 직접 때리지 않는다. 위조한 출발지 하나가 방향을 바꾼다.
# 출처: US-CERT/CISA TA14-017A "UDP-Based Amplification Attacks" 의 증폭 배수.
# 타입 스펙: type-data-flow — 단계마다 *누가* 무엇을 하는지. 레인은 실행 주체이고
#           칸 사이를 건너가는 것은 패킷 자체다.
#           축약: §2 공식의 label_col_w 140 · right_pad 28 은 그대로 두고 step_slot_w 를 240 으로,
#           lane_h 를 116 으로 올린다(한글 3줄 노드).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

LABEL_W, SLOT_W, RIGHT_PAD = 140, 240, 28
HEADER_TOP, HEADER_H, LANE_H, LEGEND_H = 96, 36, 116, 104
STEPS = [("01", "위조"), ("02", "반사"), ("03", "도착")]
LANES = [("공격자", "ATTACKER"), ("공개 UDP 서버", "REFLECTOR"), ("피해자", "VICTIM")]
NODE_W, NODE_H = 196, 76

W = LABEL_W + len(STEPS) * SLOT_W + RIGHT_PAD
H = HEADER_TOP + HEADER_H + len(LANES) * LANE_H + LEGEND_H

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-01 §5",
      "반사와 증폭이 방향을 바꾸는 법",
      "DrDoS 에서 공격자는 피해자에게 아무것도 보내지 않는다. 출발지를 피해자로 위조한 작은 요청이 공개 서버에 닿고, 규격대로 답한 큰 응답이 피해자에게 쏟아진다.",
      "피해자의 캡처에는 공격자가 아니라 멀쩡한 서버들만 남습니다")

def step_cx(j): return LABEL_W + 20 + j * SLOT_W + NODE_W / 2
def lane_top(k): return HEADER_TOP + HEADER_H + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for j, (num, label) in enumerate(STEPS):
    cx = step_cx(j)
    on = (j == 1)
    d.o.append(f'<rect x="{cx - 56}" y="{HEADER_TOP + 6}" width="20" height="18" rx="9" '
               f'fill="{ACC if on else PAPER2}" stroke="{ACC if on else RULE}" stroke-width="1"/>')
    d.t(cx - 46, HEADER_TOP + 19, num, 9, PAPER if on else MUTED, MONO)
    d.t(cx - 26, HEADER_TOP + 19, label, 11, ACC if on else MUTED, KR, "start", 600)

for k, (name, eyebrow) in enumerate(LANES):
    d.line(LABEL_W, lane_top(k), W - RIGHT_PAD, lane_top(k), RULE, 1.0)
    d.t(20, lane_mid(k) - 2, name, 12, INK, KR, "start", 600)
    d.t(20, lane_mid(k) + 14, eyebrow, 9, SOFT, MONO, "start")
d.line(LABEL_W, lane_top(3), W - RIGHT_PAD, lane_top(3), RULE, 1.0)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(3), RULE, 1.0)

def node(j, k, title, l1, l2, c=None):
    x, y = step_cx(j) - NODE_W / 2, lane_mid(k) - NODE_H / 2
    if c: d.tone(x, y, NODE_W, NODE_H, c, 6)
    else: d.box(x, y, NODE_W, NODE_H, PAPER2, RULE, 1.0, 6)
    d.t(x + NODE_W / 2, y + 24, title, 11, c if c else INK, KR, "middle", 600)
    d.t(x + NODE_W / 2, y + 44, l1, 11, MUTED, MONO)
    d.t(x + NODE_W / 2, y + 62, l2, 11, MUTED, KR)
    return x, y

node(0, 0, "작은 요청을 보냅니다", "src = 피해자 IP", "출발지만 바꿔 씁니다")
node(1, 1, "규격대로 답합니다", "dst = src = 피해자 IP", "서버는 속은 줄 모릅니다", ACC)
node(2, 2, "증폭된 응답이 몰립니다", "NTP 556.9x · DNS 28~54x", "보낸 적 없는 답만 쌓입니다", BAD)

def hop(j0, k0, j1, k1, c, m):
    x0, y0 = step_cx(j0) + NODE_W / 2, lane_mid(k0)
    x1, y1 = step_cx(j1) - NODE_W / 2, lane_mid(k1)
    mid = (x0 + x1) / 2
    d.arrow([(x0, y0), (mid, y0), (mid, y1), (x1 - 4, y1)], c, m, 1.4)

hop(0, 0, 1, 1, MUTED, "ar")
hop(1, 1, 2, 2, BAD, "bad")

d.t(LABEL_W, lane_top(3) + 28,
    "증폭 배수는 US-CERT TA14-017A 의 값입니다 — BitTorrent 3.8x 까지 같은 목록에 올라 있습니다",
    11, MUTED, KR, "start")

d.legend(H - 62, [("속은 채 규격대로 답하는 쪽", ACC), ("증폭된 응답이 닿는 쪽", BAD)])
d.save("07-01.drdos-reflection.svg")
