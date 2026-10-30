# 04-05 §5 — 2차원 데이터 큐브(data cube) 집계 격자와 차원별 소계 및 유연성 트레이드오프.
# 사실 출처: 본문 §5(L79~L88), DDIA Figure 4-10(Two dimensions of a data cube, aggregating data by summing). 셀·소계는 원서 값 그대로(소계는 원서가 생략한 칸까지 합한 값). 2026-10-30 검증에서 지어낸 날짜·카테고리·수치와 O(1) 를 교체
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
LEG = 412
H = LEG + 56

d = D(W, H, "04-05 · DATA CUBE", "2차원 데이터 큐브(OLAP Cube) 집계 격자",
      "date_key와 product_sk 두 차원의 교차 집계를 미리 계산해 셀 및 행·열 소계를 즉시 조회하지만 비포함 속성 질의에는 원본 유지가 필수적이다.",
      "날짜 축 · 상품 축 · 사전 계산 SUM · 행/열 1차원 요약 · 질의 유연성 제약")

X0 = 24
BOX_W = 832

# 큐브 본체 패널
CUBE_Y = PY
CUBE_H = 206
d.box(X0, CUBE_Y, BOX_W, CUBE_H, PAPER2, RULE, 0.9)
d.chip(X0 + 44, CUBE_Y + 20, "2D 큐브", ACC, 11)
d.t(X0 + 94, CUBE_Y + 24, "날짜 × 상품 2차원 집계 격자 (SUM(net_price))", 13, INK, KR, "start", 600)
d.t(X0 + BOX_W - 20, CUBE_Y + 24, "소계는 표에 없는 칸까지 합한 원서 값", 11.5, SOFT, KR, "end")
d.line(X0 + 12, CUBE_Y + 36, X0 + BOX_W - 12, CUBE_Y + 36, RULE, 0.8)

# 격자 컬럼 구성: [구분/date_key, Fresh fruit, Candy, Bakery, Dairy, 일자별 소계]
COLS = [
    ("date_key 축", 130),
    ("product_sk 32", 126),
    ("product_sk 33", 126),
    ("product_sk 34", 126),
    ("product_sk 35", 126),
    ("일자별 소계", 150),
]

GRID_X0 = X0 + 20
GRID_Y0 = CUBE_Y + 44
CELL_H = 24

# 헤더 행
cx_cur = GRID_X0
for c_title, c_w in COLS:
    d.box(cx_cur, GRID_Y0, c_w, CELL_H, PAPER, RULE, 0.8)
    is_sub = ("소계" in c_title)
    is_axis = ("축" in c_title)
    d.t(cx_cur + c_w / 2, GRID_Y0 + 16, c_title, 11.5, INFO if is_sub else (SOFT if is_axis else INK), KR, "middle", 600)
    cx_cur += c_w + 4

# 데이터 행 4개
ROWS = [
    ("260101", ["149.60", "31.01", "84.58", "28.18"], "40710.53"),
    ("260102", ["132.18", "19.78", "82.91", "10.96"], "73091.28"),
    ("260103", ["196.75", "0.00", "12.52", "64.67"], "54688.10"),
    ("260104", ["178.36", "9.98", "88.75", "56.16"], "95121.09"),
]

for r_idx, (r_date, r_vals, r_sub) in enumerate(ROWS):
    ry = GRID_Y0 + (r_idx + 1) * (CELL_H + 3)
    cx_cur = GRID_X0
    
    # date_key 레이블
    d.box(cx_cur, ry, COLS[0][1], CELL_H, PAPER, RULE, 0.8)
    d.t(cx_cur + COLS[0][1] / 2, ry + 16, r_date, 11, SOFT, MONO, "middle", 600)
    cx_cur += COLS[0][1] + 4
    
    # 4개 카테고리 셀 (OK 톤)
    for v_idx, val in enumerate(r_vals):
        c_w = COLS[v_idx + 1][1]
        is_focal_cell = (r_idx == 0 and v_idx == 0) # 260101 · 32 강조 (원서 말풍선)
        cell_fill = OK if is_focal_cell else PAPER
        d.box(cx_cur, ry, c_w, CELL_H, cell_fill, OK if is_focal_cell else RULE, 1.2 if is_focal_cell else 0.8)
        d.t(cx_cur + c_w / 2, ry + 16, val, 11.5, INK if is_focal_cell else OK, MONO, "middle", 600)
        cx_cur += c_w + 4
        
    # 일자별 소계 (INFO 톤)
    sub_w = COLS[5][1]
    d.tone(cx_cur, ry, sub_w, CELL_H, INFO, 4, "16", 1.0)
    d.t(cx_cur + sub_w / 2, ry + 16, f"SUM: {r_sub}", 11.5, INFO, MONO, "middle", 600)

# 최하단: 상품별 소계 및 전체 총합 행
ry_tot = GRID_Y0 + 5 * (CELL_H + 3)
cx_cur = GRID_X0

d.box(cx_cur, ry_tot, COLS[0][1], CELL_H, PAPER, RULE, 0.8)
d.t(cx_cur + COLS[0][1] / 2, ry_tot + 16, "상품별 소계", 11.5, INFO, KR, "middle", 600)
cx_cur += COLS[0][1] + 4

cat_totals = ["14967.09", "5910.43", "7328.85", "6885.39"]
for v_idx, tot in enumerate(cat_totals):
    c_w = COLS[v_idx + 1][1]
    d.tone(cx_cur, ry_tot, c_w, CELL_H, INFO, 4, "16", 1.0)
    d.t(cx_cur + c_w / 2, ry_tot + 16, f"SUM: {tot}", 11.5, INFO, MONO, "middle", 600)
    cx_cur += c_w + 4

# 우하단 전체 총합 셀 (ACC 톤)
grand_w = COLS[5][1]
d.tone(cx_cur, ry_tot, grand_w, CELL_H, ACC, 6, "22", 1.4)
d.t(cx_cur + grand_w / 2, ry_tot + 16, "총합: …", 12, ACC, MONO, "middle", 600)

# 하단: 장점과 유연성 한계 트레이드오프 패널
TR_Y = CUBE_Y + CUBE_H + 12
TR_H = 74
d.box(X0, TR_Y, BOX_W, TR_H, PAPER2, RULE, 0.9)
d.chip(X0 + 52, TR_Y + 20, "트레이드오프", WARN, 11)
d.t(X0 + 116, TR_Y + 24, "데이터 큐브의 성능 이점과 질의 유연성 제약", 13, INK, KR, "start", 600)
d.line(X0 + 12, TR_Y + 36, X0 + BOX_W - 12, TR_Y + 36, RULE, 0.8)

d.t(X0 + 24, TR_Y + 54, "장점: 특정 쿼리는 미리 계산돼 원본 fact 를 훑지 않아 크게 빨라짐", 11.5, OK, KR, "start")
d.t(X0 + 24, TR_Y + 67, "한계: price 등 비차원 속성 조건(price > $100) 계산 불가 · 대부분 웨어하우스는 원본 유지 후 큐브는 보조 활용", 11.5, WARN, KR, "start")

d.legend(LEG, [("2차원 셀 집계 (강조 포함)", OK), ("1차원 축별 소계 요약", INFO), ("2차원 전체 총합", ACC), ("질의 유연성 제약", WARN)])
d.save("04-05.data-cube.svg")
