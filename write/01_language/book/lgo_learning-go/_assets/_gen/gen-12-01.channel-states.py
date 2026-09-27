# 12-01.channel-states — 채널 상태 여섯 가지에서 읽기·쓰기·닫기가 하는 일
# 본문 요구(12-01 §3 「채널의 상태별 동작」): 원문 표 12-1 을 이 노트의 go1.25.1 에서 여섯 상태로 나눠 직접 확인한 것.
#           원문의 "버퍼 있음·열림" 열은 버퍼가 빈 경우와 찬 경우로 나눴다.
# 타입 스펙: type-dp-security-matrix — 행 = 동작(읽기·쓰기·닫기), 열 = 채널 상태 여섯. §2 공식을 따르되 열이 여섯이라
#           폭 상한 1000 안에 넣으려고 comp_col_w 208 → 88, role_col_w 148 → 130, role_col_gap 16 → 8 로 줄였고,
#           한글 13px 하한 때문에 row_h 36 → 52, row_stride 40 → 60 으로 키웠다. level 은 값 돌려줌·동작(OK) · 상대를 기다림(INFO)
#           · 영원히 멈춤(WARN) · panic(BAD) 넷.
# 사실 출처: Learning Go 2판 12장 표 12-1 「How channels behave」, go1.25.1 로컬 실행 — 각 동작을 고루틴에서 돌려 100ms 안에 끝나는지,
#           recover 로 panic 인지 확인(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, BAD, PAPER, KR, MONO

LP, RP, COMP_W, GAP0, ROLE_W, GAP = 12, 48, 88, 12, 130, 8
HEAD_Y, HEAD_H, ROW_H, ROW_S = 96, 52, 52, 60
states = [("버퍼 없음", "열림"), ("버퍼 없음", "닫힘"), ("버퍼 있음", "열림 · 빔"),
          ("버퍼 있음", "열림 · 가득"), ("버퍼 있음", "닫힘 · 값 남음"), ("nil", "제로 값")]
ops = ["읽기", "쓰기", "닫기"]
cells = [
    [("상대가 쓸 때까지", "wait"), ("제로 값 · false", "ok"), ("쓸 때까지", "wait"), ("값을 읽음", "ok"), ("남은 값 · true", "ok"), ("영원히 멈춤", "hang")],
    [("상대가 읽을 때까지", "wait"), ("PANIC", "bad"), ("버퍼에 넣음", "ok"), ("읽을 때까지", "wait"), ("PANIC", "bad"), ("영원히 멈춤", "hang")],
    [("닫힘", "ok"), ("PANIC", "bad"), ("닫힘", "ok"), ("닫힘 · 값 남음", "ok"), ("PANIC", "bad"), ("PANIC", "bad")],
]
N = len(states)
W = LP + COMP_W + GAP0 + N * ROLE_W + (N - 1) * GAP + RP
ROW0 = HEAD_Y + HEAD_H + 16
rows_bottom = ROW0 + (len(ops) - 1) * ROW_S + ROW_H
LEG = rows_bottom + 24
H = LEG + 44
TONE = {"ok": OK, "wait": INFO, "hang": WARN, "bad": BAD}


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def rx(j):
    return LP + COMP_W + GAP0 + j * (ROLE_W + GAP)


def ry(k):
    return ROW0 + k * ROW_S


d = D(W, H, "MATRIX · 12-01 §3",
      "채널 상태마다 읽기·쓰기·닫기가 하는 일",
      "원문 표 12-1 을 go1.25.1 에서 여섯 상태로 나눠 확인한 결과. 버퍼 없는 열린 채널은 읽기·쓰기 모두 상대 고루틴을 기다린다. "
      "닫힌 채널은 읽으면 남은 값을, 다 비면 제로 값과 false 를 돌려주고, 쓰거나 다시 닫으면 panic 이다. "
      "버퍼 있는 열린 채널은 비었을 때 읽기가, 가득 찼을 때 쓰기가 기다린다. nil 채널은 읽기·쓰기가 영원히 멈추고 닫으면 panic 이다.",
      lead="행은 동작, 열은 채널 상태입니다. 원문 표의 버퍼 있음·열림 열을 빔과 가득으로 나눴습니다.")

d.box(LP, HEAD_Y, COMP_W, HEAD_H)
d.t(LP + COMP_W / 2, HEAD_Y + 31, "동작", 13, INK, KR, "middle", 600)
for j, (a, b) in enumerate(states):
    d.tone(rx(j), HEAD_Y, ROLE_W, HEAD_H, INFO, 6, "22", 1.0)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 23, a, 13, INK, kr(a), "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 41, b, 11, MUTED, kr(b), "middle")

for k, op in enumerate(ops):
    d.box(LP, ry(k), COMP_W, ROW_H, r=4)
    d.t(LP + COMP_W / 2, ry(k) + 31, op, 13, INK, KR, "middle", 600)
    for j, (val, lv) in enumerate(cells[k]):
        c = TONE[lv]
        d.tone(rx(j), ry(k), ROLE_W, ROW_H, c, 4, "16", 0.9)
        d.t(rx(j) + ROLE_W / 2, ry(k) + 31, val, 12, c, kr(val), "middle", 600)

d.legend(LEG, [("값을 돌려줌 · 동작함", OK), ("상대를 기다림", INFO), ("영원히 멈춤", WARN), ("panic", BAD)])
d.save("12-01.channel-states.svg")
print("ok 12-01 states", W, H)
