# write/network-roadmap.md §도입 — Kubernetes 네트워크 학습 로드맵.
# 네트워크는 02_os·08_cloud·99_ETC 에 걸쳐 있어 문서를 write/ 직계에 둔다. eyebrow 도 WRITE 다.
# 판형은 roadmap.sh 를 따른다 — 세로 척추에 국면을 걸고, 책을 노드로, 배우는 개념을 좌우로 뻗는다.
#
# 이 도식의 논점은 "무엇을 어떤 순서로 읽고 거기서 뭘 배우나" 하나다. 그래서 두 가지를 뺐다.
#   - 실습(LAB): 21개 중 책만으로 되는 것이 0개다. 외부 저장소·클러스터가 필요한 다른 축이라
#     같은 열에 같은 크기로 그리면 책 개념과 대등해 보여 논점이 흐려진다. 본문 실습 절이 맡는다.
#   - 단계 일련번호: 실제로 강제되는 선행은 둘뿐인데(eBPF→Cilium, Istio→앰비언트)
#     0→1→…→15 로 그리면 없는 순서를 있는 것처럼 만든다. 국면 사이만 순서고 국면 안은 병렬이다.
#
# 참조서는 척추에 걸지 않는다 — 읽는 순서에 들지 않기 때문이다. 대신 우상단에 흐름 밖 상자로 둔다.
#   안 그리면 Kurose 9판(©2026)처럼 가장 최신인 책이 그림에서 존재하지 않게 된다.
# 배지 넷으로 무게를 가른다 — 필수·추천·선택·대체. 참고 이미지의 체크·하트·회색 원에 대응한다.
# 강제 선행이 있는 책 사이에만 화살표를 긋는다. 선이 없으면 순서가 없다는 뜻이다.
# 타입 스펙: type-tree — 부모(국면)에서 자식(책)으로 갈라지는 계층. coral 은 데이터패스 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
PH_W, PH_H = 300, 48          # 국면 노드
BK_W, BK_H = 300, 52          # 책 노드
CH_W, CH_H, CH_GAP = 232, 32, 8
BUS, ROW_GAP, PHASE_GAP = 186, 44, 40
NOTE_H = 76

BADGE = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": WARN}

