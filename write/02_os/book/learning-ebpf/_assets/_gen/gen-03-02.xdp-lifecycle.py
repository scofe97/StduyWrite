# 타입 스펙: type-state — 적재·고정 → 부착 → 적재만 → 해제 네 상태와 상태를 바꾸는 명령 셋
# 사실 출처: 추출본 ebpf3.txt 687~763행(net attach · net list · ip link) · 912~963행(detach · rm /sys/fs/bpf/hello),
#   bpftool-net.rst v7.7.0 61~81행(attach · detach), 본문 §2.
# Layout conventions(type-state): 상태 4 · 상태 상자 400×64 · stride 100 · 위→아래 흐름. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 03-02 §2",
      "분리해도 고정 파일이 있으면 프로그램은 남는다",
      "부착을 떼면 장치에서는 내려가지만 /sys/fs/bpf/hello 가 참조를 쥐고 있어 커널에는 남고, 파일을 지워야 해제된다.",
      "프로그램 540 의 네 상태")

BX, BW, BH, STRIDE, Y0 = 280, 400, 64, 100, 112
STATES = [
    ("적재 · 고정", "ID 540 · /sys/fs/bpf/hello", INFO, True),
    ("부착", "eth0(2) driver id 540", OK, True),
    ("적재만", "prog show name hello 에 남음", ACC, False),
    ("해제", "prog show 출력 없음", MUTED, False),
]
MOVES = [
    "bpftool net attach xdp id 540 dev eth0",
    "bpftool net detach xdp dev eth0",
    "rm /sys/fs/bpf/hello",
]

for i, (name, sub, c, mono_sub) in enumerate(STATES):
    y = Y0 + i * STRIDE
    if c == MUTED:
        d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    else:
        d.tone(BX, y, BW, BH, c, 8, "14", 1.4 if c == ACC else 1.2)
    d.t(BX + BW / 2, y + 28, name, 14, INK if c == MUTED else c, KR, "middle", 600)
    d.t(BX + BW / 2, y + 48, sub, 12, MUTED, MONO if mono_sub else KR)

for i, mv in enumerate(MOVES):
    ya = Y0 + i * STRIDE + BH
    yb = Y0 + (i + 1) * STRIDE
    cx = BX + BW / 2
    d.arrow([(cx, ya + 2), (cx, yb - 8)], MUTED, "ar", 1.5)
    d.t(cx + 20, (ya + yb) / 2 + 4, mv, 12, INK, MONO, "start")

d.legend(H - 56, [("적재 · 고정", INFO), ("실행 중", OK), ("남아 있음", ACC), ("해제", MUTED)])
d.save("03-02.xdp-lifecycle.svg")
