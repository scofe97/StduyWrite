# 04-06 §2 전문 검색 — inverted index의 단어별 postings list 조회와 bitmap AND 연산 흐름.
# 사실 출처: 04-06 본문 L42~L50(§2 전문 검색: 단어 term이 차원, postings list, sparse bitmap 변환, "red apples" 두 bitmap의 bitwise AND 계산, Lucene 정렬 파일)
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 96, 316
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-06 · §2 INVERTED INDEX", "전문 검색 역색인과 비트맵 AND 연산",
      "키워드 질의는 각 단어의 postings list를 찾아 sparse bitmap으로 표현한 뒤, bitwise AND 연산으로 두 단어가 모두 포함된 문서를 찾는다.",
      "단어별 역색인 조회 → 비트맵 변환 → 비트 AND 연산 → 최종 일치 문서 도출 과정입니다.")

# 4개 단계 컬럼 (폭: 180, 간격: 36, X0: 26)
COL_W = 180
COL_GAP = 36
X0 = 26
xs = [X0 + i * (COL_W + COL_GAP) for i in range(4)]
# xs: [26, 242, 458, 674]

# 컬럼 헤더 4개
headers = [
    ("01 · 검색 질의", "두 키워드 질의어"),
    ("02 · 역색인 조회", "단어별 postings list"),
    ("03 · 비트맵 변환", "문서 순차 ID 비트열"),
    ("04 · 비트 AND 연산", "일치 문서 집합 도출"),
]

for i, (step_t, step_sub) in enumerate(headers):
    x = xs[i]
    is_focal = (i == 3)
    c = ACC if is_focal else INFO
    d.chip(x + COL_W / 2, PY + 14, step_t, c, 12)
    d.t(x + COL_W / 2, PY + 38, step_sub, 12, MUTED, KR, "middle")

# 데이터 박스들 (상단 레인: "red", 하단 레인: "apples")
Y_TOP = PY + 56
H_ROW = 88
Y_BOT = Y_TOP + H_ROW + 16

# --- 단계 1: 질의어 ---
d.box(xs[0], Y_TOP, COL_W, H_ROW, PAPER2, INFO, 1.0)
d.t(xs[0] + 16, Y_TOP + 28, "키워드 1", 12, SOFT, KR, "start")
d.t(xs[0] + 16, Y_TOP + 52, "\"red\"", 16, INK, MONO, "start", 600)
d.chip(xs[0] + COL_W - 44, Y_TOP + 24, "term x", INFO, 11)

d.box(xs[0], Y_BOT, COL_W, H_ROW, PAPER2, INFO, 1.0)
d.t(xs[0] + 16, Y_BOT + 28, "키워드 2", 12, SOFT, KR, "start")
d.t(xs[0] + 16, Y_BOT + 52, "\"apples\"", 16, INK, MONO, "start", 600)
d.chip(xs[0] + COL_W - 44, Y_BOT + 24, "term y", INFO, 11)

# 화살표 1 → 2 (수평)
d.arrow([(xs[0] + COL_W, Y_TOP + H_ROW / 2), (xs[1], Y_TOP + H_ROW / 2)], MUTED, "ar", 1.4)
d.arrow([(xs[0] + COL_W, Y_BOT + H_ROW / 2), (xs[1], Y_BOT + H_ROW / 2)], MUTED, "ar", 1.4)

# --- 단계 2: 역색인 postings list ---
d.box(xs[1], Y_TOP, COL_W, H_ROW, PAPER2, RULE, 1.0)
d.t(xs[1] + 16, Y_TOP + 26, "postings list (red)", 12, SOFT, KR, "start")
d.t(xs[1] + 16, Y_TOP + 50, "[doc 1, 3, 5]", 14, INK, MONO, "start", 600)
d.t(xs[1] + 16, Y_TOP + 70, "예시 문서 ID", 12, MUTED, KR, "start")

d.box(xs[1], Y_BOT, COL_W, H_ROW, PAPER2, RULE, 1.0)
d.t(xs[1] + 16, Y_BOT + 26, "postings list (apples)", 12, SOFT, KR, "start")
d.t(xs[1] + 16, Y_BOT + 50, "[doc 2, 3, 5]", 14, INK, MONO, "start", 600)
d.t(xs[1] + 16, Y_BOT + 70, "예시 문서 ID", 12, MUTED, KR, "start")

