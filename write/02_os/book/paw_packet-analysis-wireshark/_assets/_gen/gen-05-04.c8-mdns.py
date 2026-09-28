# 05-04 C8 (책 밖) — 제3자 dhcp-client2 에서 5353 을 잡은 두 캡처. 위는 avahi 를 막 띄운 직후(c8-bystander), 아래는 클라이언트 기억을 비운 뒤(c8b-bystander).
# 타입 스펙: type-sequence — 네 주체 사이의 시간순 메시지. 멀티캐스트 그룹을 레인 하나로 두고, 제3자 레인을 지나는 자리에 점을 찍어 캡처에 찍혔음을 보인다.
#           focal(accent)은 이름의 주인이 그룹에 외친 응답 A 10.55.0.20.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _seq0504 import LabSeq, height, STRIDE
from dd import ACC, MUTED, INFO, OK

C, S, B, G = "dhcp-client", "dhcp-server", "dhcp-client2", "224.0.0.251"
d = LabSeq(height(6, 2), "PACKET ANALYSIS WITH WIRESHARK · 05-04 C8",
           "C8 — mDNS 는 답까지 그룹에 외친다",
           "질의·응답·알림이 모두 224.0.0.251:5353 그룹으로 간다. 이름의 주인이 직접 답하고 이름 서버는 끼지 않는다. 교환과 상관없는 제3자 캡처에도 셋이 모두 찍힌다.",
           "왼쪽 #숫자는 제3자 캡처의 프레임 번호, 점은 그 캡처에 찍힌 자리입니다")
d.cast([(C, "10.55.0.137 · avahi"), (S, "10.55.0.20 · avahi"), (B, "제3자"), (G, "mDNS 그룹 · 5353")], 176, capture=B)

def seen(y):
    x = d.LX[B]
    d.o.append(f'<circle cx="{x}" cy="{y}" r="4" fill="{INFO}"/>')

y = d.region("avahi 를 막 띄운 직후 · 첫 캡처", 3)
d.msg(C, G, "알림 client.local", y, MUTED, tag="#1"); seen(y)
d.msg(S, G, "알림 server.local", y + STRIDE, MUTED, sub="neighbor.local 도 같은 방식 · #3", tag="#5"); seen(y + STRIDE)
d.note(C, "알림을 캐시", y + 2 * STRIDE, OK)

y = d.region("클라이언트 기억을 비운 뒤 · 둘째 캡처", 3)
d.msg(C, G, "질의 A server.local", y, INFO, "info", sub="#3 은 같은 질의의 IPv6 판", tag="#4"); seen(y)
d.msg(S, G, "응답 A 10.55.0.20", y + STRIDE, ACC, "acc", sub="이름의 주인이 직접", tag="#5", lw=1.8); seen(y + STRIDE)
d.note(B, "셋 다 찍힘", y + 2 * STRIDE, INFO)

d.finish([("그룹에 외친 응답", ACC), ("제3자 캡처에 찍힘", INFO), ("캐시로 남는 알림", OK)], "05-04.c8-mdns.svg")
