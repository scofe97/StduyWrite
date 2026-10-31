# 08-04 §3 — XA 이기종 분산 트랜잭션 아키텍처, 앱 내장 코디네이터, 로컬 로그와 단일 장애점(SPoF).
# 검증(10-31 cc-ddia-dverify08): 원서 p57~58 에 없는 XADataSource·XASession 을 빼고 본문 L64 "앱 서버가 죽으면 코디네이터도 함께 죽고"로 · 계층 제목 두 개가 x=250 화살표에 겹쳐 가운데로
# 사실 출처: 08-04 §3(L48~L58), 원서 Ch.8 "XA transactions" & "Problems with XA transactions"(PDF p.58~60)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
LEG = 556
H = LEG + 56

d = D(W, H, "08-04 §3 · XA TRANSACTION ARCHITECTURE", "XA 이기종 분산 트랜잭션 구조와 단일 장애점",
      "애플리케이션 프로세스 내장 코디네이터와 로컬 디스크 로그, 드라이버를 경유하는 이기종 참여자 구조와 근본적 한계를 보인다.",
      "애플리케이션 서버 내장 코디네이터 라이브러리가 로컬 디스크 로그를 사용하며 단일 장애점과 의심 상태 잠금 장기화를 유발한다.")

# 상단: 애플리케이션 서버 경계 (단일 장애점 SPoF)
d.box(30, 96, 820, 142, PAPER2, WARN, 1.2)
d.t(45, 116, "애플리케이션 서버 (단일 장애 지점 SPoF)", 12, WARN, KR, "start", 600)

# 앱 코드
d.box(50, 128, 230, 96, PAPER, RULE, 1.0)
d.t(165, 150, "애플리케이션 코드", 13, INK, KR, "middle", 600)
d.t(165, 172, "비즈니스 로직 실행", 12, MUTED, KR, "middle")
d.t(165, 192, "트랜잭션 시작 · 경계 제어", 12, MUTED, KR, "middle")
d.t(165, 210, "모든 통신의 경유 지점", 12, BAD, KR, "middle")

# 코디네이터 라이브러리
d.tone(310, 128, 250, 96, ACC, 6, "16", 1.4)
d.t(435, 150, "트랜잭션 코디네이터", 13, ACC, KR, "middle", 600)
d.t(435, 172, "JTA / XA API 구현 라이브러리", 12, INK, KR, "middle")
d.t(435, 192, "참여자 준비 · 커밋 조율", 12, MUTED, KR, "middle")
d.t(435, 210, "앱 프로세스 내 메모리 상주", 12, MUTED, KR, "middle")

# 로컬 디스크 로그
d.tone(590, 128, 240, 96, WARN, 6, "14", 1.2)
d.t(710, 150, "로컬 디스크 로그", 13, WARN, KR, "middle", 600)
d.t(710, 172, "트랜잭션 커밋 결정 영속화", 12, INK, KR, "middle")
d.t(710, 192, "서버 장애 시 코디네이터도 중단", 12, MUTED, KR, "middle")
d.t(710, 210, "로그 유실 시 수동 개입 필수", 12, BAD, KR, "middle")

# 앱 <-> 코디네이터, 코디네이터 -> 로컬 로그 화살표
d.arrow([(280, 176), (310, 176)], c=INFO, m="info")
d.arrow([(560, 176), (590, 176)], c=ACC, m="acc")

# 중단: 드라이버 계층
d.box(30, 254, 820, 62, PAPER2, RULE, 1.0)
d.t(440, 272, "드라이버 계층 (XA 인터페이스 콜백 브릿지)", 12, SOFT, KR, "middle", 600)

d.box(90, 278, 320, 30, PAPER, RULE, 0.8)
d.t(250, 298, "JDBC 드라이버 (DB)", 12, INFO, KR, "middle", 600)

d.box(470, 278, 320, 30, PAPER, RULE, 0.8)
d.t(630, 298, "JMS 드라이버 (브로커)", 12, INFO, KR, "middle", 600)

# 앱 코드 -> 드라이버 연결선
d.arrow([(165, 224), (165, 246), (250, 246), (250, 278)], c=MUTED, m="ar")
d.arrow([(165, 224), (165, 246), (630, 246), (630, 278)], c=MUTED, m="ar")

# 코디네이터와 자원 관리자 간 직접 통신 불가 경고 (드라이버와 자원 관리자 사이 여백)
d.tone(330, 324, 210, 24, BAD, 4, "18", 1.0)
d.t(435, 340, "직접 통신 불가 (앱 경유 필수)", 11, BAD, KR, "middle", 600)

# 하단: 이기종 참여자 (자원 관리자)
d.box(30, 356, 820, 108, PAPER2, OK, 1.1)
d.t(440, 374, "이기종 참여자 자원 관리자 (Resource Managers)", 12, OK, KR, "middle", 600)

d.box(90, 382, 320, 70, PAPER, OK, 1.0)
d.t(250, 402, "관계형 데이터베이스 (RDBMS)", 13, INK, KR, "middle", 600)
d.t(250, 422, "PostgreSQL · MySQL · Oracle", 12, MUTED, KR, "middle")
d.t(250, 439, "행 단위 배타 잠금 유지", 12, WARN, KR, "middle")

d.box(470, 382, 320, 70, PAPER, OK, 1.0)
d.t(630, 402, "메시지 브로커 (Message Broker)", 13, INK, KR, "middle", 600)
d.t(630, 422, "ActiveMQ · IBM MQ", 12, MUTED, KR, "middle")
d.t(630, 439, "메시지 수신 · 발행 원자성", 12, OK, KR, "middle")

# 드라이버 -> 자원 관리자 연결선
d.arrow([(250, 308), (250, 382)], c=OK, m="ok")
d.arrow([(630, 308), (630, 382)], c=OK, m="ok")

# 하단 결함 요약 배너
d.tone(30, 480, 820, 52, WARN, 6, "14", 1.2)
d.t(440, 502, "이기종 최소 공통 분모: 분산 교착 상태 감지 불가 · SSI 동시성 제어 미지원", 12, WARN, KR, "middle", 600)
d.t(440, 522, "비상 탈출구: 원자성을 의도적으로 깨뜨리는 휴리스틱 결정 위험 존재", 12, BAD, KR, "middle")

# 범례 (폭 880 초과 방지 위해 간결화)
d.legend(LEG, [
    ("앱 계층", INFO),
    ("코디네이터", ACC),
    ("로컬 로그", WARN),
    ("자원 관리자", OK),
    ("단일 장애점", BAD)
])

d.save("08-04.xa-transaction.svg")
