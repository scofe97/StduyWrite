# 07-01 §5 Prometheus 가 두 리소스로 두 대상을 긁는 배치.
# 본문: "ServiceMonitor 는 Service 를 고른 뒤 그 Service 가 이름 붙인 포트를 긁고, PodMonitor 는 파드를 직접
#       훑습니다." 네임스페이스 경계와 포트가 이 그림의 내용이다.
# 주의: 원문의 PodMonitor 에는 포트 필드가 없다. relabeling 이 __address__ 를 파드의 prometheus.io/port
#       애노테이션으로 바꿔 쓰므로, 스크랩 포트를 :15090 으로 단정하지 않는다(적대적 검증 2026-08-30 지적).
# 타입 스펙: type-deployment — 무엇이 어느 네임스페이스에 설치되고 어느 포트로 열리는지가 논점이다.
#           존 3 · 노드 4 · 아티팩트 칩 4 · 경로 3, accent 는 둘(PodMonitor 경로와 그 라벨).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1120, 640
d = D(W, H, "ISTIO IN ACTION · 07-01 §5",
      "Prometheus 는 두 리소스로 두 대상을 긁는다",
      "ServiceMonitor 는 istiod 를 서비스 셀렉터로 잡고, PodMonitor 는 모든 파드를 훑어 istio-proxy "
      "컨테이너만 남긴다. 색이 붙은 경로가 사이드카를 잡기 위해 relabeling 이 필요한 쪽이다.",
      "사이드카의 통계 포트는 앱 Service 의 포트 목록에 없어 파드 단위로 훑습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 10}" y="{y + 10}" width="34" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 27, y + 21, tag, 8, INK, MONO, "middle", 600)
    d.t(x + 54, y + 22, name, 13, INK, KR, "start", 600)
    d.t(x + 54, y + 38, sub, 9, MUTED, MONO, "start")

def chip(x, y, w, name, ver):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="24" rx="4" fill="{INK}0D" stroke="{MUTED}" stroke-width="0.8"/>')
    d.t(x + 12, y + 16, name, 12, INK, KR, "start")
    d.t(x + w - 12, y + 16, ver, 9, MUTED, MONO, "end")

zone(32, 200, 308, 196, "PROMETHEUS")
zone(560, 100, 520, 164, "ISTIO-SYSTEM")
zone(560, 300, 520, 244, "ISTIOINACTION")

node(64, 240, 244, 116, "STS", "prometheus", "prometheus ns")
chip(76, 296, 220, "kube-prometheus-stack", "13.13.1")

node(592, 132, 456, 100, "POD", "istiod", "istio-system")
chip(604, 188, 432, "istiod", "1.13.0")

node(592, 328, 456, 84, "POD", "webapp", "2/2 READY")
chip(604, 374, 432, "istio-proxy", "1.13.0")

node(592, 436, 456, 84, "POD", "catalog", "2/2 READY")
chip(604, 482, 432, "istio-proxy", "1.13.0")

# 스크랩 경로 — 네임스페이스를 넘으므로 link 색, PodMonitor 경로만 accent
d.path("M 308 268 L 400 268 L 400 182 L 588 182", INFO, 1.2, m="info")
d.t(408, 200, "ServiceMonitor", 9, INFO, MONO, "start", 600)
d.t(408, 216, ":15014 http-monitoring · 15s", 8, MUTED, MONO, "start")

d.path("M 308 312 L 440 312 L 440 370 L 588 370", ACC, 1.5, m="acc")
d.t(448, 326, "PodMonitor · 15s", 9, ACC, MONO, "start", 600)
d.t(448, 342, "/stats/prometheus", 8, ACC, MONO, "start")
d.t(448, 356, "port = prometheus.io/port", 8, ACC, MONO, "start")

d.path("M 308 340 L 360 340 L 360 478 L 588 478", INFO, 1.2, m="info")
d.t(368, 462, "PodMonitor", 8, MUTED, MONO, "start")

d.t(32, 572, "PodMonitor 에는 포트 필드가 없다 — relabeling 이 파드 애노테이션에서 주소를 만든다", 11, SOFT, KR, "start")
d.legend(592, [("사이드카를 잡는 경로", ACC), ("네임스페이스를 넘는 스크랩", INFO)])
d.save("07-01.scrape-topology.svg")
