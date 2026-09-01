# 04-03 §2 — 카탈로그 조각 안의 지역 라우팅. 저자의 Catalog 컴포넌트 코드가 productId 유무로 갈리는 그대로다.
# 셸은 1 단계 경로까지만 알고, 그 아래는 이 조각이 스스로 관리한다.
# 타입 스펙: type-state — 유한한 상태와 그 사이 전이. accent 는 독자가 알아채야 할 상태 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1200
SW, SH, SY = 300, 72, 184
XS = (250, 750)
MY = SY + SH / 2
BACK_Y = SY + SH + 76
LEGEND_Y = BACK_Y + 52
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-03 §2",
      "productId 하나가 뷰를 가른다",
      "셸이 /catalog 까지 데려다 놓으면 그다음은 이 조각의 몫이다. 색이 붙은 상태가 셸이 존재조차 모르는 자리다.",
      "화살표 위 글이 그 전이를 일으키는 방아쇠입니다")

# 시작점 — 셸이 넘겨주는 지점
d.o.append(f'<circle cx="86" cy="{MY}" r="6" fill="{INK}"/>')
d.arrow([(94, MY), (XS[0] - 2, MY)], MUTED, "ar", 1.4)
d.t(96, MY - 14, "셸이 /catalog 로 라우팅", 9.5, MUTED, KR, "start")

d.arrow([(XS[0] + SW, MY), (XS[1] - 2, MY)], ACC, "acc", 1.5)
d.t((XS[0] + SW + XS[1]) / 2, MY - 24, "타일 선택", 10, ACC, KR)
d.t((XS[0] + SW + XS[1]) / 2, MY - 8, "navigate(`/catalog/${productId}`)", 9, ACC, MONO)
d.path(f"M {XS[1] + SW / 2} {SY + SH} V {BACK_Y} H {XS[0] + SW / 2} V {SY + SH + 2}", MUTED, 1.4, m="ar")
d.t((XS[0] + XS[1]) / 2 + SW / 2, BACK_Y + 20, "뒤로 가면 productId 가 사라진다", 10, MUTED, KR)

states = [
    ("카탈로그 목록", "productId 가 없다", False),
    ("상품 상세", "productId 가 있다", True),
]
for x, (name, sub, focal) in zip(XS, states):
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "14", 1.4)
        d.t(x + SW / 2, SY + 30, name, 15, ACC, KR, "middle", 600)
        d.t(x + SW / 2, SY + 52, sub, 10, ACC, MONO)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
        d.t(x + SW / 2, SY + 30, name, 15, INK, KR, "middle", 600)
        d.t(x + SW / 2, SY + 52, sub, 10, MUTED, MONO)

d.legend(LEGEND_Y, [("셸이 존재조차 모르는 상태", ACC)])
d.save("04-03.catalog-routing.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
