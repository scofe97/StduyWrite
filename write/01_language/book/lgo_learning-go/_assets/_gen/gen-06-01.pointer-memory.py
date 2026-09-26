# 06-01.pointer-memory — 포인터는 가리키는 값의 주소를 값으로 담는다
# 본문 요구(06-01 §1 「포인터 — 다른 값이 놓인 주소를 담는 변수입니다」): 원문 그림 6-2 처럼 x(주소 1~4, 값 10)·
#           y(주소 5, 값 1) 뒤에 pointerX(6~9, 값 1)·pointerY(10~13, 값 5)·pointerZ(14~17, 값 0)가 놓이고,
#           포인터의 값이 곧 가리키는 변수의 시작 주소라는 관계를 한 줄의 메모리 칸 위에서 보인다.
# 타입 스펙: type-nested — 바깥 = 메모리 칸 한 줄(주소 1~17), 안쪽 = 변수 하나가 차지한 연속 칸 묶음.
#           03-02.string-bytes 와 같은 칸 방식. 포인터 → 대상은 직교 화살표(대각선 금지). 두 화살표의 구간 [1,6]·[5,10] 이 겹쳐,
#           같은 쪽으로 돌면 교차하므로 pointerX 는 칸 위, pointerY 는 칸 아래로 돈다.
#           stride: 칸 폭 48, 칸 사이 0, 레인은 묶음 테두리에서 위 40·아래 40. focal 은 pointerX → x 화살표 하나. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 6장 「A Quick Pointer Primer」 그림 6-1·6-2 의 설명 문단(4바이트 포인터 가정).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, PAPER2, KR, MONO

W, H = 984, 432
X0, CW, N = 84, 48, 17
BY, BH = 204, 72            # 변수 묶음 y · 높이
UP_Y, DOWN_Y = 152, 328     # pointerX 는 칸 위, pointerY 는 칸 아래 레인 — 두 구간이 겹쳐 같은 쪽이면 교차한다


def cx(addr):               # 주소 addr 칸의 왼쪽 x
    return X0 + (addr - 1) * CW


vars_ = [  # 이름, 타입, 시작 주소, 칸 수, 값, 색
    ("x", "int32", 1, 4, "10", INFO),
    ("y", "bool", 5, 1, "1", INFO),
    ("pointerX", "*int32", 6, 4, "1", OK),
    ("pointerY", "*bool", 10, 4, "5", OK),
    ("pointerZ", "*string", 14, 4, "0", SOFT),
]

d = D(W, H, "NESTED · 06-01 §1",
      "포인터는 가리키는 값의 주소를 담는다",
      "원문 그림 6-2 의 메모리 배치. x 는 주소 1~4 에 10, y 는 주소 5 에 1(true) 로 놓인다. "
      "pointerX 는 주소 6~9 에 값 1, pointerY 는 주소 10~13 에 값 5 를 담아 각각 x 와 y 의 시작 주소를 가리킨다. "
      "pointerZ 는 아무것도 가리키지 않아 값이 0(nil) 이다. 포인터는 가리키는 타입과 무관하게 모두 4칸이다.",
      lead="칸 위쪽 작은 숫자는 주소, 아래 큰 숫자는 저장된 값입니다. 원문처럼 4바이트 포인터를 가정합니다.")

# 바깥 — 메모리 칸 한 줄
d.box(X0 - 12, BY - 12, N * CW + 24, BH + 24, r=8)
for name, typ, a, n, val, c in vars_:
    x = cx(a)
    d.tone(x + 2, BY, n * CW - 4, BH, c, 4, "18", 1.2)
    for k in range(n):
        if k:
            d.line(x + k * CW, BY + 6, x + k * CW, BY + 22, c, 0.6)
        d.t(x + k * CW + CW // 2, BY + 16, str(a + k), 10, MUTED, MONO, "middle")
    label = name if n == 1 else f"{name} · {typ}"
    d.t(x + n * CW // 2, BY + 40, label, 11, c if c != SOFT else MUTED, MONO, "middle", 600)
    d.t(x + n * CW // 2, BY + 62, val, 16, INK, MONO, "middle", 600)

# 포인터 → 대상 (직교 화살표). pointerX 는 위, pointerY 는 아래로 돌아 서로 교차하지 않는다.
top, bot = BY - 12, BY + BH + 12
px, tx = cx(6) + 2 * CW, cx(1) + CW // 2
d.arrow([(px, top), (px, UP_Y), (tx, UP_Y), (tx, top - 2)], ACC, "acc", 1.6)
d.t(px + 8, UP_Y - 8, "pointerX 의 값 1 = x 의 주소", 12, ACC, KR, "start", 600)
py, ty = cx(10) + 2 * CW, cx(5) + CW // 2
d.arrow([(py, bot), (py, DOWN_Y), (ty, DOWN_Y), (ty, bot + 2)], OK, "ok", 1.6)
d.t(py + 8, DOWN_Y + 18, "pointerY 의 값 5 = y 의 주소", 12, OK, KR, "start")
d.t(cx(14) + 2 * CW, top - 12, "nil · 가리키는 곳 없음", 12, MUTED, KR, "middle")

d.legend(372, [("값 변수", INFO), ("포인터", OK), ("nil 포인터", SOFT), ("x 를 가리키는 화살표", ACC)])
d.save("06-01.pointer-memory.svg")
print("ok 06-01 pointer-memory")
