# 09-02 §1 「시그널 — 커널이 프로세스를 두드리는 방법」 — 같은 kill(SIGTERM) 이 세 프로세스의 처리 방식 칸
#           (15번 칸: 기본 동작 · 핸들러 · 무시)을 읽고 서로 다른 종료 상태로 끝나는 실제 자리.
# 1차 자료 signal(7): "A process can elect one of the following behaviors to occur on delivery of the
#       signal: perform the default action; ignore the signal; or catch the signal with a signal handler"
#       · "The signals SIGKILL and SIGSTOP cannot be caught, blocked, or ignored."
# 실측(debian:12, bash 5.2.15, /tmp/rerun.sh): notrap.sh → exit=143 · trap.sh("TERM 받음, 정리 후 종료")
#       → exit=0 · ign.sh 는 TERM 1.2초 뒤 생존("TERM 뒤에도 살아 있음"), kill -KILL 뒤
#       "line 11: 4324 Killed ./ign.sh", exit=137.
# 축약: 처리 방식은 프로세스 속성(시그널 번호마다 한 칸)이다. 64칸 가운데 이 실험이 건드린 15번과,
#       바꿀 수 없는 9번 두 칸만 그렸다. notrap.sh·trap.sh 의 PID 는 출력에 없어 적지 않았다.
# 타입 스펙: type-architecture — 셸·커널·프로세스 셋(처리 방식 칸)과 종료 상태. 위→아래 한 방향.
#           focal(accent)은 기본 동작을 대체한 trap.sh 의 15번 칸 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 664
d = D(W, H, "LEARNING MODERN LINUX · 09-02 §1",
      "같은 SIGTERM 을 받아도 15번 칸의 처리 방식이 끝을 정한다",
      "/tmp/rerun.sh 가 notrap.sh·trap.sh·ign.sh 에 차례로 kill 을 보낸 실험. 커널은 각 프로세스의 처리 "
      "방식 칸 가운데 15번(SIGTERM)을 읽는다. 기본 동작이면 143, 핸들러가 exit 0 을 부르면 0, 무시면 "
      "살아남는다. 살아남은 ign.sh(PID 4324)에 kill -KILL 을 보내면 9번 칸은 바꿀 수 없어 137 로 끝난다.",
      "처리 방식은 프로세스마다 시그널 번호별 칸으로 있습니다")

CX = (152, 440, 728)
CW = 256
KY, KH = 100, 44                 # 커널 띠
CY = 196                         # 프로세스 카드 위
R15, R9, RH = CY + 12, CY + 56, 36
CB = CY + 136                    # 카드 아래
LW = 92                          # 칸 번호 열 폭
M1Y, M2Y, MH = 372, 444, 48      # 중간 상자 두 줄
EY, EH = 524, 52                 # 종료 상자

procs = [  # 이름, 설정 줄, 15번 칸 값, 15번 칸 색, focal
    ("notrap.sh", "trap 없음", "기본 · Term", INK, False),
    ("trap.sh", "trap 'echo …; exit 0' TERM", "핸들러", ACC, True),
    ("ign.sh · PID 4324", "trap '' TERM", "무시", MUTED, False),
]

# ── 연결선은 상자보다 먼저 ─────────────────────────────

# notrap: 카드 → exit=143 (중간 상자 없이)
d.arrow([(CX[0], CB + 2), (CX[0], EY - 4)], WARN, "warn", 1.3)
d.t(CX[0] + 10, (CB + EY) / 2, "기본 동작 Term", 12, WARN, KR, "start")
# trap: 카드 → 핸들러 출력 → exit=0
d.arrow([(CX[1], CB + 2), (CX[1], M1Y - 4)], ACC, "acc", 1.4)
d.arrow([(CX[1], M1Y + MH + 2), (CX[1], EY - 4)], OK, "ok", 1.3)
d.t(CX[1] + 10, (M1Y + MH + EY) / 2 + 4, "exit 0", 12, OK, MONO, "start")
# ign: 카드 → 살아 있음 → kill -KILL → exit=137
d.arrow([(CX[2], CB + 2), (CX[2], M1Y - 4)], MUTED, "ar", 1.3)
d.arrow([(CX[2], M1Y + MH + 2), (CX[2], M2Y - 4)], MUTED, "ar", 1.3)
d.arrow([(CX[2], M2Y + MH + 2), (CX[2], EY - 4)], BAD, "bad", 1.3)

# ── 셸과 커널 ────────────────────────────────────
d.box(24, KY, W - 48, KH, PAPER2, RULE, 1.0, 8)
d.t(44, KY + 27, "/tmp/rerun.sh", 13, INK, MONO, "start", 600)
d.t(176, KY + 27, "kill $p", 13, MUTED, MONO, "start")
d.t(264, KY + 27, "→ 커널 · SIGTERM (15) 을 PID 마다 전달", 13, INK, KR, "start")

