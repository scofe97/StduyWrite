# 15-02 §4 — 두 값이 정하는 것은 상한과 하한이다
# 본문이 "값이 원하는 복제본 수에 상대적"이라고 못박는다. 그러니 단계별 개수만 나열하면
# 안 되고, 총합의 천장과 가용의 바닥이 선으로 그어져 있어야 그 상대성이 보인다.
# 타입 스펙: type-architecture.md — 상자에 든 것은 단계마다의 파드 수다. 내용만 보면 순차 인덱스 위의 값 추이라 type-line 이 더 맞을 수 있는데, 그림은 상자 사슬로 그려져 있어 재설계 없이는 line 을 선언할 수 없다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 900, 540
d = D(W, H, "KUBERNETES IN ACTION · 15-02",
      "천장과 바닥 사이에서만 움직인다",
      "maxSurge 는 원하는 수를 얼마나 넘어설 수 있는지를, maxUnavailable 은 얼마나 모자랄 수 있는지를 "
      "정한다. 두 값 모두 원하는 복제본 수에 상대적이다.")

lead = "replicas 3 · maxSurge 1 · maxUnavailable 1 → 총합 ≤ 4 · 가용 ≥ 2"
d.t(12, 74, lead, 12, MUTED, KR, "start")

STEP = [("시작", 3, 0, 3, 3), ("새 +2 · 옛 −1", 2, 2, 4, 2),
        ("교체 진행", 1, 3, 4, 3), ("옛 −1", 0, 3, 3, 3)]
BW, GP = 164, 36
X0 = (W - (4 * BW + 3 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(4)]

d.line(36, 194, 864, 194, WARN, 1.2, "6 5")
d.t(860, 186, "총합 천장 4 = replicas + maxSurge", 12, WARN, KR, "end")
d.line(36, 396, 864, 396, OK, 1.2, "6 5")
d.t(860, 388, "가용 바닥 2 = replicas − maxUnavailable", 12, OK, KR, "end")

def my_tag(d, cx, cy, txt, c, w=120):
    d.box(cx - w // 2, cy - 12, w, 24, fill=PAPER, stroke=c, sw=1.1, r=4)
    d.t(cx, cy + 4, txt, 12, c, KR, "middle", 600)

for cx, (t, old, new, total, avail) in zip(CX, STEP):
    d.t(cx, 168, t, 12, SOFT, KR)
    d.box(cx - BW // 2, 208, BW, 102, PAPER2, RULE, 1.0, 6)
    d.t(cx, 236, f"옛 0.5 × {old}", 12, MUTED, MONO)
    d.t(cx, 258, f"새 0.6 × {new}", 12, MUTED, MONO)
    my_tag(d, cx, 290, f"총합 {total}", WARN if total == 4 else SOFT, 116)
    my_tag(d, cx, 356, f"가용 {avail}", ACC if avail == 2 else OK, 116)

for a, b in zip(CX, CX[1:]):
    d.path(f"M {a + BW // 2 + 4} {258} L {b - BW // 2 - 8} {258}", MUTED, 1.4, m="ar")

d.t(24, 434, "값은 원하는 수가 기준 — replicas 3 · maxUnavailable 1 의 가용 하한은 현재 5 개여도 2 개(=3−1), 4 개가 아님",
    12, MUTED, KR, "start")
d.t(24, 456, "순서가 강제됨 — maxSurge 0: 천장 3, 옛 파드를 먼저 지움 · maxUnavailable 0: 바닥 3, 새 파드를 먼저 띄움",
    12, MUTED, KR, "start")

def my_legend(d, y, items):
    d.line(12, y, d.w - 48, y, RULE, 0.8)
    d.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
    x = 100
    for lab, c in items:
        d.o.append(f'<rect x="{x}" y="{y+10}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        d.t(x + 22, y + 22, lab, 12, MUTED, KR, "start")
        x += 44 + len(lab) * 14

my_legend(d, 488, [("천장에 닿은 단계", WARN), ("가용 파드", OK), ("바닥에 닿은 단계", ACC)])
d.save("15-02-maxsurge-maxunavailable.svg")
print("ok")
