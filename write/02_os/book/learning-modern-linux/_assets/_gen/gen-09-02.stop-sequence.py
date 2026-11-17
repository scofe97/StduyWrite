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
# 실제 구조: 두 프로세스는 유닛의 cgroup(stubborn.service) 안에 있고, systemd 는 그 cgroup 에 남은 프로세스
#       모두에게 보낸다. 이 경계를 점선 영역으로 그렸다. cgroup 경로 이름은 출력에 없어 유닛 이름만 적었다.
# 타입 스펙: type-sequence — actor 넷(lifeline 점선), 시간은 위→아래, return 은 점선, 화살표를 위로 그리지 않는다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, BAD, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 636
d = Seq(W, H, "LEARNING MODERN LINUX · 09-02 §3",
        "SIGTERM 을 무시하는 서비스는 3초를 버티고 SIGKILL 을 맞는다",
        "TimeoutStopSec=3 인 서비스를 systemctl stop 으로 멈춘 실측. journal 의 시각을 그대로 옮겼다. "
        "주 프로세스 1262 와 자식 sleep 1283 은 유닛의 cgroup 안에 있고, KillMode=control-group 이라 "
        "SIGTERM·SIGCONT 와 SIGKILL 이 둘 모두에게 간다. 기본값이었다면 같은 일이 90초 뒤에 일어난다.",
        "systemd 는 cgroup 안의 프로세스 모두에게 보내고, 시간이 다 되면 모두를 죽입니다")

DY = 20                                    # 영역 머리 자리만큼 아래로
LY0 = 104 + DY
# cgroup 영역 — 테두리는 메시지 라벨을 지나는 자리를 비워 맨 끝에 그린다(GAPS)
GX0 = 24 + 180 / 2 + 668 * 2 / 3 - 180 / 2 - 12
GX1 = W - 24
GY0, GY1 = LY0 - 32, 556 + DY + 8
GAPS = []
d.t(GX0 + 12, GY0 + 15, "cgroup · stubborn.service · KillMode=control-group", 11, SOFT, MONO, "start")

LX = d.lanes([("systemctl", "stop stubborn"), ("systemd", "PID 1"),
              ("stubborn.sh", "PID 1262"), ("sleep", "PID 1283")], y0=LY0, lane_w=180)
assert abs(LX["stubborn.sh"] - 90 - 12 - GX0) < 0.5, (LX, GX0)
d.rails(556 + DY)


def m(a, b, label, y, c=MUTED, mk="ar", dash=None, lx=None, sub=None):
    y += DY
    x1, x2 = LX[a], LX[b]; s = 1 if x2 > x1 else -1
    d.path(f"M {x1 + 10 * s} {y} L {x2 - 12 * s} {y}", c, 1.5, m=mk, dash=dash)
    tx = lx if lx else (x1 + x2) / 2
    lw = len(label) * 7.4 + 12
    if tx - lw / 2 < GX0 < tx + lw / 2:    # 영역 왼쪽 변이 라벨을 지나면 그 높이를 비운다
        GAPS.append((y - 24, y - 4))
    d.t(tx, y - 9, label, 12, c, MONO, "middle", 600)
    if sub:
        d.t(tx, y + 18, sub, 12, MUTED, MONO)


m("systemctl", "systemd", "stop stubborn.service", 192)
m("systemd", "stubborn.sh", "SIGTERM, SIGCONT", 236)
m("systemd", "sleep", "SIGTERM, SIGCONT", 276, lx=(LX["stubborn.sh"] + LX["sleep"]) / 2)

# stubborn.sh 의 핸들러
nx, nw = LX["stubborn.sh"], 196
d.box(nx - nw / 2, 304 + DY, nw, 40, PAPER2, RULE, 1.0, 6)
d.t(nx, 320 + DY, "01.131827", 11, SOFT, MONO)
d.t(nx, 336 + DY, "echo  TERM 받음, 무시", 12, INK, KR)

# 기다리는 3초 — systemd lifeline 위의 막대
sx = LX["systemd"]
d.o.append(f'<rect x="{sx - 5}" y="{240 + DY}" width="10" height="140" rx="3" fill="{ACC}33" '
           f'stroke="{ACC}" stroke-width="1.2"/>')
d.t(sx - 16, 296 + DY, "TimeoutStopSec=3", 12, ACC, MONO, "end", 600)
d.t(sx - 16, 316 + DY, "stop-sigterm 3.1초", 12, ACC, KR, "end")
d.t(sx - 16, 336 + DY, "기본값이면 90초", 12, MUTED, KR, "end")
d.t(sx - 16, 376 + DY, "04.249285 timed out", 12, BAD, MONO, "end")

m("systemd", "stubborn.sh", "SIGKILL  04.249325", 404, BAD, "bad")
m("systemd", "sleep", "SIGKILL  04.249399", 440, BAD, "bad", lx=(LX["stubborn.sh"] + LX["sleep"]) / 2)
m("stubborn.sh", "systemd", "status=9/KILL  04.250047", 480, MUTED, "ar", "4 4")
m("systemd", "systemctl", "Result=timeout", 516, MUTED, "ar", "4 4", sub="ExecMainStatus=9")

# cgroup 영역 테두리: 위·오른쪽·아래는 이어서, 왼쪽 변은 라벨 높이를 비우고
r = 8
z = (f"M {GX0:.1f} {GY0 + r} Q {GX0:.1f} {GY0} {GX0 + r:.1f} {GY0} H {GX1 - r} Q {GX1} {GY0} {GX1} {GY0 + r} "
     f"V {GY1 - r} Q {GX1} {GY1} {GX1 - r} {GY1} H {GX0 + r:.1f} Q {GX0:.1f} {GY1} {GX0:.1f} {GY1 - r}")
ys = [GY1 - r]
for a, b in sorted(GAPS, reverse=True):
    ys += [b, a]
ys.append(GY0 + r)
segs = [f"M {GX0:.1f} {ys[i]} V {ys[i + 1]}" for i in range(0, len(ys), 2)]
d.path(z, SOFT, 1.0, dash="4 3")
d.path(" ".join(segs), SOFT, 1.0, dash="4 3")

LEG = 556 + DY + 16
d.legend(LEG, [("SIGTERM 뒤 기다리는 시간", ACC), ("강제 종료", BAD), ("유닛의 cgroup", SOFT)])
assert LEG + 44 <= H, (LEG, H)
d.save("09-02.stop-sequence.svg")
print("ok 09-02.stop-sequence")
