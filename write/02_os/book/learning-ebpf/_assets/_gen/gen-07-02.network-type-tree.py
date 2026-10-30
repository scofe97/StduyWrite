# 타입 스펙: type-tree — 뿌리 하나(네트워크 유형), 묶음 다섯(XDP · TC · 소켓 · 경로·분해 · cgroup), 묶음 아래 세로 목록(잎). 깊이 3. focal 은 SOCKET_FILTER 잎.
# 사실 출처: 커널 v7.2 include/linux/bpf_types.h L5~36(컨텍스트 xdp_md · __sk_buff · bpf_sock · bpf_sock_addr · bpf_sock_ops), include/uapi/linux/bpf.h L6577~6581(XDP_* 코드),
#   include/uapi/linux/pkt_cls.h L64~66(TC_ACT_*), tools/lib/bpf/libbpf.c L10101~10103(tcx/ingress·tc), kernel/bpf/syscall.c L4600~4617(SOCK_OPS 는 cgroup 에 붙는 유형),
#   L4677(SK_SKB 는 sockmap), L4683(FLOW_DISSECTOR 는 netns), 본문 §3 의 관리 도구(ip link · bpftool net · tc · ip route).
# Layout conventions: 묶음 열 stride 180·폭 172, 잎 높이 36·stride 44, 잎은 묶음 아래 세로 척추(잎 상자 왼쪽 바깥)에 엘보로 잇는다. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 556
d = D(W, H, "LEARNING EBPF · 07-02 §3", "네트워크 유형은 붙는 높이로 갈리고 높이마다 컨텍스트가 다르다",
      "XDP 는 xdp_md, TC·소켓 필터·경로·분해·cgroup SKB 는 __sk_buff, SOCK_OPS 는 bpf_sock_ops 를 받는다. 잎의 ip link · bpftool net · tc · ip route 는 관리 도구다.",
      "같은 패킷도 잡는 높이에 따라 받는 구조체가 다릅니다")

COLS = [
    ("XDP", "NIC 드라이버 직후", [("xdp_md", "컨텍스트", None), ("XDP_*", "반환 코드", None), ("ip link", "관리 도구", INFO), ("bpftool net", "관리 도구", INFO)]),
    ("TC", "ingress·egress", [("__sk_buff", "컨텍스트", None), ("TC_ACT_*", "반환 코드", None), ("tcx/ingress", "새 방식", None), ("tc", "관리 도구", INFO)]),
    ("소켓", "소켓·sockmap", [("SOCKET_FILTER", "소켓", ACC), ("SOCK_OPS", "cgroup", None), ("SK_SKB", "sockmap", None)]),
    ("경로·분해", "라우트·네임스페이스", [("LWT_*", "경량 터널", None), ("FLOW_DISSECTOR", "분해", None), ("ip route", "관리 도구", INFO)]),
    ("cgroup", "cgroup 단위", [("CGROUP_SOCK", "소켓 작업", None), ("CGROUP_SKB", "패킷", None), ("CGROUP_SOCK_ADDR", "주소", None)]),
]
X0, STRIDE, GW = 12, 180, 172
RX, RY, RW, RH = 340, 100, 240, 52
GY, BUS = 196, 176
LEAF_Y0, LEAF_W = 272, 156

# 연결선 먼저
cx = [X0 + i * STRIDE + GW // 2 for i in range(5)]
d.line(RX + RW // 2, RY + RH, RX + RW // 2, BUS, MUTED, 1.2)
d.line(cx[0], BUS, cx[-1], BUS, MUTED, 1.2)
for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i * STRIDE
    d.line(cx[i], BUS, cx[i], GY, MUTED, 1.2)
    sx = x + 4  # 척추는 잎 상자 왼쪽 바깥에 두어 잎 글자 사이로 지나지 않게 한다
    last = LEAF_Y0 + (len(leaves) - 1) * 44 + 18
    d.line(sx, GY + 52, sx, last, RULE, 1.2)
    for k in range(len(leaves)):
        ly = LEAF_Y0 + k * 44 + 18
        d.line(sx, ly, sx + 12, ly, RULE, 1.2)

d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0)
d.t(RX + RW // 2, RY + 24, "네트워크 유형", 15, INK, KR, "middle", 600)
d.t(RX + RW // 2, RY + 42, "높이로 가른 다섯 묶음", 12, MUTED, KR)
for i, (g, gs, leaves) in enumerate(COLS):
    x = X0 + i * STRIDE
    d.box(x, GY, GW, 52, PAPER2, RULE, 1.0)
    d.t(x + GW // 2, GY + 24, g, 14, INK, KR, "middle", 600)
    d.t(x + GW // 2, GY + 42, gs, 12, MUTED, KR)
    for k, (name, hint, c) in enumerate(leaves):
        lx, ly = x + 16, LEAF_Y0 + k * 44
        if c:
            d.tone(lx, ly, LEAF_W, 36, c, 5, "14", 1.3)
        else:
            d.box(lx, ly, LEAF_W, 36, PAPER2, RULE, 0.9, 5)
        d.t(lx + 8, ly + 23, name, 11, c or INK, MONO, "start", 600)
        d.t(lx + LEAF_W - 8, ly + 23, hint, 12, MUTED, KR, "end")

d.legend(H - 56, [("관리 도구", INFO), ("소켓의 수신 데이터를 거르는 유형", ACC)])
d.save("07-02.network-type-tree.svg")
