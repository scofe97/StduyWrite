# 04-02 §4 — 셸이 fetch 를 갈아 끼워 토큰을 붙이는 방식의 갈림길.
# 저자가 "수평 분할에서는 잘 맞지만 수직 분할에서는 조각이 스스로 정해야 할 수 있다"고 적은 대목을 판단으로 세운다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

W = 1100
S_Y, D_CY, B_Y, R_Y = 104, 216, 312, 400
NH, RH = 52, 52
LEFT, RIGHT = 275, 825
LEGEND_Y = R_Y + RH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-02 §4",
      "토큰을 누가 붙일 것인가",
      "셸이 window.fetch 를 감싸면 모든 조각의 요청에 헤더가 붙는다. 색이 붙은 갈래가 저자가 이 방식에 잘 맞는다고 적은 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

d.arrow([(550, S_Y + NH), (550, D_CY - 46)], MUTED, "ar", 1.4)
d.arrow([(420, D_CY), (LEFT, D_CY), (LEFT, B_Y)], ACC, "acc", 1.5)
d.arrow([(680, D_CY), (RIGHT, D_CY), (RIGHT, B_Y)], MUTED, "ar", 1.4)
d.arrow([(LEFT, B_Y + NH), (LEFT, R_Y)], MUTED, "ar", 1.4)
d.arrow([(RIGHT, B_Y + NH), (RIGHT, R_Y)], MUTED, "ar", 1.4)

d.box(550 - 200, S_Y, 400, NH, PAPER2, RULE, 1.0, 6)
d.t(550, S_Y + 24, "조각이 API 를 부를 때 토큰이 필요하다", 12.5, INK, KR, "middle", 600)
d.t(550, S_Y + 41, "Authorization: Bearer ...", 9, MUTED, MONO)

d.o.append(f'<polygon points="550,{D_CY-46} 680,{D_CY} 550,{D_CY+46} 420,{D_CY}" '
           f'fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(550, D_CY + 5, "수평 분할인가", 12.5, INK, KR, "middle", 600)
d.t(LEFT + 14, D_CY + 46, "그렇다", 9.5, ACC, MONO, "start")
d.t(RIGHT + 14, D_CY + 46, "아니다 · 수직 분할", 9.5, MUTED, MONO, "start")

d.tone(LEFT - 180, B_Y, 360, NH, ACC, 6, "14", 1.3)
d.t(LEFT, B_Y + 24, "셸이 fetch 를 감싸 일괄로 붙인다", 12, ACC, KR, "middle", 600)
d.t(LEFT, B_Y + 41, "window.fetch = async (...) => {...}", 9, ACC, MONO)

d.box(RIGHT - 180, B_Y, 360, NH, PAPER2, RULE, 1.0, 6)
d.t(RIGHT, B_Y + 24, "조각이 붙일지 스스로 정한다", 12, INK, KR, "middle", 600)
d.t(RIGHT, B_Y + 41, "도메인마다 팀이 다르다", 9, MUTED, KR)

d.box(LEFT - 180, R_Y, 360, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(LEFT, R_Y + 24, "횡단 관심사를 셸이 모은다", 12, INK, KR, "middle", 600)
d.t(LEFT, R_Y + 41, "토큰이 필요 없는 엔드포인트까지 붙는다", 9.5, WARN, KR)

d.box(RIGHT - 180, R_Y, 360, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(RIGHT, R_Y + 24, "필요한 곳에만 붙는다", 12, INK, KR, "middle", 600)
d.t(RIGHT, R_Y + 41, "다른 도메인으로 토큰이 새지 않는다", 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("저자가 잘 맞는다고 적은 갈래", ACC), ("그 갈래가 지는 위험", WARN)])
d.save("04-02.token-middleware.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
