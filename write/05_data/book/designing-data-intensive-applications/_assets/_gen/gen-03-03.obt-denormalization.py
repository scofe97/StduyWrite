# 03-03 §3 — fact 테이블과 dimension 테이블이 비정규화 조인 사전 계산을 거쳐 하나의 넓은 테이블(OBT)로 펼쳐지는 데이터 흐름을 그린다.
# 사실 출처: 본문 §3(dimension 정보를 fact 에 접어 넣음, 사전 계산 조인), 컬럼명·행 예시는 책 그림 3-5
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 104
T1_X, T1_W = 28, 216
T2_X, T2_W = 308, 156
T3_X, T3_W = 516, 336

TIER_Y = PY
B1_Y = 148
B2_Y = 196
B3_Y = 148

COMP_Y = 412
COMP_H = 40
LEG = COMP_Y + COMP_H + 20
H = LEG + 56

d = D(W, H, "03-03 · OBT DENORMALIZATION", "OBT의 조인 사전 계산과 비정규화",
      "OBT는 별도의 dimension 테이블 없이 모든 메타데이터를 fact 행에 접어 넣어 조인을 사전 계산하는 단일 넓은 테이블이다.",
      "원천 테이블에서 OBT로의 데이터 흐름")

# 상단 단계 표시 바
for x, w, label, color in [
    (T1_X, T1_W, "1단계 · 원천 테이블 (별 스키마)", INFO),
    (T2_X, T2_W, "2단계 · 사전 계산", SOFT),
    (T3_X, T3_W, "3단계 · One Big Table (focal)", ACC),
]:
    d.box(x, TIER_Y, w, 28, PAPER2, RULE, 0.9)
    d.t(x + w / 2, TIER_Y + 18, label, 12, color, KR, "middle", 600)

# 1단계: 원천 fact 및 dimension 넷
boxes1 = [
    ("fact_sales (이벤트)", "quantity · net_price", 148, 56, INFO),
    ("dim_product (상품)", "sku · brand · category", 216, 52, RULE),
    ("dim_store (매장)", "state · city", 280, 52, RULE),
    ("dim_date (날짜)", "date_key · is_holiday", 344, 52, RULE),
]
for title, sub, y, bh, stroke in boxes1:
    d.box(T1_X, y, T1_W, bh, PAPER2, stroke, 1.0)
    d.t(T1_X + 16, y + 22, title, 13, INK, KR if "이벤트" in title or "상품" in title or "매장" in title or "날짜" in title else MONO, "start", 600)
    d.t(T1_X + 16, y + 42, sub, 12, MUTED, MONO, "start")

# 2단계: 조인 사전 계산 (ETL)
d.box(T2_X, B2_Y, T2_W, 160, PAPER2, RULE, 1.0)
d.t(T2_X + T2_W / 2, B2_Y + 26, "조인 사전 계산", 14, INK, KR, "middle", 600)
d.t(T2_X + T2_W / 2, B2_Y + 46, "Precomputed Join", 12, SOFT, MONO, "middle")
d.line(T2_X + 12, B2_Y + 58, T2_X + T2_W - 12, B2_Y + 58, RULE, 0.8)
d.t(T2_X + 16, B2_Y + 80, "외래 키(FK) 참조 해소", 12, INK, KR, "start")
d.t(T2_X + 16, B2_Y + 104, "dimension 메타 병합", 12, INK, KR, "start")
d.t(T2_X + 16, B2_Y + 128, "단일 넓은 행으로 전개", 12, INK, KR, "start")
d.t(T2_X + 16, B2_Y + 148, "ETL 이 변환해 적재", 11, MUTED, KR, "start")

# 3단계: OBT (focal)
d.tone(T3_X, B3_Y, T3_W, 248, ACC, 6, "14", 1.4)
d.t(T3_X + T3_W / 2, B3_Y + 28, "one_big_table (OBT)", 15, INK, MONO, "middle", 600)
d.t(T3_X + T3_W / 2, B3_Y + 50, "단일 넓은 비정규화 테이블", 12, ACC, KR, "middle")
d.line(T3_X + 16, B3_Y + 62, T3_X + T3_W - 16, B3_Y + 62, RULE, 0.8)

# 병합된 컬럼 구조 박스
d.box(T3_X + 16, B3_Y + 74, T3_W - 32, 44, PAPER, RULE, 0.9)
d.t(T3_X + 24, B3_Y + 92, "병합 컬럼 구성", 11, SOFT, KR, "start", 600)
d.t(T3_X + 24, B3_Y + 108, "[fact 속성] + [상품 메타] + [매장] + [날짜 정보]", 11, INK, KR, "start")

# 실제 행 예시 박스
d.box(T3_X + 16, B3_Y + 126, T3_W - 32, 48, PAPER, RULE, 0.9)
d.t(T3_X + 24, B3_Y + 144, "행 예시 · 그림 3-5 첫 판매", 11, SOFT, KR, "start", 600)
d.t(T3_X + 24, B3_Y + 162, "260102 | Fish food | Palo Alto | 1 | 2.49", 11, INK, MONO, "start")

# 장점 및 비용 칩/라인
d.tone(T3_X + 16, B3_Y + 184, T3_W - 32, 24, OK, 4, "18", 1.0)
d.t(T3_X + T3_W / 2, B3_Y + 200, "장점 — 조인 없이 조회 · 때로 더 빠른 쿼리", 11, OK, KR, "middle", 600)

d.tone(T3_X + 16, B3_Y + 214, T3_W - 32, 24, WARN, 4, "18", 1.0)
d.t(T3_X + T3_W / 2, B3_Y + 230, "비용 — 메타데이터 중복 저장 · 저장 공간 증가", 11, WARN, KR, "middle", 600)

# 연결선 1: 원천 테이블들 -> 버스 -> 사전 계산
bus_x = 264
for _, _, y, bh, _ in boxes1:
    cy = y + bh / 2
    d.line(T1_X + T1_W, cy, bus_x, cy, RULE, 1.2)
d.line(bus_x, 148 + 28, bus_x, 344 + 26, RULE, 1.2)
d.arrow([(bus_x, B2_Y + 76), (T2_X - 4, B2_Y + 76)], MUTED, "ar", 1.4)
d.t((bus_x + T2_X) / 2, B2_Y + 66, "ETL", 11, MUTED, MONO, "middle", 600)

# 연결선 2: 사전 계산 -> OBT
d.arrow([(T2_X + T2_W, B2_Y + 76), (T3_X - 4, B2_Y + 76)], ACC, "acc", 1.6)
d.t((T2_X + T2_W + T3_X) / 2, B2_Y + 66, "적재", 11, ACC, KR, "middle", 600)

# 하단 비교 설명 바
d.box(T1_X, COMP_Y, W - T1_X * 2, COMP_H, PAPER2, RULE, 0.9)
d.t(T1_X + 20, COMP_Y + 24, "분석 맥락의 정당성", 12, ACC, KR, "start", 600)
d.t(T1_X + 144, COMP_Y + 24, "분석 데이터의 불변 이력 특성 · OLTP와 달리 일관성 및 쓰기 오버헤드 부담 완화", 12, MUTED, KR, "start")

d.legend(LEG, [("OBT 비정규화 (focal)", ACC), ("원천 테이블", INFO), ("쿼리 속도 이점", OK), ("저장 공간 비용", WARN)])
d.save("03-03.obt-denormalization.svg")
