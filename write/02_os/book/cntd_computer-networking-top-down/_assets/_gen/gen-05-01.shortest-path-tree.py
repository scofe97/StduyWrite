# 타입 스펙: type-tree — 다익스트라가 끝나면 남는 것은 전임 노드가 만든 트리 하나다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.1 Table 5.1 · Figure 5.4
import sys, pathlib, heapq
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

E = {('u', 'v'): 2, ('u', 'x'): 1, ('u', 'w'): 5, ('v', 'x'): 2, ('v', 'w'): 3,
     ('x', 'w'): 3, ('x', 'y'): 1, ('w', 'y'): 1, ('w', 'z'): 5, ('y', 'z'): 2}
adj = {}
for (a, b), c in E.items():
    adj.setdefault(a, {})[b] = c
    adj.setdefault(b, {})[a] = c

Dd = {n: float('inf') for n in adj}
Dd['u'] = 0
P, pq, done = {}, [(0, 'u')], set()
while pq:
    dist, n = heapq.heappop(pq)
    if n in done:
        continue
    done.add(n)
    for m, c in adj[n].items():
        if dist + c < Dd[m]:
            Dd[m] = dist + c
            P[m] = n
            heapq.heappush(pq, (dist + c, m))

W, H = 1000, 700
d = D(W, H, "SECTION 5.2.1 · DIJKSTRA RESULT",
      "남는 것은 전임 노드뿐입니다",
      "링크 상태 알고리즘이 끝난 뒤 u 에서 본 최소 비용 트리와 그로부터 만든 전달 표. 간선 열 개짜리 그래프가 가지 다섯 개 트리로 줄어든다.",
      "노드마다 전임 하나를 기억해 두면 경로 전체가 복원됩니다")

NW, NH = 120, 56
POS = {'u': (240, 130), 'v': (90, 250), 'x': (390, 250),
       'y': (390, 370), 'w': (270, 490), 'z': (510, 490)}


def node(key, focal=False):
    x, y = POS[key]
    c = ACC if focal else RULE
    d.box(x, y, NW, NH, PAPER2, c, 1.5 if focal else 1.0, 7)
    d.t(x + NW / 2, y + 24, key, 14, ACC if focal else INK, MONO, "middle", 600)
    lab = "출발" if key == 'u' else f"비용 {Dd[key]}"
    d.t(x + NW / 2, y + 42, lab, 11, MUTED, KR)


# 트리 간선 — 전임 노드 P 가 만든 것만
EDGES = [('u', 'v', "M 300 186 L 300 218 L 150 218 L 150 250"),
         ('u', 'x', "M 300 186 L 300 218 L 450 218 L 450 250"),
         ('x', 'y', "M 450 306 L 450 370"),
         ('y', 'w', "M 450 426 L 450 458 L 330 458 L 330 490"),
         ('y', 'z', "M 450 426 L 450 458 L 570 458 L 570 490")]
for a, b, path in EDGES:
    assert P[b] == a, (a, b, P[b])
    d.path(path, ACC, 1.6, m="acc")

# 비용 칩은 연결선 옆에 둔다 — 선 위에 얹으면 화살촉과 꺾임이 가려진다
for cx, cy, cost in ((124, 236, 2), (398, 236, 1), (472, 340, 1), (304, 474, 1), (596, 474, 2)):
    d.chip(cx, cy, cost, ACC, 11, 6)

for k in POS:
    node(k, k == 'u')

# 전달 표 — Figure 5.4 오른쪽
TX, TY, TW = 700, 150, 260
d.box(TX, TY, TW, 244, PAPER2, RULE, 1.0, 8)
d.t(TX + TW / 2, TY + 26, "u 의 전달 표", 12, INK, KR, "middle", 600)
d.line(TX + 16, TY + 40, TX + TW - 16, TY + 40, RULE, 0.9)
d.t(TX + 60, TY + 60, "목적지", 11, SOFT, KR)
d.t(TX + 178, TY + 60, "나가는 링크", 11, SOFT, KR)
row = TY + 88
for dst in "vxywz":
    hop = dst
    while P[hop] != 'u':
        hop = P[hop]
    hot = hop == 'x'
    d.t(TX + 60, row, dst, 12, INK, MONO)
    d.t(TX + 178, row, f"(u, {hop})", 12, ACC if hot else MUTED, MONO)
    row += 30

d.t(TX, 430, "다섯 목적지 중 넷이 같은 링크로 나갑니다", 11, ACC, KR, "start")

d.t(30, 596, "간선 열 개 중 다섯 개만 트리에 남습니다. u-w 직통 링크는 비용 5 라서 "
             "u-x-y-w 의 3 에 밀렸고, 그렇게 밀린 간선이 그림에서 사라진 다섯 개입니다.",
     11, MUTED, KR, "start")

d.legend(624, [("최소 비용 트리의 간선", ACC), ("노드", MUTED)])
d.t(960, 672, "KUROSE-ROSS 9E TABLE 5.1 · FIG 5.4", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.shortest-path-tree.svg"
d.save(out)
print("최소 비용:", {k: Dd[k] for k in 'vwxyz'}, "· 전임:", {k: P[k] for k in 'vwxyz'}, "→", out)
