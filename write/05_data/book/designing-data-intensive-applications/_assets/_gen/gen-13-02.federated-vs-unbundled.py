# 13-02 세부 도식 — 연합 데이터베이스(읽기 통합) vs 언번들드 데이터베이스(쓰기 통합) 비교
# 사실 출처: 13-02 본문 §5(L71~L83), 원서 Ch.13 p.13~16 (Federated databases: unifying reads, Unbundled databases: unifying writes, PostgreSQL FDW, Trino, Hoptimator, Unix pipes, loose coupling)
# 2026-10-31 검증: 원서 p.13 에 없는 MongoDB·Hive/S3·Redis·DWH, "애플리케이션에 위임"·"분산 최적화"·"분산 트랜잭션 취약" 제거. 파생 저장소는 본문 §4 의 인덱스·구체화 뷰로, 이점 박스는 중립
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 100
PH1 = 184
PY2 = 298
PH2 = 194
LEG = PY2 + PH2 + 18
H = LEG + 46

d = D(W, H, "13-02 · SECTION 5", "연합 데이터베이스와 언번들드 데이터베이스의 구성 비교",
      "읽기 쿼리 인터페이스를 통합하는 연합 모델과 CDC·이벤트 로그로 쓰기 동기화를 해결하는 언번들드 모델",
      "연합 쿼리 엔진 · 고수준 쿼리 언어 · CDC · 이벤트 로그 · Unix 파이프 · 쓰기 동기화")

# 1. 연합 데이터베이스 패널 (읽기 통합)
d.box(24, PY1, 832, PH1, PAPER2, RULE, 0.9)
d.chip(24 + 40, PY1 + 20, "연합 모델", INFO, 11)
d.t(24 + 86, PY1 + 24, "연합 데이터베이스 (읽기 통합 · Unifying Reads)", 13, INK, KR, "start", 600)
d.t(24 + 14, PY1 + 44, "다양한 저장 엔진 위에 통합 쿼리 인터페이스 제공 · 쓰기 동기화에는 답 없음", 11, SOFT, KR, "start")
d.line(24 + 8, PY1 + 54, 24 + 832 - 8, PY1 + 54, RULE, 0.8)

# 연합 컴포넌트
# 클라이언트 질의
d.box(38, PY1 + 68, 110, 104, PAPER, RULE, 0.6)
d.t(93, PY1 + 104, "사용자 질의", 12, INK, KR, "middle", 600)
d.t(93, PY1 + 126, "통합 인터페이스로", 11, INK, KR, "middle")
d.t(93, PY1 + 144, "여러 곳 데이터 결합", 11, MUTED, KR, "middle")

# 연합 쿼리 엔진
d.box(174, PY1 + 66, 280, 108, PAPER, RULE, 0.6)
d.t(186, PY1 + 90, "연합 쿼리 엔진 (FDW · Trino)", 12, INK, KR, "start", 600)
d.t(186, PY1 + 112, "다양한 저장 엔진 위 통합 쿼리", 11, MUTED, KR, "start")
d.t(186, PY1 + 132, "고수준 쿼리 언어 · 우아한 의미론", 11, MUTED, KR, "start")
d.t(186, PY1 + 152, "구현은 복잡 · Hoptimator·Xorq 등", 11, MUTED, KR, "start")

# 3개 하위 저장소
d.box(480, PY1 + 66, 196, 32, PAPER, RULE, 0.6)
d.t(492, PY1 + 86, "저장 엔진 A", 11, INK, KR, "start", 600)

d.box(480, PY1 + 104, 196, 32, PAPER, RULE, 0.6)
d.t(492, PY1 + 124, "저장 엔진 B", 11, INK, KR, "start", 600)

d.box(480, PY1 + 142, 196, 32, PAPER, RULE, 0.6)
d.t(492, PY1 + 162, "다른 처리 방식", 11, INK, KR, "start", 600)

# 우측 한계점 박스
d.tone(702, PY1 + 66, 142, 108, WARN, 4, "16", 1.0)
d.t(773, PY1 + 90, "한계: 쓰기", 11, WARN, KR, "middle", 600)
d.t(773, PY1 + 114, "여러 시스템 간", 11, INK, KR, "middle")
d.t(773, PY1 + 134, "쓰기 동기화에", 11, INK, KR, "middle")
d.t(773, PY1 + 154, "좋은 답 없음", 11, WARN, KR, "middle")

