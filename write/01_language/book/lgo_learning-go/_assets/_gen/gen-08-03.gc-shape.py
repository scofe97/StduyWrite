# 08-03.gc-shape — Go 컴파일러는 구체 타입마다가 아니라 바탕 타입마다 함수를 만들고 포인터는 함수 하나를 나눠 쓴다
# 본문 요구(08-03 §2 「Go 는 바탕 타입마다 함수를 만들고 포인터는 함수 하나를 나눠 씁니다」): 원문은 Vicent Marti 를 인용해
#           현재 컴파일러가 서로 다른 바탕 타입에만 고유 함수를 만들고, 모든 포인터 타입이 만들어진 함수 하나를 함께 쓰며,
#           구별을 위해 실행 중 조회를 더한다고 말한다. 호출(타입 인자) → 만들어진 함수의 다대일 대응이 논지다.
# 타입 스펙: type-architecture — 왼쪽 열 = 타입 인자별 호출 5개, 오른쪽 열 = 만들어진 함수 3개, 간선 = "이 함수를 쓴다".
#           직교 화살표만(수평 → 세로 합류 → 수평). stride: 호출 칸 높이 44·간격 16, 함수 칸은 합류하는 호출들의 세로 중앙.
#           focal 은 포인터 타입들이 함께 쓰는 함수 하나(실행 중 조회가 더해지는 곳).
# 사실 출처: Learning Go 2판 8장 「Idiomatic Go and Generics」(원문이 소개한 Vicent Marti 의 설명). 타입 이름 MyInt·*Adult·*Child 는
#           노트가 예로 고른 것이다.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 984, 540
CX, CWD, CH, CG = 36, 280, 44, 16
FX, FW = 620, 324
calls = ["f[int]", "f[MyInt]", "f[string]", "f[*Adult]", "f[*Child]"]
groups = [  # 함수 제목, 부제, 호출 인덱스, 색
    ("바탕 타입 int 용 함수", "int · MyInt 가 함께 씀", [0, 1], INFO),
    ("바탕 타입 string 용 함수", "string", [2], INFO),
    ("포인터 모양 함수 하나", "모든 포인터 타입이 함께 씀", [3, 4], ACC),
]
Y0 = 136
cy = lambda i: Y0 + i * (CH + CG) + (CG if i >= 2 else 0) + (CG if i >= 3 else 0)


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "ARCHITECTURE · 08-03 §2",
      "Go 는 바탕 타입마다 함수를 만든다",
      "제네릭 함수 f 를 다섯 가지 타입 인자로 불렀을 때 컴파일러가 만드는 함수의 대응. 바탕 타입이 같은 int 와 MyInt 는 함수 하나를 함께 쓰고, "
      "string 은 따로 하나를 받는다. 포인터 타입 *Adult 와 *Child 는 모두 포인터 모양 함수 하나를 함께 쓴다. 함수를 함께 쓰는 타입들을 구별하려고 컴파일러가 실행 중 조회를 더한다. "
      "구체 타입마다 함수를 만드는 C++ 과 다른 점이며, 원문은 이것을 제네릭 호출이 느려지는 원인으로 든다.",
      lead="함께 쓰는 함수에는 타입을 구별하는 실행 중 조회가 붙습니다. 타입 이름은 노트가 고른 예입니다.")

for i, c in enumerate(calls):
    y = cy(i)
    d.box(CX, y, CWD, CH)
    d.t(CX + 20, y + 28, c, 14, INK, MONO, "start", 600)

for title, sub, idx, c in groups:
    ys = [cy(i) + CH // 2 for i in idx]
    top, bot = min(ys), max(ys)
    fy = (top + bot) // 2 - 32
    fh = 64
    focal = c == ACC
    d.tone(FX, fy, FW, fh, c, 6, "22" if focal else "14", 1.4 if focal else 1.0)
    d.t(FX + 20, fy + 27, title, 14, c, KR, "start", 600)
    d.t(FX + 20, fy + 48, sub, 12, MUTED, kr(sub), "start")
    mx = CX + CWD + 72
    for y in ys:
        d.line(CX + CWD, y, mx, y, SOFT, 1.2)
    if len(ys) > 1:
        d.line(mx, top, mx, bot, SOFT, 1.2)
    d.arrow([(mx, fy + fh // 2), (FX - 2, fy + fh // 2)], SOFT, "soft", 1.2)

d.legend(484, [("바탕 타입별 함수", INFO), ("포인터가 함께 쓰는 함수", ACC)])
d.save("08-03.gc-shape.svg")
print("ok 08-03 gc-shape")
