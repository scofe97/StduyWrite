# 03-02 §8 「터미널이 끊겨도 명령을 살리기」 — 터미널이 끊길 때 SIGHUP 이 닿는 프로세스와 닿지 않는 프로세스.
# 근거(책 밖 보강): signal(7) SIGHUP "Hangup detected on controlling terminal"; GNU Bash "Signals" —
#       "Before exiting, an interactive shell resends the SIGHUP to all jobs, running or stopped";
#       disown 은 작업 목록에서 뺀다; nohup 은 SIGHUP 을 무시하게 하고 실행; setsid(1) 은 새 세션에서 실행.
# 실측(Debian 12, bash 5.2.15 · tmux 3.3a): script -qfc 'exec bash --norc -i' 로 bash(250)를 세션 리더로 두고
#       sleep 301 & / nohup sleep 302 … & / setsid sleep 303 … & / sleep 304 & disown / tmux new -d -s work "sleep 305"
#       뒤 script 를 kill -9. 사라짐: 250, 251. 남음: 252·254(PPID 1, SID 250, TTY ?), 256(SID 256), 258·259(pts/1).
# 타입 스펙: type-architecture — 세션(SID)마다 점선 영역으로 묶고 프로세스를 PID 로 단 상자로 둔다.
#           흐름은 위→아래(끊김 → bash → 작업). coral 은 SIGHUP 을 퍼뜨리는 bash 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 03-02 §8",
      "터미널이 끊길 때 SIGHUP 이 닿는 곳과 닿지 않는 곳",
      "한 셸에서 다섯 방법으로 sleep 을 띄우고 터미널 쪽을 죽인 실험. 세션(SID)마다 영역으로 묶고 실제 PID 를 달았다. "
      "bash 가 받은 SIGHUP 을 작업 목록의 작업에 다시 보낸다.",
      "SIGHUP 은 pts/0 에 묶인 세션 250 안에서만 퍼집니다")


def zone(x, y, w, h, label, c):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}06" '
               f'stroke="{c}" stroke-width="1.1" stroke-dasharray="6 5"/>')
    lw = sum(12 if "가" <= ch <= "힣" else 7 for ch in label) + 16
    d.o.append(f'<rect x="{x + 12}" y="{y - 8}" width="{lw}" height="16" fill="{PAPER}"/>')
    d.t(x + 20, y + 4, label, 11, c, MONO, "start", 600)


def proc(x, y, w, pid, cmd, verdict, col, h=60):
    d.box(x, y, w, h, PAPER2, col, 1.2, 6)
    d.t(x + 12, y + 22, pid, 11, SOFT, MONO, "start", 600)
    d.t(x + 12, y + 44, cmd, 12, INK, MONO, "start")
    d.t(x + w - 12, y + 22, verdict, 11, col, KR, "end", 600)


# 영역
zone(24, 120, 544, 336, "SID 250 · pts/0", INFO)
zone(592, 120, 264, 108, "SID 256 · TTY 없음", SOFT)
zone(592, 260, 264, 196, "SID 258 · SID 259 · pts/1", SOFT)

# 끊김 출발점
d.tone(196, 140, 200, 36, BAD, op="12")
d.t(296, 163, "pts/0 끊김", 12, BAD, KR, "middle", 600)

# 화살표 먼저
d.arrow([(296, 176), (296, 202)], BAD, "bad", 1.4)
d.t(304, 194, "SIGHUP", 11, BAD, MONO, "start", 600)
BUS = 288
d.line(296, 264, 296, BUS, BAD, 1.3)
d.line(140, BUS, 296 + 156, BUS, BAD, 1.3)
d.arrow([(140, BUS), (140, 318)], BAD, "bad", 1.3)
d.arrow([(452, BUS), (452, 318)], BAD, "bad", 1.3)
d.t(304, 282, "작업 목록에 재전송", 11, BAD, KR, "start")
# disown 된 작업은 버스와 이어지지 않는다
d.t(404, 422, "작업 목록 밖", 11, SOFT, KR, "start")

# bash
d.o.append(f'<rect x="196" y="204" width="200" height="60" rx="6" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
d.t(208, 226, "250", 11, SOFT, MONO, "start", 600)
d.t(208, 248, "bash --norc -i", 12, ACC, MONO, "start", 600)
d.t(384, 226, "종료", 11, BAD, KR, "end", 600)

proc(40, 320, 200, "251", "sleep 301 &", "종료", BAD)
proc(352, 320, 200, "252", "nohup sleep 302 &", "무시 · 남음", OK)
proc(196, 392, 200, "254", "sleep 304 & disown", "남음", OK, h=52)

proc(608, 148, 232, "256", "setsid sleep 303", "남음", OK)
proc(608, 288, 232, "258", "tmux 서버", "남음", OK, h=52)
d.arrow([(724, 340), (724, 362)], MUTED, "ar", 1.1)
proc(608, 364, 232, "259", "sleep 305", "남음", OK, h=52)
d.t(724, 440, "tmux attach -t work", 11, MUTED, MONO)

d.tone(24, 476, W - 48, 52, MUTED, op="0a", sw=0.8)
d.t(40, 498, "끊은 뒤 252 · 254", 12, INK, KR, "start", 600)
d.t(40, 516, "PPID 1 · SID 250 · TTY ?", 11, MUTED, MONO, "start")
d.t(W - 40, 498, "끊은 뒤 256 · 258 · 259", 12, INK, KR, "end", 600)
d.t(W - 40, 516, "변화 없음 · tmux ls → work", 11, MUTED, KR, "end")

d.legend(548, [("pts/0 세션", INFO), ("SIGHUP 을 퍼뜨리는 셸", ACC), ("SIGHUP 경로·종료", BAD), ("살아남음", OK)])
d.save("03-02.hangup-reach.svg")
print("ok 03-02.hangup-reach")
