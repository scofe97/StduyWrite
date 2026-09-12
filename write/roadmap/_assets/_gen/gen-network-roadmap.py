# write/roadmap/network-roadmap.md §학습 순서 — 네트워크 학습 로드맵.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 연결", "응용과 전송 — 연결이 무엇인가",
     [("socket · bind · listen · accept", "TCP/IP Illustrated 12·13장", "필수"),
      ("4-tuple · 듣는 소켓과 연결 소켓", "TCP/IP Illustrated 12장", "필수"),
      ("TCP 상태 · 3-way handshake", "TCP/IP Illustrated 13장", "필수"),
      ("재전송 · 타임아웃 · RTT", "TCP/IP Illustrated 14장", "필수"),
      ("흐름 제어 · cwnd · in-flight", "TCP/IP Illustrated 15장", "필수"),
      ("혼잡 제어 · CUBIC · BBR", "TCP/IP Illustrated 16장", "필수"),
      ("UDP · 단편화", "TCP/IP Illustrated 10장", "추천"),
      ("TCP keepalive", "TCP/IP Illustrated 17장", "선택")],
     [("DNS 질의 · 이름 해석", "TCP/IP Illustrated 11장", "필수"),
      ("HTTP/1.1 · HTTP/2", "HTTP/2 in Action 4·8장", "필수"),
      ("QUIC · HTTP/3", "HTTP/2 in Action 9장", "추천"),
      ("HTTP 성능 축", "HPBN 11·12장", "대체"),
      ("TLS 핸드셰이크 · SNI · ECH", "HPBN 4장", "필수"),
      ("reverse proxy · half-close · 배압", "", "추천"),
      ("listen 큐 · accept 큐 · 포트 고갈", "", "추천"),
      ("OS CA bundle · truststore", "", "선택")]),

    ("2 · Linux 경로", "커널 안에서 패킷이 지나는 길",
     [("interface · MAC · ARP · NDP", "TCP/IP Illustrated 3·4장", "필수"),
      ("IP 주소 · 서브네팅 · CIDR", "TCP/IP Illustrated 2·5장", "필수"),
      ("라우팅 테이블 · next hop · 포워딩", "TCP/IP Illustrated 5장", "필수"),
      ("netns · veth · bridge", "Networking and K8s 2장", "필수"),
      ("netfilter · iptables · nftables", "TCP/IP Illustrated 7장", "필수"),
      ("NAT · SNAT · DNAT · MASQUERADE", "TCP/IP Illustrated 7장", "필수"),
      ("conntrack · 상태 테이블 포화", "Networking and K8s 2장", "필수")],
     [("MTU · MSS · PMTUD", "TCP/IP Illustrated 10장", "필수"),
      ("ICMP · traceroute", "TCP/IP Illustrated 8장", "추천"),
      ("컨테이너 네트워킹 모드 · 포트 매핑", "Networking and K8s 3장", "추천"),
      ("DHCP · 자동 구성", "TCP/IP Illustrated 6장", "선택"),
      ("NAT traversal", "", "선택"),
      ("bonding · LACP", "", "선택"),
      ("policy routing · ip rule · VRF", "", "선택")]),

    ("3 · 관측", "정말 그 길로 갔는지 눈으로 본다",
     [("캡처 위치 · 디스플레이 필터", "Packet Analysis 2장", "필수"),
      ("TCP 이상 판독 · RST · 재전송", "Packet Analysis 3장", "필수"),
      ("TLS 핸드셰이크 판독", "Packet Analysis 4장", "필수"),
      ("계층 순서 진단 — ss · ip · ethtool", "Networking and K8s 2장", "필수"),
      ("resolv.conf · ndots · NXDOMAIN", "", "필수")],
     [("Corefile · 플러그인 체인", "Learning CoreDNS 3장", "추천"),
      ("질문과 답의 불일치", "Learning CoreDNS 7장", "추천"),
      ("연결 지연 분포 · P99 · 측정 오차", "", "선택"),
      ("GRO · GSO · TSO 오프로딩", "", "선택"),
      ("tc qdisc · netem", "", "선택")]),

    ("4 · Kubernetes", "같은 커널 경로 위에 얹힌 이름과 정책",
     [("Pod IP · Pod CIDR · Node CIDR", "Networking and K8s 4장", "필수"),
      ("CNI", "Cilium 4장", "필수"),
      ("CNI 구현체 비교 — 무엇이 다른가", "Cilium 1~3장", "추천"),
      ("CNI 계약 — ADD · DEL · CHECK", "Networking and K8s 4장", "추천"),
      ("오버레이 · VXLAN", "Cilium 5장", "필수"),
      ("underlay 와 overlay 의 갈림", "Cloud Native DC Net 6장", "추천"),
      ("Service · EndpointSlice", "Networking and K8s 5장", "필수"),
      ("kube-proxy — iptables · IPVS", "Networking and K8s 2장", "필수"),
      ("readiness · stale Endpoint", "", "필수")],
     [("클러스터 DNS · Service FQDN", "Learning CoreDNS 6장", "필수"),
      ("service discovery · east-west", "", "추천"),
      ("Ingress", "Networking and K8s 5장", "필수"),
      ("Gateway API · HTTPRoute", "Cilium 7장", "추천"),
      ("L4 로드밸런싱 · health check", "", "추천"),
      ("인증서 만료와 TLS 실패 구분", "", "추천"),
      ("externalTrafficPolicy · 소스 IP", "", "추천")]),

    ("5 · 클라우드 네트워크", "클러스터가 서 있는 underlay",
     [("VPC · 서브넷 · 라우트 테이블", "Networking and K8s 6장", "필수"),
      ("Security Group · NACL", "Networking and K8s 6장", "필수"),
      ("클라우드 로드밸런서 — L4 · L7", "Networking and K8s 6장", "필수"),
      ("3사 기본값의 갈림", "Networking and K8s 6장", "추천")],
     [("VPN · 사이트 간 연결", "", "추천"),
      ("AWS Direct Connect · 전용선", "", "추천"),
      ("Clos 토폴로지 · BGP · ECMP", "Cloud Native DC Net 2·14장", "선택")]),

    ("6 · 데이터패스와 정책", "같은 일을 다른 데이터패스로",
     [("NetworkPolicy · default deny", "Cilium 12장", "필수"),
      ("L7 · FQDN 정책", "Cilium 13장", "추천"),
      ("identity-aware policy", "Cilium 12장", "추천"),
      ("eBPF 프로그램 유형 · hook", "Learning eBPF 3·7장", "추천"),
      ("XDP · TC hook", "Learning eBPF 7·8장", "추천"),
      ("eBPF map · helper", "Learning eBPF 3장", "추천"),
      ("verifier · CO-RE · BTF", "Learning eBPF 5·6장", "추천")],
     [("eBPF 네트워킹", "Learning eBPF 8장", "추천"),
      ("Cilium 데이터패스 · IPAM", "Cilium 4·5장", "추천"),
      ("Hubble 관측", "Cilium 15장", "선택"),
      ("L4 와 L7 텔레메트리의 갈림", "", "추천"),
      ("Beyla · Caretta — 자동 계측", "", "선택"),
      ("투명 암호화 · WireGuard", "Cilium 14장", "선택"),
      ("egress 게이트웨이 · 클러스터 access", "Cilium 10·11장", "선택"),
      ("eBPF host routing", "", "선택")]),

    ("7 · 운영 경계", "클러스터가 한 종류가 아닐 때",
     [("dual-stack · ipFamilyPolicy", "", "추천"),
      ("topology-aware routing", "", "추천"),
      ("서비스 메시가 옮긴 것", "Istio in Action 1장", "추천"),
      ("Windows HNS · HCS", "", "선택"),
      ("멀티클러스터 메시", "Cilium 9장", "선택")],
     [("Envoy · Gateway · VirtualService", "Istio in Action 3·4장", "추천"),
      ("mTLS · 기본값 닫아 가기", "Istio in Action 5·9장", "추천"),
      ("Zero Trust 전제", "Zero Trust Networks 1·2장", "선택"),
      ("ambient · ztunnel · waypoint", "Sidecar-less Istio 1~3장", "대체")]),

    ("8 · 오버레이와 신뢰", "분산 네트워크가 되풀이하는 문제들",
     [("bootstrap · trust anchor", "", "추천"),
      ("peer discovery · DHT · gossip", "Patterns of Distributed Sys 7장", "추천"),
      ("signed descriptor · 공개키 신원", "Real-World Crypto 7장", "추천"),
      ("key rotation · replay 방지", "Real-World Crypto 5·8장", "추천"),
      ("Sybil · eclipse · poisoning", "Zero Trust Networks 10장", "추천")],
     [("identity 와 trust 의 차이", "Zero Trust Networks 2·6장", "필수"),
      ("traffic correlation", "Zero Trust Networks 8장", "필수"),
      ("암호화가 숨기지 않는 것", "Real-World Crypto 9·10장", "필수"),
      ("오버레이 · 터널링 · relay", "", "추천")]),

    ("9 · 터널과 경로", "고른 노드로 실제 길을 내는 일",
     [("피어 발견과 터널 구성은 다르다", "", "필수"),
      ("멀티홉 — 홉 수의 대가", "", "필수"),
      ("path selection · 경로 다양성", "", "필수"),
      ("inbound 와 outbound 의 분리", "", "추천"),
      ("클라이언트가 경로를 정한다", "", "추천")],
     [("종단 성공 확률 — 곱으로 쌓인다", "", "필수"),
      ("기하분포와 평균 시도 횟수", "", "추천"),
      ("재시도 · 타임아웃 · 감지 시간", "Patterns of Distributed Sys 7장", "필수"),
      ("터널 풀 — 미리 열어 두기", "", "추천"),
      ("예비 터널 — 준비 비용과 전환 시간", "", "추천")]),
]

