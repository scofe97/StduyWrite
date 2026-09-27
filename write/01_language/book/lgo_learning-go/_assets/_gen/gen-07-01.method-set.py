# 07-01.method-set — 인스턴스와 리시버 종류별로 메서드 집합에 드는가, 변수로 부를 수 있는가
# 본문 요구(07-01 §3 「메서드 집합은 포인터 인스턴스가 더 큽니다」·§4): 값 인스턴스의 메서드 집합에는 값 리시버만,
#           포인터 인스턴스에는 둘 다 든다. 그런데 값 변수로 포인터 리시버를 부르는 것은 자동 주소 변환(문법 편의)으로 된다.
#           nil 포인터로 값 리시버를 부르면 panic, nil 을 다루게 쓴 포인터 리시버는 불린다. "어느 조합이 되는가" 형태다.
# 타입 스펙: type-dp-security-matrix — 행 = 인스턴스 · 메서드 6개, 열 = 메서드 집합(인터페이스 대입) 1개와 변수로 호출 1개.
#           05-03.call-by-value 와 같은 조정 공식(comp_col 264 · row_h 44 · row_stride 52 · header_y 112 · role_col_w 280).
#           focal 은 두 열의 답이 갈리는 "값 Counter · Increment" 행 하나.
# 사실 출처: Learning Go 2판 7장 「Pointer Receivers and Value Receivers」·「Code Your Methods for nil Instances」·
#           「A Quick Lesson on Interfaces」, go1.25.1 실행(2026-09-27) — nil *Counter 의 String() panic, IntTree Contains true false,
#           Counter does not implement Incrementer (method Increment has pointer receiver).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, WARN, PAPER2, KR, MONO

LEFT, RIGHT = 12, 48
COMP_W, GAP_CR = 264, 12
ROLE_W, ROLE_GAP = 280, 16
HEADER_Y, HEADER_H = 112, 52
ROW_H, STRIDE = 44, 52
roles = ["메서드 집합에 드는가", "변수로 직접 부르면"]
rows = [  # 인스턴스, 메서드(리시버), (집합 판정, 색), (호출 판정, 색)
    ("Counter 값", "String · 값 리시버", ("든다", OK), ("불린다", OK)),
    ("Counter 값", "Increment · 포인터 리시버", ("안 든다", BAD), ("(&c) 로 자동 변환", OK)),
    ("*Counter", "String · 값 리시버", ("든다", OK), ("(*c) 로 자동 변환", OK)),
    ("*Counter", "Increment · 포인터 리시버", ("든다", OK), ("불린다", OK)),
    ("nil *Counter", "String · 값 리시버", ("든다", OK), ("panic", BAD)),
    ("nil *IntTree", "Contains · 포인터 리시버", ("든다", OK), ("불린다 · nil 을 다룸", WARN)),
]
FOCAL = 1
W = LEFT + COMP_W + GAP_CR + len(roles) * ROLE_W + (len(roles) - 1) * ROLE_GAP + RIGHT   # 912
row_y = lambda k: HEADER_Y + HEADER_H + 24 + k * STRIDE
role_x = lambda j: LEFT + COMP_W + GAP_CR + j * (ROLE_W + ROLE_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 20 + 48


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


d = D(W, H, "MATRIX · 07-01 §3",
      "메서드 집합과 직접 호출은 다르다",
      "값 인스턴스의 메서드 집합에는 값 리시버 메서드만, 포인터 인스턴스에는 두 리시버 메서드가 모두 든다. "
      "그런데 값 변수로 포인터 리시버 메서드를 부르면 Go 가 주소를 얻어 (&c) 로 바꿔 부르므로 호출은 된다. 이 자동 변환은 문법 편의라 메서드 집합을 바꾸지 않는다. "
      "nil 포인터로 값 리시버를 부르면 panic 이고, nil 을 다루게 쓴 포인터 리시버는 그대로 불린다.",
      lead="왼쪽 열은 인터페이스에 대입할 수 있는지, 오른쪽 열은 변수에서 점으로 부를 수 있는지입니다.")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H)
d.t(LEFT + COMP_W // 2, HEADER_Y + 22, "인스턴스 · 메서드", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W // 2, HEADER_Y + 40, "리시버 종류", 12, MUTED, KR, "middle")
for j, r in enumerate(roles):
    d.o.append(f'<rect x="{role_x(j)}" y="{HEADER_Y}" width="{ROLE_W}" height="{HEADER_H}" rx="6" fill="{INK}"/>')
    d.t(role_x(j) + ROLE_W // 2, HEADER_Y + 32, r, 14, "#0D1117", kr(r), "middle", 600)

for k, (inst, meth, (s_txt, s_c), (c_txt, c_c)) in enumerate(rows):
    y = row_y(k)
    focal = k == FOCAL
    if focal:
        d.tone(LEFT, y, COMP_W, ROW_H, ACC, 4, "14", 1.4)
    else:
        d.box(LEFT, y, COMP_W, ROW_H, r=4)
    d.t(LEFT + 16, y + 20, inst, 14, ACC if focal else INK, kr(inst), "start", 600)
    d.t(LEFT + 16, y + 37, meth, 12, MUTED, kr(meth), "start")
    for j, (txt, c) in enumerate(((s_txt, s_c), (c_txt, c_c))):
        d.tone(role_x(j), y, ROLE_W, ROW_H, c, 4, "18", 1.0)
        d.t(role_x(j) + ROLE_W // 2, y + 28, txt, 14, c, kr(txt), "middle", 600)

d.legend(bottom + 20, [("된다", OK), ("안 된다", BAD), ("조건부로 된다", WARN), ("두 열이 갈리는 행", ACC)])
d.save("07-01.method-set.svg")
print("ok 07-01 method-set", W, H)
