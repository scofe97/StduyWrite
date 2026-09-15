# 04-04 §3 「MTU 1280 고정은 탐색 없이 IPv6 최소 크기로 보냅니다」.
# 타입 스펙: type-architecture — 문제 도식과 같은 노드 자리 · 트랙을 쓰고, 방화벽은 여전히 ICMP 를 막는다.
#       달라진 것은 송신자가 처음부터 1280 을 넘지 않게 보낸다는 한 가지이고, 대가는 경로가 허락하는 1480 을 안 쓰는 것이다.
# 출처: 원문 밖. 전부 1차 자료에서 가져왔다.
#       - 모든 IPv6 링크는 1280 이상 · 최소 구현은 1280 이하로만 보내고 PMTUD 를 빼도 됨: RFC 8200 §5
#       - 보수적 추정은 실제 경로 MTU 보다 작기 쉬워 위 계층 성능을 깎음: RFC 8900 §2.1
# 노트의 예시: 문제 도식과 같은 1500 · 1480 망. "패킷당 200 B" 는 이 망의 1480 − 1280 이다.
# focal: 쓰지 않은 200 B — 본문이 짚는 대가.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from dd import OK, BAD, INFO, ACC, MUTED, SOFT, MONO
from _cc_04_04_pmtu import (frame, topology, step, send, chip, UP, DN, CHIP_Y, LEGEND_Y,
                            SND_CX, FW_CX, RT_CX, RCV_CX)

d = frame("IPV6 · MINIMUM MTU 1280",
          "1280 을 넘지 않으면 어느 경로든 들어맞습니다",
          "문제 도식과 같은 망이고 방화벽은 ICMP 를 막는다. 송신자가 경로 MTU 를 1280 으로 고정하고 1280 바이트로 보내면 "
          "방화벽과 터널 입구를 모두 지나 Packet Too Big 이 생기지 않는다. 모든 IPv6 링크는 1280 이상이라 탐색이 필요 없다. "
          "대신 이 경로가 허락하는 1480 바이트는 쓰지 않아 패킷마다 200 바이트를 덜 싣는다.",
          "방화벽은 그대로 ICMP 를 막습니다. 송신자가 처음부터 1280 을 넘지 않게 보냅니다")

topology(d, "ICMP 막음", BAD, "터널 입구")

# 1 · 1280 으로 고정해 보냄
send(d, UP, SND_CX, RCV_CX, OK)
step(d, SND_CX + 24, UP, 1, "MTU 1280 고정 · 1280 B · 통과", OK)

chip(d, FW_CX, DN[0], "ICMP 막혀도 무관", MUTED)
chip(d, RT_CX, DN[0], "Packet Too Big 없음", OK)

# 2 · 경로가 허락하는 크기는 쓰지 않음
send(d, DN[1], SND_CX, RCV_CX, MUTED, dash="5 4")
step(d, SND_CX + 24, DN[1], 2, "경로가 허락하는 1480 B · 쓰지 않음", MUTED)

chip(d, SND_CX + 60, DN[2], "탐색 없음", OK)
chip(d, RCV_CX - 60, DN[2], "패킷당 200 B 덜 실음", BAD)
chip(d, SND_CX + 130, CHIP_Y, "IPv6 링크는 모두 1280 이상", INFO)

d.legend(LEGEND_Y, [("통과한 패킷", OK), ("쓰지 않는 크기", MUTED), ("대가 · 본문이 짚는 곳", BAD), ("규격이 보장하는 바닥", INFO)])
d.t(960, 520, "RFC 8200 §5 · RFC 8900 §2.1", 8, SOFT, MONO, "end")
d.save("04-04.mtu-1280-fixed.svg")
print("→ 04-04.mtu-1280-fixed.svg")
