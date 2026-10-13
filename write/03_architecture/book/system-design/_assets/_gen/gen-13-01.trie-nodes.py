# 타입 스펙: type-tree — 접두사 트리. 부모가 아래로 짧은 수직선을 내리고 수평 버스가 형제를 잇고 자식마다 수직 드롭이 윗변에 닿는다(직각 연결선). focal 은 tr 으로 내려가는 길.
# 사실 출처: 추출본 v2.txt 3655~3662행(트라이 정의 · 질의 여섯)
#   PDF 207쪽 표 13-2(tree 10 · try 29 · true 35 · toy 14 · wish 25 · win 50)와 그림 · 3681~3687행(tr 입력, k=2 → true 35 · try 29, 208쪽).
# Layout conventions: 노드 폭 120·높이 44, 깊이 stride 80(y=104·184·264·344·424), 버스 y = 부모 윗변 + 60. 형제 x stride 144. 모든 좌표 4의 배수. 연결선은 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, SOFT, PAPER2, RULE, KR, MONO

W, H = 960, 660
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §3",
      "트라이는 글자 하나를 노드 하나에 두고 질의가 끝나는 노드에 빈도를 둔다",
      "tr 을 치면 tr 노드 아래에서 질의 셋 tree 10 · try 29 · true 35 가 나오고 그중 위쪽 둘이 제안이 된다.",
      "예시 질의 여섯 · 접두사 tr · k = 2")

NW, NH = 120, 44
Y = (104, 184, 264, 344, 424)

# 이름 → (x, 깊이, 부모, 빈도)
N = {
    "root": (522, 0, None, None),
    "t": (324, 1, "root", None), "w": (720, 1, "root", None),
    "tr": (168, 2, "t", None), "to": (480, 2, "t", None), "wi": (720, 2, "w", None),
    "tre": (24, 3, "tr", None), "tru": (168, 3, "tr", None), "try": (312, 3, "tr", 29),
    "toy": (480, 3, "to", 14), "wis": (648, 3, "wi", None), "win": (792, 3, "wi", 50),
    "tree": (24, 4, "tre", 10), "true": (168, 4, "tru", 35), "wish": (648, 4, "wis", 25),
}
FOCAL_PATH = ("root", "t", "tr")
HIT = ("tree", "try", "true")


def cx(n):
    return N[n][0] + NW // 2


def top(n):
    return Y[N[n][1]]


kids = {}
for n, (_, _, p, _) in N.items():
    if p:
        kids.setdefault(p, []).append(n)

for p, cs in kids.items():
    py = top(p) + NH
    bus = py + 16
    d.path(f"M {cx(p)} {py} L {cx(p)} {bus}", MUTED, 1.2)
    xs = [cx(c) for c in cs] + [cx(p)]
    d.path(f"M {min(xs)} {bus} L {max(xs)} {bus}", MUTED, 1.2)
    for c in cs:
        d.path(f"M {cx(c)} {bus} L {cx(c)} {top(c)}", MUTED, 1.2)

# 초점 경로 덧그리기
for a, b in (("root", "t"), ("t", "tr")):
    py = top(a) + NH
    bus = py + 16
    d.path(f"M {cx(a)} {py} L {cx(a)} {bus} L {cx(b)} {bus} L {cx(b)} {top(b)}", ACC, 1.8)

for n, (x, dep, p, f) in N.items():
    y = Y[dep]
    if n in FOCAL_PATH:
        d.tone(x, y, NW, NH, ACC, 6, "12", 1.4)
    elif n in HIT:
        d.tone(x, y, NW, NH, OK, 6, "14", 1.2)
    elif f is not None:
        d.tone(x, y, NW, NH, INFO, 6, "14", 1.4)
    else:
        d.tone(x, y, NW, NH, MUTED, 6, "10", 1.0)
    label = n if f is None else f"{n} · {f}"
    d.t(x + NW / 2, y + 27, label, 14, INK, MONO, "middle", 600 if f is not None else 400)

# 결과 상자
d.box(312, 416, 300, 68, PAPER2, RULE, 1.0, 6)
d.t(328, 440, "tr 의 후보", 13, SOFT, KR, "start", 600)
d.t(328, 466, "tree 10 · try 29 · true 35", 13, MUTED, MONO, "start")
d.box(312, 500, 300, 68, PAPER2, ACC, 1.4, 6)
d.t(328, 524, "상위 2", 13, SOFT, KR, "start", 600)
d.t(328, 550, "true 35 · try 29", 14, INK, MONO, "start", 600)

d.legend(H - 56, [("지나가는 접두사", MUTED), ("질의가 끝나는 노드", INFO), ("접두사 tr 아래 후보", OK), ("접두사까지 내려가는 길", ACC)])
d.save("13-01.trie-nodes.svg")
