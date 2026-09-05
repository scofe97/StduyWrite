# 03-01 §5 — 잡 컨트롤이 오가는 상태들.
# 원문("Job control"): "By default, when you enter a command, it takes control of the screen and the
#       keyboard, which we usually call running in the foreground ... to launch a process in the background,
#       put an & at the end, or to send a foreground process to the background, press Ctrl+Z."
#       "With the fg command, we can bring a process to the foreground." 그리고 셸을 닫아도 살리려면
#       "you can prepend the nohup command", 이미 돌고 있으면 "you can use disown after the fact".
#       없애려면 "the kill command with various levels of forcefulness".
# 정지 상태와 bg 는 bash 매뉴얼이 정본이다 — "Typing the suspend character (typically '^Z', Control-Z)
#       while a process is running stops that process and returns control to Bash", 그리고 그 뒤에
#       "the bg command to continue it in the background, the fg command to continue it in the foreground".
#       accent 를 그 한 칸에 건 이유가 원서가 건너뛴 단계라서다.
# 타입 스펙: type-state — 주체 하나(잡)의 상태 전이와 종료.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, BAD, PAPER2, RULE, KR, MONO

W, H = 880, 636
d = D(W, H, "LEARNING MODERN LINUX · 03-01 §5",
      "잡 하나가 오가는 네 상태",
      "명령 하나를 잡으로 보고 그 상태 전이를 그린 것. 원서가 든 & · fg · kill 에 더해, "
      "정지에서 백그라운드로 이어 돌리는 bg 한 칸을 bash 매뉴얼 근거로 채웠다.",
      "Ctrl+Z 는 백그라운드로 보내는 것이 아니라 멈추는 것입니다")


def state(x, y, w, h, name, sub, c=RULE, tc=INK):
    d.box(x, y, w, h, PAPER2, c, 1.1, 8)
    d.t(x + w / 2, y + 32, name, 15, tc, KR, "middle", 600)
    d.t(x + w / 2, y + 56, sub, 12, MUTED, KR)


def oval(x, y, w, h, txt):
    d.box(x, y, w, h, PAPER2, SOFT, 1.0, 20)
    d.t(x + w / 2, y + h / 2 + 5, txt, 12, MUTED, KR)


FG = (60, 168, 300, 80)
BG = (520, 168, 300, 80)
ST = (290, 336, 300, 80)
EN = (290, 470, 300, 60)

oval(110, 96, 200, 40, "명령을 그냥 입력")
d.arrow([(210, 136), (210, FG[1] - 2)], MUTED, "ar", 1.2)
oval(570, 96, 200, 40, "명령 끝에 & 를 붙임")
d.arrow([(670, 136), (670, BG[1] - 2)], MUTED, "ar", 1.2)

state(*FG, "포그라운드", "화면과 키보드를 쥔다", OK, OK)
state(*BG, "백그라운드", "셸이 프롬프트를 돌려준다", INFO, INFO)
state(*ST, "정지", "실행이 멈춘 채 남아 있다", WARN, WARN)
d.tone(EN[0], EN[1], EN[2], EN[3], BAD, r=8)
d.t(EN[0] + EN[2] / 2, EN[1] + 36, "종료", 15, BAD, KR, "middle", 600)

# 백그라운드 -> 포그라운드
d.path("M 520 196 L 366 196", MUTED, 1.4, m="ar")
d.t(443, 186, "fg", 12, MUTED, MONO)

# 포그라운드 -> 정지
d.path("M 240 248 L 240 300 L 380 300 L 380 334", WARN, 1.4, m="warn")
d.t(300, 292, "Ctrl+Z", 12, WARN, MONO)

# 정지 -> 백그라운드 (원서가 건너뛴 칸)
d.path("M 590 348 L 700 348 L 700 250", ACC, 1.6, m="acc")
d.t(700, 368, "bg", 13, ACC, MONO, "middle", 600)
d.t(700, 388, "여기가 원서에 없다", 12, ACC, KR)

# 정지 -> 포그라운드
d.path("M 290 380 L 140 380 L 140 250", OK, 1.4, m="ok")
d.t(140, 400, "fg", 12, OK, MONO)

# 종료로 가는 길 셋
d.path("M 440 416 L 440 468", BAD, 1.4, m="bad")
d.t(468, 446, "kill", 12, BAD, MONO, "start")
d.path("M 100 248 L 100 500 L 288 500", BAD, 1.2, m="bad")
d.t(150, 490, "Ctrl+C", 12, BAD, MONO, "start")
d.path("M 780 248 L 780 500 L 592 500", BAD, 1.2, m="bad")
d.t(690, 490, "kill", 12, BAD, MONO, "start")

d.t(20, 556, "셸을 닫아도 계속 돌리려면 실행 전에는 nohup 을 앞에 붙이고, 이미 돌고 있으면 disown 을 씁니다.",
    12, MUTED, KR, "start")
d.t(20, 578, "저자는 이 모든 것 대신 터미널 멀티플렉서를 권합니다. 다음 노트가 그 이야기입니다.",
    12, SOFT, KR, "start")
d.legend(596, [("실행 중", OK), ("배경 실행", INFO), ("멈춤", WARN),
               ("원서가 건너뛴 칸", ACC), ("끝냄", BAD)])
d.save("03-01.job-control.svg")
print("ok 03-01.job-control")
