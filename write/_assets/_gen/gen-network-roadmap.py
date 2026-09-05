# write/network-roadmap.md §도입 — Kubernetes 네트워크 학습 로드맵.
# 네트워크는 02_os·08_cloud·99_ETC 에 걸쳐 있어 문서를 write/ 직계에 둔다. eyebrow 도 WRITE 다.
# 판형은 roadmap.sh 를 따른다 — 세로 척추에 국면과 단계를 걸고, 각 단계의 개념을 좌우로 뻗는다.
# 박스는 세 종류다 — 실선(책이 다루는 개념), 점선(책 밖 키워드), 초록 테두리 + LAB 태그(실습편).
#   LAB 은 '손으로 확인하는 자리' 이고 출처는 셋이다 — network-fundamentals-lab 편 번호,
#   책의 예제 저장소, 공식 핸즈온 문서. 실습이 필요 없어서 비는 단계는 없고,
#   검증한 자료를 못 찾은 단계만 비운다(11·12·13·14). 지어낸 출처를 채우지 않는다.
# 좌상단 '읽는 법' 상자와 국면 사이 주석 띠는 roadmap.sh 판형을 따른 것 — 판단 근거를 그림 안에 남긴다.
# 낡음 기준을 적용해 13단계에서 HPBN(2013)을, 15단계에서 Programming Kubernetes(2019)를 뺐다.
#   그 자리는 RFC 9000·9113·9114 와 client-go 공식 문서가 맡는다. 근거는 본문 낡음 점검 절에 있다.
# 트리로 읽으면 root → 국면 5 → 단계 11 → 개념 이라 깊이 4·한 부모당 너비 3 으로 예산 안에 든다.
# 높이는 개념 개수에서 산출한다(고정값 금지). 연결선은 스펙대로 직교 엘보로만 긋는다.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계층. coral 은 데이터패스 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
NODE_W, NODE_H = 284, 48
CH_W, CH_H, CH_GAP = 236, 32, 8
BUS, ROW_GAP, PHASE_GAP = 178, 40, 36
NOTE_H = 76

