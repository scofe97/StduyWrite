# 08-01 §1 — 질의 하나가 라벨 조합을 타고 어느 카운터로 가는가. 시계열 수가 라벨의 곱이라는 것이 요점.
# 원문 근거: 표 8-1 의 coredns_dns_request_count_total 라벨은 server, zone, proto, family 넷.
#            현재 문서는 이름을 coredns_dns_requests_total 로 바꾸고 view 와 type 을 더해 여섯이다.
#            "coredns_dns_requests_total{server, zone, view, proto, family, type}" (coredns.io/plugins/metrics/)
# 타입 스펙: type-tree — 질의 하나가 라벨 축을 따라 갈라져 잎이 곧 시계열 하나가 된다.
#           갈래 수의 곱이 잎의 수라는 것이 트리로만 보이는 사실이다.
#           축약: 라벨마다 값이 여럿이라 실제 잎은 곱만큼이지만 그것을 다 그리면 읽히지 않는다.
#           그래서 축만 줄기에 걸고 잎 하나를 오른쪽에 펼쳐 보인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 880, 560
d = D(W, H, "LEARNING COREDNS · 08-01 §1",
      "질의 하나가 라벨 조합을 타고 카운터가 된다",
      "지표는 질의를 줄이 아니라 카운터 증가로 바꾼다. 다만 카운터가 라벨 조합마다 따로 생겨서, "
      "시계열 수는 각 라벨이 가지는 값의 곱으로 늘어난다.",
      "주황이 원서 이후 새로 붙은 라벨입니다")

ROWS = [("질의 한 건", 120, INK, False),
        ("server", 190, MUTED, False),
        ("zone", 250, MUTED, False),
        ("view", 310, ACC, True),
        ("proto · family", 370, MUTED, False),
        ("type", 430, ACC, True)]

# 줄기
d.path("M 150 140 L 150 448", MUTED, 1.4)

for name, y, c, new in ROWS[1:]:
    d.path(f"M 150 {y} L 190 {y}", c, 1.3, m="acc" if new else "ar")
    if new:
        d.tone(196, y - 17, 150, 34, ACC, 6, "12", 1.3)
    else:
        d.box(196, y - 17, 150, 34, PAPER2, RULE, 1.0)
    d.t(271, y + 5, name, 12, c, MONO)

d.box(60, 100, 180, 40, PAPER2, RULE, 1.0)
d.t(150, 125, "질의 한 건", 13, INK, KR, "middle", 600)

# 오른쪽 — 잎이 곧 시계열
d.box(400, 100, 450, 200, PAPER, RULE, 0.8)
d.t(416, 126, "잎 하나가 시계열 하나다", 13, INK, KR, "start", 600)
d.t(416, 152, "coredns_dns_requests_total{", 11, MUTED, MONO, "start")
d.t(432, 174, "server=\"dns://:53\", zone=\"cluster.local.\",", 11, MUTED, MONO, "start")
d.t(432, 194, "view=\"\",", 11, ACC, MONO, "start")
d.t(486, 194, "proto=\"udp\", family=\"1\",", 11, MUTED, MONO, "start")
d.t(432, 214, "type=\"A\"", 11, ACC, MONO, "start")
d.t(416, 234, "}", 11, MUTED, MONO, "start")
d.t(416, 268, "라벨 여섯이 각각 가지는 값의 곱만큼 생긴다", 12, MUTED, KR, "start")

d.tone(400, 320, 450, 128, ACC, 6, "0E", 1.3)
d.t(416, 346, "지표의 손잡이는 이 라벨 축이다", 13, ACC, KR, "start", 600)
d.t(416, 372, "존이 많고 질의 유형이 다양하면 시계열이 곱셈으로 늘어난다", 12, MUTED, KR, "start")
d.t(416, 396, "원서 표 8-1 의 라벨은 넷이었다", 12, MUTED, KR, "start")
d.t(416, 420, "server · zone · proto · family", 11, MUTED, MONO, "start")

d.box(20, 468, 840, 40, PAPER, RULE, 0.8)
d.t(36, 493, "같은 질의가 log 에서는 줄 하나가 되고 지표에서는 카운터 하나가 1 오른다 — 저장되는 것이 사건이 아니라 사건의 수다",
     12, MUTED, KR, "start")

d.legend(520, [("원서 이후 붙은 라벨", ACC), ("원서에도 있던 라벨", MUTED)])
d.save("08-01.metric-labels.svg")
