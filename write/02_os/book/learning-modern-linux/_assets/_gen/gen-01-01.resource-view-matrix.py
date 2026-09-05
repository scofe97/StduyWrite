# 01-01 §4 — 원서가 "Resource Visibility" 에서 던진 세 물음과, 1장이 답한 것·미룬 것.
# 원문: /proc/cpuinfo 로 CPU 를 세고 "would you expect to see the same number of CPUs?" 를 묻는다.
#       troy 가 만든 /tmp/myfile 을 worf 가 보는가를 묻고, 결론에서 "two users see a file at the exact
#       same location" 을 전역 뷰의 예로 든다. "Can there be multiple processes with the same PID in Linux?
#       ... The answer is yes, there can be multiple processes with the same PID, in different contexts
#       called namespaces." 그리고 그 물음이 "turns out to be the basis for containers" 라고 못 박는다.
#       나머지 자원이 네임스페이스에서 어떻게 갈리는지는 1장이 답하지 않고 6장으로 넘긴다.
# 타입 스펙: type-dp-security-matrix — 격자 문법을 대조 행렬로 쓴다. 행 = 자원, 열 = 보는 자리.
#           회색 열이 1장이 답을 미룬 칸이고, accent 는 컨테이너로 이어지는 한 칸이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER, PAPER2, RULE, KR, MONO

rows = [
    ("cat /proc/cpuinfo", "이 기계의 CPU 목록",
     ("네 개로 보인다", "출력이 그렇게 답한다", INFO),
     ("1장은 답을 미룬다", "원서 6장", SOFT)),
    ("/tmp/myfile", "troy 가 만든 파일",
     ("두 사용자가 같은 자리에서", "전역 뷰의 예", OK),
     ("1장은 답을 미룬다", "원서 6장", SOFT)),
    ("cat /proc/$$/status", "지금 셸의 PID",
     ("PID 2056 하나", "프로세스 하나에 번호 하나", INFO),
     ("같은 PID 가 또 있다", "여기서 컨테이너가 나온다", ACC)),
]
cols = [("한 호스트 안에서", "원서가 출력으로 보여 준 것"),
        ("네임스페이스가 다르면", "다른 문맥에서 보면")]

LEFT, RIGHT = 16, 48
COMP_W, GAP, COL_W, COL_GAP = 300, 12, 240, 16
HEADER_Y, HEADER_H = 112, 56
ROW_H, STRIDE, ROW0 = 72, 80, 188

n = len(cols)
W = LEFT + COMP_W + GAP + n * COL_W + (n - 1) * COL_GAP + RIGHT
row_y = lambda k: ROW0 + k * STRIDE
col_x = lambda j: LEFT + COMP_W + GAP + j * (COL_W + COL_GAP)
bottom = row_y(len(rows) - 1) + ROW_H
H = bottom + 120

d = D(W, H, "LEARNING MODERN LINUX · 01-01 §4",
      "같은 자원인데 보는 자리에 따라 답이 갈린다",
      "원서 1장이 던진 세 물음을 자원과 보는 자리로 갈라 놓은 표. 왼쪽 열은 원서가 명령과 출력으로 "
      "답한 칸이고, 오른쪽 열에서 한 칸만 답이 뒤집힌다.",
      "회색 칸은 원서 1장이 답하지 않고 6장으로 넘긴 자리입니다")

d.box(LEFT, HEADER_Y, COMP_W, HEADER_H, PAPER2, RULE, 0.9)
d.t(LEFT + COMP_W / 2, HEADER_Y + 24, "무엇을 조회하나", 13, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HEADER_Y + 42, "vs. 어디서 보나", 12, MUTED, KR)

for j, (name, sub) in enumerate(cols):
    d.box(col_x(j), HEADER_Y, COL_W, HEADER_H, PAPER2, RULE, 1.0)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 24, name, 13, INK, KR, "middle", 600)
    d.t(col_x(j) + COL_W / 2, HEADER_Y + 42, sub, 12, MUTED, KR)

for k, (cmd, what, *cells) in enumerate(rows):
    y = row_y(k)
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.9, r=4)
    d.t(LEFT + 14, y + 30, cmd, 13, INK, MONO, "start", 600)
    d.t(LEFT + 14, y + 52, what, 12, MUTED, KR, "start")
    for j, (val, note, c) in enumerate(cells):
        if c is ACC:
            d.tone(col_x(j), y, COL_W, ROW_H, ACC, r=4)
        else:
            d.box(col_x(j), y, COL_W, ROW_H, PAPER, RULE, 0.6, r=4)
        d.t(col_x(j) + COL_W / 2, y + 30, val, 13, c, KR, "middle", 600)
        d.t(col_x(j) + COL_W / 2, y + 52, note, 12, MUTED, KR)

d.t(LEFT, bottom + 32, "원서는 마지막 칸을 두고 이렇게 적습니다 — 실없어 보이는 물음이지만 컨테이너의 바탕이 된다고.",
    12, MUTED, KR, "start")
d.legend(bottom + 48, [("원서가 출력으로 답한 칸", INFO), ("전역 뷰의 예", OK),
                       ("1장이 미룬 칸", SOFT), ("답이 뒤집히는 칸", ACC)])
d.save("01-01.resource-view-matrix.svg")
print("ok 01-01.resource-view-matrix")
