# 11-03 §3 — 워크플로우 스케줄러와 잡 간 DAG 의존성(Airflow/Dagster 및 Spark→HDFS→Trino 파이프라인).
# 사실 출처: 11-03 §3(L60~L73; L63 로그 정제 → 집계 → 보고서 생성), 원서 Ch.11 p.15~16.
# 도구 표기(Spark → HDFS → Trino SQL → S3)는 원서 p.15 예. 잡별 처리 내용은 본문이 주지 않으므로 잡 이름 수준에서 멈춘다.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 412
H = LEG + 48

d = D(W, H, "11-03 · §3 BATCH WORKFLOW SCHEDULING", "잡 간 DAG 의존성과 워크플로우 오케스트레이션",
      "단일 잡 자원 배분과 분리하여, 워크플로우 스케줄러가 여러 잡 사이의 산출물 의존성 DAG를 정의하고 선행 잡 완료를 검증해 후속 잡을 순서대로 실행한다.",
      "선행 잡 산출물 의존성 · Airflow/Dagster DAG 제어 · 이기종 도구 데이터 파이프라인 · YARN/K8s 잡 스케줄러와의 역할 분담")

# 1. 상단: 워크플로우 스케줄러 계층 (Airflow · Dagster · Prefect)
TOP_X, TOP_Y, TOP_W, TOP_H = 24, 102, W - 48, 64
d.tone(TOP_X, TOP_Y, TOP_W, TOP_H, ACC, 6, "14", 1.4)
d.chip(TOP_X + 46, TOP_Y + 18, "DAG 제어", ACC, 11, pad=4)
d.t(TOP_X + 96, TOP_Y + 22, "워크플로우 스케줄러 (Airflow · Dagster · Prefect)", 13, ACC, KR, "start", 600)
d.line(TOP_X + 10, TOP_Y + 34, TOP_X + TOP_W - 10, TOP_Y + 34, RULE, 0.6)
d.t(TOP_X + TOP_W / 2, TOP_Y + 50, "잡 간 DAG 의존성 정의 · 선행 잡 성공 감지 후 후속 트리거 · 실패 재시도 정책 및 스케줄 관리", 11, INK, KR, "middle")

# 2. 중간: 3단계 DAG 데이터 파이프라인 (Spark -> HDFS -> Trino)
J_Y = 192
J_H = 158
J_W = 246
GAP = 47

# Job A (좌측)
JA_X = 24
d.box(JA_X, J_Y, J_W, J_H, PAPER2, INFO, 1.1)
d.chip(JA_X + 28, J_Y + 18, "Job A", INFO, 11, pad=4)
d.t(JA_X + 138, J_Y + 22, "로그 정제 잡 (Spark)", 12, INK, KR, "middle", 600)
d.line(JA_X + 10, J_Y + 34, JA_X + J_W - 10, J_Y + 34, RULE, 0.6)

d.t(JA_X + 14, J_Y + 54, "입력: 원시 로그 (DFS)", 11, INK, KR, "start")
d.t(JA_X + 14, J_Y + 74, "처리: 로그 정제", 11, MUTED, KR, "start")
d.t(JA_X + 14, J_Y + 94, "출력: 정제된 로그 (HDFS)", 11, INK, KR, "start")
d.box(JA_X + 14, J_Y + 112, J_W - 28, 32, PAPER, OK, 0.8)
d.t(JA_X + J_W / 2, J_Y + 132, "성공 완료", 11, OK, KR, "middle", 600)

# Job B (중앙)
JB_X = JA_X + J_W + GAP
d.box(JB_X, J_Y, J_W, J_H, PAPER2, OK, 1.1)
d.chip(JB_X + 28, J_Y + 18, "Job B", OK, 11, pad=4)
d.t(JB_X + 138, J_Y + 22, "집계 잡", 12, INK, KR, "middle", 600)
d.line(JB_X + 10, J_Y + 34, JB_X + J_W - 10, J_Y + 34, RULE, 0.6)

