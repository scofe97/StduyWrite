# 타입 스펙: type-sequence — 참여자 넷(hello.py·BCC·커널·터미널 2), 메시지 여덟. focal 은 execve 마다 도는 hello() 한 줄.
# 사실 출처: 예제 저장소 chapter2/hello.py, 추출본 src/ebpf2.txt 92~146행·164~167행(bash-5412·90432.904952),
#   BCC v0.37.0 src/python/bcc/__init__.py get_syscall_prefix(832행)·trace_print(1632행),
#   커널 v7.2 arch/x86/entry/syscalls/syscall_64.tbl 71행(59 execve).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12)/2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 11)/2}" y="{y + 5}" width="{_w(sub, 11)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 12, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 13, sub, 11, MUTED, _kr(sub), "start")

W, H = 920, 780
d = SeqKR(W, H, "LEARNING EBPF · 02-01 §1",
          "적재에서 첫 출력 한 줄까지",
          "hello.py 가 BCC 로 C 문자열을 컴파일하고, attach_kprobe 가 프로그램을 bpf() 로 적재해 execve 의 kprobe 에 붙인다. 다른 터미널에서 ls 를 실행하면 execve 가 불리고 hello() 가 돌아 trace_pipe 에 한 줄이 쓰이며, trace_print 가 그 줄을 화면에 낸다.",
          "다른 터미널의 ls 한 번이 hello() 를 한 번 돌립니다")

NAMES = (("hello.py", "사용자 공간 · Python"), ("BCC", "clang · LLVM"), ("커널", "kprobe · eBPF"), ("터미널 2", "다른 터미널"))
d.LX = {"hello.py": 120, "BCC": 340, "커널": 560, "터미널 2": 780}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR if any("가" <= c <= "힣" for c in nm) else MONO, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg("hello.py", "BCC", "BPF(text=program)", 196, MUTED, "ar")
d.selfmsg("BCC", "컴파일", 252, MUTED, "clang · LLVM")
d.msg("hello.py", "BCC", "attach_kprobe", 308, MUTED, "ar", sub="__x64_sys_execve")
d.msg("BCC", "커널", "bpf()", 364, MUTED, "ar", sub="프로그램 적재")
d.selfmsg("커널", "kprobe 부착", 420, MUTED, "__x64_sys_execve")
d.msg("터미널 2", "커널", "ls", 480, INFO, "info", sub="execve · syscall 59")
d.selfmsg("커널", "hello()", 540, ACC, "bpf_trace_printk")
d.msg("커널", "hello.py", "trace_pipe 한 줄", 604, WARN, "warn", sub="bash-5412 · 90432.904952")
d.selfmsg("hello.py", "trace_print()", 660, OK, "화면 출력")

d.legend(H - 56, [("hello() 실행", ACC), ("trace_pipe 로 돌아온 줄", WARN), ("execve 를 일으키는 명령", INFO), ("화면 출력", OK)])
d.save("02-01.launch-sequence.svg")
