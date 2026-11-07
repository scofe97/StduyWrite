# 11-03 §2 — headless 는 파드 IP 를 그대로 돌려준다
# 이름 해석에서 직접 연결까지의 한 줄 흐름. 파드로 뻗는 화살표의 출발점을 '클라이언트가 받은
# 목록'으로 이름 붙였다 — DNS 가 파드에 붙는 것처럼 읽히면 안 된다.
# 타입 스펙: type-architecture.md — 클라이언트 파드 · cluster DNS · 파드 넷을 잇는 구성도. 목록에서 파드로 갈라지는 팬아웃이 논지다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
# 폭 1000 이하 — 노드 폭을 줄이고 서술 캡션은 본문에 맡긴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1000, 516, "KUBERNETES IN ACTION · 11-03",
      "headless 는 파드 IP 를 그대로 돌려준다",
      "clusterIP 를 None 으로 두면 cluster DNS 가 가상 주소 하나가 아니라 뒷받침 파드마다 A 레코드를 답한다. "
      "클라이언트는 그 목록을 받아 파드에 직접 붙는다.",
      "quote-headless · clusterIP: None")

IPS = ("10.244.1.10", "10.244.2.8", "10.244.2.10", "10.244.3.4")

ddx.node(d, 94, 300, "클라이언트 파드", "getAllByName", 140, 88, INFO)
ddx.node(d, 323, 300, "cluster DNS", "CoreDNS 가 답한다", 150, 88)
d.box(482, 244, 190, 112, PAPER2, ACC, 1.4, 6)
d.t(577, 274, "클라이언트가 받은 목록", 13, ACC, KR, "middle", 600)
for i, ip in enumerate(IPS):
    d.t(577, 296 + i * 17, ip, 10, MUTED, MONO)

d.path("M 170 300 L 242 300", MUTED, 1.5, m="ar")
d.t(206, 286, "이름을 묻는다", 11, SOFT, KR)
d.path("M 404 300 L 476 300", MUTED, 1.5, m="ar")
d.t(440, 286, "A 레코드 4 개", 11, SOFT, KR)

PODY = (176, 250, 324, 398)
d.path("M 678 300 L 730 300", OK, 1.3)
d.path(f"M 730 {PODY[0]} L 730 {PODY[-1]}", OK, 1.3)
for i, cy in enumerate(PODY):
    ddx.node(d, 891, cy, f"파드 {i+1}", IPS[i], 170, 58, INFO)
    d.path(f"M 730 {cy} L 800 {cy}", OK, 1.3, m="ok")
d.t(730, 444, "앱이 목록을 돌며 직접 붙는다", 11, OK, KR)

d.legend(474, [("클라이언트와 파드", INFO), ("앱이 쥔 목록", ACC), ("직접 연결", OK)])
d.save("11-03-headless-service-dns.svg")
print("ok")
