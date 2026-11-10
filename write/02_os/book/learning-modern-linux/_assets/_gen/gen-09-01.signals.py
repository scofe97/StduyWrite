# 09-01 §1 「시그널 — 커널이 프로세스를 두드리는 방법」 — SIGTERM 하나가 처리 방식 셋을 거쳐 다른 종료 상태로 끝나는 길.
# 1차 자료 signal(7): "A process can elect one of the following behaviors to occur on delivery of the
#       signal: perform the default action; ignore the signal; or catch the signal with a signal handler"
#       · "The signals SIGKILL and SIGSTOP cannot be caught, blocked, or ignored."
# 실측(debian:12, bash 5.2.15, /tmp/rerun.sh): notrap.sh → exit=143 · trap.sh("TERM 받음, 정리 후 종료")
#       → exit=0 · ign.sh 는 TERM 1.2초 뒤 생존("TERM 뒤에도 살아 있음"), kill -KILL 뒤 exit=137.
# 주의: 칸 안 값은 본문 실험 블록의 스크립트 이름과 출력 그대로다.
# 타입 스펙: type-flowchart — 결정 하나(처리 방식)에서 출구 셋, 시작·끝은 rx=20 타원, 단계는 rx=6 사각, 위→아래.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER2, RULE, KR, MONO

W, H = 880, 600
d = D(W, H, "LEARNING MODERN LINUX · 09-01 §1",
      "SIGTERM 하나가 처리 방식 셋을 지나 서로 다른 종료 상태로 끝난다",
      "같은 반복문에 처리 방식만 바꿔 kill 을 보낸 실험. 핸들러는 기본 동작을 대체하므로 핸들러 안의 exit 이 "
      "종료 상태를 정한다. SIGKILL 은 처리 방식을 보지 않는다.",
      "기본 동작·무시·핸들러, 셋 중 하나가 프로세스의 처리 방식입니다")

CX = (152, 440, 728)
BW = 232

# 시작
d.box(320, 100, 240, 44, PAPER2, MUTED, 1.0, 20)
d.t(440, 127, "kill PID  →  SIGTERM (15)", 13, INK, MONO)
d.arrow([(440, 144), (440, 168)], MUTED, "ar", 1.3)

# 결정
DY = 212
d.o.append(f'<polygon points="440,{DY-40} 532,{DY} 440,{DY+40} 348,{DY}" fill="{PAPER2}" '
           f'stroke="{MUTED}" stroke-width="1.0"/>')
d.t(440, DY - 4, "처리 방식", 13, INK, KR, "middle", 600)
d.t(440, DY + 14, "SigIgn·SigCgt", 11, SOFT, MONO)

# 출구 셋
d.path(f"M 348 {DY} L {CX[0]} {DY} L {CX[0]} 296", MUTED, 1.3, m="ar")
d.arrow([(440, DY + 40), (440, 296)], MUTED, "ar", 1.3)
d.path(f"M 532 {DY} L {CX[2]} {DY} L {CX[2]} 296", ACC, 1.4, m="acc")
d.chip(CX[0], 256, "SIG_DFL", MUTED, 11)
d.chip(440, 272, "trap '' TERM", MUTED, 11)
d.chip(CX[2], 256, "trap '…; exit 0' TERM", ACC, 11)

# 1단 상자
RY, RH = 300, 64
rows = [
    (CX[0], "기본 동작 Term", "notrap.sh", MUTED, False),
    (CX[1], "무시, 반복문 계속", "ign.sh · 1.2초 뒤 생존", MUTED, False),
    (CX[2], "핸들러 실행", "TERM 받음, 정리 후 종료", ACC, True),
]
for cx, name, sub, c, focal in rows:
    if focal:
        d.tone(cx - BW / 2, RY, BW, RH, ACC, 6, "12", 1.4)
    else:
        d.box(cx - BW / 2, RY, BW, RH, PAPER2, RULE, 1.0, 6)
    d.t(cx, RY + 27, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(cx, RY + 48, sub, 12, SOFT if not focal else MUTED, MONO if sub.endswith(".sh") else KR)

# 가운데 2단 — SIGKILL
K_Y = 404
d.arrow([(CX[1], RY + RH), (CX[1], K_Y - 4)], MUTED, "ar", 1.3)
d.box(CX[1] - BW / 2, K_Y, BW, RH, PAPER2, BAD, 1.1, 6)
d.t(CX[1], K_Y + 27, "kill -KILL PID", 13, INK, MONO, "middle", 600)
d.t(CX[1], K_Y + 48, "처리 방식 확인 없음", 12, BAD, KR)

# 끝
EY, EH = 500, 44
ends = [(CX[0], "exit=143", WARN, RY + RH), (CX[1], "exit=137", BAD, K_Y + RH), (CX[2], "exit=0", OK, RY + RH)]
for cx, txt, c, ytop in ends:
    d.arrow([(cx, ytop), (cx, EY - 4)], c if c is not WARN else MUTED, "ar", 1.3)
    d.box(cx - 80, EY, 160, EH, PAPER2, c, 1.2, 20)
    d.t(cx, EY + 27, txt, 14, c, MONO, "middle", 600)

d.legend(556, [("기본 동작을 대체하는 핸들러", ACC), ("128+15", WARN), ("128+9, 잡을 수 없음", BAD), ("핸들러가 정한 값", OK)])
d.save("09-01.signals.svg")
print("ok 09-01.signals")
