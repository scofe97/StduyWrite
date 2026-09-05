# 05-02 §2 — 원문이 dig·nslookup 예제로 드는 DNS 레코드 타입을 쓰임새로 묶는다.
# 숫자 값은 원문의 dns.qry.type 표에 적힌 것만 쓰고, 원문에 없는 값은 적지 않는다.
# 타입 스펙: type-tree — 부모(쓰임새) → 자식(레코드 타입). 루트를 왼쪽에 두고 오른쪽으로 펼치며
#           연결선은 직교 엘보다. focal 은 루트 하나만 건다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

BRANCHES = [
    ("주소를 묻는다", [("A", "IPv4 주소 · dns.qry.type == 1"),
                   ("AAAA", "IPv6 주소 · dns.qry.type == 28")]),
    ("이름을 잇는다", [("CNAME", "별칭을 실제 이름으로"),
                   ("PTR", "주소를 이름으로 · 역방향 조회")]),
    ("권한을 묻는다", [("NS", "이 존의 이름 서버 · dns.qry.type == 2"),
                   ("SOA", "권한 정보 · 이름 서버와 메일")]),
    ("부가 정보", [("MX", "메일 교환 · dns.qry.type == 15"),
                ("TXT", "텍스트 레코드"),
                ("ANY", "모든 종류 · dns.qry.type == 255"),
                ("AXFR", "존 파일 전송 · 주에서 보조로")]),
]
LEAF_STRIDE, LEAF_H = 48, 40
ROOT_W, BR_W, LEAF_W = 176, 176, 360
X_ROOT, X_BR, X_LEAF = 24, 244, 456
Y0 = 112
n = sum(len(v) for _, v in BRANCHES)
W = X_LEAF + LEAF_W + 32
H = Y0 + n * LEAF_STRIDE + 76

d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-02 §2",
      "DNS 레코드 타입을 쓰임새로",
      "원문이 dig·nslookup 예제로 드는 레코드 타입을 네 갈래로 묶은 것. 무엇을 알고 싶은지가 정해지면 타입이 정해지고, 타입이 정해지면 필터가 정해진다.",
      "질의 타입 하나가 dns.qry.type 필터 값 하나에 대응합니다")

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
d.t(X_ROOT + ROOT_W / 2, root_mid - 2, "무엇을 묻는가", 14, ACC, KR, "middle", 600)
d.t(X_ROOT + ROOT_W / 2, root_mid + 16, "dns · UDP 53", 10, MUTED, MONO)

idx = 0
for bi, (name, leaves) in enumerate(BRANCHES):
    m = br_mid[bi]
    d.box(X_BR, m - 22, BR_W, 44, PAPER2, RULE, 1.0, 6)
    d.t(X_BR + BR_W / 2, m + 4, name, 13, INK, KR, "middle", 600)
    for j, (nm, meaning) in enumerate(leaves):
        y = leaf_y(idx + j)
        d.box(X_LEAF, y, LEAF_W, LEAF_H, PAPER, RULE, 0.8, 6)
        d.t(X_LEAF + 14, y + 25, nm, 12, INK, MONO, "start", 600)
        d.t(X_LEAF + LEAF_W - 14, y + 25, meaning, 11, MUTED, KR, "end")
    idx += len(leaves)

d.legend(H - 52, [("질의의 출발점", ACC)])
d.save("05-02.dns-record-types.svg")
