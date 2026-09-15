# 04-04 §1 「알림이 닿으면 경로 MTU 를 찾아 줄입니다」 — 해결 도식. 문제 도식(gen-04-04.pmtud-problem.py)과 노드 자리 · 트랙이 같다.
#       줄 단위로 짝을 맞췄다: 1 · 2 는 두 장이 같고, 3 번 줄에서 알림이 방화벽을 지나며, 5 번 줄에서 줄인 크기가 통과한다.
# 타입 스펙: type-architecture — 송신자 · 방화벽 · 터널 입구 라우터 · 수신자를 한 줄에 두고 번호 붙은 수평 화살표로 순서를 보인다.
# 출처: 원문 §4.3.4 "The sender can then resend the data, using a smaller IP datagram size." 원문 밖 사실은 RFC 에서 가져왔다.
#       - 송신자는 첫 링크 MTU 로 시작하고 PTB 를 받으면 그 MTU 로 추정을 낮춘다: RFC 8201 §3 · §4
#       - PTB 는 ICMPv6 타입 2 이고 다음 링크 MTU 칸을 갖는다: RFC 4443 §3.2
#       - 터널 입구는 IPv4 경로 MTU − 20 을 IPv6 MTU 로 본다: RFC 4213 §3.2.2
# 노트의 예시: 문제 도식과 같다 — IPv4 경로 MTU 1500, 방화벽 자리.
# focal: 송신자가 추정을 1480 으로 낮추는 자리 — 본문이 짚는 "알림이 닿으면".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, BAD, INFO, ACC, SOFT, MONO
from _cc_04_04_pmtu import (frame, topology, step, send, chip, UP, DN, CHIP_Y, LEGEND_Y,
                            SND_CX, FW_CX, RT_CX, RCV_CX, DROP_X)

d = frame("IPV6 · PATH MTU DISCOVERY · RFC 8201",
          "알림이 닿으면 1480 으로 줄여 통과합니다",
          "문제 도식과 같은 망에서 방화벽이 ICMP 를 통과시킨다. 작은 패킷은 끝까지 간다. "
          "1500 바이트 패킷이 터널 입구에서 버려지고 라우터가 MTU 1480 을 적은 Packet Too Big 을 돌려보낸다. "
          "알림이 방화벽을 지나 송신자에게 닿고, 송신자는 경로 MTU 추정을 1480 으로 낮춘 뒤 1480 바이트로 보내 수신자까지 통과한다.",
          "위 그림과 같은 망입니다. 달라진 것은 방화벽이 알림을 통과시킨다는 한 가지입니다")

topology(d, "ICMP 통과", OK, "터널 입구")

# 1 · 작은 패킷은 끝까지 (문제 도식과 같음)
send(d, UP, SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, UP, 1, "SYN · 작은 패킷 통과", OK)

# 2 · 큰 패킷은 터널 앞에서 버려짐 (문제 도식과 같음)
send(d, DN[0], SND_CX, DROP_X, BAD, drop=BAD)
step(d, SND_CX + 24, DN[0], 2, "1500 B · 다음 링크보다 큼 · 버림", BAD)

# 3 · 알림이 방화벽을 지나 송신자까지
send(d, DN[1], RT_CX - 8, SND_CX, INFO, dash="5 4")
step(d, FW_CX + 40, DN[1], 3, "Packet Too Big · MTU 1480", INFO)

# 4 · 송신자가 추정을 낮추고  5 · 줄인 크기로 통과
send(d, DN[2], SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, DN[2], 4, "경로 MTU 1480 으로 낮춤", ACC)
step(d, RT_CX + 8, DN[2], 5, "1480 B · 통과", OK)
chip(d, RCV_CX, CHIP_Y, "데이터 받음", OK)

d.legend(LEGEND_Y, [("통과한 패킷", OK), ("버려진 패킷", BAD), ("ICMP 알림", INFO), ("줄인 추정 · 본문이 짚는 곳", ACC)])
d.t(960, 520, "RFC 8201 §3 §4 · RFC 4443 §3.2 · RFC 4213 §3.2.2", 8, SOFT, MONO, "end")
d.save("04-04.pmtud-solution.svg")
print("→ 04-04.pmtud-solution.svg")