d.t(JB_X + 14, J_Y + 54, "입력: Job A 출력 (HDFS)", 11, INK, KR, "start")
d.t(JB_X + 14, J_Y + 74, "처리: 집계", 11, MUTED, KR, "start")
d.t(JB_X + 14, J_Y + 94, "출력: 집계 결과 (HDFS)", 11, INK, KR, "start")
d.box(JB_X + 14, J_Y + 112, J_W - 28, 32, PAPER, OK, 0.8)
d.t(JB_X + J_W / 2, J_Y + 132, "성공 완료", 11, OK, KR, "middle", 600)

# Job C (우측)
JC_X = JB_X + J_W + GAP
d.box(JC_X, J_Y, J_W, J_H, PAPER2, WARN, 1.1)
d.chip(JC_X + 28, J_Y + 18, "Job C", WARN, 11, pad=4)
d.t(JC_X + 138, J_Y + 22, "보고서 생성 잡 (Trino SQL)", 12, INK, KR, "middle", 600)
d.line(JC_X + 10, J_Y + 34, JC_X + J_W - 10, J_Y + 34, RULE, 0.6)

d.t(JC_X + 14, J_Y + 54, "입력: Job B 출력 (HDFS)", 11, INK, KR, "start")
d.t(JC_X + 14, J_Y + 74, "처리: SQL 쿼리", 11, MUTED, KR, "start")
d.t(JC_X + 14, J_Y + 94, "출력: 보고서 (S3)", 11, INK, KR, "start")
d.box(JC_X + 14, J_Y + 112, J_W - 28, 32, PAPER, WARN, 0.8)
d.t(JC_X + J_W / 2, J_Y + 132, "앞 잡이 모두 성공한 뒤 실행", 11, WARN, KR, "middle", 600)

# DAG 데이터 연결선 (A -> B, B -> C)
d.path(f"M {JA_X + J_W} {J_Y + 74} L {JB_X} {J_Y + 74}", INFO, 1.4, m="info")
d.t((JA_X + J_W + JB_X) / 2, J_Y + 64, "HDFS", 11, INFO, MONO, "middle", 600)

d.path(f"M {JB_X + J_W} {J_Y + 74} L {JC_X} {J_Y + 74}", OK, 1.4, m="ok")
d.t((JB_X + J_W + JC_X) / 2, J_Y + 64, "HDFS", 11, OK, MONO, "middle", 600)

# 상단 스케줄러 계층 -> 개별 잡 트리거 제어선 (직선 수직 연결)
d.path(f"M {JA_X + J_W / 2} {TOP_Y + TOP_H} L {JA_X + J_W / 2} {J_Y}", ACC, 1.2, m="acc")
d.path(f"M {JB_X + J_W / 2} {TOP_Y + TOP_H} L {JB_X + J_W / 2} {J_Y}", ACC, 1.2, m="acc")
d.path(f"M {JC_X + J_W / 2} {TOP_Y + TOP_H} L {JC_X + J_W / 2} {J_Y}", ACC, 1.2, m="acc")

# 3. 하단: 인프라 오케스트레이터 계층
BOT_X, BOT_Y, BOT_W, BOT_H = 24, 362, W - 48, 34
d.box(BOT_X, BOT_Y, BOT_W, BOT_H, PAPER, RULE, 0.9)
d.t(BOT_X + BOT_W / 2, BOT_Y + 22, "하위 인프라 계층 (YARN / Kubernetes): 단일 잡의 태스크 단위 자원 배분만 담당 (잡 간 DAG 의존성 미인지)", 11, SOFT, KR, "middle")

# 범례
d.legend(LEG, [
    ("워크플로우 DAG 제어 (focal)", ACC),
    ("선행 처리 잡", INFO),
    ("중간 집계 잡", OK),
    ("후속 분석 잡", WARN),
])

d.save("11-03.workflow-dag.svg")
