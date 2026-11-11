# 03-01 §5 「터미널이 끊길 때 살아남는 잡」 — SIGHUP 이 닿는 잡과 닿지 않는 잡.
# 근거: Debian 12 컨테이너(bash 5.2) 실행 결과(2026-11-10). bash PID 213 이 세션 리더인 pty 에서
#       sleep 300 &(214), nohup sleep 301 &(215), sleep 302 & + disown -h %3(216), sleep 303 & + disown %4(217)
#       를 띄우고 pty 를 쥔 프로세스를 죽인 뒤 ps: 214 없음, 215·216·217 은 PPID 1 · TTY ? 로 남음.
#       setsid(2): "a terminal hangup occurs, then the session leader is sent a SIGHUP signal".
#       bash(1) SIGNALS: "Before exiting, an interactive shell resends the SIGHUP to all jobs, running or stopped",
#       "removed from the jobs table with the disown builtin or marked to not receive SIGHUP using disown -h".
#       nohup(1): "Run COMMAND, ignoring hangup signals."
# 타입 스펙: type-tree — 뿌리(끊긴 터미널)에서 셸을 거쳐 잎 넷으로 내려가는 직교 꺾은선 나무. 깊이 3, 너비 4.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 568
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "터미널이 끊길 때 SIGHUP 이 닿는 잡",
      "터미널 /dev/pts/0 이 끊기면 커널이 세션 리더 bash(PID 213)에 SIGHUP 을 보내고, bash 가 잡 표의 잡에 다시 보낸다. "
      "& 로 띄운 잡도 모두 같은 세션(SID 213)에 머문다. "
      "sleep 300 은 받아서 종료한다. nohup sleep 301 은 받지만 무시한다. disown -h 한 sleep 302 에는 보내지 않는다. "
      "disown 한 sleep 303 은 잡 표에 없어 대상이 아니다. 뒤의 셋은 PPID 1, TTY ? 로 살아남는다.",
      "& 로 띄워도 세션(SID)은 같아서, 사슬의 고리를 끊은 잡만 PID 1 아래에서 돕니다")

# 뿌리와 셸
RX, RY, RW, RH = 380, 100, 240, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0, 8)
d.t(500, RY + 30, "/dev/pts/0 끊김", 14, INK, MONO, "middle", 600)
d.arrow([(500, RY + RH), (500, 205)], BAD, "bad", 1.4)
d.t(512, 182, "SIGHUP · 커널이 세션 리더에", 12, BAD, KR, "start")

BX, BY, BW, BH = 360, 208, 280, 64
d.tone(BX, BY, BW, BH, ACC, 8, "16", 1.5)
d.t(500, BY + 26, "bash · PID 213", 14, ACC, MONO, "middle", 600)
d.t(500, BY + 48, "세션 213 리더 · 잡 표 [1] [2] [3]", 12, MUTED)

# 잎 넷
LW, LH, LGAP, LX0, LY = 220, 128, 20, 30, 376
BUS = 316
leaves = [
    ("sleep 300 &", "대비 없음", "PID 214 · SID 213", "종료", BAD, "SIGHUP", BAD, None),
    ("nohup sleep 301 &", "시작부터 SIGHUP 무시", "PID 215 · SID 213", "생존 · PPID 1 · TTY ?", OK, "SIGHUP · 무시됨", MUTED, None),
    ("sleep 302 &", "disown -h %3", "PID 216 · SID 213", "생존 · PPID 1 · TTY ?", OK, "보내지 않음", SOFT, "5 4"),
    ("sleep 303 &", "disown %4", "PID 217 · SID 213", "생존 · PPID 1 · TTY ?", OK, "잡 표에 없음", SOFT, "5 4"),
]
cxs = [LX0 + i * (LW + LGAP) + LW / 2 for i in range(4)]
d.line(500, BY + BH, 500, BUS, MUTED, 1.4)
d.line(cxs[0], BUS, cxs[-1], BUS, MUTED, 1.4)
for cx, (cmd, how, pid, result, rc, elab, ec, dash) in zip(cxs, leaves):
    x = cx - LW / 2
    mk = {BAD: "bad", MUTED: "ar", SOFT: "soft"}[ec]
    d.arrow([(cx, BUS), (cx, LY - 3)], ec, mk, 1.4, dash)
    d.t(cx + 10, 350, elab, 12, ec if ec != SOFT else MUTED, KR, "start")
    d.tone(x, LY, LW, LH, rc, 8, "10", 1.1)
    d.t(x + 14, LY + 28, cmd, 13, INK, MONO, "start", 600)
    d.t(x + 14, LY + 50, how, 12, MUTED, MONO if "disown" in how else KR, "start")
    d.t(x + 14, LY + 78, pid, 12, MUTED, MONO, "start")
    d.t(x + 14, LY + 106, result, 12, rc, KR, "start", 600)

d.legend(520, [("SIGHUP 을 잡에 다시 보내는 자리", ACC), ("종료", BAD), ("생존", OK)])
d.save("03-01.hangup.svg")
print("ok 03-01.hangup")
