# 03-03 §4 — 재전송된 세그먼트의 ACK 로는 RTT 를 잴 수 없다는 것.
# 본문 근거: "재전송된 세그먼트에 대해서는 표본을 잡지 않습니다. ... 어느 전송에 대한 응답인지 알 수 없기 때문입니다."
#   이 도식은 그 한 줄이 왜 필요한지를 숫자로 벌려 놓은 것이다.
# 1차 자료: RFC 6298 §3 "RTT samples MUST NOT be made using segments that were retransmitted
#   (and thus for which it is ambiguous whether the reply was for the first instance of the packet
#   or a later instance)." 그리고 (5.5) "The host MUST set RTO <- RTO * 2".
# 수치는 이 도식이 세운 예다 — t=0 1차, t=100 2차, t=120 ACK. 두 해석이 120 대 20 으로 갈린다.
# 타입 스펙: type-sequence — 같은 순서 번호가 두 번 나가고 답이 하나 오는 시간 구조 자체가 모호함의 원인이다.
#   축약: 1차 세그먼트나 그 ACK 중 무엇이 사라졌는지는 그리지 않는다. 어느 쪽이든 송신자가 보는 그림은 같다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 684
d = Seq(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §4",
        "이 ACK 는 어느 쪽의 답입니까",
        "같은 순서 번호를 두 번 보내고 답을 하나 받으면, 그 답이 1차의 것인지 2차의 것인지 가릴 수 없다. "
        "어느 쪽으로 재느냐에 따라 RTT 가 여섯 배 갈린다.",
        "그래서 재전송된 세그먼트는 표본에서 통째로 뺍니다")

d.lanes([("송신자", "sender"), ("수신자", "receiver")], y0=104, lane_w=260)
d.rails(404)

d.msg("송신자", "수신자", "seq 1000 · 1차", 206, MUTED, sub="t = 0 — 처음 보냅니다")
d.selfmsg("송신자", "timeout", 264, WARN, sub="기다려도 ACK 가 오지 않습니다")
d.msg("송신자", "수신자", "seq 1000 · 2차", 322, WARN, sub="t = 100 — 번호는 1차와 똑같습니다")
d.msg("수신자", "송신자", "ACK 1500", 380, BAD, sub="t = 120 — 몇 번째 전송의 답인지 적혀 있지 않습니다")
d.chip(700, 380, "?", BAD, 13)

d.tone(24, 428, 470, 84, INFO, 6, "10", 1.3)
d.t(44, 454, "1차의 답이었다면", 12, INFO, KR, "start", 600)
d.t(44, 478, "RTT = 120 - 0 = 120", 11.5, INK, MONO, "start")
d.t(44, 498, "진짜 값입니다", 11, MUTED, KR, "start")

d.tone(506, 428, 470, 84, BAD, 6, "10", 1.3)
d.t(526, 454, "2차의 답이라 치고 재면", 12, BAD, KR, "start", 600)
d.t(526, 478, "RTT = 120 - 100 = 20", 11.5, INK, MONO, "start")
d.t(526, 498, "여섯 배 낮게 잡힙니다", 11, BAD, KR, "start")

d.box(24, 528, W - 48, 92, PAPER2, RULE, 0.9, 6)
d.t(44, 554, "낮게 잡히면 악순환이 됩니다", 12, INK, KR, "start", 600)
d.t(44, 576, "추정값이 내려가면 타임아웃도 따라 내려가고, 짧아진 타임아웃이 또 성급한 재전송을 부릅니다. 재전송이 재전송을 부르는 자리입니다.",
    11, MUTED, KR, "start")
d.t(44, 598, "그래서 재전송된 세그먼트는 1차로도 2차로도 재지 않습니다. 대신 타임아웃이 날 때마다 값을 두 배로 늘려 보수적으로 물러섭니다.",
    11, OK, KR, "start")

d.legend(H - 44, [("한 번만 보낸 것", MUTED), ("재전송", WARN), ("가릴 수 없는 답", BAD), ("옳게 재는 쪽", INFO), ("대신 하는 일", OK)])
d.save("03-03.karn-ambiguity.svg")
print("ok karn-ambiguity")
