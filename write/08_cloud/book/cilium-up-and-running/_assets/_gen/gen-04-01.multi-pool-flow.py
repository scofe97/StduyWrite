# 타입 스펙: type-data-flow — 네임스페이스 주석이 고른 CiliumPodIPPool 에서 한 노드가 풀마다 /27 을 받아 Pod 주소로 내주는 흐름.
# 사실 출처: 추출본 cil4.txt 줄 491-523 · 544-553 · 560-571, docs.cilium.io/en/stable/network/concepts/ipam/multi-pool/ (ipam.cilium.io/ip-pool).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 424
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §4", "네임스페이스별 풀에서 Pod 주소까지",
      "같은 노드가 풀마다 /27 을 따로 받고 Pod 는 자기 풀의 대역에서 주소를 받습니다",
      "acme-corp · foobar-inc 두 테넌트")

X_NS, W_NS = 24, 188
X_POOL, W_POOL = 276, 172
X_NODE, W_NODE = 512, 204
X_POD, W_POD = 780, 116
HEAD_Y = 108
ROWS = [(132, "acme-corp", "ip-pool=acme-pool", "acme-pool", "10.20.0.0/16 · /27", "10.20.0.0/27", "10.20.0.25"),
        (252, "foobar-inc", "ip-pool=foobar-pool", "foobar-pool", "10.30.0.0/16 · /27", "10.30.0.0/27", "10.30.0.28")]
BH = 64

for x, w, t in [(X_NS, W_NS, "NAMESPACE"), (X_POOL, W_POOL, "CILIUMPODIPPOOL"), (X_NODE, W_NODE, "CILIUMNODE"), (X_POD, W_POD, "POD")]:
    d.t(x + w / 2, HEAD_Y, t, 8, SOFT, MONO, "middle")

node_y, node_h = 124, 224
d.tone(X_NODE, node_y, W_NODE, node_h, ACC, r=8, op="10", sw=1.4)
d.t(X_NODE + W_NODE / 2, node_y + 18, "kind-worker2", 11, ACC, MONO, "middle", 600)

for y, ns, ann, pool, pcidr, nodecidr, pod in ROWS:
    d.box(X_NS, y, W_NS, BH, PAPER2, INFO, 1.0, 6)
    d.t(X_NS + W_NS / 2, y + 26, ns, 12, INK, MONO, "middle", 600)
    d.t(X_NS + W_NS / 2, y + 46, ann, 10, INFO, MONO, "middle")
    d.box(X_POOL, y, W_POOL, BH, PAPER2, INFO, 1.0, 6)
    d.t(X_POOL + W_POOL / 2, y + 26, pool, 12, INK, MONO, "middle", 600)
    d.t(X_POOL + W_POOL / 2, y + 46, pcidr, 10, INFO, MONO, "middle")
    d.chip(X_NODE + W_NODE / 2, y + BH / 2 + 8, nodecidr, ACC, size=11)
    d.box(X_POD, y, W_POD, BH, PAPER2, OK, 1.0, 6)
    d.t(X_POD + W_POD / 2, y + 26, "nginx", 12, INK, MONO, "middle", 600)
    d.t(X_POD + W_POD / 2, y + 46, pod, 11, OK, MONO, "middle")
    cy = y + BH / 2
    d.arrow([(X_NS + W_NS, cy), (X_POOL, cy)], INFO, "info", 1.5)
    d.arrow([(X_POOL + W_POOL, cy), (X_NODE, cy)], INFO, "info", 1.5)
    d.arrow([(X_NODE + W_NODE, cy), (X_POD, cy)], OK, "ok", 1.5)
    d.t((X_NS + W_NS + X_POOL) / 2, cy - 10, "주석", 12, MUTED, KR, "middle")
    d.t((X_POOL + W_POOL + X_NODE) / 2, cy - 10, "/27 몫", 12, MUTED, KR, "middle")
    d.t((X_NODE + W_NODE + X_POD) / 2, cy - 10, "Pod IP", 12, MUTED, KR, "middle")

d.legend(372, [("선언한 값", INFO), ("노드가 받은 대역", ACC), ("Pod 주소", OK)])
d.save("04-01.multi-pool-flow.svg")
