# 03-06 §3 — 영화 평점 관계형 테이블이 DataFrame을 통해 희소 행렬로 변환되고 ML 추천 알고리즘의 입력으로 이어지는 흐름.
# 사실 출처: 03-06 본문 §3, 원서 Ch.3 Figure 3-9(영화 평점의 행렬 변환, 행 100~104 발췌)와 그 뒤 문단(추천 시스템 예)
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 260
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-06 · DATAFRAME & MATRIX", "관계형 데이터의 행렬 변환과 ML 입력",
      "영화 평점 관계형 테이블을 DataFrame으로 피벗해 희소 행렬로 변환하고, 선형대수 연산을 거쳐 ML 알고리즘의 입력으로 잇는다.",
      "관계형 행 (평점) → 희소 행렬 (피벗) → 선형대수 및 ML 추천 모델")

# 1구역: 관계형 테이블 (movie_ratings)
d.box(16, PY, 240, PH, PAPER, RULE, 0.9)
d.t(28, 124, "관계형 테이블", 14, INK, KR, "start", 600)
d.chip(190, 122, "movie_ratings", INFO, 11)

d.box(28, 142, 216, 156, PAPER2, RULE, 0.8)
d.t(62, 160, "user_id", 11, MUTED, MONO, "middle")
d.t(134, 160, "movie_id", 11, MUTED, MONO, "middle")
d.t(204, 160, "rating", 11, MUTED, MONO, "middle")
d.line(28, 168, 244, 168, RULE, 0.8)

rows_r = [
    ("100", "12", "4"),
    ("100", "14", "5"),
    ("101", "10", "1"),
    ("101", "11", "3"),
    ("101", "13", "2"),
    ("102", "15", "4"),
    ("103", "13", "3"),
    ("104", "13", "3"),
    ("104", "14", "5"),
]
for idx, (uid, mid, rat) in enumerate(rows_r):
    ry = 182 + idx * 13
    d.t(62, ry, uid, 11, INK, MONO, "middle")
    d.t(134, ry, mid, 11, INK, MONO, "middle")
    d.t(204, ry, rat, 11, INK, MONO, "middle", 600)

d.t(136, 324, "사용자별 평점 행 단위 기록", 11, MUTED, KR, "middle")
d.t(136, 342, "관계형식 표현 · 그림 3-9 왼쪽", 11, MUTED, KR, "middle")

# 화살표 1: 관계형 → 희소 행렬
d.arrow([(256, 216), (292, 216)], MUTED, "ar", 1.4)
d.chip(274, 184, "피벗", ACC, 11)

# 2구역: 희소 행렬 (피벗) — Focal ACC
d.tone(296, PY, 324, PH, ACC, 6, "14", 1.4)
d.t(308, 124, "희소 행렬 (피벗)", 14, ACC, KR, "start", 600)
d.chip(546, 122, "NumPy · Pandas", ACC, 11)

d.box(308, 142, 300, 144, PAPER2, RULE, 0.8)
d.t(478, 158, "movies (열)", 11, MUTED, KR, "middle")
d.t(340, 174, "users", 11, MUTED, KR, "middle")

m_cols = ["10", "11", "12", "13", "14", "15"]
m_xs = [390, 426, 462, 498, 534, 570]
for mx, mlab in zip(m_xs, m_cols):
    d.t(mx, 174, mlab, 11, MUTED, MONO, "middle")

d.line(316, 182, 598, 182, RULE, 0.8)
d.line(366, 164, 366, 278, RULE, 0.8)

matrix_data = [
    ("100", ["·", "·", "4", "·", "5", "·"]),
    ("101", ["1", "3", "·", "2", "·", "·"]),
    ("102", ["·", "·", "·", "·", "·", "4"]),
    ("103", ["·", "·", "·", "3", "·", "·"]),
    ("104", ["·", "·", "·", "3", "5", "·"]),
]
for idx, (uid, vals) in enumerate(matrix_data):
    my = 200 + idx * 16
    d.t(340, my, uid, 11, INK, MONO, "middle")
    for mx, v in zip(m_xs, vals):
        c = ACC if v != "·" else SOFT
        w = 600 if v != "·" else 400
        d.t(mx, my, v, 11, c, MONO, "middle", w)

d.box(308, 294, 300, 54, PAPER, RULE, 0.8)
d.t(458, 314, "one-hot 인코딩 (장르) · 날짜 스케일링", 11, INK, KR, "middle")
d.t(458, 334, "빈 칸은 미평가 · 대규모 희소 배열 처리", 11, MUTED, KR, "middle")

# 화살표 2: 희소 행렬 → ML 알고리즘
d.arrow([(620, 216), (654, 216)], OK, "ok", 1.4)
d.chip(637, 184, "연산", OK, 11)

# 3구역: ML 알고리즘 입력
d.box(658, PY, 206, PH, PAPER, RULE, 0.9)
d.t(670, 124, "ML 모델 입력", 14, INK, KR, "start", 600)
d.chip(816, 122, "추천 모델", OK, 11)

d.box(670, 142, 182, 60, PAPER2, OK, 1.0)
d.t(761, 164, "선형대수 연산", 13, INK, KR, "middle", 600)
d.t(761, 184, "ML 알고리즘의 기반", 11, MUTED, KR, "middle")

d.arrow([(761, 202), (761, 222)], OK, "ok", 1.4)

d.box(670, 222, 182, 60, PAPER2, OK, 1.2)
d.t(761, 244, "영화 추천 시스템", 13, INK, KR, "middle", 600)
d.t(761, 264, "좋아할 만한 영화 추천", 11, MUTED, KR, "middle")

d.t(761, 314, "숫자 행렬이 학습 입력", 11, MUTED, KR, "middle")
d.chip(761, 338, "그림 3-9 데이터의 쓰임", OK, 11)

d.legend(LEG, [("관계형 테이블", INFO), ("DataFrame · 희소 행렬", ACC), ("선형대수 · ML 알고리즘", OK)])
d.save("03-06.dataframe-matrix.svg")
