# 09-02 §5 「/proc/PID/status 로 처리 방식 읽기」 — SigCgt 16진 마스크의 끝 다섯 자리를 비트 칸 넷씩으로 풀어,
#           켜진 비트가 어느 시그널인지와 trap 이 켠 비트가 어느 것인지를 실제 비트 자리로 보인다.
# 실측(debian:12, bash 5.2.15): 같은 bash 에서 trap "" TERM; trap : USR1 HUP 전후
#       SigCgt 0000000000010002 → 0000000000010203 (SigIgn 0000000200000004 → 0000000200004004)
# 1차 자료 proc(5): "SigBlk, SigIgn, SigCgt: Masks (expressed in hexadecimal) indicating signals being
#       blocked, ignored, and caught" — 비트 n-1 이 시그널 n.
# 본문: 0번 비트(1 SIGHUP)·9번 비트(10 SIGUSR1)는 trap 이 더한 것, 1번 비트(2 SIGINT)·16번 비트(17 SIGCHLD)는
#       trap 전부터 서 있던 bash 자신의 것.
# 축약: 앞 열한 자리는 모두 0 이라 칸으로 풀지 않았다. 칸 안 0·1 은 16진 값을 2진으로 옮긴 것이다.
# 타입 스펙: type-data-flow — 16진 자리 → 비트 칸 넷 → 시그널 번호로 값이 아래로 흐른다. 칸마다 실제 값.
import sys; sys.path.insert(0, ".")
from dd import D, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 880, 468
d = D(W, H, "LEARNING MODERN LINUX · 09-02 §5",
      "SigCgt 0x10203 을 비트 칸으로 풀면 잡는 시그널 넷이 나온다",
      "trap \"\" TERM; trap : USR1 HUP 전후 bash 의 /proc/PID/status SigCgt. 끝 다섯 자리를 16진 한 자리당 "
      "비트 칸 넷으로 풀면 비트 16·9·1·0 이 켜져 있고, 비트 n-1 이 시그널 n 이므로 17 SIGCHLD·10 SIGUSR1·"
      "2 SIGINT·1 SIGHUP 을 잡는다. 0x10002 에서 바뀐 비트 9 와 0 이 trap 이 더한 것이다.",
      "16진 자리 → 비트 칸 넷 → 시그널 번호 순서로 읽습니다")

# ── 위: 마스크 두 줄 ─────────────────────────────────
X0 = 28
d.t(X0, 104, "trap 전", 12, SOFT, KR, "start")
d.t(X0 + 72, 104, "SigCgt: 0000000000010002", 14, SOFT, MONO, "start")
d.t(X0, 130, "trap 뒤", 12, INK, KR, "start", 600)
d.o.append(f'<text x="{X0 + 72}" y="130" text-anchor="start" font-family="{MONO}" font-size="14" '
           f'font-weight="400" fill="{SOFT}">SigCgt: 00000000000<tspan fill="{INK}" font-weight="600">10203'
           f'</tspan></text>')
d.t(W - 28, 130, "끝 다섯 자리를 아래로 풀어 씀", 12, MUTED, KR, "end")

CW, GAP = 152, 16
R1, R1H = 152, 48        # 16진 자리
BL = 220                 # 비트 번호
R2, R2H = 228, 32        # 비트 칸
R3, R3H = 304, 40        # 시그널
SRC = R3 + R3H + 20      # 출처
CELL, CG = 32, 4

cols = [  # 자리, 뒤 값, 전 값
    (4, 1, 1), (3, 0, 0), (2, 2, 0), (1, 0, 0), (0, 3, 2),
]
ADDED = {9, 0}
SIG = {16: ("17 SIGCHLD", "bash 자신"), 9: ("10 SIGUSR1", "trap : USR1"),
       1: ("2 SIGINT", "bash"), 0: ("1 SIGHUP", "trap")}


def cell_x(x0, i):
    return x0 + 6 + i * (CELL + CG)


