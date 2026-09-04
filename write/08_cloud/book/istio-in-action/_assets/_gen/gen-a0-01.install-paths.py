# a0-01 §1 리소스를 클러스터에 올리는 길 넷.
# 본문(부록 A 도입): helm · istioctl · istio-operator · kubectl 넷이고, "All the customization
#       possibilities of the Istio installation are powered by Helm templating" 이므로 셋은
#       결국 같은 템플릿을 돌린다. istioctl 은 "Under the hood, it uses Helm to generate the
#       Istio resources". kubectl 은 이미 만들어진 리소스를 받는 쪽이라 축이 다르다.
# 타입 스펙: type-dependency — 무엇이 무엇에 기대는가. 랭크 행으로 놓고 팬인 배지를 단다.
#           Helm 템플릿이 다중 부모를 받는 수렴점이라 tree 가 아니라 이 타입이다.
#           축약: 되돌아가는 의존이 없으므로 back-edge 를 그리지 않고, accent 는 수렴점 하나에 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 940, 560
d = D(W, H, "ISTIO IN ACTION · A0-01 §1",
      "셋은 결국 같은 템플릿을 돌린다",
      "설치 도구가 넷이지만 대등한 선택지가 아니다. 셋은 Helm 템플릿이라는 같은 바닥 위에 서 있고, "
      "갈리는 것은 템플릿에 값을 넣기 전에 무엇이 값을 검사하느냐다. 색이 붙은 칸이 그 수렴점이다.",
      "kubectl 은 이미 만들어진 리소스를 받는 쪽이라 축이 다릅니다")

NW, NH = 200, 60
def node(x, y, name, sub, fanin, focal=False, ext=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif ext:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" '
                   f'fill="{INK}05" stroke="{INK}4D" stroke-width="1" stroke-dasharray="5 5"/>')
    else:
        d.box(x, y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 16, y + 26, name, 13, ACC if focal else (SOFT if ext else INK), MONO, "start", 600)
    d.t(x + 16, y + 46, sub, 11, MUTED, KR, "start")
    bw = len(fanin) * 7 + 12
    d.o.append(f'<rect x="{x + NW - bw - 10}" y="{y + 10}" width="{bw}" height="16" rx="2" fill="{INK}14"/>')
    d.t(x + NW - bw / 2 - 10, y + 22, fanin, 10, INK, MONO, "middle", 600)

R0, R1, R2 = 132, 252, 372
XS = [40, 268, 496]

node(XS[0], R0, "helm", "차트로 직접 만든다", "0 in")
node(XS[1], R0, "istioctl", "CRD 로 감싼다", "0 in")
node(XS[2], R0, "istio-operator", "클러스터 안에서 지켜본다", "0 in")
node(724, R0, "kubectl", "만들어진 것을 올린다", "0 in", ext=True)

node(268, R1, "IstioOperator API", "바라는 상태를 적는 스키마", "2 in")
node(268, R2, "Helm 템플릿", "설정 가능성이 여기서 나온다", "2 in", focal=True)

# istioctl · istio-operator 는 IstioOperator API 를 거친다
for i in (1, 2):
    cx = XS[i] + NW / 2
    if i == 1:
        d.arrow([(cx, R0 + NH), (cx, R1 - 2)], MUTED, "ar", 1.3)
    else:
        d.path(f"M {cx} {R0 + NH} L {cx} {R1 - 28} L 420 {R1 - 28} L 420 {R1 - 2}", MUTED, 1.2, m="ar")
# API -> 템플릿
d.arrow([(368, R1 + NH), (368, R2 - 2)], ACC, "acc", 1.5)
# helm 은 API 를 건너뛰고 템플릿으로 곧장 간다
d.path(f"M {XS[0] + NW / 2} {R0 + NH} L {XS[0] + NW / 2} {R2 + NH / 2} L {268 - 2} {R2 + NH / 2}",
       ACC, 1.3, m="acc")

d.t(488, R1 + 34, "검증이 붙는 층", 11, INFO, KR, "start", 600)
d.t(556, R2 + 26, "여기서 갈리지 않는다 — 셋 다 같은 템플릿", 11, SOFT, KR, "start")
d.t(556, R2 + 48, "갈리는 것은 값을 넣기 전의 검사다", 11, MUTED, KR, "start")

d.t(28, 480, "kubectl · ArgoCD · Flux 는 이미 만들어진 리소스를 받아 적용하므로 이 사슬 밖에 선다", 11, SOFT, KR, "start")
d.legend(504, [("모두가 수렴하는 바닥", ACC), ("사슬 밖에 서는 쪽", MUTED)])
d.save("a0-01.install-paths.svg")
