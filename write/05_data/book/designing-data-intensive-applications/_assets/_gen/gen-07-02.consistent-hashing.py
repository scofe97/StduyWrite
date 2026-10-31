# 07-02 §5 일관 해싱 — 노드 추가 때 기존 노드의 범위 일부만 새 노드로 넘어가는 모습 (Cassandra·ScyllaDB 방식).
# 사실 출처: 07-02 본문 §5(L78 두 성질, L86 Cassandra·ScyllaDB 가 원래 정의에 가까움),
#            DDIA 2판 7장 p.15 Figure 7-6 (해시 범위 0~1024, 노드마다 범위 3개, 구간 경계는 그림 그대로),
#            p.15 본문 "node 1 transfers parts of two of its ranges to node 3, and node 2 transfers part of one".
# 이전 판의 원형 링·시계 방향 배정·k1~k3·"K / N" 은 본문과 원서 어디에도 없어 걷어냈다.
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
X0, X1 = 60, 820
SCALE = (X1 - X0) / 1024
BAR_H = 40
A_Y = 190
B_Y = 330
SUM_Y = 448
LEG = SUM_Y + 92
H = LEG + 56

d = D(W, H, "07-02 · §5 FLOWCHART", "노드 추가 때 일부 범위만 새 노드로",
      "Node 3 이 추가되면 Node 1 의 범위 두 개와 Node 2 의 범위 한 개에서 일부만 떼어 Node 3 에 넘기고, 나머지 범위의 배정은 그대로 둔다.",
      "해시 범위 0 ~ 1024 · 노드마다 범위 3개 · Node 3 추가 전과 후")

# 상단 안내 배너 (본문 L78 둘째 성질)
d.box(28, BANNER_Y, W - 56, BANNER_H, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BANNER_Y + 22, "샤드 수가 바뀔 때 최소한의 키만 다른 샤드로 이동", 12, INK, KR, "middle", 600)

def xv(v):
    return X0 + v * SCALE

def bar(y, segs):
    for a, b, node, moved in segs:
        x, w = xv(a), (b - a) * SCALE
        if moved:
            d.tone(x, y, w, BAR_H, ACC, 0, "30", 1.2)
            d.t(x + w / 2, y + 25, node, 11, ACC, MONO, "middle", 600)
        else:
            d.box(x, y, w, BAR_H, PAPER2, RULE, 0.9, 0)
            d.t(x + w / 2, y + 25, node, 11, SOFT, MONO, "middle")

def ticks(y, vals):
    # 가까운 경계(60·88, 672·702 등)가 겹치지 않도록 두 줄에 번갈아 적는다
    for i, v in enumerate(vals):
        row = i % 2
        d.line(xv(v), y + BAR_H, xv(v), y + BAR_H + 6 + row * 16, RULE, 0.8)
        d.t(xv(v), y + BAR_H + 18 + row * 16, f"{v}", 11, MUTED, MONO, "middle")

# ── A: Node 3 추가 전 (Figure 7-6 위쪽) ──
d.t(X0, A_Y - 12, "Node 3 추가 전", 12, INK, KR, "start", 600)
segs_a = [(0, 88, "n1", False), (88, 128, "n0", False), (128, 309, "n2", False),
          (309, 398, "n0", False), (398, 511, "n2", False), (511, 672, "n1", False),
          (672, 702, "n2", False), (702, 930, "n1", False), (930, 1024, "n0", False)]
bar(A_Y, segs_a)
ticks(A_Y, [0, 88, 128, 309, 398, 511, 672, 702, 930, 1024])

# ── B: Node 3 추가 후 (Figure 7-6 아래쪽) ──
d.t(X0, B_Y - 12, "Node 3 추가 후", 12, ACC, KR, "start", 600)
segs_b = [(0, 60, "n1", False), (60, 88, "n3", True), (88, 128, "n0", False),
          (128, 276, "n2", False), (276, 309, "n3", True), (309, 398, "n0", False),
          (398, 511, "n2", False), (511, 551, "n1", False), (551, 672, "n3", True),
          (672, 702, "n2", False), (702, 930, "n1", False), (930, 1024, "n0", False)]
bar(B_Y, segs_b)
ticks(B_Y, [0, 60, 88, 128, 276, 309, 398, 511, 551, 672, 702, 930, 1024])

# ── 넘겨준 범위 요약 ──
d.box(X0, SUM_Y, X1 - X0, 72, PAPER2, RULE, 0.9)
d.t(X0 + 20, SUM_Y + 28, "Node 1 → Node 3", 12, ACC, MONO, "start", 600)
d.t(X0 + 200, SUM_Y + 28, "60 ~ 88 · 551 ~ 672", 12, INK, MONO, "start")
d.t(X0 + 420, SUM_Y + 28, "범위 두 개에서 일부", 12, SOFT, KR, "start")
d.t(X0 + 20, SUM_Y + 54, "Node 2 → Node 3", 12, ACC, MONO, "start", 600)
d.t(X0 + 200, SUM_Y + 54, "276 ~ 309", 12, INK, MONO, "start")
d.t(X0 + 420, SUM_Y + 54, "범위 한 개에서 일부 · Node 0 은 그대로", 12, SOFT, KR, "start")

d.legend(LEG, [("Node 3 이 넘겨받은 범위", ACC), ("배정이 그대로인 범위", MUTED)])
d.save("07-02.consistent-hashing.svg")
