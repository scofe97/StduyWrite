# 타입 스펙: type-architecture — eth0 XDP 훅과 BPF 프로그램 540, BPF 맵 165·166, trace_pipe 와 사용자 공간 bpftool 관리 구조
# 사실 출처: 《Learning eBPF》 Ch.3 9~10쪽(ID 540 · jited 148B), 13~14쪽(net attach · eth0), 15쪽(trace_pipe · Hello World 453),
#   16~17쪽(맵 165 hello.bss · 166 hello.rodata), 17~18쪽(net detach · rm /sys/fs/bpf/hello), bpftool-net.rst v7.7.0 L61-L84, 본문 §1~§3.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 03-02",
      "XDP 부착과 BPF 맵·로그 파이프 아키텍처",
      "eth0 XDP 훅에 붙은 프로그램 540 은 bss·rodata 맵을 읽고 갱신하며 trace_pipe 에 로그를 남기고, 사용자 공간은 bpftool 과 고정 파일로 이를 제어합니다.",
      "커널 내부 실행 경로와 사용자 공간의 프로그램·맵 제어 경로")

# 존
KZ = (16, 100, 672, 376)   # 커널 공간
UZ = (704, 100, 240, 376)  # 사용자 공간
for (x, y, w, h), name in ((KZ, "KERNEL"), (UZ, "USER SPACE")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 9, SOFT, MONO, "start")

def node(x, y, title, sub, c, w=152, h=64, mono_title=True, sec=None):
    d.tone(x, y, w, h, c, 6, "14", 1.2)
    if sec:
        d.t(x + 10, y + 16, sec, 9, SOFT, KR, "start", 600)
    d.t(x + w/2, y + 28, title, 14, c, MONO if mono_title else KR, "middle", 600)
    d.t(x + w/2, y + 48, sub, 12, MUTED, MONO if all(ord(ch) < 128 for ch in sub) else KR)

# 커널 공간 노드들
# 1. 패킷 입력 (왼쪽 중앙)
node(36, 248, "eth0", "XDP 훅", INFO, 120, 64, sec="§2")
# 2. XDP 프로그램 (중앙)
node(204, 248, "hello()", "ID 540 · JIT 148B", OK, 156, 64, sec="§1·§2")
# 3. 맵 두 개 및 trace_pipe (오른쪽 세로 배치)
node(484, 136, "hello.bss", "맵 165 · value 4B", WARN, 160, 64, sec="§3")
node(484, 248, "hello.rodata", "맵 166 · value 15B", WARN, 160, 64, sec="§3")
node(484, 360, "trace_pipe", "Hello World 453", ACC, 160, 64, sec="§2")

# 사용자 공간 노드들
node(724, 136, "bpftool net", "attach · detach", INFO, 200, 64, sec="§2")
node(724, 248, "bpftool map", "dump 165 · 166", WARN, 200, 64, sec="§3")
node(724, 360, "고정 파일", "rm /sys/fs/bpf/hello", ACC, 200, 64, mono_title=False, sec="§2")

# 커널 내부 화살표
# eth0 -> hello()
yc = 280
d.arrow([(158, yc), (198, yc)], INFO, "info", 1.5)
d.chip(180, yc - 18, "수신", MUTED, 11)

# hello() -> hello.bss
d.arrow([(360, 256), (420, 256), (420, 168), (478, 168)], WARN, "warn", 1.4)
d.chip(420, 200, "counter++", WARN, 11)

# hello() -> hello.rodata (칩 좌우로 선을 나누어 text-line 접촉 방지)
d.line(360, yc, 382, yc, WARN, 1.4)
d.arrow([(458, yc), (478, yc)], WARN, "warn", 1.4)
d.chip(420, yc, "문자열 읽기", WARN, 11)

# hello() -> trace_pipe
d.arrow([(360, 304), (420, 304), (420, 392), (478, 392)], ACC, "acc", 1.4)
d.chip(420, 346, "bpf_printk", ACC, 11)

# 사용자 공간 제어 화살표
# bpftool net -> eth0 (부착/분리)
d.arrow([(824, 132), (824, 108), (104, 108), (104, 242)], INFO, "info", 1.3, dash="4 4")

# bpftool map -> hello.bss & hello.rodata
d.arrow([(724, 280), (650, 280)], WARN, "warn", 1.3, dash="4 4")
d.arrow([(676, 280), (676, 168), (650, 168)], WARN, "warn", 1.3, dash="4 4")

# bpffs 고정 파일 -> hello() (참조 유지, 칩 좌우로 선을 나누어 text-line 접촉 방지)
d.path("M 724 392 L 676 392 L 676 444 L 536 444", ACC, 1.3, dash="4 4")
d.arrow([(408, 444), (282, 444), (282, 318)], ACC, "acc", 1.3, dash="4 4")
d.chip(472, 444, "참조 카운트 유지", ACC, 11)

# 사용자 공간 명령은 다루는 커널 대상과 같은 색이라 범례도 둘을 함께 적는다
d.legend(H - 56, [("네트워크 훅 · net 명령", INFO), ("BPF 프로그램", OK), ("BPF 맵 · map 명령", WARN), ("로깅·참조 관리", ACC)])
d.save("03-02.chapter-overview.svg")
