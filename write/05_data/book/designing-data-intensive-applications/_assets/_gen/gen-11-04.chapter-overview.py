# 11-04 개요 — 데이터플로우 엔진(§1)부터 쿼리 언어(§2), ETL·분석(§3), 머신러닝·서빙(§4), 11장 종합(§5)을 잇는 전체 지도.
# 사실 출처: 11-04 서두(L13~L19), §1(L24~L45), §2(L47~L64), §3(L66~L77), §4(L79~L96), §5(L98~L112), 원서 Ch.11 (PDF p.17~35)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 432
H = LEG + 56

d = D(W, H, "11-04 · CHAPTER OVERVIEW", "데이터플로우 엔진과 배치 활용 전체 지도",
      "MapReduce 한계 극복에서 SQL·DataFrame 쿼리 추상화, ETL·분석·ML 응용과 파생 데이터 서빙 패턴까지의 전개.",
      "데이터플로우 파이프라이닝 · 쿼리 인터페이스 추상화 · ETL과 레이크하우스 · 파생 데이터 서빙 · 계층 종합")

# 루트 노드: 데이터플로우 엔진과 배치 처리 체계
RX, RY, RW, RH = 180, 96, 520, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 118, "데이터플로우 엔진과 배치 처리 체계", 14, INK, KR, "middle", 600)
d.t(440, 134, "MapReduce 극복에서 쿼리 추상화, 응용 파이프라인과 파생 데이터 서빙까지", 11, MUTED, KR, "middle")

# 5개 카드 컬럼 기하 (CW=156, GAP=14, X0=24)
CW = 156
GAP = 14
X0 = 24
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(5)]

# 루트 -> 5개 컬럼 배선 버스
BUS_Y = 162
d.line(440, RY + RH, 440, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[4], BUS_Y, RULE, 1.2)
for i in range(5):
    d.line(cx[i], BUS_Y, cx[i], 178, ACC if i == 0 else RULE, 1.2)

Y_CARD = 178
H_CARD = 230

cards = [
    ("데이터플로우", "§1", [
        "단일 잡 DAG 파이프라인",
        "메모리·로컬 중간 상태",
        "워커 프로세스 재사용",
        "RDD 리니지·체크포인트"
    ], ACC, True),
    ("쿼리 언어", "§2", [
        "비용 기반 옵티마이저",
        "조인 순서 자동 최적화",
        "DataFrame 지연 실행",
        "Apache Arrow 포맷"
    ], INFO, False),
    ("ETL과 분석", "§3", [
        "병렬 변환·Airflow DAG",
        "Data Mesh 도메인 소유",
        "사전 집계 vs 애드혹",
        "Data Lakehouse 융합"
    ], OK, False),
    ("ML·파생 서빙", "§4", [
        "피처 변환·추론 단계",
        "Pregel BSP 그래프",
        "Kafka 토픽 버퍼 수집",
        "SST bulk import"
    ], WARN, False),
    ("11장 종합", "§5", [
        "저장·스케줄러·엔진",
        "컴퓨트·스토리지 분리",
        "불변 입력·재실행 보장",
        "스트림 처리 연결(12장)"
    ], INFO, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, color, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)

    # 섹션 칩
    chip_x = x + 30
    d.chip(chip_x, Y_CARD + 24, sec_chip, color, 11, pad=5)
    d.t(x + CW / 2 + 16, Y_CARD + 28, title, 12, INK, KR, "middle", 600)
    d.line(x + 10, Y_CARD + 44, x + CW - 10, Y_CARD + 44, RULE, 0.8)

    for j, it in enumerate(items):
        iy = Y_CARD + 66 + j * 40
        d.box(x + 8, iy - 13, CW - 16, 26, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 4, it, 11, INK if not is_focal else color, KR, "middle")

# 범례
d.legend(LEG, [
    ("데이터플로우 (focal)", ACC),
    ("쿼리 언어·종합", INFO),
    ("ETL·분석", OK),
    ("ML·서빙", WARN)
])

d.save("11-04.chapter-overview.svg")
