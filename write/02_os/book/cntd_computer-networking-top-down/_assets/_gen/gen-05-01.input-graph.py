# 타입 스펙: type-architecture — 노드 여섯과 간선 열 개의 구성요소·연결 지도.
#   축약: 무방향 가중 그래프라 화살촉이 없고, 간선 라벨은 비용 숫자 칩이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2 Figure 5.3
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, KR, MONO

# gen-05-01.path-costs.py 와 같은 간선 집합 — 두 도식이 같은 그래프를 그린다
E = {('u', 'v'): 2, ('u', 'x'): 1, ('u', 'w'): 5, ('v', 'x'): 2, ('v', 'w'): 3,
     ('x', 'w'): 3, ('x', 'y'): 1, ('w', 'y'): 1, ('w', 'z'): 5, ('y', 'z'): 2}
adj = {}
for (a, b), c in E.items():
    adj.setdefault(a, {})[b] = c
    adj.setdefault(b, {})[a] = c

paths = []


def walk(cur, seen, trail, cost):
    if cur == 'z':
        paths.append(("-".join(trail), cost))
        return
    for n, c in adj[cur].items():
        if n not in seen:
            walk(n, seen | {n}, trail + [n], cost + c)


walk('u', {'u'}, ['u'], 0)
paths.sort(key=lambda p: p[1])
assert len(paths) == 17, len(paths)
assert paths[0] == ("u-x-y-z", 4), paths[0]
assert paths[1][1] == 7, paths[1]

W, H = 920, 640
d = D(W, H, "SECTION 5.2 · FIGURE 5.3",
      "5장이 내내 쓰는 입력 그래프",
      "노드 여섯(u v w x y z)과 간선 열 개, 그리고 각 간선의 비용. 다익스트라와 벨만-포드가 모두 이 그래프 하나를 입력으로 받는다.",
      "간선 열 개와 그 위의 비용 — 이 그림이 §2 부터 §5 까지의 입력입니다")

NW, NH = 120, 56
POS = {'u': (80, 320), 'v': (292, 200), 'w': (504, 200),
       'x': (292, 440), 'y': (504, 440), 'z': (716, 320)}
SUB = {'u': "출발", 'z': "도착"}

# 직각 꺾임만 쓴다 — type-architecture 는 사선 연결선을 금지한다
EDGES = [
    ('u', 'v', "M 200 332 L 316 332 L 316 256"),
    ('u', 'x', "M 200 364 L 332 364 L 332 440"),
    ('u', 'w', "M 140 320 L 140 160 L 564 160 L 564 200"),
    ('v', 'x', "M 352 256 L 352 440"),
    ('v', 'w', "M 412 220 L 504 220"),
    ('x', 'w', "M 412 452 L 460 452 L 460 244 L 504 244"),
    ('x', 'y', "M 412 476 L 504 476"),
    ('w', 'y', "M 564 256 L 564 440"),
    ('w', 'z', "M 624 228 L 776 228 L 776 320"),
    ('y', 'z', "M 624 468 L 776 468 L 776 376"),
]
assert {frozenset(e[:2]) for e in EDGES} == {frozenset(k) for k in E}

# 최소 비용 경로 u-x-y-z 가 이 도식의 focal
HOT = {frozenset(('u', 'x')), frozenset(('x', 'y')), frozenset(('y', 'z'))}

for a, b, path in EDGES:
    hot = frozenset((a, b)) in HOT
    d.path(path, ACC if hot else MUTED, 1.6 if hot else 1.1)

# 비용 칩은 연결선 옆에 둔다 — 선 위에 얹으면 꺾임이 가려진다
CHIP = {('u', 'v'): (268, 316), ('u', 'x'): (268, 382), ('u', 'w'): (352, 146),
        ('v', 'x'): (376, 348), ('v', 'w'): (458, 204), ('x', 'w'): (436, 348),
        ('x', 'y'): (458, 494), ('w', 'y'): (588, 348), ('w', 'z'): (700, 212),
        ('y', 'z'): (700, 484)}
for key, (cx, cy) in CHIP.items():
    hot = frozenset(key) in HOT
    d.chip(cx, cy, E[key], ACC if hot else SOFT, 13, 7)

for k, (x, y) in POS.items():
    end = k in SUB
    d.box(x, y, NW, NH, PAPER2, INFO if end else RULE, 1.4 if end else 1.0, 7)
    d.t(x + NW / 2, y + (26 if end else 36), k, 20, INFO if end else INK, MONO, "middle", 600)
    if end:
        d.t(x + NW / 2, y + 45, SUB[k], 13, MUTED, KR)

d.t(12, 524, "간선은 열 개이고 그 위의 숫자가 비용입니다. 다익스트라도 벨만-포드도 "
             "이 그래프 하나를 입력으로 받습니다.", 13, MUTED, KR, "start")
d.t(12, 546, f"u 에서 z 로 가는 단순 경로는 {len(paths)} 개, 그중 최소는 "
             f"{paths[0][0]} 의 {paths[0][1]} 하나뿐이고 차순위는 {paths[1][1]} 입니다.",
     13, MUTED, KR, "start")

d.legend(576, [("최소 비용 경로 u-x-y-z", ACC), ("나머지 간선", MUTED), ("출발과 도착", INFO)])
d.t(W - 12, 620, "KUROSE-ROSS 9E FIG 5.3", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.input-graph.svg"
d.save(out)
print(f"경로 {len(paths)}개 · 최소 {paths[0]} · 차순위 {paths[1]} → {out}")
