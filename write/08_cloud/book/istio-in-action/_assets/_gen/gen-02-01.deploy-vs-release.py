# 02-01 §4 배포와 릴리스를 가르는 상태 전이.
# 본문: 배포는 새 코드를 프로덕션에 가져다 놓는 일이고, 릴리스는 그 코드에 실제 트래픽을 흘리는 일이다.
#       Kubernetes 기본값은 둘을 붙여 놓는다 — 올리는 순간 Service 가 이미 부하를 나눈다.
#       저자가 DestinationRule 로 버전을 가르고 VirtualService 로 전량 v1 에 묶는 것은 그 붙음을 떼기 위해서다.
# 타입 스펙: type-state — 주체 하나(새 버전 코드)의 상태 전이. 시작점 · 상태 3 · 종료점 · 지름길 전이 하나,
#           전이 라벨은 event [guard] 형태, coral 은 저자가 위험하다고 지목한 지름길에.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · 02-01 §4",
      "올리는 일과 흘리는 일을 떼어 놓는다",
      "기본값은 둘이 붙어 있다. 올리는 순간 Kubernetes 가 이미 부하를 나눠 보내므로 유료 고객이 새 "
      "코드의 첫 시험대가 된다. 색이 붙은 전이가 그 지름길이고, 아래 경로가 저자가 만드는 길이다.",
      "올릴 때 트래픽 정책을 함께 정하지 않았다면 그것은 이미 릴리스입니다")

CY, SW, SH = 216, 280, 72
XS = [36, 360, 684]

def state(x, y, name, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, y + 30, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, y + 52, sub, 11, MUTED, MONO)

d.o.append(f'<circle cx="48" cy="{CY + SH / 2}" r="6" fill="{INK}"/>')
d.o.append(f'<circle cx="964" cy="{CY + SH / 2}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="964" cy="{CY + SH / 2}" r="5" fill="{INK}"/>')

MY = CY + SH / 2
d.arrow([(56, MY), (XS[0] - 2, MY)], MUTED, "ar", 1.4)
d.arrow([(XS[1] + SW, MY), (XS[2] - 2, MY)], MUTED, "ar", 1.4)
d.arrow([(XS[2] + SW, MY), (954, MY)], MUTED, "ar", 1.4)

# 아래 경로 — 저자가 만드는 길
d.path(f"M {XS[0] + SW} {MY} L {XS[1] - 2} {MY}", MUTED, 1.4, m="ar")
# 위 지름길 — Kubernetes 기본값
d.path(f"M {XS[0] + SW / 2} {CY} L {XS[0] + SW / 2} 140 L {XS[2] + SW / 2} 140 L {XS[2] + SW / 2} {CY - 2}", ACC, 1.6, m="acc")
d.t((XS[0] + XS[2]) / 2 + SW / 2, 128, "정책 없이 올리면 여기로 바로 간다", 11, ACC, KR, "middle", 600)

state(XS[0], CY, "배포됨", "kubectl apply · v2 기동")
state(XS[1], CY, "릴리스되지 않음", "VirtualService 전량 v1")
state(XS[2], CY, "일부에게 릴리스", "x-dark-launch: v2", focal=True)

d.t((XS[0] + SW + XS[1]) / 2, CY - 26, "DestinationRule 로 subset 을 가른다", 11, MUTED, MONO, "middle", 600)
d.t((XS[1] + SW + XS[2]) / 2, CY - 26, "헤더 매칭 라우팅", 11, MUTED, MONO, "middle", 600)
d.t((XS[2] + SW + 954) / 2, CY - 26, "비율을 넓힌다", 11, MUTED, MONO, "middle", 600)

BY = CY + SH + 48
d.box(XS[0], BY, 928, 104, PAPER2, RULE, 1.0, 6)
d.t(XS[0] + 20, BY + 28, "저자가 제시하는 단계적 릴리스", 11, ACC, KR, "start", 600)
d.t(XS[0] + 20, BY + 54, "내부 직원  ->  비유료 고객  ->  실버 등급 고객  ->  전체", 11, INK, MONO, "start")
d.t(XS[0] + 20, BY + 80, "등급을 판정하는 주체는 메시가 아니다 — 헤더나 쿠키로 만들어 주는 계층이 앞에 있어야 한다", 11, SOFT, KR, "start")

d.t(32, 524, "목적은 둘이다 — 프로덕션에서 깨질 확률을 낮추고, 유료 고객이 최전선에 서지 않게 한다", 11, SOFT, KR, "start")
d.legend(548, [("정책 없이 올렸을 때 가는 길", ACC)])
d.save("02-01.deploy-vs-release.svg")
