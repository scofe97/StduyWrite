# 04-01 §4 — r·w·x 가 일반 파일에서와 디렉토리에서 각각 무엇을 허용하는가.
# 근거(원서의 file w "modify and delete", file x "if the user also has read", dir x "list" 는 매뉴얼과
#       2026-11-17 데비안 실측에 맞춰 고쳤다):
#       path_resolution(7): "execute permission in case of ordinary files, or search permission in case
#                            of directories"
#       unlink(2): "EACCES Write access to the directory containing path is not allowed ..., or one of
#                  the directories in path did not allow search permission" — 삭제는 디렉토리의 w+x.
#       실측: 디렉토리 r-- 는 이름만 보이고 cd 불가, --x 는 ls 불가·cd 와 이름으로 열기 가능.
#             바이너리는 --x 로 실행, 셸 스크립트는 r 도 있어야 한다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 대조 행렬로 쓴다. 행 = 비트, 열 = 대상 종류.
#           accent 는 뜻이 가장 많이 갈리는 한 칸(디렉토리의 x).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

rows = [
    ("r", "읽기 · 4",
     ("내용 읽기", "cat 으로 열기", OK),
     ("이름 목록 읽기", "ls 로 이름만", INFO)),
    ("w", "쓰기 · 2",
     ("내용 고치기", "삭제는 디렉토리 몫", OK),
     ("항목 만들기 · 지우기", "x 도 함께 필요", INFO)),
    ("x", "실행 · 1",
     ("프로그램으로 실행", "스크립트는 r 도 필요", OK),
     ("들어가기 · 이름으로 열기", "검색 권한 · cd", ACC)),
]
cols = [("일반 파일에서", "내용에 대한 접근"), ("디렉토리에서", "안의 이름에 대한 접근")]

LEFT, RIGHT = 16, 48
COMP_W, GAP, COL_W, COL_GAP = 268, 12, 268, 16
HEADER_Y, HEADER_H = 116, 56
ROW_H, STRIDE, ROW0 = 76, 84, 192

n = len(cols)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT
row_y = lambda k: ROW0 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 72

d = D(W, H, "LEARNING MODERN LINUX · 04-01 §4",
      "같은 비트가 파일과 디렉토리에서 다른 것을 허용한다",
      "세 비트가 일반 파일에서와 디렉토리에서 각각 무엇을 허용하는지 갈라 놓은 표. "
      "디렉토리의 x 는 실행이 아니라 검색 권한이다.",
      "디렉토리의 x 는 실행이 아니라 들어가기입니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "비트", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 42, "이름 · 8진수 값", 12, MUTED, KR)

for j, (name, sub) in enumerate(cols):
    d.box(col_x(j), HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 42, sub, 12, MUTED, KR)

for k, (bit, what, *cells) in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LEFT + 18, y + 44, bit, 20, INK, MONO, "start", 600)
    d.t(LEFT + 52, y + 42, what, 13, MUTED, KR, "start")
    for j, (val, note, c) in enumerate(cells):
        if c is ACC:
            d.tone(col_x(j), y, COL_W, ROW_H, ACC, r=4)
        else:
            d.box(col_x(j), y, COL_W, ROW_H, PAPER, RULE, 0.6, r=4)
        d.t(col_x(j) + COL_W / 2, y + 32, val, 13, c, KR, "middle", 600)
        d.t(col_x(j) + COL_W / 2, y + 54, note, 12, MUTED, KR)

d.legend(bottom + 24, [("파일에서의 뜻", OK), ("디렉토리에서의 뜻", INFO), ("가장 많이 갈리는 칸", ACC)])
d.save("04-01.file-mode.svg")
print("ok 04-01.file-mode")
