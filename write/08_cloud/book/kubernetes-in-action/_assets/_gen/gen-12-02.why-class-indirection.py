# 12-02 §4 — 한 단계가 무엇을 가능하게 하나
# 본문이 "직접 적는 구조였다면 이 구분이 불가능하다"고 반사실로 설명한다. 그러니 두 구조를
# 나란히 놓고, 위쪽에서 구별이 안 된다는 사실 자체를 보여야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1200, 684, "KUBERNETES IN ACTION · 12-02",
      "설정 묶음마다 붙일 이름이 필요했다",
      "같은 컨트롤러를 다른 파라미터로 여러 번 쓰려면 컨트롤러 이름 말고 따로 붙일 이름이 있어야 한다. "
      "참조가 한 단계 늘어나는 대신 설정을 갈라 둘 자리를 얻는다.",
      "ALB 컨트롤러 하나로 public 과 internal 을 나누려면")

ddx.band(d, 100, 316, "컨트롤러를 직접 적는다면", x=24, w=1152)
for t, cy in (("사내 API", 186), ("외부 공개 API", 262)):
    ddx.node(d, 200, cy, t, "controller: ingress.k8s.aws/alb", 300, 62, INFO)
    d.path(f"M 352 {cy} L 480 {cy}", MUTED, 1.4)
d.path("M 480 186 L 480 262", MUTED, 1.4)
d.path("M 480 224 L 600 224", MUTED, 1.4, m="ar")
ddx.node(d, 760, 224, "ALB 컨트롤러", "둘 다 같은 이름을 적었다", 300, 76)
ddx.tag(d, 1020, 224, "구별할 방법이 없다", BAD, 220)

ddx.band(d, 340, 588, "클래스를 한 단계 두면", x=24, w=1152)
for t, cy, cls in (("사내 API", 426, "alb-internal"), ("외부 공개 API", 502, "alb-public")):
    ddx.node(d, 200, cy, t, f"ingressClassName: {cls}", 300, 62, INFO)
for cls, param, cy in (("alb-internal", "scheme: internal", 426), ("alb-public", "scheme: internet-facing", 502)):
    d.o.append(f'<rect x="{600-140}" y="{cy-31}" width="280" height="62" rx="6" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(600, cy - 6, cls, 12, ACC, MONO, "middle", 600)
    d.t(600, cy + 16, param, 10, MUTED, MONO)
    d.path(f"M 352 {cy} L 454 {cy}", ACC, 1.4, m="acc")
    d.path(f"M 742 {cy} L 786 {cy}", OK, 1.4)
d.path("M 786 426 L 786 502", OK, 1.4)
d.path("M 786 464 L 830 464", OK, 1.4, m="ok")
ddx.node(d, 990, 464, "ALB 컨트롤러", "같은 컨트롤러, 다른 설정", 300, 76, OK)
d.t(600, 552, "이름이 경계가 되어 앱 쪽은 클래스 이름 하나만 알면 된다", 11, ACC, KR)

d.t(24, 616, "클래스 파라미터가 Ingress annotation 을 이긴다. 앱 쪽에서 scheme: internet-facing 을 적어도 "
             "클래스가 internal 로 못 박아 두었으면 공인 IP 가 열리지 않는다 — 인프라팀의 결정이 뚫리지 않는다.",
     11, MUTED, KR, "start")
d.legend(636, [("Ingress", INFO), ("갈라 둘 자리", ACC), ("한 컨트롤러", OK), ("구별 불가", BAD)])
d.save("12-02-why-class-indirection.svg")
print("ok")
