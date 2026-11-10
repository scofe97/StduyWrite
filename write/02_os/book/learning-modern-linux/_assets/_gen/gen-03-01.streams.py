# 03-01 §2 — 같은 명령의 FD 0·1·2 가 리다이렉션 앞뒤로 붙는 곳.
# 근거: Debian 12 컨테이너(bash 5.2)에서 pty 위에 `ls -l /proc/self/fd` 를 돌린 출력
#       (0·1·2 -> /dev/pts/0, 3 -> /proc/9/fd)과, `< /etc/hostname > /tmp/out 2> /dev/null` 을 붙여 돌린 출력
#       (0 -> /etc/hostname, 1 -> /tmp/out, 2 -> /dev/null, 3 -> /proc/8/fd). 2026-11-10 실행.
# 타입 스펙: type-architecture-delta — Before · Changes · After 를 같은 좌표 격자에 놓는다.
#           축약: SVG 한 장이라 HTML 메타데이터 계약은 쓰지 않고, 세 띠를 위에서 아래로 쌓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 572
d = D(W, H, "LEARNING MODERN LINUX · 03-01",
      "FD 셋이 리다이렉션 앞뒤로 붙는 곳",
      "ls -l /proc/self/fd 한 명령의 파일 서술자 0·1·2 가 가리키는 곳을 리다이렉션 앞뒤로 나란히 놓았다. "
      "앞에서는 셋 모두 터미널 /dev/pts/0 이고, 뒤에서는 0 이 /etc/hostname, 1 이 /tmp/out, 2 가 /dev/null 이다.",
      "명령은 그대로이고 셸이 실행 전에 FD 의 끝만 바꿔 끼웁니다")

PX, PW, PH = 20, 280, 136
TX, TW = 560, 340
ROWS = [28, 68, 108]
PORTS = [("FD 0 · stdin", INFO, "info"), ("FD 1 · stdout", OK, "ok"), ("FD 2 · stderr", BAD, "bad")]


def proc(py, pid):
    d.box(PX, py, PW, PH, PAPER2, RULE, 1.0, 8)
    d.t(PX + 16, py + 36, "ls -l /proc/self/fd", 12, INK, MONO, "start")
    d.t(PX + 16, py + 60, f"프로세스 PID {pid}", 12, MUTED, KR, "start")
    for (lab, c, _), ry in zip(PORTS, ROWS):
        d.t(PX + PW - 12, py + ry + 4, lab, 12, c, MONO, "end", 600)


def wire(py, i, chip=None):
    lab, c, mk = PORTS[i]
    y = py + ROWS[i]
    if i == 0:
        d.arrow([(TX - 4, y), (PX + PW + 4, y)], c, mk, 1.4)
    else:
        d.arrow([(PX + PW + 4, y), (TX - 4, y)], c, mk, 1.4)
    if chip:
        d.chip(430, y, chip, c, 12, 8)


# Before
B = 112
d.t(20, B - 10, "BEFORE · 리다이렉션 없음", 12, SOFT, KR, "start")
proc(B, 9)
d.box(TX, B + 8, TW, 120, PAPER2, RULE, 1.0, 8)
d.t(TX + TW / 2, B + 64, "/dev/pts/0", 16, INK, MONO, "middle", 600)
d.t(TX + TW / 2, B + 90, "터미널 장치 · 키보드와 화면", 12, MUTED)
for i in range(3):
    wire(B, i)

# Changes
C = 284
d.t(20, C - 10, "CHANGES · 명령 뒤에 붙인 것", 12, SOFT, KR, "start")
d.tone(20, C, 880, 36, ACC, 6, "14", 1.3)
d.t(460, C + 23, "ls -l /proc/self/fd  < /etc/hostname  > /tmp/out  2> /dev/null", 13, ACC, MONO, "middle", 600)

# After
A = 356
d.t(20, A - 10, "AFTER · 같은 명령, 다른 끝", 12, SOFT, KR, "start")
proc(A, 8)
targets = [("/etc/hostname", "읽는 파일", "< /etc/hostname"),
           ("/tmp/out", "쓰는 파일", "> /tmp/out"),
           ("/dev/null", "버리는 자리", "2> /dev/null")]
for i, (path, role, chip) in enumerate(targets):
    c = PORTS[i][1]
    y = A + ROWS[i]
    d.tone(TX, y - 16, TW, 32, c, 6, "12", 1.1)
    d.t(TX + 16, y + 4, path, 13, INK, MONO, "start", 600)
    d.t(TX + TW - 16, y + 4, role, 12, MUTED, KR, "end")
    wire(A, i, chip)

d.legend(524, [("stdin", INFO), ("stdout", OK), ("stderr", BAD), ("셸이 바꿔 끼우는 부분", ACC)])
d.save("03-01.streams.svg")
print("ok 03-01.streams")
