# 03-06 개요 — 3장에서 다룬 데이터 모델 전체 지도(본문 §4 종합의 분류와 각 절의 관계).
# 사실 출처: 03-06 본문 도입부(L29~L32), §4 3장 종합(L116~L128), §1(L50~L53), §3(L99~L102)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
PY = 96
LEG = 436
H = LEG + 56

d = D(W, H, "03-06 · CHAPTER OVERVIEW", "3장 데이터 모델 전체 지도",
      "관계형·문서·그래프의 단일 표현 쿼리에서 DataFrame의 다차원 배열 변환, 이벤트 소싱·CQRS의 쓰기·읽기 분리로 확장된다.",
      "단일 표현 질의 → 다차원 배열 변환 → 쓰기·읽기 분리")

# 루트 노드 (3장 데이터 모델 종합)
RX, RY, RW, RH = 300, 104, 280, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 126, "3장 데이터 모델 지형", 14, INK, KR, "middle", 600)
d.t(440, 142, "데이터 모델과 쿼리 언어 · 종합 §4", 11, MUTED, KR, "middle")

# 5개 모델 컬럼 기하
CW = 156
GAP = 16
X0 = 18
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(5)]
# cx: [96, 268, 440, 612, 784]

# 상위 분류 (3개 갈래)
# 갈래 1: 단일 표현 질의 (Cols 0, 1, 2)
G1_X, G1_W = X0, CW * 3 + GAP * 2  # 18, 500
d.box(G1_X, 188, G1_W, 38, PAPER2, RULE, 1.0)
d.t(G1_X + G1_W / 2, 206, "단일 표현 질의", 13, INK, KR, "middle", 600)
d.t(G1_X + G1_W / 2, 220, "쓴 형태 그대로 쿼리 · 03-01 ~ 03-05", 11, MUTED, KR, "middle")

# 갈래 2: 다차원 배열 변환 (Col 3)
G2_X, G2_W = X0 + 3 * (CW + GAP), CW  # 534, 156
d.box(G2_X, 188, G2_W, 38, PAPER2, RULE, 1.0)
d.t(G2_X + G2_W / 2, 206, "다차원 배열 변환", 13, INK, KR, "middle", 600)
d.t(G2_X + G2_W / 2, 220, "03-06 §3", 11, MUTED, MONO, "middle")

# 갈래 3: 쓰기 · 읽기 분리 (Col 4) — Focal ACC
G3_X, G3_W = X0 + 4 * (CW + GAP), CW  # 706, 156
d.tone(G3_X, 188, G3_W, 38, ACC, 6, "18", 1.4)
d.t(G3_X + G3_W / 2, 206, "쓰기 · 읽기 분리", 13, ACC, KR, "middle", 600)
d.t(G3_X + G3_W / 2, 220, "03-06 §1 · §2", 11, ACC, MONO, "middle")

# 루트 → 세 갈래 직각 버스 배선
BUS1_Y = 168
d.line(440, RY + RH, 440, BUS1_Y, RULE, 1.2)
d.line(G1_X + G1_W / 2, BUS1_Y, G3_X + G3_W / 2, BUS1_Y, RULE, 1.2)
d.line(G1_X + G1_W / 2, BUS1_Y, G1_X + G1_W / 2, 188, RULE, 1.2)
d.line(G2_X + G2_W / 2, BUS1_Y, G2_X + G2_W / 2, 188, RULE, 1.2)
d.line(G3_X + G3_W / 2, BUS1_Y, G3_X + G3_W / 2, 188, ACC, 1.4)

# 갈래 1 → 하위 세 모델 직각 버스 배선
BUS2_Y = 240
d.line(G1_X + G1_W / 2, 226, G1_X + G1_W / 2, BUS2_Y, RULE, 1.2)
d.line(cx[0], BUS2_Y, cx[2], BUS2_Y, RULE, 1.2)
for i in range(3):
    d.line(cx[i], BUS2_Y, cx[i], 254, RULE, 1.2)

# 갈래 2 → Col 3 직결선
d.line(cx[3], 226, cx[3], 254, RULE, 1.2)

# 갈래 3 → Col 4 직결선
d.line(cx[4], 226, cx[4], 254, ACC, 1.4)

# 5개 모델 리프 카드 (y = 254, height = 160)
Y_CARD = 254
H_CARD = 160

cards = [
    ("관계형 모델", "03-01 ~ 03-03", ["테이블 · 행 구조", "별 · 눈송이 스키마", "선언형 SQL 질의", "DW · 비즈니스 분석"], INFO, False),
    ("문서 모델", "03-01 · 03-04", ["자족적 JSON 문서", "문서 간 관계 드묾", "1:N 중첩 계층 트리", "암묵적 스키마"], INFO, False),
    ("그래프 모델", "03-05", ["정점 · 간선 연관", "다중 홉 경로 순회", "재귀 쿼리 언어", "Cypher · SPARQL"], INFO, False),
    ("DataFrame", "03-06 §3", ["다차원 숫자 배열", "관계형 행 → 희소 행렬", "선형대수 연산 기반", "ML 모델 학습 입력"], INFO, False),
    ("이벤트 소싱 · CQRS", "03-06 §1 · §2", ["불변 이벤트 로그", "쓰기 최적화 append", "구체화 뷰 파생 (읽기)", "진실의 원천 유지"], ACC, True),
]

for i, (title, section, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)
    
    # 카드 헤더
    d.t(cx[i], Y_CARD + 24, title, 13, INK if not is_focal else ACC, KR, "middle", 600)
    d.chip(cx[i], Y_CARD + 44, section, color, 11)
    
    # 구분선
    d.line(x + 12, Y_CARD + 58, x + CW - 12, Y_CARD + 58, RULE, 0.8)
    
    # 항목 4줄
    for j, item in enumerate(items):
        item_y = Y_CARD + 76 + j * 22
        d.t(cx[i], item_y, item, 11, INK if not is_focal else INK, KR, "middle")

d.legend(LEG, [("단일 표현 · 배열 모델", INFO), ("쓰기 · 읽기 분리 (핵심)", ACC)])
d.save("03-06.chapter-overview.svg")
