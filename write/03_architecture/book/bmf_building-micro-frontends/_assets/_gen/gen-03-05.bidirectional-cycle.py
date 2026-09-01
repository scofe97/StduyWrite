# 03-05 §4 — 양방향 공유가 만드는 되돌아오는 간선. 저자가 "계층적 성질이 평탄해진다"고 적은 것을 그린다.
# 단방향으로 두면 이 accent 간선이 사라지고 그림은 평범한 트리가 된다.
# 타입 스펙: type-dependency — 트리로 못 그리는 fan-in 과 되돌아오는 간선이 논지다. accent 는 back-edge 와 그 라벨뿐.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
NW, NH = 200, 60
R0_Y, R1_Y = 124, 244
HOST_X = 400
remotes = [("리모트 A", "remote", 150, 1), ("리모트 B", "remote", 650, 0)]
LEGEND_Y = R1_Y + NH + 52
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-05 §4",
      "양방향으로 공유하면 계층이 평탄해진다",
      "아래로 내려가는 화살표가 호스트에서 리모트로 가는 정상 방향이다. 색이 붙은 점선이 저자가 권하지 않는 되돌아오는 공유다.",
      "이 점선을 지우면 그림은 그냥 트리가 됩니다")

def node(x, y, name, sub, fanin, leaf=False):
    d.box(x, y, NW, NH, f"{INK}05" if leaf else PAPER2, MUTED if leaf else RULE, 1.0, 6)
    d.t(x + 16, y + 26, name, 12.5, INK, KR, "start", 600)
    d.t(x + 16, y + 43, sub, 9, MUTED, MONO, "start")
    bw = 34
    d.o.append(f'<rect x="{x + NW - bw - 10}" y="{y + 9}" width="{bw}" height="15" rx="2" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + NW - bw / 2 - 10, y + 20, f"{fanin} in", 8, SOFT, MONO)

node(HOST_X, R0_Y, "호스트", "host · 조합 지점", 1)
for name, sub, x, fanin in remotes:
    node(x, R1_Y, name, sub, fanin)

# 정상 의존 — 호스트 아랫변 부착점을 벌린다
my = (R0_Y + NH + R1_Y) / 2
for x, ax in ((150, HOST_X + 60), (650, HOST_X + NW - 60)):
    d.arrow([(ax, R0_Y + NH), (ax, my), (x + NW / 2, my), (x + NW / 2, R1_Y)], MUTED, "ar", 1.4)

# 되돌아오는 간선 — 노드 더미 바깥(왼쪽 x=60)으로 돌린다
d.arrow([(150, R1_Y + NH / 2), (60, R1_Y + NH / 2), (60, R0_Y + NH / 2), (HOST_X, R0_Y + NH / 2)],
        ACC, "acc", 1.4, "5 4")
d.o.append(f'<rect x="34" y="{my + 12}" width="52" height="17" rx="2" fill="{PAPER}"/>')
d.t(60, my + 24, "CYCLE", 8, ACC, MONO)
d.t(500, R1_Y + NH + 30, "리모트가 호스트에 코드를 되돌려 주면 어느 쪽이 위인지 사라진다", 10.5, MUTED, KR)

d.legend(LEGEND_Y, [("저자가 권하지 않는 되돌아오는 공유", ACC), ("정상 의존 방향", MUTED)])
d.save("03-05.bidirectional-cycle.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