# 화살표 2 → 3 (수평)
d.arrow([(xs[1] + COL_W, Y_TOP + H_ROW / 2), (xs[2], Y_TOP + H_ROW / 2)], MUTED, "ar", 1.4)
d.arrow([(xs[1] + COL_W, Y_BOT + H_ROW / 2), (xs[2], Y_BOT + H_ROW / 2)], MUTED, "ar", 1.4)

# --- 단계 3: 비트맵 표현 ---
d.box(xs[2], Y_TOP, COL_W, H_ROW, PAPER2, RULE, 1.0)
d.t(xs[2] + 16, Y_TOP + 24, "sparse bitmap", 12, SOFT, MONO, "start")
d.t(xs[2] + 16, Y_TOP + 46, "1  0  1  0  1", 14, OK, MONO, "start", 600)
d.t(xs[2] + 16, Y_TOP + 68, "doc 1 2 3 4 5", 11, MUTED, MONO, "start")

d.box(xs[2], Y_BOT, COL_W, H_ROW, PAPER2, RULE, 1.0)
d.t(xs[2] + 16, Y_BOT + 24, "sparse bitmap", 12, SOFT, MONO, "start")
d.t(xs[2] + 16, Y_BOT + 46, "0  1  1  0  1", 14, OK, MONO, "start", 600)
d.t(xs[2] + 16, Y_BOT + 68, "doc 1 2 3 4 5", 11, MUTED, MONO, "start")

# 화살표 3 → 4 (직각 직진: 수평 → 수직 → 수평)
MID_X = (xs[2] + COL_W + xs[3]) / 2  # (638 + 674) / 2 = 656
Y1 = Y_TOP + H_ROW / 2               # 152 + 44 = 196
Y2 = Y_BOT + H_ROW / 2               # 256 + 44 = 300
TARGET_Y1 = 224
TARGET_Y2 = 272

d.arrow([(xs[2] + COL_W, Y1), (MID_X, Y1), (MID_X, TARGET_Y1), (xs[3], TARGET_Y1)], MUTED, "ar", 1.4)
d.arrow([(xs[2] + COL_W, Y2), (MID_X, Y2), (MID_X, TARGET_Y2), (xs[3], TARGET_Y2)], MUTED, "ar", 1.4)

# --- 단계 4: 비트 AND 연산 및 결과 (Focal ACC) ---
BOX4_H = H_ROW * 2 + 16
d.tone(xs[3], Y_TOP, COL_W, BOX4_H, ACC, 6, "14", 1.4)
d.t(xs[3] + COL_W / 2, Y_TOP + 24, "bitwise AND 연산", 13, ACC, KR, "middle", 600)

# 비트 AND 수식 박스
CALC_Y = Y_TOP + 38
d.box(xs[3] + 8, CALC_Y, COL_W - 16, 74, PAPER, RULE, 0.8)
d.t(xs[3] + 16, CALC_Y + 18, "1 0 1 0 1  (red)", 12, MUTED, MONO, "start")
d.t(xs[3] + 16, CALC_Y + 36, "0 1 1 0 1  (apples)", 12, MUTED, MONO, "start")
d.line(xs[3] + 14, CALC_Y + 44, xs[3] + COL_W - 14, CALC_Y + 44, RULE, 0.8)
d.t(xs[3] + 16, CALC_Y + 62, "0 0 1 0 1  (결과 비트)", 12, OK, MONO, "start", 600)

# 최종 일치 문서 목록
RES_Y = CALC_Y + 84
d.box(xs[3] + 8, RES_Y, COL_W - 16, 62, PAPER, OK, 1.2)
d.t(xs[3] + COL_W / 2, RES_Y + 22, "최종 일치 문서", 12, OK, KR, "middle", 600)
d.t(xs[3] + COL_W / 2, RES_Y + 44, "doc 3 · doc 5", 14, INK, MONO, "middle", 600)

# 하단 종합 요약 줄
d.box(X0, PY + PH - 38, W - X0 * 2, 32, PAPER2, RULE, 0.8)
d.t(W / 2, PY + PH - 18, "Lucene은 term → postings list 매핑을 SSTable식 정렬 파일에 저장하고 백그라운드 병합", 12, MUTED, KR, "middle")

d.legend(LEG, [("키워드 질의 및 역색인", INFO), ("비트맵 일치 비트", OK), ("최종 교집합 추출 (핵심)", ACC)])
d.save("04-06.inverted-index.svg")
