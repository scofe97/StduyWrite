# 13-01 §6 클러스터와 VM 이 놓인 두 망, 그 사이에 서는 문 — 원문 그림 13.9 · 13.11.
# 본문(원문 13.2 · 13.3.1): webapp 과 catalog 는 쿠버네티스 클러스터에, forum 은 VM 에 배포한다.
#       클러스터와 VM 이 서로 다른 망에 있어서 VM 에서 클러스터 서비스로 가는 트래픽을 역방향 프록시할
#       동서 게이트웨이가 필요하다. 메시에 들려면 VM 이 istiod 와 통신하고 클러스터 서비스로 연결을
#       걸 수 있어야 한다. 멀티 클러스터 mTLS 포트 15443 을 먼저 노출하는데 이것이 VM 에서 온 요청을
#       메시 안의 서비스로 역방향 프록시한다. 이어서 Gateway 와 VirtualService 로 istiod 포트를 노출한다.
#       VM 의 istio-agent 는 istiod.istio-system.svc:15012 를 업스트림으로 잡고(13.3.3 의 xdsproxy 로그),
#       그 호스트명은 /etc/hosts 가 동서 게이트웨이 IP 로 푼다. 그래서 두 연결 모두 VM 에서 문으로 향한다.
#       망 이름은 istio-system 네임스페이스의 topology.istio.io/network=west-network 라벨과 설치 설정의
#       meshID · clusterName · network 로 못 박고, VM 쪽 망은 WorkloadGroup 의 template.network 가 정한다.
# 타입 스펙: type-deployment — 무엇이 어느 망에 서고 그 사이에 무엇이 있는지가 논점이다.
#           존 2 · 노드 7 · 경로 4, accent 는 두 망을 잇는 자리 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 704
d = D(W, H, "ISTIO IN ACTION · 13-01 §6",
      "두 연결 모두 기계에서 문으로 향한다",
      "VM 은 컨트롤 플레인에 붙어야 하고 클러스터 서비스도 불러야 하는데, 망이 달라 둘 다 동서 "
      "게이트웨이를 거친다. 색이 붙은 자리가 그 문이고 여는 포트가 둘이다.",
      "12 장에서 클러스터 둘을 이었던 물건이 여기서는 클러스터와 기계를 잇습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, tag, name, sub, focal=False, stack=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.o.append(f'<rect x="{x + 12}" y="{y + 12}" width="40" height="14" rx="2" fill="{INK}14"/>')
    d.t(x + 32, y + 23, tag, 8, INK, MONO, "middle", 600)
    if stack:
        d.t(x + w / 2, y + 62, name, 13, ACC if focal else INK, KR, "middle", 600)
        d.t(x + w / 2, y + 84, sub, 11, MUTED, KR, "middle")
    else:
        d.t(x + 62, y + 24, name, 13, ACC if focal else INK, KR, "start", 600)
        d.t(x + 62, y + 42, sub, 9, MUTED, MONO, "start")

zone(40, 140, 516, 356, "WEST-NETWORK · KUBERNETES")
zone(636, 140, 324, 356, "VM-NETWORK")

node(60, 168, 324, 60, "CP", "istiod", "meshID usmesh · west-cluster")
node(60, 240, 324, 60, "SVC", "webapp · catalog", "istioinaction 네임스페이스")
node(60, 312, 324, 60, "GW", "인그레스 게이트웨이", "바깥에서 들어오는 트래픽")
node(400, 168, 136, 204, "EWG", "동서 게이트웨이", "두 망을 잇는 문", focal=True, stack=True)
node(656, 168, 288, 60, "APP", "forum", "8080 을 듣는다")
node(656, 240, 288, 60, "AGT", "istio-agent", "Envoy · DNS 프록시")
node(656, 336, 288, 60, "GRP", "WorkloadGroup 의 network", "vm-network")

d.path("M 652 252 H 540", INFO, 1.3, m="info")
d.path("M 652 288 H 540", ACC, 1.5, m="acc")
d.t(596, 240, "15012", 9, INFO, MONO, "middle", 600)
d.t(596, 308, "15443", 9, ACC, MONO, "middle", 600)
d.path("M 400 198 H 384", INFO, 1.3, m="info")
d.path("M 400 270 H 384", ACC, 1.5, m="acc")

d.t(40, 544, "여는 것 둘 — 15443 은 VM 에서 온 요청을 메시 안의 서비스로 역방향 프록시하고,", 11, SOFT, KR, "start")
d.t(40, 566, "Gateway 와 VirtualService 는 istiod 로 가는 트래픽을 받아들인다", 11, SOFT, KR, "start")
d.t(40, 594, "망 이름을 붙이는 자리 — 클러스터는 istio-system 에 topology.istio.io/network=west-network 라벨을 건다", 11, MUTED, KR, "start")
d.t(40, 622, "같은 망이었다면 이 문이 필요 없다 — 컨트롤 플레인이 IP 로 곧장 보낸다", 11, SOFT, KR, "start")
d.legend(642, [("두 망을 잇는 문", ACC), ("VM 이 컨트롤 플레인에 붙는 길", INFO)])
d.save("13-01.two-networks.svg")