CUT_AFTER = 2          # 3단계 뒤에 노드 한 대 ↔ 클러스터 절단선
NOTES = {
    2: "Kubernetes 네트워크 장애의 상당수가 4단계가 아니라 2단계에서 풀린다. conntrack 과 MTU 가 먼저다.",
    4: "클라우드 축은 소장본이 Networking and Kubernetes 6장 하나뿐이다. 나머지는 공식 문서로 메운다.",
    6: "책 줄이 빈 노드는 아직 자료가 없는 자리다. 소장 목록이 늘면 그 줄만 채운다.",
    7: "8·9단계는 기술 이름이 아니라 문제를 배우는 자리다. Tor·I2P·libp2p 는 그 문제의 답 중 하나다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · NETWORK ROADMAP",
      "네트워크 학습 로드맵",
      "애플리케이션이 여는 socket 에서 커널 패킷 경로로 내려간 뒤 Kubernetes 데이터패스로 다시 "
      "올라간다. 척추에 단계 아홉을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 "
      "그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("k8s-roadmap", "오브젝트 배포와 클러스터 운영"),
        ("os-roadmap", "socket 과 파일 디스크립터의 커널 쪽"),
        ("Computer Networking 6~8장", "무선 · 물리 계층 · 암호 일반"),
        ("06_observability", "앱이 내보내는 지표와 트레이스")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~3단계는 노드 한 대 · 4단계부터 클러스터", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("노드 한 대와 클러스터의 경계", WARN)])
d.save("network-roadmap.svg")
