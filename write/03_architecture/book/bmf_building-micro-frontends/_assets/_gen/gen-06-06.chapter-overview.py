# 06-06 학습 목표 뒤 전체 지도 — 피트니스 함수에서 6장을 닫는 데까지 다섯 자리를 순서로 잇는다.
# 색이 붙은 칸은 §2 다. 여섯 특성 가운데 넷째가 이 아키텍처의 것이라는 것이 이 편의 논지이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체 없는 단계 지도라 §1 lanes 를 쓰지 않는다. stride 는 06-03 의 CW+GAP=240 을 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 216, 96, 24, 40, 104
LEGEND_Y = Y + CH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-06",
      "피트니스 함수에서 6장을 닫기까지",
      "아키텍처 결정을 재는 방법에서 출발해 조각에만 붙는 단계와 관측을 지나 6장의 결론에서 멈춘다.",
      "칸마다 절 번호와 그 절이 답하는 것이 붙습니다")

cards = [
    ("§1", "어떻게 재는가", "피트니스 함수의 정의"),
    ("§2", "재는 여섯", "넷째가 이 아키텍처의 것"),
    ("§3", "조각에만 붙는 단계", "package.json 을 검사한다"),
    ("§4", "관측이 루프를 닫는다", "프로덕션에서 오는 신호"),
    ("§5", "6장을 닫으며", "반복되는 과정이다"),
]
FOCAL = 1

for i in range(len(cards) - 1):
    x = X0 + i * (CW + GAP)
    d.arrow([(x + CW, Y + CH / 2), (x + CW + GAP - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, q) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if i == FOCAL:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if i == FOCAL else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 13.5, ACC if i == FOCAL else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 11, MUTED, KR, "start")

d.legend(LEGEND_Y, [("이 아키텍처의 것이 나오는 자리", ACC)])
d.save("06-06.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 5 * CW + 4 * GAP)
