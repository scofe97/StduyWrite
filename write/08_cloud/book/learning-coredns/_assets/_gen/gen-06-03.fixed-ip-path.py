# 06-03 §3 — DNS 서비스의 IP 는 클러스터를 만들 때 정해져 kubelet 을 거쳐 모든 파드의 resolv.conf 로 간다.
# 본문 근거: 이 노트 §3(원서 요지 — 클러스터 생성 시점의 고정값, 각 kubelet 에 전달, kubelet 이 파드 resolv.conf 를 만들 때 쓴다).
#            10.7.240.10 은 원서 Example 6-17 의 예제 값. kubelet 쪽 이름 clusterDNS 는 KubeletConfiguration 필드.
#            Service 이름 kube-dns 와 clusterIP 의 불변은 이 노트 §3 각주 serviceapi.
# 타입 스펙: type-data-flow — 같은 값 하나가 단계마다 다른 이름으로 실려 가는 흐름이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 408
d = D(W, H, "LEARNING COREDNS · 06-03 §3",
      "IP 하나가 모든 파드의 resolv.conf 까지 간다",
      "DNS 서비스의 IP 는 자동 할당이 아니라 클러스터를 만들 때 정한 값이다. kubelet 이 그 값을 받아 "
      "자기가 띄우는 파드마다 resolv.conf 의 nameserver 로 쓰므로, Service 의 IP 와 이름은 바뀌면 안 된다.",
      "주황 상자가 이름과 IP 를 바꿀 수 없는 자리입니다")

BW, GAP, X0, Y = 156, 15, 20, 116
steps = [
    ("클러스터 생성", [("DNS IP 를 정한다", KR), ("10.7.240.10", MONO)]),
    ("kubelet", [("clusterDNS", MONO), ("10.7.240.10", MONO)]),
    ("파드 resolv.conf", [("nameserver", MONO), ("10.7.240.10", MONO)]),
    ("Service", [("kube-dns", MONO), ("10.7.240.10", MONO)]),
    ("CoreDNS 파드", [("엔드포인트로", KR), ("질의를 받는다", KR)]),
]
for i, (title, lines) in enumerate(steps):
    x = X0 + i * (BW + GAP)
    focal = (i == 3)
    if focal:
        d.tone(x, Y, BW, 110, ACC, 8, "12", 1.4)
    else:
        d.box(x, Y, BW, 110, PAPER2, RULE, 1.0, 8)
    d.t(x + 14, Y + 30, title, 14, ACC if focal else INK, KR, "start", 600)
    for j, (txt, fam) in enumerate(lines):
        d.t(x + 14, Y + 60 + j * 24, txt, 12, INK if fam == MONO else MUTED, fam, "start")
    if i < 4:
        d.path(f"M {x + BW + 2} {Y + 55} L {x + BW + GAP - 3} {Y + 55}", MUTED, 1.3, m="ar")

x4 = X0 + 3 * (BW + GAP)
d.chip(x4 + BW / 2, 254, "이름 불변", ACC, 12)
d.chip(x4 + BW / 2, 282, "clusterIP 불변", ACC, 12)

d.t(20, 324, "같은 IP 가 kubelet 마다 전달된다 · ClusterFirst 파드는 이 값으로 DNS 를 찾는다", 13, MUTED, KR, "start")
d.t(20, 346, "10.7.240.10 은 원서 예제 값 · 클러스터마다 다르다", 12, SOFT, KR, "start")

d.legend(362, [("바꿀 수 없는 자리", ACC)])
d.save("06-03.fixed-ip-path.svg")
