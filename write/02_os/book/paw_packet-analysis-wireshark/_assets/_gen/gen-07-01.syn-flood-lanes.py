# 07-01 §2 — SYN 홍수에서 세 주체가 각각 무엇을 하는가. 정상 사용자가 왜 밀려나는지가 핵심이다.
# 타입 스펙: type-swimlane — 가로 레인 하나에 주체 하나. 레인을 건너는 화살표가 인계이고,
#           마지막 인계(정상 사용자의 SYN 이 떨어지는 자리)만 강조한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 488
LX, LW, LANE_H, Y0 = 156, 828, 92, 108
NW, NH = 148, 52

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 07-01 §2",
      "SYN 홍수에서 벌어지는 일",
      "공격자·서버·정상 사용자 셋이 같은 시간축 위에서 무엇을 하는지. 서버가 자리를 잡아 두고 기다리는 동안 백로그가 차고, 마지막에 밀려나는 것은 공격자가 아니라 정상 사용자다.",
      "서버는 규격대로 행동하는데도 무너집니다 — 자리를 미리 잡아 두기 때문입니다")

LANES = [("공격자", "ATTACKER"), ("서버", "SERVER"), ("정상 사용자", "CLIENT")]
def lane_top(k): return Y0 + k * LANE_H
def lane_mid(k): return lane_top(k) + LANE_H / 2

for k, (name, eyebrow) in enumerate(LANES):
    d.line(LX, lane_top(k), LX + LW, lane_top(k), RULE, 1.0)
    d.t(20, lane_mid(k) - 2, name, 12, INK, KR, "start", 600)
    d.t(20, lane_mid(k) + 15, eyebrow, 9, SOFT, MONO, "start")
d.line(LX, lane_top(3), LX + LW, lane_top(3), RULE, 1.0)
d.line(LX, Y0, LX, lane_top(3), RULE, 1.0)

COLS = [168, 332, 496, 660, 824]
def cx(j): return COLS[j] - 8

def node(j, k, title, sub, focal=False):
    x, y = cx(j), lane_mid(k) - NH / 2
    if focal: d.tone(x, y, NW, NH, ACC, 6)
    else: d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + NW / 2, y + 21, title, 11, ACC if focal else INK, KR, "middle", 600)
    d.t(x + NW / 2, y + 39, sub, 11, MUTED, KR)

node(0, 0, "빠른 SYN 을 쏟기", "출발지는 대개 위조")
node(1, 1, "SYN-ACK 회신", "SYN_RECV 로 대기")
node(2, 0, "마지막 ACK 없음", "반쪽 연결로 남음")
node(3, 1, "재전송하며 기다림", "synack_retries 만큼")
node(3, 2, "정상 사용자의 SYN", "같은 포트로 들어옴")
node(4, 1, "자리가 없어 거절", "backlog 가 가득 참", focal=True)

def hand(j0, k0, j1, k1, c=MUTED, m="ar"):
    x0, y0 = cx(j0) + NW, lane_mid(k0)
    x1, y1 = cx(j1), lane_mid(k1)
    mid = (x0 + x1) / 2
    d.arrow([(x0, y0), (mid, y0), (mid, y1), (x1 - 4, y1)], c, m, 1.3)

hand(0, 0, 1, 1)
hand(1, 1, 2, 0)
hand(2, 0, 3, 1)
hand(3, 2, 4, 1, ACC, "acc")

d.t(LX, lane_top(3) + 28,
    "백로그 크기는 tcp_max_syn_backlog · 기다리는 횟수는 tcp_synack_retries · 자리를 아예 안 잡는 길이 tcp_syncookies 입니다",
    11, MUTED, KR, "start")

d.legend(H - 60, [("정상 사용자가 밀려나는 자리", ACC), ("레인을 건너는 인계", MUTED)])
d.save("07-01.syn-flood-lanes.svg")
