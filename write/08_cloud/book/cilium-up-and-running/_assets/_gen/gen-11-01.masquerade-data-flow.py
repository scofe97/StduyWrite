# 타입 스펙: type-data-flow — netshoot-client 의 송신 패킷이 목적지 IP 대역에 따라 예외 대역 우회(원본 IP 유지)와 노드 IP SNAT 마스커레이딩으로 갈라지는 데이터 흐름.
# 사실 출처: Cilium Up and Running 11장 cil11.txt 줄 97-157(netshoot-client 10.244.1.252, kind-worker 172.18.0.2, kind-echo-server 172.18.0.7:8080), 222-268(ip-masq-agent nonMasqueradeCIDRs 172.16.0.0/12), 295-300(예외 대역 시 10.244.1.252 도착 및 응답 유실)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 420
d = D(W, H, "CILIUM UP AND RUNNING · 11-01 §2", "목적지 대역에 따른 마스커레이딩 판정 흐름",
      "ip-masq-agent 예외 대역 여부에 따라 SNAT 적용과 원본 IP 유지가 갈린다",
      "ip-masq-agent 예외 대역 여부에 따라 SNAT 적용과 원본 IP 유지가 갈린다")

Y0, HN = 104, 252
XL, WL = 24, 250
XM, WM = 304, 286
XR, WR = 618, 278

# 왼쪽: 송신 노드 및 클라이언트 Pod
d.box(XL, Y0, WL, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XL + 16, Y0 + 26, "kind-worker", 12, INFO, MONO, "start", 600)
d.t(XL + WL - 16, Y0 + 26, "172.18.0.2", 11, MUTED, MONO, "end")

d.tone(XL + 16, Y0 + 44, WL - 32, 70, INFO, r=6, op="10", sw=1.0)
d.t(XL + 28, Y0 + 70, "netshoot-client", 12, INK, MONO, "start", 600)
d.t(XL + 28, Y0 + 94, "IP 10.244.1.252", 11, INFO, MONO, "start")

d.tone(XL + 16, Y0 + 126, WL - 32, 110, ACC, r=6, op="12", sw=1.2)
d.t(XL + 28, Y0 + 150, "Cilium eBPF", 12, ACC, KR, "start", 600)
d.t(XL + 28, Y0 + 174, "bpf.masquerade", 11, INK, MONO, "start", 600)
d.t(XL + 28, Y0 + 196, "bpf ipmasq list", 11, MUTED, MONO, "start")
d.t(XL + 28, Y0 + 218, "172.16.0.0/12", 11, WARN, MONO, "start")

# 중앙: 두 경로 분기
y_top = Y0 + 44
y_bot = Y0 + 146

# 상단 경로: 예외 대역 (nonMasqueradeCIDRs 매칭)
d.box(XM, y_top, WM, 88, PAPER2, RULE, sw=0.9, r=6)
d.t(XM + 14, y_top + 22, "예외 대역 목적지", 12, WARN, KR, "start", 600)
d.t(XM + WM - 14, y_top + 22, "172.18.0.7", 11, MUTED, MONO, "end")
d.t(XM + 14, y_top + 45, "SNAT 생략 · 원본 유지", 12, INK, KR, "start")
d.t(XM + 14, y_top + 68, "src 10.244.1.252", 11, BAD, MONO, "start", 600)

# 하단 경로: 일반 외부 (마스커레이딩 적용)
d.box(XM, y_bot, WM, 88, PAPER2, RULE, sw=0.9, r=6)
d.t(XM + 14, y_bot + 22, "일반 외부 목적지", 12, OK, KR, "start", 600)
d.t(XM + WM - 14, y_bot + 22, "외부 IP", 11, MUTED, MONO, "end")
d.t(XM + 14, y_bot + 45, "노드 IP 로 SNAT 적용", 12, INK, KR, "start")
d.t(XM + 14, y_bot + 68, "src 172.18.0.2", 11, OK, MONO, "start", 600)

# 오른쪽: 수신지 kind-echo-server
d.box(XR, Y0, WR, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XR + 16, Y0 + 26, "kind-echo-server", 12, INK, MONO, "start", 600)
d.t(XR + WR - 16, Y0 + 26, "172.18.0.7:8080", 11, MUTED, MONO, "end")

d.tone(XR + 16, y_top, WR - 32, 88, BAD, r=6, op="10", sw=1.0)
d.t(XR + 28, y_top + 24, "수신: 10.244.1.252", 11, BAD, MONO, "start", 600)
d.t(XR + 28, y_top + 46, "귀환 경로 없음", 12, BAD, KR, "start")
d.t(XR + 28, y_top + 68, "응답 드롭 · 연결 실패", 11, MUTED, KR, "start")

d.tone(XR + 16, y_bot, WR - 32, 88, OK, r=6, op="10", sw=1.0)
d.t(XR + 28, y_bot + 24, "수신: 172.18.0.2:43490", 11, OK, MONO, "start", 600)
d.t(XR + 28, y_bot + 46, "노드로 응답 반환", 12, OK, KR, "start")
d.t(XR + 28, y_bot + 68, "역 SNAT 거쳐 정상 수신", 11, MUTED, KR, "start")

# 직교 연결 화살표 (축 정렬 준수)
x_exit = XL + WL
x_mid = (x_exit + XM) / 2

d.arrow([(x_exit, Y0 + 174), (x_mid, Y0 + 174), (x_mid, y_top + 44), (XM, y_top + 44)], WARN, "warn", 1.4)
d.arrow([(x_exit, Y0 + 196), (x_mid, Y0 + 196), (x_mid, y_bot + 44), (XM, y_bot + 44)], OK, "ok", 1.4)
d.arrow([(XM + WM, y_top + 44), (XR, y_top + 44)], BAD, "bad", 1.4)
d.arrow([(XM + WM, y_bot + 44), (XR, y_bot + 44)], OK, "ok", 1.4)

d.legend(H - 44, [("클라이언트 Pod", INFO), ("Cilium eBPF", ACC), ("노드 IP 변환", OK), ("예외 대역", WARN), ("귀환 불가 드롭", BAD)])
d.save("11-01.masquerade-data-flow.svg")
