# 13-02.reference-time — 기준 시각 2006-01-02 15:04:05 -0700 의 각 자리는 1부터 7까지의 수다
# 본문 요구(13-02 §2 「기준 시각으로 형식을 적습니다」): 원문 메모대로 월·일·시·분·초·연·시간대가 01/02 03:04:05PM '06 -0700 에서
#           차례로 1~7 이라는 대응을 보인다. 시는 12시간제면 3(03), 24시간제면 15 로 적는다.
# 타입 스펙: type-dp-security-matrix — 행 = 기준 값 · 형식 문자열 예 · 순서, 열 = 자리 일곱. §2 공식을 따르되 열이 일곱이라
#           폭 상한 1000 안에 넣으려고 comp_col_w 208 → 120, role_col_w 148 → 104, role_col_gap 16 → 8 로 줄였고,
#           한글 13px 하한 때문에 row_h 36 → 52, row_stride 40 → 60 으로 키웠다. focal 은 없고, 순서 행만 OK 색이다.
# 사실 출처: Learning Go 2판 13장 「time」의 NOTE, go1.25.1 의 time.RFC3339 · time.DateTime · time.Kitchen 값(2026-09-28).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, PAPER, KR, MONO

LP, RP, COMP_W, GAP0, ROLE_W, GAP = 12, 48, 120, 12, 104, 8
HEAD_Y, HEAD_H, ROW_H, ROW_S = 96, 52, 52, 60
cols = [("월", "month"), ("일", "day"), ("시", "hour"), ("분", "minute"), ("초", "second"), ("연", "year"), ("시간대", "zone")]
rows = [("기준 값", ["January", "2", "3PM", "04", "05", "2006", "MST"]),
        ("형식 문자열", ["01 · Jan", "02 · 2", "03 · 15", "04", "05", "06 · 2006", "-0700 · MST"]),
        ("순서", ["1", "2", "3", "4", "5", "6", "7"])]
N = len(cols)
W = LP + COMP_W + GAP0 + N * ROLE_W + (N - 1) * GAP + RP
ROW0 = HEAD_Y + HEAD_H + 16
LEG = ROW0 + (len(rows) - 1) * ROW_S + ROW_H + 24
H = LEG + 44


def kr(t):
    return KR if any("가" <= c <= "힣" for c in t) else MONO


def rx(j):
    return LP + COMP_W + GAP0 + j * (ROLE_W + GAP)


def ry(k):
    return ROW0 + k * ROW_S


d = D(W, H, "MATRIX · 13-02 §2",
      "기준 시각의 각 자리는 1부터 7까지입니다",
      "Go 의 형식 문자열은 기준 시각 Mon Jan 2 15:04:05 MST 2006 을 원하는 모양으로 적어 만든다. "
      "월 1(01, Jan), 일 2, 시 3(12시간제 03, 24시간제 15), 분 4, 초 5, 연 6(06 또는 2006), 시간대 7(-0700, MST 는 UTC 보다 7시간 늦음)로 차례대로 1부터 7이다. "
      "그래서 01/02 03:04:05PM '06 -0700 으로 외운다.",
      lead="가운데 행은 형식 문자열에 적는 모양입니다. 둘 이상이면 가운뎃점으로 나눴습니다.")

d.box(LP, HEAD_Y, COMP_W, HEAD_H)
d.t(LP + COMP_W / 2, HEAD_Y + 31, "자리", 13, INK, KR, "middle", 600)
for j, (a, b) in enumerate(cols):
    d.tone(rx(j), HEAD_Y, ROLE_W, HEAD_H, INFO, 6, "22", 1.0)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 24, a, 13, INK, KR, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HEAD_Y + 42, b, 11, MUTED, MONO, "middle")
for k, (name, vals) in enumerate(rows):
    d.box(LP, ry(k), COMP_W, ROW_H, r=4)
    d.t(LP + COMP_W / 2, ry(k) + 31, name, 13, INK, KR, "middle", 600)
    for j, v in enumerate(vals):
        if k == 2:
            d.tone(rx(j), ry(k), ROLE_W, ROW_H, OK, 4, "18", 0.9)
            d.t(rx(j) + ROLE_W / 2, ry(k) + 33, v, 16, OK, MONO, "middle", 600)
        else:
            d.box(rx(j), ry(k), ROLE_W, ROW_H, r=4)
            d.t(rx(j) + ROLE_W / 2, ry(k) + 31, v, 12, INK, kr(v), "middle", 600)

d.legend(LEG, [("자리", INFO), ("차례로 1부터 7", OK)])
d.save("13-02.reference-time.svg")
print("ok 13-02 ref", W, H)
