# 05-05 §3 — BBC 가 QCon London 2025 에서 공유한 계층별 캐시 배치 (원문 Figure 5-4).
# 계층 이름과 각 계층의 캐시, TTL 수치는 저자가 적은 것만 옮긴다.
# 타입 스펙: type-architecture — 계층 경계로 묶은 구성요소와 그 사이 연결.
#           accent 는 요청 대부분을 흡수해 나머지를 지키는 단 하나의 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, KR, MONO

W = 1240
BX, BW = 300, 640
LAYERS = [
    ("CDN", "인기 콘텐츠는 여기서 끝난다", "속보 30초 · 아카이브는 며칠", None, True),
    ("website / app APIs", "람다가 SSR 을 처리한다", "렌더된 HTML 조각", "Redis", False),
    ("business layer", "여러 소스를 모아 로직을 적용한다", "자주 쓰는 비즈니스 데이터", "Redis", False),
    ("service gateway", "하위 데이터 소스로 잇는다", "만료 시각을 흩뜨린다", "Redis", False),
    ("데이터 소스", "여기까지 오는 요청이 가장 적다", "", None, False),
]
TOP, LH, GAP = 112, 84, 30
LEGEND_Y = TOP + len(LAYERS) * (LH + GAP) - GAP + 34
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-05 §3",
      "BBC 는 층마다 캐시를 둔다",
      "요청이 아래로 내려갈수록 수가 준다. 색이 붙은 맨 위가 반복 요청 대부분을 흡수해 안쪽 시스템을 지킨다.",
      "왼쪽 상자가 계층이고 오른쪽 칩이 그 계층에 붙은 캐시입니다")

for i, (name, sub, note, cache, focal) in enumerate(LAYERS):
    y = TOP + i * (LH + GAP)
    if focal:
        d.tone(BX, y, BW, LH, ACC, 6, "12", 1.4)
    else:
        d.box(BX, y, BW, LH, PAPER2, RULE, 1.0, 6)
    d.t(BX + 20, y + 30, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(BX + 20, y + 52, sub, 10, MUTED, KR, "start")
    if note:
        d.t(BX + 20, y + 72, note, 9.5, SOFT, MONO, "start")
    if cache:
        d.o.append(f'<rect x="{BX + BW + 40}" y="{y + 24}" width="150" height="36" rx="4" '
                   f'fill="{OK}14" stroke="{OK}" stroke-width="1.1"/>')
        d.t(BX + BW + 115, y + 47, cache, 11, OK, MONO)
        d.line(BX + BW, y + LH / 2, BX + BW + 40, y + 42, RULE, 1.0)
    if i < len(LAYERS) - 1:
        d.arrow([(BX + BW / 2, y + LH), (BX + BW / 2, y + LH + GAP - 2)], INFO, "info", 1.4)
        d.t(BX + BW / 2 + 14, y + LH + GAP / 2 + 4, "캐시 미스만 내려간다", 8.5, INFO, KR, "start")

d.t(150, TOP + 40, "요청이", 11, MUTED, KR)
d.t(150, TOP + 60, "아래로 갈수록", 11, MUTED, KR)
d.t(150, TOP + 80, "줄어든다", 11, MUTED, KR)
d.arrow([(150, TOP + 110), (150, TOP + len(LAYERS) * (LH + GAP) - GAP - 20)], SOFT, "soft", 1.1)

d.legend(LEGEND_Y, [("반복 요청 대부분을 흡수하는 계층", ACC), ("계층마다 붙은 캐시", OK)])
d.save("05-05.bbc-architecture.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
