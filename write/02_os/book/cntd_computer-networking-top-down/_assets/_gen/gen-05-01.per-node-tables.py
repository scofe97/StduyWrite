# 타입 스펙: type-architecture — 같은 지도를 받아도 출발점이 달라 라우터마다 다른 전달 표가 남는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.1 — Figure 5.3 에 노드별로 다익스트라를 돌려 직접 계산
import sys, pathlib, heapq
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

E = {('u','v'):2, ('u','x'):1, ('u','w'):5, ('v','x'):2, ('v','w'):3,
     ('x','w'):3, ('x','y'):1, ('w','y'):1, ('w','z'):5, ('y','z'):2}
adj = {}
for (a,b),c in E.items():
    adj.setdefault(a,{})[b]=c; adj.setdefault(b,{})[a]=c

def table(src):
    """src 를 출발점으로 다익스트라를 돌려 목적지별 첫 홉을 낸다."""
    Dd={n:float('inf') for n in adj}; Dd[src]=0; P={}; pq=[(0,src)]; done=set()
    while pq:
        dist,n=heapq.heappop(pq)
        if n in done: continue
        done.add(n)
        for m,c in adj[n].items():
            if dist+c<Dd[m]: Dd[m]=dist+c; P[m]=n; heapq.heappush(pq,(dist+c,m))
    out={}
    for dst in sorted(adj):
        if dst==src: continue
        cur=dst
        while P[cur]!=src: cur=P[cur]
        out[dst]=(cur, Dd[dst])
    return out

W, H = 1000, 700
d = D(W, H, "SECTION 5.2.1 · ONE MAP, MANY TABLES",
      "지도는 같고 표는 저마다 다릅니다",
      "같은 링크 상태 지도를 받은 라우터들이 각자 자기를 출발점으로 다익스트라를 돌려 서로 다른 전달 표를 만드는 모습. u·x·y 세 라우터의 표를 나란히 놓았다.",
      "링크 상태에서 중앙인 것은 정보이지 계산이 아닙니다 — 다익스트라는 라우터 수만큼 돕니다")

# ── 왼쪽: 모두가 받는 지도 하나
d.box(20, 124, 320, 400, f"{INK}05", RULE, 1.0, 10)
d.t(180, 112, "모두가 받는 같은 지도", 11, INK, KR, "middle", 600)
POS = {'u':(180,186), 'v':(72,262), 'x':(288,262), 'y':(288,348), 'w':(150,428), 'z':(282,452)}
COLOR = {'u':ACC, 'x':INFO, 'y':OK}
for (a,b),c in E.items():
    (x1,y1),(x2,y2) = POS[a], POS[b]
    d.line(x1,y1,x2,y2,RULE,1.0)
    d.t((x1+x2)/2, (y1+y2)/2 - 8, str(c), 11, SOFT, MONO)
for k,(x,y) in POS.items():
    c = COLOR.get(k, RULE)
    d.box(x-19, y-15, 38, 30, PAPER2, c, 1.3 if k in COLOR else 1.0, 6)
    d.t(x, y+5, k, 12, COLOR.get(k, INK), MONO, "middle", 600)
d.t(180, 500, "간선 열 개와 비용이 전부 같습니다", 11, MUTED, KR)

# ── 오른쪽: 노드마다 다른 전달 표
XS = [(366, 'u'), (576, 'x'), (786, 'y')]
for x0, src in XS:
    c = COLOR[src]
    rows = table(src)
    d.box(x0, 124, 194, 400, f"{INK}05", RULE, 1.0, 10)
    d.tone(x0+12, 140, 170, 30, c, 6, "12", 1.2)
    d.t(x0+97, 160, f"{src} 의 전달 표", 11, c, KR, "middle", 600)
    d.t(x0+40, 196, "목적지", 11, MUTED, KR)
    d.t(x0+134, 196, "내보낼 링크", 11, MUTED, KR)
    d.line(x0+12, 206, x0+182, 206, RULE, 0.8)
    for i,(dst,(hop,cost)) in enumerate(rows.items()):
        y = 232 + i*44
        d.t(x0+40, y, dst, 12, INK, MONO)
        d.t(x0+134, y, f"({src}, {hop})", 12, c, MONO)
        d.t(x0+134, y+17, f"비용 {cost}", 11, SOFT, MONO)
    d.line(x0+12, 462, x0+182, 462, RULE, 0.8)
    hops = {h for h,_ in rows.values()}
    d.t(x0+97, 484, f"나가는 링크 {len(hops)} 종류", 11, MUTED, KR)

d.t(20, 556, "u 는 다섯 목적지 중 넷을 x 로 내보내고, x 는 셋을 y 로 내보내며, y 는 목적지마다 다른 이웃으로 내보냅니다.", 11, MUTED, KR, "start")
d.t(20, 578, "같은 지도에 같은 알고리즘이라 최소 비용 경로 집합은 모두 같지만, 출발점이 다르므로 남는 트리와 표는 노드마다 다릅니다.", 11, MUTED, KR, "start")
d.t(20, 600, "어느 라우터도 경로 전체를 들고 있지 않습니다. 첫 홉만 알고, 그다음은 그 이웃의 표가 이어받습니다.", 11, INFO, KR, "start")

d.legend(634, [("u 의 표", ACC), ("x 의 표", INFO), ("y 의 표", OK)])
d.t(976, 676, "KUROSE-ROSS 9E FIG 5.3", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.per-node-tables.svg"
d.save(out)
print("→", out)
