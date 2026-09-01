# 03-04 전체 지도 — 수평 분할을 감당하려면 아래에서부터 쌓아야 하는 것.
# 저자는 이 넷을 층으로 세지 않는다. 층으로 묶은 것은 노트의 읽기이며, 각 층의 문구는 원문 서술을 옮긴 것이다.
# 타입 스펙: type-pyramid — 아래가 넓은 토대, 위로 갈수록 드물고 결정적. 층 넷은 스펙의 4~6 범위 안이다.
#           accent 는 apex 하나에만 (스펙의 "coral on ONE layer only, apex of pyramid").
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
CX = 500
TOP_Y, LAYER_H = 112, 68
W_APEX, W_BASE = 260, 780
N = 4
bw = lambda j: W_APEX + j * (W_BASE - W_APEX) / N     # 경계 j(0=꼭대기)의 폭
by = lambda j: TOP_Y + j * LAYER_H

layers = [  # 위(apex)에서 아래(base)로
    ("최종 산출을 한 팀이 책임진다", "뷰마다 대표 팀 하나", True),
    ("격리 규약을 먼저 정한다", "CSS 접두 · 단일 프레임워크 · 토큰 저장 위치", False),
    ("공유 상태 대신 비동기 통신", "입력 · 출력 이벤트를 문서로 남긴다", False),
    ("굵은 경계로 시작한다", "한 뷰에 조각 6~7 개를 넘기지 않는다", False),
]
LEGEND_Y = by(N) + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04",
      "수평 분할이 요구하는 네 층",
      "아래가 먼저 서야 하는 토대이고 위로 갈수록 드물게 지켜지는 규약이다. 색이 붙은 꼭대기가 저자가 뷰마다 정하라고 못 박은 자리다.",
      "아래에서 위로 읽습니다")

for i, (name, sub, focal) in enumerate(layers):
    yt, yb = by(i), by(i + 1)
    wt, wb = bw(i), bw(i + 1)
    pts = f"{CX - wt/2},{yt} {CX + wt/2},{yt} {CX + wb/2},{yb} {CX - wb/2},{yb}"
    if focal:
        d.o.append(f'<polygon points="{pts}" fill="{ACC}14" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        fill = PAPER2 if i % 2 == 1 else f"{INK}08"
        d.o.append(f'<polygon points="{pts}" fill="{fill}" stroke="{RULE}" stroke-width="1.0"/>')
    d.t(CX, yt + 29, name, 13.5, ACC if focal else INK, KR, "middle", 600)
    d.t(CX, yt + 49, sub, 9.5, ACC if focal else MUTED, KR)

# 왼쪽 여백 축 — 피라미드 가장 넓은 층(x=110)보다 왼쪽
d.arrow([(52, by(N) - 10), (52, by(0) + 12)], SOFT, "soft", 1.1)
d.o.append(f'<text x="36" y="{(by(0) + by(N)) / 2}" transform="rotate(-90 36 {(by(0) + by(N)) / 2})" '
           f'text-anchor="middle" font-family="{MONO}" font-size="9" fill="{SOFT}" letter-spacing="0.14em">RARER</text>')

d.legend(LEGEND_Y, [("저자가 뷰마다 정하라고 못 박은 층", ACC)])
d.save("03-04.horizontal-split-stack.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " base 왼쪽 x:", CX - W_BASE / 2)
