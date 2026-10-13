# 타입 스펙: type-tree — 들여쓰기 트리(파일 트리 변형). 왼쪽 열은 노드와 질의 빈도, 오른쪽 열은 그 노드가 캐시한 상위 5 개. 연결선은 수직선과 수평 틱이다. focal 은 be 노드.
# 사실 출처: 추출본 v2.txt 3699~3708행(노드마다 상위 k 캐시 · be 노드 목록 [best 35, bet 29, bee 20, be 15, beer 10]) · PDF 210쪽 그림(best 35 · bet 29 · bee 20 · be 15 · beer 10 · buy 14 와 노드별 목록).
#   leaf 노드(beer·best·bet·buy)의 목록은 그림에 점선 상자가 없으나 질의 자신 하나만 든다(같은 데이터의 키-값 표에서 beer → [beer 10], best → [best 35]).
#   b 노드 목록은 그림 그대로 [best 35, bet 29, bee 20, be 15, buy 14] 이고 beer 10 은 여섯째라 빠진다(k = 5).
# Layout conventions: 행 stride 44(y=124 부터 9 행), 들여쓰기 stride 36, 목록 열 x=464. 모든 좌표 4의 배수. 연결선은 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, BAD, MUTED, INK, SOFT, KR, MONO

W, H = 960, 612
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 13-01 §4",
      "노드마다 상위 5 개를 들고 있으면 접두사 노드에서 바로 읽는다",
      "b 노드는 아래 질의 여섯 개 중 위쪽 다섯 개만 캐시하고, 질의 하나뿐인 leaf 는 자기 하나를 캐시한다.",
      "예시 질의 · best 35 · bet 29 · bee 20 · be 15 · buy 14 · beer 10 · k = 5")

# (이름, 깊이, 질의 빈도, 캐시 목록)
ROWS = (
    ("b", 0, None, ("best 35", "bet 29", "bee 20", "be 15", "buy 14")),
    ("be", 1, 15, ("best 35", "bet 29", "bee 20", "be 15", "beer 10")),
    ("bee", 2, 20, ("bee 20", "beer 10")),
    ("beer", 3, 10, ("beer 10",)),
    ("bes", 2, None, ("best 35",)),
    ("best", 3, 35, ("best 35",)),
    ("bet", 2, 29, ("bet 29",)),
    ("bu", 1, None, ("buy 14",)),
    ("buy", 2, 14, ("buy 14",)),
)
NW, NH, ST, Y0, IND = 120, 32, 44, 124, 36
LX = 464

d.t(24, 108, "노드 · 질의 빈도", 13, SOFT, KR, "start", 600)
d.t(LX, 108, "캐시한 상위 5", 13, SOFT, KR, "start", 600)

ypos = [Y0 + i * ST for i in range(len(ROWS))]

# 연결선: 부모 노드 아래에서 자식 줄까지 세로선을 내리고 수평 틱으로 자식에 닿는다
parent_stack = []
for i, (n, dep, f, lst) in enumerate(ROWS):
    parent_stack = parent_stack[:dep]
    if dep > 0:
        p = parent_stack[dep - 1]
        px = 24 + (dep - 1) * IND + 12
        yy = ypos[i] + NH // 2
        # 세로선은 부모 노드 아래에서 이 줄까지 이어진다
        d.path(f"M {px} {ypos[p] + NH} L {px} {yy} L {24 + dep * IND - 4} {yy}", MUTED, 1.2)
    parent_stack.append(i)

for i, (n, dep, f, lst) in enumerate(ROWS):
    x, y = 24 + dep * IND, ypos[i]
    focal = n == "be"
    c = ACC if focal else INFO
    d.tone(x, y, NW, NH, c, 6, "12" if focal else "10", 1.4 if focal else 1.0)
    label = n if f is None else f"{n} · {f}"
    d.t(x + NW / 2, y + 21, label, 13, INK, MONO, "middle", 600)
    # 캐시 목록: 칩 나열
    cx = LX
    for it in lst:
        w = len(it) * 7.8 + 16
        d.tone(cx, y + 2, w, 28, INFO, 4, "12", 1.0)
        d.t(cx + w / 2, y + 21, it, 12, INK, MONO, "middle")
        cx += w + 8

# b 의 목록에서 밀려난 질의
bx = LX + sum(len(it) * 7.8 + 16 + 8 for it in ROWS[0][3]) + 12
d.t(bx, ypos[0] + 21, "beer 10 탈락", 13, BAD, KR, "start")

d.legend(H - 56, [("노드와 캐시", INFO), ("be 노드", ACC), ("밀려나는 질의", BAD)])
d.save("13-01.top-k-cache.svg")
