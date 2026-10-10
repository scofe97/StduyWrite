# 타입 스펙: type-data-flow — Pod 의 DNS 질의가 kube-dns 서비스 IP 로 향할 때 LRP 가 동일 노드 node-local-dns 로 가로채고 캐시 미스 시 중앙 CoreDNS 로 전달되는 데이터 흐름.
# 사실 출처: Cilium Up and Running 8장 cil8.txt 줄 528-532(kube-dns-upstream 및 CoreDNS 라벨), 줄 550(노드 로컬 IP 169.254.20.10·10.96.0.10), 줄 563-567(노드별 node-local-dns Pod IP), 줄 575-596(LRP nodelocaldns YAML), 줄 603-607(ID 3·4 LocalRedirect), 줄 644-668(로컬 메트릭 1→14 증가 및 원격 메트릭 1 유지)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 440
d = D(W, H, "CILIUM UP AND RUNNING · 08-01 §4", "NodeLocal DNSCache 와 LRP 연동 질의 흐름",
      "Pod 의 DNS 질의가 노드 로컬 캐시로 가로채지고 미스 시 업스트림으로 전달되는 구조",
      "kube-dns 주소로의 DNS 질의를 eBPF LRP 로 로컬 캐시에 가로채고 미스 시 업스트림 전달")

# 구역 상자: 동일 노드 (kind-worker)
d.box(16, 96, 570, 316, PAPER2, RULE, 0.8, r=6)
d.t(36, 120, "동일 노드 내부 완결 구역 (kind-worker)", 12, OK, KR, "start", 600)
d.t(566, 120, "외부 네트워크 경유 없음", 11, MUTED, KR, "end")

# 클라이언트 Pod
d.box(36, 146, 160, 80, PAPER, RULE, 0.9)
d.t(116, 172, "netshoot-client", 12, INK, MONO, "middle", 600)
d.t(116, 192, "DNS 질의 발송", 11, MUTED, KR)
d.t(116, 210, "UDP/TCP 53", 11, MUTED, MONO)

# kube-dns 서비스 VIP
d.box(232, 146, 150, 80, PAPER, SOFT, 1.0)
d.t(307, 172, "kube-dns VIP", 12, INK, MONO, "middle", 600)
d.t(307, 192, "10.96.0.10:53", 11, INK, MONO)
d.t(307, 210, "서비스 대상 주소", 11, MUTED, KR)

d.arrow([(196, 186), (232, 186)], MUTED, "ar", 1.4)

# LRP 가로채기 (focal)
d.tone(418, 146, 150, 80, ACC, r=4, op="14", sw=1.4)
d.t(493, 172, "LRP nodelocaldns", 12, ACC, MONO, "middle", 600)
d.t(493, 192, "LocalRedirect ID 3/4", 11, INK, MONO)
d.t(493, 210, "동일 노드 DNAT 변환", 11, ACC, KR)

d.arrow([(382, 186), (418, 186)], ACC, "acc", 1.5)

# 노드 로컬 DNS 캐시 Pod (하단)
d.tone(232, 276, 336, 116, OK, r=4, op="12", sw=1.2)
d.t(400, 302, "node-local-dns (10.0.0.172)", 12, OK, MONO, "middle", 600)
d.t(400, 322, "로컬 캐시 응답 (메트릭 1 → 14 증가)", 11, INK, KR)
d.t(400, 342, "프로메테우스 포트 9253 메트릭 수집", 11, MUTED, KR)
d.t(400, 362, "캐시에 있는 이름은 노드 안에서 응답", 11, OK, KR)

# LRP -> 로컬 캐시 (직교)
d.arrow([(493, 226), (493, 276)], OK, "ok", 1.5)

# 로컬 캐시 -> 클라이언트 응답 (직교)
d.arrow([(232, 334), (116, 334), (116, 226)], OK, "ok", 1.5, dash="4 4")
d.t(174, 324, "캐시 응답 반환", 11, OK, KR, "middle")

# 원격 클러스터 구역
d.box(606, 96, 298, 316, PAPER2, RULE, 0.8, r=6)
d.t(626, 120, "원격 클러스터 영역", 12, WARN, KR, "start", 600)
d.t(884, 120, "캐시 미스 시만 전달", 11, MUTED, KR, "end")

# 업스트림 서비스
d.box(626, 146, 258, 64, PAPER, SOFT, 1.0)
d.t(755, 170, "kube-dns-upstream", 12, INK, MONO, "middle", 600)
d.t(755, 192, "캐시 미스 시 포트 53 포워딩", 11, MUTED, KR)

# 로컬 캐시 -> 업스트림 (직교)
d.arrow([(568, 300), (596, 300), (596, 178), (626, 178)], WARN, "warn", 1.4)

# 중앙 CoreDNS
d.box(626, 236, 258, 64, PAPER, RULE, 0.9)
d.t(755, 260, "중앙 CoreDNS Pod", 12, INK, KR, "middle", 600)
d.t(755, 282, "k8s-app: kube-dns", 11, MUTED, MONO)

d.arrow([(755, 210), (755, 236)], MUTED, "ar", 1.4)

# 다른 노드의 캐시 (질의 미수신)
d.box(626, 326, 258, 66, PAPER, RULE, 0.7)
d.t(755, 350, "node-local-dns (10.0.2.20)", 11, MUTED, MONO, "middle")
d.t(755, 370, "요청 미수신 (메트릭 1 유지)", 11, MUTED, KR)

d.save("08-01.node-local-dns-lrp.svg")
