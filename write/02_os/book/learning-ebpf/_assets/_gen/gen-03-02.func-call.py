# 타입 스펙: type-sequence — 참여자 셋(hello · get_opcode · bpf_trace_printk), 메시지 여섯. focal 은 0번 call pc+7 한 줄.
# 사실 출처: 추출본 ebpf3.txt 966~1063행(xlated 0~9번 · call pc+7 · r0 = *(u64 *)(r1 +8)),
#   예제 저장소 chapter3/hello-func.bpf.c, v7.2 include/uapi/linux/bpf.h L7316~7318(args[0] 의 u64 배열),
#   docs.kernel.org BPF Instruction Set 의 Program-local functions(호출 다음 명령 기준 offset).
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

W, H = 960, 656
d = SeqKR(W, H, "LEARNING EBPF · 03-02 §4",
          "call pc+7 은 오프셋 8 로 가서 exit 로 돌아온다",
          "hello 의 0번 call 이 다음 명령 1 에 7 을 더한 오프셋 8 의 get_opcode 로 가고, exit 가 1번으로 돌려보낸다.",
          "프레임 0 과 프레임 1 이 한 호출에서 주고받는 명령")

NAMES = (("hello", "프레임 0 · raw_tp"), ("get_opcode", "프레임 1 · noinline"), ("bpf_trace_printk", "커널 헬퍼"))
d.LX = {"hello": 160, "get_opcode": 480, "bpf_trace_printk": 800}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, MONO, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg("hello", "get_opcode", "0: call pc+7", 196, ACC, "acc", sub="1 + 7 = 오프셋 8")
d.selfmsg("get_opcode", "8: r0 = *(u64 *)(r1 +8)", 268, INFO, "args[1] · 바이트 오프셋 8")
d.msg("get_opcode", "hello", "9: exit", 340, OK, "ok", dash="5 4", sub="r0 = args[1]")
d.selfmsg("hello", "1: r1 = map[id:193][0]+0", 412, INFO, "3: r2 = 12 · 4: r3 = r0")
d.msg("hello", "bpf_trace_printk", "5: call bpf_trace_printk", 484, MUTED, "ar", sub="Syscall: %d")
d.selfmsg("hello", "6: r0 = 0 · 7: exit", 556, INFO, "프레임 0 종료")

d.legend(H - 56, [("함수 호출", ACC), ("복귀", OK), ("프레임 안 명령", INFO), ("헬퍼 호출", MUTED)])
d.save("03-02.func-call.svg")
