# 21-01 「반환값이 스택에 있으면 join 이 받을 때 이미 사라진다」 — 같은 네 국면을 스택 변수(oops)와 heap 변수(Malloc)로 나란히 놓는다.
# 본문 근거: 이 노트 「2. join 으로 완료 기다리기」의 「스택 변수의 주소를 돌려주면 안 되는 이유」.
# 값 근거: 개념 도식이라 값은 없다. 변수 이름 oops·rvals 와 x=1, y=2 는 OSTEP 27장 코드에 있는 것이다.
# 공식 근거: OSTEP 27장 §27.2 — 스택에 할당한 변수의 포인터를 돌려주면 반환 때 자동 해제된 변수를 가리키게 된다. 그림 27.2 는 Malloc 한 myret_t 를 돌려주고 main 이 free 한다.
# 타입 스펙: type-state — 대상 하나(반환값 변수)가 국면을 차례로 지난다. 위 줄은 위험 경로(BAD), 아래 줄은 정상 경로(OK), 국면 이름과 번호가 두 줄에서 같다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER, PAPER2, OK, INFO, BAD, WARN, KR, MONO

W, H = 880, 456
d = D(W, H, "OSTEP · 21-01 §2",
      "반환값 변수가 어디에 있느냐가 join 뒤의 운명을 정한다",
      "위 줄은 mythread 의 스택에 둔 oops 의 주소를 돌려주는 경우로, 반환 때 프레임이 해제되어 main 은 해제된 자리를 읽는다. "
      "아래 줄은 Malloc 으로 heap 에 둔 rvals 를 돌려주는 경우로, 프레임이 해제돼도 값이 남아 main 이 읽고 free 한다.")

X0, BW, GAP = 24, 172, 48
phases_bad = [
    ("1 할당", "oops 는 mythread 의", "스택 프레임 안"),
    ("2 반환", "return &oops", "스택 주소를 돌려줌"),
    ("3 프레임 해제", "oops 의 자리가", "해제됨"),
    ("4 main 이 읽음", "해제된 자리를 가리키는", "포인터를 따라감"),
]
phases_ok = [
    ("1 할당", "Malloc 으로 heap 에", "myret_t 를 받음"),
    ("2 반환", "return rvals", "heap 주소를 돌려줌"),
    ("3 프레임 해제", "스택 프레임은 사라져도", "heap 값은 그대로"),
    ("4 main 이 읽음", "x=1, y=2 를 읽은 뒤", "free(rvals)"),
]


def row(y, title, phases, c, m, last_fill):
    d.t(24, y - 12, title, 13, c, KR, "start", 600)
    for i, (head, l1, l2) in enumerate(phases):
        x = X0 + i * (BW + GAP)
        last = i == len(phases) - 1
        col = last_fill if last else c
        d.tone(x, y, BW, 96, col)
        d.t(x + BW / 2, y + 26, head, 13, INK, KR, "middle", 600)
        d.line(x + 12, y + 38, x + BW - 12, y + 38, RULE, 0.6)
        d.t(x + BW / 2, y + 62, l1, 12, INK, KR, "middle")
        d.t(x + BW / 2, y + 82, l2, 12, MUTED, KR, "middle")
        if not last:
            d.arrow([(x + BW, y + 48), (x + BW + GAP, y + 48)], c, m, 1.4)


row(124, "스택 변수의 주소를 돌려줌 — 위험", phases_bad, WARN, "warn", BAD)
row(284, "heap 변수의 주소를 돌려줌 — 정상", phases_ok, INFO, "info", OK)

d.legend(H - 56, [("진행 국면", WARN), ("위험한 끝", BAD), ("정상 경로", INFO), ("정상 끝", OK)])
d.save("21-01.stack-return.svg")
print("ok 21-01 stack-return")
