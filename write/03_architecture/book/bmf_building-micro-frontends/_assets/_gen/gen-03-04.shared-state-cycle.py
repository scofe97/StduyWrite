# 03-04 §3 — 공유 상태가 왜 안티패턴인가 (원문 Figure 3-13).
# 조각 셋이 같은 상태에 모이고(fan-in 3), 그 상태가 바뀔 때마다 팀에게 검증을 되돌려 요구한다(back-edge).
# 타입 스펙: type-dependency — 트리로 못 그리는 fan-in 과 되돌아오는 간선이 논지다. accent 는 back-edge 와 그 라벨 둘뿐.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
NW, NH = 190, 60
R0_Y, R1_Y = 124, 244
teams = [
    ("MFE A", "팀 부리토", 140, 1),
    ("MFE B", "팀 파히타", 405, 0),
    ("MFE C", "팀 타코", 670, 0),
]
SS_X, SS_W = 340, 320
LEGEND_Y = R1_Y + NH + 52
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04 §3",
      "공유 상태로 모이면 분산 모놀리스가 된다",
      "조각 셋이 같은 상태에 의존하고, 그 상태가 바뀔 때마다 검증 요구가 팀으로 되돌아온다. 되돌아오는 간선이 이 그림의 논지다.",
      "아래로 내려가는 화살표가 의존이고 색이 붙은 점선이 되돌아오는 요구입니다")

def node(x, y, w, name, sub, fanin, leaf=False):
    fill = f"{INK}05" if leaf else PAPER2
    stroke = MUTED if leaf else RULE
    d.box(x, y, w, NH, fill, stroke, 1.0, 6)
    d.t(x + 16, y + 26, name, 12.5, INK, KR, "start", 600)
    d.t(x + 16, y + 43, sub, 9, MUTED, MONO, "start")
    bw_ = 34
    d.o.append(f'<rect x="{x + w - bw_ - 10}" y="{y + 9}" width="{bw_}" height="15" rx="2" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(x + w - bw_ / 2 - 10, y + 20, f"{fanin} in", 8, SOFT, MONO)

for name, sub, x, fanin in teams:
    node(x, R0_Y, NW, name, sub, fanin)
node(SS_X, R1_Y, SS_W, "공유 상태", "shared state · 세 팀이 함께 설계하고 유지", 3)

# 의존 간선 — 공유 상태 윗변 부착점을 12px 이상 벌린다
for (name, sub, x, _), ax in zip(teams, (SS_X + 60, SS_X + SS_W / 2, SS_X + SS_W - 60)):
    cx = x + NW / 2
    if abs(cx - ax) < 2:
        d.arrow([(cx, R0_Y + NH), (ax, R1_Y)], MUTED, "ar", 1.4)
    else:
        my = (R0_Y + NH + R1_Y) / 2
        d.arrow([(cx, R0_Y + NH), (cx, my), (ax, my), (ax, R1_Y)], MUTED, "ar", 1.4)

# 되돌아오는 간선 — 노드 더미 바깥(왼쪽 x=64)으로 돌린다
d.arrow([(SS_X, R1_Y + NH / 2), (64, R1_Y + NH / 2), (64, R0_Y + NH / 2), (140, R0_Y + NH / 2)],
        ACC, "acc", 1.4, "5 4")
d.o.append(f'<rect x="38" y="{(R0_Y + R1_Y) / 2 + 12}" width="52" height="17" rx="2" fill="{PAPER}"/>')
d.t(64, (R0_Y + R1_Y) / 2 + 24, "CYCLE", 8, ACC, MONO)
d.t(500, R1_Y + NH + 30, "상태가 바뀌면 모든 팀이 자기 조각을 검증해야 하고, 그래서 함께 배포된다", 10.5, MUTED, KR)

d.legend(LEGEND_Y, [("되돌아오는 검증 요구", ACC), ("의존 방향", MUTED)])
d.save("03-04.shared-state-cycle.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