# (제목, 장, 왼쪽 개념, 오른쪽 개념, 책 밖 키워드, 실습편)
phases = [
    ("바닥과 눈", "0~1단계", INFO, [
        ("0 · Learning Modern Linux", "7장",
         ["네트워크 네임스페이스", "인터페이스와 라우팅"], ["ip · ss 진단 도구"],
         ["ip netns 실습", "veth · 브리지 만들기"], ["00 온램프 · CIDR 와 도구 셋"]),
        ("1 · Packet Analysis with Wireshark", "1~5장",
         ["캡처와 필터 문법", "TCP 수립 · 종료"], ["재전송과 지연 분석", "TLS 복호화 · DNS · HTTP"],
         ["MTU · PMTUD 블랙홀", "conntrack 포화"],
         ["01·02 · L2 인접성과 ARP", "04~06 · 라우팅 · LPM · TTL", "08·09·12 · TCP·conntrack·MTU",
          "CP-1 · 증상만으로 좁히기"]),
    ], "실습 저장소는 고장을 미리 심어 두고 증상만 준다. 1단계의 책 밖 키워드 둘이 그대로 12편과 09편이다."),
    ("클러스터 모델", "2~4단계", INFO, [
        ("2 · Networking and Kubernetes", "3~5장 · 2021",
         ["컨테이너 네트워킹 모드", "Pod 네트워크 모델"], ["Service 다섯 유형", "EndpointSlice"],
         ["CNI 스펙과 체이닝", "Multus · SR-IOV"], ["03·07 · VLAN 과 VXLAN", "10·11 · NAT 와 대칭성"]),
        ("3 · Kubernetes in Action 2nd", "11~13장 · 2023",
         ["Service 선언과 어피니티", "Ingress 와 TLS"], ["Gateway API 와 HTTPRoute"],
         ["GAMMA 이니셔티브", "Ingress 에서 이행하기"], ["16 · NAT 헤어핀", "책 예제 · kia-2nd"]),
        ("4 · Learning CoreDNS", "1~8장 · 2019",
         ["Corefile 과 플러그인 체인", "존 데이터와 위임"], ["서비스 디스커버리", "질의 조작과 관측"],
         ["ndots:5 질의 폭증", "NodeLocal DNSCache"], ["14·15 · DNS TTL 과 ICMP", "공식 · CoreDNS 플러그인"]),
    ], None),
    ("데이터패스", "5~6단계", ACC, [
        ("5 · Learning eBPF", "1~3 / 6~9장 · 2023",
         ["프로그램 구조와 맵", "verifier 가 거는 제약"], ["XDP · TC · socket 훅", "커널에서 패킷 가로채기"],
         ["cgroup · sockmap 훅", "bpftool"], ["책 예제 · learning-ebpf"]),
        ("6 · Cilium Up and Running", "16장",
         ["데이터패스", "IPAM 과 Pod IP", "kube-proxy 대체"],
         ["L3~L7 · FQDN 정책", "egress 와 전송 암호화", "Hubble 흐름 관측"],
         ["kube-proxy nftables 모드", "ClusterMesh · netkit"], ["13 · 터널 오버레이 MTU", "공식 · Cilium 시작하기"]),
    ], "이 국면이 필수 분량의 절반 가까이를 차지한다. 앞의 두 국면을 건너뛰면 설정 이름만 외우게 된다."),
    ("정책과 메시", "7~9단계", INFO, [
        ("7 · Policy as Code · KBP", "4·5·7·8장 / 9·11장",
         ["OPA 와 Rego 판정", "어드미션 컨트롤"], ["Gatekeeper · Kyverno"],
         ["AdminNetworkPolicy", "CEL 어드미션 정책"], ["공식 · OPA Playground", "공식 · Kyverno 정책 모음"]),
        ("8 · Istio in Action", "1~9장 · 2022",
         ["메시가 인프라로 민 것", "Envoy 와 데이터 플레인"], ["게이트웨이와 트래픽 라우팅", "mTLS 와 메시 관측"],
         ["Envoy xDS 프로토콜", "SPIFFE · SPIRE"], ["책 예제 · istio-in-action"]),
        ("9 · Sidecar-less Istio Explained", "4장",
         ["앰비언트 모드의 전제", "ztunnel 이 맡는 L4"], ["waypoint 가 맡는 L7", "사이드카와의 차이"],
         ["waypoint 배치 단위"], ["공식 · Ambient 시작하기"]),
    ], None),
    ("운영과 신뢰", "10~12단계", INFO, [
        ("10 · Production Kubernetes", "5·6·10장 · 2021",
         ["오버레이 · 라우팅 · BGP", "서비스 라우팅 선택"], ["워크로드 신원"],
         ["Topology Aware Routing", "CNI 성능 벤치마크"], ["17 · 동적 라우팅 OSPF·BGP"]),
        ("11 · Container Security 2판", "10·11장 · 2025",
         ["계층별 네트워크 차단", "컨테이너 방화벽"], ["TLS 로 컴포넌트 잇기", "인증서와 CA 의 역할"],
         ["인증서 회전과 SDS", "cert-manager"], []),
        ("12 · Zero Trust · CKS · RWC", "4~8 / 2·3·5 / 5·9장",
         ["신뢰 모델과 인가 결정", "트래픽 신뢰 기준"], ["클러스터 하드닝", "키 교환과 보안 전송"],
         ["암호화를 겹쳐 쓸 때의 판단"], []),
    ], None),
]

tail = [
    ("13 · HTTP:2 in Action · RFC 9000·9114", "4·8장 / 공식",
     ["HTTP/2 프레이밍", "HPACK 헤더 압축"], ["QUIC 와 HTTP/3 는 RFC 로"],
     ["Envoy 의 QUIC 지원", "gRPC 로드밸런싱"], []),
    ("14 · AWS · OpenStack · OpenShift", "5·9장 / 6장 / 3·4장",
     ["VPC 와 로드밸런서", "Neutron"], ["OpenShift 운영"],
     ["ENI 한계와 prefix delegation", "OVN-Kubernetes"], []),
    ("15 · Go · client-go 공식 문서", "1~7장 / 공식",
     ["소켓과 주소 해석", "TCP · UDP 직접 다루기"], ["sample-controller 로 배우기"],
     ["CNI 의 ADD · DEL · CHECK", "netlink 로 veth"], ["공식 · sample-controller", "내 프로젝트 · podwire"]),
]

def row_h(left, right, extra, lab):
    n = max(len(left) + len(lab), len(right) + len(extra))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24

y = 116 + 96 + 48 + PHASE_GAP
for _, _, _, steps, note in phases:
    y += NODE_H + ROW_GAP
    for s in steps:
        y += row_h(s[2], s[3], s[4], s[5]) + ROW_GAP
    y += (NOTE_H if note else 0) + PHASE_GAP - ROW_GAP
y += 56
for s in tail:
    y += row_h(s[2], s[3], s[4], s[5]) + ROW_GAP
H, W = y + 76, 1000

