# 04-04 §1 — 기본키 인덱스(유일 키)와 보조 인덱스(비유일 키)의 차이 및 중복 키 해결 두 방식(postings list vs 행 ID 덧붙임).
# 사실 출처: 04-04 본문 §1(L36~L40), DDIA 2판 Ch.4 "Secondary Indexes"(원서 PDF 20쪽). 기본키 쪽 예시(user_id=251 기본키·Alice)는 보조 인덱스 컬럼과 겹치고 근거가 없어 2026-10-30 검증에서 바꿈
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 96
PH = 308
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "04-04 · SECONDARY INDEX", "보조 인덱스와 비유일 키 해소",
      "기본키는 행을 유일 식별하지만 보조 인덱스는 한 키에 여러 행이 대응하므로, postings list나 행 ID 덧붙임으로 유일성을 확보한다.",
      "기본키 1:1 매핑 대 보조 인덱스 1:N 매핑(postings list · 행 ID 덧붙임)")

# 좌측: 기본키 인덱스 영역
LEFT_W = 272
d.box(24, PY, LEFT_W, PH, PAPER2, RULE, 0.9)
d.chip(24 + LEFT_W / 2, PY + 22, "기본키 인덱스 (1:1 매핑)", INFO, 12)
d.t(24 + LEFT_W / 2, PY + 46, "유일 키로 단일 행 직접 식별", 12, SOFT, KR, "middle")
d.line(38, PY + 58, 24 + LEFT_W - 14, PY + 58, RULE, 0.8)

# 기본키 검색 예
d.box(40, PY + 72, LEFT_W - 32, 54, PAPER, RULE, 0.8)
d.t(40 + (LEFT_W - 32) / 2, PY + 92, "검색 키 (PK)", 12, MUTED, KR, "middle")
d.t(40 + (LEFT_W - 32) / 2, PY + 112, "id = 1", 13, INK, MONO, "middle", 600)

d.arrow([(24 + LEFT_W / 2, PY + 128), (24 + LEFT_W / 2, PY + 152)], INFO, "info", 1.4)
d.t(24 + LEFT_W / 2 + 42, PY + 144, "1:1 매핑", 12, INFO, KR, "start")

# 기본키 리프 항목
d.box(40, PY + 154, LEFT_W - 32, 60, PAPER, INFO, 1.2)
d.t(40 + (LEFT_W - 32) / 2, PY + 175, "인덱스 리프 항목", 12, INFO, KR, "middle", 600)
d.t(40 + (LEFT_W - 32) / 2, PY + 196, "1 → row_1", 13, INK, MONO, "middle")

d.arrow([(24 + LEFT_W / 2, PY + 216), (24 + LEFT_W / 2, PY + 238)], MUTED, "ar", 1.4)

# 실제 테이블 행
d.box(40, PY + 240, LEFT_W - 32, 52, PAPER, MUTED, 1.1)
d.t(40 + (LEFT_W - 32) / 2, PY + 260, "테이블 행", 12, SOFT, KR, "middle", 600)
d.t(40 + (LEFT_W - 32) / 2, PY + 278, "row_1 (한 행)", 12, INK, MONO, "middle")


# 우측: 보조 인덱스 영역
RIGHT_X = 312
RIGHT_W = 544
d.box(RIGHT_X, PY, RIGHT_W, PH, PAPER2, ACC, 1.2)
d.chip(RIGHT_X + RIGHT_W / 2, PY + 22, "보조 인덱스 (1:N 비유일 키 검색)", ACC, 12)
d.t(RIGHT_X + RIGHT_W / 2, PY + 46, "동일한 키에 여러 행이 매칭되는 문제 해결", 12, SOFT, KR, "middle")
d.line(RIGHT_X + 16, PY + 58, RIGHT_X + RIGHT_W - 16, PY + 58, RULE, 0.8)

# 검색 대상: positions 테이블
d.box(RIGHT_X + 16, PY + 70, RIGHT_W - 32, 46, PAPER, RULE, 0.8)
d.t(RIGHT_X + 28, PY + 96, "보조 키 검색:", 12, MUTED, KR, "start")
d.t(RIGHT_X + 118, PY + 96, "user_id = 251", 13, ACC, MONO, "start", 600)
d.t(RIGHT_X + RIGHT_W - 28, PY + 96, "일치 행: row_1 · row_3 · row_7 (3건)", 12, INK, MONO, "end")

# 두 방식 분할 박스
BOX_W = 248
Y_SOL = PY + 128
H_SOL = 164

# 해결 방식 1: postings list
d.box(RIGHT_X + 16, Y_SOL, BOX_W, H_SOL, PAPER, RULE, 0.9)
d.chip(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 20, "방식 1. postings list", WARN, 12)
d.t(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 42, "값에 행 식별자 리스트 저장", 12, WARN, KR, "middle")
d.line(RIGHT_X + 28, Y_SOL + 52, RIGHT_X + 4 + BOX_W, Y_SOL + 52, RULE, 0.6)

d.box(RIGHT_X + 26, Y_SOL + 62, BOX_W - 20, 48, PAPER2, WARN, 1.0)
d.t(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 81, "Key: 251", 12, INK, MONO, "middle")
d.t(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 98, "Value: [row_1, row_3, row_7]", 12, WARN, MONO, "middle", 600)

d.t(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 126, "전문 인덱스 postings list 처럼", 12, MUTED, KR, "middle")
d.t(RIGHT_X + 16 + BOX_W / 2, Y_SOL + 146, "값 하나에 행 식별자 여럿", 12, SOFT, KR, "middle")

# 해결 방식 2: 행 ID 덧붙임
d.box(RIGHT_X + 32 + BOX_W, Y_SOL, BOX_W, H_SOL, PAPER, RULE, 0.9)
d.chip(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 20, "방식 2. 행 ID 덧붙임", OK, 12)
d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 42, "복합키로 각 항목 고유화", 12, OK, KR, "middle")
d.line(RIGHT_X + 44 + BOX_W, Y_SOL + 52, RIGHT_X + 20 + 2 * BOX_W, Y_SOL + 52, RULE, 0.6)

d.box(RIGHT_X + 42 + BOX_W, Y_SOL + 60, BOX_W - 20, 56, PAPER2, OK, 1.0)
d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 78, "Key: (251, row_1) → ∅", 12, INK, MONO, "middle")
d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 94, "Key: (251, row_3) → ∅", 12, INK, MONO, "middle")
d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 110, "Key: (251, row_7) → ∅", 12, INK, MONO, "middle")

d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 132, "모든 항목이 고유 키로 변환", 12, MUTED, KR, "middle")
d.t(RIGHT_X + 32 + BOX_W + BOX_W / 2, Y_SOL + 150, "B-tree · LSM 키-값 엔진 적재", 12, SOFT, KR, "middle")

d.legend(LEG, [("기본키 인덱스", INFO), ("보조 인덱스", ACC), ("postings list", WARN), ("행 ID 덧붙임", OK)])
d.save("04-04.secondary-index.svg")
