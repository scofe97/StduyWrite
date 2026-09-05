# 04-01 §4 — r·w·x 가 일반 파일에서와 디렉토리에서 각각 무엇을 허용하는가.
# 원문("File Permissions"):
#       Read (r): "For a normal file, this allows a user to view the contents of the file. For a
#                 directory, it allows a user to view the names of files in the directory."
#       Write (w): "For a normal file, this allows a user to modify and delete the file. For a directory,
#                  it allows a user to create, rename, and delete files in the directory."
#       Execute (x): "For a normal file, this allows a user to execute the file if the user also has read
#                    permissions on it. For a directory, it allows a user to access file information in
#                    the directory, effectively permitting them to change into it (cd) or list its
#                    content (ls)."
#       그리고 대상은 좁은 것에서 넓은 것으로 User(소유자) · Group · Other 셋이다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 대조 행렬로 쓴다. 행 = 접근 종류, 열 = 대상 종류.
#           accent 는 뜻이 가장 많이 갈리는 한 행.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

rows = [
    ("r", "읽기 · 8진수 4",
     ("내용을 본다", "파일 안을 읽는다", OK),
     ("이름을 본다", "안에 있는 파일 이름을 본다", INFO)),
    ("w", "쓰기 · 8진수 2",
     ("고치고 지운다", "파일 자체를 수정·삭제", OK),
     ("만들고 바꾸고 지운다", "그 안의 파일을 대상으로", INFO)),
    ("x", "실행 · 8진수 1",
     ("실행한다", "읽기 권한도 함께 있어야 한다", ACC),
     ("들어가고 나열한다", "cd 와 ls 가 가능해진다", ACC)),
]
cols = [("일반 파일에서", "touch 로 만든 것"), ("디렉토리에서", "같은 글자, 다른 뜻")]

LEFT, RIGHT = 16, 48
COMP_W, GAP, COL_W, COL_GAP = 268, 12, 268, 16
HEADER_Y, HEADER_H = 116, 56
ROW_H, STRIDE, ROW0 = 76, 84, 192

n = len(cols)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT
row_y = lambda k: ROW0 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 146

d = D(W, H, "LEARNING MODERN LINUX · 04-01 §4",
      "같은 글자가 파일과 디렉토리에서 다른 것을 허용한다",
      "세 접근 종류가 일반 파일에서와 디렉토리에서 각각 무엇을 허용하는지 갈라 놓은 표. "
      "실행 비트가 두 경우에 가장 크게 갈린다.",
      "디렉토리의 x 는 실행이 아니라 들어가기입니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "어떤 접근인가", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 42, "vs. 무엇에 붙었나", 12, MUTED, KR)

for j, (name, sub) in enumerate(cols):
    d.box(col_x(j), HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 42, sub, 12, MUTED, KR)

for k, (bit, what, *cells) in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LEFT + 18, y + 34, bit, 20, INK, MONO, "start", 600)
    d.t(LEFT + 52, y + 34, what, 13, MUTED, KR, "start")
    for j, (val, note, c) in enumerate(cells):
        if c is ACC:
            d.tone(col_x(j), y, COL_W, ROW_H, ACC, r=4)
        else:
            d.box(col_x(j), y, COL_W, ROW_H, PAPER, RULE, 0.6, r=4)
        d.t(col_x(j) + COL_W / 2, y + 32, val, 13, c, KR, "middle", 600)
        d.t(col_x(j) + COL_W / 2, y + 54, note, 12, MUTED, KR)

d.t(LEFT, bottom + 34, "대상은 좁은 것에서 넓은 것으로 셋입니다 — 소유자(user) · 그룹(group) · 그 밖의 모두(other).",
    12, MUTED, KR, "start")
d.t(LEFT, bottom + 56, "그래서 -rw-r--r-- 는 앞 한 칸이 파일 종류이고 나머지 아홉 칸이 셋 곱하기 셋입니다.",
    12, MUTED, KR, "start")
d.t(LEFT, bottom + 78, "숫자로 적으면 rwx 가 7, rw- 가 6, r-x 가 5, r-- 가 4 입니다.",
    12, SOFT, KR, "start")
d.legend(bottom + 96, [("파일에서의 뜻", OK), ("디렉토리에서의 뜻", INFO), ("가장 많이 갈리는 비트", ACC)])
d.save("04-01.file-mode.svg")
print("ok 04-01.file-mode")
