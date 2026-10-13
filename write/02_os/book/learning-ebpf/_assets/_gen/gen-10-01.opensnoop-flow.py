# 타입 스펙: type-data-flow — 한 번의 openat 호출 값이 사용자 공간 프로세스에서 입구 프로그램, 해시 맵, 출구 프로그램, perf_event_array, 화면으로 단계마다 바뀌어 가는 흐름.
# 사실 출처: bpftrace v0.27.0 tools/opensnoop.bt L122~126(fd=ret, errno 0)·L153, 추출본 ebpf10.txt 94~112행(입구 `@filename[tid] = args->filename`, 출구 `/@filename[tid]/` 와 printf), 132~136행(출력 `297360 node 23 0 /proc/307224/cmdline`),
#   156~176행(bpftool: 프로그램 494~497, 해시 맵 254 key 8B value 8B, perf_event_array 255 name printf). 값 23 은 fd, 0 은 errno.
# Layout conventions: 상단 사용자 공간 띠 y=88~200, 하단 커널 띠 y=232~380, 상자 w=176·h=100 stride 248(x=24·272·520·768), 화살표 간격 72. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 464
d = D(W, H, "LEARNING EBPF · 10-01 §1",
      "입구 프로그램이 맵에 넣은 파일 이름을 출구 프로그램이 꺼낸다",
      "openat 한 번이 입구 tracepoint 에서 인자를 맵에 적고, 출구 tracepoint 가 반환값과 맵의 이름을 합쳐 한 줄을 출력한다.",
      "값이 바뀌는 자리는 맵 254 와 perf_event_array 255")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def band(y, h, name):
    d.box(12, y, 936, h, PAPER2, RULE, 0.9, 8)
    d.t(24, y + 18, name, 9, SOFT, MONO, "start")


band(88, 112, "USER SPACE")
band(232, 148, "KERNEL")


def card(x, y, w, h, c, lines, focal=False):
    d.tone(x, y, w, h, c, 6, "14" if focal else "12", 1.6 if focal else 1.2)
    ys = [y + 26 + 20 * i for i in range(len(lines))]
    for k, (txt, size, fill, wt) in enumerate(lines):
        d.t(x + w / 2, ys[k], txt, size, fill, fam(txt), "middle", wt)


# 사용자 공간 — 호출하는 프로세스와 화면
card(24, 112, 320, 76, MUTED, [("node · PID 297360", 13, INK, 600), ('openat("/proc/307224/cmdline")', 12, MUTED, 400)])
card(640, 112, 304, 76, MUTED, [("297360 node 23 0", 13, INK, 600), ("/proc/307224/cmdline", 12, MUTED, 400)])

# 커널 — 네 상자
Y = 264
BW = 176
card(24, Y, BW, 100, OK, [("sys_enter_openat", 14, INK, 600), ("입구 프로그램", 12, MUTED, 400), ("args.filename", 12, MUTED, 400)])
card(272, Y, BW, 100, ACC, [("해시 맵 254", 14, INK, 600), ("[tid 297360] =", 12, MUTED, 400), ("filename 포인터 (8B)", 12, MUTED, 400)], True)
card(520, Y, BW, 100, OK, [("sys_exit_openat", 14, INK, 600), ("/@filename[tid]/", 12, MUTED, 400), ("ret = 23", 12, MUTED, 400), ("str() 로 이름 읽기", 12, MUTED, 400)])
card(768, Y, BW, 100, INFO, [("perf_event_array", 13, INK, 600), ("255 · name printf", 12, MUTED, 400), ("FD 23 · ERR 0", 12, MUTED, 400)])

# 프로세스 → 입구 프로그램
d.arrow([(112, 190), (112, Y - 2)], MUTED, "ar", 1.5)
d.chip(112 + 16 + 44, 216, "tracepoint", MUTED, 11)
# 입구 → 맵(쓰기) · 맵 → 출구(읽기) · 출구 → perf 배열(출력)
mid = Y + 50
d.arrow([(24 + BW + 2, mid), (272 - 6, mid)], OK, "ok", 1.6)
d.chip(24 + BW + 36, mid - 20, "쓰기", OK, 12)
d.arrow([(272 + BW + 2, mid), (520 - 6, mid)], INFO, "info", 1.6)
d.chip(272 + BW + 36, mid - 20, "읽기", INFO, 12)
d.arrow([(520 + BW + 2, mid), (768 - 6, mid)], MUTED, "ar", 1.6)
d.chip(520 + BW + 36, mid - 20, "출력", MUTED, 12)
# perf 배열 → 화면
d.arrow([(856, Y - 2), (856, 190)], MUTED, "ar", 1.5)
d.chip(856 - 16 - 24, 216, "읽기", MUTED, 12)

d.legend(H - 56, [("프로그램", OK), ("맵 254", ACC), ("출력 배열", INFO), ("프로세스·화면", MUTED)])
d.save("10-01.opensnoop-flow.svg")
