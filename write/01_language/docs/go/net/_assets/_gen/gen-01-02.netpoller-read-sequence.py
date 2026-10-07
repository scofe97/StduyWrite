# 사실 출처: go1.25.1 src/net/net.go:192, src/net/fd_posix.go:67, src/internal/poll/fd_unix.go:141, src/internal/poll/fd_poll_runtime.go:88, src/runtime/netpoll.go:548, src/runtime/netpoll_epoll.go:99
# 타입 스펙: type-sequence
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 640

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub), "middle")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        fam = _kr(txt)
        w = len(str(txt)) * (11.0 if fam == KR else 7.0) + 18
        s.o.append(f'<rect x="{x-w/2}" y="{y-10}" width="{w}" height="20" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 11, c, fam)

d = SeqKR(W, H,
          "NETPOLLER READ SEQUENCE",
          "블로킹 Read 의 내부 netpoller 동작 시퀀스",
          "EAGAIN 발생 시 고루틴 파킹과 OS 멀티플렉서의 unpark 재개 흐름",
          "스레드를 묶지 않고 고루틴만 재우는 논블로킹 I/O 와 런타임 스케줄러 연동")

lanes = d.lanes([
    ("고루틴 (G)", "conn.Read()"),
    ("poll.FD", "internal/poll"),
    ("커널 소켓", "OS Socket"),
    ("netpoller", "runtime epoll/kqueue")
], y0=96, lane_w=190)

d.rails(545)

# 1. 고루틴 -> poll.FD: Read(p)
d.msg("고루틴 (G)", "poll.FD", "1. Read(p)", 160, MUTED, "ar")

# 2. poll.FD -> 커널 소켓: syscall.Read
d.msg("poll.FD", "커널 소켓", "2. syscall.Read(fd, p)", 195, MUTED, "ar")

# 3. 커널 소켓 -> poll.FD: EAGAIN
d.msg("커널 소켓", "poll.FD", "3. EAGAIN", 230, WARN, "warn", dash="4 3")

# 4. poll.FD -> netpoller: waitRead
d.msg("poll.FD", "netpoller", "4. waitRead() → runtime_pollWait()", 265, WARN, "warn")

# 5. netpoller 고루틴 파킹 (waiting 전환)
d.state("고루틴 (G)", "_Gwaiting (gopark)", 300, WARN)
d.state("netpoller", "netpollblock() 등록", 300, MUTED)

# 6. 커널 소켓 패킷 도착
d.chip(d.LX["커널 소켓"], 345, "패킷 도착 (소켓 버퍼)", OK, size=11)

# 7. 커널 소켓 -> netpoller: 이벤트 통지
d.msg("커널 소켓", "netpoller", "5. epoll_wait / kevent 준비 완료", 385, OK, "ok")

# 8. netpoller -> 고루틴: 깨움 (runnable 전환)
d.msg("netpoller", "고루틴 (G)", "6. netpollready() → _Grunnable", 420, OK, "ok", dash="4 3")

# 9. poll.FD -> 커널 소켓: syscall.Read 재시도 (focal)
d.msg("poll.FD", "커널 소켓", "7. syscall.Read(fd, p) 재시도", 460, ACC, "acc")

# 10. 커널 소켓 -> poll.FD: 데이터 반환
d.msg("커널 소켓", "poll.FD", "8. 데이터 바이트", 495, ACC, "acc", dash="4 3")

# 11. poll.FD -> 고루틴: (n, nil)
d.msg("poll.FD", "고루틴 (G)", "9. (n, nil) 반환", 530, OK, "ok", dash="4 3")

# 범례
d.legend(575, [
    ("동기 호출 / 반환", MUTED),
    ("EAGAIN / 고루틴 파킹", WARN),
    ("이벤트 감지 / unpark", OK),
    ("재시도 성공 (focal)", ACC)
])

d.save("01-02.netpoller-read-sequence.svg")
