# 03-01 §5 「잡의 상태를 옮기는 명령」 — sleep 100 한 잡이 오가는 상태.
# 근거: Debian 12 컨테이너(bash 5.2) 대화형 셸 기록(2026-11-10).
#       sleep 100 & → [1] 195, jobs -l → [1]+ 195 Running sleep 100 &,
#       kill -TSTP %1 뒤 [1]+ 195 Stopped sleep 100, bg %1 → [1]+ sleep 100 & 뒤 다시 Running,
#       kill %1; wait %1 → [1]+ Terminated sleep 100, wait=143.
#       bash(1) JOB CONTROL: "Typing the suspend character (typically ^Z, Control-Z) while a process is running
#       stops that process and returns control to bash", bg · fg 설명. signal(7): SIGTSTP "Stop typed at terminal",
#       SIGINT "Interrupt from keyboard", SIGTERM "Termination signal".
# 타입 스펙: type-state — 둥근 상태 넷과 사건 라벨이 붙은 전이 여덟(상태 수 × 2 이내). 대각선 없이 꺾은선.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 960, 652
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "sleep 100 한 잡이 오가는 상태",
      "잡의 상태 넷(포그라운드, 백그라운드 Running, 멈춤 Stopped, 종료 Terminated)과 그 사이를 옮기는 입력을 그렸다. "
      "Ctrl+Z 는 포그라운드 잡을 Stopped 로 보낼 뿐이고, bg %1 이 그것을 백그라운드 Running 으로 옮긴다. "
      "fg %1 은 어느 쪽에서든 포그라운드로 가져오고, Ctrl+C 와 kill %1 이 종료로 보낸다.",
      "Ctrl+Z 만으로는 가운데 칸에 머뭅니다. bg 나 fg 가 있어야 다시 돕니다")

FG = (40, 148, 280, 84)
BG = (640, 148, 280, 84)
ST = (340, 328, 280, 84)
EN = (340, 500, 280, 72)


def state(b, c, name, line, sub=None, focal=False):
    x, y, w, h = b
    d.tone(x, y, w, h, c, 12, "16" if focal else "10", 1.5 if focal else 1.1)
    d.t(x + 16, y + 26, name, 14, c, KR, "start", 600)
    d.t(x + 16, y + 50, line, 12, INK, MONO, "start")
    if sub:
        d.t(x + 16, y + 70, sub, 12, MUTED, KR, "start")


# 시작점 둘
for cx, lab, out in ((180, "sleep 100", None), (780, "sleep 100 &", "[1] 195")):
    d.o.append(f'<circle cx="{cx}" cy="104" r="5" fill="{MUTED}"/>')
    d.arrow([(cx, 110), (cx, 145)], MUTED, "ar", 1.4)
    d.t(cx + 12, 122 if out else 130, lab, 12, INK, MONO, "start")
    if out:
        d.t(cx + 12, 138, out, 12, MUTED, MONO, "start")

# 백그라운드 → 포그라운드
d.arrow([(BG[0], 176), (FG[0] + FG[2] + 3, 176)], MUTED, "ar", 1.4)
d.t(480, 168, "fg %1", 12, INK, MONO, "middle", 600)

# 포그라운드 → 멈춤 (Ctrl+Z)
d.path(f"M 240 {FG[1] + FG[3]} L 240 356 L {ST[0] - 3} 356", MUTED, 1.4, m="ar")
d.t(252, 290, "Ctrl+Z", 12, INK, MONO, "start", 600)
d.t(252, 308, "SIGTSTP", 12, MUTED, MONO, "start")

# 백그라운드 → 멈춤 (kill -TSTP) — 본문 실험이 지나는 길
d.path(f"M {BG[0] - 3} 215 L 600 215 L 600 {ST[1] - 3}", MUTED, 1.4, m="ar")
d.t(588, 262, "kill -TSTP %1", 12, INK, MONO, "end", 600)
d.t(588, 280, "SIGTSTP", 12, MUTED, MONO, "end")

# 멈춤 → 포그라운드 (fg)
d.path(f"M {ST[0]} 388 L 140 388 L 140 {FG[1] + FG[3] + 3}", MUTED, 1.4, m="ar")
d.t(152, 410, "fg %1", 12, INK, MONO, "start", 600)

# 멈춤 → 백그라운드 (bg) — focal
d.path(f"M {ST[0] + ST[2]} 370 L 780 370 L 780 {BG[1] + BG[3] + 3}", ACC, 1.8, m="acc")
d.t(768, 300, "bg %1", 13, ACC, MONO, "end", 600)
d.t(768, 320, "[1]+ sleep 100 &", 12, MUTED, MONO, "end")

# 포그라운드 → 종료 (Ctrl+C)
d.path(f"M 80 {FG[1] + FG[3]} L 80 536 L {EN[0] - 3} 536", MUTED, 1.4, m="ar")
d.t(92, 500, "Ctrl+C", 12, INK, MONO, "start", 600)
d.t(92, 518, "SIGINT", 12, MUTED, MONO, "start")

# 백그라운드 → 종료 (kill)
d.path(f"M 880 {BG[1] + BG[3]} L 880 536 L {EN[0] + EN[2] + 3} 536", MUTED, 1.4, m="ar")
d.t(868, 482, "kill %1", 12, INK, MONO, "end", 600)
d.t(868, 500, "SIGTERM", 12, MUTED, MONO, "end")
d.t(868, 518, "wait %1 = 143", 12, MUTED, MONO, "end")

state(FG, INFO, "포그라운드", "$ sleep 100", "터미널 입력을 쥔 잡")
state(BG, OK, "백그라운드 · Running", "[1]+  Running    sleep 100 &", "프롬프트 반환")
state(ST, ACC, "멈춤 · Stopped", "[1]+  Stopped    sleep 100", "죽지 않았지만 일하지 않는 잡", focal=True)
state(EN, SOFT, "종료 · Terminated", "[1]+  Terminated    sleep 100")

d.legend(604, [("Ctrl+Z 뒤에 머무는 상태와 빠져나가는 명령", ACC), ("실행 중", OK), ("터미널을 쥠", INFO)])
d.save("03-01.job-control.svg")
print("ok 03-01.job-control")
