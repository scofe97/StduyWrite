# 05-03 A2 — A1 과 같은 교환을 옆자리(dhcp-neighbor)에서 잡은 세 줄. 값은 a1-neighbor.pcap 표 그대로다.
# 타입 스펙: type-sequence — 옆자리가 캡처 지점. 선 위의 교환 전체를 그리고 옆자리에 찍힌 것만 실선으로 둔다.
#           focal 은 REQUEST(고르지 않은 서버도 들어야 해서 브로드캐스트인 자리).
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", True), ("cl", "클라이언트", "udhcpc", False), ("sv", "서버 .20", "dnsmasq", False)]
y = [216 + i * ROW for i in range(7)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 A2",
           "A2 — 옆자리 캡처에 남은 세 줄",
           "A1 의 교환 일곱 줄 가운데 옆자리 캡처에 남은 것은 DISCOVER 둘과 REQUEST 하나, 모두 브로드캐스트다. 클라이언트 MAC 앞으로 간 ICMP·OFFER·ACK 와 받은 주소로 나간 ping 은 스위치가 옆자리 포트로 보내지 않아 없다.",
           "실선은 옆자리에 찍힌 프레임, 점선은 선 위에만 있던 프레임입니다", L)
d.rails(y[-1] + 24)
d.bcast("cl", "DISCOVER", y[0], INFO, "ff:ff:ff:ff:ff:ff")
d.bcast("cl", "DISCOVER 재전송", y[1], INFO, "옆자리에도 둘 · 실제 재전송")
d.msg("sv", "cl", "ICMP → .137", y[2], sub="클라이언트 MAC 앞", missing=True)
d.msg("sv", "cl", "OFFER", y[3], sub="클라이언트 MAC 앞", missing=True)
d.bcast("cl", "REQUEST", y[4], ACC, "옵션 54 = .20 · 50 = .137")
d.msg("sv", "cl", "ACK", y[5], sub="클라이언트 MAC 앞", missing=True)
d.msg("cl", "sv", "ping", y[6], sub="서버 MAC 앞", missing=True)
d.legend(H - 44, [("옆자리에 찍힌 브로드캐스트", INFO), ("옆자리에 없는 유니캐스트", SOFT), ("모든 서버가 듣는 REQUEST", ACC)])
d.save("05-03.a2-neighbor-view.svg")
