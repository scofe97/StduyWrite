# 06-01 §1 단일 리더 구조 — 리더의 로컬 쓰기와 복제 로그 스트림 전파 및 팔로워 읽기 분담 구조.
# 사실 출처: 06-01 본문 §1(L27~L39), DDIA 2판 6장 Figure 6-1 "Single-leader replication"
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 104
PH = 280
LEG = 474
H = LEG + 56

d = D(W, H, "06-01 · §1 ARCHITECTURE", "단일 리더 복제의 쓰기·읽기 경로와 복제 로그",
      "클라이언트는 모든 쓰기를 단일 리더로 보내 로컬 저장소에 선행 기록하고, 리더는 변경 스트림을 모든 팔로워로 전파하며 읽기 질의는 모든 노드가 분담한다.",
      "클라이언트 쓰기 전담 · 로컬 저장소 기록 · 복제 로그 스트림 전파 · 팔로워 읽기 분산 서빙")

# 1. 클라이언트 계층
d.box(28, PY, 188, PH, PAPER2, RULE, 0.9)
d.chip(28 + 94, PY + 18, "클라이언트 계층", MUTED, 11)

# 쓰기 클라이언트
d.tone(42, PY + 38, 160, 96, ACC, 6, "18", 1.2)
d.t(42 + 80, PY + 62, "쓰기 클라이언트", 13, INK, KR, "middle", 600)
d.t(42 + 80, PY + 82, "모든 쓰기는 리더로 집중", 12, ACC, KR, "middle")
d.box(42 + 6, PY + 94, 148, 26, PAPER, ACC, 0.8)
d.t(42 + 80, PY + 111, "UPDATE users ...", 11, INK, MONO, "middle")

# 읽기 클라이언트
d.tone(42, PY + 154, 160, 96, OK, 6, "18", 1.2)
d.t(42 + 80, PY + 178, "읽기 클라이언트", 13, INK, KR, "middle", 600)
d.t(42 + 80, PY + 198, "어느 노드에서나 조회 가능", 12, OK, KR, "middle")
d.box(42 + 6, PY + 210, 148, 26, PAPER, OK, 0.8)
d.t(42 + 80, PY + 227, "SELECT * FROM ...", 11, INK, MONO, "middle")

# 2. 리더 노드 (FOCAL)
d.box(268, PY, 246, PH, PAPER2, ACC, 1.4)
d.chip(268 + 123, PY + 18, "리더 노드 (Primary)", ACC, 11)
d.t(268 + 123, PY + 40, "쓰기 전담 및 복제 로그 생성", 12, SOFT, KR, "middle")

# 리더 내부: 로컬 저장소
d.box(284, PY + 52, 214, 88, PAPER, RULE, 0.9)
d.t(284 + 107, PY + 74, "로컬 DB 저장소", 13, INK, KR, "middle", 600)
d.t(284 + 107, PY + 94, "새 데이터 로컬 디스크 우선 기록", 12, MUTED, KR, "middle")
d.tone(284 + 14, PY + 104, 186, 24, INFO, 4, "16", 0.9)
d.t(284 + 107, PY + 120, "picture_url = 'me-new.jpg'", 11, INFO, MONO, "middle")

# 리더 내부: 복제 로그 엔진
d.box(284, PY + 168, 214, 88, PAPER, RULE, 0.9)
d.t(284 + 107, PY + 190, "복제 로그 (Change Stream)", 13, INK, KR, "middle", 600)
d.t(284 + 107, PY + 210, "데이터 변경 · user_id 1234", 12, MUTED, KR, "middle")
d.tone(284 + 14, PY + 220, 186, 24, ACC, 4, "20", 0.9)
d.t(284 + 107, PY + 236, "me-old.jpg → me-new.jpg", 11, ACC, MONO, "middle")

# 리더 내부 수직 화살표
d.arrow([(284 + 107, PY + 140), (284 + 107, PY + 166)], ACC, "acc", 1.4)

# 3. 팔로워 계층
d.box(564, PY, 288, PH, PAPER2, RULE, 0.9)
d.chip(564 + 144, PY + 18, "팔로워 계층 (Read Replicas)", INFO, 11)
d.t(564 + 144, PY + 40, "복제 로그 순차 적용 및 읽기 전용 질의 분담", 12, SOFT, KR, "middle")

# 팔로워 1
d.box(580, PY + 52, 256, 98, PAPER, RULE, 0.9)
d.chip(580 + 52, PY + 70, "팔로워 1", INFO, 11)
d.t(580 + 162, PY + 72, "읽기 전용 (Read-Only)", 12, MUTED, KR, "middle")
d.t(580 + 128, PY + 96, "복제 로그 수신 및 동일 순서 적용", 12, INK, KR, "middle")
d.tone(580 + 12, PY + 110, 232, 26, OK, 4, "16", 0.9)
d.t(580 + 128, PY + 127, "읽기 질의 서빙 가능 (사본 동기화)", 12, OK, KR, "middle")

# 팔로워 2
d.box(580, PY + 162, 256, 98, PAPER, RULE, 0.9)
d.chip(580 + 52, PY + 180, "팔로워 2", INFO, 11)
d.t(580 + 162, PY + 182, "읽기 전용 (Read-Only)", 12, MUTED, KR, "middle")
d.t(580 + 128, PY + 206, "복제 로그 수신 및 동일 순서 적용", 12, INK, KR, "middle")
d.tone(580 + 12, PY + 220, 232, 26, OK, 4, "16", 0.9)
d.t(580 + 128, PY + 237, "읽기 질의 서빙 가능 (사본 동기화)", 12, OK, KR, "middle")

# 4. 연결 화살표
# 쓰기 요청: 쓰기 클라이언트 -> 리더 로컬 저장소
d.arrow([(202, PY + 86), (282, PY + 86)], ACC, "acc", 1.5)
d.t(242, PY + 74, "쓰기 요청", 12, ACC, KR, "middle", 600)

# 복제 로그 스트림: 리더 복제 로그 -> 팔로워 1 & 팔로워 2
# Follower 1 (Y=PY+101)
d.arrow([(498, PY + 212), (538, PY + 212), (538, PY + 101), (578, PY + 101)], INFO, "info", 1.4)
# Follower 2 (Y=PY+212)
d.arrow([(498, PY + 212), (578, PY + 212)], INFO, "info", 1.4)
d.box(512, PY + 146, 52, 22, fill=PAPER, stroke=RULE, sw=0.8, r=4)
d.t(538, PY + 161, "복제 로그", 11, INFO, KR, "middle", 600)

# 읽기 질의: 읽기 클라이언트 -> 팔로워 노드로 분산
y_route = PY + PH + 14
d.arrow([(202, PY + 202), (238, PY + 202), (238, y_route), (708, y_route), (708, PY + 262)], OK, "ok", 1.4)
d.t(470, y_route + 17, "읽기 질의 (Read Query)", 12, OK, KR, "middle", 600)

# 5. 하단 구현 사례 배너
d.tone(24, 422, W - 48, 34, INFO, 4, "12", 0.9)
d.t(W / 2, 443, "적용 사례: PostgreSQL · MySQL · Oracle Data Guard · Always On · MongoDB · Kafka · Raft 기반 합의", 12, INK, KR, "middle", 500)

d.legend(LEG, [("리더 쓰기 전담 (focal)", ACC), ("복제 로그 스트림", INFO), ("읽기 질의 분산 서빙", OK), ("클라이언트 요청", MUTED)])
d.save("06-01.single-leader.svg")
