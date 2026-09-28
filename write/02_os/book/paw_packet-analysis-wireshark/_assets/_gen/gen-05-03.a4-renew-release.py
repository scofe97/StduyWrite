# 05-03 A4 — DORA 뒤 SIGUSR1 로 갱신, SIGUSR2 로 반납. 값은 a4-server.pcap 의 7~9번 그대로다.
# 타입 스펙: type-sequence — 시그널(선 밖)과 그에 따른 유니캐스트 교환. focal 은 갱신을 닫는 ACK.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _lab_seq import LabSeq, ROW, W
from dd import ACC, MUTED, INFO, WARN, SOFT
L = [("nb", "옆자리", "dhcp-neighbor", False), ("cl", "클라이언트", "udhcpc -b", False), ("sv", "서버 .20", "dnsmasq", True)]
y = [236 + i * ROW for i in range(7)]
H = y[-1] + 96
d = LabSeq(H, "PACKET ANALYSIS WITH WIRESHARK · 05-03 A4",
           "A4 — 갱신 둘, 반납 하나",
           "A1 과 같은 DORA(1~6번) 뒤, 시그널로 갱신과 반납을 시킨다. 갱신은 REQUEST 와 ACK 두 개의 유니캐스트이고 ciaddr 에 자기 주소가 들어간다. 반납은 새 트랜잭션 ID 의 RELEASE 하나이며 서버는 답하지 않는다.",
           "주소와 서버를 이미 아는 단계라 외치지 않고 서버에게 바로 보냅니다", L)
d.rails(y[-1] + 24)
d.divider(y[0] - 16, "1~6번 · A1 과 같은 DORA")
d.note("cl", "kill -USR1 · 갱신", y[0] + 8)
d.msg("cl", "sv", "REQUEST (갱신)", y[1] + 8, MUTED, "ciaddr .137 · xid 0x7ca7dc24", t="5.038")
d.msg("sv", "cl", "ACK", y[2] + 8, ACC, "같은 xid 0x7ca7dc24", t="5.040")
d.note("cl", "kill -USR2 · 반납", y[3] + 8)
d.msg("cl", "sv", "RELEASE", y[4] + 8, MUTED, "ciaddr .137 · 새 xid 0xcf0b0c37", t="7.039")
d.note("sv", "응답 없음", y[5] + 8, WARN)
d.note("cl", "ip -4 addr · 빈 출력", y[6] + 8)
d.legend(H - 44, [("유니캐스트", MUTED), ("두 개로 끝나는 갱신", ACC), ("답하지 않는 반납", WARN)])
d.save("05-03.a4-renew-release.svg")
