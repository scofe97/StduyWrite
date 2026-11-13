# 09-02 §3 「128+n 종료 코드와 systemctl stop」 — SIGTERM 을 무시하는 서비스를 멈출 때의 3초.
# 실측(debian:12 + systemd 252.39, TimeoutStopSec=3, trap 'echo "TERM 받음, 무시"' TERM), journalctl -o short-precise:
#       05:08:01.131827 stubborn.sh[1262]: TERM 받음, 무시
#       05:08:04.249285 systemd[1]: stubborn.service: State 'stop-sigterm' timed out. Killing.
#       05:08:04.249325 … Killing process 1262 (stubborn.sh) with signal SIGKILL.
#       05:08:04.249399 … Killing process 1283 (sleep) with signal SIGKILL.
#       05:08:04.250047 … Main process exited, code=killed, status=9/KILL
#       systemctl show: Result=timeout, ExecMainStatus=9, KillMode=control-group
# 1차 자료 systemd.kill(5): "right after sending the signal specified in this setting, systemd will always
#       send SIGCONT" — 그래서 SIGTERM 뒤에 SIGCONT 를 적었다.
# 주의: SIGTERM 이 두 프로세스에 간 것은 KillMode=control-group 의 정의에서 온 것이고, journal 은 SIGKILL 만 줄로 남긴다.
# 타입 스펙: type-sequence — actor 넷(lifeline 점선), 시간은 위→아래, return 은 점선, 화살표를 위로 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, BAD, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 596
d = Seq(W, H, "LEARNING MODERN LINUX · 09-02 §3",
        "SIGTERM 을 무시하는 서비스는 3초를 버티고 SIGKILL 을 맞는다",
        "TimeoutStopSec=3 인 서비스를 systemctl stop 으로 멈춘 실측. journal 의 시각을 그대로 옮겼다. "
        "기본값이었다면 같은 일이 90초 뒤에 일어난다.",
        "systemd 는 cgroup 안의 프로세스 모두에게 보내고, 시간이 다 되면 모두를 죽입니다")
LX = d.lanes([("systemctl", "stop stubborn"), ("systemd", "PID 1"),
              ("stubborn.sh", "PID 1262"), ("sleep", "PID 1283")], y0=104, lane_w=180)
d.rails(536)


def m(a, b, label, y, c=MUTED, mk="ar", dash=None, lx=None):
    x1, x2 = LX[a], LX[b]; s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * s} {y} L {x2 - 12 * s} {y}", c, 1.5, m=mk, dash=dash)
    d.t(lx if lx else (x1 + x2) / 2, y - 9, label, 12, c, MONO, "middle", 600)


m("systemctl", "systemd", "stop stubborn.service", 192)
m("systemd", "stubborn.sh", "SIGTERM, SIGCONT", 236)
m("systemd", "sleep", "SIGTERM, SIGCONT", 276, lx=(LX["stubborn.sh"] + LX["sleep"]) / 2)

# stubborn.sh 의 핸들러
nx, nw = LX["stubborn.sh"], 196
d.box(nx - nw / 2, 304, nw, 40, PAPER2, RULE, 1.0, 6)
d.t(nx, 320, "01.131827", 11, SOFT, MONO)
d.t(nx, 336, "echo  TERM 받음, 무시", 12, INK, KR)

# 기다리는 3초 — systemd lifeline 위의 막대
sx = LX["systemd"]
d.o.append(f'<rect x="{sx - 5}" y="240" width="10" height="140" rx="3" fill="{ACC}33" stroke="{ACC}" stroke-width="1.2"/>')
d.t(sx - 16, 300, "TimeoutStopSec=3", 12, ACC, MONO, "end", 600)
d.t(sx - 16, 320, "stop-sigterm 3.1초", 12, ACC, KR, "end")
d.t(sx - 16, 340, "기본값이면 90초", 12, MUTED, KR, "end")

m("systemd", "stubborn.sh", "SIGKILL  04.249325", 396, BAD, "bad")
m("systemd", "sleep", "SIGKILL  04.249399", 432, BAD, "bad", lx=(LX["stubborn.sh"] + LX["sleep"]) / 2)
m("stubborn.sh", "systemd", "status=9/KILL  04.250047", 476, MUTED, "ar", "4 4")
m("systemd", "systemctl", "Result=timeout", 516, MUTED, "ar", "4 4")

d.legend(552, [("SIGTERM 뒤 기다리는 시간", ACC), ("강제 종료", BAD)])
d.save("09-02.stop-sequence.svg")
print("ok 09-02.stop-sequence")
