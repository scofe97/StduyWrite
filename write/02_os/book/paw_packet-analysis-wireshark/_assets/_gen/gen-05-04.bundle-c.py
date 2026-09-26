# 05-04 묶음 C — 이름과 요청(05-02). C4 는 "느린 요청은 SYN·ACK 간격"(잘못 알던 인과)을 겨눈다. C7·C8 은 학습자 요청으로 넣은 책 밖 확장.
# 타입 스펙: type-flowchart — 단계를 실행 순서대로 잇는 절차 흐름. focal 은 잘못 알던 인과를 겨누는 단계.
import sys; sys.path.insert(0, "."); sys.path.insert(0, "_gen")
from _bundle_flow import bundle
from dd import ACC, WARN, INFO
bundle("05-04.bundle-c.svg", "PACKET ANALYSIS WITH WIRESHARK · 05-04 BUNDLE C",
       "묶음 C — 이름과 요청",
       "이름 실패와 연결 실패를 캡처에서 가르고, 질의 타입과 CNAME 체인을 읽고, 큰 응답이 TCP 로 넘어가는 순간을 EDNS(0) 로 없애고, 연결 하나에 실린 요청들의 http.time 을 재고, 재조립을 껐다 켜고, 평문 POST 와 CONNECT 터널 안의 ClientHello 를 본 뒤, DoT 와 mDNS 로 넓힌다.",
       "dns.conf 의 lab.test 존과 www/server.py 하나로 여덟 단계를 돕니다",
       [("C1", "이름 실패 · 연결 실패", "nope.lab.test · 닫힌 81", "NXDOMAIN 뒤 SYN 없음 / RST", "SYN 이 보이나", False, False),
        ("C2", "질의 타입 · CNAME", "dig A·AAAA·CNAME·MX·TXT", "www → web 두 줄", "네 갈래 · 답 두 줄", False, False),
        ("C3", "TCP 전환 · EDNS(0)", "big.lab.test TXT 891바이트", "+noedns 는 TC 뒤 TCP", "TCP 로 가는 조건", False, False),
        ("C4", "http.time", "/fast /slow /fast 한 연결", "SYN 한 번 · 응답마다 시간", "SYN·ACK 간격으로 잰다", True, False),
        ("C5", "재조립 켬 · 끔", "/big 2MB", "개수가 찍히는 자리만 바뀜", "켜면 조각이 사라지나", False, False),
        ("C6", "평문 · CONNECT 터널", "POST 비밀번호 · 프록시 8888", "CONNECT 뒤 SNI 평문", "터널이 암호화하나", False, False),
        ("C7", "DoT", "dig +tls @1.1.1.1", "dns 필터 0줄 · 853 TLS", "전송과 암호화는 다른 축", False, True),
        ("C8", "mDNS", "avahi-resolve · .local", "224.0.0.251 · 제3자에도", "주소 찾기와 같은 방식", False, True)],
       [("잘못 알던 인과를 겨눔", ACC), ("몰랐던 사실을 겨눔", WARN), ("책 밖 확장", INFO)], per_row=4)
