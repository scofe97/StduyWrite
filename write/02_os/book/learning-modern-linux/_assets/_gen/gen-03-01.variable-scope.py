# 03-01 §3 — 변수를 만드는 세 가지 방법과 그 각각이 어디까지 보이는가.
# 원문("Variables"): 두 종류를 가른다 — "Environment variables: Shell-wide settings; list them with env",
#       "Shell variables: Valid in the context of the current execution; list with set in bash.
#       Shell variables are not inherited by subprocesses." 그리고 "You can, in bash, use export to create
#       an environment variable ... when you want to get rid of it, use unset."
#       원서의 실습은 `set MY_VAR=42` 로 셸 변수를 만든다고 적고 `unset $MY_VAR` 로 지운다고 적는다.
#       셋째 행이 그 실습을 그대로 재현한 결과이고, 정오는 본문 인용 블록에 병기했다.
#       (2026-09-05 bash 5 실측: `set MY_VAR=42` 뒤 $MY_VAR 은 비어 있고 $1 이 "MY_VAR=42" 가 된다.
#        `unset $MY_VAR2` 는 "not a valid identifier" 오류를 내고 변수는 살아남는다.)
# 타입 스펙: type-dp-security-matrix — 격자 문법을 대조 행렬로 쓴다. 행 = 만드는 법, 열 = 보이는 자리.
#           accent 는 원서의 실습이 의도와 어긋나는 한 행.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, BAD, PAPER, PAPER2, RULE, KR, MONO

rows = [
    ("MY_VAR=42", "셸 변수를 만드는 올바른 법",
     ("보인다", "set 이 나열", OK),
     ("안 보인다", "환경 변수가 아님", SOFT),
     ("안 보인다", "자식은 물려받지 못함", SOFT)),
    ("export MY_GLOBAL_VAR=…", "환경 변수를 만드는 법",
     ("보인다", "set 이 나열", OK),
     ("보인다", "env 가 나열", OK),
     ("보인다", "자식이 물려받음", OK)),
    ("set MY_VAR=42", "원서가 쓴 명령",
     ("만들어지지 않는다", "$1 이 MY_VAR=42 가 된다", ACC),
     ("안 보인다", "애초에 없음", SOFT),
     ("안 보인다", "애초에 없음", SOFT)),
]
cols = [("현재 셸 · set", "셸 변수 나열"),
        ("현재 셸 · env", "환경 변수 나열"),
        ("자식 셸", "bash 를 새로 띄우면")]

LEFT, RIGHT = 16, 48
COMP_W, GAP, COL_W, COL_GAP = 292, 12, 196, 14
HEADER_Y, HEADER_H = 116, 56
ROW_H, STRIDE, ROW0 = 76, 84, 192

n = len(cols)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT
row_y = lambda k: ROW0 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 124

d = D(W, H, "LEARNING MODERN LINUX · 03-01 §3",
      "변수를 만드는 법에 따라 보이는 범위가 갈린다",
      "셸 변수와 환경 변수의 차이를 만드는 법과 보이는 자리로 갈라 놓은 표. "
      "맨 아래 행은 원서의 실습 명령을 그대로 재현한 결과다.",
      "셸 변수는 자식 프로세스가 물려받지 못합니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "어떻게 만드나", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 42, "vs. 어디서 보이나", 12, MUTED, KR)

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
        d.t(col_x(j) + COL_W / 2, y + 54, note, 12, MUTED, KR)

d.t(LEFT, bottom + 32, "환경 변수는 셸 전체 설정이고 셸 변수는 지금 실행의 문맥에서만 삽니다.",
    12, MUTED, KR, "start")
d.t(LEFT, bottom + 54, "셋째 행은 2026-09-05 에 bash 5 로 직접 돌려 확인한 결과입니다.",
    12, SOFT, KR, "start")
d.legend(bottom + 72, [("보인다", OK), ("보이지 않는다", SOFT), ("원서 실습이 어긋나는 자리", ACC)])
d.save("03-01.variable-scope.svg")
print("ok 03-01.variable-scope")
