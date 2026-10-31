# 12-02 §2 — 데이터베이스 복제 로그를 유일한 단일 리더로 삼는 CDC 파생 시스템 동기화 흐름.
# 사실 출처: 12-02 §2(L45~L59), DDIA 2판 Ch.12 Figure 12-5(PDF p.21, offset 번호 없음) — 원본 DB(System of Record),
#   CDC 프로세스, 변경 데이터 로그(Log of data changes), 파생 시스템(Search index, Data warehouse, Cache).
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 526
H = LEG + 52

d = D(W, H, "12-02 · §2 CHANGE DATA CAPTURE AND DERIVED SYSTEMS", "CDC 기반 데이터베이스와 파생 시스템 동기화 흐름",
      "데이터베이스 복제 로그를 스트림으로 추출해 검색 인덱스·캐시·DW에 동일 순서로 동기화한다.",
      "단일 리더 순서 결정 · 복제 로그 추출 · 순차 이벤트 스트림 · 파생 시스템 동일 순서 적용")

# 4단계 카드 정의
Y0 = 104
CARD_H = 318

# Stage 1: 클라이언트 쓰기
S1_X, S1_W = 24, 150
d.box(S1_X, Y0, S1_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S1_X + 28, Y0 + 20, "요청", WARN, 11, pad=4)
d.t(S1_X + 88, Y0 + 24, "클라이언트", 12, INK, KR, "middle", 600)
d.line(S1_X + 10, Y0 + 38, S1_X + S1_W - 10, Y0 + 38, RULE, 0.6)
d.t(S1_X + S1_W / 2, Y0 + 52, "동시 쓰기 요청", 11, MUTED, KR, "middle")

