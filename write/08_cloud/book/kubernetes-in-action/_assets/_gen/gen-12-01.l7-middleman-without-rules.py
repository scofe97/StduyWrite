# 12-01 §7 — 규칙이 없어도 중간자가 생긴다
# 본문이 흔한 오해("Ingress 는 HTTP 를 쓰니까")를 먼저 걷어내고 "차이는 누가 HTTP 를
# 이해하느냐"로 옮긴다. 그러니 오가는 트래픽은 양쪽 같게 그리고, 중간자의 유무만 달라야 한다.
# 타입 스펙: type-data-flow.md — 같은 요청 경로에 중간자가 있고 없고를 두 밴드로 나눈 흐름.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 680, "KUBERNETES IN ACTION · 12-01",
      "규칙이 하나도 없어도 얻는 것",
      "LoadBalancer 로 노출한 앱도 HTTP 를 쓴다. 오가는 트래픽은 양쪽 다 같은 HTTP 이고, "
      "달라지는 것은 그 사이에 HTTP 를 이해하는 자가 서 있느냐다.",
      "규칙 없이 defaultBackend 만 둔 Ingress")

def row(y0, label, mid, mid_sub, mid_focal, verdict, verdict_c):
    ddx.band(d, y0, y0 + 216, label, x=24, w=1152)
    cy = y0 + 116
    ddx.node(d, 170, cy, "클라이언트", "GET /orders", 210, 84, INFO)
    ddx.node(d, 990, cy, "앱 파드", "같은 HTTP 를 받는다", 210, 84, INFO)
    if mid:
        ddx.node(d, 580, cy, mid, mid_sub, 260, 84, focal=mid_focal)
        d.path(f"M 278 {cy} L 442 {cy}", MUTED, 1.5, m="ar")
        d.path(f"M 714 {cy} L 878 {cy}", MUTED, 1.5, m="ar")
    else:
        d.path(f"M 278 {cy} L 878 {cy}", MUTED, 1.5, m="ar")
        d.t(580, cy - 14, "봉투를 열지 않고 지나 보낸다", 11, SOFT, KR)
    d.t(580, y0 + 190, verdict, 11, verdict_c, KR)

row(100, "LoadBalancer 로 노출", None, None, False,
    "HTTP 를 이해하는 자가 없다 — 할 수 있는 일도 없다", MUTED)
row(340, "규칙 없는 Ingress 로 노출", "L7 프록시", "봉투를 열어 읽는다", True,
    "규칙이 없어도 이 중간자가 선다는 것 자체가 이득이다", ACC)

d.t(24, 596, "그 중간자가 서는 순간 인프라 계층에서 가능해지는 것들 — "
             "TLS 종료 · HTTP 인증 · 쿠키 기반 세션 어피니티 · 헤더 조작 · URL 재작성 · 재시도 · rate limit.",
     11, MUTED, KR, "start")
d.t(24, 618, "경로로 가르는 일은 그 중간자가 할 수 있는 여러 일 가운데 하나일 뿐이다.", 11, MUTED, KR, "start")
d.legend(636, [("오가는 HTTP", INFO), ("HTTP 를 이해하는 자", ACC)])
d.save("12-01-l7-middleman-without-rules.svg")
print("ok")
