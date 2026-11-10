# 09-01 §1 「멈춤과 재개 — STOP·TSTP·CONT」 — 멈춘 프로세스에 보낸 SIGTERM 이 기다렸다가 CONT 에 전달되는 길.
# 실측(debian:12, procps 4.0.2, /tmp/rerun.sh): sleep 300 의 STAT S → kill -STOP 뒤 T, State: T (stopped)
#       → kill -TERM 뒤에도 T, SigPnd 0000000000000000, ShdPnd 0000000000004000 → kill -CONT 뒤 exit=143.
#       tstp.sh(trap … TSTP) 는 kill -TSTP 를 받고도 "끝까지 실행", exit=0.
# 1차 자료 proc(5): "ShdPnd: Mask … of signals pending for … process as a whole"; signal(7): SIGSTOP 은 잡을 수 없다.
# 주의: 0x4000 은 비트 14, 곧 시그널 15(SIGTERM)다.
# 타입 스펙: type-state — 상태는 rx=8 사각, 시작은 r=6 점, 끝은 고리 점, 전이마다 event [guard] / action 라벨.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 452
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §1",
      "멈춘 프로세스에 보낸 SIGTERM 은 사라지지 않고 기다린다",
      "sleep 300 하나에 STOP, TERM, CONT 를 차례로 보낸 실측. 칸 아래 줄은 그 상태에서 ps 의 STAT 과 "
      "/proc/PID/status 에서 읽은 값이다.",
      "CONT 가 오는 순간 기다리던 SIGTERM 이 전달되어 143 으로 끝납니다")

SY, SH, SW = 176, 96, 176
XS = (112, 368, 624)
states = [
    ("실행 중", "STAT S", "ShdPnd …0000", MUTED, False),
    ("멈춤, TERM 대기", "STAT T", "ShdPnd …4000", ACC, True),
    ("종료", "exit=143", "128+15", MUTED, False),
]
for x, (name, a, b, c, focal) in zip(XS, states):
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "12", 1.4)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(x + SW / 2, SY + 32, name, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + SW / 2, SY + 58, a, 12, MUTED, MONO)
    d.t(x + SW / 2, SY + 78, b, 12, SOFT, MONO)

# 시작 점
d.o.append(f'<circle cx="48" cy="{SY + SH / 2}" r="6" fill="{INK}"/>')
d.arrow([(54, SY + SH / 2), (XS[0] - 4, SY + SH / 2)], MUTED, "ar", 1.3)
d.t(28, SY + SH / 2 - 16, "sleep 300 &", 11, SOFT, MONO, "start")
# 끝 고리
ex = XS[2] + SW + 40
d.o.append(f'<circle cx="{ex}" cy="{SY + SH / 2}" r="8" fill="none" stroke="{INK}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{ex}" cy="{SY + SH / 2}" r="5" fill="{INK}"/>')
d.arrow([(XS[2] + SW, SY + SH / 2), (ex - 10, SY + SH / 2)], MUTED, "ar", 1.3)

# 실행 → 멈춤
y1 = SY + 30
d.arrow([(XS[0] + SW, y1), (XS[1] - 4, y1)], MUTED, "ar", 1.4)
d.t((XS[0] + SW + XS[1]) / 2, y1 - 10, "SIGSTOP", 12, MUTED, MONO, "middle", 600)
# 멈춤 → 종료 (CONT)
d.arrow([(XS[1] + SW, y1), (XS[2] - 4, y1)], ACC, "acc", 1.4)
d.t((XS[1] + SW + XS[2]) / 2, y1 - 10, "SIGCONT", 12, ACC, MONO, "middle", 600)
d.t((XS[1] + SW + XS[2]) / 2, y1 + 22, "/ TERM", 12, ACC, MONO)
d.t((XS[1] + SW + XS[2]) / 2, y1 + 40, "전달", 12, ACC, KR)

# 멈춤 자기 전이 — SIGTERM [STAT T] / 대기에 쌓음
cx = XS[1] + SW / 2
d.path(f"M {cx - 40} {SY} L {cx - 40} {SY - 36} L {cx + 40} {SY - 36} L {cx + 40} {SY - 4}", MUTED, 1.3, m="ar")
d.t(cx, SY - 46, "SIGTERM [STAT T] / ShdPnd 에 쌓임", 12, MUTED, KR)

# 실행 상태의 자기 전이 — SIGTSTP 를 잡은 경우
cx0 = XS[0] + SW / 2
d.path(f"M {cx0 - 40} {SY} L {cx0 - 40} {SY - 36} L {cx0 + 40} {SY - 36} L {cx0 + 40} {SY - 4}", OK, 1.3, m="ok")
d.t(cx0, SY - 46, "SIGTSTP [trap … TSTP] / 계속 실행", 12, OK, KR)

# SIGTERM 이 실행 중에 오면 곧바로 종료 — 아래로 돌아가는 경로
by = SY + SH + 96
d.path(f"M {XS[0] + SW - 30} {SY + SH} L {XS[0] + SW - 30} {by} L {XS[2] + SW / 2} {by} L {XS[2] + SW / 2} {SY + SH + 4}",
       SOFT, 1.2, m="soft", dash="4 4")
d.t((XS[1] + XS[2] + SW) / 2, by - 8, "SIGTERM [STAT S] / 곧바로 종료", 12, SOFT, KR)

d.legend(408, [("TERM 이 기다리는 상태", ACC), ("핸들러로 잡은 정지 요청", OK)])
d.save("09-01.stop-cont.svg")
print("ok 09-01.stop-cont")
