# 03-03 §2 — 눈송이 스키마에서 dimension이 subdimension으로 더 쪼개지는 다대일(N:1) 계층 구조를 그린다.
# 사실 출처: 본문 §2(dim_product 가 brand·category 를 외래 키로 참조, 다대일 관계)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
T1_X, T1_W = 28, 220
T2_X, T2_W = 308, 236
T3_X, T3_W = 604, 244

TIER_Y = PY
BOX_Y1 = 152
BOX_Y2 = 148
BOX_Y3A = 132
BOX_Y3B = 260

COMP_Y = 384
COMP_H = 40
LEG = COMP_Y + COMP_H + 20
H = LEG + 56

d = D(W, H, "03-03 · SNOWFLAKE SCHEMA", "눈송이 스키마의 subdimension 분해",
      "눈송이 스키마는 dimension 테이블의 컬럼을 subdimension 테이블로 더 정규화해 외래 키 다대일(N:1) 관계로 쪼갠다.",
      "dimension 에서 subdimension 으로 이어지는 계층 구조")

# 상단 단계 표시 바
for x, w, label, color in [
    (T1_X, T1_W, "1단계 · 중앙 fact", SOFT),
    (T2_X, T2_W, "2단계 · dimension (focal)", ACC),
    (T3_X, T3_W, "3단계 · subdimension", INFO),
]:
    d.box(x, TIER_Y, w, 28, PAPER2, RULE, 0.9)
    d.t(x + w / 2, TIER_Y + 18, label, 12, color, KR, "middle", 600)

# 1단계: fact_sales
d.box(T1_X, BOX_Y1, T1_W, 196, PAPER2, RULE, 1.0)
d.t(T1_X + T1_W / 2, BOX_Y1 + 26, "fact_sales", 14, INK, MONO, "middle", 600)
d.t(T1_X + T1_W / 2, BOX_Y1 + 46, "이벤트 한 행 · 구매 기록", 12, MUTED, KR, "middle")
d.line(T1_X + 12, BOX_Y1 + 58, T1_X + T1_W - 12, BOX_Y1 + 58, RULE, 0.8)
d.t(T1_X + 16, BOX_Y1 + 78, "→ date_key (FK)", 12, MUTED, MONO, "start")
d.t(T1_X + 16, BOX_Y1 + 102, "→ product_sk (FK)", 12, ACC, MONO, "start", 600)
d.t(T1_X + 16, BOX_Y1 + 126, "→ store_sk (FK)", 12, MUTED, MONO, "start")
d.t(T1_X + 16, BOX_Y1 + 150, "속성: price · cost", 12, MUTED, KR, "start")
d.t(T1_X + 16, BOX_Y1 + 174, "구매 상품마다 한 행", 11, MUTED, KR, "start")

# 2단계: dim_product (focal)
d.tone(T2_X, BOX_Y2, T2_W, 204, ACC, 6, "14", 1.4)
d.t(T2_X + T2_W / 2, BOX_Y2 + 26, "dim_product", 14, INK, MONO, "middle", 600)
d.t(T2_X + T2_W / 2, BOX_Y2 + 46, "상품 dimension · 분기점", 12, ACC, KR, "middle")
d.line(T2_X + 12, BOX_Y2 + 58, T2_X + T2_W - 12, BOX_Y2 + 58, RULE, 0.8)
d.t(T2_X + 16, BOX_Y2 + 78, "# product_sk (PK)", 12, SOFT, MONO, "start")
d.t(T2_X + 16, BOX_Y2 + 102, "속성: sku · desc · size", 12, MUTED, MONO, "start")
d.t(T2_X + 16, BOX_Y2 + 126, "→ brand_sk (FK)", 12, INFO, MONO, "start", 600)
d.t(T2_X + 16, BOX_Y2 + 150, "→ category_sk (FK)", 12, INFO, MONO, "start", 600)
d.t(T2_X + 16, BOX_Y2 + 180, "문자열 대신 외래 키로 참조", 11, ACC, KR, "start", 600)