d = D(W, H, "WRITE · NETWORK ROADMAP",
      "Kubernetes 네트워크 학습 로드맵",
      "위에서 아래로 읽는 순서. 척추에 국면 다섯과 단계 열여섯을 걸고 각 단계에서 배우는 개념을 좌우로 뻗었다. "
      "실선은 책이 다루는 개념, 점선은 공식 문서로 채울 키워드, 초록 테두리는 containerlab 실습편이다. "
      "절단선 아래 셋은 목표가 생겼을 때만 여는 조건부 단계다.",
      "실선은 책, 점선은 공식 문서, 초록은 실습편입니다")

# 좌상단 읽는 법 상자 — 판형의 범례 자리
LX, LY, LW, LH = 40, 96, 300, 96
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
# 스와치는 실제 셀과 같은 칠·선을 쓴다 — 범례와 본체가 다르면 범례가 거짓말이 된다
for i, (txt, kind) in enumerate([
        ("책이 다루는 개념", "book"),
        ("공식 문서로 채울 키워드", "extra"),
        ("손으로 확인하는 자리", "lab")]):
    cy = LY + 44 + i * 18
    if kind == "extra":
        d.o.append(f'<rect x="{LX + 16}" y="{cy - 8}" width="18" height="14" rx="3" fill="{PAPER}" '
                   f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="3 3"/>')
    elif kind == "lab":
        d.o.append(f'<rect x="{LX + 16}" y="{cy - 8}" width="18" height="14" rx="3" '
                   f'fill="{OK}12" stroke="{OK}" stroke-width="1.0"/>')
    else:
        d.o.append(f'<rect x="{LX + 16}" y="{cy - 8}" width="18" height="14" rx="3" '
                   f'fill="{PAPER2}" stroke="{RULE}" stroke-width="0.9"/>')
    d.t(LX + 44, cy + 3, txt, 13, MUTED, KR, "start")

ROOT_Y = 116 + 96
d.box(SX - 120, ROOT_Y, 240, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 116, RULE, 1.4)

def cell(bx, cy, label, kind):
    if kind == "extra":
        d.o.append(f'<rect x="{bx}" y="{cy - CH_H/2}" width="{CH_W}" height="{CH_H}" rx="6" '
                   f'fill="{PAPER}" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
        d.t(bx + CH_W / 2, cy + 5, label, 13, SOFT, KR, "middle")
    elif kind == "lab":
        d.o.append(f'<rect x="{bx}" y="{cy - CH_H/2}" width="{CH_W}" height="{CH_H}" rx="6" '
                   f'fill="{OK}12" stroke="{OK}" stroke-width="1.0"/>')
        d.o.append(f'<rect x="{bx + 8}" y="{cy - 9}" width="30" height="18" rx="3" fill="{OK}22" stroke="{OK}" stroke-width="0.8"/>')
        d.t(bx + 23, cy + 4, "LAB", 10, OK, MONO)
        d.t(bx + 46 + (CH_W - 54) / 2, cy + 5, label, 12, MUTED, KR, "middle")
    else:
        d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
        d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")

def draw_step(title, chap, left, right, extra, lab, y):
    h = row_h(left, right, extra, lab)
    mid = y + h / 2
    for side, items in (("left", [(v, "book") for v in left] + [(v, "lab") for v in lab]),
                        ("right", [(v, "book") for v in right] + [(v, "extra") for v in extra])):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (label, kind) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 36) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 36, cy, RULE, 1.0)
            cell(bx, cy, label, kind)
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    d.t(SX, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 14, chap, 12, SOFT, MONO)
    return h

def draw_note(text, y):
    d.o.append(f'<rect x="120" y="{y}" width="760" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(140, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(140, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H

y = ROOT_Y + 48 + PHASE_GAP
for name, stage, color, steps, note in phases:
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for s in steps:
        y += draw_step(*s, y) + ROW_GAP
    if note:
        y += draw_note(note, y)
    y += PHASE_GAP - ROW_GAP

xc_y = y + 20
d.line(40, xc_y, W - 40, xc_y, WARN, 1.4, "6 5")
d.o.append(f'<rect x="{SX - 108}" y="{xc_y - 12}" width="216" height="22" rx="4" fill="{PAPER}"/>')
d.t(SX, xc_y + 5, "여기부터는 목표가 생겼을 때만", 13, WARN, KR)
y += 56
for s in tail:
    y += draw_step(*s, y) + ROW_GAP

d.legend(H - 68, [("필수 구간", INFO), ("가장 큰 덩어리", ACC), ("조건부 구간", WARN)])
d.save("network-roadmap.svg")
