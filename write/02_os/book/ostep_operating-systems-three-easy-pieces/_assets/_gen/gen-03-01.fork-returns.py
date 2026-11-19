# 03-01 「한 번 호출하고 두 번 돌아오기」 — fork() 호출 하나가 부모에게는 자식의 PID 를, 자식에게는 0 을 돌려주며 둘로 갈라진다.
# 본문 근거: 이 노트 「1. fork 로 프로세스 복제하기」.
# 값 근거: 5장 p1.c 실행 예의 PID(부모 29146, 자식 29147). 직접 실행해 얻은 값이 아니다.
# 공식 근거: OSTEP 5장 §5.1 — 부모는 자식의 PID 를, 자식은 0 을 받는다. rc < 0 이면 fork 실패.
# 타입 스펙: type-sequence — 호출 하나가 둘로 갈라지는 반환을 시간순으로.
import sys; sys.path.insert(0, ".")
from dd import PAPER, Seq, ACC, MUTED, SOFT, INK, OK, INFO, RULE, KR, MONO

W, H = 920, 520
d = Seq(W, H, "OSTEP · 03-01 §1",
        "fork() 는 한 번 부르면 두 번 돌아온다",
        "부모가 fork 를 부르면 커널이 자식을 만들고, 부모에게는 자식의 PID 인 29147 을, 자식에게는 0 을 돌려준다. "
        "코드는 반환값이 0 인지 0 보다 큰지로 자식 갈래와 부모 갈래를 나눈다.",
        lead="PID 는 5장 실행 예의 값입니다.")
def stbk(a, txt, y, c):
    w = len(txt) * 7.0 + 18
    d.box(d.LX[a] - w / 2, y - 10, w, 20, PAPER, PAPER, 0, 4)
    d.state(a, txt, y, c)


d.lanes([("부모", "pid 29146"), ("커널", "kernel mode"), ("자식", "pid 29147")], lane_w=200)
d.rails(470)
d.msg("부모", "커널", "fork()", 200, ACC, mk="acc", sub="호출은 한 번")
d.msg("커널", "부모", "rc = 29147", 280, OK, mk="ok", sub="자식의 PID", dash="5 4")
d.msg("커널", "자식", "rc = 0", 350, INFO, mk="info", sub="fork 자리에서 시작", dash="5 4")
stbk("부모", "rc > 0", 410, OK)
stbk("자식", "rc == 0", 410, INFO)
d.legend(H - 40, [("부모에게 반환", OK), ("자식에게 반환", INFO), ("호출", ACC)])
d.save("03-01.fork-returns.svg")
print("ok 03-01 fork-returns")
