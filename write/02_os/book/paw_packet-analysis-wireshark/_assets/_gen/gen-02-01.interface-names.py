# 02-01 §2 — 인터페이스 이름이 OS 별로 어떤 규칙을 따르는가. 원문 도해(common interface names)를
# 같은 정보로 옮기되 마인드맵 대신 계층으로 세운다.
# 타입 스펙: type-tree — 부모(OS) → 자식(이름 규칙) 관계. 루트를 왼쪽에 두고 오른쪽으로 펼친다.
#           연결선은 직교 엘보이고, focal 은 루트 하나만 건다(스펙 안티패턴: 루트와 잎에 동시 금지).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

BRANCHES = [
    ("Linux", [("lo", "가상 루프백"), ("any", "가상 인터페이스"),
               ("eth0 · eth1", "이더넷"), ("wlan0 · wlan1", "무선 LAN")]),
    ("BSD · AIX", [("lo0", "가상 루프백"), ("ppp0 · ppp1", "PPP")]),
    ("macOS", [("lo0", "루프백"), ("ppp0 · ppp1", "PPP"),
               ("en0 · en1 …", "이더넷 또는 AirPort")]),
    ("Solaris", [("trN", "토큰 링"), ("beN · bgeN · ceN", "이더넷 계열"),
                 ("sxpN", "FDDI")]),
    ("Windows", [("카드 제조사가 정한 이름", "일반 전화접속 어댑터")]),
]

LEAF_STRIDE, LEAF_H = 44, 36
ROOT_W, BR_W, LEAF_W = 168, 168, 320
X_ROOT, X_BR, X_LEAF = 24, 236, 448
Y0 = 108
n_leaves = sum(len(v) for _, v in BRANCHES)
W = X_LEAF + LEAF_W + 32                                  # 800
H = Y0 + n_leaves * LEAF_STRIDE + 76                      # 108 + 572 + 76 = 756

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-01 §2",
      "인터페이스 이름 규칙",
      "OS 별 인터페이스 이름과 그 이름이 가리키는 네트워크 종류. 이름만 보고 어떤 매체를 잡게 되는지 판단하기 위한 표.",
      "이름을 읽을 줄 알면 목록에서 어느 인터페이스를 고를지가 정해집니다")

def leaf_y(i): return Y0 + i * LEAF_STRIDE

# 연결선 먼저 — 직교 엘보
idx = 0
br_mid = []
for name, leaves in BRANCHES:
    ys = [leaf_y(idx + j) + LEAF_H / 2 for j in range(len(leaves))]
    mid = (ys[0] + ys[-1]) / 2
    br_mid.append(mid)
    bus = X_BR + BR_W + 24
    if len(ys) > 1:
        d.line(bus, ys[0], bus, ys[-1], RULE, 1.0)
    d.line(X_BR + BR_W, mid, bus, mid, RULE, 1.0)
    for y in ys:
        d.line(bus, y, X_LEAF - 4, y, RULE, 1.0)
    idx += len(leaves)

root_mid = (br_mid[0] + br_mid[-1]) / 2
root_bus = X_ROOT + ROOT_W + 24
d.line(root_bus, br_mid[0], root_bus, br_mid[-1], RULE, 1.0)
d.line(X_ROOT + ROOT_W, root_mid, root_bus, root_mid, RULE, 1.0)
for m in br_mid:
    d.line(root_bus, m, X_BR - 4, m, RULE, 1.0)

# 루트
d.o.append(f'<rect x="{X_ROOT}" y="{root_mid - 26}" width="{ROOT_W}" height="52" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(X_ROOT + ROOT_W / 2, root_mid - 2, "인터페이스 이름", 14, ACC, KR, "middle", 600)
d.t(X_ROOT + ROOT_W / 2, root_mid + 16, "ifconfig · dumpcap -D", 10, MUTED, MONO)

# 가지와 잎
idx = 0
for bi, (name, leaves) in enumerate(BRANCHES):
    m = br_mid[bi]
    d.box(X_BR, m - 22, BR_W, 44, PAPER2, RULE, 1.0, 6)
    d.t(X_BR + BR_W / 2, m + 4, name, 13, INK, KR, "middle", 600)
    for j, (nm, meaning) in enumerate(leaves):
        y = leaf_y(idx + j)
        d.box(X_LEAF, y, LEAF_W, LEAF_H, PAPER, RULE, 0.8, 6)
        d.t(X_LEAF + 14, y + 23, nm, 12, INK, MONO, "start", 600)
        d.t(X_LEAF + LEAF_W - 14, y + 23, meaning, 12, MUTED, KR, "end")
    idx += len(leaves)

d.legend(H - 52, [("이름을 얻는 자리", ACC)])
d.save("02-01.interface-names.svg")
