# 03-01.slice-share — 부분 slice 에 append 하면 원본을 덮어쓰고, 완전 slice 식은 새 배열로 떼어 낸다
# 본문 요구(03-01 §4 「부분 slice 에 append 하면 원본이 바뀝니다」): 예제 3-6 의 x·y 가 한 배열을 나눠 쓰다가
#           append 한 번에 x[2] 가 바뀌는 과정과, y := x[:2:2] 로 바꾸면 같은 append 가 새 배열을 만드는 과정을
#           같은 배열을 두 시점(append 전·후)으로 옮겨 그린다.
# 타입 스펙: type-state — 상태 = 뒷받침 배열의 스냅숏(둥근 사각 rx 8), 전이 = append 호출(mono 라벨).
#           흐름은 위→아래, 두 생애를 좌우 두 열로 나란히 둔다. coral 은 덮어쓴 칸이 있는 상태 하나.
#           stride: 열 중심 x 248·736, 칸 폭 64(간격 0), 상태 높이 176, 두 상태 사이 48. 모든 좌표 4 의 배수.
# 사실 출처: Learning Go 2판 3장 예제 3-6·3-8, go1.25.1 실행(2026-09-27) — x[:2:2] 에 "z" 를 append 하면
#           x 는 [a b c d] 그대로, y 는 [a b z] len 3 cap 4.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 604
SW, SH = 416, 176
COLS = (40, 528)                 # 상태 상자 왼쪽 x
TOP, GAP = 116, 64               # 위 상태 y, 두 상태 사이
CW, CH = 64, 36


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def state(x, y, title, c=None):
    stroke = c or "rgba(191,192,192,0.22)"
    fill = (c + "14") if c else PAPER2
    d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="{1.4 if c else 0.9}"/>')
    d.t(x + 20, y + 28, title, 14, c or INK, kr(title), "start", 600)


def cells(x, y, vals, hot=None, empty_from=None):
    for i, v in enumerate(vals):
        cx = x + i * CW
        if hot is not None and i == hot:
            d.tone(cx, y, CW, CH, BAD, 2, "22", 1.2)
            col = BAD
        elif empty_from is not None and i >= empty_from:
            d.box(cx, y, CW, CH, stroke="rgba(191,192,192,0.22)")
            col = SOFT
        else:
            d.box(cx, y, CW, CH)
            col = INK
        d.t(cx + CW // 2, y + 24, v, 14, col, MONO, "middle", 600)


def bracket(x0, x1, y, label, c, cap_to=None):
    d.line(x0 + 4, y, x1 - 4, y, c, 1.6)
    d.line(x0 + 4, y - 6, x0 + 4, y, c, 1.6)
    d.line(x1 - 4, y - 6, x1 - 4, y, c, 1.6)
    if cap_to:
        d.line(x1 - 4, y, cap_to - 4, y, c, 1.0, "4 4")
    d.t((cap_to or x1) + 8, y + 5, label, 12, c, kr(label), "start")


d = D(W, H, "STATE · 03-01 §4",
      "부분 slice 의 append 가 원본을 덮어쓰는 이유",
      "예제 3-6 의 두 가지 생애를 나란히 그린 상태도. 왼쪽은 y := x[:2] 로 잘라 y 의 용량이 x 와 같은 4 라서 "
      "append 한 값이 뒷받침 배열의 2번 칸, 곧 x[2] 에 들어간다. 오른쪽은 y := x[:2:2] 로 용량을 2 로 묶어, "
      "같은 append 가 새 배열을 만들고 x 는 그대로 남는다.",
      lead="위는 append 전, 아래는 append 후입니다. 점선은 len 을 넘어 cap 까지 닿는 구간입니다.")

vals = ["a", "b", "c", "d"]
bot = TOP + SH + GAP
for k, (title, title2) in enumerate((("y := x[:2]", "y = append(y, \"z\")"),
                                     ("y := x[:2:2]", "y = append(y, \"z\")"))):
    X = COLS[k]
    ax = X + 24
    # 위 상태 — append 전
    state(X, TOP, title)
    cells(ax, TOP + 48, vals)
    bracket(ax, ax + 4 * CW, TOP + 104, "x · len 4 cap 4", INFO)
    if k == 0:
        bracket(ax, ax + 2 * CW, TOP + 140, "y · len 2 cap 4", OK, cap_to=ax + 4 * CW)
    else:
        bracket(ax, ax + 2 * CW, TOP + 140, "y · len 2 cap 2", OK)
    # 전이
    mx = X + SW // 2
    d.arrow([(mx, TOP + SH), (mx, bot)], SOFT, "soft", 1.2)
    d.t(mx + 12, TOP + SH + 38, title2, 13, MUTED, MONO, "start")
    # 아래 상태 — append 후
    if k == 0:
        state(X, bot, "같은 배열 · x[2] 덮어씀", ACC)
        cells(ax, bot + 48, ["a", "b", "z", "d"], hot=2)
        bracket(ax, ax + 4 * CW, bot + 104, "x → [a b z d]", INFO)
        bracket(ax, ax + 3 * CW, bot + 140, "y · len 3 cap 4", OK, cap_to=ax + 4 * CW)
    else:
        state(X, bot, "새 배열 · x 그대로")
        cells(ax, bot + 48, vals)
        d.t(ax + 4 * CW + 12, bot + 72, "x → [a b c d]", 12, INFO, MONO, "start")
        cells(ax, bot + 100, ["a", "b", "z", ""], empty_from=3)
        d.t(ax + 4 * CW + 12, bot + 124, "y · len 3 cap 4", 12, OK, MONO, "start")

d.legend(548, [("x", INFO), ("y", OK), ("덮어쓴 칸", BAD), ("원본이 바뀐 상태", ACC)])
d.save("03-01.slice-share.svg")
print("ok 03-01 slice-share")
