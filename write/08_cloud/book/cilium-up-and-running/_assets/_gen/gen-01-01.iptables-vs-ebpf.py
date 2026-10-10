# 타입 스펙: type-data-flow — Service IP 요청 패킷의 iptables 순차 탐색과 eBPF O(1) 맵 조회 비교.
# 사실 출처: Cilium Up and Running 1장 From Early CNIs to Modern Datapaths · Networking with Cilium as a CNI.
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §1", "Service IP 패킷 경로: iptables vs eBPF",
      "서비스 엔드포인트 증가 시 iptables 의 선형 탐색 병목과 eBPF 의 BPF 맵 조회 처리 차이",
      "규칙 수가 늘어도 eBPF 는 BPF 맵 조회로 지연을 일정하게 유지합니다")

# 두 경로 레인 박스
Y_TOP = 108
LANE_H = 156
GAP_LANE = 24

# 상단 레인: iptables
d.box(24, Y_TOP, 872, LANE_H, PAPER2, RULE, sw=0.9, r=8)
d.box(36, Y_TOP + 12, 190, 24, PAPER, WARN, sw=1.0, r=4)
d.t(131, Y_TOP + 28, "iptables 경로 (kube-proxy)", 11, WARN, KR, "middle", 600)
d.t(880, Y_TOP + 28, "규칙 증가 시 O(N) 순차 탐색 지연", 11, MUTED, KR, "end")

# 하단 레인: eBPF
d.box(24, Y_TOP + LANE_H + GAP_LANE, 872, LANE_H, PAPER2, RULE, sw=0.9, r=8)
d.box(36, Y_TOP + LANE_H + GAP_LANE + 12, 190, 24, PAPER, OK, sw=1.0, r=4)
d.t(131, Y_TOP + LANE_H + GAP_LANE + 28, "eBPF 데이터패스 (Cilium)", 11, OK, KR, "middle", 600)
d.t(880, Y_TOP + LANE_H + GAP_LANE + 28, "규모 무관 BPF 맵 기반 조회", 11, MUTED, KR, "end")

# 상단 노드들 (iptables 흐름)
# 단계: 패킷 도착 -> KUBE-SERVICES -> KUBE-SVC -> KUBE-SEP -> 목적지 Pod
x_steps = [48, 220, 440, 660]
box_w = 140
box_h = 76
y_box1 = Y_TOP + 54

top_nodes = [
    ("패킷 진입", "DST 10.96.0.10:80", "ClusterIP 요청", SOFT),
    ("KUBE-SERVICES", "규칙 체인 순차 탐색", "N개 서비스 선형 대조", WARN),
    ("KUBE-SVC", "엔드포인트 확률 분기", "1/N 확률 매치 모듈", WARN),
    ("KUBE-SEP (DNAT)", "10.244.1.5:8080", "목적지 Pod 변환 완료", OK),
]

for i, (title, sub1, sub2, col) in enumerate(top_nodes):
    x = x_steps[i]
    d.box(x, y_box1, box_w, box_h, PAPER, RULE, sw=0.9, r=6)
    d.t(x + box_w/2, y_box1 + 22, title, 12, col, KR, "middle", 600)
    d.t(x + box_w/2, y_box1 + 42, sub1, 11, INK, MONO, "middle")
    d.t(x + box_w/2, y_box1 + 62, sub2, 11, MUTED, KR, "middle")
    if i < len(top_nodes) - 1:
        next_x = x_steps[i+1]
        d.line(x + box_w, y_box1 + box_h/2, next_x, y_box1 + box_h/2, WARN, sw=1.2)
        d.arrow([(x + box_w, y_box1 + box_h/2), (next_x - 2, y_box1 + box_h/2)], WARN, "warn", sw=1.2)

# 하단 노드들 (eBPF 흐름)
# 단계: 패킷 도착 -> tc/XDP 후크 -> BPF_MAP_LOOKUP -> 목적지 Pod 직결
y_box2 = Y_TOP + LANE_H + GAP_LANE + 54
bottom_nodes = [
    ("패킷 진입", "DST 10.96.0.10:80", "ClusterIP 요청", SOFT),
    ("소켓 훅 / tc", "커널 레벨 변환·가로챔", "netfilter 체인 생략", ACC),
    ("BPF 맵 조회", "Key: 10.96.0.10:80", "서비스·백엔드 맵 대조", OK),
    ("백엔드 포워딩", "10.244.1.5:8080", "목적지 Pod 직접 송신", OK),
]

for i, (title, sub1, sub2, col) in enumerate(bottom_nodes):
    x = x_steps[i]
    d.box(x, y_box2, box_w, box_h, PAPER, RULE, sw=0.9, r=6)
    d.t(x + box_w/2, y_box2 + 22, title, 12, col, KR, "middle", 600)
    d.t(x + box_w/2, y_box2 + 42, sub1, 11, INK, MONO, "middle")
    d.t(x + box_w/2, y_box2 + 62, sub2, 11, MUTED, KR, "middle")
    if i < len(bottom_nodes) - 1:
        next_x = x_steps[i+1]
        d.line(x + box_w, y_box2 + box_h/2, next_x, y_box2 + box_h/2, OK, sw=1.2)
        d.arrow([(x + box_w, y_box2 + box_h/2), (next_x - 2, y_box2 + box_h/2)], OK, "ok", sw=1.2)

# 범례
d.legend(474, [
    ("패킷 진입", SOFT),
    ("선형 체인 탐색", WARN),
    ("커널 eBPF 후크", ACC),
    ("BPF 맵 조회·포워딩", OK),
])

d.save("01-01.iptables-vs-ebpf.svg")