for k, (pos, after, before) in enumerate(cols):
    x0 = X0 + k * (CW + GAP)
    cx = x0 + CW / 2
    zero = after == 0
    changed = after != before
    # 16진 자리 상자
    d.box(x0, R1, CW, R1H, PAPER2, OK if changed else RULE, 1.2 if changed else 1.0, 6)
    d.t(cx, R1 + 32, str(after), 22, SOFT if zero else INK, MONO, "middle", 600)
    d.t(x0 + 10, R1 + 18, f"자리 {pos}", 12, SOFT, KR, "start")
    d.t(x0 + CW - 10, R1 + 18, f"전 {before}", 12, OK if changed else SOFT, KR, "end")
    # 비트 칸 넷: 왼쪽부터 4k+3 … 4k
    bits = [(after >> (3 - i)) & 1 for i in range(4)]
    for i, b in enumerate(bits):
        n = 4 * pos + 3 - i
        x = cell_x(x0, i)
        d.t(x + CELL / 2, BL - 4, str(n), 11, SOFT, MONO)
        if b:
            c = OK if n in ADDED else INFO
            d.tone(x, R2, CELL, R2H, c, 3, "22", 1.2)
            d.t(x + CELL / 2, R2 + 21, "1", 14, c, MONO, "middle", 600)
        else:
            d.box(x, R2, CELL, R2H, PAPER, RULE, 0.8, 3)
            d.t(x + CELL / 2, R2 + 21, "0", 14, SOFT, MONO)
    if zero:
        d.t(cx, R3 + 26, "켜진 비트 없음", 12, SOFT, KR)
        continue
    lit = [(i, 4 * pos + 3 - i) for i, b in enumerate(bits) if b]
    if len(lit) == 1:
        i, n = lit[0]
        c = OK if n in ADDED else INFO
        bx = cell_x(x0, i) + CELL / 2
        d.arrow([(bx, R2 + R2H + 2), (bx, R3 - 3)], c, "ok" if c == OK else "info", 1.3)
        d.box(x0, R3, CW, R3H, PAPER2, c, 1.1, 6)
        name, src = SIG[n]
        d.t(cx, R3 + 26, name, 13, INK, MONO, "middle", 600)
        d.t(cx, SRC, src, 12, c, MONO if src.startswith("trap") else KR)
    else:
        # 비트 1 → 왼쪽 상자(꺾어서), 비트 0 → 오른쪽 상자(곧게)
        halves = {1: (x0, x0 + 70), 0: (x0 + 82, x0 + CW)}
        for i, n in lit:
            c = OK if n in ADDED else INFO
            m = "ok" if c == OK else "info"
            bx = cell_x(x0, i) + CELL / 2
            hx0, hx1 = halves[n]
            hc = (hx0 + hx1) / 2
            if hx0 <= bx <= hx1:
                d.arrow([(bx, R2 + R2H + 2), (bx, R3 - 3)], c, m, 1.3)
            else:
                ym = R2 + R2H + 20
                d.arrow([(bx, R2 + R2H + 2), (bx, ym), (hc, ym), (hc, R3 - 3)], c, m, 1.3)
            d.box(hx0, R3, hx1 - hx0, R3H, PAPER2, c, 1.1, 6)
            name, src = SIG[n]
            d.t(hc, R3 + 26, name, 12, INK, MONO, "middle", 600)
            d.t(hc, SRC, src, 12, c, MONO if src.startswith("trap") else KR)

FY = SRC + 32
d.line(X0, FY - 18, X0 + 5 * CW + 4 * GAP, FY - 18, RULE, 1)
d.t(X0, FY, "자리 k 의 칸 = 비트 4k+3 … 4k   ·   비트 n-1 = 시그널 n   ·   앞 열한 자리는 모두 0", 12, MUTED, KR, "start")
LEG = FY + 18
d.legend(LEG, [("trap 이 더한 비트 (0x10002 → 0x10203)", OK), ("trap 전부터 bash 가 잡던 비트", INFO)])
assert LEG + 32 <= H, (LEG, H)
d.save("09-02.sigmask.svg")
print("ok 09-02.sigmask")
