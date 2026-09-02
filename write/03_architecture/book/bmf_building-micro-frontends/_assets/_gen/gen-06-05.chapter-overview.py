# 06-05 학습 목표 뒤 전체 지도 — E2E 테스트의 다섯 자리를 읽는 순서로 잇는다.
# 색이 붙은 칸은 §4 다. 소유권 질문이 한 겹 더 생기는 자리가 거기이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체 없는 단계 지도라 §1 lanes 를 쓰지 않는다. stride 는 06-03 의 CW+GAP=240 을 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 216, 96, 24, 40, 104
LEGEND_Y = Y + CH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-05",
      "E2E 테스트의 다섯 자리",
      "왜 E2E 만 달라지는지에서 출발해 두 분할의 난제를 지나 기술 선택지 셋에서 멈춘다.",
      "칸마다 절 번호와 그 절이 답하는 것이 붙습니다")

cards = [
    ("§1", "왜 E2E만 달라지나", "소유 경계를 넘는다"),
    ("§2", "어디서 테스트하나", "온디맨드가 있는가"),
    ("§3", "수직 분할의 난제", "양쪽이 문을 나눠 쓴다"),
    ("§4", "수평 분할의 난제", "한 조각이 여러 뷰에"),
    ("§5", "세 기술 선택지", "프록시가 의존을 없앤다"),
]
FOCAL = 3

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

d.legend(LEGEND_Y, [("소유권 질문이 한 겹 더 생기는 자리", ACC)])
d.save("06-05.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 5 * CW + 4 * GAP)
