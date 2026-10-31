# 07-03 §2 — ZooKeeper/etcd 조율 서비스를 이용한 권위 있는 샤드 매핑 관리 및 라우팅 티어의 토폴로지 구독 갱신 구조.
# 사실 출처: 07-03 본문 §2(L39~L52)
# 원서 대목: Ch.7 PDF p.20 ZooKeeper 설명, Figure 7-8 (PDF p.21) — Get "Danube", 키 범위·shard·node·IP 표 12행(앞 6행만 옮김)
#   노드별 샤드 목록(0·3·6·9 등)은 표 12행에서 노드별로 모은 값
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
LEG = 456
H = LEG + 56

d = D(W, H, "07-03 · SECTION 2", "ZooKeeper를 이용한 샤드 매핑 조율",
      "각 노드가 자신을 조율 서비스에 등록하고, ZooKeeper가 권위 있는 샤드→노드 매핑을 유지하며, 라우팅 티어가 이를 구독해 클라이언트 요청을 올바른 노드로 포워드한다.",
      "노드 등록 · 합의 기반 권위 매핑 · 매핑 구독 · 특정 키 라우팅")

# ── 좌측 컬럼: 요청 처리 경로 및 노드 클러스터 ──────────────────────────────
# 클라이언트
tier_x = 36
tier_w = 310
client_x, client_y = 83, 116
d.box(client_x, client_y, 216, 46, PAPER, RULE, 0.8)
d.t(client_x + 108, client_y + 19, "클라이언트 (Client)", 12, INK, KR, "middle", 600)
d.t(client_x + 108, client_y + 36, '특정 키 읽기', 11.5, MUTED, KR, "middle")

# 클라이언트 -> 라우팅 티어 요청 화살표
tier_y = 198
tier_h = 60
d.arrow([(client_x + 108, client_y + 46), (client_x + 108, tier_y)], MUTED, "ar")
d.t(client_x + 116, tier_y - 18, 'Get "Danube"', 11, MUTED, MONO, "start")

# 라우팅 티어
d.box(tier_x, tier_y, tier_w, tier_h, PAPER2, RULE, 1.0)
d.t(tier_x + tier_w / 2, tier_y + 22, "라우팅 티어 (Routing Tier)", 13, INK, KR, "middle", 600)
d.t(tier_x + tier_w / 2, tier_y + 44, '"Danube" → shard 2 · node 2', 11.5, ACC, MONO, "middle")

# 데이터 노드 클러스터
ny = 326
nh = 72
node_w = 92
nodes = [
    (tier_x, "Node 0", "10.20.30.100", "shard 0·3·6·9", False),
    (tier_x + 109, "Node 1", "10.20.30.101", "shard 1·4·7·10", False),
    (tier_x + 218, "Node 2", "10.20.30.102", "shard 2·5·8·11", True),
]

for bx, n_name, ip, shards, is_focal in nodes:
    cx = bx + node_w / 2
    if is_focal:
        d.tone(bx, ny, node_w, nh, ACC, 6, "22", 1.4)
        d.t(cx, ny + 20, n_name, 12, INK, MONO, "middle", 600)
        d.t(cx, ny + 38, ip, 11, ACC, MONO, "middle")
        d.t(cx, ny + 56, shards, 10.5, ACC, MONO, "middle")
    else:
        d.box(bx, ny, node_w, nh, PAPER, RULE, 0.8)
        d.t(cx, ny + 20, n_name, 12, INK, MONO, "middle", 600)
        d.t(cx, ny + 38, ip, 11, SOFT, MONO, "middle")
        d.t(cx, ny + 56, shards, 10.5, MUTED, MONO, "middle")

# 라우팅 티어 -> Node 2 포워드 화살표 (화살표 좌측에 라벨)
n2_cx = tier_x + 218 + node_w / 2
d.arrow([(n2_cx, tier_y + tier_h), (n2_cx, ny)], ACC, "acc")
d.t(n2_cx - 8, (tier_y + tier_h + ny) / 2 + 4, '포워드 (shard 2)', 11.5, ACC, KR, "end")

# ── 우측 컬럼: 조율 서비스 및 권위 매핑 테이블 ────────────────────────────
zk_x = 448
zk_w = 408
zk_y = 116
zk_h = 56

# ZooKeeper 조율 서비스 상자
d.tone(zk_x, zk_y, zk_w, zk_h, INFO, 6, "1A", 1.2)
d.chip(zk_x + 36, zk_y + 28, "조율", INFO, 11)
d.t(zk_x + 220, zk_y + 24, "ZooKeeper · etcd (합의 기반 조율)", 13, INK, KR, "middle", 600)
d.t(zk_x + 220, zk_y + 43, "합의 알고리즘으로 권위 매핑 유지 · split-brain 방지", 11.5, INFO, KR, "middle")

