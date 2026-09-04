# write/network-roadmap.md §도입 — Kubernetes 네트워크 학습 로드맵.
# 네트워크는 02_os·08_cloud·99_ETC 에 걸쳐 있어 문서를 write/ 직계에 둔다. eyebrow 도 WRITE 다.
# 판형은 roadmap.sh 를 따른다 — 세로 척추에 국면과 단계를 걸고, 개념을 좌우로 뻗는다.
# 점선 테두리 박스는 책이 다루지 않는 키워드다. 실선(책)과 점선(책 밖)을 한 눈에 가르려고 나눴다.
# 낡음 기준을 적용해 13단계에서 HPBN(2013)을, 15단계에서 Programming Kubernetes(2019)를 뺐다.
# 그 자리는 RFC 9000·9113·9114 와 client-go 공식 문서가 맡는다. 근거는 본문 낡음 점검 절에 있다.
# 조건부 세 단계는 국면 노드를 두지 않고 절단선 아래 꼬리로 붙인다.
#   국면을 여섯으로 만들면 type-tree 의 한 단계 너비 5 를 넘기 때문이고, 필수와 조건부는 층이 다르다.
# 높이는 좌우 박스 개수에서 산출한다(고정값 금지). 연결선은 스펙대로 직교 엘보로만 긋는다.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계층. coral 은 데이터패스 국면 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, KR, MONO

SX = 500
NODE_W, NODE_H = 280, 48
CH_W, CH_H, CH_GAP = 236, 32, 8
BUS, ROW_GAP, PHASE_GAP = 176, 40, 36

phases = [
    ("바닥과 눈", "0~1단계", INFO, [
        ("0 · Learning Modern Linux", "7장",
         ["네트워크 네임스페이스", "인터페이스와 라우팅"], ["ip · ss 진단 도구"],
         ["ip netns 실습", "veth · 브리지 만들기"]),
        ("1 · Packet Analysis with Wireshark", "1~5장",
         ["캡처와 필터 문법", "TCP 수립 · 종료"], ["재전송과 지연 분석", "TLS 복호화 · DNS · HTTP"],
         ["MTU · PMTUD 블랙홀", "conntrack 포화"]),
    ]),
    ("클러스터 모델", "2~4단계", INFO, [
        ("2 · Networking and Kubernetes", "3~5장",
         ["컨테이너 네트워킹 모드", "Pod 네트워크 모델"], ["Service 다섯 유형", "EndpointSlice"],
         ["CNI 스펙과 체이닝", "Multus · SR-IOV"]),
        ("3 · Kubernetes in Action 2nd", "11~13장",
         ["Service 선언과 어피니티", "Ingress 와 TLS"], ["Gateway API 와 HTTPRoute"],
         ["GAMMA 이니셔티브", "Ingress 에서 이행하기"]),
        ("4 · Learning CoreDNS", "1~8장 · 2019",
         ["Corefile 과 플러그인 체인", "존 데이터와 위임"], ["서비스 디스커버리", "질의 조작과 관측"],
         ["ndots:5 질의 폭증", "NodeLocal DNSCache"]),
    ]),
    ("데이터패스", "5~6단계", ACC, [
        ("5 · Learning eBPF", "1~3 / 6~9장",
         ["프로그램 구조와 맵", "verifier 가 거는 제약"], ["XDP · TC · socket 훅", "커널에서 패킷 가로채기"],
         ["cgroup · sockmap 훅", "bpftool"]),
        ("6 · Cilium Up and Running", "16장",
         ["데이터패스", "IPAM 과 Pod IP", "kube-proxy 대체"],
         ["L3~L7 · FQDN 정책", "egress 와 전송 암호화", "Hubble 흐름 관측"],
         ["kube-proxy nftables 모드", "ClusterMesh · netkit"]),
    ]),
    ("정책과 메시", "7~9단계", INFO, [
        ("7 · Policy as Code · KBP", "4·5·7·8장 / 9·11장",
         ["OPA 와 Rego 판정", "어드미션 컨트롤"], ["Gatekeeper · Kyverno"],
         ["AdminNetworkPolicy", "CEL 어드미션 정책"]),
        ("8 · Istio in Action", "1~9장",
         ["메시가 인프라로 민 것", "Envoy 와 데이터 플레인"], ["게이트웨이와 트래픽 라우팅", "mTLS 와 메시 관측"],
         ["Envoy xDS 프로토콜", "SPIFFE · SPIRE"]),
        ("9 · Sidecar-less Istio Explained", "4장",
         ["앰비언트 모드의 전제", "ztunnel 이 맡는 L4"], ["waypoint 가 맡는 L7", "사이드카와의 차이"],
         ["waypoint 배치 단위"]),
    ]),
    ("운영과 신뢰", "10~12단계", INFO, [
        ("10 · Production Kubernetes", "5·6·10장",
         ["오버레이 · 라우팅 · BGP", "서비스 라우팅 선택"], ["워크로드 신원"],
         ["Topology Aware Routing", "CNI 성능 벤치마크"]),
        ("11 · Container Security 2판", "10·11장 · 2025",
         ["계층별 네트워크 차단", "컨테이너 방화벽"], ["TLS 로 컴포넌트 잇기", "인증서와 CA 의 역할"],
         ["인증서 회전과 SDS", "cert-manager"]),
        ("12 · Zero Trust · CKS · RWC", "4~8 / 2·3·5 / 5·9장",
         ["신뢰 모델과 인가 결정", "트래픽 신뢰 기준"], ["클러스터 하드닝", "키 교환과 보안 전송"],
         ["암호화를 겹쳐 쓸 때의 판단"]),
    ]),
]

