# 타입 스펙: type-deployment — 워커 노드 안 사용자 공간 DaemonSet(cilium, cilium-envoy)과 커널 공간(eBPF 데이터패스)의 배치 및 Pod 교체 중 공백 비교.
# 값 근거: 본문 §2 및 ch16.txt 줄 547-613(eBPF datapath 유지, L3/L4 유지, cilium-envoy DaemonSet, Gateway API/Ingress/HTTP/SNI/TLS interception 끊김, HTTP/2·WebSocket 포함, Cilium DaemonSet DNS 프록시 드롭, CNI 부재로 새 Pod 없음, preflight 이미지 사전 pull), v1.20.2 values.yaml(envoy.enabled)
import sys

sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 560
d = D(
    W,
    H,
    "CILIUM UP AND RUNNING · 16-02 §2",
    "L7 프록시와 eBPF 데이터패스의 재시작 공백",
    "사용자 공간 DaemonSet 인 cilium-envoy 와 cilium 이 교체되는 동안 기존 L7 연결과 DNS 요청은 끊기지만, 커널에 남은 eBPF 데이터패스는 기존 L3·L4 연결을 계속 나릅니다.",
    lead="재시작이나 업그레이드 때 사용자 공간 Pod 는 비지만 커널 eBPF 프로그램은 남습니다.",
)

# Zone 1: User space (DaemonSet pods)
ZX, ZW = 24, 912
d.box(ZX, 100, ZW, 232, "rgba(245,245,243,0.02)", "rgba(245,245,243,0.20)", 0.9, 8)
d.t(ZX + 16, 122, "사용자 공간 · DaemonSet 교체 시 공백 (기존 삭제 → pull → Ready)", 13, MUTED, KR, "start", 600)

# Zone 2: Kernel space (eBPF datapath)
d.box(ZX, 360, ZW, 128, "rgba(245,245,243,0.02)", "rgba(245,245,243,0.20)", 0.9, 8)
d.t(ZX + 16, 382, "커널 공간 · 재시작 중 유지", 13, MUTED, KR, "start", 600)

# Orthogonal paths between Kernel datapath and User space DaemonSets (drawn before nodes!)
# L3/L4 traffic enters Kernel eBPF directly
d.arrow([(44, 436), (180, 436)], OK, "ok", 1.4)
d.t(112, 424, "L3·L4 트래픽", 13, OK, KR, "middle", 600)

# cilium agent -> eBPF sync (dashed downward)
d.arrow([(300, 312), (300, 388)], MUTED, "ar", 1.2, "4 3")
d.t(288, 350, "eBPF 맵·정책 동기화", 13, MUTED, KR, "end")

# eBPF -> cilium DNS proxy (upward)
d.arrow([(416, 388), (416, 316)], WARN, "warn", 1.3)
d.t(428, 350, "DNS 질의", 13, WARN, KR, "start", 600)

# eBPF -> cilium-envoy L7 proxy (upward)
d.arrow([(728, 388), (728, 316)], ACC, "acc", 1.4)
d.t(740, 350, "L7 HTTP · TLS", 12, ACC, MONO, "start", 600)

