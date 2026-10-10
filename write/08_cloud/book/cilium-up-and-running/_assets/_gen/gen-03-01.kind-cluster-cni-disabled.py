# 타입 스펙: type-deployment — kind 노드 세 개(Docker 컨테이너)와 각 노드의 비어 있는 CNI 자리·미설치 Cilium 에이전트 자리.
# 사실 출처: cil3.txt 줄 138~214 (kind.yaml, kubectl get nodes NotReady, NetworkReady=false·cni plugin not initialized), 02-01 노트 §2 (05-cilium.conflist 는 에이전트가 설치).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 416
d = D(W, H, "CILIUM UP AND RUNNING · 03-01 §2", "CNI 없이 뜬 kind 노드 세 개",
      "disableDefaultCNI 로 kindnetd 를 빼면 kubelet 이 네트워크를 준비하지 못한다",
      "노드 안에 CNI 설정 파일과 Cilium 에이전트가 들어올 자리가 비어 있다")

Y_TOP, H_NODE, W_NODE, GAP, X0 = 104, 236, 272, 24, 24
nodes = [
    ("kind-control-plane", "control-plane"),
    ("kind-worker", "worker"),
    ("kind-worker2", "worker"),
]
def dashed(x, y, w, h, c, fill=None):
    f = f'{c}1F' if fill else "none"
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="4" fill="{f}" stroke="{c}" stroke-width="1.3" stroke-dasharray="5 4"/>')

for i, (name, role) in enumerate(nodes):
    x = X0 + i * (W_NODE + GAP)
    d.box(x, Y_TOP, W_NODE, H_NODE, PAPER2, RULE, sw=0.9, r=8)
    d.t(x + 14, Y_TOP + 24, name, 12, INK, MONO, "start", 600)
    d.chip(x + W_NODE - 46, Y_TOP + 20, "NotReady", BAD, size=11)
    d.t(x + 14, Y_TOP + 46, f"{role} · v1.33.4", 11, MUTED, MONO, "start")
    d.line(x + 12, Y_TOP + 60, x + W_NODE - 12, Y_TOP + 60, RULE, 0.6)
    # kubelet
    d.box(x + 12, Y_TOP + 72, W_NODE - 24, 52, PAPER, RULE, sw=0.7, r=4)
    d.t(x + 22, Y_TOP + 92, "kubelet", 12, INK, KR, "start", 600)
    d.t(x + 22, Y_TOP + 112, "NetworkReady=false", 11, BAD, MONO, "start")
    # 비어 있는 CNI 자리 (focal)
    dashed(x + 12, Y_TOP + 136, W_NODE - 24, 44, ACC, fill=True)
    d.t(x + 22, Y_TOP + 156, "CNI 설정 자리", 12, ACC, KR, "start", 600)
    d.t(x + 22, Y_TOP + 172, "05-cilium.conflist", 11, MUTED, MONO, "start")
    # 미설치 Cilium 에이전트 자리
    dashed(x + 12, Y_TOP + 188, W_NODE - 24, 36, SOFT)
    d.t(x + 22, Y_TOP + 210, "DaemonSet cilium", 11, SOFT, MONO, "start")

# 설정 막대
yb = Y_TOP + H_NODE + 20
d.box(X0, yb, 872, 40, PAPER2, RULE, sw=0.9, r=6)
d.t(X0 + 16, yb + 25, "kind.yaml", 12, SOFT, MONO, "start")
d.t(X0 + 120, yb + 25, "networking.disableDefaultCNI: true", 12, INK, MONO, "start", 600)
d.chip(X0 + 756, yb + 20, "kindnetd 제외", WARN, size=12)

d.save("03-01.kind-cluster-cni-disabled.svg")
