# 05-03.ingress-path-routing — 같은 진입점, 경로만으로 갈린다
# 타입 스펙: type-flowchart.md — 마지막에서 경로로 둘로 갈리므로 체인 셋 + 부채꼴 둘.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
W, H = 1000, 632
d = D(W, H, "INGRESS · ONE ENTRY, PATHS SPLIT",
      "같은 진입점으로 들어와 경로만으로 다른 서비스에 닿는다",
      "포트도 호스트도 같다. 갈리는 것은 경로 하나뿐이고, 어디에도 안 걸리면 기본 백엔드로 간다.",
      lead="포트도 호스트도 같고 갈리는 것은 경로 하나뿐이다")
BW, BH, GAP, EP_W = 148, 108, 44, 296
CX = [40 + BW // 2 + i * (BW + GAP) for i in range(3)]
EP_X, EP_Y = 812, (280, 430)
CY = 300
def box(cx, cy, t, s, tag, c=None, focal=False, w=BW):
    x, y = cx - w // 2, cy - BH // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, BH, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 22, ddx.fit(t, 13, w - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 0, ddx.fit(s, 11, w - 16, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':/…-' for ch in s) else KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)
ddx.band(d, 104, 568, "경로가 어디에도 안 걸리면 기본 백엔드로 간다 — 그것도 규칙의 일부다")
for cx, s in zip(CX + [EP_X], ["① 외부 요청", "② 진입점", "③ 규칙 대조", "④ 백엔드"]):
    d.t(cx, 196, s, 12, SOFT, KR, "middle", 600)
box(CX[0], CY, "요청", "curl localhost/…", "같은 진입점 하나", INFO)
box(CX[1], CY, "LB", "extraPortMappings", "KIND 로컬 80/443")
box(CX[2], CY, "컨트롤러", "NGINX Pod", "불일치는 기본 백엔드로", ACC)
box(EP_X, EP_Y[0], "/host", "clusterip-service", "app Pod 들", OK, w=EP_W)
box(EP_X, EP_Y[1], "/data", "clusterip-service-2", "app2 Pod 들", OK, w=EP_W)
for i, lab in enumerate(["80 포트", "전달"]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+6} {CY} L {b-10} {CY}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, CY - 16, ddx.fit(lab, 10, GAP - 4, lab), 10, MUTED, KR)
A_X, B_X = CX[2] + BW // 2 + 6, EP_X - EP_W // 2 - 10
for ey, lab in zip(EP_Y, ["path /host", "path /data"]):
    d.path(f"M {A_X} {CY + (ey-CY)//4} L {B_X} {ey}", OK, 1.5, m="ok")
    d.t((A_X + B_X) // 2, (CY + ey) // 2 - 10, ddx.fit(lab, 10, B_X - A_X - 4, lab), 10, OK, MONO)
d.t(36, 540, "규칙을 고르는 것은 컨트롤러 Pod 다 — LB 는 80 포트를 그 Pod 로 넘길 뿐이다",
     12, MUTED, KR, "start")
d.legend(584, [("들어오는 요청", INFO), ("규칙을 고르는 자리", ACC), ("백엔드", OK)])
d.save("05-03.ingress-path-routing.svg"); print("ok ingress-path-routing")
