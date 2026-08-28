# 12-02 §4 — 이름으로 맞물린다
# 캡션이 "한 Ingress 에서 나가는 화살표는 언제나 하나"를 못박는다. 그러니 여러 Ingress 가
# 각자 클래스 하나를 지목하는 그림이어야 하고, 개수 관계가 함께 보여야 한다.
# 타입 스펙: type-dependency.md — Ingress 셋 → IngressClass 둘 → 컨트롤러 둘의 참조 팬인. 흐르는 것이 아니라 가리키는
#           관계라 data-flow 가 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 654, "KUBERNETES IN ACTION · 12-02",
      "이름 하나가 처리 주체를 정한다",
      "Ingress 는 클래스 이름만 알고, 그 클래스가 어느 컨트롤러인지 안다. 컨트롤러를 여럿 두는 의미는 "
      "트래픽을 나눠 갖는 것이 아니라 Ingress 집합, 곧 일감을 나눠 갖는 것이다.",
      "spec.ingressClassName → IngressClass.name → spec.controller")

ING = [("사내 관리자 페이지", "ingressClassName: nginx", 190, 0),
       ("외부 공개 API", "ingressClassName: alb-public", 320, 1),
       ("사내 API", "ingressClassName: alb-public", 450, 1)]
for t, s, cy, _ in ING:
    ddx.node(d, 180, cy, t, s, 280, 84, INFO)

CLS = [("IngressClass  nginx", "controller: k8s.io/ingress-nginx", 220),
       ("IngressClass  alb-public", "controller: ingress.k8s.aws/alb", 400)]
for t, s, cy in CLS:
    d.box(500, cy - 42, 320, 84, PAPER2, ACC, 1.2, 6)
    d.t(660, cy - 12, t, 12, ACC, MONO, "middle", 600)
    d.t(660, cy + 12, s, 10, MUTED, MONO)

CTL = [("ingress-nginx 컨트롤러", "프록시 파드를 세운다", 220),
       ("AWS Load Balancer 컨트롤러", "ALB 를 프로비저닝한다", 400)]
for t, s, cy in CTL:
    ddx.node(d, 1010, cy, t, s, 300, 84, OK)

for i, (_, _, cy, idx) in enumerate(ING):
    ty = CLS[idx][2]
    ay = ty + (0 if cy == ty else (-12 if cy < ty else 12))
    bx = 380 + i * 24
    d.path(f"M 322 {cy} L {bx} {cy} L {bx} {ay} L 494 {ay}", ACC, 1.4, m="acc")
for _, _, cy in CLS:
    d.path(f"M 822 {cy} L 854 {cy}", OK, 1.4, m="ok")

d.t(660, 496, "한 Ingress 에서 나가는 화살표는 언제나 하나다", 11, ACC, KR)
d.t(24, 540, "클래스를 안 적으면 기본 IngressClass 가 적용되고, 기본이 없으면 아무 컨트롤러도 처리하지 않아 "
             "ADDRESS 가 영원히 빈다.", 11, MUTED, KR, "start")
d.t(24, 562, "반대로 기본을 둘 이상 두면 여럿이 같은 Ingress 를 각자 처리해 로드밸런서가 중복 생성된다.",
     11, MUTED, KR, "start")
d.legend(590, [("Ingress", INFO), ("클래스가 잇는다", ACC), ("처리 주체", OK)])
d.save("12-02-ingressclass-relationship.svg")
print("ok")
