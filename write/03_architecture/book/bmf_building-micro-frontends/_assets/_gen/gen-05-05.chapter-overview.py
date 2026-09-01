# 05-05 학습 목표 뒤 전체 지도 — 절 넷을 읽는 순서로 잇는다.
# 타입 스펙: type-process — 절마다 같은 의미 슬롯(번호 · 이름 · 질문)이 반복되고 화살표가 읽는 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 §1 lanes 와 §2 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다
#           (visual-diagram-selection §알려진 공백 "주체 없는 단계 지도" 관례).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 288
d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-05",
      "5 장을 닫는 네 절",
      "데이터가 어디서 오는지에서 출발해 그것을 어떻게 캐시할지로 가고, BBC 의 실제 배치를 본 뒤 성능을 재는 방법으로 닫는다.",
      "앞 세 칸이 견디는 법이고 색이 붙은 마지막 칸이 그것을 확인하는 법입니다")

CW, CH, GAP, X0, Y = 280, 108, 24, 40, 104
cards = [
    ("§1", "데이터는 어디서 오나", "GraphQL 단일 그래프 · REST 는 BFF"),
    ("§2", "캐시를 세 종류로 안다", "CDN · 인메모리 · 웜 캐시"),
    ("§3", "BBC 는 층마다 캐시한다", "CDN 부터 서비스 게이트웨이까지"),
    ("§4", "성능은 재야 지켜진다", "부분 하이드레이션 · 예산 · RUM"),
]

def x_of(i): return X0 + i * (CW + GAP)

for i in range(3):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, title, q) in enumerate(cards):
    x = x_of(i)
    focal = (i == 3)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{CW}" height="{CH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 28, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 56, title, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 82, q, 11.5, MUTED, KR, "start")

d.legend(Y + CH + 32, [("끝나지 않는 순환", ACC)])
d.save("05-05.chapter-overview.svg")
print("h:", Y + CH + 32 + 40, "/", H)
