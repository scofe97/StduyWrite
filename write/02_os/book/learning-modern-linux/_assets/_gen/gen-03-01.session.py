# 03-01 §5 「세션과 제어 터미널」 — 세션 192 안의 프로세스 그룹 넷.
# 근거: Debian 12 컨테이너(bash 5.2)에서 `sleep 100 | sleep 101 &`, `sleep 200 &` 를 띄운 뒤
#       `ps -o pid,ppid,pgid,sid,tty,stat,cmd` 출력(2026-11-10):
#         192 190 192 192 pts/0 Ss bash / 194 192 194 192 pts/0 S sleep 100 / 195 192 194 192 pts/0 S sleep 101
#         196 192 196 192 pts/0 S sleep 200 / 197 192 197 192 pts/0 R+ ps.
#       credentials(7): "Sessions and process groups are abstractions devised to support shell job control",
#       "All of the processes in a session share a controlling terminal". ps(1) STAT: s = session leader,
#       + = foreground process group.
# 타입 스펙: type-nested — 세션 ⊃ 프로세스 그룹 ⊃ 프로세스 세 겹. 가장 안쪽 focal 하나에 ACC.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 464
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "세션 192 안의 프로세스 그룹 넷",
      "제어 터미널 /dev/pts/0 을 쓰는 세션 SID 192 안에 프로세스 그룹 넷이 들어 있다. PGID 192 는 세션 리더 bash, "
      "PGID 194 는 파이프라인 sleep 100 | sleep 101 로 잡 1번, PGID 196 은 sleep 200 으로 잡 2번, "
      "PGID 197 은 지금 포그라운드인 ps 다.",
      "셸의 잡 하나가 프로세스 그룹 하나이고, 그 그룹들이 세션 하나에 담깁니다")

SX, SY, SW, SH = 20, 104, 920, 296
d.box(SX, SY, SW, SH, PAPER, SOFT, 1.2, 14)
d.t(SX + 18, SY + 28, "세션 · SID 192", 14, INK, KR, "start", 600)
d.t(SX + SW - 18, SY + 28, "제어 터미널 /dev/pts/0", 12, MUTED, MONO, "end")

GW, GH, GGAP = 210, 228, 16
GY = SY + 48
groups = [
    ("PGID 192", "세션 리더", INFO, [("bash -i", "PID 192 · STAT Ss")], False),
    ("PGID 194", "잡 [1] · 파이프라인", OK, [("sleep 100", "PID 194 · STAT S"), ("sleep 101", "PID 195 · STAT S")], False),
    ("PGID 196", "잡 [2]", OK, [("sleep 200", "PID 196 · STAT S")], False),
    ("PGID 197", "포그라운드 그룹", ACC, [("ps -o pid,pgid,sid …", "PID 197 · STAT R+")], True),
]
for i, (pg, role, c, procs, focal) in enumerate(groups):
    gx = SX + 16 + i * (GW + GGAP)
    d.tone(gx, GY, GW, GH, c, 10, "0C", 1.5 if focal else 1.0)
    d.t(gx + 14, GY + 24, "프로세스 그룹 · " + pg, 12, c, KR, "start", 600)
    d.t(gx + 14, GY + 44, role, 12, MUTED, KR, "start")
    for k, (cmd, meta) in enumerate(procs):
        py = GY + 60 + k * 80
        if focal:
            d.tone(gx + 14, py, GW - 28, 64, ACC, 6, "22", 1.4)
        else:
            d.box(gx + 14, py, GW - 28, 64, PAPER2, RULE, 0.9, 6)
        d.t(gx + 26, py + 26, cmd, 13, ACC if focal else INK, MONO, "start", 600)
        d.t(gx + 26, py + 48, meta, 12, MUTED, MONO, "start")
    if len(procs) == 2:
        d.t(gx + GW / 2, GY + 60 + 64 + 12, "|", 13, MUTED, MONO)

d.legend(416, [("터미널 입력과 Ctrl+C 를 받는 그룹", ACC), ("백그라운드 잡", OK), ("세션 리더", INFO)])
d.save("03-01.session.svg")
print("ok 03-01.session")
