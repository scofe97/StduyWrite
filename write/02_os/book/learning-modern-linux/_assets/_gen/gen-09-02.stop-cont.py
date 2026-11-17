# 09-02 §4 「멈춤과 재개」 — 같은 프로세스 PID 4334(sleep 300)를 명령 넷의 시점마다 다시 그려, STAT 이 S → T 로
#           가고, 멈춘 채 받은 SIGTERM 이 ShdPnd 의 비트 14 에 남았다가 CONT 에 전달되어 143 으로 끝나는 자리.
# 실측(debian:12, procps 4.0.2, /tmp/rerun.sh): ps "4334 S sleep 300" → kill -STOP 뒤 "4334 T sleep 300",
#       State: T (stopped) → kill -TERM 뒤에도 "4334 T", SigPnd 0000000000000000, ShdPnd 0000000000004000
#       → kill -CONT; wait → exit=143. 같은 방식으로 멈춘 sleep 에 kill -KILL 을 보내면 깨우지 않아도 137.
#       tstp.sh(trap … TSTP) 는 kill -TSTP 를 받고도 "끝까지 실행", exit=0.
# 1차 자료 proc(5): "ShdPnd: Mask … of signals pending for … process as a whole"; signal(7): SIGSTOP 은 잡을 수 없다.
# 주의: 0x4000 은 16진 자리 3 의 4(=0100), 곧 비트 14, 비트 n-1 이 시그널 n 이므로 15(SIGTERM)다.
# 축약: 마스크 값은 출력이 있는 시점(세 번째 칸)에만 적었다. 137 갈래는 같은 방식의 다른 실행이다.
# 타입 스펙: type-state — 한 프로세스의 상태 S → T → 종료를 시간 칸 넷으로 펴서 같은 객체를 반복해 그렸다.
#           전이 라벨은 칸 위 명령. focal(accent)은 보류된 SIGTERM 비트 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 524
d = D(W, H, "LEARNING MODERN LINUX · 09-02 §4",
      "멈춘 프로세스에 보낸 SIGTERM 은 ShdPnd 비트로 남아 기다린다",
      "sleep 300(PID 4334)에 STOP, TERM, CONT 를 차례로 보낸 실측. 칸마다 그 시점의 ps 줄과 /proc/4334/status "
      "값이다. 멈춘 채 받은 SIGTERM 은 ShdPnd 0000000000004000, 곧 비트 14 로 남고 STAT 은 T 그대로다. "
      "CONT 가 오는 순간 이 SIGTERM 이 전달되어 143 으로 끝난다. 멈춘 채 SIGKILL 을 받으면 깨우지 않아도 137 이다.",
      "같은 PID 4334 를 명령 넷의 시점마다 다시 그렸습니다")

X0, CW, GAP = 24, 190, 24
CY, CH = 148, 216
SROW = CY + 56                    # STAT 줄
cmds = ["sleep 300 &", "kill -STOP $p", "kill -TERM $p", "kill -CONT $p"]


def cx0(i):
    return X0 + i * (CW + GAP)


# ── 연결선 먼저 ───────────────────────────────────
for i in range(3):
    d.arrow([(cx0(i) + CW + 2, SROW - 6), (cx0(i + 1) - 3, SROW - 6)],
            ACC if i == 2 else MUTED, "acc" if i == 2 else "ar", 1.4)
# 멈춘 채 SIGKILL 갈래: 둘째 칸 아래 → 넷째 칸 아래 상자
BY0, BH = CY + CH + 20, 48
bmid = BY0 + BH / 2
x2 = cx0(1) + CW / 2
d.arrow([(x2, CY + CH + 2), (x2, bmid), (cx0(3) - 3, bmid)], BAD, "bad", 1.3)
d.t(cx0(2) + 12, bmid - 10, "kill -KILL $p", 12, BAD, MONO, "start", 600)
d.t(cx0(2) + 124, bmid - 10, "깨우지 않아도", 12, BAD, KR, "start")

# ── 명령 칩 ─────────────────────────────────────
for i, c in enumerate(cmds):
    d.chip(cx0(i) + CW / 2, CY - 24, c, ACC if i == 3 else MUTED, 12)


def card(i, dashed=False):
    x = cx0(i)
    if dashed:
        d.o.append(f'<rect x="{x}" y="{CY}" width="{CW}" height="{CH}" rx="8" fill="none" '
                   f'stroke="{SOFT}" stroke-width="1" stroke-dasharray="4 3"/>')
    else:
        d.box(x, CY, CW, CH, PAPER2, RULE, 1.0, 8)
    return x


