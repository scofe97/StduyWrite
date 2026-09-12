# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

W = 1000
SX = 500
TOP = 164
STRIDE = 156
STAGE_W = 300
STAGE_H = 64
SIDE_W = 300
SIDE_H = 110

stages = [
    (
        "1",
        "연결",
        "필수",
        INFO,
        ["socket · file descriptor", "TCP state · listen/accept queue", "ephemeral port · DNS resolver"],
        ["DNS · SYN · accept · app 응답으로", "연결 실패를 나눠 설명합니다"],
    ),
    (
        "2",
        "Linux 경로",
        "필수",
        INFO,
        ["interface · routing · ARP", "network namespace · veth · bridge", "netfilter · NAT · conntrack · MTU"],
        ["출발 namespace부터 목적지까지", "route · hook · 주소 변환을 잇습니다"],
    ),
    (
        "3",
        "관측",
        "필수",
        INFO,
        ["ss · tcpdump · Wireshark", "SYN · RST · 재전송 · TLS", "resolv.conf · ndots", "NXDOMAIN · CoreDNS"],
        ["패킷 캡처와 DNS 응답으로", "실패한 층을 구분합니다"],
    ),
    (
        "4",
        "Kubernetes",
        "필수",
        INFO,
        ["Pod CIDR · CNI", "overlay · native routing · BGP", "Service · CoreDNS · Gateway API"],
        ["Pod · Service · 외부 진입 경로를", "Linux 패킷 경로와 연결합니다"],
    ),
    (
        "5",
        "데이터패스와 정책",
        "추천",
        OK,
        ["eBPF map · verifier · hook", "Cilium · kube-proxy 대체", "NetworkPolicy · Hubble"],
        ["정책 선언이 집행되는", "hook과 데이터패스를 설명합니다"],
    ),
    (
        "6",
        "운영",
        "추천",
        OK,
        ["dual-stack · topology", "Windows HNS · HCS", "service mesh · mTLS · Zero Trust"],
        ["환경별 구현 차이와", "정책 · 관측 · 신뢰 경계를 판단합니다"],
    ),
]

H = TOP + STRIDE * len(stages) + 92
d = D(
    W,
    H,
    "WRITE · NETWORK ROADMAP",
    "네트워크 학습 로드맵",
    "연결에서 Linux 경로와 관측을 지나 Kubernetes 데이터패스와 운영으로 올라가는 여섯 단계입니다.",
    "왼쪽은 핵심 키워드, 가운데는 단계, 오른쪽은 완료 기준입니다",
)

d.box(SX - 116, 96, 232, 44, PAPER2, RULE, 1.0)
d.t(SX, 123, "여섯 단계를 순서대로 봅니다", 14, INK, KR, "middle", 600)
d.line(SX, 140, SX, TOP + STRIDE * (len(stages) - 1) + STAGE_H, RULE, 1.4)

for index, (number, title, priority, color, keywords, completion) in enumerate(stages):
    y = TOP + index * STRIDE
    mid = y + STAGE_H / 2
    left_y = mid - SIDE_H / 2
    right_y = left_y

    d.line(330, mid, SX - STAGE_W / 2, mid, RULE, 1.0)
    d.line(SX + STAGE_W / 2, mid, 670, mid, RULE, 1.0)

    d.box(30, left_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(46, left_y + 20, "핵심 키워드", 13, SOFT, KR, "start", 600)
    for line_index, keyword in enumerate(keywords):
        d.t(46, left_y + 42 + line_index * 18, keyword, 13, MUTED, KR, "start")

    if index == 3:
        d.tone(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, ACC, 6, "14", 1.4)
    else:
        d.box(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, PAPER, color, 1.2)
    d.t(SX - 128, y + 25, number, 12, color, MONO, "start", 600)
    d.t(SX + 6, y + 26, title, 15, ACC if index == 3 else INK, KR, "middle", 600)
    d.t(SX + 6, y + 49, priority, 13, color, KR)

    d.box(670, right_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(686, right_y + 20, "완료 기준", 13, SOFT, KR, "start", 600)
    for line_index, line in enumerate(completion):
        d.t(686, right_y + 48 + line_index * 20, line, 13, MUTED, KR, "start")

d.legend(H - 52, [("필수", INFO), ("추천", OK), ("Kubernetes 경계", ACC)])
d.save("network-roadmap.svg")
