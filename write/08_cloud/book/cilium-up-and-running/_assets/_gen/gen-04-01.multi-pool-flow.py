# 타입 스펙: type-data-flow — 네임스페이스 주석·기본 폴백으로 고른 CiliumPodIPPool 에서 노드가 풀별 /27 을 받고 수요 증가 시 동적 확장되는 흐름.
# 사실 출처: 추출본 ch04.txt 줄 431-440 · 491-524 · 544-553 · 560-622, docs.cilium.io/en/v1.20/network/concepts/ipam/multi-pool/ (ipam.cilium.io/ip-pool).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 940, 496
d = D(W, H, "CILIUM UP AND RUNNING · 04-01 §4", "네임스페이스별 풀 선택과 동적 /27 확장",
      "한 노드가 풀마다 /27 을 따로 받고, 수요가 40개로 늘면 두 번째 /27 을 이어 붙입니다",
      "kind-worker2 · acme-corp(40 replica) · foobar-inc(10 replica) · default(매칭 없을 때)")

X_NS, W_NS = 24, 184
X_POOL, W_POOL = 264, 176
X_NODE, W_NODE = 496, 224
X_POD, W_POD = 776, 140
HEAD_Y = 104
ROWS = [
    (128, "acme-corp", "ip-pool=acme-pool", "acme-pool", "10.20.0.0/16 · /27", "10.20.0.0/27 + .32/27", "nginx ×40", "10.20.0.25", "주석", "수요 40"),
    (224, "foobar-inc", "ip-pool=foobar-pool", "foobar-pool", "10.30.0.0/16 · /27", "10.30.0.0/27", "nginx ×10", "10.30.0.28", "주석", "수요 10"),
    (320, "(주석·셀렉터 없음)", "기본 풀 폴백", "default", "10.10.0.0/16 · /27", "10.10.0.0/27", "인프라 주소", "router · health", "폴백", "요청 16"),
]
BH = 68

for x, w, t in [(X_NS, W_NS, "NAMESPACE / POD"), (X_POOL, W_POOL, "CILIUMPODIPPOOL"), (X_NODE, W_NODE, "CILIUMNODE"), (X_POD, W_POD, "POD / ENDPOINT")]:
    d.t(x + w / 2, HEAD_Y, t, 8, SOFT, MONO, "middle")

node_y, node_h = 116, 288
d.tone(X_NODE, node_y, W_NODE, node_h, ACC, r=8, op="10", sw=1.4)
d.t(X_NODE + W_NODE / 2, node_y + 18, "kind-worker2 · pools.allocated", 10, ACC, MONO, "middle", 600)

for idx, (y, ns, ann, pool, pcidr, nodecidr, pod_t, pod_ip, a1, a2) in enumerate(ROWS):
    d.box(X_NS, y, W_NS, BH, PAPER2, INFO if idx < 2 else RULE, 1.0, 6)
    d.t(X_NS + W_NS / 2, y + 27, ns, 12 if idx < 2 else 13, INK, MONO if idx < 2 else KR, "middle", 600)
    d.t(X_NS + W_NS / 2, y + 48, ann, 10 if idx < 2 else 12, INFO if idx < 2 else MUTED, MONO if idx < 2 else KR, "middle")

    d.box(X_POOL, y, W_POOL, BH, PAPER2, INFO if idx < 2 else RULE, 1.0, 6)
    d.t(X_POOL + W_POOL / 2, y + 27, pool, 12, INK, MONO, "middle", 600)
    d.t(X_POOL + W_POOL / 2, y + 48, pcidr, 10, INFO if idx < 2 else MUTED, MONO, "middle")

    d.chip(X_NODE + W_NODE / 2, y + BH / 2 + 10, nodecidr, ACC if idx == 0 else MUTED, size=10 if idx == 0 else 11)

    d.box(X_POD, y, W_POD, BH, PAPER2, OK if idx < 2 else RULE, 1.0, 6)
    d.t(X_POD + W_POD / 2, y + 27, pod_t, 12, INK, MONO, "middle", 600)
    d.t(X_POD + W_POD / 2, y + 48, pod_ip, 11, OK if idx < 2 else MUTED, MONO, "middle")

    cy = y + BH / 2
    col_in = INFO if idx < 2 else MUTED
    mk_in = "info" if idx < 2 else "ar"
    d.arrow([(X_NS + W_NS, cy), (X_POOL, cy)], col_in, mk_in, 1.4)
    d.arrow([(X_POOL + W_POOL, cy), (X_NODE, cy)], ACC if idx == 0 else col_in, "acc" if idx == 0 else mk_in, 1.4)
    d.arrow([(X_NODE + W_NODE, cy), (X_POD, cy)], OK if idx < 2 else MUTED, "ok" if idx < 2 else "ar", 1.4)
    d.t((X_NS + W_NS + X_POOL) / 2, cy - 10, a1, 13, MUTED, KR, "middle")
    d.t((X_POOL + W_POOL + X_NODE) / 2, cy - 10, a2, 13, ACC if idx == 0 else MUTED, KR, "middle")
    d.t((X_NODE + W_NODE + X_POD) / 2, cy - 10, "Pod IP", 12, MUTED, KR, "middle")

d.legend(H - 52, [("풀 선언·선택", INFO), ("노드 풀 배정(핵심)", ACC), ("Pod 주소", OK), ("기본 풀 폴백", MUTED)])
d.save("04-01.multi-pool-flow.svg")
