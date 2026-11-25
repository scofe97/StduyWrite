# 03-01 §7 Envoy를 부양하는 것 — 설정 · 디스커버리 · 인증서 · 텔레메트리 연동.
# 값 근거: 03-01 본문 §7(Kubernetes API, istiod, Envoy 사이드카, Prometheus, Jaeger/Zipkin).
# 타입 스펙: type-architecture — 구성요소와 연결. 존 셋(컨트롤 플레인 · 데이터 플레인 · 관측 인프라), 초점 1곳(istiod), 직각 연결선.
#           폭을 920으로 두고 K8s API와 컨트롤 플레인 존 사이 간격을 넓혀 '레지스트리 읽기' 라벨이 존 경계에 걸터앉지 않게 했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 584
d = D(W, H, "ISTIO IN ACTION · 03-01 §7",
      "Envoy를 부양하는 네 가지 역할",
      "Kubernetes API 에서 Istio 설정과 서비스 레지스트리를 읽은 istiod 가 xDS 로 설정을, CA 로 인증서를 Envoy 사이드카에 내려보낸다. "
      "Envoy 가 내보내는 메트릭과 스팬은 Prometheus 와 Jaeger/Zipkin 으로 간다.",
      "istiod가 설정·디스커버리·인증서를 대 주고, 텔레메트리는 어디로 보낼지를 Istio가 설정합니다")


def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
    lw = len(label) * 13 + 20
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 17, label, 13, SOFT, KR)


def node(x, y, w, h, title, subs, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 26, title, 14, ACC if focal else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 50 + i * 20, s, 13, MUTED, KR)


# 존 (배경 → 존 → 화살표 → 노드)
zone(296, 136, 212, 184, "컨트롤 플레인")
zone(636, 104, 240, 260, "데이터 플레인")
zone(528, 392, 372, 124, "관측 인프라")

# 좌표
K8 = (24, 192, 152, 92)        # Kubernetes API
IS = (310, 168, 184, 120)      # istiod
EA = (660, 136, 192, 76)       # Envoy A
EB = (660, 264, 192, 76)       # Envoy B
PR = (556, 424, 156, 68)       # Prometheus
JG = (728, 424, 156, 68)       # Jaeger / Zipkin

def cx(n): return n[0] + n[2] / 2
def cy(n): return n[1] + n[3] / 2

# 화살표 — 노드보다 먼저
# Kubernetes API -> istiod (가로, x=176 ~ 310)
d.path(f"M {K8[0] + K8[2]} {cy(K8)} H {IS[0] - 2}", MUTED, 1.2, m="ar")
d.t(236, cy(K8) - 10, "설정 읽기", 13, MUTED, KR)
d.t(236, cy(K8) + 22, "레지스트리 읽기", 13, MUTED, KR)

# istiod -> Envoy A, B (x1=494, EA[0]=660, mid=577; gap between zones 508..636)
x1, y1 = IS[0] + IS[2], cy(IS)
mid = (x1 + EA[0]) / 2
ya, yb = cy(EA), cy(EB)
d.path(f"M {x1} {y1} H {mid - 8} Q {mid} {y1} {mid} {y1 - 8} V {ya + 8} Q {mid} {ya} {mid + 8} {ya} H {EA[0] - 2}", MUTED, 1.2, m="ar")
d.path(f"M {x1} {y1} H {mid - 8} Q {mid} {y1} {mid} {y1 + 8} V {yb - 8} Q {mid} {yb} {mid + 8} {yb} H {EB[0] - 2}", MUTED, 1.2, m="ar")
d.o.append(f'<rect x="{mid - 52}" y="{y1 - 30}" width="104" height="20" rx="3" fill="{PAPER}"/>')
d.t(mid, y1 - 15, "xDS · 인증서", 13, MUTED, KR)

# 데이터 플레인(Envoy 전체) -> Prometheus, Jaeger. 서비스 A·B 모두 같은 경로로 내보내므로 화살표는 존 아래 테두리(y=364)에서 나온다.
# Prometheus 진입 x는 zone 라벨 오른쪽인 cx(PR)+20=654 로 둔다.
pr_entry = cx(PR) + 20
jg_entry = cx(JG)
for tx in (pr_entry, jg_entry):
    d.path(f"M {tx} 364 V {PR[1] - 2}", INFO, 1.2, m="info")
d.t(pr_entry + 10, PR[1] - 12, "메트릭", 13, INFO, KR, "start")
d.t(jg_entry + 10, JG[1] - 12, "스팬", 13, INFO, KR, "start")

# 노드
node(*K8, "Kubernetes API", ["VirtualService", "서비스 레지스트리"])
node(*IS, "istiod", ["xDS 구현 (설정)", "레지스트리 추상화", "인증서 서명 · 순환"], focal=True)
node(*EA, "Envoy 사이드카", ["서비스 A"])
node(*EB, "Envoy 사이드카", ["서비스 B"])
node(*PR, "Prometheus", ["시계열 메트릭"])
node(*JG, "Jaeger / Zipkin", ["분산 추적 스팬"])

d.legend(544, [("istiod가 대 주는 것", ACC), ("Istio가 설정하는 텔레메트리 경로", INFO)])
d.save("03-01.istio-support.svg")
print("ok 03-01 istio-support")
