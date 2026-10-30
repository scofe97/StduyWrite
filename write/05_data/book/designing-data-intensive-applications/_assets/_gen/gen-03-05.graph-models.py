# 03-05 §1·§4 — Lucy 의 출생지 사슬을 속성 그래프(정점·간선)와 트리플 스토어((주어, 술어, 목적어))로 병기한다.
# 옛 도식의 쿼리 언어 목록은 뺐다. §2~§6 본문이 맡는다. 노드 이름은 본문 Turtle 예의 값만 쓴다.
# 타입 스펙: type-dependency
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LEG = 488
H = LEG + 56

d = D(W, H, "03-05 · GRAPH MODELS", "같은 데이터의 두 그래프 모델",
      "Lucy 의 출생지 사슬을 속성 그래프는 정점과 간선으로, 트리플 스토어는 (주어, 술어, 목적어) 문장으로 표현한다.",
      "속성 그래프와 트리플 스토어의 대응")

XS = [32, 248, 464, 680]

# 속성 그래프
d.box(16, 100, 848, 140, PAPER, RULE, 0.9)
d.t(32, 124, "속성 그래프 — 정점과 간선", 14, INK, KR, "start", 600)
NODES = [("Lucy", "Person"), ("Idaho", "state"), ("United States", "country"), ("North America", "continent")]
for x, (a, b) in zip(XS, NODES):
    d.box(x, 156, 132, 56, PAPER2, INFO, 1.2)
    d.t(x + 66, 180, a, 13, INK, KR, "middle", 600)
    d.t(x + 66, 200, b, 12, MUTED, MONO)
for i, lab in enumerate(["bornIn", "within", "within"]):
    x = XS[i] + 132
    d.arrow([(x + 4, 184), (x + 80, 184)], ACC, "acc", 1.6)
    d.chip(x + 42, 166, lab, ACC, 11)

# 트리플 스토어
d.box(16, 256, 848, 200, PAPER, RULE, 1.0)
d.t(32, 280, "트리플 스토어 — (주어, 술어, 목적어)", 14, INK, KR, "start", 600)
for x, lab in zip(XS, ["주어 · 꼬리 정점", "술어 · 간선", "목적어 · 머리 정점"]):
    d.t(x, 312, lab, 12, MUTED, KR, "start")
ROWS = [("lucy", "bornIn", "idaho"), ("idaho", "within", "usa"), ("usa", "within", "namerica")]
for i, row in enumerate(ROWS):
    y = 324 + 44 * i
    for j, (x, cell) in enumerate(zip(XS, row)):
        d.box(x, y, 132, 32, PAPER2, ACC if j == 1 else INFO, 1.2 if j == 1 else 1.0)
        d.t(x + 66, y + 21, cell, 12, INK, MONO)

d.legend(LEG, [("술어 · 간선", ACC), ("정점", INFO)])
d.save("03-05.graph-models.svg")
