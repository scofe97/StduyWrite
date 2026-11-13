# 09-02 §5 「/proc/PID/status 로 처리 방식 읽기」 — SigCgt 16진 마스크를 비트로 풀어 잡는 시그널을 읽는 길.
# 실측(debian:12, bash 5.2.15): 같은 bash 에서 trap "" TERM; trap : USR1 HUP 전후
#       SigCgt 0000000000010002 → 0000000000010203 (SigIgn 0000000200000004 → 0000000200004004)
# 1차 자료 proc(5): "SigBlk, SigIgn, SigCgt: Masks (expressed in hexadecimal) indicating signals being
#       blocked, ignored, and caught" — 비트 n-1 이 시그널 n.
# 주의: 1 (HUP)·10 (USR1) 은 trap 으로 더해진 것, 2 (INT)·17 (CHLD) 은 trap 전부터 서 있던 bash 자신의 것이다.
# 타입 스펙: type-data-flow — 16진 자리 하나가 비트, 비트가 시그널 번호로 바뀌어 아래로 흐른다. 칸마다 실제 값.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 516
d = D(W, H, "LEARNING MODERN LINUX · 09-02 §5",
      "SigCgt 0x10203 을 비트로 풀면 잡는 시그널 넷이 나온다",
      "trap \"\" TERM; trap : USR1 HUP 를 건 bash 의 /proc/PID/status. 16진 한 자리가 비트 넷이고, "
      "0 부터 센 비트 n-1 이 시그널 n 이다.",
      "16진 자리 → 비트 → 시그널 번호 순서로 읽습니다")

d.t(42, 116, "SigCgt:", 14, MUTED, MONO, "start")
d.t(124, 116, "00000000000", 16, SOFT, MONO, "start")
d.t(124 + 11 * 9.6, 116, "10203", 16, INK, MONO, "start", 600)
d.t(838, 116, "trap 전 0000000000010002", 12, SOFT, MONO, "end")

CW, GAP, X0 = 140, 24, 42
cols = [  # (자리, 16진, 비트, 시그널, 출처, focal)
    (4, "1", "비트 16", "17 SIGCHLD", "bash 자신", False),
    (3, "0", "—", "", "", False),
    (2, "2", "비트 9", "10 SIGUSR1", "trap : USR1", True),
    (1, "0", "—", "", "", False),
    (0, "3", "비트 0, 1", "1 SIGHUP · 2 SIGINT", "trap : HUP · bash", False),
]
R1, R2, R3, R4 = 160, 248, 328, 404
for i, (pos, hx, bits, sig, src, focal) in enumerate(cols):
    x = X0 + i * (CW + GAP); cx = x + CW / 2
    zero = hx == "0"
    c = ACC if focal else (SOFT if zero else MUTED)
    if focal:
        d.tone(x, R1, CW, 52, ACC, 6, "12", 1.4)
    else:
        d.box(x, R1, CW, 52, PAPER2, RULE, 1.0, 6)
    d.t(cx, R1 + 28, hx, 20, ACC if focal else (SOFT if zero else INK), MONO, "middle", 600)
    d.t(cx, R1 + 44, f"자리 {pos}", 12, SOFT, KR)
    if zero:
        d.t(cx, R2 + 26, "—", 14, SOFT, MONO)
        continue
    d.arrow([(cx, R1 + 52), (cx, R2 - 4)], c, "acc" if focal else "ar", 1.3)
    d.box(x, R2, CW, 40, PAPER2, ACC if focal else RULE, 1.0, 6)
    d.t(cx, R2 + 25, bits, 12, ACC if focal else INK, KR)
    d.arrow([(cx, R2 + 40), (cx, R3 - 4)], c, "acc" if focal else "ar", 1.3)
    d.box(x, R3, CW, 44, PAPER2, ACC if focal else RULE, 1.0, 6)
    if " · " in sig:
        s1, s2 = sig.split(" · ")
        d.t(cx, R3 + 19, s1, 13, INK, MONO, "middle", 600)
        d.t(cx, R3 + 37, s2, 13, INK, MONO, "middle", 600)
    else:
        d.t(cx, R3 + 27, sig, 13, ACC if focal else INK, MONO, "middle", 600)
    d.t(cx, R4 + 4, src, 12, ACC if focal else MUTED, MONO if src.startswith("trap") else KR)

d.line(X0, 432, X0 + 5 * CW + 4 * GAP, 432, RULE, 1)
d.t(X0, 452, "자리 k 의 1 = 비트 4k   ·   0x200 = 비트 9 = 시그널 10   ·   0x3 = 비트 0, 1 = 시그널 1, 2", 12, MUTED, KR, "start")
d.legend(468, [("trap : USR1 로 더해진 자리", ACC)])
d.save("09-02.sigmask.svg")
print("ok 09-02.sigmask")
