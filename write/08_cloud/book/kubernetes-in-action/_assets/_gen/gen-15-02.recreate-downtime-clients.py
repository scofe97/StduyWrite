# 15-02 §2 — 같은 순간인데 응답이 다른 이유
# 본문이 "요청을 받아 주는 주체가 있느냐"로 이유를 댄다. 그러니 두 경로를 나란히 두되
# 중간에 서 있는 것이 무엇인지가 보여야 한다. kube-proxy 모드 갈림도 함께 적는다.
# 타입 스펙: type-data-flow.md — 같은 요청 경로를 두 진입점으로 지나는 두 벌의 흐름. 파드가 없을 때 무엇이 응답하는지가
#           경로마다 달라진다는 것이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1200, 660, "KUBERNETES IN ACTION · 15-02",
      "받아 주는 주체가 있느냐가 응답을 가른다",
      "가용 파드가 0 인 같은 순간인데 경로마다 다른 답이 온다. Ingress 프록시는 자기가 살아 있으니 "
      "'보낼 곳이 없다'를 상태 코드로 만들어 돌려줄 수 있다.",
      "Recreate 의 가용 0 구간에 요청이 들어왔을 때")

def path_row(y0, label, mid, mid_sub, mid_c, ans, ans_sub, ans_c, why):
    ddx.band(d, y0, y0 + 200, label, x=24, w=1152)
    cy = y0 + 112
    ddx.node(d, 160, cy, "클라이언트", "GET /", 200, 76, INFO)
    ddx.node(d, 480, cy, mid, mid_sub, 260, 76, mid_c)
    d.path(f"M 262 {cy} L 348 {cy}", MUTED, 1.5, m="ar")
    ddx.node(d, 800, cy, "파드", "하나도 없다", 200, 76, dim=True)
    d.path(f"M 612 {cy} L 698 {cy}", BAD, 1.4, m="bad", dash="5 5")
    ddx.tag(d, 1050, cy - 14, ans, ans_c, 220)
    d.t(1050, cy + 24, ans_sub, 10, MUTED, KR)
    d.t(480, y0 + 176, why, 11, SOFT, KR)

path_row(100, "Ingress 프록시를 거칠 때", "L7 프록시", "자기는 살아 있다", ACC,
         "503 Service Unavailable", "상태 코드를 만들어 돌려준다", ACC,
         "보낼 곳이 없다는 사실을 HTTP 로 표현할 수 있다")
path_row(324, "ClusterIP 로 직접 갈 때", "노드 커널", "EndpointSlice 가 비었다", INFO,
         "연결 거부", "iptables · nftables 모드", BAD,
         "readiness 를 잃은 주소는 명단에서 빠져 전달할 백엔드가 없다")

d.t(24, 570, "빈 ClusterIP 의 반응은 kube-proxy 모드에 따라 갈린다. iptables·nftables 는 거부 규칙을 심어 "
             "연결 거부가 오지만, IPVS 는 그런 경로가 없어 빈 virtual server 로 남아 타임아웃이 될 수 있다.",
     11, MUTED, KR, "start")
d.t(24, 592, "어느 모드인지는 kube-system 의 kube-proxy ConfigMap 에서 mode 필드로 확인한다.", 11, MUTED, KR, "start")
d.legend(614, [("클라이언트", INFO), ("답을 만들어 주는 주체", ACC), ("끊기는 자리", BAD)])
d.save("15-02-recreate-downtime-clients.svg")
print("ok")
