# 01-02 학습 목표 뒤 전체 지도 — 절 일곱을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 같은 폴더의 01-01 지도와 같은 문법을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-02",
      "일곱 원칙과 프론트엔드로의 번역 — 읽는 순서",
      "1장 후반부 노트의 절 일곱을 읽는 순서로 이은 지도. 원칙을 세우고 프론트엔드로 옮긴 뒤 고유 난제를 지나 적합성 판정으로 닫는다.",
      "앞 여섯 칸이 원칙을 옮기는 과정이고, 마지막 칸이 이 장의 결론입니다")

CW, CH, GAP, X0 = 272, 96, 24, 40          # stride = CW + GAP = 296
Y1, Y2 = 104, 248
cards = [
    ("§1", "원칙을 어디서 빌려 왔나", "2016년엔 가이드가 없었다"),
    ("§2", "마이크로서비스의 일곱 원칙", "Sam Newman이 정리한 축"),
    ("§3", "같은 일곱을 프론트엔드로", "그대로인 것과 비싸지는 것"),
    ("§4", "컴포넌트와 무엇이 다른가", "기술 문제 대 비즈니스 도메인"),
    ("§5", "실패 격리가 더 비싼 이유", "런타임 조합이 만드는 404·500"),
    ("§6", "이 아키텍처만의 난제 넷", "상태 · 라우팅 · 성능 · UX"),
    ("§7", "은탄환이 아니라는 말의 뜻", "적합한 네 상황과 그 밖"),
]

def pos(i):
    if i < 4: return X0 + i * (CW + GAP), Y1
    return X0 + (i - 4) * (CW + GAP), Y2

def card(i, focal=False):
    x, y = pos(i); n, title, q = cards[i]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, y + 52, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, y + 76, q, 12, MUTED, KR, "start")

for i in range(6):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:
        cx1, cx2 = x1 + CW / 2, x2 + CW / 2
        d.path(f"M {cx1} {y1 + CH} V 224 H {cx2} V {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(7):
    card(i, focal=(i == 6))

d.legend(376, [("이 장의 결론", ACC)])
d.save("01-02.chapter-overview.svg")
print("h 필요:", 376 + 22 + 16, " 실제:", H)
