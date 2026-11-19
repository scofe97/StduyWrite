# 02-01 「프로그램의 바이트가 주소 공간이 되고 main() 에서 시작한다」 — 운영체제는 코드와 정적 데이터를 올리고, 스택·힙을 마련하고, 표준 입출력을 열고, main() 으로 점프한다.
# 본문 근거: 이 노트 「3. 프로그램에서 프로세스로」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 4장 §4.3 과 그림 4.1 — 코드와 정적 데이터를 적재하고, 스택에 main() 의 인자(argc, argv)를 채우고, 힙은 작게 시작하며, 표준 입력·출력·에러 파일 디스크립터 세 개를 열고, 진입점 main() 으로 점프한다.
# 타입 스펙: type-data-flow — 디스크의 바이트가 메모리로 옮겨지는 흐름. 옮겨지는 것(INFO)과 운영체제가 새로 마련하는 것(OK)을 색으로 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, INFO, KR, MONO

W, H = 920, 500
d = D(W, H, "OSTEP · 02-01 §3",
      "프로그램의 바이트가 주소 공간이 되고 main() 에서 시작한다",
      "디스크의 프로그램에서 code 와 static data 가 프로세스의 주소 공간으로 적재된다. 운영체제는 스택에 argc 와 argv 를 채우고 힙을 작게 마련할 수 있으며, "
      "표준 입력·출력·에러의 파일 디스크립터 세 개를 열고, 진입점 main() 으로 점프해 CPU 제어를 프로세스에 넘긴다.")

# 디스크
d.tone(24, 112, 200, 176, INFO, 6, "10", 1.1)
d.t(124, 136, "디스크 (또는 SSD)", 13, INK, KR, "middle", 600)
for y, name, sub in ((152, "code", "명령"), (212, "static data", "초기화된 변수")):
    d.box(44, y, 160, 48, PAPER2, INFO, 1.0, 6)
    d.t(124, y + 22, name, 13, INK, MONO, "middle", 600)
    d.t(124, y + 40, sub, 12, MUTED, KR)

# 주소 공간
d.tone(300, 112, 240, 300, SOFT, 6, "10", 1.1)
d.t(420, 136, "프로세스의 주소 공간", 13, INK, KR, "middle", 600)
cells = (
    (152, "code", "디스크에서 읽어 옴", INFO),
    (212, "static data", "디스크에서 읽어 옴", INFO),
    (272, "heap", "작게 시작 · malloc 때 확장", OK),
    (332, "stack", "argc · argv 를 채움", OK),
)
for y, name, sub, c in cells:
    d.tone(320, y, 200, 48, c, 6, "14", 1.1)
    d.t(420, y + 22, name, 13, INK, MONO, "middle", 600)
    d.t(420, y + 40, sub, 12, MUTED, KR)

# 1. 적재
d.arrow([(204, 176), (320, 176)], INFO, "info", 1.6)
d.arrow([(204, 236), (320, 236)], INFO, "info", 1.6)
d.chip(262, 160, "1 적재", INFO, 12, 7)

# 2·3. 스택과 힙 — 본문 순서(스택 → 힙)대로 번호를 단다. 주소 공간 왼쪽 여백에 둔다.
d.chip(262, 356, "2 스택", OK, 12, 4)
d.chip(262, 296, "3 힙", OK, 12, 4)

# 4. 표준 입출력 — 주소 공간이 아니라 프로세스에 열어 주는 것이므로 주소 공간과 잇지 않고 main 앞단에 둔다.
d.tone(640, 152, 232, 92, OK, 6, "14", 1.1)
d.t(756, 180, "열린 파일 디스크립터 세 개", 13, INK, KR, "middle", 600)
d.t(756, 204, "표준 입력 · 표준 출력", 12, MUTED, KR)
d.t(756, 224, "표준 에러", 12, MUTED, KR)
d.chip(756, 140, "4 입출력 준비", OK, 12, 6)

# 5. main 진입
d.tone(640, 320, 232, 92, ACC, 6, "14", 1.4)
d.t(756, 354, "main() 으로 점프", 14, ACC, MONO, "middle", 600)
d.t(756, 380, "CPU 제어를 프로세스에 넘김", 12, MUTED, KR)
d.arrow([(540, 366), (640, 366)], ACC, "acc", 1.6)
d.arrow([(756, 244), (756, 320)], OK, "ok", 1.4)
d.chip(590, 350, "5 점프", ACC, 12, 6)

d.legend(H - 56, [("디스크에서 옮긴 것", INFO), ("운영체제가 마련한 것", OK), ("제어를 넘기는 곳", ACC)])
d.save("02-01.load-process.svg")
print("ok 02-01 load-process")
