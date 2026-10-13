# 타입 스펙: type-architecture — 커널 안 두 갈래(perf 버퍼로 밀기 · prog array 로 tail call)와 사용자 공간 두 출구.
# 사실 출처: 추출본 ebpf2.txt 460~1048행 · 예제 저장소 chapter2/hello-buffer.py · chapter2/hello-tail.py (HEAD 91ded4a)
#   위 줄 kprobe 대상은 b.get_syscall_fnname("execve") — x86_64 에서 __x64_sys_execve (BCC src/python/bcc/__init__.py 줄 841~843 주석)
#   아래 줄 BPF_PROG_ARRAY(syscall, 500), attach_raw_tracepoint(tp="sys_enter"), 대상 hello_exec·hello_timer·ignore_opcode, b.trace_print()
# Layout conventions: 노드 폭 164·높이 64, 열 간격 28, 존 둘(커널·사용자), 위 줄 y=132, 아래 줄 y=276. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, INK, PAPER, PAPER2, RULE, SOFT, INFO, KR, MONO

W, H = 960, 560
d = D(W, H, "LEARNING EBPF · 02-02",
      "커널 안 두 갈래, 사용자 공간 두 출구",
      "execve kprobe 의 hello() 는 헬퍼로 모은 data_t 를 perf 버퍼 output 에 밀고, sys_enter raw tracepoint 의 hello() 는 syscall prog array 로 tail call 한다.",
      "위 줄은 값을 밀어 주고, 아래 줄은 프로그램을 갈아 끼웁니다")

# 존
KZ = (16, 100, 720, 372)   # 커널 공간
UZ = (752, 100, 192, 372)  # 사용자 공간
for (x, y, w, h), name in ((KZ, "KERNEL"), (UZ, "USER SPACE")):
    d.box(x, y, w, h, PAPER2, RULE, 0.9, 8)
    d.t(x + 12, y + 20, name, 9, SOFT, MONO, "start")

NW, NH = 164, 64
COLS = [36, 228, 420]            # 열 간격 28
R1, R2 = 132, 244                # 줄 y

def node(x, y, title, sub, c, w=NW, h=NH, mono_title=True):
    d.tone(x, y, w, h, c, 6, "12", 1.2)
    d.t(x + w/2, y + 28, title, 14, c, MONO if mono_title else KR, "middle", 600)
    d.t(x + w/2, y + 48, sub, 12, MUTED, MONO if all(ord(ch) < 128 for ch in sub) else KR)

# 위 줄 — 값을 밀어 주는 갈래
node(COLS[0], R1, "kprobe", "__x64_sys_execve", INFO)
node(COLS[1], R1, "hello()", "헬퍼 4개 → data_t", OK)
node(COLS[2], R1, "output", "BPF_PERF_OUTPUT", INFO)
# 아래 줄 — 프로그램을 갈아 끼우는 갈래
node(COLS[0], R2, "sys_enter", "raw tracepoint", INFO)
node(COLS[1], R2, "hello()", "opcode = ctx->args[1]", OK)
node(COLS[2], R2, "syscall", "PROG_ARRAY · 500칸", INFO)
# tail call 대상 — 세 줄
TX, TY, TW, TH = COLS[2], 348, NW, 100
d.tone(TX, TY, TW, TH, WARN, 6, "12", 1.2)
for i, nm in enumerate(("hello_exec", "hello_timer", "ignore_opcode")):
    d.t(TX + TW/2, TY + 28 + 28*i, nm, 13, WARN, MONO, "middle", 600)

# 사용자 공간 노드
UX, UW = 772, 160
node(UX, R1, "perf_buffer_poll", "print_event 호출", OK, UW, NH)
TPY = TY + TH//2 - NH//2
node(UX, TPY, "trace_print", "trace_pipe 읽기", OK, UW, NH)

# 화살표 — 위 줄
yc1 = R1 + NH//2
d.arrow([(COLS[0] + NW + 2, yc1), (COLS[1] - 6, yc1)], MUTED, "ar", 1.5)
d.arrow([(COLS[1] + NW + 2, yc1), (COLS[2] - 6, yc1)], OK, "ok", 1.5)
d.arrow([(COLS[2] + NW + 2, yc1), (UX - 6, yc1)], INFO, "info", 1.5)
d.chip(668, yc1 - 18, "perf_submit", MUTED, 12)
# 화살표 — 아래 줄
yc2 = R2 + NH//2
d.arrow([(COLS[0] + NW + 2, yc2), (COLS[1] - 6, yc2)], MUTED, "ar", 1.5)
d.arrow([(COLS[1] + NW + 2, yc2), (COLS[2] - 6, yc2)], OK, "ok", 1.5)
# tail call — 아래로
cx = COLS[2] + NW//2
d.arrow([(cx, R2 + NH + 2), (cx, TY - 6)], ACC, "acc", 1.8)
d.chip(cx + 64, R2 + NH + 20, "tail call", ACC, 12)
# 대상 → trace_print
ytp = TPY + NH//2
d.arrow([(TX + TW + 2, ytp), (UX - 6, ytp)], WARN, "warn", 1.5)
d.chip(656, ytp - 18, "bpf_trace_printk", MUTED, 12)

d.legend(H - 56, [("헬퍼·프로그램", OK), ("맵·진입점", INFO), ("tail call 대상", WARN), ("tail call", ACC)])
d.save("02-02.chapter-overview.svg")
