# 타입 스펙: type-layers — 터널 패킷의 헤더 겹. 바깥에서 안쪽 순으로 5개 층(4–6), 층 높이 64, 폭 800. focal 은 VNI 에 신원을 싣는 VXLAN 층 하나.
# 사실 출처: Cilium Up and Running 5장 cil5.txt 줄 670-710(VXLAN 패킷 형식·tcpdump -r vxlan_traffic.pcap). 헤더 크기 20·8·8·14 는 RFC 791·768·7348·IEEE 802.3 표준 값(합 50 은 docs.cilium.io routing 의 "50 bytes")
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 464
LX, LW, LH, Y0 = 88, 800, 64, 108
d = D(W, H, "CILIUM UP AND RUNNING · 05-01 §3", "VXLAN 터널 패킷의 헤더 겹",
      "20 + 8 + 8 + 14 = 50바이트가 Pod 패킷 하나에 더 붙는다", "20 + 8 + 8 + 14 = 50바이트가 Pod 패킷 하나에 더 붙는다")

layers = [
    ("20B", "바깥 IP", "172.18.0.3 > 172.18.0.4", False),
    ("8B", "UDP", "51713 > 8472", False),
    ("8B", "VXLAN", "flags I · VNI = 출발 Pod 신원", True),
    ("14B", "안쪽 이더넷", "원본 프레임", False),
    ("원본", "안쪽 IP · TCP", "10.244.0.185 > 10.244.1.212", False),
]
for i, (tag, name, sub, focal) in enumerate(layers):
    y = Y0 + i * LH
    if focal:
        d.tone(LX, y, LW, LH, ACC, r=0, op="14", sw=1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2 if i % 2 == 0 else PAPER, RULE, 0.8, r=0)
    cy = y + LH / 2
    d.t(LX + 16, cy + 4, tag, 12, ACC if focal else SOFT, KR if any('가' <= c <= '힣' for c in tag) else MONO, "start")
    d.t(LX + 88, cy + 6, name, 15, ACC if focal else INK, KR, "start", 600)
    sfam = KR if any("가" <= c <= "힣" for c in sub) else MONO
    d.t(LX + LW - 16, cy + 5, sub, 12, MUTED, sfam, "end")

# 왼쪽 여백: 바깥 → 안쪽 방향
d.t(44, Y0 + 24, "바깥", 12, MUTED, KR)
d.arrow([(44, Y0 + 40), (44, Y0 + 5 * LH - 44)], MUTED, "ar", 1.4)
d.t(44, Y0 + 5 * LH - 20, "안쪽", 12, MUTED, KR)
d.save("05-01.vxlan-packet-layers.svg")
