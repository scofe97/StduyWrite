# 03-07 전체 지도 — 웹 컴포넌트를 이루는 세 기술과 각각이 조각에서 맡는 일.
# 저자가 "셋 가운데 조각에 특히 유용한 것은 custom elements 와 shadow DOM"이라 못 박으므로 shadow DOM 에 accent 를 준다.
# 타입 스펙: type-tree — 뿌리 하나에서 갈라지는 단일 부모 계층. 되돌아오는 간선이 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
ROOT_W, NW, NH = 260, 240, 52
ROOT_Y, T1_Y, T2_Y = 104, 208, 312
CENTERS = (180, 500, 820)

tier1 = [("커스텀 요소", "custom elements"), ("섀도 DOM", "shadow DOM"), ("HTML 템플릿", "template · slot")]
tier2 = [("조각을 감싸는 컨테이너", "콜백 · 이벤트 · 속성"),
         ("스타일과 DOM 을 격리", "메인 문서와 따로 렌더"),
         ("표시되지 않는 마크업", "커스텀 요소 구조의 바탕")]
FOCAL = 1

LEGEND_Y = T2_Y + NH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-07",
      "웹 컴포넌트를 이루는 세 기술",
      "셋을 함께 쓰면 코드 충돌 없이 재사용되는 커스텀 요소를 만든다. 색이 붙은 것이 조각에 결정적이라고 저자가 적은 기술이다.",
      "위에서 아래로 읽습니다")

BUS_Y = ROOT_Y + NH + 26
d.line(500, ROOT_Y + NH, 500, BUS_Y, MUTED, 1.0)
d.line(CENTERS[0], BUS_Y, CENTERS[2], BUS_Y, MUTED, 1.0)
for cx in CENTERS:
    d.line(cx, BUS_Y, cx, T1_Y, MUTED, 1.0)
    d.line(cx, T1_Y + NH, cx, T2_Y, MUTED, 1.0)

d.box(500 - ROOT_W / 2, ROOT_Y, ROOT_W, NH, PAPER2, RULE, 1.0, 6)
d.t(500, ROOT_Y + 22, "웹 컴포넌트", 13.5, INK, KR, "middle", 600)
d.t(500, ROOT_Y + 39, "web platform APIs", 9, MUTED, MONO)

for i, (cx, (name, en)) in enumerate(zip(CENTERS, tier1)):
    if i == FOCAL:
        d.tone(cx - NW / 2, T1_Y, NW, NH, ACC, 6, "14", 1.4)
        d.t(cx, T1_Y + 22, name, 13, ACC, KR, "middle", 600)
        d.t(cx, T1_Y + 39, en, 9, ACC, MONO)
    else:
        d.box(cx - NW / 2, T1_Y, NW, NH, PAPER2, RULE, 1.0, 6)
        d.t(cx, T1_Y + 22, name, 13, INK, KR, "middle", 600)
        d.t(cx, T1_Y + 39, en, 9, MUTED, MONO)

for cx, (name, sub) in zip(CENTERS, tier2):
    d.box(cx - NW / 2, T2_Y, NW, NH, f"{INK}08", MUTED, 0.8, 6)
    d.t(cx, T2_Y + 22, name, 11.5, INK, KR, "middle", 600)
    d.t(cx, T2_Y + 39, sub, 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("조각에 결정적이라고 적은 기술", ACC)])
d.save("03-07.chapter-overview.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
