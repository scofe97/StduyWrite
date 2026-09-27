# 10-03.mvs — 최소 버전 선택: go-isatty 요구 v0.0.14·v0.0.12 가운데 모두를 만족하는 가장 낮은 v0.0.14 를 고른다
# 본문 요구(10-03 §2 「최소 버전 선택 — 요구를 만족하는 가장 낮은 버전」): money 는 fatih/color 와 go-colorable 에 기대고,
#           둘은 go-isatty 의 v0.0.14 와 v0.0.12 를 요구한다. Go 는 v0.0.14 를 고르며 최신 v0.0.24 는 고르지 않는다.
# 타입 스펙: type-architecture — 왼→오른 의존 그래프. 열 = 내 모듈 · 직접/간접 의존 · 요구 버전 · 고른 버전.
#           직교 화살표만. stride: 열 x 36·276·516·756, 노드 폭 200. focal 은 고른 버전 노드 하나.
# 사실 출처: Learning Go 2판 10장 「Minimal Version Selection」, go1.25.1 go mod graph·go list -m all(2026-09-27) —
#           color@v1.13.0 → isatty@v0.0.14, colorable@v0.1.9 → isatty@v0.0.12, 선택 v0.0.14, 최신 v0.0.24.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 460
COLS = [36, 276, 516, 756]
NW, NH = 200, 56
Y1, Y2 = 148, 276
YM = (Y1 + Y2) // 2


def node(x, y, title, sub, c=None, focal=False):
    if c:
        d.tone(x, y, NW, NH, c, 6, "22" if focal else "14", 1.4 if focal else 1.0)
    else:
        d.box(x, y, NW, NH)
    d.t(x + NW // 2, y + 24, title, 13, c or INK, MONO, "middle", 600)
    d.t(x + NW // 2, y + 44, sub, 11, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO, "middle")


d = D(W, H, "ARCHITECTURE · 10-03 §2",
      "최소 버전 선택이 go-isatty 를 고르는 모습",
      "money 는 fatih/color v1.13.0 과 go-colorable v0.1.9 에 기댄다. color 는 go-isatty v0.0.14 를, colorable 은 v0.0.12 를 요구한다. "
      "Go 는 두 요구를 모두 만족하는 가장 낮은 버전인 v0.0.14 를 고르고, 그보다 새 최신 v0.0.24 는 누구도 요구하지 않았으니 쓰지 않는다.",
      lead="화살표는 '이 버전 이상을 요구한다'입니다. 고른 버전은 요구들의 최댓값이자 가장 낮은 만족 버전입니다.")

node(COLS[0], YM, "money", "내 모듈")
node(COLS[1], Y1, "fatih/color", "v1.13.0")
node(COLS[1], Y2, "go-colorable", "v0.1.9")
node(COLS[2], Y1, "isatty ≥ v0.0.14", "color 의 요구", INFO)
node(COLS[2], Y2, "isatty ≥ v0.0.12", "colorable 의 요구", INFO)
node(COLS[3], YM, "go-isatty v0.0.14", "고른 버전", ACC, focal=True)
node(COLS[3], YM + 120, "v0.0.24", "최신 · 쓰지 않음", SOFT)

mx = COLS[0] + NW + 20
d.line(COLS[0] + NW, YM + NH // 2, mx, YM + NH // 2, SOFT, 1.2)
d.line(mx, Y1 + NH // 2, mx, Y2 + NH // 2, SOFT, 1.2)
for y in (Y1, Y2):
    d.arrow([(mx, y + NH // 2), (COLS[1] - 2, y + NH // 2)], SOFT, "soft", 1.2)
    d.arrow([(COLS[1] + NW, y + NH // 2), (COLS[2] - 2, y + NH // 2)], SOFT, "soft", 1.2)
jx = COLS[2] + NW + 20
d.line(COLS[2] + NW, Y1 + NH // 2, jx, Y1 + NH // 2, SOFT, 1.2)
d.line(COLS[2] + NW, Y2 + NH // 2, jx, Y2 + NH // 2, SOFT, 1.2)
d.line(jx, Y1 + NH // 2, jx, Y2 + NH // 2, SOFT, 1.2)
d.arrow([(jx, YM + NH // 2), (COLS[3] - 2, YM + NH // 2)], ACC, "acc", 1.4)

d.legend(404, [("요구 버전", INFO), ("최소 버전 선택의 결과", ACC), ("요구되지 않은 최신", SOFT)])
d.save("10-03.mvs.svg")
print("ok 10-03 mvs")
