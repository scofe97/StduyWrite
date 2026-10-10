# 타입 스펙: type-architecture — L2 공지 정책과 쿠버네티스 리스 기반 단일 노드 선출 아키텍처
# 사실 출처: 추출본 cil10.txt 줄 200-260(l2policy.yaml·serviceSelector·nodeSelector·interfaces·Lease 조회) / docs.cilium.io v1.20 network/l2-announcements/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 560
d = D(W, H, "CILIUM UP AND RUNNING · 10-01 §2", "L2 Announcements 정책과 리스 기반 리더 선출",
      "정책과 일치하는 노드 중 단 하나의 노드만 리스를 쥐고 BPF 맵으로 ARP 에 응답합니다",
      "Kubernetes Coordination Lease · cilium-agent · BPF responder")

# 1. 상단: 선언 계층 (정책 & 서비스)
# 좌측 정책 박스
PX, PY, PW, PH = 40, 104, 400, 100
d.box(PX, PY, PW, PH, PAPER2, INFO, 1.0)
d.t(PX + 16, PY + 24, "CiliumL2AnnouncementPolicy", 12, INFO, MONO, "start", 600)
d.t(PX + PW - 16, PY + 24, "l2-policy", 11, MUTED, MONO, "end")
d.line(PX + 12, PY + 34, PX + PW - 12, PY + 34, RULE, 0.6)
d.t(PX + 16, PY + 52, "serviceSelector: announcement=l2", 11, INK, MONO, "start")
d.t(PX + 16, PY + 70, "nodeSelector: !control-plane (워커 한정)", 11, INK, MONO, "start")
d.t(PX + 16, PY + 88, "interfaces: ^eth0 · loadBalancerIPs: true", 11, MUTED, MONO, "start")

# 우측 서비스 박스
SX, SY, SW, SH = 480, 104, 400, 100
d.box(SX, SY, SW, SH, PAPER2, WARN, 1.0)
d.t(SX + 16, SY + 24, "Service (type: LoadBalancer)", 12, WARN, MONO, "start", 600)
d.t(SX + SW - 16, SY + 24, "default/httpd", 11, MUTED, MONO, "end")
d.line(SX + 12, SY + 34, SX + SW - 12, SY + 34, RULE, 0.6)
d.t(SX + 16, SY + 52, "EXTERNAL-IP: 172.18.255.200", 11, INK, MONO, "start")
d.t(SX + 16, SY + 70, "labels: announcement=l2", 11, INK, MONO, "start")
d.t(SX + 16, SY + 88, "externalTrafficPolicy: Local 비호환", 11, MUTED, MONO, "start")

# 2. 중앙: 조정 계층 (Kubernetes Lease)
LX, LY, LW, LH = 210, 226, 500, 64
d.tone(LX, LY, LW, LH, ACC, r=6, op="14", sw=1.3)
d.t(LX + LW / 2, LY + 24, "kube-apiserver Lease (coordination.k8s.io/v1)", 12, ACC, MONO, "middle", 600)
d.t(LX + LW / 2, LY + 44, "cilium-l2announce-default-httpd · holder: kind-worker2 · 15s", 11, INK, MONO, "middle")

# 정책 & 서비스 -> Lease 화살표
d.arrow([(PX + PW / 2, PY + PH), (PX + PW / 2, LY)], INFO, "info", 1.2)
d.arrow([(SX + SW / 2, SY + SH), (SX + SW / 2, LY)], WARN, "warn", 1.2)

# 3. 하단: 노드 계층 (선출 노드 vs 대기 노드)
# 좌측 노드 (리더)
N1X, NY, NW, NH = 40, 318, 400, 166
d.box(N1X, NY, NW, NH, PAPER2, OK, 1.2)
d.t(N1X + 16, NY + 26, "kind-worker2 (선출된 리더 노드)", 13, OK, KR, "start", 600)
d.chip(N1X + NW - 56, NY + 22, "리더", OK, size=11)
d.line(N1X + 12, NY + 40, N1X + NW - 12, NY + 40, RULE, 0.6)

d.box(N1X + 16, NY + 52, NW - 32, 32, PAPER, RULE, 0.8)
d.t(N1X + 28, NY + 72, "cilium-agent: 5초마다 리스 갱신", 11, INK, KR, "start")

d.box(N1X + 16, NY + 90, NW - 32, 32, PAPER, ACC, 0.8)
d.t(N1X + 28, NY + 110, "BPF cilium_l2_responder_v4: VIP 등록", 11, ACC, MONO, "start")

d.box(N1X + 16, NY + 128, NW - 32, 28, PAPER, OK, 0.8)
d.t(N1X + 28, NY + 146, "eth0 (ea:f5:fb:51:a1:17): ARP Reply 응답", 11, OK, MONO, "start")

# 우측 노드 (대기)
N2X = 480
d.box(N2X, NY, NW, NH, PAPER2, SOFT, 1.0)
d.t(N2X + 16, NY + 26, "kind-worker (대기 노드)", 13, MUTED, KR, "start", 600)
d.chip(N2X + NW - 56, NY + 22, "대기", SOFT, size=11)
d.line(N2X + 12, NY + 40, N2X + NW - 12, NY + 40, RULE, 0.6)

d.box(N2X + 16, NY + 52, NW - 32, 32, PAPER, RULE, 0.8)
d.t(N2X + 28, NY + 72, "cilium-agent: 리스 만료 감시", 11, MUTED, KR, "start")

d.box(N2X + 16, NY + 90, NW - 32, 32, PAPER, RULE, 0.8)
d.t(N2X + 28, NY + 110, "BPF responder: 비활성 (미등록)", 11, MUTED, MONO, "start")

d.box(N2X + 16, NY + 128, NW - 32, 28, PAPER, RULE, 0.8)
d.t(N2X + 28, NY + 146, "eth0: ARP 무응답 (침묵 유지)", 11, MUTED, MONO, "start")

# Lease -> 노드 화살표
d.arrow([(N1X + NW / 2, LY + LH), (N1X + NW / 2, NY)], OK, "ok", 1.4)
d.arrow([(N2X + NW / 2, LY + LH), (N2X + NW / 2, NY)], SOFT, "soft", 1.2, dash="3 3")

# 범례
d.legend(514, [("정책", INFO), ("서비스 VIP", WARN), ("조정 리스", ACC), ("선출 리더", OK), ("대기 상태", SOFT)])
d.save("10-01.l2-policy-lease-architecture.svg")
