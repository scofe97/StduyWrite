# 06-01 학습 목표 뒤 전체 지도 — 저자가 든 자동화 원칙 다섯을 읽는 순서로 잇는다.
# 색이 붙은 칸은 마지막이 아니라 §4 다. 이 편이 매달린 주장이 "한 번 정하고 끝나지 않는다"이기 때문이다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 요약)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). stride 는 01-01 의 것을 승계한다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-01",
      "자동화 원칙 다섯 — 읽는 순서",
      "6장 전반부 노트의 절 여섯을 읽는 순서로 이은 지도. 조각이 늘어 파이프라인이 막히는 자리에서 출발해 테스트 전략을 세우는 데서 멈춘다.",
      "앞 세 칸이 속도의 문제이고 뒤 세 칸이 사람과 경계의 문제입니다")

CW, CH, GAP, X0 = 368, 96, 24, 40          # stride = CW + GAP = 392 (01-01 승계)
Y1, Y2 = 104, 248                          # 두 줄. 사이 corridor 224
cards = [
    ("§1", "파이프라인이 먼저 막힌다", "수평 분할이면 아티팩트가 수십에서 수백"),
    ("§2", "어디까지 자동인가", "통합 · 전달 · 배포가 멈추는 자리가 다르다"),
    ("§3", "피드백 루프를 빠르게", "초 단위 · 병렬과 직렬을 가른다"),
    ("§4", "한 번 정하고 끝나지 않는다", "8~10분이 재검토 신호다"),
    ("§5", "권한과 가드레일", "도구는 플랫폼 팀 · 스크립트는 개발 팀"),
    ("§6", "테스트 전략을 먼저", "선별적이고 빠르게 · E2E 만 달라진다"),
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

# 연결선을 먼저 — z-order
for i in range(5):
    x1, y1 = pos(i); x2, y2 = pos(i + 1)
    if y1 == y2:
        d.arrow([(x1 + CW, y1 + CH / 2), (x2 - 2, y2 + CH / 2)], MUTED, "ar", 1.4)
    else:   # 줄바꿈: 아래로 → corridor → 왼쪽 → 아래로
        cx1, cx2 = x1 + CW / 2, x2 + CW / 2
        d.path(f"M {cx1} {y1 + CH} V 224 H {cx2} V {y2 - 2}", MUTED, 1.4, m="ar")
for i in range(6):
    card(i, focal=(i == 3))

d.legend(376, [("이 편이 매달린 주장", ACC)])
d.save("06-01.chapter-overview.svg")
print("h 필요:", 376 + 22 + 16, " 실제:", H)
