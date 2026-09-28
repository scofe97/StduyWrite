# 05-03 A3 — 서버의 dnsmasq 를 끄고 요청한 캡처. 값은 a3-neighbor.pcap 과 udhcpc 출력 그대로다.
# 타입 스펙: type-sequence — 같은 DISCOVER 네 번 뒤 클라이언트가 스스로 실패를 판단한다. focal 은 그 판단.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", True), ("cl", "클라이언트", "udhcpc -t 4 -T 2", False), ("sv", "서버 .20", "dnsmasq 꺼짐", False)]
y = [216 + i * ROW for i in range(6)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 A3",
           "A3 — 답이 없을 때 DISCOVER 만 반복",
           "서버의 dnsmasq 를 멈춘 채 클라이언트가 주소를 요청한다. 같은 트랜잭션 ID 의 DISCOVER 가 약 2초 간격으로 네 번 나가고 답은 한 줄도 없다. 꺼진 서버는 없다는 사실을 알릴 수단이 없으므로, 클라이언트가 횟수와 시간이 다 지난 것으로 실패를 판단한다.",
           "실패를 알리는 메시지는 없고, 클라이언트가 기다림을 끝낼 뿐입니다", L)
d.rails(y[-1] + 24)
d.note("sv", "dnsmasq 중지", y[0] - 8, WARN)
d.bcast("cl", "DISCOVER 1", y[1], INFO, "xid 0x309d8c09", t="0.000")
d.bcast("cl", "DISCOVER 2", y[2], INFO, "같은 xid", t="2.007")
d.bcast("cl", "DISCOVER 3", y[3], INFO, "같은 xid", t="4.017")
d.bcast("cl", "DISCOVER 4", y[4], INFO, "같은 xid", t="6.024")
d.note("cl", "no lease, failing", y[5], focal=True)
d.legend(H - 44, [("브로드캐스트", INFO), ("꺼진 서버", WARN), ("클라이언트의 실패 판단", ACC)])
d.save("05-03.a3-no-server.svg")
