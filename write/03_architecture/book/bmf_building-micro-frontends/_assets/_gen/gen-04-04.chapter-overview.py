# 04-04 학습 목표 뒤 전체 지도 — 절 넷을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 288
d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-04",
      "프로젝트가 자라는 순서",
      "만든 것을 지키는 이야기다. 레거시를 끌어안고 새 기능을 얹고, 그것을 어디에 두고 얼마나 캐시할지로 닫는다.",
      "앞 두 칸이 코드의 진화이고 뒤 두 칸이 그것을 서빙하는 방식입니다")

CW, CH, GAP, X0, Y = 280, 108, 24, 40, 104
cards = [
    ("§1", "레거시를 끌어안는다", "어댑터 조각이 iframe 을 감싼다"),
    ("§2", "장바구니를 얹는다", "컴포넌트가 자기 노출을 스스로 정한다"),
    ("§3", "어디에 둘 것인가", "스토리지와 CDN 세 조합"),
    ("§4", "얼마나 캐시할 것인가", "변화율에 따라 TTL 을 달리한다"),
]

def x_of(i): return X0 + i * (CW + GAP)

for i in range(3):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, q) in enumerate(cards):
    x = x_of(i)
    focal = (i == 0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 28, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 56, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 82, q, 11.5, MUTED, KR, "start")

d.legend(Y + CH + 32, [("어댑터 패턴이 들어오는 자리", ACC)])
d.save("04-04.chapter-overview.svg")
print("h:", Y + CH + 32 + 40, "/", H)
