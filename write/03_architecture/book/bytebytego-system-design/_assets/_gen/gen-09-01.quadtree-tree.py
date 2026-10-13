# 타입 스펙: type-tree — 루트에서 아래로 갈라지는 쿼드트리. 위 세 층(루트·네 사분면·한 사분면의 네 하위)과 아래 깊은 가지(340 → 잎 셋과 140 → 잎 둘)를 두 패널로 나눠 한 장이 네 층을 넘지 않게 한다. 초점은 100 을 막 넘어 갈라지는 140.
# 사실 출처: PDF 143쪽 그림(Building a quadtree: 루트 200m 아래 NW 40m·NE 30m·SW 70m·SE 60m, 30m 아래 NW 12m·NE 4m·SW 5m·SE 9m, 4m 아래 여러 층 생략 뒤 340 노드 아래 50·90·60·140, 140 아래 60·80, 원 노드 = 안쪽 노드·네모 = 잎, m = 백만)과
#   추출본 v1.txt 3527행(루트가 한 노드의 사업장이 100 곳을 넘지 않을 때까지 재귀적으로 넷으로 갈라짐, 200 million businesses).
# Layout conventions: 노드 폭 120·높이 40 한 가지 크기, 가로 stride 144, 층 stride 76, 직각 연결(부모 수직 → 가로 버스 → 자식 수직). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 648
d = D(W, H, "BYTEBYTEGO · 09-01 §4",
      "사업장이 100 곳을 넘으면 넷으로 갈라 100 이하가 될 때까지 내려간다",
      "루트 2억 곳이 네 사분면으로 갈리고 340 곳짜리 노드는 잎 셋과 140 곳 노드로, 140 곳은 다시 60 곳과 80 곳 잎으로 갈립니다.",
      "숫자는 노드가 담은 사업장 수이고 M 은 백만입니다")

NW, NH, SX, SY = 120, 40, 144, 76


def fam(s):
    return KR if any("가" <= ch <= "힣" for ch in s) else MONO


def children_xs(cx, n):
    return [cx - (n - 1) * SX / 2 + SX * k for k in range(n)]


def connect(px, py, xs, cy):
    bus = py + NH + 18
    d.line(px, py + NH, px, bus, MUTED, 1)
    d.line(min(xs), bus, max(xs), bus, MUTED, 1)
    for x in xs:
        d.line(x, bus, x, cy, MUTED, 1)


def node(cx, y, label, kind="int"):
    x = cx - NW / 2
    if kind == "focal":
        d.tone(x, y, NW, NH, ACC, 6, "14", 1.4); col = ACC
    elif kind == "leaf":
        d.tone(x, y, NW, NH, OK, 2, "10", 0.8); col = INK
    else:
        d.tone(x, y, NW, NH, INFO, 6, "14", 1.2); col = INK
    d.t(cx, y + 25, label, 13, col, fam(label), "middle", 600)


# 패널 A — 맨 위 세 층.
d.t(12, 104, "맨 위 세 층", 13, INK, KR, "start", 600)
YA = [112, 188, 264]
rootA = 480
t2 = children_xs(rootA, 4)
t2l = ["NW 40M", "NE 30M", "SW 70M", "SE 60M"]
t3 = children_xs(t2[1], 4)
t3l = ["NW 12M", "NE 4M", "SW 5M", "SE 9M"]
connect(rootA, YA[0], t2, YA[1])
connect(t2[1], YA[1], t3, YA[2])
node(rootA, YA[0], "200M")
for x, l in zip(t2, t2l):
    node(x, YA[1], l)
for x, l in zip(t3, t3l):
    node(x, YA[2], l)

# 가운데 — 중간 층 생략.
cxB = t3[1]
d.line(cxB, YA[2] + NH, cxB, 372, MUTED, 1, "4 3")
d.chip(cxB, 338, "중간 층 생략", MUTED, 11)

# 패널 B — 깊은 가지.
d.t(12, 360, "4M 노드 아래 깊은 곳", 13, INK, KR, "start", 600)
YB = [372, 448, 524]
b2 = children_xs(cxB, 4)
b2l = [("50", "leaf"), ("90", "leaf"), ("60", "leaf"), ("140", "focal")]
b3 = children_xs(b2[3], 2)
connect(cxB, YB[0], b2, YB[1])
connect(b2[3], YB[1], b3, YB[2])
node(cxB, YB[0], "340")
for x, (l, k) in zip(b2, b2l):
    node(x, YB[1], l, k)
for x, l in zip(b3, ["60", "80"]):
    node(x, YB[2], l, "leaf")

d.legend(H - 48, [("100 초과 · 더 갈라짐", INFO), ("100 이하 · 잎", OK), ("갈라지는 경계", ACC)])
d.save("09-01.quadtree-tree.svg")
