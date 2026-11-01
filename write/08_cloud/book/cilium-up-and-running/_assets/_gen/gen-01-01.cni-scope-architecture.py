# 타입 스펙: type-architecture — 단일 클러스터 내외부에서 동작하는 Cilium 의 5대 기능 영역.
# 사실 출처: 본문 §3 (L107-130: 표, IPAM, HTTP 라우팅·TLS 종단, ToR BGP 피어링·서비스 IP 광고, L3/L4 는 eBPF·L7 은 Envoy·DNS 는 DNS 프록시,
#   WireGuard/IPsec 을 켜면 노드 간 암호화, Hubble 플로우 메트릭) · 원서 1장 Cilium's Use Cases (p.6 Figure 1-1 network fabric,
#   p.8 Figure 1-2 Gateway API, p.9-10 Cluster Mesh·Figure 1-4 failover, p.10-11 BGP·Figure 1-5 router→node, p.11 CiliumNetworkPolicy,
#   p.12 Figure 1-6 Transparent Encryption).
# 예시 Pod IP·업무 이름·"L3–L7 을 eBPF 가 집행"·"내장 서버" 는 본문·원서에 없거나 본문과 달라 뺀다 (2026-11-01 검증).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §3", "클러스터 안팎의 Cilium 기능 작동 영역",
      "클러스터 입구부터 노드 내부 데이터패스, 외부 망 연동 및 멀티클러스터까지 포괄하는 동작 범위",
      "단일 CNI 기반 네트워크 패브릭·게이트웨이·보안·가시성 통합")

# 영역 1: 외부 인프라 존 (좌측)
d.box(24, 108, 140, 344, PAPER2, RULE, sw=0.9, r=8)
d.t(36, 128, "외부 인프라", 11, SOFT, KR, "start", 600)

d.box(36, 150, 116, 56, PAPER, RULE, sw=0.8, r=6)
d.t(94, 172, "외부 클라이언트", 11, INK, KR, "middle", 600)
d.t(94, 192, "인터넷 트래픽", 11, MUTED, KR, "middle")

d.box(36, 270, 116, 68, PAPER, WARN, sw=1.0, r=6)
d.t(94, 292, "BGP 라우터 / ToR", 11, WARN, KR, "middle", 600)
d.t(94, 312, "BGP 피어링", 11, MUTED, KR, "middle")
d.t(94, 328, "Service IP 광고 수신", 11, SOFT, KR, "middle")

# 영역 2: Kubernetes 클러스터 존 (중앙)
d.box(180, 108, 550, 344, PAPER2, RULE, sw=0.9, r=8)
d.t(194, 128, "KUBERNETES 클러스터", 11, SOFT, KR, "start", 600)

# 클러스터 입구: Ingress & Gateway API
d.box(200, 148, 150, 60, PAPER, WARN, sw=1.1, r=6)
d.t(275, 172, "Ingress / Gateway API", 11, WARN, MONO, "middle", 600)
d.t(275, 194, "HTTP 라우팅 · TLS 종단", 11, INK, KR, "middle")

# 노드 1
d.box(196, 236, 230, 202, PAPER, RULE, sw=0.8, r=6)
d.t(208, 256, "Worker Node 1", 10, SOFT, MONO, "start", 600)

# Pod A
d.box(208, 270, 96, 52, PAPER2, RULE, sw=0.8, r=4)
d.t(256, 292, "Pod A", 11, INK, MONO, "middle", 600)
d.t(256, 310, "IPAM 할당 IP", 11, MUTED, KR, "middle")

# Pod B
d.box(316, 270, 96, 52, PAPER2, RULE, sw=0.8, r=4)
d.t(364, 292, "Pod B", 11, INK, MONO, "middle", 600)
d.t(364, 310, "IPAM 할당 IP", 11, MUTED, KR, "middle")

