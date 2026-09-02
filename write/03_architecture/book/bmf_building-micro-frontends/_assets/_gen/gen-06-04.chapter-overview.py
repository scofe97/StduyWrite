# 06-04 학습 목표 뒤 전체 지도 — 폴리레포에서 CI 소유권까지 네 자리를 순서로 잇는다.
# 색이 붙은 칸은 §1 이다. 이 편의 논지가 "저장소를 나누면 결합이 계약으로 바뀐다"이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체 없는 단계 지도라 §1 lanes 를 쓰지 않는다. stride 는 06-02 의 CW+GAP=300 을 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 276, 96, 24, 40, 104
LEGEND_Y = Y + CH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-04",
      "폴리레포와 CI 소유권 — 읽는 순서",
      "저장소를 나눌 때 생기는 것에서 출발해 둘을 섞는 길을 지나 CI 를 누가 소유하는가에서 멈춘다.",
      "칸마다 절 번호와 그 절이 답하는 것이 붙습니다")

cards = [
    ("§1", "나누면 무엇이 생기나", "결합이 계약으로 바뀐다"),
    ("§2", "못 주는 넷", "저장소의 난립"),
    ("§3", "둘을 섞는 길", "서브도메인으로 묶는다"),
    ("§4", "CI를 누가 소유하나", "외부 수호자가 아니라 팀"),
]
FOCAL = 0

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
    d.t(x + 16, Y + 52, title, 14, ACC if i == FOCAL else INK, KR, "start", 600)
    d.t(x + 16, Y + 76, q, 12, MUTED, KR, "start")

d.legend(LEGEND_Y, [("이 편의 논지", ACC)])
d.save("06-04.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 4 * CW + 3 * GAP)
