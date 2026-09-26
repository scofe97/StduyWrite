# 06-02.slice-header — 함수에 넘긴 slice 는 길이·용량·포인터 헤더만 복사된다
# 본문 요구(06-02 §3 「slice 는 헤더가 복사되어 길이 변경이 보이지 않습니다」): 원문 그림 6-6~6-9 의 세 경우를
#           노트 예제(s := make([]int, 3, 4))의 값으로 옮긴다. 원소 변경은 함께 쓰는 배열이라 보이고, 용량 안 append 는
#           배열에 값이 들어가도 main 의 len 밖이라 안 보이며, 용량 밖 append 는 새 배열이라 그 뒤 변경도 안 보인다.
# 타입 스펙: type-state — 상태 = 함수 호출 하나가 끝나기 직전의 배열 스냅숏(둥근 사각 rx 8), 전이 = 다음 호출.
#           03-01.slice-share 와 같은 칸·괄호 방식. main 의 len·cap 은 칸 위 괄호(info), 함수 안 사본은 칸 아래 괄호(ok).
#           stride: 칸 폭 64(간격 0), 왼쪽 설명 열 폭 280, 스냅숏 사이 32. focal(coral)은 결과가 갈리는 appendIn 하나.
# 사실 출처: Learning Go 2판 6장 「The Difference Between Maps and Slices」 그림 6-5~6-9 설명,
#           go1.25.1 실행(2026-09-27) — after modify [10 2 3] 3 4 · in appendIn [10 2 3 4] 4 4 · s[:4] [10 2 3 4] ·
#           in appendOut [99 2 3 4 5] 5 8 · after appendOut [10 2 3] 3 4.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER2, KR, MONO

W, H = 984, 700
SX, SW = 24, 924            # 스냅숏 상자
AX = SX + 312               # 배열 첫 칸 x
CW, CH = 64, 36
GAP = 32
SNAPS = [  # 제목, 한 일, 결과, 높이, focal
    ("1. modify(s)", "s[0] = 10", "원소 변경 · main 에 보임", 124, None),
    ("2. appendIn(s)", "s = append(s, 4)", "len 4 는 사본만 · 4 는 안 보임", 124, ACC),
    ("3. appendOut(s)", "append(s, 4, 5) · s[0] = 99", "새 배열 · 99 도 안 보임", 196, None),
]


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def cells(x, y, vals, hot=None, hot_c=OK):
    for i, v in enumerate(vals):
        cx = x + i * CW
        if i == hot:
            d.tone(cx, y, CW, CH, hot_c, 2, "22", 1.2)
            col = hot_c
        elif v == "":
            d.box(cx, y, CW, CH)
            col = SOFT
        else:
            d.box(cx, y, CW, CH)
            col = INK
        d.t(cx + CW // 2, y + 24, v, 14, col, MONO, "middle", 600)


def bracket(n_len, n_cap, y, label, c, up):
    x0, x1, xc = AX, AX + n_len * CW, AX + n_cap * CW
    tick = 6 if up else -6
    d.line(x0 + 4, y, x1 - 4, y, c, 1.6)
    d.line(x0 + 4, y, x0 + 4, y + tick, c, 1.6)
    d.line(x1 - 4, y, x1 - 4, y + tick, c, 1.6)
    if n_cap > n_len:
        d.line(x1 - 4, y, xc - 4, y, c, 1.0, "4 4")
    if n_cap > 4:            # 8칸 배열은 오른쪽 여백이 없어 라벨을 괄호 아래 왼쪽에 둔다
        d.t(x0 + 4, y + 22, label, 12, c, kr(label), "start")
    else:
        d.t(xc + 8, y + 5, label, 12, c, kr(label), "start")


d = D(W, H, "STATE · 06-02 §3",
      "함수에 넘긴 slice 는 헤더만 복사된다",
      "s := make([]int, 3, 4) 를 세 함수에 차례로 넘긴 상태도. slice 는 길이·용량·포인터 세 필드라 함수에는 이 헤더의 사본이 간다. "
      "modify 의 원소 변경은 같은 배열이라 main 에 보인다. appendIn 은 용량 안이라 4 가 같은 배열에 들어가지만 main 의 len 은 3 이라 보이지 않는다. "
      "appendOut 은 용량을 넘어 새 배열(cap 8)을 만들므로 그 뒤 s[0] = 99 도 main 에 보이지 않는다.",
      lead="칸 위 괄호는 main 의 s, 칸 아래 괄호는 함수 안 사본입니다. 점선은 len 을 넘어 cap 까지 닿는 구간입니다.")

y = 104
for k, (title, act, result, h, focal) in enumerate(SNAPS):
    if focal:
        d.tone(SX, y, SW, h, focal, 8, "10", 1.4)
    else:
        d.box(SX, y, SW, h, r=8)
    d.t(SX + 20, y + 30, title, 14, focal or INK, MONO, "start", 600)
    d.t(SX + 20, y + 52, act, 12, MUTED, MONO, "start")
    d.t(SX + 20, y + 76, result, 12, focal or MUTED, KR, "start", 600 if focal else 400)
    top = y + 48
    if k == 0:
        bracket(3, 4, top - 12, "main · len 3 cap 4", INFO, True)
        cells(AX, top, ["10", "2", "3", ""], hot=0)
        bracket(3, 4, top + CH + 12, "사본 · len 3 cap 4", OK, False)
    elif k == 1:
        bracket(3, 4, top - 12, "main · len 3 cap 4", INFO, True)
        cells(AX, top, ["10", "2", "3", "4"], hot=3, hot_c=ACC)
        bracket(4, 4, top + CH + 12, "사본 · len 4 cap 4", OK, False)
    else:
        bracket(3, 4, top - 12, "main · len 3 cap 4 · 옛 배열", INFO, True)
        cells(AX, top, ["10", "2", "3", "4"])
        top2 = top + CH + 24
        cells(AX, top2, ["99", "2", "3", "4", "5", "", "", ""], hot=0, hot_c=BAD)
        bracket(5, 8, top2 + CH + 12, "사본 · len 5 cap 8 · 새 배열", OK, False)
    if k < len(SNAPS) - 1:
        d.arrow([(SX + 140, y + h), (SX + 140, y + h + GAP)], SOFT, "soft", 1.2)
    y += h + GAP

d.legend(y - GAP + 24, [("main 의 s", INFO), ("함수 안 사본", OK), ("main 에 안 보이는 값", ACC), ("새 배열의 변경", BAD)])
d.save("06-02.slice-header.svg")
print("ok 06-02 slice-header")
