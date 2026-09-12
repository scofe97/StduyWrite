# write/roadmap/network-roadmap.md §학습 순서 — 네트워크 학습 로드맵.
# 판형은 data-roadmap 과 같다 — 세로 척추에 국면과 단계를 걸고, 왼쪽에 배우는 개념을,
#   오른쪽에 자료가 다루지 않는 키워드를 뻗는다.
#
# 이 로드맵은 자료가 두 종류다. 정독 노트가 있는 자리(cntd·paw·CoreDNS·Istio·nk)와
#   소장본만 있고 노트가 없는 자리(Cilium·Learning eBPF·TCP/IP Illustrated)다.
#   후자는 부제 mono 슬롯에 "책만" 으로 표시한다. 노드 스타일로 올리면 배지·국면 accent 와
#   시각 어휘가 셋이 되어 읽히지 않는다. 출처의 SSOT 는 본문 §책 읽기 흐름 표다.
#
# 절단선은 3단계 뒤에 긋는다 — 1~3 이 노드 한 대, 4 부터가 클러스터다.
#   본문이 "Kubernetes 네트워크 장애의 상당수는 4단계가 아니라 2단계에서 풀린다"고 적은
#   자리라 이 선이 편집상 논점이다. accent 도 클러스터 국면 하나에만 쓴다.
# 타입 스펙: type-tree — 부모(국면)에서 자식(단계)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 48
CH_W, CH_H, CH_GAP = 256, 32, 8
BUS, ROW_GAP, PHASE_GAP = 190, 40, 36
NOTE_H = 76

BADGE = {"필수": INFO, "추천": OK, "선택": SOFT}

# (제목, 부제 mono, 배지, 왼쪽 개념, 오른쪽 자료 밖 키워드, 점선 여부)
phases = [
    ("호스트", "1~3단계", INFO, [
        ("1 · 연결", "cntd 1~5장 · TCP/IP Illustrated", "필수",
         ["socket · bind · listen · accept",
          "handshake · TCP 상태 · 재전송",
          "흐름 제어 · 혼잡 제어",
          "UDP · 단편화 · DNS 질의",
          "HTTP/1.1·2·3 · TLS 핸드셰이크"],
         ["listen 큐 · 포트 고갈", "OS CA bundle · truststore"], False),

        ("2 · Linux 경로", "networking 4편 · nk 2·3장", "필수",
         ["interface · MAC · ARP",
          "IP 주소 · 서브네팅 · CIDR",
          "라우팅 테이블 · next hop",
          "netns · veth · bridge",
          "netfilter · NAT · conntrack",
          "MTU · MSS · ICMP"],
         ["bonding · LACP", "policy routing · ip rule"], False),

        ("3 · 관측", "paw 1~5장 · CoreDNS 3·7장", "필수",
         ["캡처 위치 · 디스플레이 필터",
          "TCP 이상 판독 · RST · 재전송",
          "TLS 핸드셰이크 판독",
          "resolv.conf · ndots · NXDOMAIN",
          "Corefile · 플러그인 체인"],
         ["GRO · GSO · TSO 오프로딩", "tc qdisc · netem"], False),
    ]),

    ("클러스터", "4~5단계", ACC, [
        ("4 · Kubernetes", "04_networking 10편 · nk 4·5장", "필수",
         ["Pod IP · CNI · Pod CIDR",
          "오버레이 · VXLAN · native routing",
          "Service · EndpointSlice",
          "kube-proxy · iptables · IPVS",
          "클러스터 DNS · Service FQDN",
          "Ingress · Gateway API"],
         ["BGP · ECMP · Clos", "externalTrafficPolicy"], False),

        ("5 · 데이터패스와 정책", "Cilium · Learning eBPF — 책만", "추천",
         ["eBPF 프로그램 유형 · hook",
          "verifier · CO-RE · BTF",
          "NetworkPolicy · default deny",
          "L7 · FQDN 정책",
          "Hubble · 투명 암호화"],
         ["WireGuard 노드 간 암호화", "eBPF host routing"], True),
    ]),

    ("운영 경계", "6단계", OK, [
        ("6 · 운영 경계", "04_networking 08~10 · Istio 6장", "추천",
         ["dual-stack · 토폴로지 라우팅",
          "Windows HNS · HCS",
          "Envoy · Gateway · VirtualService",
          "mTLS · 기본값 닫아 가기",
          "Zero Trust 전제 셋"],
         ["ambient mode · ztunnel", "멀티클러스터 메시"], False),
    ]),
]

NOTES = {
    "호스트":
        "Kubernetes 네트워크 장애의 상당수가 4단계가 아니라 2단계에서 풀린다.",
    "클러스터":
        "5단계는 소장본만 있고 정독 노트가 없다. 점선 노드가 그 뜻이다.",
    "운영 경계":
        "실습 자료가 없는 유일한 단계다. zone 이 여럿이거나 컨트롤 플레인이 서야 한다.",
}
CUT_AFTER = "호스트"


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 24