tail = [
    ("13 · HTTP:2 in Action · RFC 9000·9114", "4·8장 / 공식",
     ["HTTP/2 프레이밍", "HPACK 헤더 압축"], ["QUIC 와 HTTP/3 는 RFC 로"],
     ["Envoy 의 QUIC 지원", "gRPC 로드밸런싱"]),
    ("14 · AWS · OpenStack · OpenShift", "5·9장 / 6장 / 3·4장",
     ["VPC 와 로드밸런서", "Neutron"], ["OpenShift 운영"],
     ["ENI 한계와 prefix delegation", "OVN-Kubernetes"]),
    ("15 · Go · client-go 공식 문서", "1~7장 / 공식",
     ["소켓과 주소 해석", "TCP · UDP 직접 다루기"], ["sample-controller 로 배우기"],
     ["CNI 의 ADD · DEL · CHECK", "netlink 로 veth"]),
]

def row_h(left, right, extra):
    n = max(len(left), len(right) + len(extra))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24

y = 116 + 48 + PHASE_GAP
for _, _, _, steps in phases:
    y += NODE_H + ROW_GAP
    for s in steps:
        y += row_h(s[2], s[3], s[4]) + ROW_GAP
    y += PHASE_GAP - ROW_GAP
y += 56                                   # 절단선
for s in tail:
    y += row_h(s[2], s[3], s[4]) + ROW_GAP
H, W = y + 76, 1000

d = D(W, H, "WRITE · NETWORK ROADMAP",
      "Kubernetes 네트워크 학습 로드맵",
      "위에서 아래로 읽는 순서. 척추에 국면 다섯과 단계 열여섯을 걸고 각 단계에서 배우는 개념을 좌우로 뻗었다. "
      "실선 박스는 책이 다루는 개념이고 점선 박스는 책이 다루지 않아 공식 문서로 채울 키워드다. "
      "절단선 아래 셋은 목표가 생겼을 때만 여는 조건부 단계다.",
      "실선은 책이 다루는 개념, 점선은 공식 문서로 채울 키워드입니다")

ROOT_Y = 116
d.box(SX - 120, ROOT_Y, 240, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 100, RULE, 1.4)

def draw_step(title, chap, left, right, extra, y):
    h = row_h(left, right, extra)
    mid = y + h / 2
    for side, items in (("left", [(v, False) for v in left]),
                        ("right", [(v, False) for v in right] + [(v, True) for v in extra])):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (label, dashed) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 40) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 40, cy, RULE, 1.0)
            if dashed:
                d.o.append(f'<rect x="{bx}" y="{cy - CH_H/2}" width="{CH_W}" height="{CH_H}" rx="6" '
                           f'fill="{PAPER}" stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
                d.t(bx + CH_W / 2, cy + 5, label, 13, SOFT, KR, "middle")
            else:
                d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
                d.t(bx + CH_W / 2, cy + 5, label, 13, MUTED, KR, "middle")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    d.t(SX, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 14, chap, 12, SOFT, MONO)
    return h

y = ROOT_Y + 48 + PHASE_GAP
for name, stage, color, steps in phases:
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for s in steps:
        y += draw_step(*s, y) + ROW_GAP
    y += PHASE_GAP - ROW_GAP

# 필수와 조건부를 가르는 절단선
d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
d.o.append(f'<rect x="{SX - 108}" y="{y + 8}" width="216" height="22" rx="4" fill="{PAPER}"/>')
d.t(SX, y + 25, "여기부터는 목표가 생겼을 때만", 13, WARN, KR)
y += 56
for s in tail:
    y += draw_step(*s, y) + ROW_GAP

d.legend(H - 68, [("책이 다루는 개념", INFO), ("가장 큰 덩어리", ACC), ("책 밖 키워드", SOFT)])
d.save("network-roadmap.svg")
