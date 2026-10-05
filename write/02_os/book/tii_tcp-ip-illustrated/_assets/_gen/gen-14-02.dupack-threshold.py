# 14-02 §2 — 원서 Figure 14-7·14-8 을 대신한다. 중복 ACK 세 개가 빠른 재전송을 촉발하는 순서.
# 사실 출처: 원서 §14.5.1 — SACK 을 끈 Linux 2.6 송신자 · FreeBSD 5.4 수신자. 23801 세그먼트는 송신 측 TCP 아래 계층에서 버려져 캡처에 보이지 않는다.
#   ACK 23801 이 처음 온 시각(Figure 14-7 의 패킷 40)은 원서 텍스트에 없어 그리지 않는다.
#   0.853s 의 ACK 23801 은 데이터 없이 창이 231,616 → 233,016 바이트로 바뀐 창 업데이트라 중복 ACK 문턱에 세지 않는다.
#   0.890 · 0.926 · 0.964s 의 ACK 23801 세 개가 중복 ACK 이고, 셋째 도착이 0.993s 의 23801 빠른 재전송을 촉발한다.
# 타입 스펙: type-sequence — 주체 둘, 메시지 여섯. 왼쪽 열은 송신자가 각 ACK 를 받은 캡처 시각.
#           focal 은 RTO 를 기다리지 않은 0.993s 의 재전송 한 줄.
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

W, H = 920, 592
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-02 §2",
          "중복 ACK 셋을 세고 바로 다시 보낸다",
          "23801 세그먼트가 버려진 뒤 ACK 23801 이 처음 온 다음에도 같은 번호의 ACK 가 이어진다. 0.853초의 것은 광고 창만 바뀐 창 업데이트라 세지 않고, 0.890 · 0.926 · 0.964초의 셋이 중복 ACK 다. "
          "셋째가 도착하자 송신자는 RTO 만료를 기다리지 않고 0.993초에 23801 을 다시 보낸다. 왼쪽 열은 송신자 쪽 캡처 시각이다.",
          "ACK 번호가 머물러도 창 업데이트는 세지 않습니다")

S, R = "송신자", "수신자"
d.LX = {S: 320, R: 760}
for nm, sub in ((S, "Linux 2.6 · SACK 끔"), (R, "FreeBSD 5.4")):
    x = d.LX[nm]
    d.box(x - 112, 100, 224, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, _kr(sub))
d.lane_top = 144
d.rails(504)
xs = d.LX[S]

def when(y, t, note=None, c=SOFT):
    d.t(176, y + 4, t, 12, c, MONO, "end", 600)
    if note: d.t(176, y + 21, note, 11, MUTED, KR, "end")

y = 196
d.path(f"M {xs + 10} {y} L 600 {y}", BAD, 1.5, dash="5 4")
d.t((xs + 600) / 2, y - 9, "seq 23801", 12, BAD, MONO, "middle", 600)
d.chip(644, y, "버려짐", BAD, 12)
when(y, "—", "송신 측 아래 계층")

d.msg(R, S, "ACK 23801", 256, MUTED, "ar", dash="5 4", sub="창 231,616 → 233,016 · 창 업데이트")
when(256, "0.853s", "문턱에 안 셈")
d.msg(R, S, "ACK 23801 · 중복 1", 316, WARN, "warn")
when(316, "0.890s", c=WARN)
d.msg(R, S, "ACK 23801 · 중복 2", 368, WARN, "warn")
when(368, "0.926s", c=WARN)
d.msg(R, S, "ACK 23801 · 중복 3", 420, WARN, "warn")
when(420, "0.964s", "문턱 3 도달", WARN)
d.msg(S, R, "seq 23801 · 빠른 재전송", 480, ACC, "acc", sub="RTO 만료 전")
when(480, "0.993s", c=ACC)

d.legend(H - 56, [("RTO 를 기다리지 않은 재전송", ACC), ("중복 ACK", WARN), ("버려진 세그먼트", BAD)])
d.save("14-02.dupack-threshold.svg")
