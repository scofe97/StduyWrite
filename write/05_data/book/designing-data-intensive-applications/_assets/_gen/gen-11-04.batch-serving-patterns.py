# 11-04 §4 — 배치 잡 출력을 프로덕션 서빙 시스템에 반영하는 세 가지 경로 비교 (직접 쓰기 한계, Kafka 버퍼 수집, Bulk Import).
# 사실 출처: 11-04 §4(L88~L95), 원서 Ch.11 "Output of Batch Workflows" (PDF p.31~34)
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 456
H = LEG + 56

d = D(W, H, "11-04 · §4 SERVING BATCH OUTPUTS", "파생 데이터 서빙 패턴과 직접 쓰기 한계",
      "수천 개 병렬 태스크의 레코드별 직접 쓰기 병목을 방지하기 위한 Kafka 버퍼 수집 패턴 및 SST 파일 bulk import 패턴 대조.",
      "레코드별 직접 쓰기 병목 vs Kafka 토픽 버퍼 수집 · DB 파일 빌드 후 원자적 bulk import")

X = 24
W_SEC = 832

# 경로 1: 안티패턴 — 레코드별 직접 쓰기
Y1 = 96
H1 = 96
d.box(X, Y1, W_SEC, H1, PAPER2, BAD, 1.0)
d.chip(X + 54, Y1 + 20, "직접 쓰기", BAD, 11)
d.t(X + 224, Y1 + 24, "피해야 할 패턴 — 레코드별 DB 직접 쓰기", 12, INK, KR, "middle", 600)
d.line(X + 10, Y1 + 38, X + W_SEC - 10, Y1 + 38, RULE, 0.6)

# 박스 배치
d.box(36, 144, 200, 36, PAPER, RULE, 0.8, r=4)
d.t(136, 166, "배치 태스크 (수천 개 병렬)", 11, INK, KR, "middle", 600)

d.path("M 236 162 L 316 162", BAD, 1.2, m="bad")
d.t(276, 152, "개별 INSERT", 11, BAD, KR, "middle")

d.tone(316, 144, 180, 36, BAD, 6, "14", 1.2)
d.t(406, 166, "프로덕션 서빙 DB", 11, BAD, KR, "middle", 600)

d.t(660, 166, "위험: 네트워크 왕복 지연 · DB 연결 및 I/O 포화", 11, BAD, KR, "middle")

# 경로 2: 패턴 1 — Kafka 토픽 버퍼 수집
Y2 = 204
H2 = 112
d.box(X, Y2, W_SEC, H2, PAPER2, INFO, 1.0)
d.chip(X + 54, Y2 + 20, "패턴 1", INFO, 11)
d.t(X + 224, Y2 + 24, "Kafka 토픽 버퍼 푸시 및 독립 소비자 수집", 12, INK, KR, "middle", 600)
d.line(X + 10, Y2 + 38, X + W_SEC - 10, Y2 + 38, RULE, 0.6)

d.box(36, 252, 172, 50, PAPER, RULE, 0.8, r=4)
d.t(122, 272, "배치 잡 클러스터", 11, INK, KR, "middle", 600)
d.t(122, 290, "대용량 순차 쓰기", 11, MUTED, KR, "middle")

d.path("M 208 277 L 268 277", INFO, 1.2, m="info")

d.tone(268, 252, 208, 50, INFO, 6, "14", 1.2)
d.t(372, 272, "Kafka 토픽 (버퍼 · DMZ)", 11, INFO, KR, "middle", 600)
d.t(372, 290, "순차 로그 저장 · 보안 경계 분리", 11, INK, KR, "middle")

d.path("M 476 277 L 536 277", INFO, 1.2, m="info")

d.box(536, 252, 288, 50, PAPER, RULE, 0.8, r=4)
d.t(680, 272, "서빙 시스템 (Elasticsearch · Pinot · Druid)", 11, INK, KR, "middle", 600)
d.t(680, 290, "소비자 자체 속도 수집 · 복수 소비자 독립 읽기", 11, MUTED, KR, "middle")

# 경로 3: 패턴 2 — DB 파일 빌드 후 bulk import (focal)
Y3 = 328
H3 = 116
d.tone(X, Y3, W_SEC, H3, ACC, 6, "14", 1.4)
d.chip(X + 54, Y3 + 20, "패턴 2", ACC, 11)
d.t(X + 224, Y3 + 24, "배치 내부 DB 파일 빌드 및 원자적 Bulk Import", 12, ACC, KR, "middle", 600)
d.line(X + 10, Y3 + 38, X + W_SEC - 10, Y3 + 38, RULE, 0.6)

d.box(36, 376, 200, 52, PAPER, RULE, 0.8, r=4)
d.t(136, 396, "배치 잡 내부 생성", 11, INK, KR, "middle", 600)
d.t(136, 414, "SST 파일 · Pinot 세그먼트", 11, ACC, KR, "middle")

d.path("M 236 402 L 296 402", OK, 1.2, m="ok")

d.tone(296, 376, 200, 52, OK, 6, "14", 1.2)
d.t(396, 396, "완성된 DB 파일셋", 11, OK, KR, "middle", 600)
d.t(396, 414, "오브젝트 스토어 · DFS 적재", 11, INK, KR, "middle")

d.path("M 496 402 L 556 402", ACC, 1.2, m="acc")

d.box(556, 376, 268, 52, PAPER, RULE, 0.8, r=4)
d.t(690, 396, "서빙 스토어 (TiDB Lightning · RocksDB)", 11, INK, KR, "middle", 600)
d.t(690, 414, "원자적 버전 전환 (all-or-nothing)", 11, ACC, KR, "middle")

# 범례
d.legend(LEG, [
    ("Bulk Import (focal)", ACC),
    ("Kafka 버퍼", INFO),
    ("정상 적재", OK),
    ("직접 쓰기 병목", BAD)
])

d.save("11-04.batch-serving-patterns.svg")
