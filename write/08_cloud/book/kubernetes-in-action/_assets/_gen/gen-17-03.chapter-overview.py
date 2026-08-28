# 17-03 전체 지도 — 같은 노드로만 보내려면
# 본문이 구조를 직접 준다 — "맨 위가 풀어야 할 문제", "점선 아래 세 방법은 순서가 아니라
# 병렬 대안". 색은 두 군데로, 붉은은 §2 의 노출면, 앰버는 §3 의 엔드포인트 0 이다.
# 타입 스펙: type-dp-security-matrix.md — 가운데 세 칸이 세 방법을 같은 슬롯(이름 · 무엇을 한다 · 주의)으로 늘어놓은 격자다.
#           본문이 "순서가 아니라 병렬 대안"이라 못박아 칸 사이에 화살표를 두지 않았고, 위아래의
#           문제·판정 상자는 격자 밖 틀이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 680, "KUBERNETES IN ACTION · 17-03",
      "같은 노드로만 보내려면",
      "클라이언트 파드가 항상 같은 노드의 daemon 파드에 닿게 하는 방법이 셋이다. 어느 것을 골라도 "
      "목적지는 같고, 노드 IP 를 거치느냐 Service 이름으로 닿느냐가 갈린다.",
      "§1 hostPort · §2 hostNetwork · §3 Local Service · §4 판정")

d.box(340, 160, 540, 84, PAPER2, INFO, 1.2, 8)
d.t(610, 192, "풀어야 할 문제", 13, INFO, KR, "middle", 600)
d.t(610, 216, "클라이언트 파드가 같은 노드의 에이전트에만 연결되게 하려면", 11, MUTED, KR)

d.line(60, 280, 1160, 280, RULE, 1.0, "7 6")
d.t(60, 302, "아래 셋은 순서가 아니라 병렬 대안이다", 10, SOFT, KR, "start")

WAYS = [("§1  hostPort", "노드 포트를 컨테이너로 포워딩", "노드 IP 로 닿는다", None),
        ("§2  hostNetwork", "에이전트가 노드 포트에 직접 바인딩", "임의 포트에 바인딩할 수 있어 노출면이 넓다", BAD),
        ("§3  Local Service", "Service 이름만으로 같은 노드에", "에이전트 없는 노드에서는 엔드포인트 0 개처럼", WARN)]
BW = 340
for i, (t, s, note, c) in enumerate(WAYS):
    x = 60 + i * (BW + 40)
    if c:
        d.box(x, 330, BW, 156, PAPER2, RULE, 0.9, 8)
        d.o.append(f'<rect x="{x}" y="330" width="4" height="156" rx="2" fill="{c}"/>')
    else:
        d.box(x, 330, BW, 156, PAPER2, RULE, 0.9, 8)
    d.t(x + 26, 366, t, 13, c or INK, KR, "start", 600)
    d.t(x + 26, 394, s, 11, MUTED, KR, "start")
    if note and c:
        d.t(x + 26, 440, "주의", 10, c, KR, "start")
        d.t(x + 26, 462, ddx.fit(note, 10, BW - 52, note), 10, c, KR, "start")
    else:
        d.t(x + 26, 440, note, 11, SOFT, KR, "start")

d.box(340, 516, 540, 76, PAPER2, INFO, 1.2, 8)
d.t(610, 546, "§4  판정", 13, INFO, KR, "middle", 600)
d.t(610, 570, "셋 중 무엇을 언제 쓸지 정한다", 11, MUTED, KR)

d.legend(620, [("문제와 판정", INFO), ("노출면이 넓다", BAD), ("빈 채로 동작한다", WARN)])
d.save("17-03.chapter-overview.svg")
print("ok")
