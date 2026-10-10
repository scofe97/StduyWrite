# 타입 스펙: type-data-flow — 같은 노드 Pod 직결·다른 노드 WireGuard 암호화 터널·호스트 네임스페이스 경로 비교. focal 은 노드 사이 WireGuard 암호화 구간.
# 사실 출처: Cilium Up and Running 14장 cil14.txt 줄 108-168(Figure 14-3·ClusterIP 서비스 주소 해석 후 암호화 판정) / docs.cilium.io v1.20 security/network/encryption-wireguard/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 456
d = D(W, H, "CILIUM UP AND RUNNING · 14-01 §2", "노드 경계를 넘는 트래픽만 WireGuard 로 암호화한다",
      "같은 노드 Pod 는 eBPF 로 직결하고, 다른 노드 Pod 만 WireGuard 터널로 보낸다",
      "같은 노드 Pod 는 eBPF 로 직결하고, 다른 노드 Pod 만 WireGuard 터널로 보낸다")

Y0, HN = 104, 276
# 왼쪽: 노드 A
XL, WL = 24, 380
d.box(XL, Y0, WL, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XL + 14, Y0 + 24, "노드 A", 12, INFO, KR, "start", 600)

# 노드 A 내부: client Pod
d.tone(XL + 14, Y0 + 40, WL - 28, 56, INFO, r=6, op="10", sw=1.0)
d.t(XL + 26, Y0 + 64, "출발 Pod (client)", 12, INK, KR, "start", 600)
d.t(XL + 26, Y0 + 84, "Pod IP", 11, INFO, KR, "start")

# 노드 A 내부: eBPF datapath & Service 해석
d.tone(XL + 14, Y0 + 110, WL - 28, 64, SOFT, r=6, op="12", sw=1.0)
d.t(XL + 26, Y0 + 132, "Cilium eBPF 데이터패스", 12, INK, KR, "start", 600)
d.t(XL + 26, Y0 + 154, "ClusterIP 해석 뒤 백엔드 노드 판정", 11, MUTED, KR, "start")

# 노드 A 내부: 같은 노드 Pod (경로 1)
d.tone(XL + 14, Y0 + 192, WL - 28, 68, OK, r=6, op="10", sw=1.0)
d.t(XL + 26, Y0 + 216, "같은 노드 Pod", 12, INK, KR, "start", 600)
d.t(XL + 26, Y0 + 240, "eBPF 커널 직결 · 암호화 생략", 11, OK, KR, "start")

# 오른쪽: 노드 B
XR, WR = 516, 380
d.box(XR, Y0, WR, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XR + 14, Y0 + 24, "노드 B", 12, OK, KR, "start", 600)

# 노드 B 내부: WireGuard 복호화 장치
d.tone(XR + 14, Y0 + 40, WR - 28, 68, ACC, r=6, op="12", sw=1.2)
d.t(XR + 26, Y0 + 64, "cilium_wg0 장치", 12, ACC, MONO, "start", 600)
d.t(XR + 26, Y0 + 88, "WireGuard 복호화 (키 검증)", 11, MUTED, KR, "start")

# 노드 B 내부: webserver Pod (도착지)
d.tone(XR + 14, Y0 + 128, WR - 28, 64, OK, r=6, op="10", sw=1.0)
d.t(XR + 26, Y0 + 152, "도착 Pod (webserver)", 12, INK, KR, "start", 600)
d.t(XR + 26, Y0 + 174, "Pod IP", 11, OK, KR, "start")

# 노드 B 내부: 호스트 네임스페이스 안내
d.tone(XR + 14, Y0 + 208, WR - 28, 52, SOFT, r=6, op="08", sw=0.8)
d.t(XR + 26, Y0 + 232, "hostNetwork Pod · 호스트 프로세스", 11, MUTED, KR, "start")
d.t(XR + 26, Y0 + 248, "노드-Pod 트래픽은 암호화 제외", 11, SOFT, KR, "start")

# 화살표 1: client Pod -> eBPF
d.arrow([(XL + WL / 2, Y0 + 96), (XL + WL / 2, Y0 + 110)], MUTED, "ar", 1.2)

# 화살표 2: eBPF -> 같은 노드 Pod (녹색)
d.arrow([(XL + 60, Y0 + 174), (XL + 60, Y0 + 192)], OK, "ok", 1.4)

# 화살표 3: 노드 A eBPF -> 노드 사이 WireGuard 터널 -> 노드 B cilium_wg0 (주황색 focal)
ym_tunnel = Y0 + 74
d.arrow([(XL + WL - 14, Y0 + 142), (XL + WL + 18, Y0 + 142), (XL + WL + 18, ym_tunnel), (XR + 14, ym_tunnel)], ACC, "acc", 1.6)
d.t(XL + WL + 30, ym_tunnel - 12, "WireGuard", 11, ACC, MONO, "start", 600)
d.t(XL + WL + 30, ym_tunnel + 16, "UDP 51871", 11, ACC, MONO, "start")

# 화살표 4: 노드 B cilium_wg0 -> webserver Pod
d.arrow([(XR + WR / 2, Y0 + 108), (XR + WR / 2, Y0 + 128)], OK, "ok", 1.2)

LEG_Y = Y0 + HN + 16
d.legend(LEG_Y, [("노드 간 WireGuard 암호화", ACC), ("eBPF 직결 (암호화 생략)", OK), ("암호화 제외 대상", SOFT)])
d.save("14-01.traffic-flow.svg")