ROOT_Y = 116 + 180
y = ROOT_Y + 48 + PHASE_GAP
for name, _s, _c, steps in phases:
    y += NODE_H + ROW_GAP
    for st in steps:
        y += row_h(st[3], st[4]) + ROW_GAP
    if NOTES.get(name):
        y += NOTE_H
    y += PHASE_GAP - ROW_GAP
    if name == CUT_AFTER:
        y += 56
H = y + 80

d = D(W, H, "WRITE · NETWORK ROADMAP",
      "네트워크 학습 로드맵",
      "애플리케이션이 여는 socket 에서 시작해 커널 패킷 경로로 내려간 뒤 Kubernetes 데이터패스로 "
      "다시 올라간다. 척추에 국면 셋과 단계 여섯을 걸고, 배우는 개념을 왼쪽에 자료가 다루지 않는 "
      "키워드를 오른쪽에 뻗었다. 1~3단계가 노드 한 대이고 4단계부터가 클러스터다.",
      "1~3 은 노드 한 대, 4 부터 클러스터입니다. 번호는 의존 순서이지 진도가 아닙니다")

LX, LY, LW, LH = 40, 96, 336, 180
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만")]):
    cy = LY + 56 + i * 28
    c = BADGE[lab]
    d.o.append(f'<rect x="{LX + 16}" y="{cy - 9}" width="34" height="17" rx="4" '
               f'fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(LX + 33, cy + 3, lab, 11, c, KR)
    d.t(LX + 60, cy + 3, txt, 13, MUTED, KR, "start")
d.t(LX + 16, LY + 148, "왼쪽 — 배우는 개념 · 오른쪽 — 자료 밖 키워드", 12, SOFT, KR, "start")
d.t(LX + 16, LY + 166, "점선 — 소장본만 있고 정독 노트가 없는 자리", 12, SOFT, KR, "start")

RX, RY, RW, RH = 624, 96, 336, 180
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("k8s-roadmap", "오브젝트 배포와 클러스터 운영"),
        ("os-roadmap", "socket 과 FD 의 커널 쪽"),
        ("cntd 6~8장", "무선 · 물리 계층 · 암호 일반"),
        ("06_observability", "앱이 내보내는 지표와 트레이스")]):
    cy = RY + 56 + i * 32
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 48, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 30, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 48, SX, H - 116, RULE, 1.4)


def draw_step(title, sub, badge, left, right, dashed, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        if not items:
            continue
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, label in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * 14) - (CH_W if side == "left" else 0)
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * 14, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.t(bx + CH_W / 2, cy + 5, label, 12, MUTED, KR, "middle")
    if dashed:
        d.o.append(f'<rect x="{SX - NODE_W/2}" y="{mid - NODE_H/2}" width="{NODE_W}" '
                   f'height="{NODE_H}" rx="6" fill="{PAPER}" stroke="{SOFT}" '
                   f'stroke-width="1.0" stroke-dasharray="4 4"/>')
    else:
        d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, RULE, 1.0)
    c = BADGE[badge]
    d.o.append(f'<rect x="{SX - NODE_W/2 + 12}" y="{mid - NODE_H/2 + 8}" width="34" height="17" '
               f'rx="4" fill="{c}22" stroke="{c}" stroke-width="0.9"/>')
    d.t(SX - NODE_W / 2 + 29, mid - NODE_H / 2 + 20, badge, 11, c, KR)
    d.t(SX + 12, mid - 4, title, 13, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, MONO)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


def draw_phase(name, stage, color, steps, y):
    if color is ACC:
        d.tone(SX - NODE_W / 2, y, NODE_W, NODE_H, ACC, 6, "16", 1.4)
    else:
        d.box(SX - NODE_W / 2, y, NODE_W, NODE_H, PAPER, color, 1.2)
    d.t(SX, y + 22, name, 15, ACC if color is ACC else INK, KR, "middle", 600)
    d.t(SX, y + 40, stage, 12, SOFT, MONO)
    y += NODE_H + ROW_GAP
    for st in steps:
        y += draw_step(*st, y) + ROW_GAP
    if NOTES.get(name):
        y += draw_note(NOTES[name], y)
    return y + PHASE_GAP - ROW_GAP


y = ROOT_Y + 48 + PHASE_GAP
for ph in phases:
    y = draw_phase(*ph, y)
    if ph[0] == CUT_AFTER:
        d.line(40, y + 20, W - 40, y + 20, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y + 8}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 25, "1~3단계는 노드 한 대 · 4단계부터 클러스터", 13, WARN, KR)
        y += 56

d.legend(H - 68, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("클러스터 구간", ACC),
                  ("노드 한 대와 클러스터의 경계", WARN)])
d.save("network-roadmap.svg")
