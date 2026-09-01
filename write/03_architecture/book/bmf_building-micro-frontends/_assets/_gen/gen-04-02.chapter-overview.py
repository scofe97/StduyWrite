# 04-02 학습 목표 뒤 전체 지도 — 절 다섯을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 432
d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-02",
      "애플리케이션 셸을 읽는 순서",
      "셸이 지는 책임에서 출발해 공유 의존성과 부팅과 인증을 지나, 리모트를 런타임에 등록하는 데서 닫는다.",
      "앞 네 칸이 셸이 하는 일이고 색이 붙은 마지막 칸이 그것을 묶는 장치입니다")

CW, CH, GAP, X0 = 368, 96, 24, 40
Y1, Y2 = 104, 248
cards = [
    ("§1", "셸이 지는 책임 넷", "도메인 누출 방지가 첫 줄에 온다"),
    ("§2", "무엇을 공유로 선언하나", "singleton · requiredVersion · shareScope"),
    ("§3", "왜 파일을 셋으로 쪼개나", "동기 로드를 피해 TTFB · TTI 를 지킨다"),
    ("§4", "인증을 셸이 대신할 때", "fetch 를 갈아 끼우는 값"),
    ("§5", "리모트를 런타임에 등록", "디스커버리 JSON 에서 라우트를 만든다"),
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

d.legend(376, [("셸을 도메인 무지 상태로 두는 장치", ACC)])
d.save("04-02.chapter-overview.svg")
print("h:", 376 + 40, "/", H)
