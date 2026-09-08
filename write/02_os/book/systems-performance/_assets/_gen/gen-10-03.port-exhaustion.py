# 10-03 §2 — 포트 고갈이 왜 확장성 문제가 되는가.
# 타입 스펙: type-process — 연결을 구분하는 네 요소에서 하나만 남는 과정, 그리고 그 하나가 바닥나는 조건.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 512
CW, CH, GAP, X0, Y = 208, 116, 24, 24, 124

d = DK(W, H, "SYSTEMS PERFORMANCE · 10-03 §2",
       "포트 고갈 — 남는 것이 하나뿐일 때",
       "한 서버가 같은 목적지로만 연결하면 4-튜플 중 셋이 고정된다. 연결을 구분하는 것은 클라이언트 ephemeral 포트 하나뿐이고, 그 하나가 바닥난다.",
       "같은 목적지로 자주 연결하면 구분할 수단이 포트 하나만 남습니다")

TUPLE = [
    ("출발지 IP", "내 서버 — 고정", None),
    ("목적지 IP", "같은 상대 — 고정", None),
    ("목적지 포트", "같은 서비스 — 고정", None),
    ("출발지 포트", "이것만 변한다", ACC),
]

for i, (name, sub, c) in enumerate(TUPLE):
    x = X0 + i * (CW + GAP)
    if c: d.tone(x, Y, CW, CH, c, 8)
    else: d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 34, name, 14, c if c else INK, KR, "start", 600)
    d.t(x + 16, Y + 62, sub, 13, MUTED, KR, "start")
    d.t(x + 16, Y + CH - 20, "고정" if not c else "가변", 13, SOFT if not c else c, KR, "start")

YB = Y + CH + 44
d.box(X0, YB - 24, 880, 96, PAPER2, RULE, 1.0, 8)
d.t(X0 + 20, YB, "바닥나는 조건", 14, WARN, KR, "start", 600)
d.t(X0 + 20, YB + 26, "이론상 16비트 65,536개지만 Linux 기본 범위는 32768~60999 로 약 28,000개입니다.", 13, MUTED, KR, "start")
d.t(X0 + 20, YB + 48, "TIME_WAIT 가 60초쯤 잡고 있어, 그 사이 이 수를 넘는 연결율이면 충돌합니다.", 13, MUTED, KR, "start")

d.t(X0, YB + 104, "TIME_WAIT 중인 포트로 SYN 을 보내면 옛 연결의 일부로 오인돼 거부될 수 있습니다. 다중 IP 나 SO_LINGER 가 해법입니다.",
    13, MUTED, KR, "start")

d.legend(YB + 128, [("연결을 구분하는 유일한 축", ACC), ("고정되는 축", MUTED), ("고갈 조건", WARN)])
d.save("10-03.port-exhaustion.svg")
