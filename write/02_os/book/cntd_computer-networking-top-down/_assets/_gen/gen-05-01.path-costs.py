# 타입 스펙: type-bar — u 에서 z 로 가는 단순 경로 17개의 비용을 크기순으로 세운다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2 Figure 5.3 의 간선 비용에서 전수 열거
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

# Figure 5.3 의 간선 — 표 5.1 의 각 칸에서 역산하고 원문 그림으로 대조
E = {('u', 'v'): 2, ('u', 'x'): 1, ('u', 'w'): 5, ('v', 'x'): 2, ('v', 'w'): 3,
     ('x', 'w'): 3, ('x', 'y'): 1, ('w', 'y'): 1, ('w', 'z'): 5, ('y', 'z'): 2}
adj = {}
for (a, b), c in E.items():
    adj.setdefault(a, {})[b] = c
    adj.setdefault(b, {})[a] = c

paths = []


def walk(cur, seen, trail, cost):
    if cur == 'z':
        paths.append(("".join(trail), cost))
        return
    for n, c in adj[cur].items():
        if n not in seen:
            walk(n, seen | {n}, trail + [n], cost + c)


walk('u', {'u'}, ['u'], 0)
paths.sort(key=lambda p: p[1])
assert len(paths) == 17, len(paths)

W, H = 1000, 580
d = D(W, H, "SECTION 5.2 · LEAST-COST PATH",
      "경로는 열일곱, 최소는 하나입니다",
      "Figure 5.3 에서 u 로부터 z 까지 가는 단순 경로 17개를 전부 열거해 비용순으로 세운 막대. 눈으로 훑어 고른 경로가 최소일 확률이 얼마나 낮은지 보여준다.",
      "원문이 \"17개를 다 확인했습니까?\"라고 묻는 그 17개를 직접 세었습니다")

X0, BASE, GAP, BW = 66, 452, 14, 38
MAXC = max(c for _, c in paths)
PX = 268 / MAXC

for i, (name, cost) in enumerate(paths):
    x = X0 + i * (BW + GAP)
    h = cost * PX
    hot = i == 0
    c = ACC if hot else MUTED
    d.box(x, BASE - h, BW, h, f"{c}{'2E' if hot else '18'}", c, 1.4 if hot else 0.9, 4)
    d.t(x + BW / 2, BASE - h - 10, str(cost), 11, c, MONO, "middle", 600)
    d.t(x + BW / 2, BASE + 18, name, 9, ACC if hot else SOFT, MONO)

d.line(X0 - 14, BASE, X0 + 17 * (BW + GAP) - GAP + 8, BASE, RULE, 1.0)
d.t(X0 - 22, BASE + 4, "0", 10, SOFT, MONO, "end")
d.t(X0 - 22, BASE - 268 + 4, str(MAXC), 10, SOFT, MONO, "end")
d.t(30, 120, "경로 비용", 11, MUTED, KR, "start")

# 최소와 차순위 사이의 간격
d.line(X0 + BW + 4, BASE - 4 * PX, X0 + 2 * (BW + GAP) - 6, BASE - 4 * PX, ACC, 1.0, "4 4")
# 주석은 막대 위 빈 자리에 — 막대 높이 안에 두면 3~5번 막대를 덮는다
d.t(X0, 252, "최소 4 와 차순위 7 사이가 3 만큼 벌어집니다", 11, ACC, KR, "start")

d.t(30, 502, "최소 비용 경로는 u-x-y-z 하나뿐이고 비용 4 입니다. 두 번째로 싼 경로는 7 이라 "
             "우연히 맞힐 여지가 넓지 않습니다. 라우팅 알고리즘이 푸는 문제가 바로 이 열거입니다.",
     11, MUTED, KR, "start")

d.legend(524, [("최소 비용 경로", ACC), ("나머지 16개", MUTED)])
d.t(960, 566, "KUROSE-ROSS 9E FIG 5.3 · ENUMERATED", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.path-costs.svg"
d.save(out)
print(f"경로 {len(paths)}개 · 최소 {paths[0]} · 최대 {paths[-1]} →", out)
