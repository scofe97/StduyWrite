# 06-02 §3 — 동일 쓰기 연산에 대한 statement 기반, WAL shipping, logical(row-based) 로그의 전송 내용과 결합도 비교.
# 사실 출처: 06-02 §3(L56~L63), 원서 Ch.6 "Implementation of Replication Logs"
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 600
LEG = H - 56

d = D(W, H, "06-02 §3 · REPLICATION LOG FORMATS", "복제 로그 세 방식의 전송 데이터와 결합도 비교",
      "리더의 쓰기를 팔로워에 보내는 statement, WAL shipping, logical 세 방식의 로그 내용과 결합도 비교.",
      "SQL 문 전송 · 디스크 바이트 · 행 단위 변경과 결합도 분리")

# 상단 공통 쓰기 연산 박스
d.box(24, 104, W - 48, 42, PAPER2, INFO, 1.0)
d.chip(92, 125, "리더의 쓰기", INFO, 11)
d.t(480, 129, "리더가 처리한 쓰기를 팔로워에 보내는 로그 형태 셋", 12, INK, KR, "middle", 600)

# 3단 비교 컬럼
c_w = 264
c_h = 330
c_y = 158

# 1. statement 기반 복제
x0 = 24
d.box(x0, c_y, c_w, c_h, PAPER2, RULE, 0.9)
d.t(x0 + c_w / 2, c_y + 24, "statement 기반 복제", 13, INK, KR, "middle", 600)
d.chip(x0 + c_w / 2, c_y + 46, "SQL 문 그대로 전송", SOFT, 11)
d.line(x0 + 12, c_y + 58, x0 + c_w - 12, c_y + 58, RULE, 0.8)

d.box(x0 + 12, c_y + 68, c_w - 24, 88, PAPER, SOFT, 0.8)
d.t(x0 + 20, c_y + 88, "INSERT · UPDATE · DELETE", 11, INK, MONO, "start", 600)
d.t(x0 + 20, c_y + 108, "리더가 실행한 쓰기 문 그대로", 12, INK, KR, "start")
d.t(x0 + 20, c_y + 128, "팔로워가 SQL 파싱·실행", 12, MUTED, KR, "start")

y_c0 = c_y + 172
d.t(x0 + c_w / 2, y_c0 + 20, "비결정 함수(NOW, RAND) 불일치", 12, WARN, KR, "middle")
d.t(x0 + c_w / 2, y_c0 + 44, "autoincrement 순서 의존성", 12, INK, KR, "middle")
d.t(x0 + c_w / 2, y_c0 + 68, "트리거·저장 프로시저 부작용", 12, MUTED, KR, "middle")
d.t(x0 + c_w / 2, y_c0 + 92, "VoltDB · MySQL 5.1 전", 12, SOFT, KR, "middle")

# 2. WAL shipping (물리 복제)
x1 = 308
d.box(x1, c_y, c_w, c_h, PAPER2, RULE, 0.9)
d.t(x1 + c_w / 2, c_y + 24, "WAL shipping (물리)", 13, INK, KR, "middle", 600)
d.chip(x1 + c_w / 2, c_y + 46, "디스크 블록 바이트 전송", INFO, 11)
d.line(x1 + 12, c_y + 58, x1 + c_w - 12, c_y + 58, RULE, 0.8)

d.box(x1 + 12, c_y + 68, c_w - 24, 88, PAPER, INFO, 0.8)
d.t(x1 + 20, c_y + 88, "WAL 저수준 기록", 12, INFO, KR, "start", 600)
d.t(x1 + 20, c_y + 108, "어느 디스크 블록의", 12, INK, KR, "start")
d.t(x1 + 20, c_y + 128, "어느 바이트가 바뀌었나", 12, INK, KR, "start")
d.t(x1 + 20, c_y + 146, "팔로워가 동일한 파일 생성", 12, MUTED, KR, "start")

y_c1 = c_y + 172
d.t(x1 + c_w / 2, y_c1 + 20, "저장 엔진 내부 구조와 강결합", 12, WARN, KR, "middle")
d.t(x1 + c_w / 2, y_c1 + 44, "leader·follower 다른 버전 불가", 12, INK, KR, "middle")
d.t(x1 + c_w / 2, y_c1 + 68, "무중단 업그레이드 막힘", 12, WARN, KR, "middle")
d.t(x1 + c_w / 2, y_c1 + 92, "PostgreSQL · Oracle 물리 복제", 12, SOFT, KR, "middle")

# 3. logical (row 기반) 로그 (FOCAL)
x2 = 592
d.tone(x2, c_y, c_w, c_h, ACC, 6, "18", 1.4)
d.t(x2 + c_w / 2, c_y + 24, "logical (row 기반) 로그", 13, INK, KR, "middle", 600)
d.chip(x2 + c_w / 2, c_y + 46, "행 단위 변경 이벤트", ACC, 11)
d.line(x2 + 12, c_y + 58, x2 + c_w - 12, c_y + 58, ACC, 0.8)

d.box(x2 + 12, c_y + 68, c_w - 24, 88, PAPER, ACC, 0.8)
d.t(x2 + 20, c_y + 88, "행 단위 변경 레코드", 12, ACC, KR, "start", 600)
d.t(x2 + 20, c_y + 108, "삽입 = 모든 열의 새 값", 12, INK, KR, "start")
d.t(x2 + 20, c_y + 128, "삭제 = 행 식별 정보", 12, INK, KR, "start")
d.t(x2 + 20, c_y + 146, "갱신 = 식별 정보 + 바뀐 값", 12, INK, KR, "start")

y_c2 = c_y + 172
d.t(x2 + c_w / 2, y_c2 + 20, "저장 엔진 내부 구현과 분리", 12, OK, KR, "middle", 600)
d.t(x2 + c_w / 2, y_c2 + 44, "leader·follower 버전 혼재 가능", 12, OK, KR, "middle")
d.t(x2 + c_w / 2, y_c2 + 68, "최소 다운타임 업그레이드", 12, OK, KR, "middle")
d.t(x2 + c_w / 2, y_c2 + 92, "외부 파싱 쉬움 → CDC(12장)", 12, SOFT, KR, "middle")

# 하단 결합도 분리 이점 요약 박스
d.box(24, 502, W - 48, 32, PAPER2, OK, 1.0)
d.t(W / 2, 522, "logical 로그: 저장 엔진과 분리 · 최소 다운타임 업그레이드 · CDC", 12, OK, KR, "middle", 600)

d.legend(LEG, [("logical 로그 (focal)", ACC), ("WAL shipping", INFO), ("방식의 약점", WARN), ("결합도 분리 이점", OK)])
d.save("06-02.replication-logs.svg")
