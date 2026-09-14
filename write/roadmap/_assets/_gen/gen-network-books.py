# write/roadmap/network-roadmap.md §책 읽기 흐름.
# 이 로드맵이 쓰는 자료 스물둘을 단계 순으로 걸고, 각 자료에서 "읽을 장"만 적는다.
# 마지막 한 줄만 책이 아니다 — network-fundamentals-lab 은 containerlab 토폴로지가 원자료이고,
#   읽는 자리가 아니라 고장을 배포해 증상으로 되짚는 자리다. 같은 표에 두는 이유는
#   "어느 단계를 무엇으로 배우는가"라는 이 도식의 질문에 그것도 답하기 때문이다.
#   통독하는 책은 셋뿐이고 나머지는 부분 독서라, 범위를 안 적으면 로드맵이 통독을 요구하는 것처럼 읽힌다.
# 색이 뜻하는 것은 우선순위다 — 필수·추천·선택·대체. 모든 책을 같은 무게로 늘어놓으면
#   스물둘 중 무엇부터 펴야 하는지가 사라진다. 정독 노트 유무는 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보이고, 노트 링크는 본문 표가 맡는다.
# 대체는 같은 자리를 다른 책이 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (이 주제를 읽는 자리, 주제, [(책, 그 책 전체의 자리 — 본문 표 `자리` 열, 읽을 장, [다루는 것 2줄], 우선순위)])
#   행 번호와 카드 칩은 다른 것을 말한다 — 행은 "이 묶음을 언제 읽는가",
#   칩은 "그 책이 로드맵 전체에서 걸치는 범위"다. 한 책이 여러 주제에 걸칠 때 둘이 갈린다.
#   한 주제에 몇 권이 붙든 상관없다 — 카드가 2열씩 아래로 접히고 주제 박스가 그만큼 늘어난다.
#   앞 판은 한 행에 2권이 상한이라, 같은 1단계인 "연결"과 "웹 프로토콜"을 억지로 갈라 놓았다.
#   단계는 행이 아니라 카드가 갖는다. 한 행에 선 두 책의 단계가 서로 다른데
#   행 하나에 번호를 달면 "4–7" 처럼 둘의 합집합이 되어 어느 책도 가리키지 못한다.
rows = [
    ("1–4", "랩 — 고장에서 되짚기", [
        ("network-fundamentals-lab", "1~4단계", "코어 10편 (전 18편)", ["ARP·라우팅·NAT·conntrack", "MTU·DNS 를 깨뜨려 진단"], "필수"),
    ]),
    ("1·2", "연결과 웹 프로토콜", [
        ("Computer Networking", "1·2·5단계", "1~6 · 8장", ["응용·전송·네트워크·링크 계층", "라우팅과 보안 프로토콜"], "필수"),
        ("TCP/IP Illustrated", "1·2단계", "2~8 · 10~17장", ["주소·ARP·IP·NAT·ICMP", "TCP 연결·재전송·혼잡"], "필수"),
        ("HTTP/2 in Action", "1단계", "4·8·9장", ["프레임·HPACK", "TCP·QUIC·HTTP/3"], "추천"),
        ("High Performance Browser Networking", "1단계", "2·4·11·12·17장", ["TCP 구성 요소·TLS", "HTTP/2 와 WebSocket"], "대체"),
        ("Container Security", "1단계", "11장", ["키·인증서·CA 의 역할", "컴포넌트 사이 TLS"], "선택"),
    ]),
    ("2–6", "계층 종주", [
        ("Networking and Kubernetes", "2~6단계", "전독 · 6장이 클라우드 축", ["OSI 부터 EKS 까지 한 축", "실습 다섯 편 포함"], "필수"),
    ]),
    ("3·4", "관측", [
        ("Packet Analysis with Wireshark", "3단계", "1~5장", ["캡처·필터·TCP·TLS", "DHCP 와 이름 질의"], "필수"),
        ("Systems Performance", "1·3단계", "10장", ["큐·버퍼·오프로드", "nstat·tcpretrans·tc"], "추천"),
        ("Learning CoreDNS", "1·3·4단계", "2·3·6·7장", ["위임·레코드와 Corefile", "Kubernetes 레코드"], "추천"),
    ]),
    ("1·4", "Service 와 진입", [
        ("Kubernetes in Action", "1·4단계", "11~13 · 16·17장", ["Service·트래픽 정책·readiness", "Ingress·Gateway API"], "추천"),
        ("Production Kubernetes", "4단계", "5장", ["Pod 네트워킹", "CNI 구현체와 IPAM"], "선택"),
    ]),
    ("4·5", "underlay·클라우드", [
        ("Cloud Native Data Center Networking", "4·5단계", "2·6·7·14장", ["Clos 토폴로지·네트워크 가상화", "컨테이너 네트워킹·BGP"], "추천"),
        ("System Design on AWS", "5단계", "9장", ["VPN·Direct Connect·TGW", "PrivateLink·Route 53"], "추천"),
    ]),
    ("4–7", "데이터패스", [
        ("Cilium Up and Running", "4~7단계", "1~16장", ["왜 Cilium 인가·CNI 비교·IPAM", "정책·BGP·Egress·암호화·Hubble"], "필수"),
        ("Learning eBPF", "6단계", "3·5~8장", ["프로그램 구조·CO-RE·BTF", "verifier·네트워킹"], "추천"),
    ]),
    ("7·8", "운영 경계", [
        ("Istio in Action", "7단계", "1·3~6·9·10·12장·부록 C", ["Envoy·Gateway·복원력·mTLS", "기본값 닫기·SPIFFE"], "추천"),
        ("Zero Trust Networks", "7·8단계", "1·2·4·6·8장", ["신뢰 관리와 identity", "인가 결정·트래픽 신뢰"], "추천"),
        ("Sidecar-less Istio Explained", "7단계", "1~3장", ["ambient 모드 구조", "ztunnel 과 waypoint"], "대체"),
    ]),
    ("8–9", "신뢰와 경로", [
        ("Real-World Cryptography", "8단계", "3·7~10장", ["MAC·서명·난수", "안전한 전송과 종단 암호화"], "추천"),
        ("Patterns of Distributed Systems", "8·9단계", "7·26·28장", ["HeartBeat 와 실패 감지 시간", "Lease 와 gossip 전파"], "추천"),
        ("Database Internals", "8·9단계", "9·12장", ["실패 감지와 heartbeat", "anti-entropy 와 gossip"], "추천"),
    ]),
]

