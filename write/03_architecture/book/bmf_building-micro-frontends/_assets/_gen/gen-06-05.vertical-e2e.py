# 06-05 §3 — 수직 분할에서 경계를 넘는 테스트를 양쪽이 나눠 쓴다 (원문 Figure 6-4 와 그 서술).
# 레인이 팀이고 왼쪽 열이 자기 도메인, 오른쪽 열이 경계를 넘는 확인이다. 문구는 원문 서술 그대로다.
# 타입 스펙: type-swimlane — 역할을 가로지르며 넘겨받는 절차. 여기서는 테스트 책임이 레인마다 갈린다.
#           축약: 06-02.dx-split 의 레인 기하(라벨 열 + 가로 구분선)를 승계하고 열을 둘로 줄였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
LX = 260
LANE_Y0, LANE_H = 160, 140
BW, BH, BGAP = 440, 96, 20
X0 = 284
LEGEND_Y = LANE_Y0 + 3 * LANE_H + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-05 §3",
      "경계를 넘는 테스트는 양쪽이 나눠 쓴다",
      "왼쪽 열이 자기 도메인 안이고 오른쪽 열이 경계 너머의 확인이다. 색이 붙은 칸이 팀의 통제 밖을 향하는 테스트다.",
      "각 팀은 자기 조각이 나가는 문과 들어오는 문만 책임집니다")

lanes = [
    ("카탈로그 팀", "catalog",
     ("카탈로그의 모든 논리 경로", "SPA 에서 하던 것과 다르지 않다"),
     ("로그아웃하면 sign-in 이 뜨는가", "프로필로 가면 my account 가 뜨는가")),
    ("sign-in · my account 팀", "adjacent domains",
     ("자기 비즈니스 도메인", "각자의 논리 경로"),
     ("카탈로그가 기대대로 뜨는가", "돌아오는 문을 확인한다")),
    ("애플리케이션 셸 팀", "application shell",
     ("라우팅 로직을 소유한다", "예시에서 셸이 경로를 정한다"),
     ("전체 경로 · 로그인과 로그아웃", "URL 마다 알맞은 조각을 로드하는가")),
]

# 레인 구분선 먼저 — z-order
d.line(LX, LANE_Y0, LX, LANE_Y0 + 3 * LANE_H, RULE, 1.0)
for i in range(4):
    d.line(12, LANE_Y0 + i * LANE_H, W - 48, LANE_Y0 + i * LANE_H, RULE, 0.8)

for li, (name, en, own, cross) in enumerate(lanes):
    ly = LANE_Y0 + li * LANE_H
    d.t(24, ly + LANE_H / 2 - 4, name, 12.5, INK, KR, "start", 600)
    d.t(24, ly + LANE_H / 2 + 16, en, 9, MUTED, MONO, "start")
    by = ly + (LANE_H - BH) / 2
    d.box(X0, by, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(X0 + 18, by + 38, own[0], 12, INK, KR, "start", 600)
    d.t(X0 + 18, by + 62, own[1], 10, MUTED, KR, "start")
    x2 = X0 + BW + BGAP
    d.arrow([(X0 + BW, by + BH / 2), (x2 - 2, by + BH / 2)], ACC, "acc", 1.3)
    d.o.append(f'<rect x="{x2}" y="{by}" width="{BW}" height="{BH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(x2 + 18, by + 38, cross[0], 12, ACC, KR, "start", 600)
    d.t(x2 + 18, by + 62, cross[1], 10, MUTED, KR, "start")

d.legend(LEGEND_Y, [("팀의 통제 밖을 향하는 테스트", ACC)])
d.save("06-05.vertical-e2e.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 2 * BW + BGAP)
