# 03-09 학습 목표 뒤 전체 지도 — 절 다섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 이 폴더의 다른 전체 지도와 같은 문법이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-09",
      "3장의 마지막 다섯 절 — 읽는 순서",
      "모던 SSR 프레임워크 넷에서 출발해 엣지가 왜 아직 자리를 잡지 못했는지 보고, 3장 전체의 결론으로 닫는다.",
      "앞 네 칸이 기술을 훑고, 색이 붙은 마지막 칸이 3장의 결론입니다")

CW, CH, GAP, X0 = 368, 96, 24, 40
Y1, Y2 = 104, 248
cards = [
    ("§1", "네 프레임워크가 고른 길", "서버 아일랜드 · 재개 · 멀티 존 · htmx"),
    ("§2", "여덟 축 점수", "단순성 · 성능 · 개발자 경험이 5점"),
    ("§3", "엣지에서 왜 렌더하지 않나", "데이터 중력과 런타임 제약"),
    ("§4", "ESI 가 하던 일", "엣지에서 태그로 조립하던 방식"),
    ("§5", "3장을 닫으며", "완벽한 아키텍처 대신 덜 나쁜 것"),
]

def pos(i):
    if i < 3: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 3) * (CW + GAP), Y2

def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, q, 12, MUTED, KR, "start")

for i in range(4):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cx1, cx2 = x1 + CW / 2, x2 + CW / 2
        d.path(f"M {cx1} {y1 + CH} V 224 H {cx2} V {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(5):
    card(i, focal=(i == 4))

d.legend(376, [("3장 전체의 결론", ACC)])
d.save("03-09.chapter-overview.svg")
print("h:", 376 + 40, "/", H)
