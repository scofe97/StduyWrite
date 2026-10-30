# 04-05 §1 — 행 지향과 컬럼 지향 저장 레이아웃의 디스크 I/O 비교.
# 사실 출처: 본문 §1(L30~L41), DDIA Figure 4-7(행 지향 vs 컬럼 지향 저장 레이아웃). 컬럼 값은 Figure 4-7 앞 두 행(2026-10-30 검증에서 지어낸 140101 등을 교체)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 104, 276
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-05 · COLUMN STORAGE", "행 지향과 컬럼 지향 저장 레이아웃 비교",
      "fact_sales 100여 개 컬럼 중 3개 컬럼만 조회할 때 행 지향은 100개 속성 전체를 읽지만 컬럼 지향은 필요한 컬럼 파일만 읽는다.",
      "전체 속성 연속 저장 vs 컬럼별 분리 저장 및 위치 기반 행 재조립")

LW = 404
RW = 420
LX0 = 20
RX0 = 440

# 좌측 패널: 행 지향 저장 (OLTP 관례)
d.box(LX0, PY, LW, PH, PAPER2, RULE, 0.9)
d.chip(LX0 + 36, PY + 22, "OLTP", WARN, 11)
d.t(LX0 + 170, PY + 26, "행 지향 저장 (Row-Oriented)", 13, INK, KR, "middle", 600)
d.t(LX0 + LW / 2, PY + 46, "한 행의 모든 속성을 나란히 저장", 12, SOFT, KR, "middle")
d.line(LX0 + 12, PY + 56, LX0 + LW - 12, PY + 56, RULE, 0.8)

# 행 지향 테이블 행 4개
row_attrs = [
    ("행 0", "date · prod · store · qty · (100+ 속성)"),
    ("행 1", "date · prod · store · qty · (100+ 속성)"),
    ("행 2", "date · prod · store · qty · (100+ 속성)"),
    ("행 3", "date · prod · store · qty · (100+ 속성)"),
]

for idx, (r_lab, r_txt) in enumerate(row_attrs):
    ry = PY + 66 + idx * 32
    d.box(LX0 + 12, ry, LW - 24, 26, PAPER, RULE, 0.8)
    d.t(LX0 + 36, ry + 17, r_lab, 11, WARN, MONO, "middle", 600)
    d.line(LX0 + 58, ry + 4, LX0 + 58, ry + 22, RULE, 0.8)
    d.t(LX0 + 68, ry + 17, r_txt, 11, MUTED, MONO, "start")

# 행 지향 I/O 요약
d.tone(LX0 + 12, PY + 204, LW - 24, 60, WARN, 6, "18", 1.2)
d.t(LX0 + LW / 2, PY + 224, "분석 쿼리: 3개 속성만 필요해도 행 전체 로드", 12, INK, KR, "middle", 600)
d.t(LX0 + LW / 2, PY + 242, "100+ 속성 전체 디스크 로드 및 파싱 낭비", 12, WARN, KR, "middle")
d.t(LX0 + LW / 2, PY + 256, "디스크 I/O 대역폭 소모", 12, MUTED, KR, "middle")

# 우측 패널: 컬럼 지향 저장 (OLAP 최적화)
d.box(RX0, PY, RW, PH, PAPER2, ACC, 1.4)
d.chip(RX0 + 36, PY + 22, "OLAP", OK, 11)
d.t(RX0 + 180, PY + 26, "컬럼 지향 저장 (Column-Oriented)", 13, INK, KR, "middle", 600)
d.t(RX0 + RW / 2, PY + 46, "각 컬럼의 모든 값을 개별 파일에 저장", 12, SOFT, KR, "middle")
d.line(RX0 + 12, PY + 56, RX0 + RW - 12, PY + 56, RULE, 0.8)

# 쿼리 접근 컬럼 3개 (OK 톤)
cols_active = [
    ("date_key.col", "[ 260102, 260102, ... ]", "접근 ✓"),
    ("product_sk.col", "[     69,     69, ... ]", "접근 ✓"),
    ("quantity.col", "[      1,      3, ... ]", "접근 ✓"),
]

for idx, (c_name, c_vals, c_stat) in enumerate(cols_active):
    cy = PY + 66 + idx * 32
    d.tone(RX0 + 12, cy, RW - 24, 26, OK, 4, "16", 1.0)
    d.t(RX0 + 64, cy + 17, c_name, 11, INK, MONO, "middle", 600)
    d.t(RX0 + 134, cy + 17, c_vals, 11, OK, MONO, "start")
    d.t(RX0 + RW - 24, cy + 17, c_stat, 12, OK, KR, "end", 600)

# 미접근 컬럼 1개 (회색/점선)
cy_unused = PY + 66 + 3 * 32
d.box(RX0 + 12, cy_unused, RW - 24, 26, PAPER, RULE, 0.8)
d.t(RX0 + 64, cy_unused + 17, "나머지 컬럼", 12, SOFT, KR, "middle")
d.t(RX0 + 134, cy_unused + 17, "store_sk · promo_sk 등", 11, MUTED, MONO, "start")
d.t(RX0 + RW - 24, cy_unused + 17, "미접근", 12, SOFT, KR, "end")

# 컬럼 지향 I/O 및 재조립 요약
d.tone(RX0 + 12, PY + 204, RW - 24, 60, ACC, 6, "1C", 1.2)
d.t(RX0 + RW / 2, PY + 224, "쿼리가 쓰는 3개 컬럼 파일만 읽고 파싱", 12, INK, KR, "middle", 600)
d.t(RX0 + RW / 2, PY + 242, "모든 컬럼이 같은 행 순서 유지 · k번째 항목 결합", 12, ACC, KR, "middle")
d.t(RX0 + RW / 2, PY + 256, "안 쓰는 컬럼은 읽지 않음", 12, OK, KR, "middle")

d.legend(LEG, [("필요 컬럼 로드", OK), ("행 재조립", ACC), ("불필요 속성 로드", WARN), ("미접근 컬럼", SOFT)])
d.save("04-05.column-storage.svg")
