# 12-01 §2 — Ingress 는 LoadBalancer 를 없앤 게 아니라 그 위에 얹혔다
# 본문이 "진화가 아니라 계층별 도구"라고 못박으므로, 아래 구조에서도 LB 가 사라지지 않고
# 프록시 앞에 그대로 남아 있는 것이 도식의 요점이다. 늘어나는 것은 규칙 줄 수뿐이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 880, "KUBERNETES IN ACTION · 12-01",
      "LB 셋이냐, LB 하나에 규칙 셋이냐",
      "서비스를 더 내보낼 때 무엇이 늘어나는지가 두 구조를 가른다. 공인 IP 가 늘면 요금이 늘고, "
      "규칙 줄이 늘면 아무것도 늘지 않는다.",
      "kiada · quote · quiz 세 서비스를 밖으로")

SVC = ("kiada", "quote", "quiz")

# 위 — LoadBalancer 셋
ddx.band(d, 100, 410, "서비스마다 LoadBalancer", x=24, w=1152)
for i, (nm, y) in enumerate(zip(SVC, (180, 250, 320))):
    ddx.node(d, 250, y, f"클라이언트 {i+1}", "각자 다른 IP", 180, 58)
    ddx.node(d, 560, y, "LoadBalancer", f"공인 IP {i+1}", 190, 58, WARN)
    ddx.node(d, 860, y, nm, "ClusterIP", 150, 58, INFO)
    d.path(f"M 344 {y} L 461 {y}", MUTED, 1.4, m="ar")
    d.path(f"M 659 {y} L 781 {y}", MUTED, 1.4, m="ar")
d.t(1060, 254, "IP 가 서비스 수만큼", 11, WARN, KR)
d.t(600, 380, "서비스를 하나 더 내보내면 공인 IP 도 하나 더 든다", 11, WARN, KR)

# 아래 — LB 하나 + 프록시 + 규칙
ddx.band(d, 434, 744, "LoadBalancer 하나 + 프록시 + 규칙", x=24, w=1152)
ddx.node(d, 250, 589, "클라이언트", "IP 하나만 안다", 180, 58)
ddx.node(d, 520, 589, "LoadBalancer", "공인 IP 1 개", 190, 58, OK)
d.path("M 344 589 L 421 589", MUTED, 1.4, m="ar")
d.path("M 619 589 L 696 589", MUTED, 1.4, m="ar")
d.o.append(f'<rect x="700" y="499" width="180" height="180" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(790, 528, "L7 프록시", 13, ACC, KR, "middle", 600)
d.t(790, 549, "규칙으로 가른다", 11, MUTED, KR)
RULES = ("host: kiada", "path: /quote", "path: /questions")
for rule, ry, sy, nm in zip(RULES, (588, 613, 638), (519, 589, 659), SVC):
    d.t(790, ry, rule, 10, ACC, MONO)
    d.path(f"M 884 {ry-4} L 961 {sy}", ACC, 1.3, m="acc")
    ddx.node(d, 1040, sy, nm, "ClusterIP", 150, 58, INFO)
ddx.focal_tag(d, 790, 714, "늘어나는 건 규칙 줄뿐", 200)

d.t(24, 790, "그러니 NodePort·LoadBalancer·Ingress 는 진화 단계가 아니라 계층별 도구다. "
             "위가 아래를 대체하지 않고 그 위에 쌓인다.", 11, MUTED, KR, "start")
d.t(24, 812, "위층이 늘 나은 것도 아니다. L7 은 '이 트래픽은 HTTP 다'라는 가정을 산 대가로 경로 라우팅을 얻었다 — "
             "DB 연결·gRPC 스트림·게임 UDP 에는 LoadBalancer 가 정답이다.", 11, MUTED, KR, "start")
d.legend(832, [("서비스", INFO), ("IP 가 는다", WARN), ("IP 는 하나", OK), ("규칙만 는다", ACC)])
d.save("12-01-lb-plus-proxy-stacking.svg")
print("ok")
