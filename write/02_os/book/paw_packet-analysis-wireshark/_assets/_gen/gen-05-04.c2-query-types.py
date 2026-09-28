# 05-04 C2 — dig 로 질의 타입만 바꿔 물은 c2-client.pcap 17 프레임(질의·응답 여덟 쌍, 첫 질의는 두 번 찍힘).
# 타입 스펙: type-sequence — 두 주체 사이의 질의·응답 왕복. 이름별 질의와 도메인 기록 질의를 구획으로 나눈다.
#           focal(accent)은 www 한 번의 질의에 CNAME 과 주소가 함께 담겨 돌아온 9번 응답.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, OK, INFO

C, S = "dhcp-client", "dhcp-server"
d = LabSeq(height(9, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C2",
           "C2 — 질의 타입과 CNAME 체인",
           "같은 서버에 타입만 바꿔 여덟 번 묻는다. multi 는 A 가 두 줄, www 는 CNAME 과 A 가 한 응답에 함께 오고 web.lab.test 를 따로 묻는 질의는 없다.",
           "왼쪽 #숫자는 c2-client.pcap 의 프레임 번호입니다")
d.cast([(C, "10.55.0.137 · dig"), (S, "10.55.0.20 · dnsmasq :53")], 260, capture=C)

y = d.region("이름별 질의 넷", 7)
d.msg(C, S, "질의 A · AAAA web.lab.test", y, MUTED, tag="#1·2·4")
d.msg(S, C, "답 1줄씩 · A 10.55.0.20 · AAAA fd00:55::20", y + STRIDE, MUTED, "ar", "5 3", tag="#3·5")
d.msg(C, S, "질의 A multi.lab.test", y + 2 * STRIDE, MUTED, tag="#6")
d.msg(S, C, "answers 2 · A .41 · A .42", y + 3 * STRIDE, INFO, "info", "5 3", sub="같은 이름에 A 두 줄", tag="#7")
d.msg(C, S, "질의 A www.lab.test", y + 4 * STRIDE, MUTED, sub="answers 0", tag="#8")
d.msg(S, C, "answers 2 · CNAME web.lab.test · A 10.55.0.20", y + 5 * STRIDE, ACC, "acc", "5 3", sub="서버가 체인을 따라가 주소까지 담음", tag="#9", lw=1.8)
d.note(C, "web.lab.test 재질의 없음", y + 6 * STRIDE, OK)

y = d.region("도메인 lab.test 에 딸린 기록", 2)
d.msg(C, S, "질의 MX · TXT · NS · SOA", y, MUTED, tag="#10~16")
d.msg(S, C, "답 1줄씩", y + STRIDE, MUTED, "ar", "5 3", tag="#11~17")

d.finish([("한 응답에 담긴 체인", ACC), ("같은 이름의 여러 답", INFO), ("클라이언트가 하지 않은 일", OK)], "05-04.c2-query-types.svg")
