# 12-01 진입 — 이름은 여럿, IP 는 하나
# 캡션이 "DNS 레코드가 모두 같은 Ingress IP 를 가리킨다"를 요구한다. 수렴한 뒤 다시
# 갈라지는 형태여야 그 말이 눈에 보인다. 수렴점 하나만 focal.
# 타입 스펙: type-data-flow.md — 이름 셋이 공인 IP 하나로 몰렸다가 프록시를 지나 서비스 셋으로 갈라진다 — 수렴이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1220, 560, "KUBERNETES IN ACTION · 12-01",
      "이름은 여럿, 공인 IP 는 하나",
      "도메인마다 A 레코드를 두지만 값은 모두 같은 주소다. 갈라 보내는 일은 DNS 가 아니라 "
      "그 주소 뒤에 선 L7 프록시가 HTTP 를 읽어서 한다.",
      "kiada · quote · quiz 를 한 IP 로")

HOSTS = [("kiada.example.com", "A → 11.22.33.44"),
         ("api.example.com/quote", "A → 11.22.33.44"),
         ("api.example.com/questions", "A → 11.22.33.44")]
YS = (190, 285, 380)
for (h, rec), y in zip(HOSTS, YS):
    ddx.node(d, 190, y, h, rec, 300, 66, INFO)
    d.path(f"M 342 {y} L 392 {y} L 392 285", MUTED, 1.4) if y != 285 else None
d.path("M 342 285 L 392 285", MUTED, 1.4)
d.path("M 392 285 L 452 285", MUTED, 1.5, m="ar")

ddx.node(d, 560, 285, "11.22.33.44", "Ingress 의 공인 IP", 200, 84, focal=True)
d.path("M 662 285 L 726 285", MUTED, 1.5, m="ar")
ddx.node(d, 840, 285, "L7 프록시", "HTTP 를 읽어 규칙에 맞춘다", 220, 84)

d.path("M 952 285 L 990 285", OK, 1.4)
d.path(f"M 990 {YS[0]} L 990 {YS[-1]}", OK, 1.4)
for nm, y in zip(("kiada", "quote", "quiz"), YS):
    ddx.node(d, 1110, y, nm, "ClusterIP", 160, 66, OK)
    d.path(f"M 990 {y} L 1026 {y}", OK, 1.4, m="ok")

d.t(24, 486, "그래서 서비스를 더 내보내도 DNS 에 추가되는 값은 같고, 늘어나는 것은 프록시가 읽을 규칙 줄뿐이다.",
     11, MUTED, KR, "start")
d.legend(506, [("도메인 이름", INFO), ("모두 가리키는 한 곳", ACC), ("갈라진 목적지", OK)])
d.save("12-01-ingress-overview.svg")
print("ok")
