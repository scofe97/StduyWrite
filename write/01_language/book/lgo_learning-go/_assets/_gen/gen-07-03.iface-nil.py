# 07-03.iface-nil — 인터페이스 값은 타입 칸과 값 칸 두 개이고, 둘 다 비어야 nil 이다
# 본문 요구(07-03 §4 「인터페이스와 nil」): 원문은 인터페이스를 타입·값 두 포인터 필드의 struct 로 설명한다.
#           var incrementer Incrementer 는 두 칸이 비어 nil, nil 인 *Counter 를 대입하면 타입 칸이 차서 nil 이 아니다.
#           값이 있는 *Counter 를 대입한 경우까지 세 상태를 나란히 두어 "== nil" 이 무엇을 보는지 드러낸다.
# 타입 스펙: type-nested — 바깥 상자 = 인터페이스 값 하나, 안쪽 = 타입 칸·값 칸 두 개. 세 상자를 좌우로 나란히 둔다.
#           stride: 상자 폭 288, 간격 24, 칸 높이 52. focal 은 타입만 찬 가운데 상자 하나. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 7장 「Interfaces and nil」, go1.25.1 실행(2026-09-27) — true true false,
#           reflect.ValueOf(incrementer).IsNil() true.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 460
BW, GAP, X0 = 288, 24, 36
BY, BH = 176, 196
CELL_H = 52

states = [  # 제목 코드, 타입 칸, 값 칸, 판정, 색, 메서드 호출
    ("var incrementer Incrementer", "nil", "nil", "== nil · true", OK, "메서드 호출 → panic"),
    ("incrementer = pointerCounter", "*Counter", "nil", "== nil · false", ACC, "메서드는 불림 · nil 처리는 메서드 몫"),
    ("incrementer = &Counter{}", "*Counter", "→ Counter{...}", "== nil · false", INFO, "메서드 호출 가능"),
]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NESTED · 07-03 §4",
      "인터페이스 값은 타입과 값 두 칸이다",
      "인터페이스 변수 하나가 담는 두 칸을 세 상태로 나란히 그렸다. 선언만 한 인터페이스는 타입 칸과 값 칸이 모두 비어 nil 과 같다. "
      "nil 인 *Counter 를 대입하면 값 칸은 비어도 타입 칸에 *Counter 가 들어가 nil 과 같지 않다. 값이 있는 *Counter 를 대입하면 두 칸이 모두 찬다.",
      lead="== nil 은 두 칸이 모두 비었는지를 봅니다. 오른쪽 상자는 원문에 없는, 노트가 더한 비교용 상태입니다.")

for k, (code, typ, val, verdict, c, call) in enumerate(states):
    x = X0 + k * (BW + GAP)
    focal = c == ACC
    if focal:
        d.tone(x, BY, BW, BH, ACC, 8, "10", 1.4)
    else:
        d.box(x, BY, BW, BH, r=8)
    d.t(x + BW // 2, BY - 16, code, 12, ACC if focal else INK, MONO, "middle", 600)
    for j, (lab, v) in enumerate((("타입", typ), ("값", val))):
        cy = BY + 20 + j * (CELL_H + 12)
        filled = v != "nil"
        if filled:
            d.tone(x + 20, cy, BW - 40, CELL_H, INFO, 4, "18", 1.0)
        else:
            d.box(x + 20, cy, BW - 40, CELL_H, r=4)
        d.t(x + 36, cy + 32, lab, 12, MUTED, KR, "start")
        d.t(x + BW - 36, cy + 33, v, 14, INK if filled else SOFT, kr(v), "end", 600)
    d.t(x + BW // 2, BY + BH - 40, verdict, 15, c, MONO, "middle", 600)
    d.t(x + BW // 2, BY + BH - 16, call, 12, MUTED, kr(call), "middle")

d.legend(404, [("찬 칸", INFO), ("nil 과 같음", OK), ("nil 처럼 보이지만 아님", ACC)])
d.save("07-03.iface-nil.svg")
print("ok 07-03 iface-nil")
