# 14-02 §2 — NewReno 의 복구 지점과 부분 ACK. 원서 Figure 14-8 아래쪽 두 번째 재전송을 따로 떼어 그린다.
# 사실 출처: 원서 §14.5.1 — 첫 재전송 직전에 보낸 가장 높은 순서 번호로 복구 지점을 기억한다(43401 + 1400 = 44801).
#   1.322s(와 1.321s)의 ACK 는 44801 이 아니라 26601 이다. 이전 최고 ACK 23801 보다 크지만 복구 지점에 못 미쳐 부분 ACK.
#   부분 ACK 가 오면 빠진 것으로 보이는 세그먼트(26601)를 바로 보낸다 — 1.326s. 복구 지점 이상의 ACK 가 와야 복구가 끝난다.
#   SACK 이 없으면 송신자는 RTT 하나에 수신자 구멍을 많아야 하나 알 수 있다.
# 타입 스펙: type-sequence — 주체 둘, 메시지 셋. 왼쪽 열은 송신자 쪽 캡처 시각, 괄호는 구멍 하나를 알아내는 데 든 왕복.
#           focal 은 ACK 번호는 올랐지만 복구 지점에 못 미친 부분 ACK 26601.
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

W, H = 920, 520
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-02 §2",
          "부분 ACK 가 다음 구멍을 드러낸다",
          "빠른 재전송 직전 송신자가 보낸 가장 높은 순서 번호로 복구 지점 44801 을 기억한다. 23801 을 다시 보낸 뒤 돌아온 ACK 는 26601 이라 앞 구멍은 메워졌지만 복구 지점에는 못 미친다. "
          "NewReno 송신자는 이 부분 ACK 를 받자마자 26601 을 다시 보내고, ACK 가 44801 이상이 될 때까지 복구를 이어 간다.",
          "SACK 없이는 구멍 하나를 알아내는 데 왕복 하나가 듭니다")

S, R = "송신자", "수신자"
d.LX = {S: 360, R: 760}
for nm, sub in ((S, "NewReno · SACK 끔"), (R, "구멍 둘 · 23801 · 26601")):
    x = d.LX[nm]
    d.box(x - 112, 100, 224, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(440)
xs = d.LX[S]

def when(y, t, c=SOFT):
    d.t(176, y + 4, t, 12, c, MONO, "end", 600)

d.chip(xs, 184, "복구 지점 44801 = 43401 + 1400", INFO, 12)
d.msg(S, R, "seq 23801 · 빠른 재전송", 244, WARN, "warn", sub="첫 구멍")
when(244, "0.993s", WARN)
d.msg(R, S, "ACK 26601 · 부분 ACK", 304, ACC, "acc", sub="23801 < 26601 < 44801")
when(304, "1.322s", ACC)
d.msg(S, R, "seq 26601 · 재전송", 364, WARN, "warn", sub="다음 구멍 · 복구 유지")
when(364, "1.326s", WARN)
d.chip(xs, 420, "ACK 44801 이상에서 복구 종료", OK, 12)

# 구멍 하나에 왕복 하나
BX = 248
d.line(BX, 244, BX, 304, INFO, 1.4)
d.line(BX, 244, BX + 8, 244, INFO, 1.4)
d.line(BX, 304, BX + 8, 304, INFO, 1.4)
d.t(BX - 12, 268, "왕복 하나", 13, INFO, KR, "end", 600)
d.t(BX - 12, 285, "구멍 하나", 12, MUTED, KR, "end")

d.legend(H - 56, [("복구 지점에 못 미친 ACK", ACC), ("재전송", WARN), ("복구 지점", INFO), ("복구 종료 조건", OK)])
d.save("14-02.partial-ack.svg")
