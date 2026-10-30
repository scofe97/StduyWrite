# 타입 스펙: type-sequence — 참여자 넷(컨테이너 앱 · enter_trace · OCI 훅 · 런타임), 메시지 여덟. focal 은 훅이 쓰는 profile.json 한 줄.
# 사실 출처: containers/oci-seccomp-bpf-hook main(8daf794, 2026-09-14) oci-seccomp-bpf-hook.go 236행(PARENT_PID 치환)·248행(LoadTracepoint enter_trace)·
#   259행(AttachTracepoint raw_syscalls:sys_enter)·262행(sched:sched_process_exit)·368행(DefaultAction = ActErrno)·375행(ActAllow names), bpf/ebpf.c 11행(seen_syscalls)·44~117행(enter_trace)·120~129행(check_exit stopTracing).
#   syscall 번호 read 0·write 1·openat 257·reboot 169 는 v7.2 arch/x86/entry/syscalls/syscall_64.tbl, defaultErrnoRet 기본 EPERM 은 runtime-spec v1.3.0 config-linux.md 886행.
# Layout conventions: 레인 중심 x=120·360·600·840, 레인 상자 w=200, 메시지 stride 64, 첫 메시지 y=196. 모든 좌표 4의 배수.
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
        s.o.append(f'<rect x="{mx - _w(label, 13)/2}" y="{y - 23}" width="{_w(label, 13)}" height="18" fill="{PAPER}"/>')
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="18" fill="{PAPER}"/>')
            s.t(mx, y + 18, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 14, sub, 13, MUTED, _kr(sub), "start")


W, H = 960, 760
d = SeqKR(W, H, "LEARNING EBPF · 09-01 §2",
          "관측한 syscall 번호가 seccomp 프로파일 JSON 이 된다",
          "훅은 컨테이너 init 의 mount namespace 안 syscall 을 처음 보는 번호만 사용자 공간으로 올리고, 컨테이너가 끝나면 그 목록을 허용 이름으로 한 JSON 을 쓴다. 런타임이 다음 시작에 적재하면 목록에 없는 reboot 은 ERRNO 가 된다.",
          "관측한 호출이 허용 목록이 되고 나머지는 EPERM 이 됩니다")

d.LX = {"앱": 120, "추적": 360, "훅": 600, "런타임": 840}
for key, nm, sub in (("앱", "컨테이너 앱", "사용자 공간"), ("추적", "eBPF 프로그램", "커널"),
                     ("훅", "OCI 훅", "Go · gobpf"), ("런타임", "런타임", "OCI 런타임")):
    x = d.LX[key]
    d.box(x - 100, 100, 200, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 13, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

d.msg("앱", "추적", "read", 196, INFO, "info", sub="번호 0")
d.msg("앱", "추적", "write", 260, INFO, "info", sub="번호 1")
d.msg("앱", "추적", "openat", 324, INFO, "info", sub="번호 257")
d.msg("추적", "훅", "perf_submit", 388, MUTED, "ar", sub="sys_enter · 처음 본 번호만")
d.msg("추적", "훅", "stopTracing", 452, MUTED, "ar", sub="sched_process_exit")
d.msg("훅", "런타임", "defaultAction ERRNO", 516, ACC, "acc", sub="허용 read · write · openat")
d.msg("런타임", "앱", "seccomp 필터 적재", 580, OK, "ok", sub="다음 시작 때")
d.selfmsg("앱", "reboot", 644, BAD, "번호 169 → EPERM")

d.legend(H - 56, [("호출 관측", INFO), ("프로파일 쓰기", ACC), ("필터 적재", OK), ("차단", BAD)])
d.save("09-01.profile-generation.svg")
