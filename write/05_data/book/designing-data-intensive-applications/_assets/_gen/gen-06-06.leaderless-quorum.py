# 06-06 §2 — w + r > n 쿼럼 조건과 읽기·쓰기 노드 중첩 구조 및 엣지 케이스.
# 사실 출처: 06-06 본문 §2(L42~L52), DDIA 2판 Ch 6 Figure 6-13 (PDF p.44) — n=5, w=3, r=3 에서 중첩 노드 최신 보장, 과반수 절충, 4대 엣지 케이스(복원·리밸런싱·동시읽쓰·LWW).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 524
H = LEG + 56

d = D(W, H, "06-06 §2 · QUORUM OVERLAP & CONSISTENCY", "w + r > n 쿼럼 조건과 읽기·쓰기 노드 중첩",
      "쓰기 노드 집합과 읽기 노드 집합이 최소 한 노드에서 겹쳐 최신 쓰기 값을 읽게 되는 구조를 보인다.",
      "n = 5 · 쓰기 쿼럼 w = 3 · 읽기 쿼럼 r = 3 · 노드 중첩 · 엣지 케이스")

# 1. 5개 레플리카 노드 배치 (n=5, w=3, r=3)
NODE_W = 144
NODE_H = 68
NODE_Y = 176
GAP = 16
X0 = 48

nodes = [
    ("노드 1", "v2 최신 보유", OK, False),
    ("노드 2", "v2 최신 보유", OK, False),
    ("노드 3 (중첩)", "v2 최신 (중첩 노드)", ACC, True),
    ("노드 4", "v1 이전 사본", INFO, False),
    ("노드 5", "v1 이전 사본", INFO, False),
]

# 2. 쓰기 쿼럼 영역 (w=3: 노드 1, 2, 3)
ZW_X = X0 - 8
ZW_W = NODE_W * 3 + GAP * 2 + 16
d.box(ZW_X, 108, ZW_W, 52, PAPER2, OK, 1.0, r=4)
d.t(ZW_X + ZW_W / 2, 130, "쓰기 쿼럼 집합 (w = 3)", 13, OK, KR, "middle", 600)
d.t(ZW_X + ZW_W / 2, 148, "클라이언트 병렬 쓰기 수락 (v2 최신 값)", 11, MUTED, KR, "middle")

# 쓰기 화살표 (수직)
for i in range(3):
    nx = X0 + i * (NODE_W + GAP) + NODE_W / 2
    d.arrow([(nx, 160), (nx, NODE_Y)], OK, "ok", 1.4)

# 3. 레플리카 노드 상자 렌더
for i, (title, sub, col, is_focal) in enumerate(nodes):
    x = X0 + i * (NODE_W + GAP)
    if is_focal:
        d.tone(x, NODE_Y, NODE_W, NODE_H, ACC, 6, "22", 1.4)
        d.t(x + NODE_W / 2, NODE_Y + 28, title, 13, ACC, KR, "middle", 600)
        d.t(x + NODE_W / 2, NODE_Y + 50, sub, 11, INK, KR, "middle")
    else:
        d.box(x, NODE_Y, NODE_W, NODE_H, PAPER2, col, 1.0, r=6)
        d.t(x + NODE_W / 2, NODE_Y + 28, title, 13, INK, KR, "middle", 600)
        d.t(x + NODE_W / 2, NODE_Y + 50, sub, 11, MUTED, KR, "middle")

# 4. 읽기 쿼럼 영역 (r=3: 노드 3, 4, 5)
ZR_X = X0 + 2 * (NODE_W + GAP) - 8
ZR_W = NODE_W * 3 + GAP * 2 + 16
d.box(ZR_X, 260, ZR_W, 52, PAPER2, INFO, 1.0, r=4)
d.t(ZR_X + ZR_W / 2, 282, "읽기 쿼럼 집합 (r = 3)", 13, INFO, KR, "middle", 600)
d.t(ZR_X + ZR_W / 2, 300, "읽는 노드 중 노드 3이 최신 값(v2) 보유", 11, MUTED, KR, "middle")

# 읽기 화살표 (수직)
for i in range(2, 5):
    nx = X0 + i * (NODE_W + GAP) + NODE_W / 2
    d.arrow([(nx, NODE_Y + NODE_H), (nx, 260)], INFO, "info", 1.4)

# 5. 하단 2개 설명 카드 (절충 & 엣지 케이스)
CARD_Y = 336
CARD_H = 164
CARD_W = 396

# 카드 1: 쿼럼 조건과 절충
d.box(36, CARD_Y, CARD_W, CARD_H, PAPER2, RULE, 1.0, r=6)
d.t(36 + CARD_W / 2, CARD_Y + 26, "쿼럼 조건 (w + r > n) 절충", 13, INK, KR, "middle", 600)
d.line(48, CARD_Y + 38, 36 + CARD_W - 12, CARD_Y + 38, RULE, 0.8)

c1_items = [
    ("과반수 쿼럼 (w, r > n/2)", "읽기·쓰기 집합 중첩 · n/2 노드 장애까지 견딤"),
    ("완화 쿼럼 (w + r ≤ n)", "stale 읽기 확률 증가 · 지연 감소 및 가용성 향상"),
    ("stale 제어 손잡이", "절대 보장이 아닌 stale 확률을 조절하는 매개변수"),
]
for j, (t1, t2) in enumerate(c1_items):
    iy = CARD_Y + 52 + j * 36
    d.t(52, iy + 10, "•", 12, OK, KR, "start", 600)
    d.t(66, iy + 10, t1, 12, INK, KR, "start", 600)
    d.t(66, iy + 26, t2, 11, MUTED, KR, "start")

# 카드 2: 4대 엣지 케이스
d.box(448, CARD_Y, CARD_W, CARD_H, PAPER2, WARN, 1.0, r=6)
d.t(448 + CARD_W / 2, CARD_Y + 26, "일관성이 깨지는 4대 엣지 케이스", 13, WARN, KR, "middle", 600)
d.line(460, CARD_Y + 38, 448 + CARD_W - 12, CARD_Y + 38, RULE, 0.8)

c2_items = [
    ("구버전 복원", "새 값 노드 장애 후 이전 사본 복구로 w 미달"),
    ("리밸런싱 불일치", "rebalancing 중 레플리카 견해 엇갈려 중첩 깨짐"),
    ("동시 읽기·쓰기", "쓰기 진행 도중 읽기 실행 시 새 값 반영 불확정"),
    ("시계 기반 LWW", "노드 시계 오차로 최신 쓰기가 조용히 덮어써짐"),
]
for j, (t1, t2) in enumerate(c2_items):
    iy = CARD_Y + 46 + j * 28
    d.t(464, iy + 10, "•", 11, WARN, KR, "start", 600)
    d.t(478, iy + 10, t1, 11, INK, KR, "start", 600)
    d.t(564, iy + 10, t2, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("중첩 노드 (focal)", ACC),
    ("쓰기 집합 · v2 보유", OK),
    ("읽기 집합 · v1 사본", INFO),
    ("엣지 케이스 주의", WARN),
])
d.save("06-06.leaderless-quorum.svg")
