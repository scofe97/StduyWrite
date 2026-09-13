# 타입 스펙: type-data-flow — 자기 링크만 알던 노드들이 링크 상태 패킷을 퍼뜨려 같은 지도에 이른다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.1 링크 상태 브로드캐스트
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

E = {('u','v'):2, ('u','x'):1, ('u','w'):5, ('v','x'):2, ('v','w'):3,
     ('x','w'):3, ('x','y'):1, ('w','y'):1, ('w','z'):5, ('y','z'):2}
REL = {'u':(150,52), 'v':(46,122), 'x':(256,122), 'y':(256,200), 'w':(112,262), 'z':(236,292)}

W, H = 1000, 660
d = D(W, H, "SECTION 5.2.1 · LINK STATE BROADCAST",
      "자기 링크만 알던 노드가 지도를 갖게 됩니다",
      "각 노드가 자기에게 붙은 링크의 비용만 아는 상태에서 시작해 링크 상태 패킷을 망 전체에 퍼뜨리고, 그 결과 모두가 똑같고 완전한 지도를 갖게 되는 세 단계.",
      "u 한 대의 패킷만 따라 그렸습니다 — 나머지 다섯도 똑같이 자기 패킷을 뿌립니다")

PANELS = [
    (20,  "1. u 가 아는 것은 자기 링크 셋뿐", "나머지 일곱 간선은 u 에게 아직 없습니다"),
    (350, "2. u 의 패킷이 몇 홉째에 닿는가", "받은 노드가 다시 이웃에게 넘깁니다"),
    (680, "3. 여섯이 다 뿌리면 지도가 완성", "간선 열 개가 모두에게 모입니다"),
]
for px, title, cap in PANELS:
    d.box(px, 138, 300, 366, f"{INK}05", RULE, 1.0, 10)
    d.t(px + 150, 126, title, 11, INK, KR, "middle", 600)
    d.t(px + 150, 522, cap, 11, MUTED, KR)

def node(px, k, c, fill=PAPER2):
    x, y = REL[k]
    d.box(px + x - 19, 150 + y - 15, 38, 30, fill, c, 1.3 if c != RULE else 1.0, 6)
    d.t(px + x, 150 + y + 5, k, 12, INK if c == RULE else c, MONO, "middle", 600)

def edge(px, a, b, c, sw=1.0, dash=None, cost=False):
    (x1, y1), (x2, y2) = REL[a], REL[b]
    d.line(px + x1, 150 + y1, px + x2, 150 + y2, c, sw, dash)
    if cost:
        d.t(px + (x1 + x2) / 2, 150 + (y1 + y2) / 2 - 8, str(E[(a, b)]), 11, SOFT, MONO)

# ── 패널 1 — u 의 시야
P = 20
for (a, b) in E:
    own = 'u' in (a, b)
    edge(P, a, b, ACC if own else RULE, 1.6 if own else 0.8, None if own else "3 5", cost=own)
for k in REL:
    node(P, k, ACC if k == 'u' else RULE)
d.t(P + 150, 472, "주황은 u 가 광고할 링크 셋입니다", 11, SOFT, KR)

# ── 패널 2 — 퍼뜨리는 중
P = 350
for (a, b) in E:
    edge(P, a, b, RULE, 0.8, "3 5")
for a, b in (('u','v'), ('u','x'), ('u','w')):
    edge(P, a, b, ACC, 1.7)
for a, b in (('x','y'), ('v','w'), ('w','z'), ('y','z')):
    edge(P, a, b, INFO, 1.4)
for k in REL:
    node(P, k, ACC if k in ('u','v','x','w') else INFO)
d.t(P + 150, 462, "1 홉 — 이웃 v·x·w 가 받습니다", 11, ACC, KR)
d.t(P + 150, 482, "2 홉 — 그들이 넘겨 y·z 까지 갑니다", 11, INFO, KR)

# ── 패널 3 — 완성된 지도
P = 680
for (a, b) in E:
    edge(P, a, b, OK, 1.4, cost=True)
for k in REL:
    node(P, k, OK)
d.t(P + 150, 472, "u·v·x·y·w·z 의 광고를 합친 결과입니다", 11, SOFT, KR)

d.t(20, 556, "가운데 칸의 파란 링크는 u 의 패킷이 2 홉째에 지나가는 길이지 그 링크의 비용이 알려졌다는 뜻이 아닙니다. 링크 비용은 그 링크에 붙은 노드가 자기 차례에 광고합니다.", 11, MUTED, KR, "start")
d.t(20, 578, "퍼뜨리기가 끝나면 모두가 같은 입력을 갖습니다. 같은 알고리즘을 돌리므로 최소 비용 경로 집합도 같지만, 출발점이 달라 표는 저마다 다릅니다.", 11, MUTED, KR, "start")

d.legend(612, [("u 가 광고하는 자기 링크", ACC), ("u 의 패킷이 2 홉째에 지나는 링크", INFO), ("여섯이 다 뿌린 뒤의 지도", OK)])
out = pathlib.Path(__file__).resolve().parent.parent / "05-01.ls-broadcast.svg"
d.save(out)
print("→", out)
