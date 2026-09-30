# 01-01.two-waits — 기다리는 방식에 따라 스레드가 풀려나는가
# 본문 요구(01-01 §1): 런타임이 아는 기다림은 goroutine 만 재우고 스레드를 풀어 주며, 커널 안 blocking syscall 은
#           스레드째 갇혀 런타임이 새 스레드를 만든다 — 두 경로의 대비.
# 타입 스펙: type-flowchart — 두 줄의 단계 흐름, 끝 칸이 스레드 수의 결과. focal 은 스레드를 붙잡는 칸.
# 사실 출처: go doc runtime/debug.SetMaxThreads (go1.25.1), 00-02 §2 strace.
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, KR
from ddk import node, harrow

W, H = 960, 404
X, NW, NH, STEP = 24, 192, 64, 240
rows = [
    (140, [("네트워크 소켓 Read", "논블로킹", None, False), ("= -1 EAGAIN", "곧바로 돌아옴", None, False),
           ("goroutine 만 재움", "epoll 에 등록", None, False), ("스레드는 다른 일", "1,000 개여도 코어 수 안팎", OK, False)]),
    (272, [("blocking syscall", "파일 읽기 등", None, False), ("스레드가 커널에서 잠듦", "goroutine 을 쥔 채", ACC, True),
           ("런타임이 새 스레드", "대기열을 넘겨받음", None, False), ("스레드도 1,000 개", "상한 10,000", WARN, False)]),
]
d = D(W, H, "FLOWCHART · 01-01 TWO WAITS", "기다리는 방식이 스레드 수를 가릅니다",
      "위 줄은 런타임이 아는 기다림으로, 논블로킹 소켓의 Read 가 EAGAIN 을 받으면 런타임이 goroutine 만 재우고 "
      "스레드는 다른 goroutine 을 돌린다. 아래 줄은 blocking syscall 로, 스레드가 goroutine 을 쥔 채 커널에서 잠들어 "
      "런타임이 새 스레드를 만들어야 하므로 이런 goroutine 이 1,000 개면 스레드도 1,000 개 가까이 생긴다.",
      lead="위 줄은 스레드가 풀려나고, 아래 줄은 스레드가 갇힙니다.")
d.t(24, 124, "런타임이 아는 기다림", 12, SOFT, KR, "start", 600)
d.t(24, 256, "커널 안의 기다림", 12, SOFT, KR, "start", 600)
for y, nodes in rows:
    y += 8
    for k, (t, s, c, f) in enumerate(nodes):
        x = X + k * STEP
        node(d, x, y, NW, NH, t, s, c, f, 13)
        if k < 3:
            harrow(d, x + NW + 6, x + STEP - 6, y + NH / 2)
d.legend(360, [("스레드가 적게 듦", OK), ("스레드가 연결 수만큼", WARN), ("스레드를 붙잡는 자리", ACC)])
d.save("01-01.two-waits.svg")
print("ok two-waits")
