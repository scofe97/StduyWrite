# 타입 스펙: type-architecture — Cilium 노드 레벨 데몬과 클러스터 컨트롤 플레인 분리 아키텍처.
# 사실 출처: Cilium Up and Running 2장 Cilium at a Glance (§Figure 2-1).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 02-01", "Cilium 핵심 컴포넌트 아키텍처 지도",
      "노드마다 데이터패스를 깔고 클러스터 전체 조율은 오퍼레이터가 맡는 이원화 구조",
      "노드 레벨 데몬과 클러스터 컨트롤 플레인이 분리되어 협력합니다")

Y_TOP = 106
H_MAIN = 348

# 좌측 영역: 노드 단위 컴포넌트 (Worker Node)
X_NODE = 24
W_NODE = 506
d.box(X_NODE, Y_TOP, W_NODE, H_MAIN, PAPER2, RULE, sw=0.9, r=8)
d.box(X_NODE + 12, Y_TOP + 12, 190, 24, PAPER, ACC, sw=1.0, r=4)
d.t(X_NODE + 107, Y_TOP + 28, "노드 레벨 (Worker Node)", 11, ACC, KR, "middle", 600)
d.t(X_NODE + W_NODE - 14, Y_TOP + 28, "DaemonSet 배포", 11, MUTED, KR, "end")

# 노드 내부: 사용자 공간 (User Space)
d.box(X_NODE + 14, Y_TOP + 44, 478, 190, PAPER, RULE, sw=0.8, r=6)
d.t(X_NODE + 26, Y_TOP + 62, "사용자 공간 (User Space)", 11, SOFT, KR, "start", 600)

# cilium-agent 파드 (데몬셋) - 내장 컴포넌트 포함
d.tone(X_NODE + 20, Y_TOP + 70, 260, 154, ACC, r=6, op="12", sw=1.1)
d.t(X_NODE + 32, Y_TOP + 88, "cilium-agent 파드", 11, ACC, KR, "start", 600)

# cilium-agent 코어
d.box(X_NODE + 28, Y_TOP + 96, 244, 54, PAPER, RULE, sw=0.8, r=4)
d.t(X_NODE + 150, Y_TOP + 114, "cilium-agent 코어", 11, INK, KR, "middle", 600)
d.t(X_NODE + 150, Y_TOP + 130, "eBPF 맵 · K8s 동기화", 11, MUTED, KR, "middle")
d.t(X_NODE + 150, Y_TOP + 144, "cilium.sock (REST)", 9, SOFT, MONO, "middle")

# DNS Proxy (내장)
d.box(X_NODE + 28, Y_TOP + 158, 118, 56, PAPER, OK, sw=0.8, r=4)
d.t(X_NODE + 87, Y_TOP + 178, "DNS Proxy", 11, OK, MONO, "middle", 600)
d.t(X_NODE + 87, Y_TOP + 196, "FQDN 매핑", 11, INK, KR, "middle")

# Hubble Server (내장)
d.box(X_NODE + 154, Y_TOP + 158, 118, 56, PAPER, INFO, sw=0.8, r=4)
d.t(X_NODE + 213, Y_TOP + 178, "Hubble Server", 11, INFO, MONO, "middle", 600)
d.chip(X_NODE + 213, Y_TOP + 198, "gRPC :4244", INFO, size=8)

# 호스트 바이너리: cilium-cni
d.box(X_NODE + 290, Y_TOP + 70, 192, 64, PAPER2, RULE, sw=0.8, r=4)
d.t(X_NODE + 386, Y_TOP + 90, "cilium-cni 플러그인", 11, INK, KR, "middle", 600)
d.t(X_NODE + 386, Y_TOP + 107, "/opt/cni/bin/cilium-cni", 9, MUTED, MONO, "middle")
d.t(X_NODE + 386, Y_TOP + 122, "호스트 런타임 호출", 11, SOFT, KR, "middle")

# 독립 프록시: cilium-envoy
d.tone(X_NODE + 290, Y_TOP + 142, 192, 82, WARN, r=4, op="18", sw=1.1)
d.t(X_NODE + 386, Y_TOP + 162, "cilium-envoy 파드", 11, WARN, KR, "middle", 600)
d.t(X_NODE + 386, Y_TOP + 182, "독립 데몬셋 (1.16+ 기본)", 11, INK, KR, "middle")
d.t(X_NODE + 386, Y_TOP + 200, "L7 정책 · xDS 연동", 11, MUTED, KR, "middle")

# 노드 내부: 커널 공간 (Kernel Space)
d.tone(X_NODE + 14, Y_TOP + 242, 478, 92, ACC, r=6, op="14", sw=1.2)
d.t(X_NODE + 26, Y_TOP + 262, "커널 공간 (Kernel Space)", 11, ACC, KR, "start", 600)

