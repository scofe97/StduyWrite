# 타입 스펙: type-layers — 커널 eBPF 데이터패스부터 관측까지 Cilium 5계층 아키텍처.
# 사실 출처: Cilium Up and Running 1장 Cilium's Use Cases (§Networking as a CNI, Ingress, Mesh, Policy, Encryption, Hubble).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 01-01", "eBPF 기반 Cilium 5계층 아키텍처",
      "커널 eBPF 데이터패스 위에서 CNI 기본 연결부터 부하분산, 보안 정책, 서비스 메시, 가시성까지 한 스택으로 처리하는 구조",
      "커널 eBPF 가 네트워크 패브릭과 보안·관측을 일원화합니다")

# 스택 영역
X0 = 76
W_STACK = 808
H_LAYER = 52
GAP = 10
Y0 = 108

layers = [
    ("L5", "네트워크 및 보안 관측", "Hubble · 커널 이벤트 수집 · 서비스 맵", INFO, False),
    ("L4", "신원 기반 정책 및 보안", "CiliumNetworkPolicy · FQDN · 투명 암호화", OK, False),
    ("L3", "서비스 메시 및 트래픽 제어", "kube-proxy 대체 · Maglev LB · Gateway API", WARN, False),
    ("L2", "CNI 네트워크 패브릭", "Pod IPAM · veth/netkit 연결 · BGP 광고", SOFT, False),
    ("L1", "커널 eBPF 데이터패스", "tc · 소켓 훅 · BPF 맵 기반 조회", ACC, True),
]

for i, (tag, name, sub, color, focal) in enumerate(layers):
    y = Y0 + i * (H_LAYER + GAP)
    if focal:
        d.tone(X0, y, W_STACK, H_LAYER, color, r=6, op="18", sw=1.4)
    else:
        d.box(X0, y, W_STACK, H_LAYER, PAPER2, RULE, sw=0.9, r=6)

    # 태그
    d.box(X0 + 12, y + 14, 38, 24, PAPER, color, sw=1.0, r=4)
    d.t(X0 + 31, y + 30, tag, 11, color, MONO, "middle", 600)

    # 계층 이름
    name_color = color if focal else INK
    d.t(X0 + 64, y + 31, name, 14, name_color, KR, "start", 600)

    # 오른쪽 설명 서브라벨
    d.t(X0 + W_STACK - 16, y + 31, sub, 12, MUTED, MONO, "end")

# 왼쪽 상승 방향 표시
d.line(38, Y0 + 10, 38, Y0 + 5 * (H_LAYER + GAP) - 16, SOFT, sw=1.0, dash="3 3")
d.arrow([(38, Y0 + 5 * (H_LAYER + GAP) - 16), (38, Y0 + 6)], SOFT, "soft", sw=1.2)
d.t(38, Y0 - 4, "계층 ↑", 11, SOFT, KR, "middle", 600)

# 범례
d.legend(430, [
    ("데이터패스", ACC),
    ("CNI 패브릭", SOFT),
    ("트래픽 제어", WARN),
    ("보안 정책", OK),
    ("관측 플랫폼", INFO),
])

d.save("01-01.chapter-overview.svg")
