# 21-01 「pthread_create 의 네 인자가 새 스레드에 닿는 길」 — 호출하는 쪽의 인자 넷이 새 스레드의 어느 칸이 되는지, 값 {10, 20} 이 어디로 건너가는지.
# 본문 근거: 이 노트 「1. 스레드 생성과 시작 함수」의 「인자 구조체를 넘기는 예제」.
# 값 근거: 코드의 args = {10, 20} 을 따라간 값이다. 실행한 출력이 아니다.
# 공식 근거: OSTEP 27장 §27.1 그림 27.1 — pthread_create(&p, NULL, mythread, &args) 와 mythread 안의 (myarg_t *) arg 형변환.
# 타입 스펙: type-data-flow — 호출 쪽과 새 스레드 쪽을 가로지르는 데이터. 가로 직선 화살표 넷, 새 스레드가 값을 꺼내 쓰는 넷째 줄만 코랄(focal).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, KR, MONO

W, H = 880, 492
d = D(W, H, "OSTEP · 21-01 §1",
      "인자 네 개가 새 스레드의 칸이 되는 길",
      "main 이 pthread_create(&p, NULL, mythread, &args) 를 부르면 첫째 인자는 핸들 칸, 둘째는 기본 속성, "
      "셋째는 첫 실행 함수, 넷째는 새 스레드가 받는 void 포인터가 된다. 넷째 줄에서 main 의 args 주소가 그대로 건너간다.")

LX, LW = 24, 228
RX, RW = 600, 256
d.t(LX, 100, "호출하는 쪽 · main 스레드", 12, MUTED, KR, "start", 600)
d.t(RX + RW, 100, "새 스레드 · mythread", 12, MUTED, KR, "end", 600)

rows = [
    ("&p", "thread", "새 스레드의 핸들이 p 에 기록됨", None, INFO, "info"),
    ("NULL", "attr", "스택 크기 · 우선순위는 기본값", None, INFO, "info"),
    ("mythread", "start_routine", "새 스레드의 첫 실행 함수", None, INFO, "info"),
    ("&args", "arg", "(myarg_t *) arg 로 되돌림", "printf 로 10 20 을 따라감", ACC, "acc"),
]
Y = 124
STRIDE = 76
for i, (left, name, right, right2, c, m) in enumerate(rows):
    y = Y + i * STRIDE
    cy = y + 24
    d.tone(LX, y, LW, 48, INFO if c != ACC else ACC)
    d.t(LX + LW / 2, cy + 5, left, 13, INK, MONO, "middle", 600)
    d.arrow([(LX + LW, cy), (RX, cy)], c, m, 1.6 if c == ACC else 1.4)
    d.chip((LX + LW + RX) / 2, cy, name, c, 12, 8)
    d.tone(RX, y, RW, 48 if right2 is None else 56, OK if c != ACC else ACC)
    if right2 is None:
        d.t(RX + RW / 2, cy + 5, right, 12, INK, KR, "middle")
    else:
        d.t(RX + RW / 2, cy - 2, right, 12, INK, KR, "middle", 600)
        d.t(RX + RW / 2, cy + 18, right2, 12, MUTED, KR, "middle")

d.legend(H - 56, [("main 이 넘기는 쪽", INFO), ("새 스레드가 받는 쪽", OK), ("꺼내 쓰는 값", ACC)])
d.save("21-01.create-args.svg")
print("ok 21-01 create-args")
