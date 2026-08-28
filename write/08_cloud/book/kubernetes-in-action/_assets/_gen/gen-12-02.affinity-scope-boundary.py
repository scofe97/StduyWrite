# 12-02 §3 — 다른 구간의 일이라 만나지 않는다
# 본문이 "정책과 무관해서가 아니라 애초에 다른 구간이라서"로 이유를 바꿔 놓는다.
# 그러니 구간 축 위에 소관 범위를 대괄호로 얹고, 겹치는 한 곳만 focal 로 짚는다.
# 타입 스펙: type-gantt.md — 요청 경로를 축으로 삼고 두 소관을 구간 막대로 얹는다. 두 구간이 겹치는 곳이 한 군데뿐이라는
#           것이 결론이라 구간의 시작·끝이 값이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1220, 596, "KUBERNETES IN ACTION · 12-02",
      "소관이 겹치는 곳은 한 군데뿐이다",
      "프록시는 cluster IP 를 건너뛰고 파드로 직접 보내므로, 프록시→백엔드 구간에는 Service 가 개입할 자리가 없다. "
      "externalTrafficPolicy 도 sessionAffinity 도 거기에는 닿지 않는다.",
      "요청 하나를 구간으로 갈라 보면")

NODE = [("클라이언트", "브라우저", 140), ("로드밸런서", "Service 소관", 430),
        ("L7 프록시", "여기서 TLS·라우팅", 720), ("백엔드 파드", "직접 닿는다", 1010)]
for t, s, cx in NODE:
    ddx.node(d, cx, 240, t, s, 220, 84, INFO)
for a, b in zip([n[2] for n in NODE], [n[2] for n in NODE][1:]):
    d.path(f"M {a+112} 240 L {b-116} 240", MUTED, 1.5, m="ar")

d.o.append(f'<rect x="322" y="184" width="216" height="112" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
ddx.node(d, 430, 240, "로드밸런서", "Service 소관", 220, 84, INFO)
d.t(430, 322, "여기서만 서로를 망칠 수 있다", 11, ACC, KR)

def span(x0, x1, y, label, c):
    d.path(f"M {x0} {y-8} L {x0} {y} L {x1} {y} L {x1} {y-8}", c, 1.3)
    d.t((x0 + x1) / 2, y + 20, label, 11, c, KR)

span(140, 720, 372, "Service 소관 — externalTrafficPolicy · sessionAffinity", SOFT)
span(720, 1010, 424, "프록시 소관 — 쿠키 어피니티 · 헤더 · 재작성", OK)

d.t(24, 486, "LB→프록시 구간에 Cluster 정책이 걸려 있으면 SNAT 때문에 프록시가 보는 클라이언트 IP 가 노드 IP 로 오염된다. "
             "IP 기반 어피니티가 무의미해지고 접근 로그의 출발지도 전부 노드 주소가 된다.", 11, MUTED, KR, "start")
d.t(24, 508, "그래서 실무에서는 컨트롤러의 LB Service 에 externalTrafficPolicy: Local 을 거는 것이 관행이다.",
     11, MUTED, KR, "start")
d.legend(534, [("요청 경로", INFO), ("프록시 소관", OK), ("겹치는 한 곳", ACC)])
d.save("12-02-affinity-scope-boundary.svg")
print("ok")
