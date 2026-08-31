# 01-01 §4 — 세 세대를 지나며 무엇이 쪼개졌고 무엇이 통짜로 남았는가.
# 본문이 "전이마다 그 전이를 일으킨 조건이 있다"·"presentation 층만 마지막까지 통짜였다"를 논지로 삼는다.
# 타입 스펙: type-state — 플랫폼 하나가 조건을 만나 다음 아키텍처 상태로 넘어가고, 전이마다 방아쇠가 붙는다.
#           축약: 종료 상태를 두지 않는다. 원문은 마이크로 프론트엔드를 마지막 선택지가 아니라
#           "추가로 쓸 수 있는 옵션"이라 적으므로 ringed end dot 은 없는 사실이 된다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, WARN, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1472, 448
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01 §4",
      "세 세대 — 무엇이 쪼개졌고 무엇이 통짜로 남았는가",
      "원문 Figure 1-1·1-2·1-3 을 한 축 위에 이어 붙인 상태 전이. 세 계층 가운데 presentation 만 두 번째 세대까지 통짜로 남는다.",
      "전이 화살표 아래가 그 전이를 일으킨 조건입니다. 막대가 나뉜 층이 그 세대에 쪼개진 층입니다")

BW, BH, GAP, X0, BY = 400, 200, 64, 88, 112     # stride = BW + GAP = 464
CY = BY + BH / 2                                 # 212
LAYERS = ("PRESENTATION", "APPLICATION", "PERSISTENCE")
BAR_X, BAR_W, ROW_H, ROW0, ROW_STRIDE = 150, 230, 32, 72, 40

states = [
    ("3계층 모놀리스", "아티팩트 하나 · 파이프라인 하나", (False, False, False), None),
    ("마이크로서비스 + SPA", "API와 저장소만 서비스 단위로", (False, True, True), 0),
    ("마이크로서비스 + 마이크로 프론트엔드", "UI도 비즈니스 도메인 단위로", (True, True, True), None),
]
transitions = [
    ("팀 확장 · 트래픽 증가", "[캐시 불가 API만 오리진을 누른다] / 코드베이스 분할"),
    ("프론트엔드 팀 확장 필요", "[SPA 한 덩어리로는 더 못 나눈다] / presentation 분할"),
]

def bx(i):
    return X0 + i * (BW + GAP)

# 연결선 먼저 — z-order
d.o.append(f'<circle cx="40" cy="{CY}" r="6" fill="{INK}"/>')
d.arrow([(50, CY), (bx(0) - 2, CY)], MUTED, "ar", 1.4)
for i in range(2):
    x1, x2 = bx(i) + BW, bx(i + 1)
    d.arrow([(x1, CY), (x2 - 2, CY)], MUTED, "ar", 1.4)
    cx = (x1 + x2) / 2
    d.line(cx, CY + 8, cx, 340, RULE, 0.8, "3 5")     # 라벨로 내려가는 실낱
    d.t(cx, 356, transitions[i][0], 11, INK, KR, "middle", 600)
    d.t(cx, 374, transitions[i][1], 10, MUTED, MONO)

for i, (name, sub, split, stuck) in enumerate(states):
    x, focal = bx(i), (i == 2)
    if focal:
        d.o.append(f'<rect x="{x}" y="{BY}" width="{BW}" height="{BH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, BY, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(x + 20, BY + 30, name, 15, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, BY + 52, sub, 11, MUTED, KR, "start")
    for r, layer in enumerate(LAYERS):
        ry = BY + ROW0 + r * ROW_STRIDE
        d.t(x + 20, ry + 20, layer, 9, SOFT, MONO, "start")
        if split[r]:                                   # 네 조각으로 나뉜 층
            for k in range(4):
                sx = x + BAR_X + k * 60
                d.box(sx, ry, 50, ROW_H, PAPER, RULE, 0.9, 4)
        else:                                          # 통짜로 남은 층
            c = WARN if stuck == r else RULE
            sw = 1.3 if stuck == r else 0.9
            fill = f"{WARN}14" if stuck == r else PAPER
            d.o.append(f'<rect x="{x + BAR_X}" y="{ry}" width="{BAR_W}" height="{ROW_H}" rx="4" fill="{fill}" stroke="{c}" stroke-width="{sw}"/>')

d.legend(404, [("이 책이 다루는 자리", ACC), ("아직 쪼개지지 않은 층", WARN)])
d.save("01-01.three-generations.svg")
print("h 필요:", 404 + 22 + 16, " 실제:", H, " 우측끝:", bx(2) + BW, "/", W)
