# 타입 스펙: type-sequence — 참여자 넷(호출자 · BPF 트램펄린 · do_unlinkat · kretprobe 경로), 메시지 여섯. focal 은 fexit 프로그램이 dfd·name·ret 셋을 모두 받는 한 줄.
# 사실 출처: libbpf-bootstrap examples/c/kprobe.bpf.c 의 BPF_KRETPROBE(do_unlinkat_exit, long ret)·fentry.bpf.c 의 BPF_PROG(do_unlinkat, int dfd, struct filename *name)·
#   BPF_PROG(do_unlinkat_exit, int dfd, struct filename *name, long ret) (master 6ca4009), 추출본 ebpf7.txt 342~370행,
#   linux v5.5 arch/x86/net/bpf_jit_comp.c 1397~1456행(트램펄린 어셈블리 주석: fentry 호출 → 본문 → fexit 호출 · "5 byte nop 을 call generated_bpf_trampoline 으로 교체"),
#   v7.2 fs/namei.c 5543행(int filename_unlinkat(int dfd, struct filename *name), do_unlinkat 은 v7.0 에서 이름이 바뀜 — v6.19 5406행).
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

W, H = 960, 640
d = SeqKR(W, H, "LEARNING EBPF · 07-01 §3", "fexit 프로그램은 인자와 반환값을 함께 받고 kretprobe 는 반환값만 받는다",
          "호출자가 do_unlinkat(dfd, name) 을 부르면 트램펄린이 fentry 프로그램에 dfd·name 을 넘기고 본문을 실행한다. 본문이 ret 을 돌려주면 트램펄린이 fexit 프로그램에 dfd·name·ret 을 넘기고, kretprobe 프로그램은 ret 만 받는다.",
          "같은 함수 끝에서 받는 값이 다릅니다")

NAMES = (("호출자", "사용자 공간 · syscall"), ("BPF 트램펄린", "fentry · fexit"), ("do_unlinkat", "v7.0 부터 filename_unlinkat"), ("kretprobe", "대안 경로"))
d.LX = {"호출자": 128, "BPF 트램펄린": 368, "do_unlinkat": 608, "kretprobe": 848}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 108, 100, 216, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg("호출자", "BPF 트램펄린", "do_unlinkat(dfd, name)", 196, MUTED, "ar", sub="함수 앞머리 nop 자리")
d.selfmsg("BPF 트램펄린", "fentry 프로그램", 252, OK, "dfd · name")
d.msg("BPF 트램펄린", "do_unlinkat", "원래 본문 실행", 316, MUTED, "ar")
d.msg("do_unlinkat", "BPF 트램펄린", "ret 반환", 380, MUTED, "ar")
d.selfmsg("BPF 트램펄린", "fexit 프로그램", 440, ACC, "dfd · name · ret")
d.msg("do_unlinkat", "kretprobe", "반환 가로채기", 504, INFO, "info", dash="6 4", sub="kretprobe 프로그램은 ret 만")

d.legend(H - 56, [("fentry 프로그램", OK), ("fexit 프로그램", ACC), ("kretprobe 경로", INFO)])
d.save("07-01.type-sequence.svg")
