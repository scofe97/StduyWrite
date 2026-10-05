# 14-01 §3 — 재전송 모호성: 같은 바이트를 두 번 보낸 뒤 돌아온 ACK 는 어느 사본의 것인가.
# 사실 출처: 원서 §14.3.2.3 — 전송 → 타임아웃 → 재전송 → ACK 도착. Timestamps 옵션이 없으면 ACK 는 ACK 번호만 실어
#   어느 사본(첫째·둘째)을 확인했는지 표시가 없다. Karn 첫 부분: 재전송한 데이터의 ACK 로 RTT 추정기를 갱신하지 않는다.
#   둘째 부분: 백오프한 RTO 를 다음 패킷에도 유지하고, 재전송 없이 확인될 때 SRTT 로 다시 계산한다.
#   Timestamps 옵션을 쓰면 모호성을 피할 수 있어 첫 부분은 적용되지 않는다(§14.3.2.3 끝, RFC 7323 §4).
#   t0 · t1 은 보낸 시각을 가리키는 기호이고 원서의 수치가 아니다.
# 타입 스펙: type-sequence — 주체 둘(송신자 · 수신자) 사이의 시간순 메시지 넷. 왼쪽 괄호 둘이 두 후보 표본의 길이다.
#           focal 은 어느 사본을 확인했는지 말하지 않는 ACK 한 줄. 아래 두 칸이 그 모호성을 푸는 두 길이다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 10} L {x + 58} {y - 10} L {x + 58} {y + 10} L {x + 13} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68, y + 4, label, 12, c, _kr(label), "start", 600)

W, H = 920, 608
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-01 §3",
          "같은 바이트를 두 번 보낸 뒤의 ACK",
          "송신자가 같은 바이트를 첫 전송(t0)과 RTO 만료 뒤 재전송(t1)으로 두 번 보냈다. 곧 ACK 가 왔지만 ACK 번호에는 어느 사본을 확인했는지 표시가 없어, "
          "t0 부터 잰 표본은 너무 길고 t1 부터 잰 표본은 너무 짧을 수 있다. Karn 알고리즘은 이 표본을 버리고, Timestamps 옵션은 ACK 가 되돌려 준 TSecr 로 사본을 구분한다.",
          "ACK 번호만으로는 어느 사본의 왕복인지 알 수 없습니다")

S, R = "송신자", "수신자"
d.LX = {S: 360, R: 740}
for nm, sub in ((S, "보낸 시각을 기록"), (R, "받은 바이트를 누적 확인")):
    x = d.LX[nm]
    d.box(x - 120, 100, 240, 44, PAPER2, RULE, 1.0)
    d.t(x, 120, nm, 13, INK, KR, "middle", 600)
    d.t(x, 137, sub, 11, MUTED, KR)
d.lane_top = 144
d.rails(412)

d.msg(S, R, "seq x · 첫 전송", 200, MUTED, "ar", dash="5 4", sub="TSval t0 · 지연 또는 손실")
d.selfmsg(S, "RTO 만료", 264, WARN)
d.msg(S, R, "seq x · 재전송", 328, WARN, "warn", sub="TSval t1")
d.msg(R, S, "ACK · 같은 번호", 392, ACC, "acc", sub="TSecr t0 또는 t1")

def bracket(x, y0, y1, lines, c):
    d.line(x, y0, x, y1, c, 1.4)
    d.line(x, y0, x + 8, y0, c, 1.4)
    d.line(x, y1, x + 8, y1, c, 1.4)
    my = (y0 + y1) / 2 - 8 * (len(lines) - 1)
    for i, ln in enumerate(lines):
        d.t(x - 12, my + i * 17 + 4, ln, 12 if i else 13, c if i == 0 else MUTED, KR, "end", 600 if i == 0 else 400)

bracket(120, 200, 392, ["표본 A", "t0 부터", "너무 길 수도"], INFO)
bracket(276, 328, 392, ["표본 B", "t1 부터", "너무 짧을 수도"], INFO)

# 모호성을 푸는 두 길
BY, BH = 444, 72
d.tone(24, BY, 424, BH, WARN, 6, "12", 1.2)
d.t(236, BY + 28, "Karn · 이 표본 버림", 14, WARN, KR, "middle", 600)
d.t(236, BY + 52, "백오프한 RTO 를 다음 세그먼트에도 유지", 12, MUTED, KR)
d.tone(472, BY, 400, BH, OK, 6, "12", 1.2)
d.t(672, BY + 28, "Timestamps · TSecr 로 구분", 14, OK, KR, "middle", 600)
d.t(672, BY + 52, "t0 이면 첫 전송 · t1 이면 재전송", 12, MUTED, KR)

d.legend(H - 56, [("어느 사본인지 모르는 ACK", ACC), ("두 후보 표본", INFO), ("표본을 버리는 길", WARN), ("사본을 가리는 길", OK)])
d.save("14-01.retransmission-ambiguity.svg")