d.box(X_NODE + 24, Y_TOP + 272, 216, 52, PAPER, RULE, sw=0.8, r=4)
d.t(X_NODE + 132, Y_TOP + 292, "eBPF 프로그램 (tc / tcx)", 11, INK, KR, "middle", 600)
d.t(X_NODE + 132, Y_TOP + 310, "포워딩 · XDP 가속", 11, MUTED, KR, "middle")

d.box(X_NODE + 250, Y_TOP + 272, 230, 52, PAPER, RULE, sw=0.8, r=4)
d.t(X_NODE + 365, Y_TOP + 292, "eBPF 맵 (/sys/fs/bpf)", 11, INK, KR, "middle", 600)
d.t(X_NODE + 365, Y_TOP + 310, "ipcache_v2 · lxc · conntrack", 10, MUTED, MONO, "middle")


# 우측 영역: 클러스터 단위 컨트롤 플레인 (Cluster-wide Services)
X_CLS = 590
W_CLS = 306
d.box(X_CLS, Y_TOP, W_CLS, H_MAIN, PAPER2, RULE, sw=0.9, r=8)
d.box(X_CLS + 12, Y_TOP + 12, 160, 24, PAPER, INFO, sw=1.0, r=4)
d.t(X_CLS + 92, Y_TOP + 28, "클러스터 컨트롤 플레인", 11, INFO, KR, "middle", 600)
d.t(X_CLS + W_CLS - 14, Y_TOP + 28, "Deployment 배포", 11, MUTED, KR, "end")

# cilium-operator
d.tone(X_CLS + 14, Y_TOP + 46, 278, 76, INFO, r=4, op="18", sw=1.2)
d.t(X_CLS + 26, Y_TOP + 68, "cilium-operator (리더 선출)", 11, INFO, KR, "start", 600)
d.t(X_CLS + 26, Y_TOP + 88, "PodCIDR 할당 · CRD 관리", 11, INK, KR, "start")
d.t(X_CLS + 26, Y_TOP + 106, "미사용 엔드포인트 정리", 11, MUTED, KR, "start")

# Hubble Relay
d.box(X_CLS + 14, Y_TOP + 130, 278, 62, PAPER, INFO, sw=0.8, r=4)
d.t(X_CLS + 26, Y_TOP + 152, "Hubble Relay", 11, INFO, MONO, "start", 600)
d.t(X_CLS + 26, Y_TOP + 172, "클러스터 플로우 집계", 11, INK, KR, "start")
d.chip(X_CLS + W_CLS - 58, Y_TOP + 152, "Service :80", INFO, size=9)

# Hubble UI
d.box(X_CLS + 14, Y_TOP + 200, 278, 62, PAPER, RULE, sw=0.8, r=4)
d.t(X_CLS + 26, Y_TOP + 222, "Hubble UI 대시보드", 11, INK, KR, "start", 600)
d.t(X_CLS + 26, Y_TOP + 242, "실시간 서비스 맵", 11, MUTED, KR, "start")
d.chip(X_CLS + W_CLS - 58, Y_TOP + 222, "Service :80", SOFT, size=9)

# Cluster Mesh API Server
d.box(X_CLS + 14, Y_TOP + 270, 278, 64, PAPER, OK, sw=0.9, r=4)
d.t(X_CLS + 26, Y_TOP + 292, "Cluster Mesh API Server", 11, OK, MONO, "start", 600)
d.t(X_CLS + 26, Y_TOP + 312, "멀티클러스터 동기화", 11, INK, KR, "start")
d.chip(X_CLS + W_CLS - 54, Y_TOP + 292, "etcd :2379", OK, size=9)


# 상호 연결선 (Orthogonal paths in 60px corridor)
# 1. Operator -> Agent: PodCIDR 및 CRD 상태 동기화
d.arrow([(X_CLS, Y_TOP + 84), (X_NODE + W_NODE, Y_TOP + 84)], INFO, "info", sw=1.2, dash="3 3")
d.t(560, Y_TOP + 74, "CIDR 동기화", 11, INFO, KR, "middle")

# 2. Hubble Server -> Hubble Relay: 플로우 데이터 gRPC 수집
d.arrow([(X_NODE + W_NODE, Y_TOP + 161), (X_CLS, Y_TOP + 161)], INFO, "info", sw=1.2)
d.t(560, Y_TOP + 151, "gRPC :4244", 9, INFO, MONO, "middle")


# 범례
d.legend(474, [
    ("노드 데몬", ACC),
    ("클러스터 조율", INFO),
    ("독립 프록시", WARN),
    ("내장 관측 · 메시", OK),
])

d.save("02-01.chapter-overview.svg")
