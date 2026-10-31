# 07-02 §3 고정 샤드 수 — 다중 샤드 클러스터의 새 노드 추가 시 샤드 단위 이전 메커니즘.
# 사실 출처: 07-02 본문 §3(L50~L52), DDIA 2판 7장 p.12 Figure 7-4 (노드·샤드 배치 s0~s19 와 이전 샤드 s4·s9·s14·s19 는 그림 그대로) "Adding a new node to a database cluster with multiple shards per node"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
TOP_Y = 170
TOP_H = 92
BOT_Y = 348
BOT_H = 92
LEG = BOT_Y + BOT_H + 28
H = LEG + 56

d = D(W, H, "07-02 · §3 ARCHITECTURE", "고정 샤드 수 방식의 노드 추가와 샤드 이전",
      "클러스터에 새 노드가 추가될 때 키-샤드 매핑은 유지한 채 기존 노드에서 샤드 일부만 새 노드로 통째로 이전한다.",
      "노드 4개 클러스터(20개 샤드) · 노드 4 추가 시 노드당 1개 샤드 이전 · 키 매핑 불변")

# 상단 원칙 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "원칙: 키-샤드 매핑(hash(key)%20)은 고정하고, 샤드-노드 매핑만 변경해 샤드를 통째로 이전", 12, INK, KR, "middle", 600)

# Section A: 재배치 전 4개 노드
d.t(28, TOP_Y - 14, "재배치 전: 4개 노드 클러스터 (노드당 5개 샤드 할당 · 총 20개 샤드)", 13, INK, KR, "start", 600)

X0_TOP = 28
CW_TOP = 196
GAP_TOP = 16

top_nodes_data = [
    ("Node 0", ["s0", "s4", "s8", "s12", "s16"], "s4"),
    ("Node 1", ["s1", "s5", "s9", "s13", "s17"], "s9"),
    ("Node 2", ["s2", "s6", "s10", "s14", "s18"], "s14"),
    ("Node 3", ["s3", "s7", "s11", "s15", "s19"], "s19"),
]

top_mig_coords = {}

for i, (name, shards, mig_shard) in enumerate(top_nodes_data):
    nx = X0_TOP + i * (CW_TOP + GAP_TOP)
    d.box(nx, TOP_Y, CW_TOP, TOP_H, PAPER2, RULE, 0.9)
    d.chip(nx + CW_TOP / 2, TOP_Y + 18, name, MUTED, 12)
    d.line(nx + 10, TOP_Y + 30, nx + CW_TOP - 10, TOP_Y + 30, RULE, 0.8)

    for s_idx, s_name in enumerate(shards):
        sx = nx + 14 + s_idx * 34
        sy = TOP_Y + 42
        if s_name == mig_shard:
            d.tone(sx, sy, 30, 36, ACC, 4, "20", 1.2)
            d.t(sx + 15, sy + 22, s_name, 12, ACC, MONO, "middle", 600)
            top_mig_coords[s_name] = (sx + 15, TOP_Y + TOP_H)
        else:
            d.box(sx, sy, 30, 36, PAPER, RULE, 0.8)
            d.t(sx + 15, sy + 22, s_name, 12, MUTED, MONO, "middle")

# Section B: 재배치 후 5개 노드
d.t(28, BOT_Y - 14, "재배치 후: 5개 노드 클러스터 (노드당 4개 샤드 균등 분산) — Node 4 신규 추가", 13, INK, KR, "start", 600)

X0_BOT = 28
CW_BOT = 154
GAP_BOT = 16

bot_nodes_data = [
    ("Node 0", ["s0", "s8", "s12", "s16"], False),
    ("Node 1", ["s1", "s5", "s13", "s17"], False),
    ("Node 2", ["s2", "s6", "s10", "s18"], False),
    ("Node 3", ["s3", "s7", "s11", "s15"], False),
    ("Node 4", ["s4", "s9", "s14", "s19"], True),
]

bot_mig_coords = {}

for i, (name, shards, is_new) in enumerate(bot_nodes_data):
    nx = X0_BOT + i * (CW_BOT + GAP_BOT)
    if is_new:
        d.box(nx, BOT_Y, CW_BOT, BOT_H, PAPER2, ACC, 1.4)
        d.chip(nx + CW_BOT / 2, BOT_Y + 18, name + " (신규)", INFO, 12)
    else:
        d.box(nx, BOT_Y, CW_BOT, BOT_H, PAPER2, RULE, 0.9)
        d.chip(nx + CW_BOT / 2, BOT_Y + 18, name, MUTED, 12)

    d.line(nx + 10, BOT_Y + 30, nx + CW_BOT - 10, BOT_Y + 30, RULE, 0.8)

    for s_idx, s_name in enumerate(shards):
        sx = nx + 14 + s_idx * 32
        sy = BOT_Y + 42
        if is_new:
            d.tone(sx, sy, 28, 36, ACC, 4, "20", 1.2)
            d.t(sx + 14, sy + 22, s_name, 12, ACC, MONO, "middle", 600)
            bot_mig_coords[s_name] = (sx + 14, BOT_Y)
        else:
            d.tone(sx, sy, 28, 36, OK, 4, "16", 1.0)
            d.t(sx + 14, sy + 22, s_name, 12, OK, MONO, "middle")

# 이전 화살표 (s4, s9, s14, s19) — 직교 라우팅
mig_levels = {"s4": 276, "s9": 290, "s14": 304, "s19": 318}
for s_name in ["s4", "s9", "s14", "s19"]:
    x1, y1 = top_mig_coords[s_name]
    x2, y2 = bot_mig_coords[s_name]
    y_mid = mig_levels[s_name]
    if abs(x1 - x2) < 14:  # 위아래 칸이 겹치면 꺾지 않고 곧게 내린다
        d.arrow([(x2, y1 + 2), (x2, y2 - 2)], ACC, "acc", 1.4)
    else:
        d.arrow([(x1, y1 + 2), (x1, y_mid), (x2, y_mid), (x2, y2 - 2)], ACC, "acc", 1.4)

d.legend(LEG, [("이전 샤드", ACC), ("유지 샤드", OK), ("신규 노드 4", INFO), ("기존 노드", MUTED)])
d.save("07-02.fixed-shards.svg")
