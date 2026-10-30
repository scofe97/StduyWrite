# 타입 스펙: type-sequence — 참여자 넷(프로세스 · do_mprotect_pkey · security_file_mprotect · mprotect_audit), 메시지 여섯. focal 은 mprotect_audit 가 돌려주는 -EPERM 한 줄. 레인 머리는 하드코딩 mono 를 피해 직접 그린다.
# 사실 출처: 커널 v7.2 kernel/trace/trace_kprobe.c L1691~1706(kprobe 반환값은 perf 이벤트 기록 여부), docs.kernel.org/bpf/prog_lsm.html(SEC("lsm/file_mprotect") · int ret 은 앞선 프로그램의 반환값, 첫 프로그램이면 0 · 힙이면 -EPERM),
#   커널 v7.2 mm/mprotect.c L953~955(error = security_file_mprotect(vma, reqprot, prot); if (error) break;) · L836 do_mprotect_pkey · L985~988 SYSCALL_DEFINE3(mprotect),
#   arch/x86/entry/syscalls/syscall_64.tbl L22(10 common mprotect sys_mprotect).
# Layout conventions: 레인 중심 x=120·360·600·840, 레인 머리 w=200 h=48, 메시지 stride 72(y=196 부터). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def _w(t, size):
    return sum(size * (1.0 if "가" <= c <= "힣" else 0.62) for c in str(t)) + 12


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.o.append(f'<rect x="{mx - _w(label, 12) / 2}" y="{y - 23}" width="{_w(label, 12)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 12) / 2}" y="{y + 5}" width="{_w(sub, 12)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))


W, H = 960, 740
d = SeqKR(W, H, "LEARNING EBPF · 07-02 §2",
          "mprotect 한 번이 file_mprotect 훅에서 EPERM 으로 끝난다",
          "프로세스의 mprotect(시스템 콜 번호 10)가 do_mprotect_pkey 에서 security_file_mprotect 를 부르고, 훅에 붙은 mprotect_audit 가 힙이면 -EPERM 을 돌려 시스템 콜이 EPERM 으로 실패한다.",
          "반환값이 음수 errno 면 커널은 mprotect 를 진행하지 않습니다")

NAMES = (("프로세스", "mprotect()"), ("do_mprotect_pkey", "mm/mprotect.c"),
         ("security_file_mprotect", "LSM 훅"), ("mprotect_audit", "BPF LSM 프로그램"))
d.LX = {"프로세스": 120, "do_mprotect_pkey": 360, "security_file_mprotect": 600, "mprotect_audit": 840}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 108, 100, 216, 48, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12, INK, _kr(nm), "middle", 600)
    d.t(x, 138, sub, 12, MUTED, _kr(sub))
d.lane_top = 148
d.rails(H - 80)

d.msg("프로세스", "do_mprotect_pkey", "mprotect (번호 10)", 196, INFO, "info", sub="대상은 힙 영역")
d.msg("do_mprotect_pkey", "security_file_mprotect", "security_file_mprotect", 268, MUTED, "ar", sub="vma · reqprot · prot")
d.msg("security_file_mprotect", "mprotect_audit", "ret = 0", 340, MUTED, "ar", sub="첫 프로그램은 0")
d.msg("mprotect_audit", "security_file_mprotect", "return -EPERM", 412, ACC, "acc", dash="5 4", sub="is_heap")
d.msg("security_file_mprotect", "do_mprotect_pkey", "error = -EPERM", 484, BAD, "bad", dash="5 4", sub="break")
d.msg("do_mprotect_pkey", "프로세스", "EPERM", 556, BAD, "bad", dash="5 4", sub="mprotect() 실패")

# kprobe 대조는 이 흐름의 한 단계가 아니므로 화살표가 아니라 레인 밖 비교 메모로 둔다
d.o.append(f'<rect x="520" y="604" width="400" height="48" rx="6" fill="{PAPER}" stroke="{RULE}" stroke-width="1" stroke-dasharray="4 4"/>')
d.t(720, 624, "비교 · kprobe 반환값", 12, INK, KR, "middle", 600)
d.t(720, 642, "이벤트 기록 여부만 · 거부 못 함", 12, MUTED, KR)

d.legend(H - 56, [("시스템 콜", INFO), ("훅 호출", MUTED), ("거부", ACC), ("오류 전파", BAD)])
d.save("07-02.lsm-mprotect-sequence.svg")
