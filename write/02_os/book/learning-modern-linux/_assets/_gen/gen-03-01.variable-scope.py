# 03-01 §3 — 변수를 만든 방법마다 set · env · 자식 bash 세 자리에서 보이는 값.
# 근거: Debian 12 컨테이너(bash 5.2) 실행 결과(2026-11-10).
#       MY_VAR=42; export MY_GLOBAL_VAR="fun with vars" 뒤
#       set | grep '^MY_' → MY_GLOBAL_VAR='fun with vars' / MY_VAR=42,
#       env | grep '^MY_' → MY_GLOBAL_VAR=fun with vars,
#       bash -c 'echo "MY_VAR=[$MY_VAR] MY_GLOBAL_VAR=[$MY_GLOBAL_VAR]"' → MY_VAR=[] MY_GLOBAL_VAR=[fun with vars].
#       set MY_VAR=42 뒤 set · env 둘 다 출력 없음, $1=[MY_VAR=42], 자식에서도 빈 값.
#       bash(1) set: "Any arguments remaining after option processing are treated as values for the positional
#       parameters and are assigned, in order, to $1, $2, ..., $n."
# 타입 스펙: type-dp-security-matrix — 행(만든 방법) × 열(찾아본 자리) 격자의 칸마다 보임/안 보임을 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

LEFT, COMP_W, GAP = 16, 288, 12
COL_W, COL_GAP = 212, 12
HEADER_Y, HEADER_H = 100, 56
ROW0, ROW_H, STRIDE = 168, 72, 80
COLX = [LEFT + COMP_W + GAP + i * (COL_W + COL_GAP) for i in range(3)]
W, H = COLX[-1] + COL_W + 16, 480

d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "변수를 만든 방법마다 세 자리에서 보이는 값",
      "행은 변수를 만든 명령 셋(MY_VAR=42, export MY_GLOBAL_VAR, set MY_VAR=42)이고 열은 찾아본 자리 셋"
      "(set, env, 자식 bash)이다. 셸 변수는 set 에만 보이고, export 한 변수만 env 와 자식에 닿으며, "
      "set MY_VAR=42 는 변수를 만들지 않고 위치 인자 $1 에 들어간다.",
      "export 한 값만 오른쪽 끝 열, 곧 자식 프로세스까지 갑니다")

d.t(LEFT + 14, HEADER_Y + 34, "변수를 만든 명령", 12, MUTED, KR, "start")
heads = [("set | grep '^MY_'", "셸 변수와 환경 변수"),
         ("env | grep '^MY_'", "환경 변수만"),
         ("bash -c 'echo …'", "자식 프로세스")]
for x, (cmd, sub) in zip(COLX, heads):
    d.box(x, HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 0.9, 6)
    d.t(x + COL_W / 2, HEADER_Y + 24, cmd, 12, INK, MONO, "middle", 600)
    d.t(x + COL_W / 2, HEADER_Y + 44, sub, 12, MUTED)

NONE = ("출력 없음", None)
rows = [
    ("MY_VAR=42", "셸 변수",
     [("MY_VAR=42", OK), NONE, ("MY_VAR=[]", None)]),
    ('export MY_GLOBAL_VAR="fun with vars"', "환경 변수",
     [("MY_GLOBAL_VAR='fun with vars'", OK), ("MY_GLOBAL_VAR=fun with vars", OK), ("MY_GLOBAL_VAR=[fun with vars]", ACC)]),
    ("set MY_VAR=42", "위치 인자  $1 = MY_VAR=42",
     [NONE, NONE, ("MY_VAR=[]", None)]),
]
for r, (cmd, kind, cells) in enumerate(rows):
    y = ROW0 + r * STRIDE
    trap = (r == 2)
    if trap:
        d.tone(LEFT, y, COMP_W, ROW_H, WARN, 6, "10", 1.1)
    else:
        d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, 6)
    d.t(LEFT + 14, y + 30, cmd, 12, INK, MONO, "start", 600)
    d.t(LEFT + 14, y + 54, kind, 12, WARN if trap else MUTED, KR, "start")
    for x, (txt, c) in zip(COLX, cells):
        if c:
            d.tone(x, y, COL_W, ROW_H, c, 6, "14", 1.4 if c == ACC else 1.1)
            d.t(x + COL_W / 2, y + 41, txt, 11 if len(txt) > 26 else 12, c, MONO, "middle", 600)
        else:
            d.box(x, y, COL_W, ROW_H, PAPER2, RULE, 0.9, 6)
            d.t(x + COL_W / 2, y + 41, txt, 12, SOFT, MONO if "=" in txt else KR)

d.legend(432, [("자식까지 닿은 값", ACC), ("그 자리에서 보임", OK), ("변수가 생기지 않는 명령", WARN)])
d.save("03-01.variable-scope.svg")
print("ok 03-01.variable-scope")
