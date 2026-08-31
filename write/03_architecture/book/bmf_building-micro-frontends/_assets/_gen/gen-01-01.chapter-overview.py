# 01-01 학습 목표 뒤 전체 지도 — 절 여섯을 읽는 순서로 잇는다.
# 본문이 "칸마다 절 번호와 그 절이 답하는 질문 하나", "색이 붙은 마지막 칸이 이 편의 도착점"이라고 못 박는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 데이터 칩도 없다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 01-01",
      "모놀리스에서 분산 프론트엔드까지 — 읽는 순서",
      "1장 전반부 노트의 절 여섯을 읽는 순서로 이은 지도. 모놀리스가 옳았던 자리에서 출발해 백엔드만 쪼개진 이유를 지나 마이크로 프론트엔드의 정의로 닫는다.",
      "앞 다섯 칸은 왜 여기까지 왔는지를 잇고, 마지막 칸이 마이크로 프론트엔드의 정의로 닫습니다")

CW, CH, GAP, X0 = 368, 96, 24, 40          # stride = CW + GAP = 392
Y1, Y2 = 104, 248                          # 두 줄. 사이 corridor 224
cards = [
    ("§1", "모놀리스로 시작하는 것이 옳은 이유", "파이프라인 하나 · 관측 에이전트 하나"),
    ("§2", "성공이 만들어 낸 압력", "팀이 늘고 API마다 확장 성격이 갈린다"),
    ("§3", "마이크로서비스가 푼 것과 만든 것", "인지 부하 대 자동화 · 관측 투자"),
    ("§4", "세 세대 — 무엇이 쪼개졌나", "presentation 층만 통짜로 남았다"),
    ("§5", "프론트엔드는 왜 그대로 남았나", "재사용 중심 해법이 못 준 것"),
    ("§6", "마이크로 프론트엔드란 무엇인가", "독립 배포되는 비즈니스 도메인 조각"),
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
    card(i, focal=(i == 5))

d.legend(376, [("이 편의 도착점", ACC)])
d.save("01-01.chapter-overview.svg")
print("h 필요:", 376 + 22 + 16, " 실제:", H)
