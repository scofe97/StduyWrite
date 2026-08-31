# 03-01 §2 — 수직 분할에서 라우팅이 두 겹으로 갈리는 자리 (원문 Figure 3-2 · 3-3).
# URL 단계가 그대로 소유권 경계다 — 1단계는 셸, 2단계 이후는 조각. 저자가 든 경로 예를 그대로 쓴다.
# 타입 스펙: type-swimlane — 주체 둘을 가로 레인으로 두고 단계가 레인을 건너간다.
#           레인을 건너는 화살표가 이 도식의 논지이므로 거기에만 accent 를 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1280, 420
LABEL_W, LANE_H, LANE_Y = 140, 110, 110
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-01 §2",
      "라우팅이 두 겹으로 갈리는 자리",
      "1단계 URL 은 애플리케이션 셸이, 2단계 이후는 조각이 소유한다. 레인을 건너는 화살표가 셸이 조각에게 넘기는 지점이다.",
      "위 레인이 셸의 몫, 아래 레인이 조각의 몫입니다")

lanes = [("애플리케이션 셸", "GLOBAL ROUTING"), ("마이크로 프론트엔드", "LOCAL ROUTING")]
for k, (name, eyebrow) in enumerate(lanes):
    y = LANE_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 12}" height="{LANE_H}" fill="{INK}05"/>')
    d.line(0, y, W - 12, y, RULE, 0.8)
    d.t(LABEL_W / 2, y + LANE_H / 2 - 4, name, 11.5, INK, KR, "middle", 600)
    d.t(LABEL_W / 2, y + LANE_H / 2 + 14, eyebrow, 7.5, SOFT, MONO)
d.line(0, LANE_Y + 2 * LANE_H, W - 12, LANE_Y + 2 * LANE_H, RULE, 0.8)
d.line(LABEL_W, LANE_Y, LABEL_W, LANE_Y + 2 * LANE_H, RULE, 1.0)

BW, BH, GAP, X0 = 180, 64, 36, 170
steps = [
    (0, "URL 을 받는다", "www.mysite.com"),
    (0, "1단계 경로를 본다", "/catalog"),
    (0, "그 조각을 로드한다", "한 번에 하나만"),
    (1, "2단계 이후를 본다", "/catalog/books"),
    (1, "뷰를 그린다", "도메인 전문가가 소유"),
]
def bx(i): return X0 + i * (BW + GAP)
def by(lane): return LANE_Y + lane * LANE_H + (LANE_H - BH) / 2

# 연결선 먼저
for i in range(4):
    l1, l2 = steps[i][0], steps[i + 1][0]
    x1, x2 = bx(i) + BW, bx(i + 1)
    if l1 == l2:
        d.arrow([(x1, by(l1) + BH / 2), (x2 - 2, by(l2) + BH / 2)], MUTED, "ar", 1.3)
    else:   # 레인을 건너는 자리 — 이 도식의 논지
        y1, y2 = by(l1) + BH, by(l2) + BH / 2
        mx = x1 + GAP / 2
        d.path(f"M {bx(i) + BW / 2} {y1} V {y2 - 8} Q {bx(i) + BW / 2} {y2} {bx(i) + BW / 2 + 8} {y2} H {x2 - 2}", ACC, 1.5, m="acc")
        d.o.append(f'<rect x="{bx(i) + BW / 2 + 14}" y="{y2 - 26}" width="86" height="14" rx="2" fill="{PAPER}"/>')
        d.t(bx(i) + BW / 2 + 57, y2 - 15, "HANDOFF", 8, ACC, MONO)

for i, (lane, title, sub) in enumerate(steps):
    x, y = bx(i), by(lane)
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 26, title, 12, INK, KR, "start", 600)
    d.t(x + 14, y + 46, sub, 9.5, MUTED, MONO, "start")

d.legend(376, [("셸이 조각에게 넘기는 자리", ACC)])
d.save("03-01.routing-split.svg")
print("h 필요:", 376 + 40, " 실제:", H, " 우측끝:", bx(4) + BW)
