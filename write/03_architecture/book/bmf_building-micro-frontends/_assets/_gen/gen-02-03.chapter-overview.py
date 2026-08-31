# 02-03 학습 목표 뒤 전체 지도 — 절 다섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례). 이 폴더의 다른 전체 지도와 같은 문법이다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-03",
      "합치고 잇고 주고받기 — 읽는 순서",
      "2장 후반 노트의 절 다섯. 남은 세 결정을 조합·라우팅·통신 순으로 짚고 네 결정의 조합표로 닫는다.",
      "앞 네 칸이 남은 세 결정을 짚고, 마지막 칸이 넷을 한 표로 모읍니다")

CW, CH, GAP, X0 = 368, 96, 24, 40
Y1, Y2 = 104, 248
cards = [
    ("§1", "어디서 합칠 것인가", "클라이언트 · 엣지 · 오리진"),
    ("§2", "어디서 고를 것인가", "라우팅은 조합에 매인다"),
    ("§3", "전역 상태를 쓰고 싶은 유혹", "분산 시스템의 안티패턴"),
    ("§4", "알림과 데이터를 나누는 법", "이벤트 버스 · 커스텀 이벤트"),
    ("§5", "네 결정이 만드는 조합표", "수평과 수직이 여는 선택지"),
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

d.legend(376, [("이 편의 도착점", ACC)])
d.save("02-03.chapter-overview.svg")
print("h:", 376 + 40, "/", H)
