# 타입 스펙: type-data-flow — Service 주소로 가는 요청이 iptables 순차 대조와 eBPF 맵 조회에서 주소 변환되는 경로 비교.
# 사실 출처: 본문 §1 (L61-73: KUBE-SERVICES·KUBE-SVC 체인 순차 대조, connect() 소켓 훅, 서비스 주소를 키로 BPF 맵 조회,
#   백엔드 수와 거의 무관한 조회 비용) · 정답 2 (L198: netfilter 규칙 체인 생략) · 원서 1장 From Early CNIs to Modern Datapaths
#   (p.2: iptables 로 packet filtering·NAT·load balancing) · Networking with Cilium as a CNI (p.6-7).
# 예시 IP·KUBE-SEP·확률 분기·tc 는 본문·원서에 없어 넣지 않는다 (2026-11-01 검증).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "CILIUM UP AND RUNNING · 01-01 §1", "Service IP 패킷 경로: iptables vs eBPF",
      "서비스 엔드포인트 증가 시 iptables 의 선형 탐색 병목과 eBPF 의 BPF 맵 조회 처리 차이",
      "서비스 수에 비례하는 체인 대조와 거의 일정한 BPF 맵 조회")

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
d.t(880, Y_TOP + LANE_H + GAP_LANE + 28, "백엔드 수와 거의 무관한 조회 비용", 11, MUTED, KR, "end")

# 상단 노드들 (iptables 흐름)
# 단계: 패킷 진입 -> KUBE-SERVICES -> KUBE-SVC -> 주소 변환(NAT)
x_steps = [48, 220, 440, 660]
box_w = 140
box_h = 76
y_box1 = Y_TOP + 54

top_nodes = [
    ("패킷 진입", "DST = ClusterIP", "Service 주소로 요청", SOFT),
    ("KUBE-SERVICES", "규칙 체인 순차 탐색", "서비스 N개 선형 대조", WARN),
    ("KUBE-SVC", "엔드포인트 규칙 대조", "위에서부터 한 줄씩", WARN),
    ("주소 변환 (NAT)", "DST → Pod IP", "백엔드 Pod 로 전달", WARN),
]

for i, (title, sub1, sub2, col) in enumerate(top_nodes):
    x = x_steps[i]
    d.box(x, y_box1, box_w, box_h, PAPER, RULE, sw=0.9, r=6)
    d.t(x + box_w/2, y_box1 + 22, title, 12, col, KR, "middle", 600)
    font1 = KR if any('가' <= ch <= '힣' for ch in sub1) else MONO
    d.t(x + box_w/2, y_box1 + 42, sub1, 11, INK, font1, "middle")
    d.t(x + box_w/2, y_box1 + 62, sub2, 11, MUTED, KR, "middle")
    if i < len(top_nodes) - 1:
        next_x = x_steps[i+1]
        d.line(x + box_w, y_box1 + box_h/2, next_x, y_box1 + box_h/2, WARN, sw=1.2)
        d.arrow([(x + box_w, y_box1 + box_h/2), (next_x - 2, y_box1 + box_h/2)], WARN, "warn", sw=1.2)

# 하단 노드들 (eBPF 흐름)
# 단계: 패킷 진입 -> connect() 소켓 훅 -> BPF 맵 조회 -> 백엔드 Pod
y_box2 = Y_TOP + LANE_H + GAP_LANE + 54
bottom_nodes = [
    ("패킷 진입", "DST = ClusterIP", "Service 주소로 요청", SOFT),
    ("소켓 훅", "대개 connect() 시점", "netfilter 체인 생략", ACC),
    ("BPF 맵 조회", "Key: 서비스 주소", "백엔드 선택", OK),
    ("백엔드 Pod", "DST → Pod IP", "변환된 주소로 전달", OK),
]

for i, (title, sub1, sub2, col) in enumerate(bottom_nodes):
    x = x_steps[i]
    d.box(x, y_box2, box_w, box_h, PAPER, RULE, sw=0.9, r=6)
    d.t(x + box_w/2, y_box2 + 22, title, 12, col, KR, "middle", 600)
    font2 = KR if any('가' <= ch <= '힣' for ch in sub1) else MONO
    d.t(x + box_w/2, y_box2 + 42, sub1, 11, INK, font2, "middle")
    d.t(x + box_w/2, y_box2 + 62, sub2, 11, MUTED, KR, "middle")
    if i < len(bottom_nodes) - 1:
        next_x = x_steps[i+1]
        d.line(x + box_w, y_box2 + box_h/2, next_x, y_box2 + box_h/2, OK, sw=1.2)
        d.arrow([(x + box_w, y_box2 + box_h/2), (next_x - 2, y_box2 + box_h/2)], OK, "ok", sw=1.2)

# 범례
d.legend(474, [
    ("패킷 진입", SOFT),
    ("iptables 규칙 체인", WARN),
    ("eBPF 소켓 훅", ACC),
    ("BPF 맵 조회·전달", OK),
])

d.save("01-01.iptables-vs-ebpf.svg")
