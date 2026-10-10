# 타입 스펙: type-data-flow — 외부 클라이언트에서 LoadBalancer IP, 노드 eBPF, Envoy 를 거쳐 백엔드 Pod 로 전달되는 데이터 흐름.
# 사실 출처: Cilium Up and Running 7장 cil7.txt 줄 87-116(Helm 설정), 132-156(basic-ingress), 195-202(Envoy DaemonSet 및 CEC), 235-242(172.18.255.200/29), 273-285(L2 announcement eth0), 325-347(curl 결과)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 430
d = D(W, H, "CILIUM UP AND RUNNING · 07-01", "Cilium Ingress 의 외부 트래픽 처리 경로",
      "클라이언트가 LoadBalancer IP 로 보낸 HTTP 요청을 eBPF 와 Envoy 가 백엔드로 전달한다",
      "별도 Ingress 컨트롤러 없이 노드 상주 Envoy 와 eBPF 데이터패스가 L7 경로를 처리한다")

Y0, HN = 104, 290

# 1. 왼쪽: 외부 클라이언트
XL, WL = 24, 180
d.box(XL, Y0, WL, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XL + WL / 2, Y0 + 26, "외부 클라이언트", 13, INK, KR, "middle", 600)
d.t(XL + WL / 2, Y0 + 46, "curl HTTP 요청", 12, MUTED, KR)

d.tone(XL + 14, Y0 + 74, WL - 28, 80, INFO, r=6, op="12", sw=1.0)
d.t(XL + WL / 2, Y0 + 102, "HTTP GET", 12, INFO, MONO, "middle", 600)
d.t(XL + WL / 2, Y0 + 126, "172.18.255.200:80", 11, INK, MONO)
d.t(XL + WL / 2, Y0 + 144, "경로 / 또는 /details", 12, MUTED, KR)

d.box(XL + 14, Y0 + 174, WL - 28, 92, PAPER, RULE, sw=0.8, r=6)
d.t(XL + WL / 2, Y0 + 198, "LB IPAM 풀", 12, INK, KR, "middle", 600)
d.t(XL + WL / 2, Y0 + 220, "172.18.255.200/29", 11, OK, MONO)
d.t(XL + WL / 2, Y0 + 246, "서비스마다 주소 1개", 12, MUTED, KR)

# 2. 중앙: kind-worker 노드 내부 (L2 -> eBPF -> Envoy)
XC, WC = 232, 420
d.box(XC, Y0, WC, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XC + 16, Y0 + 26, "worker 노드", 13, OK, KR, "start", 600)

# 2-1. eth0 인터페이스 및 L2 Announcement
d.tone(XC + 16, Y0 + 46, WC - 32, 60, OK, r=6, op="10", sw=1.0)
d.t(XC + 30, Y0 + 70, "L2 Announcements (policy1 · eth0)", 12, OK, KR, "start", 600)
d.t(XC + 30, Y0 + 92, "ARP 응답으로 172.18.255.200 수신", 12, MUTED, KR, "start")

# 2-2. eBPF 데이터패스
d.tone(XC + 16, Y0 + 122, WC - 32, 66, ACC, r=6, op="12", sw=1.2)
d.t(XC + 30, Y0 + 146, "Cilium eBPF 데이터패스", 12, ACC, KR, "start", 600)
d.t(XC + 30, Y0 + 170, "eBPF 가로채기 → TPROXY → Envoy", 12, INK, KR, "start")

# 2-3. Envoy DaemonSet
d.tone(XC + 16, Y0 + 204, WC - 32, 72, INFO, r=6, op="12", sw=1.2)
d.t(XC + 30, Y0 + 228, "Envoy DaemonSet (cilium-envoy)", 12, INFO, MONO, "start", 600)
d.t(XC + 30, Y0 + 250, "CiliumEnvoyConfig (CEC) 규칙 적용", 12, INK, KR, "start")
d.t(XC + 30, Y0 + 268, "경로 파싱: /details vs /", 12, MUTED, KR, "start")

# 3. 오른쪽: 백엔드 서비스 및 Pod
XR, WR = 680, 216
d.box(XR, Y0, WR, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XR + WR / 2, Y0 + 26, "백엔드 Pod", 13, INK, KR, "middle", 600)
d.t(XR + WR / 2, Y0 + 46, "Bookinfo 애플리케이션", 12, MUTED, KR)

# details Pod
d.tone(XR + 14, Y0 + 74, WR - 28, 86, OK, r=6, op="10", sw=1.0)
d.t(XR + WR / 2, Y0 + 98, "details:9080", 12, OK, MONO, "middle", 600)
d.t(XR + WR / 2, Y0 + 120, "경로 /details 매칭", 12, INK, KR)
d.t(XR + WR / 2, Y0 + 142, "책 상세 정보 JSON", 12, MUTED, KR)

# productpage Pod
d.tone(XR + 14, Y0 + 176, WR - 28, 86, OK, r=6, op="10", sw=1.0)
d.t(XR + WR / 2, Y0 + 200, "productpage:9080", 12, OK, MONO, "middle", 600)
d.t(XR + WR / 2, Y0 + 222, "경로 / 매칭 (기본)", 12, INK, KR)
d.t(XR + WR / 2, Y0 + 244, "메인 웹 화면 200 OK", 12, MUTED, KR)

# 화살표 연결
# 1 -> 2: 클라이언트 -> eth0 L2
d.arrow([(XL + WL, Y0 + 76), (XC + 16, Y0 + 76)], INFO, "info", 1.5)
# 2 내부: eth0 -> eBPF
d.arrow([(XC + WC / 2, Y0 + 106), (XC + WC / 2, Y0 + 122)], OK, "ok", 1.4)
# 2 내부: eBPF -> Envoy
d.arrow([(XC + WC / 2, Y0 + 188), (XC + WC / 2, Y0 + 204)], ACC, "acc", 1.5)
# 2 -> 3: Envoy -> details (직교 꺾임선)
X_MID = 658
d.arrow([(XC + WC - 16, Y0 + 230), (X_MID, Y0 + 230), (X_MID, Y0 + 117), (XR + 14, Y0 + 117)], OK, "ok", 1.4)
# 2 -> 3: Envoy -> productpage (직교 꺾임선)
d.arrow([(XC + WC - 16, Y0 + 250), (X_MID, Y0 + 250), (X_MID, Y0 + 219), (XR + 14, Y0 + 219)], OK, "ok", 1.4)

d.save("07-01.chapter-overview.svg")
