# 타입 스펙: type-architecture — 클러스터 워커 노드의 BGP 스피커와 외부 FRR 라우터 간 피어링 및 프리픽스 광고 아키텍처
# 사실 출처: 추출본 cil10.txt 줄 586-664(노드 IP 172.18.0.2/3, FRR 172.18.0.6, ASN 64512), 698-700(httpd 172.18.255.200), 1024-1058(BGP Established, NextHop, ECMP route) / docs.cilium.io v1.20 network/bgp-control-plane
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 950, 480
d = D(W, H, "CILIUM UP AND RUNNING · 10-02", "Cilium BGP 제어 평면 토폴로지와 경로 광고",
      "클러스터 노드가 외부 라우터와 iBGP 세션을 맺고 서비스 VIP 경로를 광고한다",
      "예시 kind 클러스터 · FRR 10.3.1 라우터 · ASN 64512")

# Zone 1: Kubernetes Cluster (Left: x=24, y=100, w=430, h=314)
CL_X, CL_Y, CL_W, CL_H = 24, 100, 430, 314
d.box(CL_X, CL_Y, CL_W, CL_H, PAPER2, RULE, 1.0, r=8)
d.t(CL_X + 16, CL_Y + 24, "Kubernetes 클러스터", 13, INK, KR, "start", 600)
d.t(CL_X + CL_W - 16, CL_Y + 24, "172.18.0.0/16", 11, MUTED, MONO, "end")

# Service Box in Cluster
SVC_X, SVC_Y, SVC_W, SVC_H = CL_X + 16, CL_Y + 36, CL_W - 32, 44
d.box(SVC_X, SVC_Y, SVC_W, SVC_H, PAPER, INFO, 0.9, r=6)
d.t(SVC_X + 14, SVC_Y + 20, "httpd 서비스", 12, INFO, KR, "start", 600)
d.t(SVC_X + 14, SVC_Y + 35, "172.18.255.200/32", 11, INK, MONO, "start")
d.chip(SVC_X + SVC_W - 68, SVC_Y + 22, "LoadBalancer", INFO, 11, pad=4)

# Node 1: kind-worker (Stacked Top)
N1_X, N1_Y, N1_W, N1_H = CL_X + 16, CL_Y + 90, CL_W - 32, 98
d.box(N1_X, N1_Y, N1_W, N1_H, PAPER, RULE, 0.9, r=6)
d.t(N1_X + 14, N1_Y + 20, "kind-worker (172.18.0.2 · AS 64512)", 11, INK, MONO, "start", 600)

d.box(N1_X + 12, N1_Y + 30, (N1_W - 32) / 2, 56, PAPER2, OK, 0.8, r=4)
d.t(N1_X + 12 + (N1_W - 32) / 4, N1_Y + 52, "httpd 백엔드 Pod", 11, OK, KR, "middle", 600)
d.t(N1_X + 12 + (N1_W - 32) / 4, N1_Y + 72, "포트 80 서빙", 11, MUTED, KR, "middle")

d.tone(N1_X + 20 + (N1_W - 32) / 2, N1_Y + 30, (N1_W - 32) / 2, 56, ACC, r=4, op="14", sw=1.1)
d.t(N1_X + 20 + 3 * (N1_W - 32) / 4, N1_Y + 52, "cilium-agent", 11, ACC, MONO, "middle", 600)
d.t(N1_X + 20 + 3 * (N1_W - 32) / 4, N1_Y + 72, "BGP 스피커 (포트 179)", 11, MUTED, KR, "middle")

# Node 2: kind-worker2 (Stacked Bottom)
N2_X, N2_Y, N2_W, N2_H = CL_X + 16, CL_Y + 198, CL_W - 32, 98
d.box(N2_X, N2_Y, N2_W, N2_H, PAPER, RULE, 0.9, r=6)
d.t(N2_X + 14, N2_Y + 20, "kind-worker2 (172.18.0.3 · AS 64512)", 11, INK, MONO, "start", 600)

d.box(N2_X + 12, N2_Y + 30, (N2_W - 32) / 2, 56, PAPER2, OK, 0.8, r=4)
d.t(N2_X + 12 + (N2_W - 32) / 4, N2_Y + 52, "httpd 백엔드 Pod", 11, OK, KR, "middle", 600)
d.t(N2_X + 12 + (N2_W - 32) / 4, N2_Y + 72, "포트 80 서빙", 11, MUTED, KR, "middle")