# Client 1 box
d.box(S1_X + 10, Y0 + 82, S1_W - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(S1_X + S1_W / 2, Y0 + 106, "Client 1", 12, INK, KR, "middle", 600)
d.t(S1_X + S1_W / 2, Y0 + 128, "set X = A", 12, WARN, MONO, "middle", 600)

# Client 2 box
d.box(S1_X + 10, Y0 + 184, S1_W - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(S1_X + S1_W / 2, Y0 + 208, "Client 2", 12, INK, KR, "middle", 600)
d.t(S1_X + S1_W / 2, Y0 + 230, "set X = B", 12, WARN, MONO, "middle", 600)

d.t(S1_X + S1_W / 2, Y0 + 294, "레이스 컨디션", 11, MUTED, KR, "middle")

# 화살표 (직교 경로): Stage 1 -> Stage 2
d.arrow([(S1_X + S1_W, Y0 + 118), (188, Y0 + 118), (188, Y0 + 138), (200, Y0 + 138)], WARN, "warn", 1.4)
d.arrow([(S1_X + S1_W, Y0 + 220), (188, Y0 + 220), (188, Y0 + 192), (200, Y0 + 192)], WARN, "warn", 1.4)

# Stage 2: 원본 데이터베이스 (System of Record)
S2_X, S2_W = 202, 186
d.box(S2_X, Y0, S2_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S2_X + 28, Y0 + 20, "리더", INFO, 11, pad=4)
d.t(S2_X + 102, Y0 + 24, "원본 데이터베이스", 12, INK, KR, "middle", 600)
d.line(S2_X + 10, Y0 + 38, S2_X + S2_W - 10, Y0 + 38, RULE, 0.6)
d.t(S2_X + S2_W / 2, Y0 + 52, "유일한 단일 리더 (SoR)", 11, INFO, KR, "middle", 600)

d.box(S2_X + 10, Y0 + 74, S2_W - 20, 160, PAPER, RULE, 0.8, r=4)
d.t(S2_X + S2_W / 2, Y0 + 96, "쓰기 커밋 순서 결정", 12, INK, KR, "middle", 600)
d.line(S2_X + 18, Y0 + 108, S2_X + S2_W - 18, Y0 + 108, RULE, 0.5)

d.box(S2_X + 18, Y0 + 118, S2_W - 36, 40, PAPER2, RULE, 0.6, r=3)
d.t(S2_X + S2_W / 2, Y0 + 134, "1차: set X = A 커밋", 11, MUTED, KR, "middle")
d.t(S2_X + S2_W / 2, Y0 + 149, "DB 상태: X = A", 11, MUTED, MONO, "middle")

d.box(S2_X + 18, Y0 + 168, S2_W - 36, 48, PAPER2, INFO, 0.9, r=3)
d.t(S2_X + S2_W / 2, Y0 + 186, "2차: set X = B 커밋", 11, INK, KR, "middle", 600)
d.t(S2_X + S2_W / 2, Y0 + 203, "DB 최종값: X = B", 11, INFO, MONO, "middle", 600)

d.box(S2_X + 10, Y0 + 246, S2_W - 20, 56, PAPER, RULE, 0.6, r=4)
d.t(S2_X + S2_W / 2, Y0 + 266, "복제 로그 (binlog)", 11, INK, KR, "middle", 600)
d.t(S2_X + S2_W / 2, Y0 + 286, "커밋 순서 불변 기록", 11, MUTED, KR, "middle")

# 화살표 (직교 경로): Stage 2 -> Stage 3
d.arrow([(S2_X + S2_W, Y0 + 274), (400, Y0 + 274), (400, Y0 + 104), (410, Y0 + 104)], ACC, "acc", 1.4)
d.t(400, Y0 + 88, "CDC", 11, ACC, KR, "middle", 600)

# Stage 3: CDC 및 변경 로그 (Log of data changes)
S3_X, S3_W = 412, 236
d.tone(S3_X, Y0, S3_W, CARD_H, ACC, 6, "14", 1.4)
d.chip(S3_X + 34, Y0 + 20, "스트림", ACC, 11, pad=4)
d.t(S3_X + 130, Y0 + 24, "CDC & 변경 데이터 로그", 12, ACC, KR, "middle", 600)
d.line(S3_X + 10, Y0 + 38, S3_X + S3_W - 10, Y0 + 38, RULE, 0.6)
d.t(S3_X + S3_W / 2, Y0 + 52, "순서 보존 메시지 브로커 (Kafka)", 11, INK, KR, "middle")

# CDC 파서 박스
d.box(S3_X + 10, Y0 + 74, S3_W - 20, 60, PAPER, ACC, 0.9, r=4)
d.t(S3_X + S3_W / 2, Y0 + 96, "CDC 커넥터 (Debezium)", 12, INK, KR, "middle", 600)
d.t(S3_X + S3_W / 2, Y0 + 116, "복제 로그 파싱 및 표준 스키마 변환", 11, MUTED, KR, "middle")

d.arrow([(S3_X + S3_W / 2, Y0 + 134), (S3_X + S3_W / 2, Y0 + 156)], ACC, "acc", 1.4)

# 로그 토픽 박스
d.box(S3_X + 10, Y0 + 158, S3_W - 20, 144, PAPER, RULE, 0.8, r=4)
d.t(S3_X + S3_W / 2, Y0 + 178, "토픽 파티션 (전체 순서 고정)", 11, INK, KR, "middle", 600)

d.box(S3_X + 18, Y0 + 192, S3_W - 36, 44, PAPER2, RULE, 0.6, r=3)
d.t(S3_X + S3_W - 32, Y0 + 210, "X = A", 11, INK, MONO, "end")
d.t(S3_X + S3_W / 2, Y0 + 226, "컴팩션 때 삭제 대상", 11, MUTED, KR, "middle")

d.box(S3_X + 18, Y0 + 244, S3_W - 36, 46, PAPER2, ACC, 1.0, r=3)
d.t(S3_X + S3_W - 32, Y0 + 262, "X = B", 11, ACC, MONO, "end", 600)
d.t(S3_X + S3_W / 2, Y0 + 279, "키 X 최신 이벤트 (컴팩션 후 남음)", 11, ACC, KR, "middle", 600)

# 화살표 (직교 경로): Stage 3 -> Stage 4
d.arrow([(S3_X + S3_W, Y0 + 214), (660, Y0 + 214), (660, Y0 + 110), (670, Y0 + 110)], OK, "ok", 1.4)
d.arrow([(S3_X + S3_W, Y0 + 250), (660, Y0 + 250), (660, Y0 + 194), (670, Y0 + 194)], OK, "ok", 1.4)
d.arrow([(S3_X + S3_W, Y0 + 276), (660, Y0 + 276), (660, Y0 + 276), (670, Y0 + 276)], OK, "ok", 1.4)

# Stage 4: 파생 시스템 (Derived data systems)
S4_X, S4_W = 672, 184
d.box(S4_X, Y0, S4_W, CARD_H, PAPER2, RULE, 1.0)
d.chip(S4_X + 32, Y0 + 20, "소비자", OK, 11, pad=4)
d.t(S4_X + 104, Y0 + 24, "파생 시스템들", 12, INK, KR, "middle", 600)
d.line(S4_X + 10, Y0 + 38, S4_X + S4_W - 10, Y0 + 38, RULE, 0.6)
d.t(S4_X + S4_W / 2, Y0 + 52, "로그 컨슈머 (동일 순서 적용)", 11, OK, KR, "middle")

# 파생 1: 검색 인덱스
d.box(S4_X + 10, Y0 + 74, S4_W - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(S4_X + 18, Y0 + 94, "전문 검색 인덱스", 11, INK, KR, "start", 600)
d.t(S4_X + 18, Y0 + 112, "순서: A 적용 후 B 적용", 11, MUTED, KR, "start")
d.t(S4_X + 18, Y0 + 130, "최종값: X = B", 11, OK, MONO, "start", 600)

# 파생 2: 캐시
d.box(S4_X + 10, Y0 + 158, S4_W - 20, 72, PAPER, RULE, 0.8, r=4)
d.t(S4_X + 18, Y0 + 178, "분산 캐시", 11, INK, KR, "start", 600)
d.t(S4_X + 18, Y0 + 196, "순서: A 적용 후 B 적용", 11, MUTED, KR, "start")
d.t(S4_X + 18, Y0 + 214, "최종값: X = B", 11, OK, MONO, "start", 600)

# 파생 3: 분석 데이터 웨어하우스
d.box(S4_X + 10, Y0 + 242, S4_W - 20, 68, PAPER, RULE, 0.8, r=4)
d.t(S4_X + 18, Y0 + 262, "분석 DW", 11, INK, KR, "start", 600)
d.t(S4_X + 18, Y0 + 280, "순서: A 적용 후 B 적용", 11, MUTED, KR, "start")
d.t(S4_X + 18, Y0 + 298, "최종값: X = B", 11, OK, MONO, "start", 600)

# 하단 종합 배너
d.tone(24, 442, W - 48, 56, OK, 6, "14", 1.2)
d.t(W / 2, 466, "단일 리더(DB) 순서 결정 → 동일 순서 비동기 전파 → 모든 파생 시스템 최종 일관성 보장", 13, OK, KR, "middle", 600)
d.t(W / 2, 486, "듀얼 라이트의 레이스 컨디션을 복제 로그 기반 단일 리더 구조로 근본 해결", 11, MUTED, KR, "middle")

d.legend(LEG, [
    ("단일 리더 DB", INFO),
    ("CDC 스트림 (focal)", ACC),
    ("파생 일관성", OK),
    ("동시 쓰기", WARN),
])

d.save("12-02.database-and-streams.svg")
