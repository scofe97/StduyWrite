# 06-03 학습 목표 뒤 전체 지도 — 모노레포를 읽는 다섯 자리를 순서로 잇는다.
# 색이 붙은 칸은 §3 이다. 이 편의 논지가 "이점과 값이 같은 사실에서 나온다"이고 그 뒷면이 §3 이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체 없는 단계 지도라 §1 lanes 를 쓰지 않는다(visual-diagram-selection §알려진 공백).
#           다섯 칸을 한 줄에 놓으므로 stride 를 CW+GAP=240 으로 잡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 216, 96, 24, 40, 104
LEGEND_Y = Y + CH + 32
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-03",
      "모노레포를 읽는 다섯 자리",
      "저장소를 하나로 두는 정의에서 출발해 이점과 값을 지나 Google 이 스스로 내린 결론에서 멈춘다.",
      "칸마다 절 번호와 그 절이 답하는 것이 붙습니다")

cards = [
    ("§1", "저장소를 하나로", "모노레포의 정의"),
    ("§2", "쉬워지는 여섯", "한자리에 있어서"),
    ("§3", "치르는 값 다섯", "같은 사실의 뒷면"),
    ("§4", "도구가 따라온다", "sparse-checkout"),
    ("§5", "Google의 결론", "판단 기준은 문화다"),
]
FOCAL = 2

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

d.legend(LEGEND_Y, [("이점의 뒷면이 드러나는 자리", ACC)])
d.save("06-03.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 5 * CW + 4 * GAP)
