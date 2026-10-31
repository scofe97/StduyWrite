# 11-04 §1 — MapReduce의 DFS 다단계 기록 vs 데이터플로우 엔진의 단일 잡 파이프라이닝 및 메모리 중간 상태 비교.
# 사실 출처: 11-04 §1(L26~L49), 원서 Ch.11 p.16~17(워크플로우의 잡 사이 데이터는 DFS 에 기록, Spark 리니지·Flink 체크포인트), p.20(데이터플로우 엔진 6가지 이점, 태스크마다 새 JVM).
# 원서 p.20·p.21: 매퍼 출력은 로컬 디스크에 쓰고("MapReduce already uses this optimization for mapper output") DFS 복제 기록은 잡 출력에서 일어난다.
# 본문 L29 "맵 단계가 끝나면 중간 결과를 HDFS 에 기록" 은 원서와 어긋나므로 도식은 원서를 따른다(보고서에 본문 오류로 남김).
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 456
H = LEG + 56

d = D(W, H, "11-04 · §1 DATAFLOW ENGINES VS MAPREDUCE", "MapReduce 한계와 데이터플로우 엔진의 극복 구조",
      "MapReduce 워크플로우가 잡 사이마다 분산 파일시스템에 복제 기록하고 앞 잡이 끝나야 다음 잡을 시작하는 한계를 데이터플로우 엔진이 단일 잡 연산자 결합과 인메모리 파이프라이닝으로 극복하는 구조 대조.",
      "잡 사이 HDFS 복제 기록 vs 단일 잡 DAG 연산자 결합 · 인메모리 파이프라이닝 · 상주 워커 재사용")

# 구역 1: MapReduce (단계별 DFS 기록과 파이프라이닝 불가)
X = 24
Y1 = 96
W_SEC = 832
H1 = 144
d.box(X, Y1, W_SEC, H1, PAPER2, WARN, 1.0)
d.chip(X + 54, Y1 + 20, "MapReduce", WARN, 11)
d.t(X + 224, Y1 + 24, "잡 사이 DFS 복제 기록 (파이프라이닝 불가)", 12, INK, KR, "middle", 600)
d.line(X + 10, Y1 + 38, X + W_SEC - 10, Y1 + 38, RULE, 0.6)

# Map 태스크 박스
d.box(36, 146, 160, 56, PAPER, RULE, 0.8, r=4)
d.t(116, 166, "잡 1 (Map · Reduce)", 11, INK, KR, "middle", 600)
d.t(116, 184, "매퍼 출력은 로컬 디스크", 11, MUTED, KR, "middle")

# HDFS 중간 파일 복제 박스
d.tone(236, 146, 176, 56, WARN, 6, "14", 1.2)
d.t(324, 166, "HDFS 잡 출력 복제 기록", 11, WARN, KR, "middle", 600)
d.t(324, 184, "여러 머신 복제 · 잡 완료 대기", 11, INK, KR, "middle")

# Reduce 태스크 박스
d.box(452, 146, 160, 56, PAPER, RULE, 0.8, r=4)
d.t(532, 166, "잡 2 (Map · Reduce)", 11, INK, KR, "middle", 600)
d.t(532, 184, "새 JVM · HDFS 다시 읽기", 11, MUTED, KR, "middle")

# HDFS 최종 출력 박스
d.box(652, 146, 192, 56, PAPER, RULE, 0.8, r=4)
d.t(748, 166, "HDFS 최종 출력 복제 기록", 11, INK, KR, "middle", 600)
d.t(748, 184, "잡이 늘수록 같은 기록 반복", 11, MUTED, KR, "middle")

# 화살표 1
d.path("M 196 174 L 234 174", WARN, 1.2, m="warn")
d.path("M 412 174 L 450 174", WARN, 1.2, m="warn")
d.path("M 612 174 L 650 174", WARN, 1.2, m="warn")

d.t(X + W_SEC / 2, Y1 + 128, "핵심 병목: 잡마다 DFS 복제 I/O · 앞 잡이 끝나야 시작 · 태스크마다 새 JVM", 11, WARN, KR, "middle")

# 구역 2: 데이터플로우 엔진 (단일 잡 DAG와 인메모리 파이프라이닝)
Y2 = 252
H2 = 188
d.tone(X, Y2, W_SEC, H2, ACC, 6, "14", 1.4)
d.chip(X + 54, Y2 + 20, "데이터플로우", ACC, 11)
d.t(X + 236, Y2 + 24, "단일 잡 DAG 파이프라이닝 및 메모리 중간 상태", 12, ACC, KR, "middle", 600)
d.line(X + 10, Y2 + 38, X + W_SEC - 10, Y2 + 38, RULE, 0.6)

# 연산자 결합 스테이지 박스
d.box(36, 302, 188, 72, PAPER, RULE, 0.8, r=4)
d.t(130, 324, "스테이지 1 (Map + Filter)", 11, INK, KR, "middle", 600)
d.t(130, 342, "연속 연산자 단일 태스크 결합", 11, ACC, KR, "middle")
d.t(130, 358, "상주 워커 프로세스 (JVM 재사용)", 11, MUTED, KR, "middle")

# 중간 상태 메모리/버퍼 박스
d.tone(264, 302, 188, 72, OK, 6, "14", 1.2)
d.t(358, 324, "인메모리 버퍼 · 로컬 디스크", 11, OK, KR, "middle", 600)
d.t(358, 342, "HDFS 복제 I/O 제거", 11, INK, KR, "middle")
d.t(358, 358, "생산 즉시 소비 (파이프라이닝)", 11, ACC, KR, "middle")

# 스테이지 2 박스
d.box(492, 302, 156, 72, PAPER, RULE, 0.8, r=4)
d.t(570, 324, "스테이지 2 (Reduce)", 11, INK, KR, "middle", 600)
d.t(570, 342, "필요한 곳에만 정렬 수행", 11, MUTED, KR, "middle")
d.t(570, 358, "공유 메모리 버퍼 수신", 11, MUTED, KR, "middle")

# 결함 복구 대조 박스
d.box(688, 302, 156, 72, PAPER, RULE, 0.8, r=4)
d.t(766, 324, "결함 복구 메커니즘", 11, INFO, KR, "middle", 600)
d.t(766, 342, "Spark: RDD 리니지 재계산", 11, MUTED, KR, "middle")
d.t(766, 358, "Flink: 분산 스냅샷 복구", 11, MUTED, KR, "middle")

# 화살표 2
d.path("M 224 338 L 262 338", OK, 1.2, m="ok")
d.path("M 452 338 L 490 338", OK, 1.2, m="ok")
d.path("M 648 338 L 686 338", INFO, 1.2, m="info")

d.t(X + W_SEC / 2, Y2 + 168, "핵심 이점: 단일 잡 DAG 결합 · 인메모리 파이프라이닝 · 상주 워커 재사용 · 필요 시에만 정렬", 11, OK, KR, "middle")

# 범례
d.legend(LEG, [
    ("데이터플로우 (focal)", ACC),
    ("인메모리 버퍼", OK),
    ("결함 복구", INFO),
    ("DFS 복제 지연", WARN)
])

d.save("11-04.mapreduce-vs-dataflow.svg")
