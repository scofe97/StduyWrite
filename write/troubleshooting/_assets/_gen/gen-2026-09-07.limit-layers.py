# 2026-09-07 D3 곁가지 — accept 큐·스레드 풀·커넥션 풀이 어떻게 연관되는가.
# 학습자가 "용어가 왜 다른지, 셋이 어떻게 이어지는지" 물어 남긴다. 답은 방향이다.
# 타입 스펙: type-swimlane — 가로 레인 하나에 주체 하나. 요청 하나가 왼쪽에서 오른쪽으로
#           레인을 건너며 지나는 관문들을 세우고, focal 은 오늘 문항의 답이 된 관문.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 836, 560
LX, LW, LANE_H, Y0 = 124, 688, 108, 116
NW, NH = 150, 76

d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 D3",
      "상한은 어디에 몇 개나 있는가",
      "요청 하나가 주문 앱에서 결제 앱까지 가며 지나는 관문들. 이름은 저마다 다르지만 구조는 같다. "
      "상한이 있고, 평소엔 여유가 있고, 몰리면 넘친다. 다른 것은 무엇을 지키려는가와 넘쳤을 때의 태도다.",
      lead="나가는 쪽 상한은 상대를 지키고, 들어오는 쪽 상한은 자기를 지킵니다")

LANES = [("주문 Pod", "CALLER"), ("결제 노드 커널", "KERNEL"), ("결제 Pod", "CALLEE")]
def lane_top(k): return Y0 + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for k, (name, eyebrow) in enumerate(LANES):
    d.line(LX, lane_top(k), LX + LW, lane_top(k), RULE, 1.0)
    d.t(16, lane_mid(k) - 2, name, 12, INK, KR, "start", 600)
    d.t(20, lane_mid(k) + 16, eyebrow, 9, SOFT, MONO, "start")
d.line(LX, lane_top(3), LX + LW, lane_top(3), RULE, 1.0)
d.line(LX, Y0, LX, lane_top(3), RULE, 1.0)

COLS = [148, 314, 480, 646]

def node(j, k, title, limit, over, c=None, focal=False):
    x, y = COLS[j], lane_mid(k) - NH / 2
    if focal or c:
        d.tone(x, y, NW, NH, c or ACC, 6)
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    col = (c or ACC) if (focal or c) else INK
    d.t(x + NW / 2, y + 22, title, 12, col, KR, "middle", 600)
    d.t(x + NW / 2, y + 42, limit, 11, MUTED, MONO)
    d.t(x + NW / 2, y + 60, over, 12, SOFT, KR)

d.arrow([(COLS[0] + NW, lane_mid(0)), (COLS[0] + NW + 16, lane_mid(0)),
         (COLS[0] + NW + 16, lane_mid(1)), (COLS[1] - 4, lane_mid(1))], MUTED, "ar", 1.4)
d.arrow([(COLS[1] + NW, lane_mid(1)), (COLS[1] + NW + 16, lane_mid(1)),
         (COLS[1] + NW + 16, lane_mid(2)), (COLS[2] - 4, lane_mid(2))], MUTED, "ar", 1.4)
d.arrow([(COLS[2] + NW, lane_mid(2)), (COLS[3] - 4, lane_mid(2))], MUTED, "ar", 1.4)

node(0, 0, "사이드카 커넥션 풀", "maxConnections", "넘치면 503 · UO", focal=True)
node(1, 1, "accept 큐", "somaxconn", "넘치면 조용히 DROP", c=BAD)
node(2, 2, "사이드카 인바운드", "상한 없음", "그대로 넘깁니다", c=INFO)
node(3, 2, "톰캣", "accept-count", "차면 대기 · 거절")

BOT = lane_top(3)
d.t(LX, BOT + 32, "이름이 다른 것은 지키는 자원과 방향이 달라서입니다. 커널은 말없이 버리고 Envoy 는 503 으로 알려 줍니다.",
    12, MUTED, KR, "start")
d.t(LX, BOT + 54, "그래서 상한을 올리는 일은 언제나 하류로 부담을 미는 일입니다. 늘리기 전에 받는 쪽이 감당하는지를 먼저 봅니다.",
    12, SOFT, KR, "start")

d.legend(H - 52, [("오늘 문항의 답이 된 관문", ACC), ("넘쳐도 조용한 자리", BAD), ("상한이 없는 자리", INFO)])
d.save("2026-09-07.limit-layers.svg")
print("ok limit-layers")
