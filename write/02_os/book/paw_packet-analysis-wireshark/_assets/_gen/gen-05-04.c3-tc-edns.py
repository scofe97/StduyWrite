# 05-04 C3 — big.lab.test TXT 를 +noedns 와 기본값(EDNS) 으로 한 번씩 물은 c3-client.pcap.
# 타입 스펙: type-sequence — 같은 질의를 두 방식으로 보낸 두 구간. 위 구간은 UDP → TCP 로 갈아타고 아래 구간은 UDP 한 번에 끝난다.
#           focal(accent)은 OPT 기록 덕에 944바이트가 UDP 한 번에 온 15번 응답.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, WARN, INFO

C, S = "dhcp-client", "dhcp-server"
d = LabSeq(height(8, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C3",
           "C3 — TC 표시 뒤 TCP 재질의, EDNS(0) 는 한 번",
           "OPT 기록이 없는 질의에는 서버가 512바이트 한계를 적용해 TC=1 로 답하고 클라이언트가 TCP 로 다시 묻는다. 1232바이트를 알린 질의에는 944바이트 응답이 UDP 한 번에 온다.",
           "왼쪽 #숫자는 c3-client.pcap 의 프레임 번호, 끝의 B 는 frame.len 입니다")
d.cast([(C, "10.55.0.137 · dig"), (S, "10.55.0.20 · dnsmasq :53")], 260, capture=C)

y = d.region("+noedns · 옛 512바이트 한계", 6)
d.msg(C, S, "UDP 질의 · 42115 → 53 · 72B", y, MUTED, tag="#1")
d.msg(S, C, "UDP 응답 · TC=1 · 답 0줄 · rcode 0 · 72B", y + STRIDE, WARN, "warn", "5 3", sub="실패 아님 · 이 패킷에 못 담았다는 표시", tag="#3")
d.msg(C, S, "TCP 3-way · 32827 ↔ 53", y + 2 * STRIDE, INFO, None, tag="#4~6")  # 양방향 왕복을 한 줄로 요약 — 화살촉 없음
d.msg(C, S, "TCP 위로 같은 질의 · 98B", y + 3 * STRIDE, INFO, "info", tag="#7")
d.msg(S, C, "TCP 응답 · 답 1줄 · 959B", y + 4 * STRIDE, INFO, "info", "5 3", tag="#9")
d.msg(C, S, "연결 종료 · FIN · FIN · ACK", y + 5 * STRIDE, MUTED, None, tag="#11~13")

y = d.region("EDNS(0) · 기본값", 2)
d.msg(C, S, "UDP 질의 + OPT · udp_payload_size 1232 · 95B", y, MUTED, tag="#14")
d.msg(S, C, "UDP 응답 · TC 없음 · 답 1줄 · 944B", y + STRIDE, ACC, "acc", "5 3", tag="#15", lw=1.8)

d.finish([("UDP 한 번에 끝난 응답", ACC), ("잘림 표시", WARN), ("TCP 로 다시 묻는 구간", INFO)], "05-04.c3-tc-edns.svg")