# 3단계: subdimension 둘 (dim_brand, dim_category)
# dim_brand
d.box(T3_X, BOX_Y3A, T3_W, 108, PAPER2, INFO, 1.2)
d.t(T3_X + T3_W / 2, BOX_Y3A + 24, "dim_brand", 14, INK, MONO, "middle", 600)
d.t(T3_X + T3_W / 2, BOX_Y3A + 44, "브랜드 subdimension", 12, INFO, KR, "middle")
d.line(T3_X + 12, BOX_Y3A + 54, T3_X + T3_W - 12, BOX_Y3A + 54, RULE, 0.8)
d.t(T3_X + 16, BOX_Y3A + 74, "# brand_sk (PK)", 12, SOFT, MONO, "start")
d.t(T3_X + 16, BOX_Y3A + 94, "속성: brand_name", 12, INK, MONO, "start")

# dim_category
d.box(T3_X, BOX_Y3B, T3_W, 108, PAPER2, INFO, 1.2)
d.t(T3_X + T3_W / 2, BOX_Y3B + 24, "dim_category", 14, INK, MONO, "middle", 600)
d.t(T3_X + T3_W / 2, BOX_Y3B + 44, "카테고리 subdimension", 12, INFO, KR, "middle")
d.line(T3_X + 12, BOX_Y3B + 54, T3_X + T3_W - 12, BOX_Y3B + 54, RULE, 0.8)
d.t(T3_X + 16, BOX_Y3B + 74, "# category_sk (PK)", 12, SOFT, MONO, "start")
d.t(T3_X + 16, BOX_Y3B + 94, "속성: category_name", 12, INK, MONO, "start")

# 연결선 1: fact -> dim_product (N:1)
d.arrow([(T1_X + T1_W, BOX_Y1 + 98), (T2_X - 4, BOX_Y1 + 98)], MUTED, "ar", 1.4)
d.chip((T1_X + T1_W + T2_X) / 2, BOX_Y1 + 86, "N:1", MUTED, 11)

# 연결선 2: dim_product -> subdimensions (N:1)
# brand_sk 경로: (T2_X + T2_W, BOX_Y2 + 122) -> (T3_X, BOX_Y3A + 70)
d.arrow([(T2_X + T2_W, BOX_Y2 + 122), (T2_X + T2_W + 32, BOX_Y2 + 122),
         (T2_X + T2_W + 32, BOX_Y3A + 70), (T3_X - 4, BOX_Y3A + 70)], INFO, "info", 1.4)
d.chip(T2_X + T2_W + 32, (BOX_Y2 + 122 + BOX_Y3A + 70) / 2, "N:1", INFO, 10)

# category_sk 경로: (T2_X + T2_W, BOX_Y2 + 146) -> (T3_X, BOX_Y3B + 70)
d.arrow([(T2_X + T2_W, BOX_Y2 + 146), (T2_X + T2_W + 32, BOX_Y2 + 146),
         (T2_X + T2_W + 32, BOX_Y3B + 70), (T3_X - 4, BOX_Y3B + 70)], INFO, "info", 1.4)
d.chip(T2_X + T2_W + 32, (BOX_Y2 + 146 + BOX_Y3B + 70) / 2, "N:1", INFO, 10)

# 하단 비교 설명 바
d.box(T1_X, COMP_Y, W - T1_X * 2, COMP_H, PAPER2, RULE, 0.9)
d.t(T1_X + 20, COMP_Y + 24, "별 스키마와 차이", 12, ACC, KR, "start", 600)
d.t(T1_X + 132, COMP_Y + 24, "별 스키마는 브랜드·카테고리를 문자열로 보관 · 눈송이는 subdimension 외래 키로 분리 정규화", 12, MUTED, KR, "start")

d.legend(LEG, [("dimension 분기점 (focal)", ACC), ("subdimension 테이블", INFO), ("fact 테이블", SOFT)])
d.save("03-03.snowflake-schema.svg")
