# 05-04 C7 (책 밖) — 1.1.1.1 에 example.com 을 평문 DNS 와 DoT 로 한 번씩 물은 c7-client.pcap.
# 타입 스펙: type-sequence — 같은 질의를 두 전송으로 보낸 두 구간. 평문 쪽은 이름이 보이고 DoT 쪽은 상대(1.1.1.1:853)만 보인다.
#           focal(accent)은 질의 이름을 품은 채 암호화된 Application Data.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, WARN, INFO

C, R = "dhcp-client", "1.1.1.1"
d = LabSeq(height(7, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C7",
           "C7 — 평문 DNS 와 DoT 에서 보이는 것",
           "평문 DNS 는 질의 이름 example.com 이 선에 그대로 실린다. DoT 는 누구에게 물었나(1.1.1.1:853)만 보이고 이름은 Application Data 안에 암호화된다. IP 로 붙어 SNI 도 비어 있다.",
           "왼쪽 #숫자는 c7-client.pcap 의 프레임 번호입니다")
d.cast([(C, "10.55.0.137 · dig"), (R, "Cloudflare 공개 리졸버")], 260, capture=C)

y = d.region("평문 DNS · UDP 53", 2)
d.msg(C, R, "질의 A example.com", y, WARN, "warn", sub="이름이 선에 그대로", tag="#1")
d.msg(R, C, "A 104.20.23.154 · A 172.66.147.243", y + STRIDE, MUTED, "ar", "5 3", sub="→ 클라이언트 55213번", tag="#2")

y = d.region("DoT · TCP 853", 5)
d.msg(C, R, "TCP 3-way · 43383 ↔ 853", y, INFO, None, tag="#3~5")
d.msg(C, R, "Client Hello · SNI 비어 있음", y + STRIDE, INFO, "info", sub="@1.1.1.1 · IP 로 붙음", tag="#6")
d.msg(R, C, "Server Hello · CCS · Application Data", y + 2 * STRIDE, MUTED, "ar", "5 3", tag="#8")
d.msg(C, R, "Application Data · opaque_type 23", y + 3 * STRIDE, ACC, None, sub="질의와 답이 이 안에 암호화", tag="#10~", lw=1.8)
d.note(C, "dns 필터 0줄", y + 4 * STRIDE, MUTED)

d.finish([("무엇을 물었나를 가림", ACC), ("선에 드러난 질의 이름", WARN), ("누구에게 물었나", INFO)], "05-04.c7-dot.svg")
