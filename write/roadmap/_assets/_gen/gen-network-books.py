# write/roadmap/network-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 열셋을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책은 셋뿐이고 나머지는 부분 독서라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체. 모든 책을 같은 무게로 늘어놓으면
#   열셋 중 무엇부터 펴야 하는지가 사라진다. 정독 노트 유무는 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보이고, 노트 링크는 본문 표가 맡는다.
# 대체는 같은 자리를 다른 책이 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계, 국면, [(책, 읽을 장, [다루는 것 2줄], 우선순위)])
rows = [
    ("1", "연결", [
        ("Computer Networking", "1~5장", ["응용·전송·네트워크 계층", "라우팅과 SDN"], "필수"),
        ("TCP/IP Illustrated", "2~8 · 10~18장", ["주소·ARP·IP·NAT·ICMP", "TCP 연결·재전송·혼잡"], "필수"),
    ]),
    ("1", "웹 프로토콜", [
        ("HTTP/2 in Action", "4·8·9장", ["프레임·HPACK", "TCP·QUIC·HTTP/3"], "추천"),
        ("High Performance Browser Networking", "2·4·11·12장", ["TCP 구성 요소·TLS", "HTTP/1.x 와 HTTP/2"], "대체"),
    ]),
    ("2–6", "계층 종주", [
        ("Networking and Kubernetes", "전독 · 6장이 클라우드 축", ["OSI 부터 EKS 까지 한 축", "실습 다섯 편 포함"], "필수"),
    ]),
    ("3", "관측", [
        ("Packet Analysis with Wireshark", "1~5장", ["캡처·필터·TCP·TLS", "DHCP 와 이름 질의"], "필수"),
        ("Learning CoreDNS", "3·6·7장", ["Corefile 과 플러그인 체인", "Kubernetes 레코드"], "추천"),
    ]),
    ("4–5", "underlay·클라우드", [
        ("Cloud Native Data Center Networking", "2·6·7·14장", ["Clos 토폴로지·네트워크 가상화", "컨테이너 네트워킹·BGP"], "추천"),
    ]),
    ("6", "데이터패스", [
        ("Cilium Up and Running", "4~7 · 12~15장", ["IPAM·데이터패스·Service", "정책·투명 암호화·Hubble"], "추천"),
        ("Learning eBPF", "3·5~8장", ["프로그램 구조·CO-RE·BTF", "verifier·네트워킹"], "추천"),
    ]),
    ("7", "운영 경계", [
        ("Istio in Action", "1·3·4·5·9·12장", ["Envoy·Gateway·mTLS", "기본값 닫기·Zero Trust"], "추천"),
        ("Zero Trust Networks", "1·2·6·8·10장", ["신뢰 관리와 identity", "트래픽 신뢰·공격자 관점"], "추천"),
    ]),
    ("8", "신뢰와 익명", [
        ("Real-World Cryptography", "5·7~10장", ["키 교환·서명·난수", "안전한 전송과 종단 암호화"], "추천"),
        ("Patterns of Distributed Systems", "7·8장", ["HeartBeat 와 membership", "Majority Quorum"], "선택"),
    ]),
    ("7", "메시 후속", [
        ("Sidecar-less Istio Explained", "전 4장", ["ambient 모드 구조", "ztunnel 과 waypoint"], "대체"),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · NETWORK BOOK FLOW",
    "네트워크 책 읽기 흐름",
    "이 로드맵이 쓰는 책 열다섯을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 셋이고 "
    "나머지는 부분 독서다. 테두리 색이 우선순위이고, 대체는 같은 자리를 다른 책이 대신 채우는 경우다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, scope, topics, mark) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, MARK[mark], 1.2)
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.o.append(f'<circle cx="{x + 322}" cy="{y + 12}" r="4.5" fill="{MARK[mark]}"/>')
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC)])
d.save("network-books.svg")
