# 타입 스펙: type-architecture — 사용자 공간(hello.py)과 커널(kprobe → hello() → 두 출력 통로)을 경계 둘로 나눈 지도.
# 사실 출처: 예제 저장소 chapter2/hello.py·hello-map.py, 추출본 src/ebpf2.txt 33~146행·311~456행,
#   커널 v7.2 arch/x86/include/asm/syscall_wrapper.h 15~17행(`__x64_sys_*`), include/uapi/linux/bpf.h 2021~2032행(trace_pipe).
# Layout conventions: 밴드 둘(사용자 공간·커널), 박스 높이 92, 열 x 는 48·316·548·736. focal 은 hello().
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 920, 560
d = D(W, H, "LEARNING EBPF · 02-01", "hello.py 한 개가 커널에 프로그램을 올리고 두 길로 결과를 받는다",
      "사용자 공간의 hello.py 가 hello() 를 컴파일해 적재하고 execve 의 kprobe 에 붙인다. execve 가 불릴 때마다 hello() 가 돌고, 결과는 trace_pipe 와 counter_table 두 통로로 사용자 공간에 돌아온다.",
      "execve 가 불릴 때마다 hello() 가 돌고 결과는 두 통로로 돌아옵니다")

def band(y, h, label):
    d.o.append(f'<rect x="24" y="{y}" width="872" height="{h}" rx="8" fill="none" stroke="{RULE}" stroke-width="1" stroke-dasharray="6 5"/>')
    d.t(40, y + 24, label, 12, MUTED, KR, "start", 600)

band(100, 156, "사용자 공간")
band(292, 196, "커널")

UY, KY, BH = 140, 336, 92

def node(x, y, w, title, subs, c=None, fam=MONO, size=15):
    if c: d.tone(x, y, w, BH, c, 6, "14", 1.4)
    else: d.box(x, y, w, BH, PAPER2, RULE, 1.0)
    d.t(x + w/2, y + 32, title, size, c or INK, fam, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w/2, y + 56 + i*20, s, 11, MUTED, MONO if s.isascii() else KR)

# 화살표를 먼저 그린다
d.arrow([(152, 236), (152, 332)], MUTED, "ar", 1.5)
d.t(168, 282, "bpf() 적재 · kprobe 부착", 12, MUTED, KR, "start")
d.arrow([(244, 382), (312, 382)], ACC, "acc", 1.5)
d.arrow([(468, 382), (544, 382)], WARN, "warn", 1.5)
d.arrow([(392, 432), (392, 460), (816, 460), (816, 432)], OK, "ok", 1.5)
d.arrow([(622, 332), (622, 240)], WARN, "warn", 1.5)
d.arrow([(816, 332), (816, 240)], OK, "ok", 1.5)

node(48, UY, 196, "hello.py", ["BPF(text=) 컴파일", "attach_kprobe 적재 · 부착"], None, MONO)
node(548, UY, 148, "trace_print()", ["trace_pipe 읽기"], WARN)
node(736, UY, 160, 'b["counter_table"]', ["2초마다 items()"], OK, MONO, 13)
node(48, KY, 196, "__x64_sys_execve", ["kprobe 가 걸린 곳", "execve 마다 실행"], None, MONO)
node(316, KY, 152, "hello()", ["eBPF 프로그램"], ACC)
node(548, KY, 148, "trace_pipe", ["tracefs 버퍼", "문자열 한 줄"], WARN)
node(736, KY, 160, "counter_table", ["BPF_HASH", "UID → 횟수"], OK)

d.legend(H - 40, [("hello() 실행", ACC), ("trace_pipe 길", WARN), ("맵 길", OK)])
d.save("02-01.chapter-overview.svg")
