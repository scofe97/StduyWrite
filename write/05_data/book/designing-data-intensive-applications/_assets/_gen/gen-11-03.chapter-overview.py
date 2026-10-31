# 11-03 개요 — 오케스트레이터 구조(§1), 자원 할당(§2), 워크플로우 스케줄러(§3), 결함 처리와 MapReduce(§4), 셔플과 Sort-Merge Join(§5) 전체 지도.
# 사실 출처: 11-03 본문 서두(L13~L18), §1(L22~L34), §2(L37~L49), §3(L52~L62), §4(L65~L83), §5(L86~L108), 원서 Ch.11(PDF p.12~24)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 34
PY = 152
PH = 246
LEG = PY + PH + 26
H = LEG + 50

d = D(W, H, "11-03 · CHAPTER OVERVIEW", "분산 잡 오케스트레이션과 MapReduce 구조",
      "오케스트레이터 구조(§1), 자원 할당(§2), 워크플로우 스케줄러(§3), 결함 처리(§4), 셔플과 Sort-Merge Join(§5)의 체계.",
      "분산 OS 자원 배분 · NP-hard 스케줄링 휴리스틱 · 잡 간 DAG 의존성 · DFS 중간 기록 기반 무상태 재실행 · 키 해시 셔플과 조인")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 22, "분산 OS 추상화: 클러스터 자원 스케줄링 위에 MapReduce 정렬·셔플로 대규모 조인 처리", 12, INK, KR, "middle", 600)

X0 = 24
CW = 158
GAP = 11

cards = [
    ("§1", "오케스트레이터", "분산 OS 추상화",
     [("태스크 실행기", "NodeManager/kubelet"),
      ("리소스 매니저", "전역 자원 · etcd 상태"),
      ("스케줄러", "중앙 + AppMaster")],
     INFO, False),
    ("§2", "자원 할당", "스케줄링 트레이드오프",
     [("NP-hard 문제", "최적 해 계산 불가"),
      ("휴리스틱 기법", "FIFO · DRF · 선점"),
      ("비효율·경합", "Gang 예약 · 스타베이션")],
     WARN, False),
    ("§3", "워크플로우", "잡 간 DAG 관리",
     [("데이터 DAG", "업스트림 → 다운스트림"),
      ("이기종 파이프라인", "Spark → HDFS → SQL"),
      ("전용 엔진", "Airflow · Dagster")],
     OK, False),
    ("§4", "결함 처리", "MapReduce 재실행",
     [("무상태 매퍼", "독립적 레코드 매핑"),
      ("DFS 중간 기록", "태스크 단위 단독 재실행"),
      ("4단계 파이프라인", "입력·매핑·셔플·리듀스")],
     INFO, False),
    ("§5", "셔플·조인", "분산 정렬과 조인",
     [("해시 파티셔닝", "동일 키 동일 리듀서"),
      ("리듀서 MergeSort", "연속 정렬과 집계"),
      ("Secondary Sort", "DB 레코드 선행 배치")],
     ACC, True),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 24, y + 20, sec, card_c, 11)
    d.t(x + 46, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 12, y + 46, role, 11, SOFT, KR, "start")

    d.line(x + 10, y + 58, x + CW - 10, y + 58, RULE, 0.8)

    # 3개 항목
    iy0 = y + 80
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 52
        d.box(x + 8, iy - 14, CW - 16, 44, PAPER, RULE, 0.6)
        d.t(x + 14, iy + 2, head, 12, INK, KR, "start", 600)
        d.t(x + 14, iy + 20, sub, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("분산 정렬·조인 (focal)", ACC),
    ("시스템 구조·실행", INFO),
    ("워크플로우·DAG", OK),
    ("자원 제약·경합", WARN),
])

d.save("11-03.chapter-overview.svg")