# 권위 매핑 테이블 상자
tbl_y = 188
tbl_h = 222
d.box(zk_x, tbl_y, zk_w, tbl_h, PAPER2, RULE, 0.9)

# 테이블 헤더
d.t(zk_x + 20, tbl_y + 22, "키 범위 (Key range)", 11.5, SOFT, KR, "start", 600)
d.t(zk_x + 194, tbl_y + 22, "샤드", 11.5, SOFT, KR, "middle", 600)
d.t(zk_x + 264, tbl_y + 22, "담당 노드", 11.5, SOFT, KR, "middle", 600)
d.t(zk_x + 352, tbl_y + 22, "IP 주소", 11.5, SOFT, KR, "middle", 600)
d.line(zk_x + 12, tbl_y + 32, zk_x + zk_w - 12, tbl_y + 32, RULE, 0.8)

# 테이블 데이터 행 (DDIA Figure 7-8 실측치)
rows = [
    ("A-ak — Bayes", "shard 0", "node 0", "10.20.30.100", False),
    ("Bayeu — Ceanothus", "shard 1", "node 1", "10.20.30.101", False),
    ("Ceara — Deluc", "shard 2", "node 2", "10.20.30.102", True),
    ("Delusion — Frenssen", "shard 3", "node 0", "10.20.30.100", False),
    ("Freon — Holderlin", "shard 4", "node 1", "10.20.30.101", False),
    ("Holderness — Krasnoje", "shard 5", "node 2", "10.20.30.102", False),
]

row_y0 = tbl_y + 54
stride = 25

for r_idx, (krange, sh, nd, ip, is_hit) in enumerate(rows):
    ry = row_y0 + r_idx * stride
    if is_hit:
        # Danube 포함 행 강조 (Focal)
        d.tone(zk_x + 8, ry - 14, zk_w - 16, 22, ACC, 4, "26", 1.2)
        d.t(zk_x + 20, ry, krange, 11, ACC, MONO, "start", 600)
        d.t(zk_x + 194, ry, sh, 11, ACC, MONO, "middle", 600)
        d.t(zk_x + 264, ry, nd, 11, ACC, MONO, "middle", 600)
        d.t(zk_x + 352, ry, ip, 11, ACC, MONO, "middle", 600)
    else:
        d.t(zk_x + 20, ry, krange, 11, MUTED, MONO, "start")
        d.t(zk_x + 194, ry, sh, 11, MUTED, MONO, "middle")
        d.t(zk_x + 264, ry, nd, 11, MUTED, MONO, "middle")
        d.t(zk_x + 352, ry, ip, 11, SOFT, MONO, "middle")

# 하단 요약 안내
d.t(zk_x + zk_w / 2, tbl_y + tbl_h - 12, "shard 6~11 행 생략 · Danube 는 Ceara—Deluc 범위", 11, SOFT, KR, "middle")

# ── 컴포넌트 간 상호작용 화살표 (직각) ──────────────────────────────────
# 1. 노드 클러스터 -> ZooKeeper (등록 및 상태 통지)
mid_x = (tier_x + tier_w + zk_x) / 2  # (346 + 448) / 2 = 397
# 원서 Fig 7-8 처럼 세 노드 모두 ZooKeeper 에 이어지도록 노드 아래 버스로 모은다
bus_y = ny + nh + 16
for bx, *_ in nodes[1:]:
    d.line(bx + node_w / 2, ny + nh, bx + node_w / 2, bus_y, INFO, 1.2, "4 4")
n0_cx = nodes[0][0] + node_w / 2
d.arrow([(n0_cx, ny + nh), (n0_cx, bus_y), (mid_x + 16, bus_y), (mid_x + 16, zk_y + 38), (zk_x, zk_y + 38)], INFO, "info", dash="4 4")
d.t((tier_x + tier_w + mid_x + 16) / 2, bus_y - 6, "노드 등록", 11.5, INFO, KR, "middle")

# 2. ZooKeeper -> 라우팅 티어 (토폴로지 변경 통지 / 구독)
d.arrow([(zk_x, zk_y + 18), (mid_x - 16, zk_y + 18), (mid_x - 16, tier_y + 24), (tier_x + tier_w, tier_y + 24)], INFO, "info", dash="4 4")
d.t((zk_x + mid_x - 16) / 2, zk_y + 12, "매핑 구독", 11.5, INFO, KR, "middle")

# ── 범례 ──────────────────────────────────────────────────────────────
d.legend(LEG, [("목표 키 샤드 매핑", ACC), ("조율 서비스 · 등록·구독", INFO), ("요청 전달 경로", MUTED)])
d.save("07-03.zookeeper-routing.svg")
