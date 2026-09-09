# 02-05.who-answers — 같은 "안 된다"가 갈리는 자리와 거절을 지어낸 쪽
# 본문 요구: §1 은 세 가지를 따로 말한다 — DROP 은 5.062초 침묵, REJECT 는 0.036초 거절,
#           그리고 "커널 기본 동작 vs 규칙"이 RST 와 ICMP 를 가른다는 교정.
#           셋이 한 그림에 없으면 독자는 '중간이냐 끝이냐'로 다시 묶어 읽는다.
#           응답 화살표가 *어느 레인에서 출발하는가* 로 그 축을 눈에 보이게 만든다.
# 타입 스펙: type-sequence.md — 시간축이 논지다(5.062s 대 0.036s). 참여자 3(≤5),
#           메시지 4(≤12), 프래그먼트 1(≤1), alt 영역 2(≤2). 응답은 점선 + 채운 마커.
#           coral 은 헤드라인 하나 — br0 이 지어낸 ICMP.
import dd, ddx
from dd import Seq, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 848
d = Seq(W, H, "BLOCKED · WHO ANSWERS",
      "거절을 지어낸 쪽은 목적지가 아니다",
      "규칙이 없으면 목적지 커널이 RST 를 보냅니다. 중간에 규칙이 있으면 그 자리가 답을 지어내고, "
      "DROP 이면 아무것도 안 지어내 상대가 한도까지 기다립니다.",
      lead="응답이 어느 레인에서 출발하는가가 '누가 막았나'를 말한다")

LX = d.lanes([("ns1", "10.10.1.11"),
                  ("br0 · 중계", "10.10.1.1 · 규칙이 있는 자리"),
                   ("ubuntu2", "192.168.139.238")], y0=104, lane_w=212)
RAIL_BOT = 712
d.rails(RAIL_BOT)

# ── 기준선: 규칙이 없을 때 ──────────────────────────────────────────
d.t(36, 182, "규칙이 없다면 — 기준선", 12, SOFT, KR, "start", 600)

# ns1 ↔ ubuntu2 를 잇는 화살표는 br0 의 레인을 가로지른다. d.msg 는 라벨을 중점에 두는데
# 그 중점이 정확히 br0 의 레인 x 라, 라벨이 남의 레인 위에 앉는다(type-sequence 안티패턴).
# 화살표만 d.msg 로 그리고 라벨은 br0 과 ubuntu2 사이 빈 구간으로 뺀다.
LBL_X = (LX["br0 · 중계"] + LX["ubuntu2"]) / 2
def baseline(a, b, label, sub, y, c, dash=None):
    d.msg(a, b, "", y, c, dash=dash)
    d.t(LBL_X, y - 9, label, 11, c, MONO, "middle", 600)
    d.t(LBL_X, y + 15, sub, 11, MUTED)

baseline("ns1", "ubuntu2", "SYN", "중계는 그냥 넘긴다", 214, MUTED)
baseline("ubuntu2", "ns1", "RST", "그 포트에 소켓이 없다 — 커널의 기본 동작", 262, INFO, dash="5 4")
d.t(36, 300, "출발지가 목적지 IP — 도달에는 성공했다는 뜻", 11, MUTED, KR, "start")

d.line(36, 320, W - 48, 320, RULE, 1.0, "4 5")

# ── alt 프레임: 중계에 규칙을 걸었을 때 ─────────────────────────────
# 상태 칩이 레인 중심에 걸리므로 프레임을 칩 반폭보다 넓게 잡는다 — 변을 타면 lint 가 잡는다
FX0, FX1 = LX["ns1"] - 92, LX["br0 · 중계"] + 92
FY0, FY1 = 344, 706
d.box(FX0, FY0, FX1 - FX0, FY1 - FY0, "rgba(245,245,245,0.04)", "rgba(245,245,245,0.22)", 1, 4)
d.box(FX0, FY0, 44, 16, PAPER, "rgba(245,245,245,0.22)", 1, 2)
d.t(FX0 + 22, FY0 + 12, "ALT", 11, MUTED, MONO)

d.t(FX0 + 12, FY0 + 38, "[-j DROP]", 11, MUTED, MONO, "start")
d.msg("ns1", "br0 · 중계", "SYN", 420, MUTED, sub="10.10.1.11 → 192.168.139.238:9000")
d.state("br0 · 중계", "버린다 · 답을 안 만든다", 468, MUTED)
d.state("ns1", "5.062 s timed out", 512, MUTED)

d.line(FX0 + 8, 540, FX1 - 8, 540, "rgba(245,245,245,0.20)", 1.0, "4 3")

d.t(FX0 + 12, 566, "[-j REJECT]", 11, MUTED, MONO, "start")
d.msg("ns1", "br0 · 중계", "SYN", 604, MUTED)
d.msg("br0 · 중계", "ns1", "ICMP port unreachable", 646, ACC, dash="5 4",
      sub="출발지 10.10.1.1 — br0 이 지어냈다")
d.state("ns1", "0.036 s refused", 686, ACC)

# 목적지 레인은 두 갈래 내내 비어 있다 — 그것이 §1 의 논점이다.
# 칩만 한 점에 두면 위 영역(DROP)에만 걸린 것처럼 읽히므로, 프레임 높이만큼 레인을
# 굵게 덧그어 두 영역 모두에 걸친다는 것을 폭으로 말한다.
UX = LX["ubuntu2"]
d.line(UX, FY0, UX, FY1, SOFT, 2.0, "3 6")
d.state("ubuntu2", "이 연결을 본 적 없다", (FY0 + FY1) / 2, SOFT)

d.t(36, 744, "출발지 IP 는 '중간이냐 끝이냐'만 가르고, '규칙이냐 소켓 없음이냐'는 프로토콜이 가릅니다.",
     12, MUTED, KR, "start")
d.t(36, 766, "--reject-with tcp-reset 을 쓰면 방화벽이 낸 거절인데 소켓 없음처럼 보이게 위장할 수도 있습니다.",
     12, MUTED, KR, "start")
d.legend(786, [("커널 기본 동작 — RST", INFO), ("규칙이 지어낸 거절 — ICMP", ACC)])
d.save("02-05.who-answers.svg")
print("ok who-answers")