# ── 프로세스 카드: 처리 방식 칸 ─────────────────────────
for cx, (name, setting, v15, c15, focal) in zip(CX, procs):
    x0 = cx - CW / 2
    d.t(x0, CY - 12, name, 14, INK, MONO, "start", 600)
    d.box(x0, CY, CW, CB - CY, PAPER2, RULE, 1.0, 8)
    # 15번 칸
    d.box(x0 + 12, R15, LW, RH, PAPER, RULE, 0.9, 4)
    d.t(x0 + 12 + LW / 2, R15 + 23, "15 TERM", 12, INK, MONO, "middle", 600)
    vx0, vw = x0 + 12 + LW + 8, CW - 24 - LW - 8
    if focal:
        d.tone(vx0, R15, vw, RH, ACC, 4, "12", 1.4)
    else:
        d.box(vx0, R15, vw, RH, PAPER, RULE, 0.9, 4)
    d.t(vx0 + vw / 2, R15 + 23, v15, 13, c15, KR, "middle", 600)
    # 9번 칸 — 바꿀 수 없음
    d.box(x0 + 12, R9, LW, RH, PAPER, RULE, 0.9, 4)
    d.t(x0 + 12 + LW / 2, R9 + 23, "9 KILL", 12, MUTED, MONO, "middle")
    d.o.append(f'<rect x="{vx0}" y="{R9}" width="{vw}" height="{RH}" rx="4" fill="none" '
               f'stroke="{BAD}" stroke-width="0.9" stroke-dasharray="4 3"/>')
    d.t(vx0 + vw / 2, R9 + 23, "기본 · 고정", 12, BAD, KR)
    # 설정 줄
    d.t(x0 + 12, CB - 16, setting, 12, SOFT, MONO, "start")

# 커널 → 15번 칸: 카드 테두리를 넘어 칸 위에 닿아야 하므로 카드 뒤에 그린다
for cx in CX:
    ax = cx + LW / 2 + 12           # 15번 칸 값 열 안쪽
    d.arrow([(ax, KY + KH + 2), (ax, R15 - 3)], MUTED, "ar", 1.3)
d.t(CX[0] + LW / 2 + 22, KY + KH + 30, "15 를 읽음", 12, MUTED, KR, "start")

# ── 중간 상자 ─────────────────────────────────────
x0 = CX[1] - CW / 2
d.box(x0, M1Y, CW, MH, PAPER2, ACC, 1.1, 6)
d.t(CX[1], M1Y + 20, "핸들러 실행 · stdout", 12, MUTED, KR)
d.t(CX[1], M1Y + 38, "TERM 받음, 정리 후 종료", 13, INK, KR, "middle", 600)

x0 = CX[2] - CW / 2
d.box(x0, M1Y, CW, MH, PAPER2, RULE, 1.0, 6)
d.t(CX[2], M1Y + 20, "1.2초 뒤 kill -0 $p", 12, MUTED, MONO)
d.t(CX[2], M1Y + 38, "TERM 뒤에도 살아 있음", 13, INK, KR, "middle", 600)
d.box(x0, M2Y, CW, MH, PAPER2, BAD, 1.1, 6)
d.t(CX[2], M2Y + 20, "kill -KILL $p", 13, INK, MONO, "middle", 600)
d.t(CX[2], M2Y + 38, "9번 칸 → 기본 동작", 12, BAD, KR)

# ── 종료 상태 ─────────────────────────────────────
ends = [(CX[0], "exit=143", "128+15", WARN), (CX[1], "exit=0", "핸들러가 정한 값", OK),
        (CX[2], "exit=137", "4324 Killed · 128+9", BAD)]
for cx, txt, sub, c in ends:
    d.box(cx - 100, EY, 200, EH, PAPER2, c, 1.2, 20)
    d.t(cx, EY + 23, txt, 15, c, MONO, "middle", 600)
    d.t(cx, EY + 41, sub, 12, MUTED, MONO if sub[0].isdigit() else KR)

d.t(24, EY + EH + 26, "처리 방식 칸은 번호마다 있으나 실험이 닿은 15·9번만 그림 · 이름·출력·종료 상태는 rerun.sh 출력 그대로",
    11, SOFT, KR, "start")
LEG = EY + EH + 44
d.legend(LEG, [("기본 동작을 대체한 칸", ACC), ("128+15", WARN), ("바꿀 수 없는 9번 · 128+9", BAD),
               ("핸들러가 정한 값", OK)])
assert LEG + 44 <= H, (LEG, H)
d.save("09-02.signals.svg")
print("ok 09-02.signals")
