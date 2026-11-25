# 타입 스펙: type-architecture — BGP 에서 PodCIDR 광고와 Service VIP 광고의 경로 구조, 클라이언트 대상 안정성, IPv4 주소 소모 차이.
# 값 근거: 본문 §4 및 ch16.txt 줄 701-727(Pod IP 변동·DNS 부담·native routing PodCIDR·서비스 IP 안정·데이터패스 자동 분산·IPv4 주소 공간 절약), docs.cilium.io v1.20 bgp-control-plane-configuration(PodCIDR, CiliumPodIPPool, Service /32·/128, LoadBalancerIP·ClusterIP·ExternalIP)
import sys

sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 568
d = D(
    W,
    H,
    "CILIUM UP AND RUNNING · 16-02 §4",
    "Pod 대역 광고와 서비스 IP 광고 구조 비교",
    "PodCIDR 광고는 바뀌는 Pod IP 대역을 외부에 노출하고, Service 광고는 고정된 /32 또는 /128 VIP 만 알린 뒤 노드 eBPF 데이터패스가 Pod 로 분산합니다.",
    lead="위쪽은 Pod 대역을 직접 광고하는 경로, 아래쪽은 고정 VIP 뒤에서 노드가 분산하는 경로입니다.",
)

# Zone 1: PodCIDR advertisement
Z1Y, Z1H = 100, 172
d.box(24, Z1Y, 912, Z1H, "rgba(245,245,243,0.02)", "rgba(245,245,243,0.16)", 0.9, 8)
d.t(40, Z1Y + 24, "PodCIDR 광고 · 바뀌는 Pod IP 직접 노출", 13, WARN, KR, "start", 600)

# Zone 2: Service VIP advertisement
Z2Y, Z2H = 296, 172
d.box(24, Z2Y, 912, Z2H, "rgba(245,245,243,0.02)", "rgba(245,245,243,0.16)", 0.9, 8)
d.t(40, Z2Y + 24, "Service 광고 · 고정 VIP 와 데이터패스 분산", 13, OK, KR, "start", 600)

# 화살표: 실선 = 패킷 전달, 점선 = 경로 광고(에이전트 BGP 스피커 -> 피어)
def row(y, c_pkt, c_node, send_lbl, adv_lbl, mono_adv):
    d.arrow([(196, y + 40), (324, y + 40)], c_pkt, "warn" if c_pkt == WARN else "ok", 1.3)
    d.t(260, y + 28, send_lbl, 13, c_pkt, KR, "middle", 600)
    d.arrow([(480, y + 30), (596, y + 30)], c_pkt, "warn" if c_pkt == WARN else "ok", 1.3)
    d.t(538, y + 18, "패킷 전달", 13, c_pkt, KR, "middle", 600)
    d.arrow([(596, y + 72), (480, y + 72)], MUTED, "ar", 1.3, "4 3")
    d.t(538, y + 60, adv_lbl, 12 if mono_adv else 13, MUTED, MONO if mono_adv else KR, "middle", 600)
    d.arrow([(764, y + 48), (796, y + 48)], c_node, "ar" if c_node == MUTED else "acc", 1.3)


Y1 = 156
Y2 = 352
row(Y1, WARN, MUTED, "Pod IP 로 전송", "PodCIDR 광고", False)
row(Y2, OK, ACC, "단일 VIP 로 전송", "/32 · /128 광고", True)

# Row 1 Boxes
d.box(44, Y1, 152, 96, PAPER2, RULE, 0.9, 6)
d.t(120, Y1 + 32, "외부 클라이언트", 14, INK, KR, "middle", 600)
d.t(120, Y1 + 56, "DNS 갱신 잦음", 13, WARN, KR, "middle")
d.t(120, Y1 + 78, "분산 직접 부담", 13, MUTED, KR, "middle")

d.tone(328, Y1, 148, 96, WARN, r=6, op="12", sw=1.1)
d.t(402, Y1 + 32, "상류 BGP 피어", 14, WARN, KR, "middle", 600)
d.t(402, Y1 + 56, "큰 Pod 대역 학습", 13, INK, KR, "middle")
d.t(402, Y1 + 78, "IPv4 소모 큼", 13, WARN, KR, "middle")

d.box(600, Y1, 160, 96, PAPER2, RULE, 0.9, 6)
d.t(680, Y1 + 32, "노드 에이전트", 14, INK, KR, "middle", 600)
d.t(680, Y1 + 56, "BGP 스피커가 광고", 13, MUTED, KR, "middle")
d.t(680, Y1 + 78, "native routing", 12, MUTED, MONO, "middle")

d.box(800, Y1, 116, 96, PAPER2, RULE, 0.9, 6)
d.t(858, Y1 + 32, "개별 Pod", 14, INK, KR, "middle", 600)
d.t(858, Y1 + 56, "수명 짧고 변동", 13, WARN, KR, "middle")
d.t(858, Y1 + 78, "경로 잦은 변경", 13, MUTED, KR, "middle")

# Row 2 Boxes
d.tone(44, Y2, 152, 96, OK, r=6, op="12", sw=1.1)
d.t(120, Y2 + 32, "외부 클라이언트", 14, OK, KR, "middle", 600)
d.t(120, Y2 + 56, "고정 VIP 송신", 13, INK, KR, "middle")
d.t(120, Y2 + 78, "DNS 갱신 감소", 13, OK, KR, "middle")

d.tone(328, Y2, 148, 96, OK, r=6, op="12", sw=1.1)
d.t(402, Y2 + 32, "상류 BGP 피어", 14, OK, KR, "middle", 600)
d.t(402, Y2 + 56, "LoadBalancerIP", 12, INK, MONO, "middle")
d.t(402, Y2 + 78, "IPv4 공간 절약", 13, OK, KR, "middle")

d.tone(600, Y2, 160, 96, ACC, r=6, op="16", sw=1.4)
d.t(680, Y2 + 32, "노드 에이전트", 14, ACC, KR, "middle", 700)
d.t(680, Y2 + 56, "BGP 스피커가 광고", 13, INK, KR, "middle")
d.t(680, Y2 + 78, "eBPF 로 Pod 분산", 13, MUTED, KR, "middle")

d.box(800, Y2, 116, 96, PAPER2, RULE, 0.9, 6)
d.t(858, Y2 + 32, "Pod A · Pod B", 14, INK, KR, "middle", 600)
d.t(858, Y2 + 56, "VIP 는 그대로", 13, OK, KR, "middle")
d.t(858, Y2 + 78, "추상화 보존", 13, MUTED, KR, "middle")

# 선 모양 범례
d.arrow([(44, 492), (92, 492)], MUTED, "ar", 1.3)
d.t(100, 497, "패킷 전달", 13, MUTED, KR, "start")
d.arrow([(200, 492), (248, 492)], MUTED, "ar", 1.3, "4 3")
d.t(256, 497, "경로 광고 (에이전트 BGP 스피커가 피어에 알림)", 13, MUTED, KR, "start")

d.legend(
    H - 44,
    [
        ("노드 자동 분산 (핵심)", ACC),
        ("VIP 고정 · 주소 절약", OK),
        ("주소 변동 · 대역 부담", WARN),
    ],
)
d.save("16-02.pod-vs-service-advertisement.svg")
print("ok 16-02 bgp adv")