# (책, 장, 배지, 왼쪽 개념, 오른쪽 개념, 앞 책에서 화살표를 받는가)
phases = [
    ("바닥", "순서 없음", INFO, [
        ("Learning Modern Linux", "7장 · 2022", "선택",
         ["네트워크 네임스페이스", "인터페이스와 라우팅"], ["ip · ss 진단 도구"], False),
        ("Computer Networking Top-Down 9판", "3·4·5장 · 2026", "추천",
         ["TCP 혼잡제어와 재전송", "QUIC 이 UDP 위에 선 이유"],
         ["match + action 포워딩", "데이터 플레인과 컨트롤 플레인", "라우팅 알고리즘과 SDN"], False),
        ("Packet Analysis with Wireshark", "1~5장", "추천",
         ["캡처와 필터 문법", "TCP 수립 · 종료 · 재전송"], ["TLS 핸드셰이크와 복호화", "DHCP · DNS · HTTP 해부"], False),
    ], "프로토콜 모델을 잡고 캡처로 확인하는 국면이다. 4장의 match + action 이 iptables 규칙과 eBPF 데이터패스가 하는 일의 추상이다."),

    ("클러스터 모델", "약한 순서", INFO, [
        ("Networking and Kubernetes", "3~5장 · 2021", "필수",
         ["컨테이너 네트워킹 모드", "Pod 네트워크 모델", "CNI 의 자리"], ["Service 다섯 유형", "EndpointSlice"], False),
        ("Kubernetes in Action 2nd", "11~13장 · 2023", "필수",
         ["Service 선언과 어피니티", "Ingress 와 TLS"], ["Gateway API 와 HTTPRoute", "트래픽 정책"], False),
        ("Learning CoreDNS", "1~8장 · 2019", "추천",
         ["Corefile 과 플러그인 체인", "존 데이터와 위임"], ["서비스 디스커버리", "질의 조작과 관측"], False),
    ], None),

    ("데이터패스", "강한 순서", ACC, [
        ("Learning eBPF", "1~3 · 6~9장 · 2023", "필수",
         ["프로그램 구조와 맵", "verifier 가 거는 제약"], ["XDP · TC · socket 훅", "커널에서 패킷 가로채기"], False),
        ("Cilium Up and Running", "전 16장", "필수",
         ["데이터패스", "IPAM 과 Pod IP", "kube-proxy 대체"],
         ["L3~L7 · FQDN 정책", "egress 와 전송 암호화", "Hubble 흐름 관측"], True),
    ], "훅이 어디에 붙는지 모르면 Cilium 데이터패스 장을 읽어도 설정 이름만 외우게 된다. 이 둘만은 순서가 강제된다."),

    ("언더레이", "순서 없음", INFO, [
        ("Cloud Native Data Center Networking", "2·5·6·14·16장 · 2019", "추천",
         ["Clos 토폴로지", "라우팅 프로토콜 선택"], ["네트워크 가상화 · VXLAN", "BGP 와 EVPN"], False),
    ], "클러스터가 얹히는 물리 패브릭이다. 7장 Container Networking 은 2019년이라 Cilium 국면이 덮으므로 뺀다."),

    ("정책과 메시", "메시만 순서", INFO, [
        ("Policy as Code · KBP", "4·5·7·8장 / 9·11장", "추천",
         ["OPA 와 Rego 판정", "어드미션 컨트롤"], ["Gatekeeper · Kyverno", "네트워크 보안 관례"], False),
        ("Istio in Action", "1~9장 · 2022", "필수",
         ["메시가 인프라로 민 것", "Envoy 와 데이터 플레인"], ["게이트웨이와 트래픽 라우팅", "mTLS 와 메시 관측"], False),
        ("Sidecar-less Istio Explained", "전 4장", "추천",
         ["앰비언트 모드의 전제", "ztunnel 이 맡는 L4"], ["waypoint 가 맡는 L7", "사이드카와의 차이"], True),
    ], None),

    ("운영과 신뢰", "순서 없음", INFO, [
        ("Production Kubernetes", "5·6·10장 · 2021", "추천",
         ["오버레이 대 네이티브 라우팅", "서비스 라우팅 선택"], ["워크로드 신원"], False),
        ("Container Security 2판", "10·11장 · 2025", "추천",
         ["계층별 네트워크 차단", "컨테이너 방화벽"], ["TLS 로 컴포넌트 잇기", "인증서와 CA 의 역할"], False),
        ("Zero Trust · CKS · RWC", "4~8 / 2·3·5 / 5·9장", "선택",
         ["신뢰 모델과 인가 결정", "트래픽 신뢰 기준"], ["클러스터 하드닝", "키 교환과 보안 전송"], False),
    ], None),
]

tail = [
    ("HTTP:2 in Action · RFC 9000·9114", "4·8장 / 공식", "선택",
     ["HTTP/2 프레이밍", "HPACK 헤더 압축"], ["QUIC 와 HTTP/3 는 RFC 로"], False),
    ("AWS · OpenStack · OpenShift", "5·9장 / 6장 / 3·4장", "선택",
     ["VPC 와 로드밸런서", "Neutron"], ["OpenShift 운영"], False),
    ("Network Programming with Go", "1~7장 / client-go 공식", "선택",
     ["소켓과 주소 해석", "TCP · UDP 직접 다루기"], ["sample-controller 로 배우기"], False),
]

def row_h(left, right):
    n = max(len(left), len(right))
    return max(BK_H, n * CH_H + (n - 1) * CH_GAP) + 24

y = 116 + 180 + 48 + PHASE_GAP
for _, _, _, books, note in phases:
    y += PH_H + ROW_GAP
    for b in books:
        y += row_h(b[3], b[4]) + ROW_GAP
    y += (NOTE_H if note else 0) + PHASE_GAP - ROW_GAP
y += 60
for b in tail:
    y += row_h(b[3], b[4]) + ROW_GAP
H, W = y + 80, 1000

