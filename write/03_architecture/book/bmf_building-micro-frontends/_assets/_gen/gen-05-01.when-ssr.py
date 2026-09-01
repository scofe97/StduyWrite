# 05-01 §1 — SSR 이 맞는 자리를 가르는 판단. 저자가 "빛나는 시나리오" 셋과 "마지막에 고려할 것" 하나로 적은 대목이다.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, KR, MONO

W = 1140
S_Y, D_CY, B_Y, R_Y = 104, 216, 312, 400
NH, RH = 52, 52
LEFT, RIGHT = 280, 860
LEGEND_Y = R_Y + RH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-01 §1",
      "SSR 이 첫 선택지인가 마지막 선택지인가",
      "같은 기술이 어떤 서비스에는 매출이고 어떤 서비스에는 부담이다. 색이 붙은 갈래가 저자가 SSR 이 빛난다고 적은 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

d.arrow([(570, S_Y + NH), (570, D_CY - 46)], MUTED, "ar", 1.4)
d.arrow([(440, D_CY), (LEFT, D_CY), (LEFT, B_Y)], ACC, "acc", 1.5)
d.arrow([(700, D_CY), (RIGHT, D_CY), (RIGHT, B_Y)], MUTED, "ar", 1.4)
d.arrow([(LEFT, B_Y + NH), (LEFT, R_Y)], MUTED, "ar", 1.4)
d.arrow([(RIGHT, B_Y + NH), (RIGHT, R_Y)], MUTED, "ar", 1.4)

d.box(570 - 210, S_Y, 420, NH, PAPER2, RULE, 1.0, 6)
d.t(570, S_Y + 24, "어떤 렌더링 전략을 고를 것인가", 12.5, INK, KR, "middle", 600)
d.t(570, S_Y + 41, "LCP · CLS · SEO crawlability", 9, MUTED, MONO)

d.o.append(f'<polygon points="570,{D_CY-46} 700,{D_CY} 570,{D_CY+46} 440,{D_CY}" '
           f'fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(570, D_CY + 5, "콘텐츠가 공개인가", 12.5, INK, KR, "middle", 600)
d.t(LEFT + 14, D_CY + 46, "그렇다 · B2C", 9.5, ACC, MONO, "start")
d.t(RIGHT + 14, D_CY + 46, "대부분 인증 뒤 · B2B", 9.5, MUTED, MONO, "start")

d.tone(LEFT - 200, B_Y, 400, NH, ACC, 6, "14", 1.3)
d.t(LEFT, B_Y + 24, "SSR 이 빛나는 자리", 12, ACC, KR, "middle", 600)
d.t(LEFT, B_Y + 41, "뉴스 · 블로그 · 이커머스", 9.5, ACC, KR)

d.box(RIGHT - 200, B_Y, 400, NH, PAPER2, RULE, 1.0, 6)
d.t(RIGHT, B_Y + 24, "가장 마지막에 고려한다", 12, INK, KR, "middle", 600)
d.t(RIGHT, B_Y + 41, "저자가 여러 난제를 이유로 든다", 9.5, WARN, KR)

d.box(LEFT - 200, R_Y, 400, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(LEFT, R_Y + 22, "크롤러가 서버 렌더 콘텐츠를 색인한다", 10.5, INK, KR)
d.t(LEFT, R_Y + 40, "느린 망 · 약한 기기에서도 HTML 이 먼저 온다", 9.5, MUTED, KR)

d.box(RIGHT - 200, R_Y, 400, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(RIGHT, R_Y + 22, "색인할 공개 콘텐츠가 거의 없다", 10.5, INK, KR)
d.t(RIGHT, R_Y + 40, "서버 자원만 쓰고 얻는 것이 적다", 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("SSR 이 빛나는 갈래", ACC), ("저자가 붙인 경고", WARN)])
d.save("05-01.when-ssr.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
