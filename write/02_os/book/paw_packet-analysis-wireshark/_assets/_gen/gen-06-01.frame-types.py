# 06-01 학습 목표 뒤 전체 지도 — 802.11 프레임 네 종류와 그 아래 주요 서브타입.
# 값은 원문 표에 적힌 것만 쓴다. 원문이 값과 필터를 다르게 적은 자리는 노트 본문에서 정오로 다룬다.
# 타입 스펙: type-tree — 부모(프레임 종류) → 자식(서브타입). 루트를 왼쪽에 두고 오른쪽으로
#           펼치며 연결선은 직교 엘보다. focal 은 루트 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

BRANCHES = [
    ("Management · type 0", [("beacon frame", "0x08 · AP 가 자기를 알립니다"),
                             ("probe request/response", "0x04 / 0x05"),
                             ("authentication", "0x0b"),
                             ("association request/response", "0x00 / 0x01"),
                             ("deauthentication", "0x0c")]),
    ("Control · type 1", [("request/clear to send", "0x1b / 0x1c"),
                          ("acknowledgement", "0x1d"),
                          ("block ack request/ack", "0x18 / 0x19")]),
    ("Data · type 2", [("data", "0x20 · 페이로드를 나릅니다"),
                       ("qos data", "0x28"),
                       ("null function", "0x24")]),
    ("Extension · type 3", [("확장 프레임", "wlan_ext 로 표시")]),
]
LEAF_STRIDE, LEAF_H = 44, 36
ROOT_W, BR_W, LEAF_W = 168, 208, 344
X_ROOT, X_BR, X_LEAF = 24, 236, 488
Y0 = 112
n = sum(len(v) for _, v in BRANCHES)
W = X_LEAF + LEAF_W + 32
H = Y0 + n * LEAF_STRIDE + 76

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 06-01",
      "802.11 프레임 네 종류",
      "802.11 은 프레임을 관리·제어·데이터·확장 넷으로 나눈다. wlan.fc.type 이 종류를, wlan.fc.type_subtype 이 그 안의 서브타입을 가리킨다.",
      "이더넷과 달리 데이터가 아닌 프레임이 대부분입니다 — 그것을 보려면 monitor 모드가 필요합니다")

def leaf_y(i): return Y0 + i * LEAF_STRIDE
idx = 0; br_mid = []
for name, leaves in BRANCHES:
    ys = [leaf_y(idx + j) + LEAF_H / 2 for j in range(len(leaves))]
    mid = (ys[0] + ys[-1]) / 2; br_mid.append(mid)
    bus = X_BR + BR_W + 24
    if len(ys) > 1: d.line(bus, ys[0], bus, ys[-1], RULE, 1.0)
    d.line(X_BR + BR_W, mid, bus, mid, RULE, 1.0)
    for y in ys: d.line(bus, y, X_LEAF - 4, y, RULE, 1.0)
    idx += len(leaves)

root_mid = (br_mid[0] + br_mid[-1]) / 2
root_bus = X_ROOT + ROOT_W + 24
d.line(root_bus, br_mid[0], root_bus, br_mid[-1], RULE, 1.0)
d.line(X_ROOT + ROOT_W, root_mid, root_bus, root_mid, RULE, 1.0)
for m in br_mid: d.line(root_bus, m, X_BR - 4, m, RULE, 1.0)

d.o.append(f'<rect x="{X_ROOT}" y="{root_mid - 26}" width="{ROOT_W}" height="52" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(X_ROOT + ROOT_W / 2, root_mid - 2, "802.11 프레임", 14, ACC, KR, "middle", 600)
d.t(X_ROOT + ROOT_W / 2, root_mid + 16, "wlan", 10, MUTED, MONO)

idx = 0
for bi, (name, leaves) in enumerate(BRANCHES):
    m = br_mid[bi]
    d.box(X_BR, m - 22, BR_W, 44, PAPER2, RULE, 1.0, 6)
    d.t(X_BR + BR_W / 2, m + 4, name, 12, INK, MONO, "middle", 600)
    for j, (nm, meaning) in enumerate(leaves):
        y = leaf_y(idx + j)
        d.box(X_LEAF, y, LEAF_W, LEAF_H, PAPER, RULE, 0.8, 6)
        d.t(X_LEAF + 14, y + 23, nm, 11, INK, MONO, "start", 600)
        d.t(X_LEAF + LEAF_W - 14, y + 23, meaning, 11, MUTED, KR, "end")
    idx += len(leaves)

d.legend(H - 52, [("wlan.fc.type 이 가르는 지점", ACC)])
d.save("06-01.frame-types.svg")
