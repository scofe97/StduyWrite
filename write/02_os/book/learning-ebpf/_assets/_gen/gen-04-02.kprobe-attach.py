# 타입 스펙: type-sequence — 참여자 넷(hello-buffer-config.py · 커널 perf · 프로그램 6 · 다른 프로세스), 메시지 일곱. focal 은 ioctl SET_BPF 한 줄.
# 사실 출처: 추출본 ebpf4.txt 640~710행(perf_event_open({type=0x6 ...}) = 7 · ioctl(7, PERF_EVENT_IOC_SET_BPF, 6) = 0 · ioctl(7, PERF_EVENT_IOC_ENABLE, 0) = 0),
#   fd 6 = hello 프로그램(304행). BCC v0.37.0 src/cc/libbpf.c 1204~1209행(ioctl 두 번), 1035~1056행(kprobe PMU type 을 sysfs 에서 읽음).
# Layout conventions: 레인 폭 176·중심 x=120·440·664·862, 메시지 stride 56~64(y=196부터), 레일 하단 H-80. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO


def _kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


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
            s.o.append(f'<rect x="{mx - _w(sub, 13)/2}" y="{y + 5}" width="{_w(sub, 13)}" height="20" fill="{PAPER}"/>')
            s.t(mx, y + 19, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, mk="ar"):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+58} {y-10} L {x+58} {y+10} L {x+13} {y+10}", c, 1.4, m=mk)
        s.t(x + 68, y - 4, label, 13, c, _kr(label), "start", 600)
        if sub: s.t(x + 68, y + 15, sub, 13, MUTED, _kr(sub), "start")


W, H = 960, 700
d = SeqKR(W, H, "LEARNING EBPF · 04-02 §1",
          "perf 이벤트 fd 7 에 프로그램 6 을 붙인다",
          "hello-buffer-config.py 가 perf_event_open 으로 kprobe 이벤트 fd 7 을 받고 ioctl 두 번으로 프로그램 6 을 붙여 켠다. 다른 프로세스가 execve 를 부르면 fd 7 의 kprobe 가 프로그램 6 을 실행한다.",
          "bpf() 호출 0건")

NAMES = (("hello-buffer-config.py", "사용자 공간 · Python"),
         ("커널 perf", "perf_event · kprobe"),
         ("프로그램 6", "hello · eBPF"),
         ("다른 프로세스", "execve 를 부름"))
d.LX = {"hello-buffer-config.py": 120, "커널 perf": 440, "프로그램 6": 664, "다른 프로세스": 862}
for nm, sub in NAMES:
    x = d.LX[nm]
    d.box(x - 88, 100, 176, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 12 if nm.startswith("hello") else 13, INK, _kr(nm), "middle", 600)
    d.t(x, 137, sub, 12, MUTED, _kr(sub))
d.lane_top = 144
d.rails(H - 80)

A, P, G, O = "hello-buffer-config.py", "커널 perf", "프로그램 6", "다른 프로세스"
d.msg(A, P, "perf_event_open", 196, MUTED, "ar", sub="{type=0x6, ...}")
d.msg(P, A, "= 7", 252, MUTED, "ar", dash="5 4", sub="kprobe 이벤트 fd")
d.msg(A, P, "ioctl(7, PERF_EVENT_IOC_SET_BPF, 6)", 316, ACC, "acc", sub="= 0 · fd 7 에 프로그램 6 부착")
d.msg(A, P, "ioctl(7, PERF_EVENT_IOC_ENABLE, 0)", 380, MUTED, "ar", sub="= 0 · kprobe 켬")
d.msg(O, P, "execve", 444, INFO, "info", sub="다른 프로세스의 호출")
d.msg(P, G, "kprobe 7", 508, WARN, "warn", sub="fd 7 에 붙은 프로그램")
d.selfmsg(G, "hello() 실행", 580, OK, "output 맵에 기록", mk="ok")

d.legend(H - 56, [("부착 ioctl", ACC), ("execve 호출", INFO), ("kprobe 발동", WARN), ("프로그램 실행", OK)])
d.save("04-02.kprobe-attach.svg")
