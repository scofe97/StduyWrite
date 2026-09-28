# 05-03 B3 — 주소 하나뿐인 풀을 dhcp-client 가 가져간 뒤 dhcp-client2 가 요청. 값은 b3-neighbor.pcap 과 서버 로그 그대로다.
# 타입 스펙: type-sequence — DISCOVER 셋, 선 위의 답은 없고 서버 로그에만 사유가 남는다. focal 은 그 로그.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", True), ("cl", "둘째 클라이언트", "dhcp-client2", False), ("sv", "서버 .20", "범위 .100 하나", False)]
y = [216 + i * ROW for i in range(5)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 B3",
           "B3 — 빈 풀 앞의 침묵",
           "하나뿐인 .100 을 dhcp-client 가 먼저 가져간 뒤 dhcp-client2 가 요청한다. 옆자리 캡처에는 DISCOVER 셋만 남고 서버의 답은 NAK 도 없다. 서버가 무엇을 했는지는 로그의 no address available 세 줄에만 있다.",
           "캡처만으로는 서버가 꺼진 A3 와 구분되지 않습니다", L)
d.rails(y[-1] + 24)
d.note("sv", ".100 · dhcp-client 에 임대", y[0] - 8)
d.bcast("cl", "DISCOVER 1", y[1], INFO, "b2:19:84:90:96:fa", t="0.000")
d.bcast("cl", "DISCOVER 2", y[2], INFO, "같은 MAC", t="2.006")
d.bcast("cl", "DISCOVER 3", y[3], INFO, "같은 MAC", t="4.011")
d.note("sv", "로그 · no address available ×3", y[4], focal=True)
d.legend(H - 44, [("브로드캐스트", INFO), ("선 밖에만 남은 사유", ACC)])
d.save("05-03.b3-empty-pool.svg")
