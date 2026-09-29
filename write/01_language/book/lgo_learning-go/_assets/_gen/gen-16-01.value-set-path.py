# 16-01.value-set-path — 포인터를 ValueOf 에 넘기고 Elem 으로 가야 SetInt 가 원래 변수를 바꾸고, 값을 그대로 넘기면 SetInt 가 패닉을 낸다
# 본문 요구(16-01 §2 「값을 바꾸려면 포인터를 넘기고 Elem 에서 Set 합니다」): i := 10 → reflect.ValueOf(&i)(종류 ptr) → Elem()(종류 int, CanSet true)
#           → SetInt(20) → i == 20. 아랫줄은 reflect.ValueOf(i) 가 CanSet false 라 SetInt 가 unaddressable 패닉을 내는 길.
# 타입 스펙: type-flowchart — 두 줄, 윗줄 왼→오른 넷(성공 길), 아랫줄 셋(패닉 길). 노드 200×60, 가로 stride 236. focal 은 Elem() 노드 하나.
# 사실 출처: Learning Go 2판 16장 「Values」, go1.27.1 실행(2026-09-29) — CanSet false/true, reflect.Value.SetInt using unaddressable value, i = 20.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 984, 440
NW, NH, ST = 200, 60, 236
X = [28 + i * ST for i in range(4)]
Y1, Y2 = 140, 284


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def node(x, y, title, sub, c=None):
    if c:
        d.tone(x, y, NW, NH, c, 6, "18" if c == ACC else "12", 1.4 if c == ACC else 1.1)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW / 2, y + 26, title, 13, c or INK, kr(title), "middle", 600)
    d.t(x + NW / 2, y + 46, sub, 11, MUTED, kr(sub), "middle")


d = D(W, H, "FLOWCHART · 16-01 §2",
      "포인터를 넘겨 Elem 으로 가야 값을 바꿀 수 있습니다",
      "윗줄은 성공하는 길이다. 변수 i 의 포인터를 reflect.ValueOf 에 넘기면 종류가 ptr 인 값을 얻고, Elem 으로 가리키는 값에 가면 종류 int 에 CanSet 이 true 다. "
      "SetInt(20) 을 부르면 원래 변수 i 가 20 이 된다. 아랫줄은 i 를 그대로 넘긴 길로, 얻은 값은 CanSet 이 false 이고 SetInt 는 unaddressable value 패닉을 낸다.",
      lead="윗줄은 포인터를 넘긴 길, 아랫줄은 값을 그대로 넘긴 길입니다.")

d.t(28, 126, "포인터를 넘기면", 12, OK, KR, "start", 600)
node(X[0], Y1, "reflect.ValueOf(&i)", "Kind() == ptr")
node(X[1], Y1, ".Elem()", "Kind() == int · CanSet true", ACC)
node(X[2], Y1, ".SetInt(20)", "가리키는 값을 바꿈", INFO)
node(X[3], Y1, "i == 20", "원래 변수가 바뀜", OK)
for i in range(3):
    d.arrow([(X[i] + NW + 2, Y1 + NH / 2), (X[i + 1] - 4, Y1 + NH / 2)], SOFT, "soft", 1.3)

d.t(28, 270, "값을 그대로 넘기면", 12, BAD, KR, "start", 600)
node(X[0], Y2, "reflect.ValueOf(i)", "사본의 값")
node(X[1], Y2, "CanSet() == false", "주소를 쓸 수 없음", WARN)
node(X[2], Y2, ".SetInt(20)", "panic: unaddressable", BAD)
for i in range(2):
    d.arrow([(X[i] + NW + 2, Y2 + NH / 2), (X[i + 1] - 4, Y2 + NH / 2)], SOFT, "soft", 1.3)

d.legend(384, [("Elem 으로 간 값", ACC), ("바꾸기", INFO), ("결과", OK), ("막힘", WARN), ("패닉", BAD)])
d.save("16-01.value-set-path.svg")
print("ok 16-01 value-set-path")
