# 05-03 A1 — 정상 DORA 를 서버 쪽에서 잡은 일곱 줄. 값은 a1-server.pcap 표 그대로다.
# 타입 스펙: type-sequence — 옆자리 · 클라이언트 · 서버 레인, 위에서 아래로 시간.
#           focal 은 OFFER 한 줄(주소 없는 클라이언트에게 MAC 으로 꽂히는 자리).
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO

L = [("nb", "옆자리", "dhcp-neighbor", False), ("cl", "클라이언트", "udhcpc", False), ("sv", "서버 .20", "dnsmasq", True)]
y = [216 + i * ROW for i in range(7)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 A1",
           "A1 — 주소 없는 클라이언트에게 가는 OFFER",
           "서버 쪽 캡처에 찍힌 DORA 네 걸음과 앞뒤 프레임. 클라이언트는 DISCOVER 와 REQUEST 를 브로드캐스트로 외치고, 서버는 아직 IP 가 없는 클라이언트에게 OFFER 와 ACK 를 클라이언트 MAC 앞으로 보낸다. 받은 주소 .137 로 나간 ping 이 마지막 줄이다.",
           "외치는 쪽은 클라이언트, 서버의 답은 클라이언트 MAC 한 곳으로 갑니다", L)
d.rails(y[-1] + 24)
d.bcast("cl", "DISCOVER", y[0], INFO, "yiaddr 0.0.0.0", t="0.000")
d.bcast("cl", "DISCOVER 재전송", y[1], INFO, "같은 트랜잭션 ID", t="3.008")
d.msg("sv", "cl", "ICMP → .137", y[2], MUTED, "주소를 내주기 전 확인", t="3.017")
d.msg("sv", "cl", "OFFER · yiaddr .137", y[3], ACC, "eth.dst c6:68:75:04:f6:c1", t="3.017")
d.bcast("cl", "REQUEST", y[4], INFO, "옵션 54 = .20 · 50 = .137", t="3.017")
d.msg("sv", "cl", "ACK", y[5], MUTED, "yiaddr .137 확정 · 임대 120초", t="3.024")
d.msg("cl", "sv", "ping", y[6], MUTED, "출발지 10.55.0.137")
d.legend(H - 44, [("브로드캐스트", INFO), ("유니캐스트", MUTED), ("MAC 으로 꽂히는 OFFER", ACC)])
d.save("05-03.a1-dora-mac.svg")
