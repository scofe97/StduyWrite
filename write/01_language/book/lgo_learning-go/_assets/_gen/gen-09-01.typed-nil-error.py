# 09-01.typed-nil-error — 사용자 정의 오류 타입의 변수를 error 로 돌려주면 타입 칸이 차서 nil 이 아니다
# 본문 요구(09-01 §4 「사용자 정의 오류 타입 변수를 그대로 돌려주면 nil 이 아닙니다」): GenerateErrorBroken(false) 는 초기화하지 않은
#           StatusErr 를 돌려주는데도 err != nil 이 true 다. *StatusErr 로 선언해도 같다. 07-03 §4 대로 인터페이스는 타입·값 두 칸이
#           모두 비어야 nil 이고, 성공이면 nil 을 직접 돌려줘야 두 칸이 빈다.
# 타입 스펙: type-nested — 07-03.iface-nil 과 같은 골격. 바깥 상자 = 돌아온 error 값 하나, 안쪽 = 타입 칸·값 칸 두 개. 세 상자를 좌우로.
#           stride: 상자 폭 288, 간격 24, 칸 높이 52. focal 은 값 타입 StatusErr 를 돌려준 왼쪽 상자 하나.
# 사실 출처: Learning Go 2판 9장 「Errors Are Values」 GenerateErrorBroken, go1.25.1 로컬 실행(2026-09-27) — true true,
#           포인터 판에 false 를 넘겨도 true.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER2, KR, MONO

W, H = 984, 460
BW, GAP, X0 = 288, 24, 36
BY, BH = 176, 196
CELL_H = 52

states = [  # 제목 코드, 타입 칸, 값 칸, 판정, 색, 설명
    ("var genErr StatusErr", "StatusErr", "StatusErr{}", "err != nil · true", ACC, "초기화 안 한 값을 그대로 반환"),
    ("var genErr *StatusErr", "*StatusErr", "nil", "err != nil · true", WARN, "포인터로 바꿔도 같음"),
    ("return nil", "nil", "nil", "err != nil · false", OK, "성공이면 nil 을 직접 반환"),
]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "NESTED · 09-01 §4",
      "오류 타입의 변수를 돌려주면 nil 이 아닙니다",
      "GenerateErrorBroken(false) 가 돌려준 error 값의 두 칸을 세 경우로 나란히 그렸다. StatusErr 변수를 그대로 돌려주면 값이 제로 값이어도 "
      "타입 칸에 StatusErr 가 들어가 nil 이 아니다. *StatusErr 로 선언해 nil 포인터를 돌려줘도 타입 칸이 차서 같다. "
      "성공일 때 nil 을 직접 돌려줘야 두 칸이 모두 비어 err != nil 이 false 가 된다.",
      lead="error 는 인터페이스라 타입 칸과 값 칸이 모두 비어야 nil 입니다(07-03 §4).")

for k, (code, typ, val, verdict, c, note) in enumerate(states):
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
    d.t(x + BW // 2, BY + BH - 16, note, 12, MUTED, kr(note), "middle")

d.legend(404, [("찬 칸", INFO), ("nil 과 같음", OK), ("nil 처럼 보이지만 아님", ACC)])
d.save("09-01.typed-nil-error.svg")
print("ok 09-01 typed-nil-error")
