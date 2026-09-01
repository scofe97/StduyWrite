# 04-01 §4 — 리모트를 어디서 알려 줄 것인가. 저자가 "온라인 예제는 번들러 설정에 직접 적지만
# 프로덕션에서는 그렇게 하는 팀을 거의 못 봤다"고 적은 대목을 판단으로 세운다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1040
S_Y, D_CY, B_Y, R_Y = 104, 216, 312, 400
NH, RH = 52, 52
LEFT, RIGHT = 260, 780
LEGEND_Y = R_Y + RH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-01 §4",
      "리모트를 어디서 알려 줄 것인가",
      "번들러 설정에 박아 두면 예제로는 깔끔하지만 환경이 여럿이면 막힌다. 색이 붙은 갈래가 저자가 실제 현장에서 본 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

d.arrow([(520, S_Y + NH), (520, D_CY - 46)], MUTED, "ar", 1.4)
d.arrow([(390, D_CY), (LEFT, D_CY), (LEFT, B_Y)], MUTED, "ar", 1.4)
d.arrow([(650, D_CY), (RIGHT, D_CY), (RIGHT, B_Y)], ACC, "acc", 1.5)
d.arrow([(LEFT, B_Y + NH), (LEFT, R_Y)], MUTED, "ar", 1.4)
d.arrow([(RIGHT, B_Y + NH), (RIGHT, R_Y)], MUTED, "ar", 1.4)

d.box(520 - 190, S_Y, 380, NH, PAPER2, RULE, 1.0, 6)
d.t(520, S_Y + 24, "호스트가 어떤 리모트를 부를지 정한다", 12.5, INK, KR, "middle", 600)
d.t(520, S_Y + 41, "Module Federation host config", 9, MUTED, MONO)

d.o.append(f'<polygon points="520,{D_CY-46} 650,{D_CY} 520,{D_CY+46} 390,{D_CY}" '
           f'fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(520, D_CY + 5, "환경이 하나뿐인가", 12.5, INK, KR, "middle", 600)
d.t(LEFT + 14, D_CY + 46, "그렇다", 9.5, MUTED, MONO, "start")
d.t(RIGHT + 14, D_CY + 46, "아니다", 9.5, ACC, MONO, "start")

d.box(LEFT - 165, B_Y, 330, NH, PAPER2, RULE, 1.0, 6)
d.t(LEFT, B_Y + 24, "번들러 설정에 정적으로 적는다", 12, INK, KR, "middle", 600)
d.t(LEFT, B_Y + 41, "remotes: { ... }", 9, MUTED, MONO)

d.tone(RIGHT - 165, B_Y, 330, NH, ACC, 6, "14", 1.3)
d.t(RIGHT, B_Y + 24, "런타임에 등록한다", 12, ACC, KR, "middle", 600)
d.t(RIGHT, B_Y + 41, "registerRemotes()", 9, ACC, MONO)

d.box(LEFT - 165, R_Y, 330, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(LEFT, R_Y + 24, "예제에서 흔한 모양", 12, INK, KR, "middle", 600)
d.t(LEFT, R_Y + 41, "저자가 현장에서 거의 못 봤다고 적는다", 9.5, MUTED, KR)

d.box(RIGHT - 165, R_Y, 330, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(RIGHT, R_Y + 24, "환경마다 다른 엔드포인트를 쥔다", 12, INK, KR, "middle", 600)
d.t(RIGHT, R_Y + 41, "국가 · 역할별 뷰도 여기서 갈린다", 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("저자가 현장에서 본 쪽", ACC)])
d.save("04-01.remote-registration.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
