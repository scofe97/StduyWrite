# 05-04 §4 — 공유 컴포넌트를 언제 합칠 것인가. 저자가 빌드 시점을 고르고 그 근거를 적은 대목이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

W = 1180
S_Y, D_CY, B_Y, R_Y = 104, 216, 312, 400
NH, RH = 52, 52
LEFT, RIGHT = 290, 890
LEGEND_Y = R_Y + RH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-04 §4",
      "헤더와 푸터를 언제 합칠 것인가",
      "존이 독립 배포되므로 공유 컴포넌트를 언제 끼워 넣을지 정해야 한다. 색이 붙은 갈래가 저자가 대부분 팀에 권하는 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

d.arrow([(590, S_Y + NH), (590, D_CY - 46)], MUTED, "ar", 1.4)
d.arrow([(460, D_CY), (LEFT, D_CY), (LEFT, B_Y)], ACC, "acc", 1.5)
d.arrow([(720, D_CY), (RIGHT, D_CY), (RIGHT, B_Y)], MUTED, "ar", 1.4)
d.arrow([(LEFT, B_Y + NH), (LEFT, R_Y)], MUTED, "ar", 1.4)
d.arrow([(RIGHT, B_Y + NH), (RIGHT, R_Y)], MUTED, "ar", 1.4)

d.box(590 - 210, S_Y, 420, NH, PAPER2, RULE, 1.0, 6)
d.t(590, S_Y + 24, "헤더와 푸터를 모든 존이 함께 쓴다", 12.5, INK, KR, "middle", 600)
d.t(590, S_Y + 41, "@t-shirt-shop/shared", 9, MUTED, MONO)

d.o.append(f'<polygon points="590,{D_CY-46} 720,{D_CY} 590,{D_CY+46} 460,{D_CY}" '
           f'fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(590, D_CY + 5, "성능과 신뢰성이 먼저인가", 11.5, INK, KR, "middle", 600)
d.t(LEFT + 14, D_CY + 46, "그렇다", 9.5, ACC, MONO, "start")
d.t(RIGHT + 14, D_CY + 46, "갱신 속도가 먼저다", 9.5, MUTED, MONO, "start")

d.tone(LEFT - 200, B_Y, 400, NH, ACC, 6, "14", 1.3)
d.t(LEFT, B_Y + 24, "빌드 시점에 번들한다", 12, ACC, KR, "middle", 600)
d.t(LEFT, B_Y + 41, "각 존이 공통 라이브러리를 임포트", 9.5, ACC, KR)

d.box(RIGHT - 200, B_Y, 400, NH, PAPER2, RULE, 1.0, 6)
d.t(RIGHT, B_Y + 24, "런타임에 불러온다", 12, INK, KR, "middle", 600)
d.t(RIGHT, B_Y + 41, "Module Federation · HTML 조각 주입", 9.5, MUTED, KR)

d.box(LEFT - 200, R_Y, 400, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(LEFT, R_Y + 22, "런타임이 가볍고 예측 가능하다", 10.5, INK, KR)
d.t(LEFT, R_Y + 40, "대신 버저닝에 규율이 든다 · Dependabot", 9.5, MUTED, KR)

d.box(RIGHT - 200, R_Y, 400, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(RIGHT, R_Y + 22, "존을 다시 빌드하지 않고 굴린다", 10.5, INK, KR)
d.t(RIGHT, R_Y + 40, "버전 불일치와 예상 못한 동작의 위험", 9.5, WARN, KR)

d.legend(LEGEND_Y, [("저자가 대부분 팀에 권하는 갈래", ACC), ("그 갈래가 지는 위험", WARN)])
d.save("05-04.shared-timing.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
