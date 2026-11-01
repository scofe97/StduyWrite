# 타입 스펙: type-layers — 커널 eBPF 데이터패스 위에 CNI 패브릭과 기능 묶음을 얹는 구조. 칸마다 다루는 절 번호.
# 사실 출처: 본문 §3 L105 (필요한 기능만 단계적으로 켜는 모듈형 구조) · 원서 1장 Cilium's Use Cases (p.5-6: 단순 CNI 로 시작해
#   encryption·observability·service mesh·multicluster 를 켠다, p.6-13 기능별 절).
# 본문 절: §1(connect() 소켓 훅·BPF 맵 조회), §3(IPAM·BGP·Maglev·Gateway API·FQDN·투명 암호화·Hubble 플로우 메트릭), §4(서비스 메시), §5(netkit).
# 본문·원서에 "5계층"·계층 번호·쌓는 순서가 없어 L1~L5 와 상승 축을 빼고 칩에 절 번호를 둔다. tc·서비스 맵은 본문에 없어 뺀다 (2026-11-01 검증).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 01-01", "eBPF 데이터패스 위에 켜는 Cilium 기능",
      "커널 eBPF 데이터패스 위에서 CNI 기본 연결부터 부하분산, 보안 정책, 서비스 메시, 가시성까지 한 스택으로 처리하는 구조",
      "기본 CNI 에서 시작해 필요한 기능만 켜는 모듈형 구조")

# 스택 영역
X0 = 24
W_STACK = 872
H_LAYER = 52
GAP = 10
Y0 = 108

layers = [
    ("§3", "네트워크 관측", "Hubble · 커널 플로우 메트릭 수집", INFO, False),
    ("§3", "신원 기반 정책 및 암호화", "CiliumNetworkPolicy · FQDN · 투명 암호화", OK, False),
    ("§3·§4", "트래픽 제어 및 서비스 메시", "kube-proxy 대체 · Maglev · Gateway API", WARN, False),
    ("§3·§5", "CNI 네트워크 패브릭", "Pod IPAM · veth/netkit · BGP 광고", SOFT, False),
    ("§1", "커널 eBPF 데이터패스", "connect() 소켓 훅 · BPF 맵 조회", ACC, True),
]

for i, (tag, name, sub, color, focal) in enumerate(layers):
    y = Y0 + i * (H_LAYER + GAP)
    if focal:
        d.tone(X0, y, W_STACK, H_LAYER, color, r=6, op="18", sw=1.4)
    else:
        d.box(X0, y, W_STACK, H_LAYER, PAPER2, RULE, sw=0.9, r=6)

    # 태그
    d.box(X0 + 12, y + 14, 56, 24, PAPER, color, sw=1.0, r=4)
    d.t(X0 + 40, y + 30, tag, 11, color, MONO, "middle", 600)

    # 계층 이름
    name_color = color if focal else INK
    d.t(X0 + 82, y + 31, name, 14, name_color, KR, "start", 600)

    # 오른쪽 설명 서브라벨 (한글 포함이므로 KR 글꼴 적용)
    d.t(X0 + W_STACK - 16, y + 31, sub, 12, MUTED, KR, "end")

# 범례
d.legend(430, [
    ("데이터패스", ACC),
    ("CNI 패브릭", SOFT),
    ("트래픽 제어", WARN),
    ("보안 정책", OK),
    ("관측 플랫폼", INFO),
])

d.save("01-01.chapter-overview.svg")
