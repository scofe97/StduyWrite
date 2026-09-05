# 03-03 §4 — 스켈레톤 템플릿의 세 줄이 각각 무엇을 막는가.
# 원문("A skeleton template"): `set -o errexit` 는 "Define that we want to stop the script execution if
#       an error happens", `set -o nounset` 는 "Define that we treat unset variables as an error (so the
#       script is less likely to fail silently)", `set -o pipefail` 는 "Define that when one part of a
#       pipe fails, the whole pipe should be considered failed. This helps to avoid silent failures."
#       그리고 좋은 관례의 첫 항목 — "Avoid silent fails, and fail fast; things like errexit and pipefail
#       do that for you. Since bash tends to fail silently by default, failing fast is almost always a
#       good idea."
#       nounset 칸의 사고 예는 저자가 입력 검증 항목에서 든 것이다 — "an innocent-looking
#       rm -rf "$PROJECTHOME/"* wipes your drive because the variable wasn't set."
# 타입 스펙: type-dp-security-matrix — 격자 문법을 대조 행렬로 쓴다. 행 = 옵션, 열 = 끄면/켜면.
#           accent 는 저자가 구체적 사고를 든 한 행.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

rows = [
    ("set -o errexit", "오류가 나면 멈춘다",
     ("그냥 다음 줄로 간다", "실패한 채 끝까지 실행", BAD),
     ("그 자리에서 멈춘다", "빨리 실패한다", OK)),
    ("set -o nounset", "설정 안 된 변수를 오류로 본다",
     ("빈 문자열로 펼쳐진다", 'rm -rf "$PROJECTHOME/"* 가 /* 가 된다', ACC),
     ("펼치기 전에 멈춘다", "조용한 실패가 줄어든다", OK)),
    ("set -o pipefail", "파이프 한 칸의 실패를 전체 실패로",
     ("마지막 명령만 본다", "중간 실패가 묻힌다", BAD),
     ("한 칸이라도 실패하면 실패", "조용한 실패를 피한다", OK)),
]
cols = [("켜지 않으면", "bash 의 기본값"), ("켜면", "템플릿이 넣어 두는 줄")]

LEFT, RIGHT = 16, 48
COMP_W, GAP, COL_W, COL_GAP = 300, 12, 268, 16
HEADER_Y, HEADER_H = 116, 56
ROW_H, STRIDE, ROW0 = 76, 84, 192

n = len(cols)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT
row_y = lambda k: ROW0 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 124

d = D(W, H, "LEARNING MODERN LINUX · 03-03 §4",
      "세 줄이 각각 어떤 조용한 실패를 막는가",
      "스켈레톤 템플릿 맨 위의 세 줄을 켜지 않았을 때와 켰을 때로 갈라 놓은 표. "
      "저자는 bash 가 기본적으로 조용히 실패하는 쪽이라고 적는다.",
      "가운데 행이 저자가 실제 사고로 든 자리입니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "어떤 줄인가", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 42, "vs. 켜고 안 켜고", 12, MUTED, KR)

for j, (name, sub) in enumerate(cols):
    d.box(col_x(j), HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 42, sub, 12, MUTED, KR)

for k, (cmd, what, *cells) in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LEFT + 14, y + 32, cmd, 13, INK, MONO, "start", 600)
    d.t(LEFT + 14, y + 54, what, 12, MUTED, KR, "start")
    for j, (val, note, c) in enumerate(cells):
        if c is ACC:
            d.tone(col_x(j), y, COL_W, ROW_H, ACC, r=4)
        else:
            d.box(col_x(j), y, COL_W, ROW_H, PAPER, RULE, 0.6, r=4)
        d.t(col_x(j) + COL_W / 2, y + 32, val, 13, c, KR, "middle", 600)
        d.t(col_x(j) + COL_W / 2, y + 54, note, 12, MUTED,
            MONO if all(ord(ch) < 128 or ch in "·" for ch in note) else KR)

d.t(LEFT, bottom + 32, "저자는 이 세 줄에 더해 errtrace 까지 넣은 것을 마지막 예제의 첫머리로 씁니다.",
    12, MUTED, KR, "start")
d.t(LEFT, bottom + 54, "빨리 실패하는 것이 거의 언제나 좋은 생각이라는 것이 이 절의 결론입니다.",
    12, SOFT, KR, "start")
d.legend(bottom + 72, [("막아 준다", OK), ("묻힌다", BAD), ("저자가 든 사고 예", ACC)])
d.save("03-03.set-options.svg")
print("ok 03-03.set-options")
