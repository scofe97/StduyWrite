# 08-01.where-caught — 섞인 타입을 인터페이스 트리는 실행 중에, 제네릭은 컴파일 시점에 잡는다
# 본문 요구(08-01 §1 「인터페이스로 만든 트리는 섞인 타입을 막지 못합니다」·§2): Orderable 트리에 OrderableString 을 넣는
#           코드는 컴파일되고 실행 중 panic 이 난다. Stack[int] 에 "nope" 를 넣는 코드는 컴파일 오류다. 같은 실수가 어느 단계에서
#           잡히는지가 논지다.
# 타입 스펙: type-process — lanes(인터페이스+any · 타입 매개변수) × steps(코드 · 컴파일 · 실행). 칸 사이는 수평 화살표.
#           stride: 단계 열 x 236·476·716, 칸 폭 200, 레인 높이 88, 레인 사이 24. focal 은 제네릭이 컴파일에서 잡는 칸 하나.
# 사실 출처: Learning Go 2판 8장 「Generics Reduce Repetitive Code…」·「Introducing Generics in Go」, go1.25.1 실행(2026-09-27) —
#           interface {} is main.OrderableInt, not string · cannot use "nope" (untyped string constant) as int value.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, PAPER2, KR, MONO

W, H = 984, 420
LX, LW = 24, 196
COLS = [236, 476, 716]
CW = 200
LANE_Y = [148, 260]
LH = 88
STEPS = ["코드", "컴파일", "실행"]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "PROCESS · 08-01 §1",
      "섞인 타입을 어디서 잡는가",
      "같은 실수, 곧 다른 타입의 값을 한 자료구조에 넣는 코드가 어느 단계에서 잡히는지 두 방식으로 비교한다. "
      "any 를 받는 Orderable 트리는 OrderableString 을 넣는 코드를 컴파일러가 통과시키고 실행 중 타입 단언에서 panic 이 난다. "
      "타입 매개변수를 쓴 Stack[int] 는 Push(\"nope\") 를 컴파일 오류로 막아 실행까지 가지 않는다.",
      lead="위 레인은 제네릭 이전의 인터페이스 방식, 아래 레인은 타입 매개변수 방식입니다.")

for j, s in enumerate(STEPS):
    d.t(COLS[j] + CW // 2, 132, s, 13, MUTED, KR, "middle", 600)

rows = [
    ("인터페이스 + any", "Orderable 트리",
     [("Insert(OrderableString)", None), ("통과", WARN), ("panic", BAD)],
     ["OrderableInt 가 든 트리", "타입을 모름", "interface conversion"]),
    ("타입 매개변수", "Stack[int]",
     [("Push(\"nope\")", None), ("컴파일 오류", ACC), ("실행하지 않음", SOFT)],
     ["", "untyped string constant", ""]),
]
for i, (title, sub, cells, notes) in enumerate(rows):
    y = LANE_Y[i]
    d.box(LX, y, LW, LH)
    d.t(LX + LW // 2, y + 38, title, 14, INK, KR, "middle", 600)
    d.t(LX + LW // 2, y + 60, sub, 12, MUTED, MONO, "middle")
    for j, (txt, c) in enumerate(cells):
        x = COLS[j]
        if c is None:
            d.box(x, y, CW, LH)
            col = INK
        else:
            d.tone(x, y, CW, LH, c, 6, "22" if c == ACC else "14", 1.4 if c == ACC else 1.0)
            col = c if c != SOFT else MUTED
        d.t(x + CW // 2, y + 40, txt, 14, col, kr(txt), "middle", 600)
        if notes[j]:
            d.t(x + CW // 2, y + 62, notes[j], 11, MUTED, kr(notes[j]), "middle")
        if j < 2:
            d.arrow([(x + CW, y + LH // 2), (COLS[j + 1] - 2, y + LH // 2)], SOFT, "soft", 1.2)

d.legend(368, [("통과시킴", WARN), ("실행 중 실패", BAD), ("컴파일 시점에 잡음", ACC)])
d.save("08-01.where-caught.svg")
print("ok 08-01 where-caught")
