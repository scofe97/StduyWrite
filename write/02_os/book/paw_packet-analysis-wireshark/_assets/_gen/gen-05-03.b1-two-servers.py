# 05-03 B1 — 서버 둘이 함께 제안하고 클라이언트가 첫째를 고른다. 캡처는 진 쪽(dhcp-server2)의 b1-server2.pcap, 선 밖은 두 서버의 로그·임대 기록.
# 타입 스펙: type-sequence — 클라이언트 · 첫째 서버 · 둘째 서버. focal 은 REQUEST 뒤 둘째 서버의 침묵.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("cl", "클라이언트", "udhcpc", False), ("s1", "첫째 서버 .20", "범위 .100~.150", False), ("s2", "둘째 서버 .21", "범위 .200~.220", True)]
y = [216 + i * ROW for i in range(7)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 B1",
           "B1 — 두 제안을 REQUEST 하나가 정리",
           "두 서버가 각각 .137 과 .207 을 제안하고, 클라이언트는 옵션 54 에 첫째 서버를 적은 REQUEST 를 브로드캐스트한다. 둘째 서버는 그 REQUEST 를 듣고도 아무것도 보내지 않으며 임대 기록도 남기지 않는다. 첫째 서버의 OFFER·ACK 는 클라이언트 MAC 앞 유니캐스트라 둘째 서버 캡처에 없다.",
           "고르지 않은 서버는 거절하지 않고 물러납니다", L)
d.rails(y[-1] + 24)
d.bcast("cl", "DISCOVER ×2", y[0], INFO, "두 서버 모두 수신")
d.msg("s1", "cl", "OFFER .137", y[1], sub="클라이언트 MAC 앞 · 첫째 서버 로그", missing=True)
d.msg("s2", "cl", "OFFER .207", y[2], MUTED, "둘째 서버의 제안")
d.bcast("cl", "REQUEST", y[3], INFO, "옵션 54 = .20 · 50 = .137")
d.msg("s1", "cl", "ACK .137", y[4], sub="첫째 서버 로그", missing=True)
d.note("s2", "응답 없음 · 임대 기록 빈 칸", y[5], focal=True)
d.note("s1", "임대 기록 .137 한 줄", y[6])
d.legend(H - 44, [("브로드캐스트", INFO), ("유니캐스트", MUTED), ("이 캡처에 없음", SOFT), ("진 서버의 침묵", ACC)])
d.save("05-03.b1-two-servers.svg")
