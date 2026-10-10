# 타입 스펙: type-data-flow — 노드 경로 광고가 라우터 RIB/FIB에 적재되어 외부 클라이언트 요청이 ECMP로 분산되는 흐름
# 사실 출처: 추출본 cil10.txt 줄 1005-1033(State/PfxRcd 1, NextHop 172.18.0.2/3), 1053-1088(ip route nhid 13, ECMP nexthop weight 1, wget 200) / docs.cilium.io v1.20 network/bgp-control-plane
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 460
d = D(W, H, "CILIUM UP AND RUNNING · 10-02 §4", "경로 광고와 라우터 ECMP 트래픽 흐름",
      "광고된 서비스 VIP 가 라우터 RIB 과 FIB 에 반영되어 두 워커 노드로 분산된다",
      "BGP 프리픽스 전파 · 커널 다중경로(ECMP) 전달")

BW, BH = 212, 260
Y0 = 104
XS = [24, 260, 496, 732]

# Step 1: BGP Route Advertisement
d.box(XS[0], Y0, BW, BH, PAPER2, ACC, 1.0, r=8)
d.chip(XS[0] + BW / 2, Y0 + 20, "1. BGP 광고 생성", ACC, 11, pad=6)
d.t(XS[0] + BW / 2, Y0 + 44, "cilium-agent", 12, INK, MONO, "middle", 600)

d.box(XS[0] + 12, Y0 + 60, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[0] + 20, Y0 + 78, "kind-worker (172.18.0.2)", 11, INK, MONO, "start")
d.t(XS[0] + 20, Y0 + 96, "NextHop: 172.18.0.2", 11, ACC, MONO, "start")

d.box(XS[0] + 12, Y0 + 124, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[0] + 20, Y0 + 142, "kind-worker2 (172.18.0.3)", 11, INK, MONO, "start")
d.t(XS[0] + 20, Y0 + 160, "NextHop: 172.18.0.3", 11, ACC, MONO, "start")

d.tone(XS[0] + 12, Y0 + 188, BW - 24, 54, ACC, r=4, op="12", sw=1.1)
d.t(XS[0] + BW / 2, Y0 + 208, "광고 프리픽스", 11, ACC, KR, "middle", 600)
d.t(XS[0] + BW / 2, Y0 + 226, "172.18.255.200/32", 11, INK, MONO, "middle")

# Step 2: Router RIB
d.box(XS[1], Y0, BW, BH, PAPER2, WARN, 1.0, r=8)
d.chip(XS[1] + BW / 2, Y0 + 20, "2. 라우터 RIB 수신", WARN, 11, pad=6)
d.t(XS[1] + BW / 2, Y0 + 44, "FRR bgpd (AS 64512)", 12, INK, MONO, "middle", 600)

d.box(XS[1] + 12, Y0 + 60, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[1] + 20, Y0 + 78, "iBGP 피어 세션", 11, SOFT, KR, "start")
d.t(XS[1] + 20, Y0 + 96, "State: Established", 11, OK, MONO, "start")

d.box(XS[1] + 12, Y0 + 124, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[1] + 20, Y0 + 142, "수신 프리픽스 (PfxRcd)", 11, SOFT, KR, "start")
d.t(XS[1] + 20, Y0 + 160, "피어당 1개 (총 2개)", 11, INK, KR, "start")

d.tone(XS[1] + 12, Y0 + 188, BW - 24, 54, WARN, r=4, op="12", sw=1.1)
d.t(XS[1] + BW / 2, Y0 + 208, "BGP 라우팅 테이블", 11, WARN, KR, "middle", 600)
d.t(XS[1] + BW / 2, Y0 + 226, "다중 경로 후보 등록", 11, INK, KR, "middle")

# Step 3: Kernel FIB (ECMP)
d.box(XS[2], Y0, BW, BH, PAPER2, OK, 1.0, r=8)
d.chip(XS[2] + BW / 2, Y0 + 20, "3. 커널 FIB 적재", OK, 11, pad=6)
d.t(XS[2] + BW / 2, Y0 + 44, "리눅스 커널 경로표", 12, INK, KR, "middle", 600)

d.box(XS[2] + 12, Y0 + 60, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[2] + 20, Y0 + 78, "대상 VIP (proto bgp)", 11, SOFT, KR, "start")
d.t(XS[2] + 20, Y0 + 96, "172.18.255.200", 11, OK, MONO, "start", 600)

d.tone(XS[2] + 12, Y0 + 124, BW - 24, 118, OK, r=4, op="12", sw=1.1)
d.t(XS[2] + 20, Y0 + 144, "ECMP 다중 넥스트홉", 11, OK, KR, "start", 600)
d.t(XS[2] + 20, Y0 + 164, "nexthop 172.18.0.2 wt 1", 11, INK, MONO, "start")
d.t(XS[2] + 20, Y0 + 182, "nexthop 172.18.0.3 wt 1", 11, INK, MONO, "start")
d.t(XS[2] + 20, Y0 + 202, "플로우 해시 분산", 11, MUTED, KR, "start")
d.t(XS[2] + 20, Y0 + 222, "동등 비용 경로(ECMP)", 11, MUTED, KR, "start")

# Step 4: Traffic Delivery
d.box(XS[3], Y0, BW, BH, PAPER2, INFO, 1.0, r=8)
d.chip(XS[3] + BW / 2, Y0 + 20, "4. 트래픽 전달", INFO, 11, pad=6)
d.t(XS[3] + BW / 2, Y0 + 44, "FRR 라우터 (frr 컨테이너)", 12, INK, KR, "middle", 600)

d.box(XS[3] + 12, Y0 + 60, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[3] + 20, Y0 + 78, "서비스 호출", 11, SOFT, KR, "start")
d.t(XS[3] + 20, Y0 + 96, "wget 172.18.255.200", 11, INK, MONO, "start")

d.box(XS[3] + 12, Y0 + 124, BW - 24, 56, PAPER, RULE, 0.8, r=4)
d.t(XS[3] + 20, Y0 + 142, "도착 노드 (해시 결과)", 11, SOFT, KR, "start")
d.t(XS[3] + 20, Y0 + 160, "kind-worker 또는 kind-worker2", 11, INK, KR, "start")

d.tone(XS[3] + 12, Y0 + 188, BW - 24, 54, OK, r=4, op="12", sw=1.1)
d.t(XS[3] + BW / 2, Y0 + 208, "응답 성공", 11, OK, KR, "middle", 600)
d.t(XS[3] + BW / 2, Y0 + 226, "HTTP 200 (It works!)", 11, INK, MONO, "middle")

# Connecting Arrows
d.arrow([(XS[0] + BW, Y0 + BH / 2), (XS[1], Y0 + BH / 2)], ACC, "acc", 1.4)
d.arrow([(XS[1] + BW, Y0 + BH / 2), (XS[2], Y0 + BH / 2)], WARN, "warn", 1.4)
d.arrow([(XS[2] + BW, Y0 + BH / 2), (XS[3], Y0 + BH / 2)], OK, "ok", 1.4)

d.legend(H - 44, [("BGP 광고", ACC), ("RIB 학습", WARN), ("커널 ECMP", OK), ("클라이언트", INFO)])
d.save("10-02.route-propagation.svg")
