# 05-04 C5 — 2MB /big 응답 하나를 받은 c5-client.pcap 을 재조립 켬·끔으로 두 번 읽는다. 서버 데이터 조각은 #6 부터 #74 까지 45개.
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 메시지. 오른쪽 괄호 둘이 같은 요청에서 출발해 끝점만 다른 http.time.
#           focal(accent)은 재조립 켬(기본값)의 괄호 — 끝점이 마지막 조각까지 내려간다.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, WARN, INFO

C, S = "dhcp-client", "dhcp-server"
d = LabSeq(height(4, 1), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C5",
           "C5 — 재조립이 바꾸는 http.time 의 끝점",
           "같은 캡처를 두 번 읽는다. 재조립을 끄면 200 OK 가 첫 조각에 찍혀 첫 바이트까지를 재고, 켜면 마지막 조각에 찍혀 마지막 바이트까지를 잰다. 조각 45개는 어느 쪽에서도 남는다.",
           "왼쪽 #숫자는 c5-client.pcap 의 프레임 번호, 오른쪽 괄호가 두 설정의 http.time 입니다")
d.cast([(C, "10.55.0.137 · curl"), (S, "10.55.0.20 · server.py :80")], 300, capture=C)

y = d.region("GET /big · 받은 바이트 2,097,152", 4)
d.msg(C, S, "GET /big", y, MUTED, tag="#4")
d.msg(S, C, "첫 조각 · 끔에서 200 OK", y + STRIDE, WARN, "warn", "5 3", tag="#6")
d.msg(S, C, "사이 조각들 · 끔에서 Continuation", y + 2 * STRIDE, MUTED, "ar", "5 3")
d.msg(S, C, "마지막 조각 · 켬에서 200 OK", y + 3 * STRIDE, ACC, "acc", "5 3", sub="tcp.segment.count 45", tag="#74", lw=1.8)

bx = d.LX[S] + 24
d.bracket(bx, y, y + 3 * STRIDE, "0.04696초", ACC, sub="켬 · 마지막 바이트", ly=y + 2.5 * STRIDE)
d.bracket(bx + 16, y, y + STRIDE, "0.04419초", WARN, sub="끔 · 첫 바이트")

d.finish([("재조립 켬의 끝점", ACC), ("재조립 끔의 끝점", WARN)], "05-04.c5-reassembly.svg")