# Node 1: cilium DaemonSet (WARN)
N1X, N1Y, N1W, N1H = 60, 140, 412, 172
d.tone(N1X, N1Y, N1W, N1H, WARN, r=6, op="10", sw=1.1)
d.box(N1X + 12, N1Y + 10, 36, 16, PAPER, WARN, 0.8, 2)
d.t(N1X + 30, N1Y + 21, "POD", 8, WARN, MONO, "middle", 600)
d.box(N1X + N1W - 72, N1Y + 10, 60, 16, PAPER, RULE, 0.8, 2)
d.t(N1X + N1W - 42, N1Y + 21, "1/node", 8, MUTED, MONO, "middle", 600)
d.t(N1X + 60, N1Y + 24, "cilium DaemonSet", 14, WARN, MONO, "start", 700)
d.box(N1X + 16, N1Y + 42, 380, 28, "rgba(245,245,243,0.05)", MUTED, 0.8, 4)
d.t(N1X + 28, N1Y + 61, "DNS 프록시 · CNI 플러그인", 13, INK, KR, "start", 600)
d.t(N1X + 384, N1Y + 60, "v1.20.2", 10, MUTED, MONO, "end")
d.t(N1X + 16, N1Y + 98, "에이전트 중단 시: DNS 정책이 걸린 Pod 의 DNS 요청 드롭", 13, WARN, KR, "start")
d.t(N1X + 16, N1Y + 122, "캐시 TTL 만료 전이면 영향 작음", 13, MUTED, KR, "start")
d.t(N1X + 16, N1Y + 146, "CNI 도 내려가 새 Pod 기동 없음", 13, MUTED, KR, "start")

# Node 2: cilium-envoy DaemonSet (Focal ACC)
N2X, N2Y, N2W, N2H = 516, 140, 404, 172
d.tone(N2X, N2Y, N2W, N2H, ACC, r=6, op="14", sw=1.4)
d.box(N2X + 12, N2Y + 10, 36, 16, PAPER, ACC, 0.8, 2)
d.t(N2X + 30, N2Y + 21, "POD", 8, ACC, MONO, "middle", 600)
d.box(N2X + N2W - 72, N2Y + 10, 60, 16, PAPER, RULE, 0.8, 2)
d.t(N2X + N2W - 42, N2Y + 21, "1/node", 8, MUTED, MONO, "middle", 600)
d.t(N2X + 60, N2Y + 24, "cilium-envoy DaemonSet", 14, ACC, MONO, "start", 700)
d.box(N2X + 16, N2Y + 42, 372, 28, "rgba(245,245,243,0.05)", MUTED, 0.8, 4)
d.t(N2X + 28, N2Y + 61, "Envoy L7 프록시", 13, INK, KR, "start", 600)
d.t(N2X + 376, N2Y + 60, "v1.20.2 default", 10, MUTED, MONO, "end")
d.t(N2X + 16, N2Y + 98, "Gateway API · Ingress · HTTP · SNI · TLS", 12, INK, MONO, "start")
d.t(N2X + 16, N2Y + 122, "교체 공백 동안 기존 HTTP/2·WebSocket 끊김", 13, ACC, KR, "start")
d.t(N2X + 16, N2Y + 146, "preflight pull · 사전 검증으로 공백 축소", 13, MUTED, KR, "start")

# Node 3: Kernel eBPF Datapath (OK)
N3X, N3Y, N3W, N3H = 184, 392, 736, 84
d.tone(N3X, N3Y, N3W, N3H, OK, r=6, op="12", sw=1.1)
d.box(N3X + 12, N3Y + 10, 56, 16, PAPER, OK, 0.8, 2)
d.t(N3X + 40, N3Y + 21, "KERNEL", 8, OK, MONO, "middle", 600)
d.t(N3X + 80, N3Y + 24, "eBPF 데이터패스 (커널 상주)", 14, OK, KR, "start", 700)
d.box(N3X + 320, N3Y + 8, 396, 26, "rgba(245,245,243,0.05)", MUTED, 0.8, 4)
d.t(N3X + 332, N3Y + 26, "기존 L3·L4 정책 · 서비스 전달 유지", 13, INK, KR, "start")
d.t(N3X + 16, N3Y + 62, "Pod 삭제 → 새 이미지 pull → Ready 대기 동안에도 기존 L3·L4 트래픽 정상 전달", 13, MUTED, KR, "start")

d.legend(
    H - 44,
    [
        ("L7 프록시 공백 (핵심)", ACC),
        ("DNS 프록시 드롭", WARN),
        ("커널 데이터패스 유지", OK),
    ],
)
d.save("16-02.l7-proxy-restart-gap.svg")
print("ok 16-02 l7 gap")
