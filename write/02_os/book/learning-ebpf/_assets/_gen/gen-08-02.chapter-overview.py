# 타입 스펙: type-architecture — 노드 한 대(커널 하나) 안의 Pod 네임스페이스 존과 호스트 네임스페이스 존, 그 아래 공유 맵 띠. focal 은 맵 띠 하나.
# 사실 출처: 추출본 ebpf8.txt 698~859행(libssl 의 SSL_read·SSL_write 에 uprobe·uretprobe), 867~897행(Pod 마다 네임스페이스와 veth), 970~1003행(소켓 층·XDP·TC 와 장치 넷),
#   1015~1021행(프로그램들은 맵과 패킷 메타데이터로 통신). 장치 이름과 훅: Cilium v1.20.2 bpf/bpf_sock.c(cgroup/connect4·sendmsg4·recvmsg4 — 소켓 층 프로그램), 문서 network/ebpf/intro(XDP prefilter, cilium_host·cilium_net·cilium_vxlan),
#   network/concepts/routing(호스트 쪽 lxcXXXXXX, Pod 안 eth0). 맵 이름: Cilium 문서 network/ebpf/maps 의 Map Name 열(IP cache · Policy · Service Load Balancer · Connection Tracking).
# Layout conventions: 존 둘 w=280·572 y=148 h=332, 노드 상자 w=240 h=48~88, 장치 상자 w=132 stride 136 y=272 h=88, 맵 띠 x=364 y=396 w=540 h=72. 연결선은 직각, 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 596
d = D(W, H, "LEARNING EBPF · 08-02",
      "노드 한 대 안에서 uprobe 와 Cilium 프로그램이 붙는 자리",
      "Pod 네임스페이스의 앱과 libssl 의 SSL_read·SSL_write 에 uprobe·uretprobe 가 붙는다. 호스트 네임스페이스에서는 Pod veth 의 lxc*, cilium_host, cilium_vxlan, 물리 장치에 TC 가, 물리 장치에 XDP 가, 소켓 층에 cgroup connect·sendmsg 프로그램이 붙고, 이 프로그램들은 IP cache·Policy·Service Load Balancer·Connection Tracking 맵과 패킷 메타데이터를 공유한다.",
      "프로그램은 훅마다 따로 돌고 맵으로 상태를 나눕니다")

# 노드 테두리와 존
d.box(24, 100, 912, 404, PAPER, RULE, 1.0, 8)
d.t(40, 124, "쿠버네티스 노드 한 대 · 커널 하나", 13, MUTED, KR, "start", 600)
d.box(44, 148, 280, 332, PAPER2, RULE, 0.9, 8)
d.t(60, 172, "Pod 네트워크 네임스페이스", 13, MUTED, KR, "start", 600)
d.box(348, 148, 572, 332, PAPER2, RULE, 0.9, 8)
d.t(364, 172, "호스트 네임스페이스", 13, MUTED, KR, "start", 600)

# 연결선 먼저 — 앱 → libssl, eth0 → lxc*, 장치 → 맵
d.arrow([(184, 248), (184, 268)], MUTED, "ar", 1.4)
d.arrow([(304, 420), (336, 420), (336, 316), (360, 316)], MUTED, "ar", 1.5)
for cx in (430, 566, 702, 838):
    d.arrow([(cx, 360), (cx, 392)], ACC, "acc", 1.3)

# Pod 존
d.box(64, 200, 240, 48, PAPER, RULE, 1.0, 6)
d.t(184, 230, "앱", 13, INK, KR, "middle", 600)
d.tone(64, 272, 240, 100, OK, 6, "12", 1.2)
d.t(184, 298, "libssl", 13, OK, MONO, "middle", 600)
d.t(184, 320, "SSL_read · SSL_write", 12, MUTED, MONO)
d.chip(140, 352, "uprobe", OK, 11)
d.chip(236, 352, "uretprobe", OK, 11)
d.box(64, 396, 240, 56, PAPER, RULE, 1.0, 6)
d.t(184, 420, "eth0", 13, INK, MONO, "middle", 600)
d.t(184, 440, "Pod 쪽 veth", 13, MUTED, KR)

# 호스트 존 — 소켓 층 띠
d.tone(364, 200, 540, 48, WARN, 6, "12", 1.2)
d.t(380, 230, "소켓 층 프로그램", 13, WARN, KR, "start", 600)
d.t(560, 230, "cgroup connect·sendmsg", 12, MUTED, MONO, "start")

# 장치 상자 넷 — x=364 + 136k
DEV = [("lxc*", "호스트 쪽 veth", False), ("cilium_host", "호스트", False),
       ("cilium_vxlan", "터널", False), ("물리 장치", "NIC", True)]
for k, (nm, role, xdp) in enumerate(DEV):
    x = 364 + 136 * k
    cx = x + 66
    d.tone(x, 272, 132, 88, INFO, 6, "12", 1.2)
    d.t(cx, 298, nm, 13, INK, KR if any("가" <= c <= "힣" for c in nm) else MONO, "middle", 600)
    d.t(cx, 318, role, 13 if not role.isascii() else 12, MUTED, MONO if role.isascii() else KR)
    if xdp:
        d.chip(cx - 24, 344, "XDP", WARN, 11)
        d.chip(cx + 24, 344, "TC", INFO, 11)
    else:
        d.chip(cx, 344, "TC", INFO, 11)

# 공유 맵 띠 — focal
d.tone(364, 396, 540, 72, ACC, 6, "1F", 1.4)
d.t(380, 420, "공유 맵 · 패킷 메타데이터", 13, ACC, KR, "start", 600)
x = 384
for lab, w in (("IP cache", 68), ("Policy", 56), ("Service Load Balancer", 160), ("Connection Tracking", 144)):
    d.chip(x + w / 2, 448, lab, MUTED, 11)
    x += w + 12

d.legend(H - 56, [("uprobe", OK), ("TC", INFO), ("XDP · 소켓 층", WARN), ("공유 맵", ACC)])
d.save("08-02.chapter-overview.svg")
