# 05-04 C1 — 없는 이름과 닫힌 포트를 클라이언트 쪽에서 잡은 c1-client.pcap 여섯 프레임.
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 메시지. 두 시도를 구획으로 나눈다.
#           focal(accent)은 81번 SYN 에 커널이 바로 돌려준 RST·ACK 하나.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, WARN, INFO, BAD

C, S = "dhcp-client", "dhcp-server"
d = LabSeq(height(7, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C1",
           "C1 — 이름 실패와 연결 실패",
           "없는 이름 nope.lab.test 는 DNS 응답 rcode 3 에서 멈춰 SYN 이 나가지 않는다. 있는 이름 web.lab.test 의 81번은 SYN 에 RST·ACK 가 곧바로 돌아온다.",
           "왼쪽 #숫자는 c1-client.pcap 의 프레임 번호입니다")
d.cast([(C, "10.55.0.137 · curl"), (S, "10.55.0.20 · dnsmasq :53")], 260, capture=C)

y = d.region("없는 이름 · nope.lab.test", 3)
d.msg(C, S, "질의 A nope.lab.test", y, MUTED, tag="#1")
d.msg(S, C, "NXDOMAIN · rcode 3", y + STRIDE, WARN, "warn", "5 3", tag="#2")
d.note(C, "SYN 없음 · curl exit 6", y + 2 * STRIDE, WARN)

y = d.region("있는 이름 · 닫힌 81번", 4)
d.msg(C, S, "질의 A web.lab.test", y, MUTED, tag="#3")
d.msg(S, C, "rcode 0 · A 10.55.0.20", y + STRIDE, MUTED, "ar", "5 3", tag="#4")
d.msg(C, S, "SYN → 81", y + 2 * STRIDE, INFO, "info", tag="#5")
d.msg(S, C, "RST·ACK", y + 3 * STRIDE, ACC, "acc", sub="LISTEN 소켓 없음 · 커널 TCP 스택 · curl exit 7", tag="#6", lw=1.8)

d.finish([("포트 확인이 끝나는 지점", ACC), ("이름에서 멈춤", WARN), ("연결 시도", INFO)], "05-04.c1-name-vs-connect.svg")
