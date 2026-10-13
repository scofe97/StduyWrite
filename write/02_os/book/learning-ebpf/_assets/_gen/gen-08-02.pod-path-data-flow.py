# 타입 스펙: type-data-flow — 레인 둘(iptables 경로 · eBPF 경로) × 단계 다섯(수신 · 규칙 조회 · 전달 · Pod 스택 · 앱). 빈 칸은 그리지 않는다. focal 은 eBPF 레인의 Pod 스택 한 번 통과 노드와 그리로 가는 실선 화살표 하나.
# 사실 출처: 추출본 ebpf8.txt 860~915행(패킷이 호스트 스택·veth·Pod 스택을 지남, 같은 커널에서 같은 처리 두 번, eBPF 가 iptables·conntrack 을 건너뜀), 918~948행(iptables 선형 탐색 O(n), 해시 맵 O(1)),
#   Cilium 문서 network/concepts/routing(Pod 안 eth0 ↔ 호스트 lxcXXXXXX), network/ebpf/intro(XDP prefilter · TC ingress 에서 맵 조회).
# Layout formulas(type-data-flow §2): label_col_w 120, step_slot_w 168, n_steps 5 → 폭 988 (right_pad 28), header_h 52, lane_h 108, node 136×84(spec 100×64 를 글자 12px 규칙에 맞춰 확대), node_y=lane_top+12, legend 80.
#   step_cx(j)=120+168j+84 → 204·372·540·708·876, node_x=cx-68. 모든 좌표 4의 배수. 도식 시작을 제목 블록 아래 Y0=84 로 내린다. 칩(WB·DB…)은 이 도식의 값 종류가 아니라 쓰지 않는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LABEL_W, SLOT, NSTEP = 120, 168, 5
W = LABEL_W + NSTEP * SLOT + 28
Y0, HEAD, LANE = 84, 52, 108
NW, NH = 136, 84
H = Y0 + HEAD + 2 * LANE + 80
d = D(W, H, "LEARNING EBPF · 08-02 §2",
      "Pod 로 가는 패킷은 iptables 경로에서 스택을 두 번, eBPF 경로에서 한 번 지난다",
      "바깥 패킷이 eth0 에서 호스트 스택의 iptables·conntrack 규칙을 순서대로 훑고(O(n)) veth 를 건너 Pod 스택을 지나 앱에 닿는다. eBPF 경로는 NodePort 로 들어온 패킷을 eth0 의 XDP·TC 에서 서비스 맵 해시 조회(O(1))로 백엔드에 잇고, Host-Routing 이 켜져 있으면 호스트 스택을 건너뛰고 Pod 스택을 한 번 지난다.",
      "같은 패킷이 거치는 스택 횟수와 규칙 조회 비용이 다릅니다")

def kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
def cx(j): return LABEL_W + j * SLOT + SLOT // 2
def nx(j): return cx(j) - NW // 2
def lane_top(k): return Y0 + HEAD + k * LANE
def ny(k): return lane_top(k) + 12

# 레인 띠와 구분선
d.o.append(f'<rect x="12" y="{lane_top(0)}" width="{W-24}" height="{LANE}" fill="{PAPER2}" opacity="0.6"/>')
for k in range(3):
    d.line(12, lane_top(0) + k * LANE, W - 12, lane_top(0) + k * LANE, RULE, 0.8)
d.line(LABEL_W, lane_top(0), LABEL_W, lane_top(2), RULE, 0.8)

# 단계 머리
STEPS = [("01", "수신"), ("02", "규칙 조회"), ("03", "전달"), ("04", "Pod 스택"), ("05", "앱")]
for j, (num, lab) in enumerate(STEPS):
    focal = j == 3
    c = ACC if focal else MUTED
    d.o.append(f'<rect x="{cx(j) - 16}" y="{Y0 + 6}" width="32" height="16" rx="8" fill="{c}33" />')
    d.t(cx(j), Y0 + 18, num, 11, c, MONO, "middle", 600)
    d.t(cx(j), Y0 + 38, lab, 13, c, KR, "middle", 600 if focal else 400)

# 레인 라벨
LANES = [("iptables", "스택 2회"), ("eBPF", "스택 1회")]
for k, (a, b) in enumerate(LANES):
    y = lane_top(k) + LANE // 2
    d.t(LABEL_W // 2, y - 4, a, 13, MUTED, kr(a), "middle", 600)
    d.t(LABEL_W // 2, y + 14, b, 13, MUTED, KR)

# 화살표 먼저
def hop(k, j1, j2, c, m, sw=1.4, dash=None):
    y = ny(k) + NH // 2
    d.arrow([(nx(j1) + NW + 2, y), (nx(j2) - 6, y)], c, m, sw, dash)
for j in range(4):
    hop(0, j, j + 1, MUTED, "ar")
hop(1, 0, 1, MUTED, "ar")
hop(1, 3, 4, MUTED, "ar")
hop(1, 1, 3, ACC, "acc", 1.7)
# focal 화살표 라벨 — 종이색 마스크
lab = "Host-Routing 시 건너뜀"
mx = (nx(1) + NW + nx(3)) / 2
d.o.append(f'<rect x="{mx - 68}" y="{ny(1) + NH // 2 - 28}" width="136" height="20" fill="{PAPER}"/>')
d.t(mx, ny(1) + NH // 2 - 13, lab, 13, ACC, KR, "middle", 600)

# 노드: (레인, 단계, 제목, 부제1, 부제2, 색, focal)
NODES = [
    (0, 0, "eth0", "호스트 NIC", None, None, False),
    (0, 1, "호스트 스택", "iptables·conntrack", "선형 탐색 O(n)", WARN, False),
    (0, 2, "veth", "lxc* → eth0", None, None, False),
    (0, 3, "Pod 스택", "두 번째 통과", None, WARN, False),
    (0, 4, "앱", None, None, None, False),
    (1, 0, "eth0", "XDP · TC", None, None, False),
    (1, 1, "서비스 맵 조회", "해시 맵 O(1)", "NodePort → 백엔드", OK, False),
    (1, 3, "Pod 스택", "한 번 통과", None, ACC, True),
    (1, 4, "앱", None, None, None, False),
]
for k, j, title, s1, s2, c, focal in NODES:
    x, y = nx(j), ny(k)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}1F" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, NW, NH, c, 6, "12", 1.2)
    else:
        d.box(x, y, NW, NH, PAPER, RULE, 1.0, 6)
    tc = ACC if focal else (c or INK)
    d.t(cx(j), y + (30 if s1 else 48), title, 13, tc, kr(title), "middle", 600)
    # 영문 14자 넘는 줄은 상자 안에 들어오게 11px
    if s1: d.t(cx(j), y + 52, s1, 11 if (s1.isascii() or "·" in s1) and len(s1) > 14 else (13 if kr(s1) == KR else 12), MUTED, kr(s1))
    if s2: d.t(cx(j), y + 72, s2, 13 if kr(s2) == KR else 12, MUTED, kr(s2))

d.legend(H - 56, [("스택·규칙 비용", WARN), ("맵 조회", OK), ("한 번 통과", ACC)])
d.save("08-02.pod-path-data-flow.svg")
