# 04-04 §1 「줄이라는 알림이 오지 않으면」 — 문제 도식. 같은 골격의 해결 도식(gen-04-04.pmtud-solution.py)보다 앞에 둔다.
# 타입 스펙: type-architecture — 송신자 · 방화벽 · 터널 입구 라우터 · 수신자를 한 줄에 두고 번호 붙은 수평 화살표로 순서를 보인다.
#       2026-09-14: type-sequence(gen-04-04.pmtud-blackhole.py)에서 바꿨다. 레인만 남아 망 모양과 알림이 막히는 자리가 안 보였다.
# 출처: 원문 §4.3.4 "the router simply drops the datagram and sends a "Packet Too Big" ICMP error message ... back to the sender".
#       원문 밖 사실은 전부 RFC 에서 가져왔다.
#       - 터널 입구는 IPv4 경로 MTU − 20 을 IPv6 MTU 로 보고 그보다 큰 패킷에 PTB 를 돌려준다: RFC 4213 §3.2 · §3.2.2
#       - ICMP 를 막는 방화벽 · 알림이 없으면 같은 크기 재전송만 되풀이 · 작은 SYN 은 지나감: RFC 2923 §2.1
#       - 핸드셰이크는 끝나고 데이터에서 멈추는 상태를 블랙홀 연결이라 부른다: RFC 8201 §1
# 노트의 예시: IPv4 경로 MTU 1500(그래서 터널 안쪽 1480), 방화벽이 송신자와 터널 입구 사이에 있는 배치는 고른 값이다.
#       재전송 한 줄은 표시일 뿐 횟수가 아니다(RFC 2923 트레이스는 열세 번).
# focal: 방화벽에서 막힌 Packet Too Big — 본문이 짚는 "알림이 오지 않으면".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, BAD, INFO, ACC, MUTED, SOFT, MONO
from _cc_04_04_pmtu import (frame, topology, step, send, chip, UP, DN, CHIP_Y, LEGEND_Y,
                            SND_CX, FW_CX, RT_CX, RCV_CX, DROP_X)

d = frame("IPV6 · PATH MTU · BLACK HOLE",
          "알림이 막히면 같은 크기로 되풀이하다 멈춥니다",
          "송신자와 수신자 사이에 방화벽과 터널 입구 라우터가 있고 터널 안쪽 MTU 는 1480 이다. "
          "작은 SYN 은 끝까지 간다. 1500 바이트 패킷은 터널 입구에서 버려지고 라우터가 Packet Too Big 을 돌려보내지만 "
          "ICMP 를 막는 방화벽에서 사라진다. 송신자는 같은 1500 바이트를 다시 보내고 또 버려진다.",
          "작은 패킷은 끝까지 가고 큰 패킷만 터널 앞에서 버려집니다. 줄이라는 알림은 방화벽에서 사라집니다")

topology(d, "ICMP 막음", BAD, "터널 입구")

# 1 · 작은 패킷은 끝까지
send(d, UP, SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, UP, 1, "SYN · 작은 패킷 통과", OK)

# 2 · 큰 패킷은 터널 앞에서 버려짐
send(d, DN[0], SND_CX, DROP_X, BAD, drop=BAD)
step(d, SND_CX + 24, DN[0], 2, "1500 B · 다음 링크보다 큼 · 버림", BAD)
chip(d, RCV_CX, DN[0], "큰 데이터 못 받음", BAD)

# 3 · 라우터가 알림을 보내고  4 · 방화벽이 막음
send(d, DN[1], RT_CX - 8, FW_CX, INFO, dash="5 4", drop=ACC)
step(d, FW_CX + 40, DN[1], 3, "Packet Too Big · MTU 1480", INFO)
step(d, SND_CX + 24, DN[1], 4, "ICMP 막힘", ACC)

# 5 · 모르는 송신자는 같은 크기를 다시
send(d, DN[2], SND_CX, DROP_X, BAD, drop=BAD)
step(d, SND_CX + 24, DN[2], 5, "같은 1500 B 재전송 · 또 버림", BAD)
chip(d, SND_CX + 60, CHIP_Y, "블랙홀 연결", BAD)

d.legend(LEGEND_Y, [("통과한 패킷", OK), ("버려진 패킷", BAD), ("ICMP 알림", INFO), ("막힌 알림 · 본문이 짚는 곳", ACC)])
d.t(960, 520, "RFC 4213 §3.2.2 · RFC 2923 §2.1 · RFC 8201 §1", 8, SOFT, MONO, "end")
d.save("04-04.pmtud-problem.svg")
print("→ 04-04.pmtud-problem.svg")