W, TOP = 1000, 168
COLS, CARD_W, CARD_H = 2, 334, 96          # 카드 폭은 가장 긴 책 제목이 정한다
COL_GAP, LINE_GAP, ROW_GAP = 28, 22, 36    # 같은 주제가 여러 줄로 접힐 때의 간격

def chip_w(t, size=10, pad=7):
    """dd.chip 의 폭 공식. 칩을 카드 오른쪽에 맞춰 붙이려면 폭을 미리 알아야 한다."""
    kr = any('가' <= c <= '힣' for c in str(t))
    return len(str(t)) * (size * 1.0 if kr else size * 0.62) + pad * 2

def lines_of(cards):
    """한 주제의 카드를 2열씩 끊어 줄로 나눈다. 주제당 권수 상한은 없다."""
    return [cards[k:k + COLS] for k in range(0, len(cards), COLS)]

def row_h(cards):
    n = len(lines_of(cards))
    return n * CARD_H + (n - 1) * LINE_GAP + ROW_GAP

# 행마다 높이가 달라 y 를 누적으로 잡는다
row_y, _acc = [], TOP
for _r in rows:
    row_y.append(_acc)
    _acc += row_h(_r[-1])
H = _acc + 72
d = D(
    W,
    H,
    "WRITE · NETWORK BOOK FLOW",
    "네트워크 책 읽기 흐름",
    "이 로드맵이 쓰는 자료 스물둘을 단계 순으로 걸고 각 자료에서 읽을 장만 적었다. 통독하는 책은 셋이고 "
    "나머지는 부분 독서다. 맨 위 한 줄만 책이 아니라 손으로 밟는 랩이다. "
    "테두리 색이 우선순위이고, 대체는 같은 자리를 다른 자료가 대신 채우는 경우다.",
    "한 주제의 자료는 권수 제한 없이 병행합니다. 단계는 자료마다 달라 카드마다 칩으로 적었습니다",
)
d.line(126, row_y[0] + 38, 126, row_y[-1] + 38, RULE, 1.4)
for i, (number, phase, cards) in enumerate(rows):
    y = row_y[i]
    groups = lines_of(cards)
    # 주제 박스는 그 주제의 카드 전체 높이에 맞춰 늘어난다
    box_h = len(groups) * CARD_H + (len(groups) - 1) * LINE_GAP - 20
    d.box(30, y, 192, box_h, PAPER2, RULE, 1.0)
    d.t(48, y + 25, number, 12, INFO, MONO, "start", 600)
    d.t(126, y + box_h / 2 + 12, phase, 15, INK, KR, "middle", 600)
    # 주제 박스에서 각 줄로 내려가는 세로 줄기
    if len(groups) > 1:
        d.line(240, y + 38, 240, y + (len(groups) - 1) * (CARD_H + LINE_GAP) + 38, RULE, 1.0)
    for g, line_cards in enumerate(groups):
        ly = y + g * (CARD_H + LINE_GAP)
        d.line(222, ly + 38, 258, ly + 38, RULE, 1.0)
        for j, (title, stage, scope, topics, mark) in enumerate(line_cards):
            x = 258 + j * (CARD_W + COL_GAP)
            if j:
                d.line(x - COL_GAP, ly + 38, x, ly + 38, RULE, 1.0)
            d.box(x, ly - 8, CARD_W, CARD_H, PAPER, MARK[mark], 1.2)
            d.t(x + 16, ly + 18, title, 13, INK, KR, "start", 600)
            d.o.append(f'<circle cx="{x + 316}" cy="{ly + 14}" r="4.5" fill="{MARK[mark]}"/>')
            # 단계는 카드마다 — 같은 주제라도 책마다 자리가 다르다.
            #   제목 줄이 아니라 "읽을 장" 줄 오른쪽에 둔다 — 긴 책 제목과 부딪히지 않는 자리다.
            # 단계 문자열이 길어도 카드를 넘지 않도록 오른쪽 정렬로 붙인다
            d.chip(x + CARD_W - 12 - chip_w(stage) / 2, ly + 40, stage, INFO, 10)
            d.t(x + 16, ly + 44, scope, 11, SOFT, MONO, "start")
            d.t(x + 16, ly + 62, topics[0], 12, MUTED, KR, "start")
            d.t(x + 16, ly + 80, topics[1], 12, MUTED, KR, "start")
d.legend(H - 48, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC)])
d.save("network-books.svg")