d = D(W, H, "WRITE · NETWORK ROADMAP",
      "Kubernetes 네트워크 학습 로드맵",
      "무엇을 어떤 순서로 읽고 거기서 무엇을 배우는가. 척추에 국면 여섯을 걸고 책을 노드로, "
      "그 책에서 배우는 개념을 좌우로 뻗었다. 국면 사이에는 순서가 있고, 국면 안의 책은 "
      "화살표가 없으면 순서가 없다. 배지는 필수·추천·선택·대체 넷이다.",
      "국면 사이만 순서입니다. 책 사이 화살표가 없으면 순서가 없습니다")

# 우상단 참조서 상자 — 척추 밖. 읽는 순서에 들지 않지만 늘 곁에 두는 책들
RX, RY, RW, RH = 620, 96, 340, 180
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "참조서 — 막힐 때만 엽니다", 13, INK, KR, "start", 600)
for _i, (_bk, _wh) in enumerate([
        ("Computer Networking 2·6·8장", "DNS·HTTP · 링크·ARP · 보안"),
        ("CompTIA Network+ 6판", "서브네팅 · VLAN 을 빠르게"),
        ("How Linux Works 3판", "배포판 네트워크 설정"),
        ("HPBN · Programming Kubernetes", "지연 감각 · 컨트롤러 개념 지도")]):
    _cy = RY + 54 + _i * 32          # 32 = 제목 13 + 설명 12 + 여백 7. 21 이면 두 줄이 붙어 읽힌다
    d.t(RX + 16, _cy, _bk, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, _cy + 16, _wh, 12, SOFT, KR, "start")

# 좌상단 읽는 법 상자
LX, LY, LW, LH = 40, 96, 330, 180
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힌다"),
                                ("추천", "빼도 되지만 손해가 크다"),
                                ("선택", "목표가 생겼을 때만")]):
    cy = LY + 60 + i * 30
    c = BADGE[lab]
    d.o.append(f'<rect x="{LX + 16}" y="{cy - 9}" width="34" height="17" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(LX + 33, cy + 3, lab, 11, c, KR)
    d.t(LX + 60, cy + 3, txt, 13, MUTED, KR, "start")

ROOT_Y = 116 + 180
d.box(SX - 130, ROOT_Y, 260, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 116, RULE, 1.4)

def draw_book(title, chap, badge, left, right, linked, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (BK_W / 2), mid, bus, mid, RULE, 1.0)
        for i, label in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 34) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 34, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")
    # 강제 선행이면 앞 책에서 이 책으로 화살표를 긋는다
    if linked:
        d.arrow([(SX, y - ROW_GAP + 4), (SX, mid - BK_H / 2 - 4)], ACC, "acc", 1.6)
        d.o.append(f'<rect x="{SX + 8}" y="{y - ROW_GAP + 6}" width="44" height="18" rx="4" fill="{PAPER}"/>')
        d.t(SX + 30, y - ROW_GAP + 19, "선행", 11, ACC, KR)
    d.box(SX - BK_W / 2, mid - BK_H / 2, BK_W, BK_H, PAPER, RULE, 1.0)
    c = BADGE[badge]
    d.o.append(f'<rect x="{SX - BK_W/2 + 12}" y="{mid - BK_H/2 + 8}" width="34" height="17" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(SX - BK_W / 2 + 29, mid - BK_H / 2 + 20, badge, 11, c, KR)
    d.t(SX + 8, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 16, chap, 12, SOFT, MONO)
    return h

def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H

y = ROOT_Y + 48 + PHASE_GAP
for name, order, color, books, note in phases:
    if color is ACC:
        d.tone(SX - PH_W / 2, y, PH_W, PH_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - PH_W / 2, y, PH_W, PH_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, order, 12, SOFT, KR)
    y += PH_H + ROW_GAP
    for b in books:
        y += draw_book(*b, y) + ROW_GAP
    if note:
        y += draw_note(note, y)
    y += PHASE_GAP - ROW_GAP

d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
d.o.append(f'<rect x="{SX - 120}" y="{y + 8}" width="240" height="22" rx="4" fill="{PAPER}"/>')
d.t(SX, y + 25, "여기부터는 목표가 생겼을 때만", 13, WARN, KR)
y += 60
for b in tail:
    y += draw_book(*b, y) + ROW_GAP

d.legend(H - 72, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("강제 선행", ACC)])
d.save("network-roadmap.svg")
