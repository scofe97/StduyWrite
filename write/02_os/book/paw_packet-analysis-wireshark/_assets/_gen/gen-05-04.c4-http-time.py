# 05-04 C4 — /fast · /slow · /fast 를 curl 한 번으로 요청한 c4-client.pcap. 연결 하나(tcp.stream 0)에 요청 셋.
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 메시지. 오른쪽 괄호가 http.time 이 재는 구간(요청 프레임 → 응답 프레임).
#           focal(accent)은 서버가 2초를 쓴 /slow 의 괄호. 3-way 는 어느 괄호에도 들어가지 않는다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, INFO, OK

C, S = "dhcp-client", "dhcp-server"
d = LabSeq(height(8, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C4",
           "C4 — http.time 이 재는 구간",
           "연결 하나에 요청 셋이 실린다. http.time 은 요청 프레임에서 짝이 되는 응답 프레임까지이고, 앞의 3-way 는 어느 요청의 값에도 들어가지 않는다.",
           "왼쪽 #숫자는 c4-client.pcap 의 프레임 번호, 오른쪽 괄호가 http.time 입니다")
d.cast([(C, "10.55.0.137 · curl"), (S, "10.55.0.20 · server.py :80")], 300, capture=C)

y = d.region("연결 수립 · 한 번", 2)
d.msg(C, S, "SYN", y, INFO, "info", tag="#1")
d.msg(S, C, "SYN-ACK", y + STRIDE, INFO, "info", "5 3", sub="0.000059초 뒤 · 네트워크 왕복", tag="#2")

y = d.region("요청 셋 · 모두 tcp.stream 0", 6)
bx = d.LX[S] + 28
for i, (uri, rq, rs, t, c) in enumerate([("/fast", "#4", "#8", "0.0349초", OK),
                                          ("/slow", "#10", "#14", "2.0488초", ACC),
                                          ("/fast", "#16", "#20", "0.0434초", OK)]):
    y1 = y + 2 * i * STRIDE; y2 = y1 + STRIDE
    mk = "acc" if c == ACC else "ok"
    d.msg(C, S, f"GET {uri}", y1, MUTED, tag=rq)
    d.msg(S, C, "200 OK", y2, c, mk, "5 3", tag=rs, lw=1.8 if c == ACC else 1.5)
    d.bracket(bx, y1, y2, t, c, sub="http.time")

d.finish([("서버가 답을 만드는 데 쓴 시간", ACC), ("짧은 응답", OK), ("연결 수립", INFO)], "05-04.c4-http-time.svg")
