# 03-03 §1 — fact_sales 가 가운데, dimension 이 누가·무엇·어디·언제로 둘러싸는 별 모양. 본문에 나온 이름만 쓴다.
# 옛 도식의 눈송이·OBT 변형은 뺐다. §2·§3 본문이 맡는다.
# 타입 스펙: type-er
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 316
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-03 · STAR SCHEMA", "별 스키마의 fact 와 dimension",
      "fact_sales 한 행은 구매 한 건을 담고, 외래 키로 누가·무엇·어디·언제를 설명하는 dimension 테이블 넷에 연결된다.",
      "중앙 fact 와 둘러싼 dimension")
d.box(16, PY, 848, PH, PAPER, RULE, 0.9)

# 중앙 fact
d.box(320, 204, 240, 100, PAPER2, ACC, 1.4)
d.t(440, 232, "fact_sales", 14, INK, MONO, "middle", 600)
d.t(440, 256, "이벤트 한 행 · 구매 한 건", 12, MUTED, KR)
d.t(440, 280, "속성 — 가격 · 원가", 12, MUTED, KR)

# dimension 넷: 좌 무엇, 우 언제, 위 누가, 아래 어디
d.box(32, 218, 216, 72, PAPER2, INFO, 1.2)
d.t(140, 244, "dim_product", 13, INK, MONO, "middle", 600)
d.t(140, 268, "무엇 · SKU · 브랜드 · 카테고리", 12, MUTED, KR)
d.box(632, 218, 216, 72, PAPER2, INFO, 1.2)
d.t(740, 244, "날짜 dimension", 13, INK, KR, "middle", 600)
d.t(740, 268, "언제 · 공휴일 등 추가 정보", 12, MUTED, KR)
d.box(320, 112, 240, 56, PAPER2, INFO, 1.2)
d.t(440, 136, "dimension 테이블", 13, INK, KR, "middle", 600)
d.t(440, 156, "누가", 12, MUTED, KR)
d.box(320, 352, 240, 56, PAPER2, INFO, 1.2)
d.t(440, 376, "dimension 테이블", 13, INK, KR, "middle", 600)
d.t(440, 396, "어디", 12, MUTED, KR)

# 외래 키 — fact 에서 dimension 으로
d.arrow([(316, 254), (252, 254)], MUTED, "ar", 1.4)
d.arrow([(564, 254), (628, 254)], MUTED, "ar", 1.4)
d.arrow([(440, 200), (440, 172)], MUTED, "ar", 1.4)
d.arrow([(440, 308), (440, 348)], MUTED, "ar", 1.4)
d.t(284, 244, "FK", 11, MUTED, MONO)
d.t(596, 244, "FK", 11, MUTED, MONO)
d.t(456, 190, "FK", 11, MUTED, MONO, "start")
d.t(456, 332, "FK", 11, MUTED, MONO, "start")

d.legend(LEG, [("핵심 — fact 테이블", ACC), ("dimension 테이블", INFO)])
d.save("03-03.star-schema.svg")
