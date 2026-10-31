# 07-02 §2 mod N 방식의 문제 — 노드 수 변경(3개→4개)에 따른 hash(key)%N 불필요한 대규모 키 이동.
# 사실 출처: 07-02 본문 §2(L38~L40), DDIA 2판 7장 p.11 Figure 7-3 (키 0~23 배치는 그림 그대로).
# 파생 수 검산: k%3==k%4 인 키는 k mod 12 ∈ {0,1,2} → 0·1·2·12·13·14 의 6개 유지, 18개(75%) 이동 "Assigning keys to nodes by hashing the key and taking it modulo the number of nodes"
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
TOP_Y = 172
BOT_Y = 336
PH = 110
LEG = BOT_Y + PH + 28
H = LEG + 56

d = D(W, H, "07-02 · §2 DATA FLOW", "mod N 방식의 노드 수 변경과 키 대이동",
      "노드 수가 3개에서 4개로 증가할 때 hash(key) % N 결과가 바뀌어 전체 키의 75%가 다른 노드로 불필요하게 이동한다.",
      "노드 3개(hash % 3) vs 노드 4개(hash % 4) · 24개 키 중 18개 키(75%) 재배치 발생")

# 상단 안내 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, ACC, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "문제: 노드가 3개에서 4개로 1개 늘면 전체 키의 75%(18/24)가 다른 노드로 대이동", 12, INK, KR, "middle", 600)

# Section A: 재배치 전 3개 노드
d.t(28, TOP_Y - 14, "재배치 전: 3개 노드 클러스터 (hash(key) % 3)", 13, INK, KR, "start", 600)

top_nodes = [
    ("Node 0", "hash % 3 = 0", [[0, 3, 6, 9], [12, 15, 18, 21]]),
    ("Node 1", "hash % 3 = 1", [[1, 4, 7, 10], [13, 16, 19, 22]]),
    ("Node 2", "hash % 3 = 2", [[2, 5, 8, 11], [14, 17, 20, 23]]),
]

X0_TOP = 28
CW_TOP = 264
GAP_TOP = 16

for i, (name, expr, rows) in enumerate(top_nodes):
    nx = X0_TOP + i * (CW_TOP + GAP_TOP)
    d.box(nx, TOP_Y, CW_TOP, PH, PAPER2, RULE, 0.9)
    d.chip(nx + 46, TOP_Y + 18, name, MUTED, 12)
    d.t(nx + 150, TOP_Y + 20, expr, 12, SOFT, MONO, "middle")
    d.line(nx + 10, TOP_Y + 32, nx + CW_TOP - 10, TOP_Y + 32, RULE, 0.8)

    for r_idx, r_keys in enumerate(rows):
        ry = TOP_Y + 42 + r_idx * 32
        for c_idx, k in enumerate(r_keys):
            kx = nx + 14 + c_idx * 60
            d.box(kx, ry, 52, 26, PAPER, RULE, 0.8)
            d.t(kx + 26, ry + 17, str(k), 12, INK, MONO, "middle", 600)

# 중앙 전환 안내선
d.arrow([(W / 2, TOP_Y + PH + 4), (W / 2, BOT_Y - 18)], ACC, "acc", 1.4)
d.chip(W / 2, TOP_Y + PH + 18, "Node 3 추가 (N = 3 → 4)", ACC, 12)

# Section B: 재배치 후 4개 노드
d.t(28, BOT_Y - 14, "재배치 후: 4개 노드 클러스터 (hash(key) % 4)", 13, INK, KR, "start", 600)

bot_nodes = [
    ("Node 0", "hash % 4 = 0", [[0, 4, 8], [12, 16, 20]], False),
    ("Node 1", "hash % 4 = 1", [[1, 5, 9], [13, 17, 21]], False),
    ("Node 2", "hash % 4 = 2", [[2, 6, 10], [14, 18, 22]], False),
    ("Node 3", "hash % 4 = 3", [[3, 7, 11], [15, 19, 23]], True),
]

# 유지되는 키 (재배치 전 노드 번호 == 재배치 후 노드 번호)
# Node 0: 0, 12
# Node 1: 1, 13
# Node 2: 2, 14
KEPT_KEYS = {0, 12, 1, 13, 2, 14}

X0_BOT = 28
CW_BOT = 196
GAP_BOT = 14

for i, (name, expr, rows, is_new) in enumerate(bot_nodes):
    nx = X0_BOT + i * (CW_BOT + GAP_BOT)
    if is_new:
        d.box(nx, BOT_Y, CW_BOT, PH, PAPER2, ACC, 1.4)
        d.chip(nx + 44, BOT_Y + 18, name, ACC, 12)
    else:
        d.box(nx, BOT_Y, CW_BOT, PH, PAPER2, RULE, 0.9)
        d.chip(nx + 44, BOT_Y + 18, name, MUTED, 12)

    d.t(nx + 126, BOT_Y + 20, expr, 11, SOFT, MONO, "middle")
    d.line(nx + 10, BOT_Y + 32, nx + CW_BOT - 10, BOT_Y + 32, RULE, 0.8)

    for r_idx, r_keys in enumerate(rows):
        ry = BOT_Y + 42 + r_idx * 32
        for c_idx, k in enumerate(r_keys):
            kx = nx + 12 + c_idx * 58
            if k in KEPT_KEYS:
                d.tone(kx, ry, 50, 26, OK, 4, "18", 1.0)
                d.t(kx + 25, ry + 17, str(k), 12, OK, MONO, "middle", 600)
            else:
                d.tone(kx, ry, 50, 26, BAD, 4, "18", 1.0)
                d.t(kx + 25, ry + 17, str(k), 12, BAD, MONO, "middle", 600)

d.legend(LEG, [("키 이동 (75%)", BAD), ("위치 유지 (25%)", OK), ("신규 노드 3", ACC), ("기존 노드", MUTED)])
d.save("07-02.mod-n-rebalancing.svg")
