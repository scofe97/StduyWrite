# 타입 스펙: type-architecture — 사용자 공간(hello.py·hello-map.py)과 커널(kprobe → hello() → 두 출력 통로)을 경계 둘로 나눈 지도.
# 사실 출처: 《Learning eBPF》 Chapter 2 (2쪽 Figure 2-1 · 4쪽 Figure 2-2 — 적재 화살표가 hello() 로 들어감), 예제 저장소 chapter2/hello.py · hello-map.py, 본문 1~4절,
#   커널 v7.2 arch/x86/include/asm/syscall_wrapper.h 15~17행(`__x64_sys_*`), include/uapi/linux/bpf.h 2021~2032행(trace_pipe).
# Layout conventions: 밴드 둘(사용자 공간·커널), 박스 높이 92, 열 x 는 48·316·548·720. focal 은 hello().
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 560
d = D(W, H, "LEARNING EBPF · 02-01", "두 예제가 같은 execve kprobe 에 프로그램을 올리고 결과를 다른 길로 받는다",
      "사용자 공간의 hello.py 와 hello-map.py 가 각자 hello() 를 컴파일해 적재하고 execve 의 kprobe 에 붙인다. execve 가 불릴 때마다 hello() 가 돌고, 결과는 hello.py 에서는 trace_pipe 로, hello-map.py 에서는 counter_table 로 사용자 공간에 돌아온다.",
      "execve 호출마다 도는 hello() 와 예제별 두 출력 통로")

def band(y, h, label):
    d.o.append(f'<rect x="24" y="{y}" width="872" height="{h}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')
    d.t(40, y + 24, label, 12, MUTED, KR, "start", 600)

band(100, 156, "사용자 공간")
band(292, 196, "커널")

UY, KY, BH = 140, 336, 92

def node(x, y, w, title, subs, c=None, fam=MONO, size=15, sec=None):
    if c: d.tone(x, y, w, BH, c, 6, "14", 1.4)
    else: d.box(x, y, w, BH, PAPER2, RULE, 1.0)
    if sec:
        d.t(x + 12, y + 20, sec, 10, SOFT, MONO, "start", 600)
    d.t(x + w/2, y + 34, title, size, c or INK, fam, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w/2, y + 56 + i*20, s, 12, MUTED, MONO if s.isascii() else KR)

# 화살표를 먼저 그린다
# 적재 화살표는 원서 Figure 2-2 처럼 hello() 로 들어간다(Load hello() into kernel, attach to execve).
d.arrow([(248, 186), (392, 186), (392, 332)], MUTED, "ar", 1.5)
d.t(404, 282, "bpf() 적재 · kprobe 부착", 12, MUTED, KR, "start")
d.arrow([(244, 382), (312, 382)], ACC, "acc", 1.5)
d.arrow([(468, 382), (544, 382)], WARN, "warn", 1.5)
d.arrow([(392, 432), (392, 460), (798, 460), (798, 432)], OK, "ok", 1.5)
d.arrow([(622, 332), (622, 240)], WARN, "warn", 1.5)
d.arrow([(798, 332), (798, 240)], OK, "ok", 1.5)

node(48, UY, 196, "hello.py · hello-map.py", ["BPF(text=) 컴파일", "attach_kprobe 적재 · 부착"], None, MONO, 13, "§1·§4")
node(548, UY, 148, "trace_print()", ["trace_pipe 읽기"], WARN, size=14, sec="§2")
node(720, UY, 156, 'b["counter_table"]', ["2초마다 items()"], OK, MONO, 13, "§4")
node(48, KY, 196, "__x64_sys_execve", ["kprobe 가 걸린 곳", "execve 마다 실행"], None, MONO, sec="§1")
node(316, KY, 152, "hello()", ["eBPF 프로그램"], ACC, sec="§1")
node(548, KY, 148, "trace_pipe", ["tracefs 버퍼", "문자열 한 줄"], WARN, size=15, sec="§2")
node(720, KY, 156, "counter_table", ["BPF_HASH", "UID → 횟수"], OK, size=14, sec="§3·§4")

d.legend(H - 40, [("hello() 실행", ACC), ("trace_pipe 길", WARN), ("맵 길", OK)])
d.save("02-01.chapter-overview.svg")
