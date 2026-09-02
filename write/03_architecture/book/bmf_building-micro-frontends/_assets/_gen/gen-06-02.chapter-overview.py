# 06-02 학습 목표 뒤 전체 지도 — 개발자 경험의 네 자리를 겪는 순서로 잇는다.
# 색이 붙은 칸은 §2 다. 이 편의 논지가 "DX 는 도구가 아니라 분할 방식의 결과"이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체 없는 단계 지도라 §1 lanes 를 쓰지 않는다(visual-diagram-selection §알려진 공백).
#           네 칸은 한 줄에 놓으므로 stride 를 CW+GAP=300 으로 새로 잡고 06-04·06-06 이 이것을 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 276, 96, 24, 40, 104
LEGEND_Y = Y + CH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-02",
      "개발자 경험의 네 자리 — 읽는 순서",
      "DX 팀이 보는 것에서 출발해 분할 방식이 경험을 가르는 자리를 지나 환경 전략에서 멈춘다.",
      "칸마다 절 번호와 그 절이 답하는 것이 붙습니다")

cards = [
    ("§1", "DX 팀은 무엇을 보는가", "도구와 절차를 관찰한다"),
    ("§2", "분할이 경험을 가른다", "수직은 SPA 그대로"),
    ("§3", "만드는 일도 자동화한다", "표준을 함께 심는다"),
    ("§4", "환경을 몇 개 둘 것인가", "세 개 + 온디맨드"),
]
FOCAL = 1

for i in range(len(cards) - 1):
    x1 = X0 + i * (CW + GAP)
    d.arrow([(x1 + CW, Y + CH / 2), (x1 + CW + GAP - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, q) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if i == FOCAL:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if i == FOCAL else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, title, 14, ACC if i == FOCAL else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 12, MUTED, KR, "start")

d.legend(LEGEND_Y, [("이 편의 논지", ACC)])
d.save("06-02.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 4 * CW + 3 * GAP)
