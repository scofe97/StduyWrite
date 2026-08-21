# 12-01 §3 — 설치가 만드는 것과, 그중 도는 것
# 본문이 "파드를 낳는 것은 Deployment 하나뿐"과 "IngressClass 는 설치가 데려온다"는
# 두 사실을 못박는다. 그래서 목록만 그리면 안 되고 순서 축이 함께 있어야 한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 684, "KUBERNETES IN ACTION · 12-01",
      "설치는 평범한 apply 하나다",
      "YAML 한 장에 여섯 종류가 들어 있을 뿐이고, 그중 도는 프로세스를 낳는 것은 Deployment 하나다. "
      "나머지는 이름표와 권한 규칙 같은 선언물이다.",
      "kubectl apply -f .../deploy.yaml")

ddx.band(d, 100, 400, "한 장에 들어 있는 여섯 종류", x=24, w=1132)
OBJ = [("Namespace", "ingress-nginx", None), ("Deployment", "컨트롤러 파드가 나온다", ACC),
       ("Service (LoadBalancer)", "그 파드를 밖으로", None),
       ("IngressClass", "'나는 nginx 다' 명패", INFO),
       ("ServiceAccount · Role", "API 를 읽을 권한", None), ("ConfigMap", "컨트롤러 전역 설정", None)]
BW, GP = 340, 24
for i, (t, s, c) in enumerate(OBJ):
    cx = 76 + BW // 2 + (i % 3) * (BW + GP)
    cy = 200 + (i // 3) * 108
    if c is ACC:
        d.o.append(f'<rect x="{cx-BW//2}" y="{cy-38}" width="{BW}" height="76" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(cx - BW // 2, cy - 38, BW, 76, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 6, ddx.fit(t, 13, BW - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 18, s, 11, MUTED, KR)
d.t(590, 376, "도는 프로세스를 낳는 것은 Deployment 하나뿐이다", 11, ACC, KR)

ddx.band(d, 424, 588, "그래서 순서가 고정된다", x=24, w=1132)
ORD = [("① 컨트롤러 설치", "Deployment 가 뜬다"), ("② IngressClass 생성", "설치가 데려온다"),
       ("③ Ingress 가 지목", "ingressClassName: nginx")]
CX = [250, 590, 930]
for cx, (t, s) in zip(CX, ORD):
    ddx.node(d, cx, 506, t, s, 280, 84, INFO)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+146} 506 L {b-150} 506", MUTED, 1.5, m="ar")
d.t(590, 568, "없는 이름을 부르면 아무 컨트롤러도 자기 일이라 여기지 않아, 에러 대신 침묵이 온다", 11, MUTED, KR)

d.t(24, 618, "온프레미스에는 type: LoadBalancer 를 집어갈 주체가 없어 EXTERNAL-IP 가 무기한 pending 이다. "
             "MetalLB 가 그 빈자리를 메우되, 줄 IP 대역은 우리가 정해 줘야 한다.", 11, MUTED, KR, "start")
d.legend(636, [("파드를 낳는 것", ACC), ("순서를 만드는 것", INFO)])
d.save("12-01-controller-install-flow.svg")
print("ok")
