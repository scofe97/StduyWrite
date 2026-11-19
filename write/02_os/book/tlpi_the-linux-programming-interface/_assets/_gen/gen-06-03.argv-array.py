# 06-03 §1 argv 포인터 배열 — necho hello world 를 실행했을 때 argc 와 argv 가 가리키는 문자열 네 칸.
# 본문 근거: 이 노트 「1. 명령행 인자의 전달과 argv 포인터 배열」과 첫 코드 블록(necho 의 출력 argv[0]~argv[2]).
# 값 근거: argc = 3, argv[0]~argv[2] 는 노트의 necho 출력 블록과 같다. argv[3] 은 argv[argc] == NULL 규칙(TLPI 6.6, execve(2) 「argv … must be terminated by a null pointer」).
# 타입 스펙: type-architecture — 포인터 칸(왼쪽)이 문자열 칸(오른쪽)을 가리키는 구조. 같은 형태의 environ 도식과 같은 타입을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, PAPER, PAPER2, ACC, OK, INFO, KR, MONO

W, H = 880, 500
d = D(W, H, "TLPI · 06-03 §1",
      "necho hello world 의 argc 와 argv",
      "argc 는 인자 개수 3 이고, argv 는 널 종료 문자열을 가리키는 포인터 세 칸과 NULL 한 칸으로 이루어진다. argv[0] 은 프로그램을 부른 이름이다.",
      lead="왼쪽 칸은 포인터, 오른쪽 칸은 포인터가 가리키는 널 종료 문자열입니다.")

# argc
d.box(40, 104, 160, 48, PAPER, RULE, 0.9, 6)
d.t(60, 134, "argc", 14, MUTED, MONO, "start", 600)
d.t(180, 134, "3", 16, INFO, MONO, "end", 600)

# 배열 머리
d.t(40, 190, "argv", 13, ACC, MONO, "start", 600)
d.t(100, 190, "포인터 배열", 13, MUTED, KR, "start")
d.t(500, 190, "가리키는 문자열", 13, MUTED, KR, "middle")

ROWS = [
    ("argv[0]", '"necho\\0"', "프로그램을 부른 이름", OK),
    ("argv[1]", '"hello\\0"', "첫째 인자", OK),
    ("argv[2]", '"world\\0"', "둘째 인자", OK),
]
Y0, STRIDE = 204, 56
for i, (idx, val, note, c) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    d.box(40, y, 160, 40, PAPER, ACC, 0.9, 4)
    d.t(56, y + 26, idx, 14, INK, MONO, "start", 600)
    d.arrow([(200, y + 20), (356, y + 20)], ACC, "acc", 1.4)
    d.tone(360, y, 280, 40, c, 4, "14", 1.1)
    d.t(500, y + 26, val, 14, c, MONO, "middle", 600)
    d.t(660, y + 26, note, 13, MUTED, KR, "start")

y = Y0 + 3 * STRIDE
d.box(40, y, 160, 40, PAPER, MUTED, 0.9, 4)
d.t(56, y + 26, "argv[3]", 14, INK, MONO, "start", 600)
d.t(184, y + 26, "NULL", 13, MUTED, MONO, "end")
d.line(200, y + 20, 356, y + 20, MUTED, 1.0, "3 3")
d.box(360, y, 280, 40, PAPER2, RULE, 0.8, 4)
d.t(500, y + 26, "가리키는 곳 없음", 13, MUTED, KR, "middle")
d.t(660, y + 26, "argv[argc] 는 항상 NULL", 13, MUTED, KR, "start")

d.legend(H - 56, [("포인터 칸", ACC), ("인자 문자열", OK), ("개수", INFO)])
d.save("06-03.argv-array.svg")
print("ok 06-03 argv-array")
