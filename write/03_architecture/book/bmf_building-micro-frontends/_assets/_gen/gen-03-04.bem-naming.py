# 03-04 §4 — 클래스 이름이 조립되는 단계. 저자가 든 아바타 예제 그대로다.
# 마지막 단계(조각 이름 접두)만 저자가 BEM 위에 얹으라고 추가한 것이므로 거기에 accent 를 준다.
# 타입 스펙: type-process — 단계마다 같은 의미 슬롯(무엇을 더하나 · 결과 이름)이 반복되고 화살표가 순서를 나른다.
#           축약: 주체(lane)가 없는 단계 지도라 lanes 공식을 쓰지 않고 카드 한 줄 stride 로 놓는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
CW, CH, GAP, X0, Y = 280, 128, 24, 40, 112
LEGEND_Y = Y + CH + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-04 §4",
      "클래스 이름이 조립되는 네 단계",
      "BEM 이 앞의 세 단계를 만들고, 저자가 조각 이름 접두를 하나 더 얹는다. 이름이 길어지는 대신 격리가 보장된다.",
      "왼쪽에서 오른쪽으로 갈수록 이름이 길어집니다")

steps = [
    ("01", "블록", "뷰의 한 요소", ".avatar", False),
    ("02", "요소", "블록의 특정 부분", ".avatar__image", False),
    ("03", "수식자", "표시할 상태", ".avatar__image--active", False),
    ("04", "조각 이름 접두", "BEM 위에 저자가 얹은 것", ".myaccount_avatar__image--active", True),
]

def x_of(i): return X0 + i * (CW + GAP)

for i in range(3):
    d.arrow([(x_of(i) + CW, Y + CH / 2), (x_of(i + 1) - 2, Y + CH / 2)], MUTED, "ar", 1.4)

for i, (n, name, sub, css, focal) in enumerate(steps):
    x = x_of(i)
    if focal:
        d.tone(x, Y, CW, CH, ACC, 8, "12", 1.4)
    else:
        d.box(x, Y, CW, CH, PAPER2, RULE, 1.0, 8)
    d.t(x + 16, Y + 26, n, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 16, Y + 52, name, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 16, Y + 74, sub, 10.5, MUTED, KR, "start")
    d.t(x + 16, Y + 106, css, 9.5, ACC if focal else INK, MONO, "start")

d.legend(LEGEND_Y, [("BEM 만으로 모자라 저자가 더한 단계", ACC)])
d.save("03-04.bem-naming.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
