# 13-01 §1 — 쪼갠 자리가 조직 경계와 맞는다
# 본문이 리소스 대응표보다 "결정 주체와 변경 빈도가 다르다"를 요점으로 둔다. 그러니 상자 대응이
# 아니라 누가 무엇을 소유하는지가 보이는 구조여야 한다. Route 를 뺀 자리가 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 720, "KUBERNETES IN ACTION · 13-01",
      "규칙을 뺀 자리에 조직 경계가 들어선다",
      "호스트·인증서·공인 IP 는 플랫폼 팀이 정하고 몇 년을 간다. 경로가 어느 서비스로 가는지는 앱 팀이 "
      "배포마다 바꾼다. 성격이 다른 둘이 한 오브젝트에 있으면 권한을 나눌 수가 없다.",
      "RBAC 은 오브젝트 단위라 '이 경로만'을 줄 수 없다")

ddx.band(d, 100, 340, "Ingress — 한 오브젝트 안에 다 있다", x=24, w=1172)
d.box(120, 158, 420, 150, PAPER2, WARN, 1.2, 8)
d.t(330, 186, "Ingress 하나", 13, WARN, KR, "middle", 600)
for i, line in enumerate(("host: api.example.com", "tls: secretName", "path /orders → orders",
                          "path /payments → payments")):
    d.t(330, 212 + i * 22, line, 10, MUTED, MONO)
for nm, cy in (("orders", 202), ("payments", 264)):
    ddx.node(d, 860, cy, nm, "Service", 180, 54, INFO)
    d.path(f"M 544 {233} L 766 {cy}", MUTED, 1.4, m="ar")
ddx.tag(d, 1080, 233, "권한을 나눌 수 없다", WARN, 210)
d.t(330, 322, "주문 팀에 수정 권한을 주면 결제 경로와 TLS 까지 열린다", 11, WARN, KR)

ddx.band(d, 364, 616, "Gateway API — Route 로 뺐다", x=24, w=1172)
d.box(120, 422, 260, 132, PAPER2, INFO, 1.2, 8)
d.t(250, 450, "Gateway", 13, INFO, KR, "middle", 600)
d.t(250, 472, "플랫폼 팀", 11, MUTED, KR)
for i, line in enumerate(("host · port", "인증서 · 공인 IP")):
    d.t(250, 500 + i * 20, line, 10, SOFT, MONO if i == 0 else KR)
for nm, team, cy in (("HTTPRoute", "주문 팀 · orders ns", 458), ("HTTPRoute", "결제 팀 · payments ns", 526)):
    d.o.append(f'<rect x="{560-140}" y="{cy-31}" width="280" height="62" rx="6" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(560, cy - 6, nm, 12, ACC, MONO, "middle", 600)
    d.t(560, cy + 16, team, 10, MUTED, KR)
    d.path(f"M 384 488 L 414 {cy}", INFO, 1.4, m="info")
    d.path(f"M 702 {cy} L 766 {cy}", ACC, 1.4, m="acc")
    ddx.node(d, 860, cy, nm.replace("HTTPRoute", "orders" if cy < 490 else "payments"), "Service", 180, 54, INFO)
ddx.tag(d, 1080, 492, "서로 못 건드린다", OK, 210)
d.t(560, 592, "RBAC 경계가 조직 경계와 맞아떨어진다", 11, ACC, KR)

d.t(24, 654, "Route 를 뺀 덕에 Gateway 가 작게 유지되고, HTTP 말고 TLS·gRPC·TCP·UDP 도 각자의 Route 로 붙는다. "
             "네임스페이스를 넘어 Gateway 를 공유할 수도 있다.", 11, MUTED, KR, "start")
d.legend(674, [("서비스·Gateway", INFO), ("빼낸 자리", ACC), ("나눌 수 없다", WARN)])
d.save("13-01-ingress-vs-gateway-api.svg")
print("ok")
