# 02-01.netfilter-hooks-flow — 훅마다 바뀌는 필드 (DNAT 가 라우팅보다 먼저인 이유)
# 본문 요구: 어느 훅에서 어느 필드가 바뀌는지 · 라우팅 이전에는 목적지를, 이후에는 출발지만
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 단계마다 같은 필드를 세로로 맞춰
#           '무엇이 바뀌었나'가 칸 색으로 드러나게 한다. 두 구간은 type-nested 의 경계 띠.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 616
d = D(W, H, "NETFILTER HOOKS · WHICH FIELD CHANGES",
      "훅마다 패킷의 어느 필드가 바뀌는가 — DNAT 가 라우팅보다 먼저인 이유",
      "라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다. 같은 필드를 세로로 맞춰 보면 어디서 바뀌는지 드러난다.",
      lead="라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다")

BW, BH, GAP = 132, 92, 16
GUTTER = 80                                                      # src·dst 행 라벨 자리 (띠 밖)
CX = [100 + BW // 2 + i * (BW + GAP) for i in range(6)]          # 166 314 462 610 758 906
NODE_CY, SRC_Y, DST_Y, CELL_H = 250, 362, 420, 44
NODES = [("요청 도착", "밖에서 들어왔다"), ("PRE_ROUTING", "nat 에서 DNAT"),
         ("라우팅 판단", "바뀐 dst 로 조회"), ("FORWARD", "filter 판정"),
         ("POST_ROUTING", "nat 에서 MASQUERADE"), ("패킷이 떠남", "노드를 나간다")]
SRC = ["203.0.113.9:51000"] * 4 + ["노드 IP:51000"] * 2
DST = ["10.96.192.224:8080"] + ["10.244.1.66:8080"] * 5
CHANGED = {("dst", 1), ("src", 4)}                               # 그 칸에서 바뀐다

ddx.band(d, 104, 568, "라우팅이 가운데 서 있어서 앞뒤로 바꿀 수 있는 필드가 갈린다")
BTOP = 186
for x0, x1, lab, c in [(92, 394, "라우팅 이전 — 목적지를 바꿀 수 있다", ACC),
                       (530, 986, "라우팅 이후 — 출발지만 바뀐다", INFO)]:
    d.o.append(f'<rect x="{x0}" y="{BTOP}" width="{x1-x0}" height="{DST_Y+CELL_H//2+40-BTOP}" rx="8" '
               f'fill="{c}08" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x0, BTOP, lab, 11, c, off=16)

for cx, (l, s) in zip(CX, NODES):
    d.box(cx - BW // 2, NODE_CY - BH // 2, BW, BH, PAPER2, RULE, 1.1, 6)
    d.t(cx, NODE_CY - 12, ddx.fit(l, 12, BW - 14, l), 12, INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, NODE_CY + 12, ddx.fit(s, 10, BW - 12, s), 10, MUTED, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+5} {NODE_CY} L {b-BW//2-7} {NODE_CY}", MUTED, 1.4, m="ar")

d.t(GUTTER, SRC_Y + 4, "src", 11, SOFT, MONO, "end")
d.t(GUTTER, DST_Y + 4, "dst", 11, SOFT, MONO, "end")
for i, cx in enumerate(CX):
    for key, y, vals in (("src", SRC_Y, SRC), ("dst", DST_Y, DST)):
        hit = (key, i) in CHANGED
        c = ACC if hit else RULE
        d.o.append(f'<rect x="{cx-BW//2}" y="{y-CELL_H//2}" width="{BW}" height="{CELL_H}" rx="5" '
                   f'fill="{ACC+"14" if hit else PAPER}" stroke="{c}" stroke-width="{1.4 if hit else 1.0}"/>')
        d.t(cx, y + 4, ddx.fit(vals[i], 10, BW - 12, f"{key}{i}"), 10,
            ACC if hit else MUTED, MONO)
        # src 는 위, dst 는 아래에 붙인다 — 두 행이 붙어 있어 같은 쪽에 두면 겹친다
        if hit: d.t(cx, y - CELL_H // 2 - 8 if key == "src" else y + CELL_H // 2 + 16,
                    "여기서 바뀐다", 10, ACC, KR)

d.t(36, 528, "목적지를 바꾸려면 라우팅 판단 전에 끝나야 한다 — DNAT 가 PRE_ROUTING 에 있는 이유가 이것이고, "
             "출발지 위장은 나가기 직전이면 된다", 12, MUTED, KR, "start")
d.legend(584, [("바뀌는 자리", ACC), ("라우팅 이후", INFO)])
d.save("02-01.netfilter-hooks-flow.svg")
print("ok netfilter-hooks-flow")