d.tone(N2_X + 20 + (N2_W - 32) / 2, N2_Y + 30, (N2_W - 32) / 2, 56, ACC, r=4, op="14", sw=1.1)
d.t(N2_X + 20 + 3 * (N2_W - 32) / 4, N2_Y + 52, "cilium-agent", 11, ACC, MONO, "middle", 600)
d.t(N2_X + 20 + 3 * (N2_W - 32) / 4, N2_Y + 72, "BGP 스피커 (포트 179)", 11, MUTED, KR, "middle")

# Zone 2: External Router (FRR) (Right: x=520, y=100, w=406, h=314)
RT_X, RT_Y, RT_W, RT_H = 520, 100, 406, 314
d.box(RT_X, RT_Y, RT_W, RT_H, PAPER2, RULE, 1.0, r=8)
d.t(RT_X + 16, RT_Y + 24, "외부 라우터 (FRR)", 13, INK, KR, "start", 600)
d.t(RT_X + RT_W - 16, RT_Y + 24, "172.18.0.6", 11, MUTED, MONO, "end")
d.t(RT_X + 16, RT_Y + 44, "AS 64512 · ID 172.18.255.254", 11, SOFT, MONO, "start")

# BGP Session box
BGP_Y = RT_Y + 56
d.tone(RT_X + 16, BGP_Y, RT_W - 32, 64, WARN, r=6, op="12", sw=1.1)
d.t(RT_X + 26, BGP_Y + 20, "iBGP 피어링 (Established)", 11, WARN, KR, "start", 600)
d.t(RT_X + 26, BGP_Y + 38, "172.18.0.2 : PfxRcd 1", 11, INK, MONO, "start")
d.t(RT_X + 26, BGP_Y + 54, "172.18.0.3 : PfxRcd 1", 11, INK, MONO, "start")

# Routing Table (FIB) Box
FIB_Y = RT_Y + 128
d.box(RT_X + 16, FIB_Y, RT_W - 32, 90, PAPER, OK, 1.0, r=6)
d.t(RT_X + 26, FIB_Y + 20, "커널 경로표 (ECMP)", 11, OK, KR, "start", 600)
d.t(RT_X + 26, FIB_Y + 38, "172.18.255.200 (proto bgp)", 11, OK, MONO, "start")
d.t(RT_X + 36, FIB_Y + 56, "nexthop 172.18.0.2", 11, MUTED, MONO, "start")
d.t(RT_X + 36, FIB_Y + 72, "nexthop 172.18.0.3", 11, MUTED, MONO, "start")

# External Client Verification Box
CLI_Y = RT_Y + 226
d.box(RT_X + 16, CLI_Y, RT_W - 32, 54, PAPER, INFO, 0.9, r=6)
d.t(RT_X + 26, CLI_Y + 20, "클라이언트 연결 검증", 11, INFO, KR, "start", 600)
d.t(RT_X + 26, CLI_Y + 40, "wget 172.18.255.200 → 200 OK", 11, INK, MONO, "start")

# Arrows: BGP Route Advertisements (Cluster -> Router, strictly axis-aligned)
# Arrow 1 from kind-worker cilium-agent (448, 248) -> (478, 248) -> (478, 190) -> (520, 190)
d.arrow([(N1_X + N1_W, N1_Y + 58), (478, N1_Y + 58), (478, BGP_Y + 34), (RT_X, BGP_Y + 34)], ACC, "acc", 1.4)

# Arrow 2 from kind-worker2 cilium-agent (448, 356) -> (494, 356) -> (494, 204) -> (520, 204)
d.arrow([(N2_X + N2_W, N2_Y + 58), (494, N2_Y + 58), (494, BGP_Y + 48), (RT_X, BGP_Y + 48)], ACC, "acc", 1.4)

d.legend(H - 44, [("iBGP 광고", ACC), ("서비스/클라이언트", INFO), ("ECMP 경로", OK), ("세션 상태", WARN)])
d.save("10-02.chapter-overview.svg")
