# 04-01 §1 — 세상에서 가장 단순한 데이터베이스(두 bash 함수)의 쓰기(db_set)와 읽기(db_get) 데이터 흐름.
# 사실 출처: 04-01 §1(L35~L55), 원서 Ch.4 §The World's Simplest Database(`cat database` 세 줄).
# offset 0·60·125 는 그 세 줄의 바이트 길이로 계산한 값이다(60 은 원서 Figure 4-1 과 같다).
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY1 = 104
PY2 = 188
PY3 = 352
LEG = 452
H = LEG + 56

d = D(W, H, "04-01 · APPEND-ONLY LOG", "가장 단순한 데이터베이스의 쓰기와 읽기 흐름",
      "db_set은 파일 끝에 레코드를 순차 추가해 빠르고, db_get은 최신 값을 찾기 위해 파일 전체를 처음부터 순차 스캔한다.",
      "파일 끝 추가 쓰기 · 전체 파일 스캔 읽기 O(n)")

# --- 1. db_set 쓰기 경로 (Track 1) ---
d.box(24, PY1, 248, 64, PAPER2, RULE, 0.9)
d.t(36, PY1 + 22, "db_set 쓰기 요청", 13, INK, KR, "start", 600)
d.t(36, PY1 + 40, "db_set 42 '{...[\"Exploratorium\"]}'", 11, MUTED, MONO, "start")
d.t(36, PY1 + 54, "키 42 신규 값 전달", 12, OK, KR, "start")

d.arrow([(272, PY1 + 32), (396, PY1 + 32)], OK, "ok", 1.4)
d.t(334, PY1 + 22, "echo >> database", 11, OK, MONO, "middle")

d.tone(400, PY1, 456, 64, OK, 6, "18", 1.2)
d.t(412, PY1 + 22, "파일 끝(EOF) 순차 추가", 13, OK, KR, "start", 600)
d.t(412, PY1 + 40, "기존 값을 덮어쓰지 않고 파일 끝에 즉시 기록", 12, MUTED, KR, "start")
d.t(412, PY1 + 54, "파일 추가 · 일반적으로 효율적", 12, OK, KR, "start")

# --- 2. database 파일 레코드 시퀀스 (Track 2) ---
d.box(24, PY2, 832, 144, PAPER2, RULE, 1.0)
d.t(40, PY2 + 22, "append-only 데이터 파일 (database)", 13, INK, KR, "start", 600)
d.t(320, PY2 + 22, "줄 단위 키-값 쌍 텍스트 파일 · append-only 시퀀스", 12, SOFT, KR, "start")

# Row 0
d.box(40, PY2 + 32, 712, 32, PAPER, RULE, 0.8)
d.chip(96, PY2 + 48, "offset 0", INFO, 11)
d.t(148, PY2 + 52, "12,{\"name\":\"London\",\"attractions\":[\"Big Ben\",...]}", 11, MUTED, MONO, "start")
d.t(740, PY2 + 52, "키 12 등록", 12, MUTED, KR, "end")

# Row 1
d.box(40, PY2 + 68, 712, 32, PAPER, RULE, 0.8)
d.chip(96, PY2 + 84, "offset 60", INFO, 11)
d.t(148, PY2 + 88, "42,{\"name\":\"San Francisco\",\"attractions\":[\"Golden Gate Bridge\"]}", 11, MUTED, MONO, "start")
d.t(740, PY2 + 88, "키 42 옛 값", 12, MUTED, KR, "end")

# Row 2 (Focal)
d.tone(40, PY2 + 104, 712, 32, ACC, 6, "20", 1.4)
d.chip(96, PY2 + 120, "offset 125", ACC, 11)
d.t(148, PY2 + 124, "42,{\"name\":\"San Francisco\",\"attractions\":[\"Exploratorium\"]}", 11, INK, MONO, "start")
d.t(740, PY2 + 124, "키 42 최신 버전", 12, ACC, KR, "end")

# Track 1 -> Track 2 하향 연결 (신규 레코드 부착)
d.arrow([(788, PY1 + 64), (788, PY2 + 120), (756, PY2 + 120)], ACC, "acc", 1.4)
d.t(776, PY1 + 80, "신규 레코드 부착", 12, ACC, KR, "end")

# --- 3. db_get 읽기 경로 (Track 3) ---
d.box(24, PY3, 216, 76, PAPER2, RULE, 0.9)
d.t(36, PY3 + 24, "db_get 조회 요청", 13, INK, KR, "start", 600)
d.t(36, PY3 + 44, "db_get 42", 11, INK, MONO, "start")
d.t(36, PY3 + 62, "키 42 최신값 검색", 12, MUTED, KR, "start")

d.arrow([(240, PY3 + 38), (280, PY3 + 38)], SOFT, "soft", 1.3)

d.tone(284, PY3, 280, 76, WARN, 6, "18", 1.2)
d.t(296, PY3 + 24, "grep 전체 순차 스캔", 13, WARN, KR, "start", 600)
d.t(296, PY3 + 44, "grep \"^42,\" database", 11, WARN, MONO, "start")
d.t(296, PY3 + 62, "파일 처음부터 끝까지 · O(n)", 12, WARN, KR, "start")

d.arrow([(564, PY3 + 38), (640, PY3 + 38)], SOFT, "soft", 1.3)
d.t(602, PY3 + 28, "결과 전달", 12, SOFT, KR, "middle")

d.tone(644, PY3, 212, 76, OK, 6, "18", 1.2)
d.t(656, PY3 + 24, "tail -n 1 최신값 추출", 13, OK, KR, "start", 600)
d.t(656, PY3 + 44, "tail -n 1", 11, OK, MONO, "start")
d.t(656, PY3 + 62, "마지막 등장 레코드 반환", 12, OK, KR, "start")

d.legend(LEG, [("최신 레코드 (focal)", ACC), ("db_set 쓰기", OK), ("db_get 스캔", WARN), ("기존 레코드", INFO)])
d.save("04-01.append-only-log.svg")