def stat(x, v, c=INK):
    d.t(x + 12, CY + 24, "PID 4334", 12, SOFT, MONO, "start")
    d.t(x + 12, SROW + 4, "STAT", 12, MUTED, MONO, "start")
    d.t(x + CW - 16, SROW + 8, v, 24, c, MONO, "end", 600)
    d.line(x + 12, SROW + 24, x + CW - 12, SROW + 24, RULE, 0.8)


# 1 — 실행 중
x = card(0); stat(x, "S")
d.t(x + 12, CY + 112, "4334 S sleep 300", 12, INK, MONO, "start")
d.t(x + 12, CY + 136, "STOP 을 받기 전", 12, MUTED, KR, "start")

# 2 — 멈춤
x = card(1); stat(x, "T")
d.t(x + 12, CY + 112, "4334 T sleep 300", 12, INK, MONO, "start")
d.t(x + 12, CY + 136, "State: T (stopped)", 12, MUTED, MONO, "start")
d.t(x + 12, CY + 160, "SIGSTOP 은 잡을 수 없음", 12, MUTED, KR, "start")

# 3 — 멈춘 채 SIGTERM: ShdPnd 비트 14
x = card(2); stat(x, "T")
d.t(x + 12, CY + 112, "4334 T sleep 300", 12, INK, MONO, "start")
d.t(x + 12, CY + 132, "SigPnd 0000000000000000", 11, SOFT, MONO, "start")
d.o.append(f'<text x="{x + 12}" y="{CY + 150}" text-anchor="start" font-family="{MONO}" font-size="11" '
           f'font-weight="400" fill="{SOFT}">ShdPnd 000000000000<tspan fill="{ACC}" font-weight="600">4'
           f'</tspan>000</text>')
BW, BG = 22, 4
bx = x + 12
for k, (n, b) in enumerate(((15, 0), (14, 1), (13, 0), (12, 0))):
    cx = bx + k * (BW + BG)
    if b:
        d.tone(cx, CY + 160, BW, 22, ACC, 3, "22", 1.4)
        d.t(cx + BW / 2, CY + 176, "1", 13, ACC, MONO, "middle", 600)
    else:
        d.box(cx, CY + 160, BW, 22, PAPER, RULE, 0.8, 3)
        d.t(cx + BW / 2, CY + 176, "0", 13, SOFT, MONO)
    d.t(cx + BW / 2, CY + 198, str(n), 11, SOFT, MONO)
d.t(bx + 4 * (BW + BG) + 4, CY + 176, "비트 14", 12, ACC, KR, "start", 600)
d.t(bx + 4 * (BW + BG) + 4, CY + 198, "= TERM", 12, ACC, MONO, "start")

# 4 — CONT: 보류된 TERM 전달, 종료
x = card(3, dashed=True)
d.t(x + 12, CY + 24, "PID 4334 없음", 12, SOFT, KR, "start")
d.t(x + 12, SROW + 4, "wait $p", 12, MUTED, MONO, "start")
d.line(x + 12, SROW + 24, x + CW - 12, SROW + 24, RULE, 0.8)
d.t(x + CW / 2, CY + 124, "exit=143", 22, WARN, MONO, "middle", 600)
d.t(x + CW / 2, CY + 146, "128+15", 12, MUTED, MONO)
d.t(x + CW / 2, CY + 180, "보류된 TERM 전달 → Term", 12, MUTED, KR)

# 137 갈래 상자
x = cx0(3)
d.box(x, BY0, CW, BH, PAPER2, BAD, 1.2, 20)
d.t(x + CW / 2, BY0 + 21, "exit=137", 15, BAD, MONO, "middle", 600)
d.t(x + CW / 2, BY0 + 39, "128+9 · CONT 없이", 12, MUTED, KR)

FY = BY0 + BH + 32
d.t(X0, FY, "Ctrl+Z 의 SIGTSTP 는 잡힘", 12, MUTED, KR, "start")
d.t(X0 + 168, FY, "tstp.sh: trap … TSTP", 12, MUTED, MONO, "start")
d.t(X0 + 324, FY, "→ 끝까지 실행 · exit=0", 12, MUTED, KR, "start")
LEG = FY + 20
d.legend(LEG, [("보류된 SIGTERM 비트", ACC), ("128+15", WARN), ("SIGKILL · 128+9", BAD)])
assert LEG + 32 <= H, (LEG, H)
d.save("09-02.stop-cont.svg")
print("ok 09-02.stop-cont")
