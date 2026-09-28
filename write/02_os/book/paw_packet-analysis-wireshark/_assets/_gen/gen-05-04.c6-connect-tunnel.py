# 05-04 C6 — 평문 POST 와, tinyproxy(8888)를 거친 HTTPS 를 클라이언트 쪽에서 잡았다. 캡처가 닿는 구간은 클라이언트 ↔ 프록시뿐.
# 타입 스펙: type-sequence — 세 주체 사이의 시간순 메시지. 평문 POST 와 CONNECT 터널을 구획으로 나눈다.
#           focal(accent)은 터널 안을 통째로 평문으로 지나가는 ClientHello(SNI=web.lab.test).
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, WARN, INFO, OK

C, P, S = "dhcp-client", "dhcp-server2", "dhcp-server"
d = LabSeq(height(7, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C6",
           "C6 — 평문 POST 와 CONNECT 터널",
           "폼 값은 평문 HTTP 에 그대로 실린다. 프록시 경유 HTTPS 는 CONNECT 와 200 이 평문이고, 터널은 바이트만 옮기므로 그 안의 ClientHello 도 평문이다. 가리는 것은 그 뒤의 TLS 다.",
           "왼쪽 #숫자는 프레임 번호, 캡처는 클라이언트 쪽 한 곳입니다")
d.cast([(C, "10.55.0.137 · curl"), (P, "10.55.0.21 · tinyproxy :8888"), (S, "10.55.0.20 · :80 · :443")], 220, capture=C)

y = d.region("평문 POST · :80", 1)
d.msg(C, S, "POST /login", y, WARN, "warn", sub="user,password = paw,hunter2 그대로", tag="#4")

y = d.region("프록시 경유 HTTPS · :8888", 6)
d.msg(C, P, "CONNECT web.lab.test:443", y, INFO, "info", sub="평문 · 프록시에게 하는 말", tag="#4")
d.msg(P, C, "200 · 터널 열림", y + STRIDE, INFO, "info", "5 3", sub="평문", tag="#6")
d.msg(C, S, "Client Hello · SNI=web.lab.test", y + 2 * STRIDE, ACC, "acc", sub="평문 · 서버에게 하는 말 · 프록시는 넘기기만", tag="#8", lw=1.8)
d.msg(S, C, "Server Hello · CCS · Application Data ×4", y + 3 * STRIDE, MUTED, "ar", "5 3", sub="TLS 1.3 · 인증서부터 암호화", tag="#9")
d.msg(C, S, "Application Data · opaque_type 23", y + 4 * STRIDE, OK, None, tag="#10~23")
d.note(P, "프록시 ↔ 서버 구간은 미캡처", y + 5 * STRIDE, MUTED)

d.finish([("터널 안 평문 ClientHello", ACC), ("드러난 평문 값", WARN), ("프록시와 평문 대화", INFO), ("TLS 로 가림", OK)], "05-04.c6-connect-tunnel.svg")
