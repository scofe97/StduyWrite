# 05-03 B2 — 범위를 옮긴 서버에 옛 주소를 REQUEST. 값은 b2-neighbor.pcap 과 서버 로그 그대로다.
# 타입 스펙: type-sequence — REQUEST → NAK → DISCOVER 부터 다시. focal 은 브로드캐스트 NAK.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", True), ("cl", "클라이언트", "dhclient", False), ("sv", "서버 .20", "범위 .160~.170", False)]
y = [216 + i * ROW for i in range(7)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 B2",
           "B2 — 옛 주소 요청에 돌아온 NAK",
           "임대 기록 파일로 옛 주소 .137 을 기억한 dhclient 가 DISCOVER 없이 REQUEST 부터 보낸다. 범위를 옮긴 authoritative 서버는 1ms 뒤 NAK 을 브로드캐스트하고, 클라이언트는 DISCOVER 부터 다시 돌아 .166 을 받는다.",
           "REQUEST 만으로는 주소를 쓰지 않고, ACK 를 받은 뒤에 씁니다", L)
d.rails(y[-1] + 24)
d.bcast("cl", "REQUEST", y[0], INFO, "옵션 50 = .137 · 옛 주소", t="0.000")
d.bcast("sv", "NAK", y[1], ACC, "address not available", t="0.001", label_to="cl")
d.bcast("cl", "DISCOVER ×2", y[2], INFO, "2.603 에 한 번 더", t="0.008")
d.msg("sv", "cl", "OFFER .166", y[3], sub="유니캐스트", missing=True)
d.bcast("cl", "REQUEST", y[4], INFO, "옵션 50 = .166", t="3.033")
d.msg("sv", "cl", "ACK .166", y[5], sub="유니캐스트", missing=True)
d.note("cl", "bound .166", y[6])
d.legend(H - 44, [("브로드캐스트", INFO), ("옆자리에 없음", SOFT), ("브로드캐스트 NAK", ACC)])
d.save("05-03.b2-nak.svg")
