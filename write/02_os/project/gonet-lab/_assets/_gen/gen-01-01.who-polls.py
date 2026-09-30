# 01-01.who-polls — 어떤 fd 의 기다림이 netpoller 로 가고, 어떤 것이 스레드를 쥐는가
# 본문 요구(01-01 §1 「EAGAIN 없이 스레드가 막히는 곳」): 소켓은 netpoller 에 올라 [IO wait] 로 스레드를 반납하고,
#           디스크 파일·블로킹 stdin·syscall 직접 호출·cgo 는 netpoller 를 거치지 않아 [syscall] 로 스레드를 쥔다.
# 타입 스펙: type-flowchart — 네 줄의 단계 흐름(입구 → 판정 → 결과 상태). focal 은 gonet client 가 만난 stdin 줄.
# 사실 출처: go1.25.1 src/os/file_unix.go(newFile 의 pollable 판정, epoll 등록 실패 주석), runtime2.go waitReason,
#           experiments/phase1-two-waits 확인 실행(net: IO wait 101 · 스레드 8, pipe: syscall 100 · 스레드 103).
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, KR
from ddk import node, harrow

W, H = 960, 520
X, NW, NH, STEP, Y0, DY = 24, 256, 60, 332, 120, 84
rows = [
    [("소켓 net.Conn", "Go 가 논블로킹으로 만듦", None, False), ("netpoller 에 등록", "EAGAIN 이면 재움", None, False),
     ("[IO wait]", "스레드 반납", OK, False)],
    [("디스크 파일 os.Open", "일반 파일", None, False), ("epoll 이 등록 거부", "블로킹 read 로 되돌아감", None, False),
     ("[syscall]", "스레드를 쥠", WARN, False)],
    [("os.Stdin", "터미널은 보통 블로킹", ACC, True), ("NewFile 은 이미 논블로킹일 때만", "netpoller 에 올림", ACC, True),
     ("[syscall]", "취소할 수 없음", WARN, False)],
    [("syscall.Read · cgo", "런타임을 거치지 않음", None, False), ("netpoller 밖", "커널·C 코드 안에서 기다림", None, False),
     ("[syscall]", "스레드를 쥠", WARN, False)],
]
d = D(W, H, "FLOWCHART · 01-01 WHO POLLS", "어떤 기다림이 스레드를 쥐는가",
      "소켓은 Go 가 논블로킹으로 만들어 netpoller 에 올리므로 기다리는 goroutine 이 IO wait 로 잠들고 스레드를 반납한다. "
      "디스크 파일은 epoll 이 등록을 거부하고, os.Stdin 은 이미 논블로킹일 때만 등록되며, syscall 직접 호출과 cgo 는 "
      "런타임을 거치지 않으므로 셋 다 syscall 상태로 스레드를 쥔 채 기다린다. gonet client 의 stdin 이 셋째 줄이다.",
      lead="netpoller 에 올라간 줄만 스레드를 돌려줍니다.")
for r, nodes in enumerate(rows):
    y = Y0 + r * DY
    for k, (t, s, c, f) in enumerate(nodes):
        x = X + k * STEP
        node(d, x, y, NW, NH, t, s, c, f, 13)
        if k < 2:
            harrow(d, x + NW + 6, x + STEP - 6, y + NH / 2)
d.legend(Y0 + 4 * DY + 8, [("스레드 반납", OK), ("스레드를 쥠", WARN), ("gonet client 가 만난 자리", ACC)])
d.save("01-01.who-polls.svg")
print("ok who-polls")
