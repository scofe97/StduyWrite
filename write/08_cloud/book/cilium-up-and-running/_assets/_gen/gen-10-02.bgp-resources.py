# 타입 스펙: type-tree — 배정된 계층 타입이 스펙 목록에 없어 부모-자식 참조 관계를 표현하는 type-tree 로 대체했다. ClusterConfig → PeerConfig → Advertisement 참조 구조.
# 사실 출처: 추출본 cil10.txt 줄 745-793(CiliumBGPClusterConfig), 803-884(CiliumBGPPeerConfig), 895-977(CiliumBGPAdvertisement) / docs.cilium.io v1.20 network/bgp-control-plane/bgp-control-plane-configuration/
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 460
d = D(W, H, "CILIUM UP AND RUNNING · 10-02 §3", "BGP 제어 평면 세 리소스의 참조 계층",
      "클러스터 설정이 피어 설정을 참조하고, 피어 설정이 광고 대역을 라벨로 연결한다",
      "BGP Control Plane v2 리소스 모델 (cilium.io/v2)")

# Columns: 3 resources (BW=250, gaps=77)
BW, BH = 250, 270
Y0 = 100
XS = [24, 351, 678]

# 1. CiliumBGPClusterConfig
d.box(XS[0], Y0, BW, BH, PAPER2, ACC, 1.0, r=8)
d.chip(XS[0] + BW / 2, Y0 + 20, "CiliumBGPClusterConfig", ACC, 11, pad=6)
d.t(XS[0] + BW / 2, Y0 + 44, "frr", 13, INK, MONO, "middle", 600)

d.box(XS[0] + 12, Y0 + 60, BW - 24, 52, PAPER, RULE, 0.8, r=4)
d.t(XS[0] + 20, Y0 + 78, "nodeSelector", 11, SOFT, MONO, "start")
d.t(XS[0] + 20, Y0 + 96, "!control-plane", 11, INK, MONO, "start")

d.box(XS[0] + 12, Y0 + 120, BW - 24, 64, PAPER, RULE, 0.8, r=4)
d.t(XS[0] + 20, Y0 + 138, "bgpInstances", 11, SOFT, MONO, "start")
d.t(XS[0] + 20, Y0 + 154, "localASN: 64512", 11, INK, MONO, "start")
d.t(XS[0] + 20, Y0 + 170, "localPort: 179", 11, INK, MONO, "start")

d.tone(XS[0] + 12, Y0 + 192, BW - 24, 64, WARN, r=4, op="12", sw=1.1)
d.t(XS[0] + 20, Y0 + 210, "peers · peer-64512-frr", 11, WARN, MONO, "start", 600)
d.t(XS[0] + 20, Y0 + 226, "peerAddress: 172.18.0.6", 11, INK, MONO, "start")
d.t(XS[0] + 20, Y0 + 242, "peerConfigRef: peer-config", 11, WARN, MONO, "start")

# 2. CiliumBGPPeerConfig
d.box(XS[1], Y0, BW, BH, PAPER2, WARN, 1.0, r=8)
d.chip(XS[1] + BW / 2, Y0 + 20, "CiliumBGPPeerConfig", WARN, 11, pad=6)
d.t(XS[1] + BW / 2, Y0 + 44, "peer-config", 13, INK, MONO, "middle", 600)

d.box(XS[1] + 12, Y0 + 60, BW - 24, 52, PAPER, RULE, 0.8, r=4)
d.t(XS[1] + 20, Y0 + 78, "timers", 11, SOFT, MONO, "start")
d.t(XS[1] + 20, Y0 + 96, "keepalive 20s · hold 60s", 11, INK, MONO, "start")

d.box(XS[1] + 12, Y0 + 120, BW - 24, 52, PAPER, RULE, 0.8, r=4)
d.t(XS[1] + 20, Y0 + 138, "gracefulRestart", 11, SOFT, MONO, "start")
d.t(XS[1] + 20, Y0 + 154, "restart: 15s (RFC 8538)", 11, INK, MONO, "start")

d.tone(XS[1] + 12, Y0 + 180, BW - 24, 76, OK, r=4, op="12", sw=1.1)
d.t(XS[1] + 20, Y0 + 198, "families (ipv4 / unicast)", 11, OK, MONO, "start", 600)
d.t(XS[1] + 20, Y0 + 218, "advertisements.matchLabels", 11, SOFT, MONO, "start")
d.t(XS[1] + 20, Y0 + 236, "advertise: bgp", 11, OK, MONO, "start")

# 3. CiliumBGPAdvertisement
d.box(XS[2], Y0, BW, BH, PAPER2, OK, 1.0, r=8)
d.chip(XS[2] + BW / 2, Y0 + 20, "CiliumBGPAdvertisement", OK, 11, pad=6)
d.t(XS[2] + BW / 2, Y0 + 44, "bgp-advertisement", 13, INK, MONO, "middle", 600)

d.box(XS[2] + 12, Y0 + 60, BW - 24, 52, PAPER, RULE, 0.8, r=4)
d.t(XS[2] + 20, Y0 + 78, "advertisementType: Service", 11, INK, MONO, "start", 600)
d.t(XS[2] + 20, Y0 + 96, "addresses: [LoadBalancerIP]", 11, MUTED, MONO, "start")

d.box(XS[2] + 12, Y0 + 120, BW - 24, 64, PAPER, RULE, 0.8, r=4)
d.t(XS[2] + 20, Y0 + 138, "attributes (BGP 속성)", 11, SOFT, KR, "start")
d.t(XS[2] + 20, Y0 + 154, "localPreference: 200", 11, INK, MONO, "start")
d.t(XS[2] + 20, Y0 + 170, "communities: 64512:99", 11, INK, MONO, "start")

d.tone(XS[2] + 12, Y0 + 192, BW - 24, 64, OK, r=4, op="12", sw=1.1)
d.t(XS[2] + 20, Y0 + 210, "metadata.labels", 11, SOFT, MONO, "start")
d.t(XS[2] + 20, Y0 + 228, "advertise: bgp", 11, OK, MONO, "start", 600)
d.t(XS[2] + 20, Y0 + 244, "selector: announcement=bgp", 10, MUTED, MONO, "start")

# Connecting Arrows (Clean horizontal routing)
MID_X1 = (XS[0] + BW + XS[1]) / 2
d.arrow([(XS[0] + BW, Y0 + 234), (XS[1], Y0 + 234)], WARN, "warn", 1.4)
d.t(MID_X1, Y0 + 222, "peerRef", 11, WARN, MONO, "middle")

MID_X2 = (XS[1] + BW + XS[2]) / 2
d.arrow([(XS[1] + BW, Y0 + 224), (XS[2], Y0 + 224)], OK, "ok", 1.4)
d.t(MID_X2, Y0 + 212, "match", 11, OK, MONO, "middle")

d.legend(H - 44, [("노드/인스턴스", ACC), ("피어 설정 참조", WARN), ("광고/라벨 매칭", OK)])
d.save("10-02.bgp-resources.svg")
