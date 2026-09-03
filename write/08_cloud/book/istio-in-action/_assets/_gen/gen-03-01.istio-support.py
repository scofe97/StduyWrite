# 03-01 §7 Envoy를 부양하는 것 — 저자가 든 예 넷(설정 · 디스커버리 · 텔레메트리 연동 · 인증서).
# 본문: "색이 붙은 istiod 가 그중 셋(설정·디스커버리·인증서)을 맡고, 넷째인 텔레메트리는 Envoy 가
# Prometheus·Jaeger 로 보내도록 Istio 가 설정한다."
# 타입 스펙: type-architecture — 구성요소(Kubernetes API · istiod · Envoy 사이드카 · Prometheus · Jaeger)와
#           연결. 존 셋(컨트롤 플레인 · 데이터 플레인 · 관측 인프라), 초점 1곳(istiod), 직각 연결선.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 580
d = D(W, H, "ISTIO IN ACTION · 03-01 §7",
      "Envoy를 부양하는 것 — 저자가 든 예 넷",
      "Kubernetes API 에서 Istio 설정과 서비스 레지스트리를 읽은 istiod 가 xDS 로 설정을, CA 로 인증서를 Envoy 사이드카에 내려보낸다. "
      "Envoy 가 뿜는 메트릭과 스팬은 Prometheus 와 Jaeger/Zipkin 으로 간다.",
      "istiod가 설정·디스커버리·인증서를 대 주고, 텔레메트리는 어디로 보낼지를 Istio가 설정한다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(245,245,245,0.02)" stroke="rgba(245,245,245,0.10)" stroke-width="0.8"/>')
    lw = len(label) * 12 + 16
    d.o.append(f'<rect x="{x + 12}" y="{y + 4}" width="{lw}" height="18" rx="2" fill="{PAPER}"/>')
    d.t(x + 12 + lw / 2, y + 17, label, 12, SOFT, KR)

def node(x, y, w, h, title, subs, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 26, title, 14, ACC if focal else INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, y + 48 + i * 18, s, 12, MUTED, KR)

# 존 (배경 → 존 → 화살표 → 노드)
zone(296, 140, 232, 176, "컨트롤 플레인")
zone(644, 108, 232, 256, "데이터 플레인")
zone(556, 388, 408, 120, "관측 인프라")

# 좌표
K8 = (24, 192, 168, 88)        # Kubernetes API
IS = (320, 172, 184, 112)      # istiod
EA = (668, 140, 184, 72)       # Envoy A
EB = (668, 268, 184, 72)       # Envoy B
PR = (584, 420, 160, 64)       # Prometheus
JG = (772, 420, 160, 64)       # Jaeger / Zipkin

def cx(n): return n[0] + n[2] / 2
def cy(n): return n[1] + n[3] / 2

# 화살표 — 노드보다 먼저
# Kubernetes API → istiod (가로)
d.path(f"M {K8[0] + K8[2]} {cy(K8)} H {IS[0] - 2}", MUTED, 1.2, m="ar")
d.t((K8[0] + K8[2] + IS[0]) / 2, cy(K8) - 10, "설정 읽기", 12, MUTED, KR)
d.t((K8[0] + K8[2] + IS[0]) / 2, cy(K8) + 20, "레지스트리 읽기", 12, MUTED, KR)
# istiod → Envoy A (오른쪽+위, 두 번 꺾음), istiod → Envoy B (오른쪽+아래)
x1, y1 = IS[0] + IS[2], cy(IS)
mid = (x1 + EA[0]) / 2
ya, yb = cy(EA), cy(EB)
d.path(f"M {x1} {y1} H {mid - 8} Q {mid} {y1} {mid} {y1 - 8} V {ya + 8} Q {mid} {ya} {mid + 8} {ya} H {EA[0] - 2}", MUTED, 1.2, m="ar")
d.path(f"M {x1} {y1} H {mid - 8} Q {mid} {y1} {mid} {y1 + 8} V {yb - 8} Q {mid} {yb} {mid + 8} {yb} H {EB[0] - 2}", MUTED, 1.2, m="ar")
d.o.append(f'<rect x="{mid - 58}" y="{y1 - 30}" width="116" height="18" rx="3" fill="{PAPER}"/>')
d.t(mid, y1 - 17, "xDS · 인증서", 12, MUTED, KR)
# Envoy B → Prometheus (아래로 두 번 꺾음), Envoy B → Jaeger
xb, yb0 = cx(EB), EB[1] + EB[3]
corr = 388 - 8
for tgt in (PR, JG):
    tx = cx(tgt); s = 1 if tx > xb else -1
    d.path(f"M {xb + (12 * s)} {yb0} V {corr - 8} Q {xb + 12 * s} {corr} {xb + 12 * s + 8 * s} {corr} H {tx - 8 * s} Q {tx} {corr} {tx} {corr + 8} V {tgt[1] - 2}", INFO, 1.2, m="info")
d.t(cx(PR) + 12, PR[1] - 14, "메트릭", 12, INFO, KR, "start")
d.t(cx(JG) + 12, JG[1] - 14, "스팬", 12, INFO, KR, "start")

# 노드
node(*K8, "Kubernetes API", ["VirtualService", "서비스 레지스트리"])
node(*IS, "istiod", ["xDS 구현 (설정)", "레지스트리 추상화", "인증서 발급 · 순환"], focal=True)
node(*EA, "Envoy 사이드카", ["서비스 A"])
node(*EB, "Envoy 사이드카", ["서비스 B"])
node(*PR, "Prometheus", ["시계열 메트릭"])
node(*JG, "Jaeger / Zipkin", ["분산 추적 스팬"])

d.legend(540, [("istiod가 대 주는 것", ACC), ("Istio가 설정하는 텔레메트리 경로", INFO)])
d.save("03-01.istio-support.svg")
print("h 필요:", 540 + 22 + 16, " 실제:", H)
