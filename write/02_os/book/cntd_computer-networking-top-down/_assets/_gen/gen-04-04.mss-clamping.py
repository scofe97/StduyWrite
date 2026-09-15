# 04-04 §1 「알림 없이 버티는 법」 — MSS 클램핑. 문제 · 해결 도식과 같은 노드 자리 · 트랙을 쓴다.
#       방화벽은 문제 도식처럼 ICMP 를 막은 채로 두고, 달라진 것은 터널 입구의 TCPMSS 규칙 하나다.
# 타입 스펙: type-architecture — 송신자 · 방화벽 · 터널 입구 라우터 · 수신자를 한 줄에 두고 번호 붙은 수평 화살표로 순서를 보인다.
# 출처: 원문 밖. 전부 1차 자료에서 가져왔다.
#       - TCPMSS 는 TCP SYN 패킷의 MSS 값을 바꾼다 · --clamp-mss-to-pmtu 는 경로 MTU − 60(IPv6): iptables-extensions(8)
#       - 커널은 목적지 쪽 경로 MTU 와 출발지 쪽 경로 MTU 중 작은 값에서 뺀다 · 이미 작으면 올리지 않는다:
#         linux net/netfilter/xt_TCPMSS.c (min(dst_mtu, in_mtu) − minlen, oldmss <= newmss 면 그대로)
#       - MSS 옵션은 SYN 이 켜진 세그먼트에만 싣는다 · 보내는 쪽은 상대가 알린 MSS 를 넘지 않는다: RFC 9293 §3.2 · §3.7.1
#       - IPv6 헤더 40 + TCP 헤더 20 이라 MSS 1440 = MTU 1500 − 60: 06-03 심화 학습 · RFC 9293 §3.7.1 (1220 = 1280 − 60)
# 노트의 예시: 양 끝 링크 MTU 1500 · 터널 안쪽 1480 은 문제 도식과 같다. 그래서 MSS 1440 → 1420.
# focal: 터널 입구가 SYN 의 MSS 를 1420 으로 고쳐 넘기는 화살표 — 본문이 짚는 "양 끝이 애초에 작게 쓴다".
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, BAD, INFO, ACC, MUTED, SOFT, MONO
from _cc_04_04_pmtu import (frame, topology, step, send, chip, UP, DN, CHIP_Y, LEGEND_Y,
                            SND_CX, FW_CX, RT_CX, RCV_CX, RT_X, RT_W)

d = frame("TCP · MSS CLAMPING · TCPMSS",
          "SYN 의 MSS 를 고치면 알림 없이도 들어맞습니다",
          "문제 도식과 같은 망이고 방화벽은 여전히 ICMP 를 막는다. 송신자가 MSS 1440 을 적은 SYN 을 보내면 "
          "터널 입구 라우터가 1420 으로 고쳐 수신자에게 넘긴다. 수신자의 SYN-ACK 도 1440 에서 1420 으로 고쳐 송신자에게 간다. "
          "이후 데이터는 세그먼트 1420 에 헤더 60 을 더한 1480 바이트라 터널에 들어맞고 Packet Too Big 이 생기지 않는다.",
          "방화벽은 그대로 ICMP 를 막습니다. 달라진 것은 터널 입구가 SYN 의 MSS 를 고친다는 한 가지입니다")

topology(d, "ICMP 막음", BAD, "TCPMSS 규칙", ACC)

RT_L, RT_R = RT_X - 4, RT_X + RT_W + 4

# 1 · SYN 은 1440 으로 출발  2 · 터널 입구가 1420 으로 고쳐 넘김
send(d, UP, SND_CX, RT_L, INFO)
step(d, SND_CX + 24, UP, 1, "SYN · MSS 1440", INFO)
send(d, UP, RT_R, RCV_CX, ACC)
step(d, RT_R + 24, UP, 2, "MSS 1420 으로 고침", ACC)

# 3 · SYN-ACK 도 1440 으로 오고  4 · 같은 규칙이 1420 으로 고쳐 돌려보냄
send(d, DN[0], RCV_CX, RT_R, INFO)
step(d, RT_R + 24, DN[0], 3, "SYN-ACK · MSS 1440", INFO)
send(d, DN[0], RT_L, SND_CX, INFO)
step(d, SND_CX + 24, DN[0], 4, "MSS 1420 으로 고침", INFO)

# 5 · 이후 데이터는 처음부터 1480 B
send(d, DN[1], SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, DN[1], 5, "세그먼트 1420 + 헤더 60 = 1480 B · 통과", OK)

chip(d, FW_CX, DN[2], "ICMP 는 여전히 막힘", MUTED)
chip(d, RT_CX, DN[2], "Packet Too Big 없음", OK)
chip(d, RCV_CX, DN[2], "데이터 받음", OK)

d.legend(LEGEND_Y, [("통과한 패킷", OK), ("SYN · SYN-ACK", INFO), ("고친 MSS · 본문이 짚는 곳", ACC), ("ICMP 막는 방화벽", BAD)])
d.t(960, 520, "IPTABLES-EXTENSIONS(8) TCPMSS · XT_TCPMSS.C · RFC 9293 §3.7.1", 8, SOFT, MONO, "end")
d.save("04-04.mss-clamping.svg")
print("→ 04-04.mss-clamping.svg")
