# 02-01.netfilter-hooks-flow — 훅마다 바뀌는 필드 (DNAT 가 라우팅보다 먼저인 이유)
# 본문 요구: 어느 훅에서 어느 필드가 바뀌는지 · 라우팅 이전에는 목적지를, 이후에는 출발지만
# 장면: 클러스터 밖 → NodePort 30080. 외부에서 ClusterIP 로 직접 보내는 조합은 성립하지 않아
#      (ClusterIP 는 클러스터 밖에서 라우팅되지 않는다) 2026-08-28 NodePort 로 교정했다.
# 타입 스펙: type-dp-security-matrix.md 의 값 대조 행 — 단계마다 같은 필드를 세로로 맞춰
#           '무엇이 바뀌었나'가 칸 색으로 드러나게 한다. 두 구간은 type-nested 의 경계 띠.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 576
d = D(W, H, "NETFILTER HOOKS · WHICH FIELD CHANGES",
      "훅마다 패킷의 어느 필드가 바뀌는가 — DNAT 가 라우팅보다 먼저인 이유",
      "라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다. 같은 필드를 세로로 맞춰 보면 어디서 바뀌는지 드러난다.",
      lead="라우팅 이전에는 목적지를 바꿀 수 있고, 이후에는 출발지만 바뀐다")

BW, BH, GAP = 138, 92, 12   # 11px 라벨 수용
GUTTER = 72                                                      # src·dst 행 라벨 자리 (링 밖)
CX = [88 + BW // 2 + i * (BW + GAP) for i in range(6)]          # 157 307 457 607 757 907 — 마지막 카드 오른끝 976
NODE_CY, SRC_Y, DST_Y, CELL_H = 250, 362, 420, 44
NODES = [("요청 도착", "외부에서 도착"), ("PRE_ROUTING", "nat 에서 DNAT"),
         ("라우팅 판단", "바뀐 dst 로 조회"), ("FORWARD", "filter 판정"),
         ("POST_ROUTING", "nat 에서 MASQUERADE"), ("패킷이 떠남", "노드 밖으로")]
SRC = ["203.0.113.9:51000"] * 4 + ["노드 IP:51000"] * 2
DST = ["노드 IP:30080"] + ["10.244.1.66:8080"] * 5
CHANGED = {("dst", 1), ("src", 4)}                               # 그 칸에서 바뀐다

ddx.band(d, 104, 504, "라우팅 판단 기준 · 앞은 목적지, 뒤는 출발지", x=12, w=980)
# band 가 배경 사각을 칠하므로 이 줄은 반드시 band 뒤에 그린다
d.t(36, 156, "장면 · 클러스터 밖 클라이언트 → NodePort 30080 → DNAT 뒤 Pod IP · 이 노드는 중계", 12, SOFT, KR, "start")
BTOP = 186
# 링 경계는 카드 사이 12px 통로의 가운데를 지난다 — 카드 모서리(376|388, 526|538, 976)를 자르지 않게 한다.
# 링과 카드는 모두 띠(12~992) 안에 둔다. accent 는 '바뀌는 칸' 한 축에만 쓰므로 라우팅 이전 링은 warn 이다.
for x0, x1, lab, c in [(80, 382, "라우팅 이전 · 목적지 변경 가능", WARN),
                       (532, 984, "라우팅 이후 · 출발지만 변경", INFO)]:
    d.o.append(f'<rect x="{x0}" y="{BTOP}" width="{x1-x0}" height="{DST_Y+CELL_H//2+40-BTOP}" rx="8" '
               f'fill="{c}08" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, x0, BTOP, lab, 11, c, off=16)

for cx, (l, s) in zip(CX, NODES):
    d.box(cx - BW // 2, NODE_CY - BH // 2, BW, BH, PAPER2, RULE, 1.1, 6)
    d.t(cx, NODE_CY - 12, ddx.fit(l, 12, BW - 14, l), 12, INK,
        MONO if all(ord(ch) < 128 or ch == '_' for ch in l) else KR, "middle", 600)
    d.t(cx, NODE_CY + 12, ddx.fit(s, 11, BW - 12, s), 11, MUTED, KR)
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
        d.t(cx, y + 4, ddx.fit(vals[i], 11, BW - 12, f"{key}{i}"), 11,
            ACC if hit else MUTED, MONO)
        # src 는 위, dst 는 아래에 붙인다 — 두 행이 붙어 있어 같은 쪽에 두면 겹친다
        if hit: d.t(cx, y - CELL_H // 2 - 8 if key == "src" else y + CELL_H // 2 + 16,
                    "변경 지점", 12, ACC, KR)

# DNAT 가 라우팅 판단 앞(PRE_ROUTING)에 있어야 하는 이유는 본문 산문이 맡는다
d.legend(520, [("바뀌는 자리", ACC), ("라우팅 이전", WARN), ("라우팅 이후", INFO)])
d.save("02-01.netfilter-hooks-flow.svg")
print("ok netfilter-hooks-flow")
