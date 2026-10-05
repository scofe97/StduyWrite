# 14-03 §1 — 원서 Figure 14-12 를 대신한다.
# 사실 출처(ch14.txt §14.7): 패킷 8 을 보낸 뒤 ACK 경로에 지연 급증이 생겨 5 의 RTO 가 만료되고 5 를 재전송한다.
#   재전송 뒤 원본 5 의 ACK 가 도착한다. 원본 5–8 의 ACK 가 아직 오는 중이고, 도착할 때마다 TCP 는
#   'ACK 된 세그먼트의 다음' 부터 이미 받은 세그먼트를 다시 보낸다(6·7·8, go-back-N). 수신자에는 중복이 생기고
#   중복 ACK 묶음이 돌아가 빠른 재전송까지 부를 수 있다.
#   원서 그림은 단순화를 위해 바이트 대신 패킷 번호를 쓰고, ACK 는 '다음 기대' 가 아니라 '이미 도착한 것' 을 가리킨다(A5 = 5 도착).
# 축약: 원서 그림의 정확한 메시지 간격은 텍스트로 확인할 수 없어, 본문 문장대로 늦은 ACK 하나에 다음 번호 재전송 하나를 이었다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지. 반환(ACK)은 점선.
#           focal 은 타이머 오탐으로 나간 5 재전송 하나 — 뒤의 go-back-N 연쇄가 모두 여기서 시작한다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, WARN, BAD, INFO, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))

W, H = 920, 904
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §1",
          "ACK 가 늦으면 이미 받은 세그먼트까지 다시 간다",
          "송신자가 5–8 을 보냈고 수신자는 모두 받았다. 그 뒤 ACK 경로가 갑자기 느려져 A5–A8 이 오는 동안 5 의 RTO 가 먼저 만료되고 5 가 재전송된다. "
          "이어 도착한 원본 5 의 ACK 에 맞춰 송신자는 6 을, A6 에 맞춰 7 을, A7 에 맞춰 8 을 다시 보낸다. 수신자에는 5–8 이 한 번씩 더 도착하고 중복 ACK 가 돌아간다. "
          "패킷 번호와 '이미 도착한 것' 을 가리키는 ACK 는 원서 그림의 단순화를 따른다.",
          "RTO 오탐 하나가 go-back-N 재전송 연쇄로 번집니다")

S, R = "송신자", "수신자"
d.lanes([(S, "SND"), (R, "RCV")], y0=100, lane_w=260)
d.rails(824)
xs, xr = d.LX[S], d.LX[R]

def note(side, y, txt, c=SOFT):
    if side == S: d.t(xs - 24, y + 4, txt, 12, c, _kr(txt), "end")
    else: d.t(xr + 24, y + 4, txt, 12, c, _kr(txt), "start")

for i, n in enumerate(("5", "6", "7", "8")):
    d.msg(S, R, n, 192 + 40 * i, INFO, "info")
note(R, 252, "5–8 모두 도착", INFO)

# ACK 경로 지연 — 화살표가 아니라 두 레인 사이의 띠로 그린다.
d.tone(xs + 24, 336, xr - xs - 48, 32, WARN, 6, "14", 1.1)
d.t((xs + xr) / 2, 357, "ACK 경로 지연 급증 · A5–A8 이동 중", 13, WARN, KR, "middle", 600)

Y = 412
d.msg(S, R, "5 재전송", Y, ACC, "acc", sub="타이머 오탐")
note(S, Y, "RTO 만료", ACC); note(R, Y, "중복 5", BAD)
rows = [("A5", "원본 5 의 늦은 ACK"), ("6 재전송", None), ("A6", None), ("7 재전송", None),
        ("A7", None), ("8 재전송", None), ("A8", None)]
for i, (lab, sub) in enumerate(rows):
    y = Y + 48 * (i + 1)
    if lab.startswith("A"):
        d.msg(R, S, lab, y, MUTED, "ar", dash="5 4", sub=sub)
    else:
        d.msg(S, R, lab, y, BAD, "bad")
        note(R, y, "중복 " + lab[0], BAD)
note(S, Y + 48, "go-back-N 시작", BAD)
d.msg(R, S, "중복 ACK 들", Y + 48 * 8, WARN, "warn", dash="5 4", sub="빠른 재전송을 부를 수 있음")

d.legend(H - 56, [("타이머 오탐 재전송", ACC), ("go-back-N 재전송", BAD), ("ACK 지연·중복 ACK", WARN), ("원래 전송", INFO)])
d.save("14-03.delay-spike-go-back-n.svg")
