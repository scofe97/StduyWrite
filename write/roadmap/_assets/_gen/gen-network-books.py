# write/roadmap/network-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 책 열셋을 단계 순으로 걸고, 각 책에서 "읽을 장"만 적는다.
#   통독하는 책은 셋뿐이고 나머지는 부분 독서라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 색이 뜻하는 것은 진입 시점이 아니라 자료의 상태다 —
#   ACC 는 정독 노트가 write/ 에 있는 책, INFO 는 소장본만 있고 노트가 없는 책이다.
#   학습 순서 도식의 점선 노드와 같은 사실을 책 단위로 표시한다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, PAPER, PAPER2, RULE, SOFT, D

# (단계, 국면, [(책, 읽을 범위, [다루는 것 2줄], 노트 있음)])
rows = [
    ("1", "연결", [
        ("Computer Networking", "1~5장 · 정독 노트 36편", ["응용·전송·네트워크 계층", "라우팅과 SDN"], True),
        ("TCP/IP Illustrated", "2~8 · 10~18장", ["주소·ARP·IP·NAT·ICMP", "TCP 연결·재전송·혼잡"], False),
    ]),
    ("1", "연결 보조", [
        ("High Performance Browser Networking", "2·4·11·12장", ["TCP 구성 요소·TLS", "HTTP/1.x 와 HTTP/2"], False),
        ("HTTP/2 in Action", "4·8·9장", ["프레임·HPACK", "TCP·QUIC·HTTP/3"], False),
    ]),
    ("2–5", "계층 종주", [
        ("Networking and Kubernetes", "전독 · 정독 노트 25편", ["OSI 부터 EKS 까지 한 축", "실습 다섯 편 포함"], True),
    ]),
    ("3", "관측", [
        ("Packet Analysis with Wireshark", "1~5장 · 정독 노트 13편", ["캡처·필터·TCP·TLS", "DHCP 와 이름 질의"], True),
        ("Learning CoreDNS", "3·6·7장 · 정독 노트 17편", ["Corefile 과 플러그인 체인", "Kubernetes 레코드"], True),
    ]),
    ("4", "Kubernetes", [
        ("Cloud Native Data Center Networking", "2·6·7·14장", ["Clos 토폴로지·네트워크 가상화", "컨테이너 네트워킹·BGP"], False),
    ]),
    ("5", "데이터패스", [
        ("Cilium Up and Running", "4~7 · 12~15장", ["IPAM·데이터패스·Service", "정책·투명 암호화·Hubble"], False),
        ("Learning eBPF", "3·5~8장", ["프로그램 구조·CO-RE·BTF", "verifier·네트워킹"], False),
    ]),
    ("6", "운영 경계", [
        ("Istio in Action", "1·3·4·5·9·12장 · 노트 18편", ["Envoy·Gateway·mTLS", "기본값 닫기·Zero Trust"], True),
        ("Zero Trust Networks", "1·2·8장", ["신뢰 관리 모델", "트래픽을 신뢰한다는 것"], False),
    ]),
    ("6", "메시 후속", [
        ("Sidecar-less Istio Explained", "전 4장", ["ambient 모드 구조", "ztunnel 과 waypoint"], False),
    ]),
]

W, TOP, ROW_H = 1000, 168, 132
H = TOP + len(rows) * ROW_H + 72
d = D(
    W,
    H,
    "WRITE · NETWORK BOOK FLOW",
    "네트워크 책 읽기 흐름",
    "이 로드맵이 쓰는 책 열셋을 단계 순으로 걸고 각 책에서 읽을 장만 적었다. 통독하는 책은 셋이고 "
    "나머지는 부분 독서다. 주황은 정독 노트가 write/ 에 있는 책, 파랑은 소장본만 있고 노트가 없는 책이다.",
    "위에서 아래로 진행하고, 같은 행의 책은 병행합니다",
)
d.line(126, TOP + 38, 126, TOP + (len(rows) - 1) * ROW_H + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = TOP + i * ROW_H
    d.box(30, y, 192, 76, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + 51, phase, 15, INK, KR, "middle", 600)
    for j, (title, scope, topics, has_note) in enumerate(cards):
        x = 258 + j * 362
        d.line(222 if j == 0 else x - 28, y + 38, x, y + 38, RULE, 1.0)
        d.box(x, y - 8, 334, 96, PAPER, ACC if has_note else INFO, 1.2)
        d.t(x + 16, y + 16, title, 13, INK, KR, "start", 600)
        d.t(x + 16, y + 38, scope, 11, SOFT, MONO, "start")
        d.t(x + 16, y + 60, topics[0], 12, MUTED, KR, "start")
        d.t(x + 16, y + 79, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("정독 노트 있음", ACC), ("소장본만", INFO)])
d.save("network-books.svg")
