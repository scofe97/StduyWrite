# 03-02 학습 목표 뒤 전체 지도 — 증상에서 이 편의 어느 절로 가는지.
# 타입 스펙: type-tree — 부모(증상 갈래) → 자식(구체 증상과 담당 절). 루트를 왼쪽에 두고
#           오른쪽으로 펼치며 연결선은 직교 엘보다. focal 은 루트 하나만 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

BRANCHES = [
    ("연결이 안 됨", [("SYN 에 RST 가 돌아옴", "§1 · 서버 미기동"),
                    ("handshake 뒤 RST", "§1 · 연결 위조·중단")]),
    ("연결이 안 닫힘", [("CLOSE_WAIT 가 늘기만 함", "§2 · 애플리케이션 코드"),
                     ("TIME_WAIT 가 많음", "§3 · 대개 정상")]),
    ("느림", [("네트워크가 느린가", "§4 · ping·traceroute"),
             ("수신 측이 느린가", "§4 · window_size")]),
    ("전송이 이상함", [("같은 세그먼트가 반복", "§5 · 재전송"),
                   ("윈도우가 0 이 됨", "§5 · ZeroWindow"),
                   ("같은 ACK 가 반복", "§5 · 중복 ACK")]),
]

LEAF_STRIDE, LEAF_H = 48, 40
ROOT_W, BR_W, LEAF_W = 176, 176, 344
X_ROOT, X_BR, X_LEAF = 24, 244, 456
Y0 = 112
n = sum(len(v) for _, v in BRANCHES)
W = X_LEAF + LEAF_W + 32
H = Y0 + n * LEAF_STRIDE + 76

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-02",
      "증상에서 절로",
      "TCP 가 어긋날 때 겉으로 보이는 증상을 네 갈래로 나누고, 각 증상이 이 편의 어느 절에서 다뤄지는지 잇는다.",
      "증상은 넷이지만 원인의 주인은 둘입니다 — 커널이 아니라 애플리케이션이거나, 경로입니다")

def leaf_y(i): return Y0 + i * LEAF_STRIDE

idx = 0; br_mid = []
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

d.o.append(f'<rect x="{X_ROOT}" y="{root_mid - 26}" width="{ROOT_W}" height="52" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(X_ROOT + ROOT_W / 2, root_mid - 2, "TCP 가 어긋났다", 14, ACC, KR, "middle", 600)
d.t(X_ROOT + ROOT_W / 2, root_mid + 16, "ss · Wireshark", 10, MUTED, MONO)

idx = 0
for bi, (name, leaves) in enumerate(BRANCHES):
    m = br_mid[bi]
    d.box(X_BR, m - 22, BR_W, 44, PAPER2, RULE, 1.0, 6)
    d.t(X_BR + BR_W / 2, m + 4, name, 13, INK, KR, "middle", 600)
    for j, (sym, where) in enumerate(leaves):
        y = leaf_y(idx + j)
        d.box(X_LEAF, y, LEAF_W, LEAF_H, PAPER, RULE, 0.8, 6)
        d.t(X_LEAF + 14, y + 25, sym, 12, INK, KR, "start")
        d.t(X_LEAF + LEAF_W - 14, y + 25, where, 11, MUTED, MONO, "end")
    idx += len(leaves)

d.legend(H - 52, [("여기서 시작합니다", ACC)])
d.save("03-02.symptom-tree.svg")
