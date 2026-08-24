# 04-01 §리소스와 오브젝트는 같은 말이 아니다
# 본문·옛 도식: 하나의 오브젝트가 여러 리소스(URI)로 노출되고, 어떤 리소스는 아무 오브젝트도
#   가리키지 않는다(subjectaccessreviews 는 권한 여부만 응답). apps/v1 과 extensions/v1beta1 은
#   같은 객체의 다른 표현이다.
# 타입 스펙: 왼쪽 창구와 오른쪽 대상이 1:1 이 아니라는 것이 요점이므로 참조 매핑으로 두되,
#           '가리키는 것이 없는' 리소스를 맨 위에 따로 두어 그 예외가 눈에 먼저 들어오게 한다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 640
d = D(W, H, "KUBERNETES IN ACTION · 04-01",
      "리소스는 창구이고 오브젝트는 대상이다 — 1:1 이 아니다",
      "같은 Deployment 오브젝트가 apps/v1 과 extensions/v1beta1 두 스키마의 리소스로 노출되고, "
      "어떤 리소스는 아무 오브젝트도 가리키지 않고 판정만 돌려준다.",
      lead="리소스는 상호작용하는 창구(뷰)이고 오브젝트는 저장되는 대상(테이블)이다")

RX, OX = 320, 800
RW, OW = 560, 280

ddx.band(d, 104, 584, "URI 가 다르다고 다른 오브젝트가 아니고, URI 가 있다고 오브젝트가 있는 것도 아니다")

d.t(RX, 190, "리소스 — 창구(URI)", 12, SOFT, KR, "middle", 600)
d.t(OX, 190, "오브젝트 — 저장되는 대상", 12, SOFT, KR, "middle", 600)

def uri(cy, path, c):
    d.box(RX - RW // 2, cy - 24, RW, 48, PAPER2, c, 1.1, 5)
    d.t(RX - RW // 2 + 16, cy + 5, ddx.fit(path, 11, RW - 32, path), 11, c, MONO, "start")

def obj(cy, h, t, s, c):
    d.box(OX - OW // 2, cy - h // 2, OW, h, PAPER2, c, 1.1, 6)
    d.t(OX, cy - 6, t, 13, c, KR, "middle", 600)
    d.t(OX, cy + 16, s, 10, SOFT, KR)

uri(228, "/apis/authorization.k8s.io/v1/subjectaccessreviews", BAD)
obj(228, 60, "가리키는 오브젝트 없다", "권한 여부만 응답한다", BAD)
d.path(f"M {RX+RW//2+6} 228 L {OX-OW//2-10} 228", BAD, 1.6, m="bad")

for i, (cy, path) in enumerate([
        (320, "/apis/apps/v1/…/deployments"),
        (376, "/apis/apps/v1/…/deployments/mydeploy"),
        (432, "/apis/extensions/v1beta1/…/deployments"),
        (488, "/apis/extensions/v1beta1/…/deployments/mydeploy")]):
    uri(cy, path, OK if i < 2 else INFO)

obj(404, 120, "Deployment mydeploy", "저장되는 것은 이 하나뿐이다", ACC)

SPINE = 660
d.path(f"M {RX+RW//2+6} 320 L {SPINE} 320", OK, 1.4)
d.path(f"M {RX+RW//2+6} 376 L {SPINE} 376", OK, 1.4)
d.path(f"M {RX+RW//2+6} 432 L {SPINE} 432", INFO, 1.4)
d.path(f"M {RX+RW//2+6} 488 L {SPINE} 488", INFO, 1.4)
d.path(f"M {SPINE} 320 L {SPINE} 488", MUTED, 1.4)
d.path(f"M {SPINE} 404 L {OX-OW//2-10} 404", ACC, 1.8, m="acc")
d.o.append(f'<circle cx="{SPINE}" cy="404" r="4" fill="{INK}"/>')
# 칩(168px)이 URI 상자(40~600)를 84px 덮는다 — 상자 위 빈 행에 마스크 없이 적는다
d.t(660, 290, "넷 다 같은 것을 가리킨다", 11, ACC, KR)

d.t(36, 536, "apps/v1 과 extensions/v1beta1 은 같은 객체의 다른 표현이다 — 스키마가 다를 뿐 "
             "저장된 것은 하나다.", 12, MUTED, KR, "start")
d.legend(600, [("가리키는 대상이 없는 리소스", BAD), ("apps/v1 스키마", OK),
               ("extensions/v1beta1 스키마", INFO), ("저장되는 오브젝트", ACC)])
d.save("04-01-resource-vs-object.svg")
print("ok resource-vs-object")
