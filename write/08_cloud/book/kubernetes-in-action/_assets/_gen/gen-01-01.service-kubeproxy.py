# 01-01 §Service 와 kube-proxy — 파드로 가는 트래픽 라우팅
# 본문·옛 도식: Service 는 파드들을 하나의 가상 IP(ClusterIP 10.96.0.12:80)로 묶어 노출하고,
#   kube-proxy 가 그 가상 IP 로 온 요청을 실제 파드로 나눠 보낸다. 클라이언트는 가상 IP 하나만
#   안다. kube-proxy 모드는 User Space(구식)·iptables(기본)·IPVS(대규모) — 규칙을 노드 커널에
#   심는 방식이 다르다.
# 타입 스펙: type-architecture.md — 가상 하나가 실제 여럿으로 갈리는 구조라 fan-out. 규칙이 노드마다 심긴다는 것이
#           요점이므로 노드 경계를 그려 kube-proxy 를 그 안에 둔다.
#           점선 사각형이 노드 경계를 표시하고 그 안에 kube-proxy 와 파드를 둔다 — 정본의
#           "Dashed boundary rectangles mark regions" 그대로다. 파드 배치가 아니라 가상 IP 가
#           규칙을 타고 갈리는 경로가 논지라 type-deployment 가 아니다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 668
d = D(W, H, "KUBERNETES IN ACTION · 01-01",
      "가상 IP 하나가 노드마다 심긴 규칙으로 갈린다",
      "클라이언트는 Service 의 ClusterIP 하나만 안다. 그 요청은 각 노드의 kube-proxy 가 커널에 "
      "심어 둔 규칙을 타고 실제 파드로 나뉜다.",
      lead="Service 는 가상 컴포넌트다 — 실제로 트래픽을 나누는 것은 노드의 규칙이다")

SVC = (500, 224)
NODES = [(276, 452), (724, 452)]
NW, NH = 400, 216
PODS = {0: [("Pod A", "10.32.0.14"), ("Pod B", "10.32.0.15")],
        1: [("Pod C", "10.32.1.21"), ("Pod D", "10.32.1.22")]}

ddx.band(d, 104, 612, "kube-proxy 모드는 User Space · iptables(기본) · IPVS — 규칙을 심는 방식이 다르다")

d.o.append(f'<rect x="{SVC[0]-260}" y="{SVC[1]-46}" width="520" height="92" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4" stroke-dasharray="6 5"/>')
d.t(SVC[0], SVC[1] - 12, "Service: my-app — 가상 컴포넌트", 14, ACC, KR, "middle", 600)
d.t(SVC[0], SVC[1] + 16, "ClusterIP  10.96.0.12 : 80", 12, MUTED, MONO)

for i, (cx, cy) in enumerate(NODES):
    d.o.append(f'<rect x="{cx-NW//2}" y="{cy-NH//2}" width="{NW}" height="{NH}" rx="8" '
               f'fill="{INFO}06" stroke="{INFO}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, cx - NW // 2, cy - NH // 2, f"Worker Node {i+1}", 11, INFO, off=16)
    d.box(cx - 170, cy - 74, 340, 60, PAPER2, OK, 1.1, 6)
    d.t(cx, cy - 38, "kube-proxy — 커널에 규칙을 심는다", 12, OK, KR, "middle", 600)
    for j, (name, ip) in enumerate(PODS[i]):
        x = cx - 170 + j * 176
        d.box(x, cy + 6, 164, 68, PAPER2, MUTED, 1.1, 6)
        d.t(x + 82, cy + 32, name, 12, INK, KR, "middle", 600)
        d.t(x + 82, cy + 54, ip, 11, SOFT, MONO)

SPINE = 316
d.path(f"M {SVC[0]} {SVC[1]+46+6} L {SVC[0]} {SPINE}", ACC, 1.8)
d.path(f"M {NODES[0][0]} {SPINE} L {NODES[1][0]} {SPINE}", ACC, 1.8)
for cx, cy in NODES:
    d.path(f"M {cx} {SPINE} L {cx} {cy-74-10}", ACC, 1.8, m="acc")
d.chip(500, SPINE, "가상 IP 로 온 요청", ACC, 11)

for cx, cy in NODES:
    for j in range(2):
        x = cx - 170 + j * 176 + 82
        d.path(f"M {cx} {cy-44+6} L {cx} {cy-4} L {x} {cy-4} L {x} {cy+6-4}", OK, 1.4, m="ok")

# 노드 존이 344~560 을 쓴다 — 산문은 그 아래로
d.t(36, 588, "클라이언트는 가상 IP 하나만 알고, 어느 파드가 받는지는 노드의 규칙이 정한다.",
     12, MUTED, KR, "start")
d.legend(628, [("가상 진입점과 그 경로", ACC), ("규칙을 심는 쪽", OK), ("노드 경계", INFO)])
d.save("01-01-service-kubeproxy.svg")
print("ok service-kubeproxy")
