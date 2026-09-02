# 06-02 §2 — 두 분할이 개발자에게 요구하는 것 (원문 Horizontal Versus Vertical Split).
# 레인이 분할 방식이고 열이 개발자가 지나는 단계다. 칸의 문구는 원문 서술을 옮긴 것이다.
# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 여기서는 역할 대신 분할 방식이 레인이다.
#           축약: 03-01.routing-split 의 레인 기하(라벨 열 + 가로 구분선)를 승계하고 열을 셋으로 늘렸다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
LX = 240                      # 레인 라벨 열
LANE_Y0, LANE_H = 160, 152
BW, BH, BGAP = 280, 88, 44
X0 = 264
LEGEND_Y = LANE_Y0 + 2 * LANE_H + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-02 §2",
      "두 분할이 개발자에게 요구하는 것",
      "위 레인이 수직 분할이고 아래가 수평 분할이다. 색이 붙은 칸이 표준 도구가 없어 직접 만들어야 하는 자리다.",
      "왼쪽에서 오른쪽으로 개발자가 지나는 단계입니다")

lanes = [
    ("수직 분할", "vertical split", [
        ("SPA 도구 그대로", "기존 작업 흐름이 맞는다", False),
        ("단위 · 통합 · E2E", "특별한 난제가 없다", False),
        ("셸 팀이 라우팅 E2E", "조각 사이 상호작용까지", False),
    ]),
    ("수평 분할", "horizontal split", [
        ("런타임 조립 도구", "표준 도구가 아니다", True),
        ("뷰마다 누가 도나", "한 동작이 다른 반응을 부른다", False),
        ("더 강한 거버넌스", "답할 질문이 훨씬 많다", False),
    ]),
]

# 레인 구분선 먼저 — z-order
d.line(LX, LANE_Y0, LX, LANE_Y0 + 2 * LANE_H, RULE, 1.0)
for i in range(3):
    d.line(12, LANE_Y0 + i * LANE_H, W - 48, LANE_Y0 + i * LANE_H, RULE, 0.8)

for li, (name, en, cells) in enumerate(lanes):
    ly = LANE_Y0 + li * LANE_H
    d.t(24, ly + LANE_H / 2 - 4, name, 13.5, INK, KR, "start", 600)
    d.t(24, ly + LANE_H / 2 + 16, en, 9, MUTED, MONO, "start")
    by = ly + (LANE_H - BH) / 2
    for si, (title, sub, focal) in enumerate(cells):
        x = X0 + si * (BW + BGAP)
        if si < 2:      # 같은 레인 안의 단계 이음
            d.arrow([(x + BW, by + BH / 2), (x + BW + BGAP - 2, by + BH / 2)], MUTED, "ar", 1.3)
        if focal:
            d.o.append(f'<rect x="{x}" y="{by}" width="{BW}" height="{BH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        else:
            d.box(x, by, BW, BH, PAPER2, RULE, 1.0, 6)
        d.t(x + 18, by + 36, title, 12.5, ACC if focal else INK, KR, "start", 600)
        d.t(x + 18, by + 60, sub, 10, MUTED, KR, "start")

d.legend(LEGEND_Y, [("직접 만들어야 하는 자리", ACC)])
d.save("06-02.dx-split.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 3 * BW + 2 * BGAP)
