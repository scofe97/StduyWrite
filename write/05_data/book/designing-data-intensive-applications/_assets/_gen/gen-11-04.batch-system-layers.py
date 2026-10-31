# 11-04 §5 — 11장 종합: 분산 배치 처리 3계층(저장·스케줄러·처리)의 진화와 불변 입력 기반의 황금 규칙.
# 사실 출처: 11-04 §5(L98~L110), 원서 Ch.11 "Summary" (PDF p.34~35)
# 타입 스펙: type-layers
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 460
H = LEG + 56

d = D(W, H, "11-04 · §5 BATCH ARCHITECTURE LAYERS", "분산 배치 처리 시스템의 계층 구조와 황금 규칙",
      "저장·오케스트레이션·처리 엔진의 진화와 고수준 쿼리 인터페이스, 그리고 인간 결함 내성을 보장하는 불변성 원칙.",
      "쿼리 추상화 · 데이터플로우 실행 엔진 · 오케스트레이션 · 분산 저장 · 배치 불변성 원칙")

LX = 24
LW = 832

# 계층 4: 쿼리 및 분석 추상화 계층
Y4 = 96
H4 = 64
d.box(LX, Y4, LW, H4, PAPER2, RULE, 1.0)
d.chip(LX + 48, Y4 + 20, "계층 4", INFO, 11)
d.t(LX + 230, Y4 + 24, "쿼리 및 분석 추상화 계층 (SQL · DataFrame)", 12, INK, KR, "middle", 600)
d.line(LX + 10, Y4 + 36, LX + LW - 10, Y4 + 36, RULE, 0.6)
d.t(LX + LW / 2, Y4 + 50, "비용 기반 옵티마이저(조인 순서 자동 선택) · DataFrame 지연 실행 · Apache Arrow 포맷", 11, MUTED, KR, "middle")

# 계층 3: 분산 처리 실행 엔진 계층 (focal)
Y3 = 168
H3 = 72
d.tone(LX, Y3, LW, H3, ACC, 6, "14", 1.4)
d.chip(LX + 48, Y3 + 20, "계층 3", ACC, 11)
d.t(LX + 230, Y3 + 24, "분산 처리 실행 엔진 계층 (데이터플로우)", 12, ACC, KR, "middle", 600)
d.line(LX + 10, Y3 + 36, LX + LW - 10, Y3 + 36, RULE, 0.6)
d.t(LX + LW / 2, Y3 + 52, "MapReduce 극복: 단일 잡 DAG · 인메모리 파이프라이닝 · 상주 워커 프로세스(JVM 재사용)", 11, INK, KR, "middle", 600)

# 계층 2: 워크플로우 오케스트레이션 계층
Y2 = 248
H2 = 64
d.box(LX, Y2, LW, H2, PAPER2, RULE, 1.0)
d.chip(LX + 48, Y2 + 20, "계층 2", OK, 11)
d.t(LX + 230, Y2 + 24, "워크플로우 오케스트레이션 계층 (스케줄러)", 12, INK, KR, "middle", 600)
d.line(LX + 10, Y2 + 36, LX + LW - 10, Y2 + 36, RULE, 0.6)
d.t(LX + LW / 2, Y2 + 50, "태스크 의존성 DAG 관리 · 실패 태스크 부분 재실행 · 데이터 백필 (Airflow · Dagster · Prefect)", 11, MUTED, KR, "middle")

# 계층 1: 분산 저장 및 테이블 포맷 계층
Y1 = 320
H1 = 64
d.box(LX, Y1, LW, H1, PAPER2, RULE, 1.0)
d.chip(LX + 48, Y1 + 20, "계층 1", INFO, 11)
d.t(LX + 230, Y1 + 24, "분산 저장 및 테이블 포맷 계층 (스토리지)", 12, INK, KR, "middle", 600)
d.line(LX + 10, Y1 + 36, LX + LW - 10, Y1 + 36, RULE, 0.6)
d.t(LX + LW / 2, Y1 + 50, "컴퓨트-스토리지 분리(S3 · GCS) · 컬럼 지향 포맷(Parquet) · 오픈 테이블 포맷(Apache Iceberg)", 11, MUTED, KR, "middle")

# 기반 원칙: 배치 처리의 황금 규칙
Y0 = 392
H0 = 52
d.tone(LX, Y0, LW, H0, OK, 6, "14", 1.2)
d.chip(LX + 56, Y0 + 20, "황금 규칙", OK, 11)
d.t(LX + 210, Y0 + 24, "배치 불변성 원칙과 인간 결함 내성", 12, OK, KR, "middle", 600)
d.t(LX + LW / 2 + 150, Y0 + 24, "입력 불변 · 출력 재생성 가능 · 부작용 최소화", 11, INK, KR, "middle")
d.t(LX + LW / 2, Y0 + 42, "코드 버그 발생 시에도 원본 손상 없이 잡 재실행으로 데이터 복구 가능", 11, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("데이터플로우 (focal)", ACC),
    ("쿼리 및 저장 계층", INFO),
    ("오케스트레이션 및 황금 규칙", OK)
])

d.save("11-04.batch-system-layers.svg")
