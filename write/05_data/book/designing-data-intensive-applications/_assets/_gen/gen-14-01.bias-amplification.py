# 14-01 §2 — 편향과 차별: 입력의 편향이 대리 변수와 머신러닝 규칙 추론을 거쳐 출력에서 증폭되는 데이터 흐름.
# 사실 출처: 14-01 본문 §2(L36~L45)·면접 질문 1(L87), 원서 Ch.14 "Bias and Discrimination" (PDF p.3)
# 10-31 검증(cc-ddia-dverify14): 본문 라벨의 (focal) 제거, 원서에 없는 'Bias Laundering'·'인과성 없는'·'공정성 보장'·§1 알고리즘 감옥 귀속을 본문 낱말로
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, WARN, BAD, OK, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 42
Y_STAGE = 148
H_STAGE = 154
Y_LOWER = 332
H_LOWER = 64
LEG = 418
H = LEG + 52

d = D(W, H, "14-01 · §2 DATA FLOW", "대리 변수를 통한 편향 증폭과 도덕적 상상력",
      "과거 차별 데이터가 대리 변수와 머신러닝 추론을 거쳐 편향 증폭된 출력으로 변환되는 데이터 흐름과 사람의 개입.",
      "차별적 과거 · 보호 특성과 상관된 변수 · 불투명한 규칙 추론 · 출력에서 편향 증폭 · 도덕적 상상력")

# 상단 공통 전제 배너 (중립 박스 적용으로 범례 색상 불일치 방지)
d.box(35, BANNER_Y, W - 70, BANNER_H, PAPER2, RULE, 1.0)
d.t(W / 2, BANNER_Y + 17, "규칙 자체를 데이터에서 추론: 입력의 체계적 편향을 학습·증폭", 13, INK, KR, "middle", 600)
d.t(W / 2, BANNER_Y + 33, "보호 특성과 상관된 변수 · 과거의 외삽 · 사람만 제공하는 도덕적 상상력", 12, MUTED, KR, "middle")

# 3단계 스테이지 기하 (SW=230, GAP=60, X0=35)
SW = 230
GAP = 60
X0 = 35
X1 = X0
X2 = X1 + SW + GAP
X3 = X2 + SW + GAP

# 스테이지 1: 입력 데이터 (WARN)
d.box(X1, Y_STAGE, SW, H_STAGE, PAPER2, WARN, 1.0)
d.chip(X1 + SW / 2, Y_STAGE + 16, "입력 데이터", WARN, 11, pad=5)
d.box(X1 + 10, Y_STAGE + 34, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X1 + SW / 2, Y_STAGE + 53, "문화적으로 제도화된 차별", 12, INK, KR, "middle", 600)
d.t(X1 + SW / 2, Y_STAGE + 71, "체계적 편향이 담긴 입력", 11, MUTED, KR, "middle")
d.box(X1 + 10, Y_STAGE + 90, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X1 + SW / 2, Y_STAGE + 109, "보호 특성과 상관된 변수", 12, WARN, KR, "middle", 600)
d.t(X1 + SW / 2, Y_STAGE + 127, "분리 지역의 우편번호·IP 주소", 11, MUTED, KR, "middle")

# 스테이지 1 → 2 연결 화살표 (간격 60px 내부 중앙 배치)
d.arrow([(X1 + SW, Y_STAGE + H_STAGE / 2), (X2, Y_STAGE + H_STAGE / 2)], c=MUTED, m="ar", sw=1.4)
d.t((X1 + SW + X2) / 2, Y_STAGE + H_STAGE / 2 - 8, "학습", 11, SOFT, KR, "middle")

# 스테이지 2: 규칙 추론 (ACC focal)
d.tone(X2, Y_STAGE, SW, H_STAGE, ACC, 6, "14", 1.4)
d.chip(X2 + SW / 2, Y_STAGE + 16, "규칙 추론", ACC, 11, pad=5)
d.box(X2 + 10, Y_STAGE + 34, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X2 + SW / 2, Y_STAGE + 53, "규칙을 데이터에서 추론", 12, INK, KR, "middle", 600)
d.t(X2 + SW / 2, Y_STAGE + 71, "이유를 모르는 상관관계", 11, MUTED, KR, "middle")
d.box(X2 + 10, Y_STAGE + 90, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X2 + SW / 2, Y_STAGE + 109, "편향을 위한 자금 세탁(풍자)", 12, ACC, KR, "middle", 600)
d.t(X2 + SW / 2, Y_STAGE + 127, "편향된 입력에서 공정한 출력 기대", 11, MUTED, KR, "middle")

# 스테이지 2 → 3 연결 화살표 (간격 60px 내부 중앙 배치)
d.arrow([(X2 + SW, Y_STAGE + H_STAGE / 2), (X3, Y_STAGE + H_STAGE / 2)], c=MUTED, m="ar", sw=1.4)
d.t((X2 + SW + X3) / 2, Y_STAGE + H_STAGE / 2 - 8, "자동 판정", 11, SOFT, KR, "middle")

# 스테이지 3: 출력 및 배제 (BAD)
d.box(X3, Y_STAGE, SW, H_STAGE, PAPER2, BAD, 1.0)
d.chip(X3 + SW / 2, Y_STAGE + 16, "출력", BAD, 11, pad=5)
d.box(X3 + 10, Y_STAGE + 34, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X3 + SW / 2, Y_STAGE + 53, "출력에서 편향 증폭", 12, INK, KR, "middle", 600)
d.t(X3 + SW / 2, Y_STAGE + 71, "과거 외삽 · 차별의 코드화", 11, MUTED, KR, "middle")
d.box(X3 + 10, Y_STAGE + 90, SW - 20, 50, PAPER, RULE, 0.6, r=4)
d.t(X3 + SW / 2, Y_STAGE + 109, "보호 특성의 간접 재구성", 12, BAD, KR, "middle", 600)
d.t(X3 + SW / 2, Y_STAGE + 127, "보호 특성 제거만으로 못 막는 차별", 11, MUTED, KR, "middle")

# 하단 교정 패널 (OK)
d.tone(X0, Y_LOWER, W - 70, H_LOWER, OK, 6, "14", 1.2)
d.t(X0 + 20, Y_LOWER + 20, "도덕적 상상력: 오직 사람만 제공", 12, OK, KR, "start", 600)
d.t(X0 + 20, Y_LOWER + 38, "미래가 과거보다 나아지길 원할 때 필요", 11, INK, KR, "start")
d.t(X0 + 20, Y_LOWER + 54, "데이터와 모델은 도구 · 주인이 아님", 11, MUTED, KR, "start")

# 교정 패널에서 규칙 추론(스테이지 2)으로의 피드백 화살표 (30px 수직 간격 내부 배치)
d.arrow([(X2 + SW / 2, Y_LOWER), (X2 + SW / 2, Y_STAGE + H_STAGE)], c=OK, m="ok", sw=1.4, dash="4 3")
d.t(X2 + SW / 2 + 48, (Y_LOWER + Y_STAGE + H_STAGE) / 2 + 4, "도덕적 개입", 11, OK, KR, "middle")

# 범례
d.legend(LEG, [
    ("입력의 편향", WARN),
    ("불투명 추론 (focal)", ACC),
    ("증폭된 출력", BAD),
    ("사람의 도덕적 상상력", OK)
])

d.save("14-01.bias-amplification.svg")
