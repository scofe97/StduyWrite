# 08-04 §5 — 메시지 ID와 DB 내부 트랜잭션 기반 정확히-한-번(exactly-once) 멱등 처리 흐름도.
# 검증(10-31 cc-ddia-dverify08): 단계 번호 1~6 이 바로 옆 본문 목록 1~4 와 어긋나 번호를 뺌
# 사실 출처: 08-04 §5(L78~L89), 원서 Ch.8 "Exactly-Once Message Processing Revisited"(PDF p.61~62)
# 타입 스펙: type-flowchart
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 472
H = LEG + 56

d = D(W, H, "08-04 §5 · EXACTLY-ONCE VIA IDEMPOTENCE", "메시지 식별자와 DB 내부 트랜잭션 기반 멱등 처리 흐름",
      "분산 트랜잭션 없이 메시지 고유 식별자 검사와 단일 데이터베이스 내부 트랜잭션으로 장애 재시도 중복을 거르는 절차를 보인다.",
      "메시지 고유 ID를 데이터베이스 처리 테이블에 원자적으로 기록하여 장애 재시도 시 중복 처리를 차단한다.")

# 1. 메시지 수신
d.box(30, 105, 170, 68, PAPER, INFO, 1.1)
d.t(115, 127, "메시지 수신", 13, INK, KR, "middle", 600)
d.t(115, 147, "브로커 메시지 수신", 12, MUTED, KR, "middle")
d.t(115, 163, "고유 메시지 ID 포함", 12, INFO, KR, "middle")

# 1 -> 2 화살표
d.arrow([(200, 139), (230, 139)], c=MUTED, m="ar")

# 2. DB 트랜잭션 오픈
d.box(230, 105, 180, 68, PAPER, INFO, 1.1)
d.t(320, 127, "DB 트랜잭션 시작", 13, INK, KR, "middle", 600)
d.t(320, 147, "단일 DB 트랜잭션 오픈", 12, MUTED, KR, "middle")
d.t(320, 163, "처리 테이블 식별자 조회", 12, INFO, KR, "middle")

# 2 -> 3 화살표
d.arrow([(410, 139), (440, 139)], c=MUTED, m="ar")

# 3. 식별자 존재 분기 검사
d.tone(440, 102, 180, 74, ACC, 6, "16", 1.4)
d.t(530, 125, "식별자 검사", 13, ACC, KR, "middle", 600)
d.t(530, 145, "이미 처리된 메시지인가?", 12, INK, KR, "middle")
d.t(530, 163, "처리 테이블 ID 존재 여부", 12, MUTED, KR, "middle")

# 3 -> 4Y 화살표 (YES 분기)
d.arrow([(620, 139), (670, 139)], c=WARN, m="warn")
d.t(645, 131, "YES", 11, WARN, MONO, "middle")

# 4Y. 중복 건너뛰기
d.tone(670, 105, 180, 68, WARN, 6, "14", 1.2)
d.t(760, 127, "중복 처리 건너뛰기", 13, WARN, KR, "middle", 600)
d.t(760, 147, "비즈니스 로직 실행 생략", 12, INK, KR, "middle")
d.t(760, 163, "브로커 즉시 ACK (멱등 완료)", 12, OK, KR, "middle")

# 3 -> 4N 화살표 (NO 분기)
d.arrow([(530, 176), (530, 202), (350, 202), (350, 218)], c=OK, m="ok")
d.t(545, 192, "NO", 11, OK, MONO, "start")

# 4N. 식별자 기록 및 비즈니스 처리
d.box(230, 218, 240, 68, PAPER, OK, 1.1)
d.t(350, 240, "식별자 및 결과 기록", 13, INK, KR, "middle", 600)
d.t(350, 260, "처리 테이블에 메시지 ID 삽입", 12, OK, KR, "middle")
d.t(350, 276, "처리 결과를 동일 트랜잭션 기록", 12, MUTED, KR, "middle")

# 4N -> 5N 화살표
d.arrow([(470, 252), (500, 252)], c=OK, m="ok")

# 5N. DB 트랜잭션 커밋
d.tone(500, 218, 190, 68, OK, 6, "16", 1.4)
d.t(595, 240, "DB 트랜잭션 커밋", 13, OK, KR, "middle", 600)
d.t(595, 260, "WAL 디스크 기록 확정", 12, INK, KR, "middle")
d.t(595, 276, "ID와 쓰기 결과 원자적 확정", 12, OK, KR, "middle")

# 5N -> 6N 화살표
d.arrow([(690, 252), (720, 252)], c=OK, m="ok")

# 6N. 브로커 ACK
d.box(720, 218, 130, 68, PAPER, OK, 1.1)
d.t(785, 240, "브로커 ACK", 13, INK, KR, "middle", 600)
d.t(785, 260, "확인 응답 전송", 12, MUTED, KR, "middle")
d.t(785, 276, "메시지 큐 소비 완료", 12, OK, KR, "middle")

# 하단: 장애 발생 및 재시도 시 안전성 보장 박스
d.box(30, 314, 820, 130, PAPER2, RULE, 1.0)
d.t(45, 334, "장애 발생 및 재시도 시 안전성 보장 (멱등성 원리)", 12, INK, KR, "start", 600)

# 좌측 카드: 커밋 전 장애
d.tone(50, 348, 370, 80, BAD, 4, "12", 1.0)
d.t(235, 370, "커밋 전 장애 발생 (Rollback)", 13, BAD, KR, "middle", 600)
d.t(235, 390, "DB 트랜잭션 롤백으로 메시지 ID 미기록", 12, INK, KR, "middle")
d.t(235, 410, "브로커 재전달 시 식별자 미존재 → 정상 처리", 12, MUTED, KR, "middle")

# 우측 카드: 커밋 후 ACK 전 장애
d.tone(460, 348, 370, 80, WARN, 4, "12", 1.0)
d.t(645, 370, "커밋 후 ACK 전 장애 발생 (Redelivery)", 13, WARN, KR, "middle", 600)
d.t(645, 390, "DB 커밋 완료 · 브로커 ACK 미도달로 재전달 유발", 12, INK, KR, "middle")
d.t(645, 410, "브로커 재전달 시 식별자 이미 존재 → 중복 건너뜀", 12, OK, KR, "middle")

# 범례
d.legend(LEG, [
    ("정상 처리 단계", INFO),
    ("식별자 분기", ACC),
    ("멱등 건너뛰기", WARN),
    ("원자 커밋 확정", OK),
    ("장애 롤백 복구", BAD)
])

d.save("08-04.exactly-once-idempotence.svg")
