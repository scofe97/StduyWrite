# 타입 스펙: type-layers — 아래부터 NIC(오프로드)·드라이버(네이티브)·일반 경로(generic)·네트워크 스택 네 층. 층마다 왼쪽에 bpftool attach type, 오른쪽에 판정 자리. 코랄은 이 편의 예제가 붙은 일반 경로 한 층.
# 사실 출처: linux v7.2 tools/bpf/bpftool/Documentation/bpftool-net.rst 66~69행(xdp 는 네이티브를 시도하고 NIC 드라이버가 지원하지 않으면 generic 으로 폴백, xdpgeneric 은 패킷이 skb 로 수신 경로에 들어온 뒤,
#   xdpdrv 는 드라이버 수신 경로의 가장 이른 지점, xdpoffload 는 NIC 에서 직접), net/core/dev.c 10220~10229행(플래그가 없으면 ndo_bpf 가 있을 때 DRV 아니면 SKB)·drivers/net/loopback.c 154~159행(loopback_ops 에 ndo_bpf 없음),
#   drivers/net/veth.c 1725행(.ndo_bpf = veth_xdp), 예제 저장소 chapter8/Makefile 14행(bpftool net attach xdp ... dev lo), lizrice/lb-from-scratch Makefile 16행(xdpgeneric ... dev eth0).
# Layout conventions: 층 x=88 폭 840, 높이 64, stride 72(y=112 시작), 태그는 x=100, 이름은 x=252, 칩은 x=468 이후, 서브라벨은 우측 정렬 x=916. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 1000, 500
d = D(W, H, "LEARNING EBPF · 08-01 §4", "XDP 는 NIC · 드라이버 · 일반 경로 세 자리에서 돌 수 있다",
      "아래 NIC 의 오프로드 XDP 는 xdpoffload 로 호스트 CPU 를 쓰지 않고, 드라이버의 네이티브 XDP 는 xdpdrv 로 sk_buff 가 만들어지기 전에 돌며, 일반 경로의 xdpgeneric 은 sk_buff 가 만들어진 뒤에 돈다. lo 에 xdp 로 붙인 hello 는 폴백으로, 컨테이너 eth0 에 xdpgeneric 으로 붙인 로드밸런서는 지정으로 일반 경로에 있다.",
      "어디서 판정하느냐가 attach type 을 정합니다")

LX, LW, LH, ST, TOP = 88, 840, 64, 72, 120
ROWS = [
    ("—", "네트워크 스택", "프로토콜 처리", INFO, False),
    ("xdpgeneric", "일반 경로", "sk_buff 생성 뒤", ACC, True),
    ("xdpdrv", "드라이버", "sk_buff 생성 전", INFO, False),
    ("xdpoffload", "NIC", "호스트 CPU 0", OK, False),
]
d.t(LX + 12, TOP - 8, "attach type", 11, SOFT, MONO, "start", 600)
d.t(LX + LW - 12, TOP - 8, "판정 자리", 11, SOFT, KR, "end", 600)
for i, (tag, nm, sub, c, focal) in enumerate(ROWS):
    y = TOP + i * ST
    if focal:
        d.tone(LX, y, LW, LH, ACC, 6, "1F", 1.4)
    else:
        d.box(LX, y, LW, LH, PAPER2, RULE, 0.9, 6)
    d.t(LX + 12, y + 38, tag, 12, c if tag != "—" else SOFT, MONO, "start", 600)
    d.t(LX + 164, y + 40, nm, 15, c, KR, "start", 600)
    d.t(LX + LW - 12, y + 38, sub, 12, MUTED, KR, "end")

# 예제 칩 (일반 경로 층)
fy = TOP + 1 * ST + 32
d.chip(LX + 400, fy, "lo · hello · 폴백", ACC, 11)
d.chip(LX + 612, fy, "eth0 · LB · 지정", ACC, 11)

# 방향 표시 (왼쪽 바깥)
d.arrow([(48, TOP + 3 * ST + LH), (48, TOP + 16)], SOFT, "soft", 1.4)
d.t(48, TOP - 8, "패킷 ↑", 11, SOFT, KR, "middle")

d.legend(H - 56, [("예제가 붙은 자리", ACC), ("XDP 층", INFO), ("호스트 CPU 0", OK)])
d.save("08-01.xdp-attach-modes.svg")
