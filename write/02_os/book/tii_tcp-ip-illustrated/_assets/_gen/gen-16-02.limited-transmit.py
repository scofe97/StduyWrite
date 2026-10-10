# 타입 스펙: type-sequence — 작은 창에서 중복 ACK 1·2 시 제한 전송과 빠른 재전송 트리거.
# 사실 출처: RFC 3042 · RFC 5681 §3.2 · ch16.txt 898~920행
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 620
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02 §4",
          "작은 창에서 제한 전송이 빠른 재전송을 돕는 흐름",
          "창 크기 3(세그먼트 1–3)에서 1이 손실된 상황이다. 중복 ACK가 2개(2·3번 수신)에 그쳐 RTO가 터질 위험이 있지만, 제한 전송(RFC 3042)은 중복 ACK 1과 2를 받을 때마다 새 세그먼트 4와 5를 주입해 세 번째 중복 ACK 를 유도하고 빠른 재전송을 이끌어 낸다.",
          "중복 ACK 하나·둘에 새 데이터를 주입해 파이프를 유지합니다")

S, R = "송신자", "수신자"
d.LX = {S: 280, R: 740}
for nm, sub in ((S, "창 W = 3 · 제한 전송 적용"), (R, "수신 소켓")):
    x = d.LX[nm]
    d.box(x - 110, 100, 220, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(540)
xs = d.LX[S]

# 1. seq 1 손실
y = 180
d.path(f"M {xs + 10} {y} L 560 {y}", BAD, 1.5, dash="5 4")
d.t((xs + 560) / 2, y - 9, "seq 1 (손실)", 12, BAD, MONO, "middle", 600)
d.chip(600, y, "망에서 유실", BAD, 12)

# 2. seq 2, 3 전송 및 도착
d.msg(S, R, "seq 2, 3 송신", 222, MUTED, "ar", sub="초기 창 3 세그먼트 주입")

# 3. seq 2 도착에 따른 dupACK 1 및 제한 전송 1
d.msg(R, S, "ACK 1 (중복 1)", 268, WARN, "warn", sub="seq 2 수신 피드백")
d.msg(S, R, "seq 4 송신 · 제한 전송 #1", 314, INFO, "info", sub="중복 ACK 1개에 새 세그먼트 주입")

# 4. seq 3 도착에 따른 dupACK 2 및 제한 전송 2
d.msg(R, S, "ACK 1 (중복 2)", 360, WARN, "warn", sub="seq 3 수신 피드백")
d.msg(S, R, "seq 5 송신 · 제한 전송 #2", 406, INFO, "info", sub="중복 ACK 2개에 새 세그먼트 주입")

# 5. seq 4 도착에 따른 dupACK 3 및 빠른 재전송 촉발
d.msg(R, S, "ACK 1 (중복 3)", 454, WARN, "warn", sub="주입된 seq 4 수신 피드백 (문턱 3 충족)")
d.msg(S, R, "seq 1 재전송 · 빠른 재전송", 502, ACC, "acc", sub="RTO 만료 전 손실 복구 성공")

d.legend(H - 46, [
    ("빠른 재전송 (문턱 3 도달)", ACC),
    ("제한 전송 (새 데이터 주입)", INFO),
    ("중복 ACK", WARN),
    ("유실된 세그먼트", BAD)
])

d.save("16-02.limited-transmit.svg")
