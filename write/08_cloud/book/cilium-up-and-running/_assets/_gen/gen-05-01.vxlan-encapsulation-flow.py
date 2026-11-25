# 타입 스펙: type-architecture — 송신 노드와 수신 노드를 존으로 묶고, cilium_host 경유 → ipcache tunnelendpoint 조회 → cilium_vxlan 캡슐화 → 수신 노드 역캡슐화 흐름을 번호 화살표로 보인다.
# 사실 출처: Cilium Up and Running 5장 ch05.txt 줄 265-270(cil_from_overlay·cil_to_overlay), 648-667(ip route via 10.244.2.63 dev cilium_host, cilium_vxlan), 698-710(172.18.0.3.51713 > 172.18.0.4.8472, 10.244.0.185 > 10.244.1.212, kind-worker ↔ kind-worker2), 895-897(ipcache tunnelendpoint·flags=hastunnel)
import sys
sys.path.insert(0, ".")
from dd import D, ACC, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 464
d = D(W, H, "CILIUM UP AND RUNNING · 05-01 §3",
      "VXLAN 캡슐화가 cilium_host 에서 터널로 넘어가는 경로",
      "경로표가 cilium_host 를 가리키면 Cilium 이 ipcache 로 상대 노드를 찾아 cilium_vxlan 으로 보냅니다",
      "경로표가 cilium_host 를 가리키면 Cilium 이 ipcache 로 상대 노드를 찾아 cilium_vxlan 으로 보냅니다")

# Zones
LX, LW, RX, RW = 20, 352, 548, 352
ZY, ZH = 104, 292
d.o.append(f'<rect x="{LX}" y="{ZY}" width="{LW}" height="{ZH}" rx="8" fill="#161B2204" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(LX + 16, ZY + 24, "kind-worker · 172.18.0.3", 13, INK, MONO, "start", 600)

d.o.append(f'<rect x="{RX}" y="{ZY}" width="{RW}" height="{ZH}" rx="8" fill="#161B2204" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, ZY + 24, "kind-worker2 · 172.18.0.4", 13, INK, MONO, "start", 600)

BX, BW = LX + 12, 328
# Left step 1: ip route
d.box(BX, 144, BW, 56, PAPER2, RULE, 0.9, r=6)
d.t(BX + 10, 166, "1. 출발 Pod → lxc* → ip route 조회", 13, INK, KR, "start", 600)
d.t(BX + 10, 188, "10.244.1.0/24 via 10.244.2.63 dev cilium_host", 11, MUTED, MONO, "start")

d.arrow([(BX + BW / 2, 200), (BX + BW / 2, 224)], MUTED, "ar", 1.4)

# Left step 2: cilium_host + ipcache (focal ACC)
d.tone(BX, 226, BW, 60, ACC, r=6, op="14", sw=1.4)
d.t(BX + 10, 250, "2. cilium_host 가로채기 · ipcache 조회", 13, ACC, KR, "start", 600)
d.t(BX + 10, 272, "tunnelendpoint=172.18.0.4 · flags=hastunnel", 11, MUTED, MONO, "start")

d.arrow([(BX + BW / 2, 286), (BX + BW / 2, 310)], ACC, "acc", 1.4)

# Left step 3: cilium_vxlan encapsulate
d.tone(BX, 312, BW, 64, INFO, r=6, op="12", sw=1.1)
d.t(BX + 10, 336, "3. cilium_vxlan · cil_to_overlay", 13, INFO, MONO, "start", 600)
d.t(BX + 10, 358, "UDP 8472 + VNI(신원) 캡슐화 후 송출", 12, MUTED, KR, "start")

# Right zone: step 4 and step 5
RBX, RBW = RX + 12, 328
d.tone(RBX, 144, RBW, 68, INFO, r=6, op="12", sw=1.1)
d.t(RBX + 10, 168, "4. cilium_vxlan · cil_from_overlay", 13, INFO, MONO, "start", 600)
d.t(RBX + 10, 192, "바깥 헤더 제거 · VNI 로 정책 판정", 12, MUTED, KR, "start")

d.arrow([(RBX + RBW / 2, 212), (RBX + RBW / 2, 252)], INFO, "info", 1.4)

d.box(RBX, 254, RBW, 60, PAPER2, RULE, 0.9, r=6)
d.t(RBX + 10, 278, "5. 목적지 lxc* → 도착 Pod", 13, INK, KR, "start", 600)
d.t(RBX + 10, 300, "10.244.0.185 → 10.244.1.212", 12, MUTED, MONO, "start")

# Orthogonal connector across underlay
d.arrow([(BX + BW, 344), (460, 344), (460, 178), (RBX - 2, 178)], INFO, "info", 1.5)
d.box(378, 232, 164, 44, PAPER, RULE, 0.8, r=4)
d.t(460, 250, "UDP 8472", 12, INFO, MONO, "middle", 600)
d.t(460, 268, "172.18.0.3 → 172.18.0.4", 11, MUTED, MONO, "middle")

d.legend(416, [("핵심 · ipcache 조회", ACC), ("터널 장치 처리", INFO)])
d.save("05-01.vxlan-encapsulation-flow.svg")
