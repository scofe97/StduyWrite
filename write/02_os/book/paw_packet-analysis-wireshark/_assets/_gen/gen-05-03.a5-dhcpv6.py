# 05-03 A5 — dhclient -6 으로 SARR 한 번, rapid commit 으로 한 번. 옆자리 캡처(a5-neighbor.pcap)와 dhclient 로그 값 그대로다.
# 타입 스펙: type-sequence — 멀티캐스트 ff02::1:2 는 옆자리에 찍히고 서버의 유니캐스트 답은 로그에만 있다.
#           focal 은 옵션 14 가 붙은 두 번째 SOLICIT.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", True), ("cl", "클라이언트", "dhclient -6", False), ("sv", "서버", "dnsmasq · fd00:55::20", False)]
y = [236, 288, 340, 392, 444, 524, 576]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 A5",
           "A5 — DHCPv6 의 네 걸음과 두 걸음",
           "위는 기본 SARR 네 걸음과 반납, 아래는 rapid commit 두 걸음이다. 클라이언트는 링크 로컬 주소에서 멀티캐스트 ff02::1:2 로 보내 옆자리에도 찍히고, 서버의 ADVERTISE·REPLY 는 유니캐스트라 dhclient 로그에만 남는다. IPv4 와 달리 걸음마다 트랜잭션 ID 가 새로 매겨진다.",
           "브로드캐스트 자리를 멀티캐스트 ff02::1:2 가 대신합니다", L)
d.rails(y[-1] + 24)
d.divider(y[0] - 28, "== SARR")
d.bcast("cl", "SOLICIT", y[0], INFO, "→ ff02::1:2 · xid 0xcf33cd")
d.msg("sv", "cl", "ADVERTISE", y[1], sub="유니캐스트 · 로그의 RCV", missing=True)
d.bcast("cl", "REQUEST", y[2], INFO, "새 xid 0x3c05ce")
d.msg("sv", "cl", "REPLY", y[3], sub="로그의 Bound", missing=True)
d.bcast("cl", "RELEASE", y[4], INFO, "dhclient -r · xid 0x375726")
d.divider(y[5] - 28, "== RAPID")
d.bcast("cl", "SOLICIT + 옵션 14", y[5], ACC, "rapid commit · xid 0xdfd776")
d.msg("sv", "cl", "REPLY", y[6], sub="두 걸음째 · 로그에만", missing=True)
d.legend(H - 44, [("옆자리에 찍힌 멀티캐스트", INFO), ("옆자리에 없는 유니캐스트", SOFT), ("rapid commit SOLICIT", ACC)])
d.save("05-03.a5-dhcpv6.svg")
