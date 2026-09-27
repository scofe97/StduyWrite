# 12-02.deadlock-select — 예제 12-1 은 두 고루틴이 서로의 읽기를 기다리며 멈추고, 12-2 는 select 가 ch1 읽기를 고른다
# 본문 요구(12-02 §1 「교착 상태와 select」): 두 예제에서 두 고루틴이 어디서 멈추는지 나란히 보인다. 12-1 은 main 이 ch2 에,
#           띄운 고루틴이 ch1 에 쓰며 서로 읽어 주기를 기다려 교착. 12-2 는 main 의 select 가 ch1 읽기를 골라 main: 2 1 을 찍고,
#           띄운 고루틴은 ch2 읽기에서 멈춘 채 남는다.
# 타입 스펙: type-sequence — 레인 넷(main 고루틴 · ch2 · ch1 · 띄운 고루틴), 시간은 위→아래. 같은 레인을 두 번(t1 = 예제 12-1,
#           t2 = 예제 12-2) 그려 흐름을 보인다. 상태는 레인 옆 칩, focal 은 select 가 고른 읽기 화살표 하나.
# 사실 출처: Learning Go 2판 12장 예제 12-1·12-2, go1.25.1 로컬 실행 — 12-1 은 두 고루틴 모두 [chan send] 로 멈춘 deadlock,
#           12-2 원문 코드는 main: 2 1 (2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 600
d = Seq(W, H, "SEQUENCE · 12-02 §1",
        "예제 12-1 은 둘 다 쓰기에서 멈추고, 12-2 는 select 가 읽기를 고릅니다",
        "위는 예제 12-1. 띄운 고루틴은 ch1 에 1 을 쓰고 main 고루틴은 ch2 에 2 를 쓴다. 버퍼 없는 채널이라 둘 다 상대가 읽어 주기를 기다리며 멈추고, "
        "모든 고루틴이 잠들어 런타임이 deadlock 으로 프로그램을 끝낸다. 아래는 예제 12-2. main 고루틴은 ch2 쓰기와 ch1 읽기를 select 로 감싸고, "
        "띄운 고루틴이 ch1 쓰기에서 기다리고 있으니 select 가 읽기를 골라 main: 2 1 을 찍는다. 띄운 고루틴은 ch2 읽기에서 멈춘 채 남는다.",
        lead="위는 예제 12-1, 아래는 예제 12-2 입니다. 채널 두 개도 레인으로 그렸습니다.")
d.lanes([("main 고루틴", "main()"), ("ch2", "chan int"), ("ch1", "chan int"), ("띄운 고루틴", "go func()")], y0=96, lane_w=180)
d.rails(520)

d.t(24, 178, "t1 · 예제 12-1", 12, MUTED, KR, "start", 600)
d.msg("띄운 고루틴", "ch1", "ch1 <- 1", 206)
d.msg("main 고루틴", "ch2", "ch2 <- 2", 242)
d.state("띄운 고루틴", "읽을 쪽 대기", 278, WARN)
d.state("main 고루틴", "읽을 쪽 대기", 278, WARN)
FATAL = "fatal error: all goroutines are asleep - deadlock!"
fw = len(FATAL) * 12 * 0.62 + 16
d.box(W / 2 - fw / 2, 302, fw, 24, PAPER, PAPER, 0, 4)
d.t(W / 2, 318, FATAL, 12, BAD, MONO, "middle", 600)

d.line(24, 340, W - 48, 340, RULE, 0.8, "4 4")
d.t(24, 368, "t2 · 예제 12-2", 12, MUTED, KR, "start", 600)
d.msg("띄운 고루틴", "ch1", "ch1 <- 1", 396)
d.msg("ch1", "main 고루틴", "select 가 고름", 432, ACC, "acc", sub="fromGoroutine = 1")
d.state("main 고루틴", "main: 2 1 출력", 480, OK)
d.state("띄운 고루틴", "<-ch2 에서 대기", 480, WARN)

d.legend(540, [("멈춘 채 기다림", WARN), ("select 가 고른 case", ACC), ("진행함", OK), ("런타임이 끝냄", BAD)])
d.save("12-02.deadlock-select.svg")
print("ok 12-02 deadlock")
