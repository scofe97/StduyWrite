# 04-06 개요 — 4장 저장과 검색 전체 지형(OLTP·OLAP·고급 인덱스)과 다차원·전문·벡터 인덱스의 관계.
# 사실 출처: 04-06 본문 서두(L25~L28), §5 4장 종합(L97~L105), 원서 Ch.4 Summary
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 96
LEG = 434
H = LEG + 56

d = D(W, H, "04-06 · CHAPTER OVERVIEW", "4장 저장과 검색 지형",
      "단일 속성 키-값 저장(B-tree·LSM)과 대량 분석(컬럼 저장)을 넘어 여러 조건을 동시에 검색하는 다차원·전문·벡터 인덱스로 확장된다.",
      "단일 키 OLTP → 대량 분석 OLAP → 다중 조건 동시 검색 고급 인덱스")

# 루트 노드 (4장 저장과 검색 종합)
RX, RY, RW, RH = 280, 96, 320, 46
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 118, "4장 저장과 검색 지형", 14, INK, KR, "middle", 600)
d.t(440, 134, "저장 엔진 철학과 인덱스 발전 · 4장 종합", 12, MUTED, KR, "middle")

# 5개 카드 가로 배치
CW = 156
GAP = 18
X0 = 14
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(5)]

# 상위 3대 갈래
# 갈래 1: OLTP 단일 키 저장 (Cols 0, 1)
G1_X, G1_W = X0, CW * 2 + GAP  # 14, 330
d.box(G1_X, 174, G1_W, 38, PAPER2, RULE, 1.0)
d.t(G1_X + G1_W / 2, 192, "OLTP 단일 키 저장", 13, INK, KR, "middle", 600)
d.t(G1_X + G1_W / 2, 206, "단일 속성 정렬 매핑 · 04-01 ~ 04-04", 12, MUTED, KR, "middle")

# 갈래 2: OLAP 분석용 저장 (Col 2)
G2_X, G2_W = X0 + 2 * (CW + GAP), CW  # 362, 156
d.box(G2_X, 174, G2_W, 38, PAPER2, RULE, 1.0)
d.t(G2_X + G2_W / 2, 192, "OLAP 분석용 저장", 13, INK, KR, "middle", 600)
d.t(G2_X + G2_W / 2, 206, "대량 스캔 · 04-05", 12, MUTED, KR, "middle")

# 갈래 3: 다중 조건 고급 인덱스 (Cols 3, 4) — Focal ACC
G3_X, G3_W = X0 + 3 * (CW + GAP), CW * 2 + GAP  # 536, 330
d.tone(G3_X, 174, G3_W, 38, ACC, 6, "18", 1.4)
d.t(G3_X + G3_W / 2, 192, "다중 조건 고급 인덱스", 13, ACC, KR, "middle", 600)
d.t(G3_X + G3_W / 2, 206, "여러 조건 동시 쿼리 · 04-06", 12, ACC, KR, "middle")

# 루트 → 세 갈래 직각 버스 배선
BUS1_Y = 156
d.line(440, RY + RH, 440, BUS1_Y, RULE, 1.2)
d.line(G1_X + G1_W / 2, BUS1_Y, G3_X + G3_W / 2, BUS1_Y, RULE, 1.2)
d.line(G1_X + G1_W / 2, BUS1_Y, G1_X + G1_W / 2, 174, RULE, 1.2)
d.line(G2_X + G2_W / 2, BUS1_Y, G2_X + G2_W / 2, 174, RULE, 1.2)
d.line(G3_X + G3_W / 2, BUS1_Y, G3_X + G3_W / 2, 174, ACC, 1.4)

# 갈래 1 → 하위 두 카드 버스 배선
BUS2_Y = 226
d.line(G1_X + G1_W / 2, 212, G1_X + G1_W / 2, BUS2_Y, RULE, 1.2)
d.line(cx[0], BUS2_Y, cx[1], BUS2_Y, RULE, 1.2)
d.line(cx[0], BUS2_Y, cx[0], 244, RULE, 1.2)
d.line(cx[1], BUS2_Y, cx[1], 244, RULE, 1.2)

# 갈래 2 → Col 2 직결선
d.line(cx[2], 212, cx[2], 244, RULE, 1.2)

# 갈래 3 → 하위 두 카드 버스 배선
d.line(G3_X + G3_W / 2, 212, G3_X + G3_W / 2, BUS2_Y, ACC, 1.4)
d.line(cx[3], BUS2_Y, cx[4], BUS2_Y, ACC, 1.4)
d.line(cx[3], BUS2_Y, cx[3], 244, ACC, 1.4)
d.line(cx[4], BUS2_Y, cx[4], 244, ACC, 1.4)

# 5개 리프 카드
Y_CARD = 244
H_CARD = 166

cards = [
    ("LSM-tree · SSTable", "04-01 · 04-02",
     ["append-only 로그", "memtable 플러시", "백그라운드 병합", "높은 쓰기 처리량"], INFO, False),
    ("B-tree", "04-03",
     ["고정 크기 페이지", "update-in-place", "WAL 크래시 복구", "높은 읽기 처리량"], INFO, False),
    ("컬럼 지향 저장", "04-05",
     ["필요 컬럼 선별 I/O", "bitmap 압축 인코딩", "벡터화 배치 실행", "분석 쿼리 최적화"], INFO, False),
    ("다차원 & 전문 인덱스", "04-06 §1 · §2",
     ["R-tree 2D 동시 좁힘", "가까운 점 서브트리 묶음", "inverted index", "bitmap AND 연산"], ACC, True),
    ("벡터 임베딩 & 인덱스", "04-06 §3 · §4",
     ["부동소수 벡터 변환", "cosine 의미 유사도", "flat 전수 탐색", "IVF · HNSW 근사"], ACC, True),
]

for i, (title, section, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, ACC, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)
    
    # 카드 헤더
    d.t(cx[i], Y_CARD + 24, title, 13, INK if not is_focal else ACC, KR, "middle", 600)
    d.chip(cx[i], Y_CARD + 46, section, color, 12)
    
    # 구분선
    d.line(x + 10, Y_CARD + 60, x + CW - 10, Y_CARD + 60, RULE, 0.8)
    
    # 항목 4줄 (폰트 12px로 선명도 확보)
    for j, item in enumerate(items):
        item_y = Y_CARD + 80 + j * 22
        d.t(cx[i], item_y, item, 12, INK, KR, "middle")

d.legend(LEG, [("OLTP · OLAP 저장 엔진", INFO), ("다중 조건 고급 인덱스 (04-06 핵심)", ACC)])
d.save("04-06.chapter-overview.svg")