# 연합 화살표
d.arrow([(148, PY1 + 120), (170, PY1 + 120)], MUTED, "ar", 1.1)
d.arrow([(454, PY1 + 82), (476, PY1 + 82)], MUTED, "ar", 1.1)
d.arrow([(454, PY1 + 120), (476, PY1 + 120)], MUTED, "ar", 1.1)
d.arrow([(454, PY1 + 158), (476, PY1 + 158)], MUTED, "ar", 1.1)


# 2. 언번들드 데이터베이스 패널 (쓰기 통합 · Focal)
d.box(24, PY2, 832, PH2, PAPER2, ACC, 1.4)
d.chip(24 + 40, PY2 + 20, "언번들드", ACC, 11)
d.t(24 + 86, PY2 + 24, "언번들드 데이터베이스 (쓰기 통합 · Unifying Writes)", 13, ACC, KR, "start", 600)
d.t(24 + 14, PY2 + 44, "CDC와 비동기 이벤트 로그로 쓰기 동기화 달성 · Unix 파이프 철학 기반의 느슨한 결합", 11, SOFT, KR, "start")
d.line(24 + 8, PY2 + 54, 24 + 832 - 8, PY2 + 54, RULE, 0.8)

# 언번들드 컴포넌트
# 클라이언트 쓰기
d.box(38, PY2 + 66, 96, 108, PAPER, RULE, 0.6)
d.t(86, PY2 + 104, "클라이언트 쓰기", 12, INK, KR, "middle", 600)
d.t(86, PY2 + 126, "단일 쓰기 요청", 11, INK, KR, "middle")
d.t(86, PY2 + 144, "원천 기록", 11, MUTED, KR, "middle")

# 단일 원천 DB
d.box(154, PY2 + 66, 130, 108, PAPER, RULE, 0.6)
d.t(219, PY2 + 96, "원천 DB", 12, INK, KR, "middle", 600)
d.t(219, PY2 + 118, "기록 시스템", 11, INK, KR, "middle")
d.t(219, PY2 + 138, "쓰기 기록", 11, MUTED, KR, "middle")
d.t(219, PY2 + 156, "변경 캡처 대상", 11, MUTED, KR, "middle")

# CDC & 이벤트 로그 (Focal tone)
d.tone(306, PY2 + 66, 172, 108, ACC, 4, "16", 1.2)
d.t(392, PY2 + 94, "CDC & 이벤트 로그", 12, ACC, KR, "middle", 600)
d.t(392, PY2 + 116, "변경을 순서대로 전달", 11, INK, KR, "middle")
d.t(392, PY2 + 136, "Unix 파이프처럼 연결", 11, INK, KR, "middle")
d.t(392, PY2 + 154, "느린 소비자 버퍼링", 11, MUTED, KR, "middle")

# 전문 파생 저장소 3종
d.box(502, PY2 + 66, 186, 32, PAPER, OK, 0.8)
d.t(514, PY2 + 86, "전문 검색 인덱스", 11, OK, KR, "start", 600)

d.box(502, PY2 + 104, 186, 32, PAPER, OK, 0.8)
d.t(514, PY2 + 124, "구체화 뷰", 11, OK, KR, "start", 600)

d.box(502, PY2 + 142, 186, 32, PAPER, OK, 0.8)
d.t(514, PY2 + 162, "보조 인덱스", 11, OK, KR, "start", 600)

# 우측 이점 박스
d.box(710, PY2 + 66, 134, 108, PAPER2, RULE, 0.9, 4)
d.t(777, PY2 + 90, "핵심 이점: 느슨한 결합", 11, INK, KR, "middle", 600)
d.t(777, PY2 + 114, "소비자 장애 격리", 11, INK, KR, "middle")
d.t(777, PY2 + 134, "팀별 독립 배포 가능", 11, INK, KR, "middle")
d.t(777, PY2 + 154, "넓은 워크로드 수용", 11, MUTED, KR, "middle")

# 언번들드 화살표
d.arrow([(134, PY2 + 120), (150, PY2 + 120)], MUTED, "ar", 1.1)
d.arrow([(284, PY2 + 120), (302, PY2 + 120)], ACC, "acc", 1.2)
d.arrow([(478, PY2 + 82), (498, PY2 + 82)], OK, "ok", 1.2)
d.arrow([(478, PY2 + 120), (498, PY2 + 120)], OK, "ok", 1.2)
d.arrow([(478, PY2 + 158), (498, PY2 + 158)], OK, "ok", 1.2)

d.legend(LEG, [
    ("언번들드 쓰기 통합 (focal)", ACC),
    ("연합 쿼리 계층", INFO),
    ("파생 인덱스·뷰", OK),
    ("연합의 한계 (쓰기)", WARN),
])

d.save("13-02.federated-vs-unbundled.svg")
