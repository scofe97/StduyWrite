# 04-04 §3 「PLPMTUD 와 tcp_mtu_probing 은 알림 대신 시험용 패킷으로 크기를 찾습니다」.
# 타입 스펙: type-architecture — 문제 도식과 같은 노드 자리 · 트랙을 쓰고, 방화벽은 여전히 ICMP 를 막는다.
#       달라진 것은 송신자가 알림을 기다리지 않고 시험용 패킷이 닿았는지(확인 응답)로 크기를 정한다는 한 가지다.
# 출처: 원문 밖. 전부 1차 자료에서 가져왔다.
#       - 패킷화 계층이 시험용 패킷을 보내 확인 응답으로 크기를 정하므로 PTB 가 오지 않아도 돈다: RFC 4821 · RFC 8900 §2.3
#       - 리눅스 tcp_mtu_probing 1 = 블랙홀 감지 시 켬 · 2 = 늘 켜고 초기 MSS 로 tcp_base_mss: ip-sysctl.rst
#       - TCP_BASE_MSS 기본값 1024: linux include/net/tcp.h
# 노트의 예시: 기본 크기 1084 B = MSS 1024 + IPv6 40 + TCP 20. 패킷 1500 · 1480 은 고른 값이고, 실제 패킷 크기는 구현이 정한다.
# focal: 1480 패킷에 돌아온 확인 응답 — 본문이 짚는 "알림 대신 시험용 패킷".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import D, OK, BAD, INFO, ACC, MUTED, SOFT, KR, MONO
from _cc_04_04_pmtu import (topology, step, send, chip, UP,
                            W, SND_CX, FW_CX, RT_CX, RCV_CX, DROP_X)

H = 640
TR = (288, 344, 400, 456, 512)     # stride 56
CHIP_Y, LEGEND_Y = 552, 584

d = D(W, H, "TCP · PLPMTUD · TCP_MTU_PROBING",
      "시험용 패킷이 닿았는지로 크기를 정합니다",
      "문제 도식과 같은 망이고 방화벽은 ICMP 를 막는다. 송신자는 기본 크기 1084 바이트로 보내 통과한다. "
      "1500 바이트 패킷은 터널 입구에서 버려지고 Packet Too Big 은 방화벽에서 막혀 확인 응답이 오지 않는다. "
      "1480 바이트 패킷은 통과해 수신자의 확인 응답이 돌아오고, 송신자는 경로 MTU 를 1480 으로 올린다.",
      "방화벽은 그대로 ICMP 를 막습니다. 송신자는 알림을 기다리지 않고 시험용 패킷에 확인 응답이 오는지를 봅니다")

topology(d, "ICMP 막음", BAD, "터널 입구")

# 1 · 기본 크기로 시작
send(d, UP, SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, UP, 1, "기본 MSS 1024 · 1084 B · 통과", OK)

# 2 · 큰 패킷은 버려지고  3 · 알림은 막힘
send(d, TR[0], SND_CX, DROP_X, BAD, drop=BAD)
step(d, SND_CX + 24, TR[0], 2, "패킷 1500 B · 버림", BAD)
send(d, TR[1], RT_CX - 8, FW_CX, INFO, dash="5 4", drop=ACC)
step(d, FW_CX + 40, TR[1], 3, "Packet Too Big · 막힘", INFO)

# 4 · 확인 응답이 없으니 그 크기는 안 됨
step(d, SND_CX + 24, TR[2], 4, "확인 응답 없음 · 1500 은 안 됨", ACC)

# 5 · 작은 패킷은 통과  6 · 확인 응답으로 크기를 올림
send(d, TR[3], SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, TR[3], 5, "패킷 1480 B · 통과", OK)
send(d, TR[4], RCV_CX, SND_CX, ACC)
step(d, SND_CX + 24, TR[4], 6, "확인 응답 · 경로 MTU 1480 으로", ACC)

chip(d, RCV_CX - 60, CHIP_Y, "Packet Too Big 없이 크기 결정", OK)

d.legend(LEGEND_Y, [("통과한 패킷", OK), ("버려진 시험용 패킷", BAD), ("막힌 알림", INFO), ("확인 응답 · 본문이 짚는 곳", ACC)])
d.t(960, H - 8, "RFC 4821 · RFC 8900 §2.3 · IP-SYSCTL TCP_MTU_PROBING · TCP.H TCP_BASE_MSS", 8, SOFT, MONO, "end")
d.save("04-04.plpmtud-probing.svg")
print("→ 04-04.plpmtud-probing.svg")