# eBPF 데이터패스 (노드 1 커널)
d.tone(208, 332, 204, 46, ACC, r=4, op="18", sw=1.2)
d.t(310, 352, "eBPF 데이터패스 · L3/L4 정책", 11, ACC, KR, "middle", 600)
d.t(310, 368, "라벨·신원 기반 집행", 11, INK, KR, "middle")

# Hubble (노드 1)
d.box(208, 386, 204, 40, PAPER2, INFO, sw=0.9, r=4)
d.t(310, 406, "Hubble 관측 (내장)", 11, INFO, KR, "middle", 600)
d.t(310, 420, "커널 플로우 메트릭 수집", 11, MUTED, KR, "middle")

# 노드 2
d.box(484, 236, 230, 202, PAPER, RULE, sw=0.8, r=6)
d.t(496, 256, "Worker Node 2", 10, SOFT, MONO, "start", 600)

# Pod C
d.box(496, 270, 96, 52, PAPER2, RULE, sw=0.8, r=4)
d.t(544, 292, "Pod C", 11, INK, MONO, "middle", 600)
d.t(544, 310, "IPAM 할당 IP", 11, MUTED, KR, "middle")

# eBPF 데이터패스 (노드 2 커널)
d.tone(496, 332, 204, 46, ACC, r=4, op="18", sw=1.2)
d.t(598, 352, "eBPF 데이터패스 · L3/L4 정책", 11, ACC, KR, "middle", 600)
d.t(598, 368, "라벨·신원 기반 집행", 11, INK, KR, "middle")

# Hubble (노드 2)
d.box(496, 386, 204, 40, PAPER2, INFO, sw=0.9, r=4)
d.t(598, 406, "Hubble 관측 (내장)", 11, INFO, KR, "middle", 600)
d.t(598, 420, "커널 플로우 메트릭 수집", 11, MUTED, KR, "middle")

# 노드 간 연결: WireGuard / IPsec 암호화 터널
d.line(426, 355, 484, 355, OK, sw=1.5, dash="4 2")
d.arrow([(426, 355), (484, 355)], OK, "ok", sw=1.5)
d.box(428, 312, 54, 40, PAPER, RULE, sw=0.8, r=4)
d.t(455, 328, "암호화", 11, OK, KR, "middle", 600)
d.t(455, 344, "켰을 때", 11, MUTED, KR, "middle")

# 영역 3: 원격 클러스터 존 (우측)
d.box(746, 108, 150, 344, PAPER2, RULE, sw=0.9, r=8)
d.t(758, 128, "원격 클러스터", 11, SOFT, KR, "start", 600)

d.box(754, 236, 134, 114, PAPER, OK, sw=1.0, r=6)
d.t(821, 262, "Cluster Mesh", 11, OK, MONO, "middle", 600)
d.t(821, 284, "동서 부하분산", 11, INK, KR, "middle")
d.t(821, 306, "서비스 탐색", 11, MUTED, KR, "middle")
d.t(821, 326, "클러스터 간 장애 극복", 11, SOFT, KR, "middle")

# 연결선들: 직교 (Orthogonal)
# 1. 외부 클라이언트 -> Ingress
d.line(152, 178, 200, 178, WARN, sw=1.2)
d.arrow([(152, 178), (200, 178)], WARN, "warn", sw=1.2)

# 2. Ingress -> Node 1 (L-path)
d.path("M 275 208 V 234", WARN, 1.2, m="warn")

# 3. BGP -> Node 1 eBPF
d.line(152, 304, 200, 304, WARN, sw=1.2)
d.arrow([(152, 304), (200, 304)], WARN, "warn", sw=1.2)

# 4. Node 2 -> Cluster Mesh
d.line(714, 262, 754, 262, OK, sw=1.2)
d.arrow([(714, 262), (754, 262)], OK, "ok", sw=1.2)

# 범례
d.legend(474, [
    ("데이터패스 (eBPF)", ACC),
    ("게이트웨이·외부 연동", WARN),
    ("암호화·멀티클러스터", OK),
    ("가시성 (Hubble)", INFO),
])

d.save("01-01.cni-scope-architecture.svg")
