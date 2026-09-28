# 05-03 B4 — 옆자리에 손으로 붙인 .137 을 서버의 ICMP(B4a)와 클라이언트의 ARP(B4b)가 각각 걸러낸다.
# 값은 b4a-server.pcap · b4b-neighbor.pcap 표 그대로다.
# 타입 스펙: type-sequence — 위아래 두 구획(B4a · B4b). focal 은 B4b 의 DECLINE 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", ".137 수동 설정", False), ("cl", "클라이언트", "udhcpc", False), ("sv", "서버 .20", "dnsmasq", False)]
ya = [240 + i * ROW for i in range(6)]
yb = [ya[-1] + 88 + i * ROW for i in range(7)]
H = yb[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 B4",
           "B4 — 남이 쓰는 주소를 거르는 두 자리",
           "위 구획은 서버가 제안 전에 ICMP 로 .137 을 묻고 옆자리의 응답을 받아 .138 로 넘어가는 B4a, 아래 구획은 서버 확인을 끄고 클라이언트가 ACK 뒤 ARP 로 묻다가 응답을 받아 DECLINE 을 보내는 B4b 다. DECLINE 뒤 20초를 쉬고 재시작한 교환에서 서버는 .138 을 제안한다.",
           "서버는 제안 전에 ICMP 로, 클라이언트는 ACK 뒤에 ARP 로 묻습니다", L)
d.rails(yb[-1] + 24)
d.divider(ya[0] - 28, "B4a · 서버 캡처 · 서버가 ICMP 확인")
d.bcast("cl", "DISCOVER", ya[0], INFO, t="0.000")
d.msg("sv", "nb", "ICMP → .137", ya[1], MUTED, t="0.001")
d.msg("nb", "sv", "응답", ya[2], WARN, "옆자리 MAC 9e:62:0b:21:94:67", t="0.001")
d.bcast("cl", "DISCOVER 재전송", ya[3], INFO, t="3.006")
d.note("sv", "ICMP → .138 · 응답 없음", ya[4], t="3.017")
d.msg("sv", "cl", "OFFER · ACK .138", ya[5], MUTED, "ACK 는 3.021", t="3.017")
d.divider(yb[0] - 28, "B4b · 옆자리 캡처 · --no-ping · udhcpc -a")
d.bcast("cl", "DISCOVER · REQUEST .137", yb[0], INFO, "OFFER · ACK 는 유니캐스트", t="0.000")
d.bcast("cl", "ARP 요청 .137 누구?", yb[1], INFO, "출발지 0.0.0.0", t="0.022", label_to="nb")
d.msg("nb", "cl", "ARP 응답 · 나야", yb[2], WARN, "클라이언트 MAC 앞", t="0.022")
d.bcast("cl", "DECLINE .137", yb[3], ACC, "새 xid 0xf5ce5e18", t="0.023")
d.note("cl", "20초 대기", yb[4])
d.bcast("cl", "DISCOVER · REQUEST .138", yb[5], INFO, t="20.046")
d.bcast("cl", "ARP 요청 .138", yb[6], INFO, "응답 없음", t="20.058", label_to="nb")
d.legend(H - 44, [("브로드캐스트", INFO), ("유니캐스트", MUTED), ("충돌 신호", WARN), ("클라이언트의 DECLINE", ACC)])
d.save("05-03.b4-conflict.svg")
