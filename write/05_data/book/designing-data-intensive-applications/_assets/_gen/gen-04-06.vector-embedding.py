# 04-06 §3 벡터 임베딩 — 임베딩 모델을 통한 텍스트의 부동소수 벡터 변환과 의미 유사도 거리 측정.
# 사실 출처: 04-06 본문 §3 L63~L76(§3 벡터 임베딩: "구독 취소" ≈ "계정 닫기", 임베딩 모델 LLM, 농업 [0.38, 0.83, 0.41] vs 채소 [0.36, 0.64, 0.67] vs 별 스키마 [0.85, 0.10, -0.52], cosine 유사도·유클리드 거리)
# 타입 스펙: type-process
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 96, 316
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-06 · §3 VECTOR EMBEDDING", "임베딩 모델과 벡터 공간 유사도 거리",
      "임베딩 모델(LLM)이 입력 문서를 다차원 부동소수 벡터로 변환하며, 의미가 유사한 문서는 공간 내 거리가 가깝고 다른 문서는 멀어진다.",
      "텍스트 입력 → 모델 변환 → 다차원 벡터 생성 → 벡터 간 거리 측정 과정입니다.")

COL_W = 180
COL_GAP = 36
X0 = 26
xs = [X0 + i * (COL_W + COL_GAP) for i in range(4)]
# xs: [26, 242, 458, 674]

steps = [
    ("01 · 텍스트 입력", "서로 다른 어휘 문서"),
    ("02 · 임베딩 모델", "신경망 · LLM 변환"),
    ("03 · 벡터 임베딩", "다차원 부동소수 배열"),
    ("04 · 거리 측정", "의미 유사도 판정"),
]

for i, (st, sub) in enumerate(steps):
    x = xs[i]
    is_focal = (i == 3)
    c = ACC if is_focal else INFO
    d.chip(x + COL_W / 2, PY + 14, st, c, 12)
    d.t(x + COL_W / 2, PY + 38, sub, 12, MUTED, KR, "middle")

Y_DATA = PY + 56
H_DATA = 196

# 단계 1: 텍스트 입력 카드 3개
d.box(xs[0], Y_DATA, COL_W, H_DATA, PAPER2, RULE, 1.0)
d.t(xs[0] + COL_W / 2, Y_DATA + 22, "입력 텍스트 문서", 13, INK, KR, "middle", 600)

docs = [
    ("문서 A", "\"농업 위키 페이지\"", INFO),
    ("문서 B", "\"채소 재배 페이지\"", INFO),
    ("문서 C", "\"별 스키마 페이지\"", MUTED),
]
for j, (tag, title, col) in enumerate(docs):
    dy = Y_DATA + 38 + j * 50
    d.box(xs[0] + 10, dy, COL_W - 20, 42, PAPER, RULE, 0.8)
    d.t(xs[0] + 20, dy + 18, tag, 11, col, KR, "start", 600)
    d.t(xs[0] + 20, dy + 33, title, 12, INK, KR, "start")

# 단계 1 → 2 화살표
d.arrow([(xs[0] + COL_W, Y_DATA + H_DATA / 2), (xs[1], Y_DATA + H_DATA / 2)], MUTED, "ar", 1.4)

# 단계 2: 임베딩 모델
d.box(xs[1], Y_DATA, COL_W, H_DATA, PAPER2, INFO, 1.2)
d.t(xs[1] + COL_W / 2, Y_DATA + 24, "임베딩 모델 (LLM)", 13, INFO, KR, "middle", 600)

model_items = [
    ("언어 모델", "흔히 LLM 사용"),
    ("공간 위치", "다차원 공간의 한 점"),
    ("벡터 생성", "부동소수 좌표 출력"),
]
for j, (top_t, bot_t) in enumerate(model_items):
    my = Y_DATA + 44 + j * 48
    d.box(xs[1] + 12, my, COL_W - 24, 40, PAPER, RULE, 0.8)
    d.t(xs[1] + COL_W / 2, my + 17, top_t, 12, INK, KR, "middle", 600)
    d.t(xs[1] + COL_W / 2, my + 32, bot_t, 11, MUTED, KR, "middle")

# 단계 2 → 3 화살표
d.arrow([(xs[1] + COL_W, Y_DATA + H_DATA / 2), (xs[2], Y_DATA + H_DATA / 2)], MUTED, "ar", 1.4)

# 단계 3: 벡터 임베딩 (실제 값)
d.box(xs[2], Y_DATA, COL_W, H_DATA, PAPER2, RULE, 1.0)
d.t(xs[2] + COL_W / 2, Y_DATA + 22, "3차원 부동소수 벡터", 13, INK, KR, "middle", 600)

vectors = [
    ("벡터 A", "[0.38, 0.83, 0.41]", OK),
    ("벡터 B", "[0.36, 0.64, 0.67]", OK),
    ("벡터 C", "[0.85, 0.10, -0.52]", WARN),
]
for j, (tag, vec, col) in enumerate(vectors):
    vy = Y_DATA + 38 + j * 50
    d.box(xs[2] + 10, vy, COL_W - 20, 42, PAPER, RULE, 0.8)
    d.t(xs[2] + 18, vy + 17, tag, 11, col, KR, "start", 600)
    d.t(xs[2] + 18, vy + 33, vec, 11, INK, MONO, "start")

# 단계 3 → 4 화살표
d.arrow([(xs[2] + COL_W, Y_DATA + H_DATA / 2), (xs[3], Y_DATA + H_DATA / 2)], MUTED, "ar", 1.4)

# 단계 4: 거리 측정 및 유사도 판정 (Focal ACC)
d.tone(xs[3], Y_DATA, COL_W, H_DATA, ACC, 6, "14", 1.4)
d.t(xs[3] + COL_W / 2, Y_DATA + 24, "거리 & 유사도 비교", 13, ACC, KR, "middle", 600)

# 비교 1: A vs B (가까움)
d.box(xs[3] + 10, Y_DATA + 44, COL_W - 20, 64, PAPER, OK, 1.2)
d.t(xs[3] + 18, Y_DATA + 62, "벡터 A ↔ 벡터 B", 12, OK, KR, "start", 600)
d.t(xs[3] + 18, Y_DATA + 80, "거리 d ≈ 0.32 (가까움)", 12, INK, MONO, "start")
d.t(xs[3] + 18, Y_DATA + 98, "의미 유사 (농업 ≈ 채소)", 11, OK, KR, "start")

# 비교 2: A vs C (멉니다)
d.box(xs[3] + 10, Y_DATA + 118, COL_W - 20, 64, PAPER, WARN, 1.0)
d.t(xs[3] + 18, Y_DATA + 136, "벡터 A ↔ 벡터 C", 12, WARN, KR, "start", 600)
d.t(xs[3] + 18, Y_DATA + 154, "거리 d ≈ 1.27 (멂)", 12, INK, MONO, "start")
d.t(xs[3] + 18, Y_DATA + 172, "의미 상이 (무관한 주제)", 11, WARN, KR, "start")

# 하단 해설 상자
d.box(X0, PY + PH - 38, W - X0 * 2, 32, PAPER2, RULE, 0.8)
d.t(W / 2, PY + PH - 18, "동의어·오타를 넘어 코사인 유사도나 유클리드 거리로 의미적 유사 문서를 탐색", 12, MUTED, KR, "middle")

d.legend(LEG, [("텍스트 및 변환 모델", INFO), ("유사 벡터 (짧은 거리)", OK), ("상이 벡터 (먼 거리)", WARN), ("의미 유사도 판정 (핵심)", ACC)])
d.save("04-06.vector-embedding.svg")
