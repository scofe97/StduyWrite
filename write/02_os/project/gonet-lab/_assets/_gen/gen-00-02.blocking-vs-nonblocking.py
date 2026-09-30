# 00-02.blocking-vs-nonblocking — 같은 accept 를 두 방식으로 부를 때 누가 기다리나
# 본문 요구(00-02 §2): blocking 은 "스레드가 커널 안에서 잠들고", nonblocking 은 "곧바로 EAGAIN 을 돌려주고
#           Go 런타임이 goroutine 만 재운 뒤 epoll 알림으로 깨워 accept4 를 다시 부른다" — 두 흐름의 대비가 논지다.
# 타입 스펙: type-sequence — 레인 셋(호출하는 쪽·Go 런타임·커널), 위 칸 blocking / 아래 칸 nonblocking. 돌아오는 값은 점선.
# 사실 출처: accept(2) ERRORS EAGAIN, gonet-lab 실험 1-C strace (accept4 EAGAIN → = 5 → EAGAIN).
from dd import INK, MUTED, SOFT, RULE, OK, WARN, KR, MONO
from ddk import SeqKR

W, H = 960, 724
A, R, K = "호출하는 쪽", "Go 런타임", "커널"
d = SeqKR(W, H, "SEQUENCE · 00-02 BLOCKING VS NONBLOCKING", "같은 accept, 누가 기다리나",
          "위 칸은 blocking 소켓의 accept 로, 호출한 스레드가 연결이 올 때까지 커널 안에서 잠든다. 아래 칸은 "
          "SOCK_NONBLOCK 소켓의 accept4 로, 커널은 곧바로 EAGAIN 을 돌려주고 Go 런타임이 goroutine 을 재운 채 "
          "epoll 에 등록했다가, 연결 도착 알림을 받아 깨운 뒤 accept4 를 다시 불러 FD 5 를 받는다.",
          lead="위 칸은 스레드가 커널에서 잠들고, 아래 칸은 런타임이 goroutine 만 재웁니다.")
d.lanes([(A, "스레드 · goroutine"), (R, "프로그램 안"), (K, "listener · epoll")], y0=96, lane_w=200)
d.rails(668)
xa = d.LX[A]

d.t(24, 176, "blocking", 12, SOFT, MONO, "start", 600)
d.msg(A, K, "accept", 204)
d.tone(xa - 6, 216, 12, 64, WARN, 2, "30", 1.2)
d.t(xa + 16, 252, "스레드가 커널 안에서 잠듦", 12, WARN, KR, "start", 600)
d.msg(K, A, "= 5", 300, OK, "ok", dash="5 4", sub="연결이 온 뒤에야 돌아옴")

d.line(24, 340, W - 48, 340, RULE, 1.0, "6 4")
d.t(24, 364, "nonblocking", 12, SOFT, MONO, "start", 600)
d.msg(A, K, "accept4", 392)
d.msg(K, A, "-1 EAGAIN", 432, MUTED, "ar", dash="5 4", sub="곧바로")
d.msg(A, R, "goroutine 재우기", 484)
d.msg(R, K, "epoll 에 FD 4 등록", 524)
d.msg(K, R, "연결 도착 알림", 564, OK, "ok", dash="5 4")
d.msg(R, A, "깨우기", 604, OK, "ok")
d.msg(A, K, "accept4", 636, OK, "ok")
d.msg(K, A, "= 5", 660, OK, "ok", dash="5 4")

d.legend(684, [("스레드가 잠든 구간", WARN), ("깨어나 이어지는 흐름", OK)])
d.save("00-02.blocking-vs-nonblocking.svg")
print("ok blocking")
