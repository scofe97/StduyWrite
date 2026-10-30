# 04-06 §4 벡터 인덱스 — flat·IVF·HNSW 세 인덱스의 내부 저장 구조와 탐색 경로 비교.
# 사실 출처: 04-06 본문 L66~L76(§4 벡터 인덱스: flat 전수 비교, IVF centroid 클러스터링과 probe 파티션, HNSW 다층 근접 그래프 상위층→하위층 탐색, Faiss·pgvector)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 96, 324
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-06 · §4 VECTOR INDEX", "벡터 인덱스 3종 비교",
      "고차원 벡터는 R-tree 적용이 어려워 전체를 순차 비교하는 flat, 공간을 파티션으로 묶는 IVF, 다층 근접 그래프를 탐색하는 HNSW를 쓴다.",
      "flat(전수 탐색) · IVF(클러스터 파티션) · HNSW(다층 그래프 탐색)의 구조와 특성 비교입니다.")

CW = 264
GAP = 20
X0 = 24
xs = [X0 + i * (CW + GAP) for i in range(3)]
# xs: [24, 308, 592]

cards = [
    ("flat 인덱스", "전체 벡터 전수 비교", INFO, False),
    ("IVF (Inverted File)", "중심점 클러스터 분할", INFO, False),
    ("HNSW (계층 그래프)", "다층 근접 그래프 탐색", ACC, True),
]

for i, (title, sub, col, is_focal) in enumerate(cards):
    x = xs[i]
    if is_focal:
        d.tone(x, PY, CW, PH - 48, ACC, 6, "12", 1.4)
    else:
        d.box(x, PY, CW, PH - 48, PAPER2, RULE, 1.0)
    
    d.t(x + CW / 2, PY + 24, title, 14, INK if not is_focal else ACC, KR, "middle", 600)
    d.t(x + CW / 2, PY + 42, sub, 12, MUTED, KR, "middle")
    d.line(x + 12, PY + 52, x + CW - 12, PY + 52, RULE, 0.8)

# 상단 내부 박스 높이 84 (PY+60 ~ PY+144)
BOX_H = 84

# --- 카드 1: flat 인덱스 내부 ---
x1 = xs[0]
d.box(x1 + 12, PY + 60, CW - 24, BOX_H, PAPER, RULE, 0.8)
d.t(x1 + CW / 2, PY + 76, "벡터 원본 순차 배열", 12, SOFT, KR, "middle")

# 벡터 배열 박스들
for j, vname in enumerate(["v1", "v2", "v3", "..."]):
    vx = x1 + 24 + j * 54
    d.box(vx, PY + 86, 46, 24, PAPER2, INFO, 0.8)
    d.t(vx + 23, PY + 102, vname, 12, INK, MONO, "middle")

d.t(x1 + CW / 2, PY + 132, "질의 벡터와 모든 원소 거리 계산", 12, WARN, KR, "middle")

# 카드 1 특성 행들 (PY + 164 부터 시작)
flat_attrs = [
    ("탐색 방식", "모든 벡터 1:1 비교"),
    ("정확도", "정확"),
    ("검색 속도", "느림"),
    ("저장 방식", "벡터 그대로 저장"),
]
for j, (lbl, val) in enumerate(flat_attrs):
    ay = PY + 168 + j * 24
    d.t(x1 + 20, ay, lbl, 12, SOFT, KR, "start")
    d.t(x1 + CW - 20, ay, val, 12, INK if j != 2 else WARN, KR, "end", 600 if j == 1 else 400)


# --- 카드 2: IVF 인덱스 내부 ---
x2 = xs[1]
d.box(x2 + 12, PY + 60, CW - 24, BOX_H, PAPER, RULE, 0.8)
d.t(x2 + CW / 2, PY + 76, "Centroid 파티션 분할", 12, SOFT, KR, "middle")

# 파티션 3개 표시
for j, (pname, cnt) in enumerate([("파티션 1", "v1, v4"), ("파티션 2", "v2, v5"), ("파티션 3", "v3, v6")]):
    px = x2 + 20 + j * 76
    is_probe = (j == 1)
    if is_probe:
        d.tone(px, PY + 86, 72, 30, OK, 4, "20", 1.2)
        d.t(px + 36, PY + 100, pname, 11, OK, KR, "middle", 600)
        d.t(px + 36, PY + 111, cnt, 11, INK, MONO, "middle")
    else:
        d.box(px, PY + 86, 72, 30, PAPER2, RULE, 0.8)
        d.t(px + 36, PY + 100, pname, 11, SOFT, KR, "middle")
        d.t(px + 36, PY + 111, cnt, 11, MUTED, MONO, "middle")

d.t(x2 + CW / 2, PY + 132, "질의 근접 파티션만 탐색 (probe)", 12, OK, KR, "middle")

# 카드 2 특성 행들
ivf_attrs = [
    ("탐색 방식", "중심점 군집화 선별"),
    ("정확도", "근사 (다른 파티션 누락)"),
    ("검색 속도", "probe 많을수록 느림"),
    ("적용 라이브러리", "Faiss · pgvector"),
]
for j, (lbl, val) in enumerate(ivf_attrs):
    ay = PY + 168 + j * 24
    d.t(x2 + 20, ay, lbl, 12, SOFT, KR, "start")
    d.t(x2 + CW - 20, ay, val, 12, INK, KR, "end")


# --- 카드 3: HNSW 인덱스 내부 (Focal ACC) ---
x3 = xs[2]
d.box(x3 + 12, PY + 60, CW - 24, BOX_H, PAPER, ACC, 1.0)
d.t(x3 + CW / 2, PY + 76, "다층 근접 그래프", 12, ACC, KR, "middle", 600)

# 다층 그래프 3단계 표현
# Layer 2 (상층)
d.box(x3 + 20, PY + 85, 56, 16, PAPER2, ACC, 0.8)
d.t(x3 + 48, PY + 97, "L2 최상층", 11, ACC, KR, "middle")
d.arrow([(x3 + 80, PY + 93), (x3 + 114, PY + 93)], ACC, "acc", 1.2)
d.t(x3 + 124, PY + 97, "성긴 노드 · 진입", 11, MUTED, KR, "start")

# Layer 1 (중간층)
d.box(x3 + 20, PY + 104, 56, 16, PAPER2, RULE, 0.8)
d.t(x3 + 48, PY + 116, "L1 중간층", 11, SOFT, KR, "middle")
d.arrow([(x3 + 80, PY + 112), (x3 + 114, PY + 112)], MUTED, "ar", 1.2)
d.t(x3 + 124, PY + 116, "근접 노드로 하강", 11, MUTED, KR, "start")

# Layer 0 (최하층)
d.box(x3 + 20, PY + 123, 56, 16, PAPER2, OK, 0.8)
d.t(x3 + 48, PY + 135, "L0 밀집층", 11, OK, KR, "middle")
d.arrow([(x3 + 80, PY + 131), (x3 + 114, PY + 131)], OK, "ok", 1.2)
d.t(x3 + 124, PY + 135, "최근접 벡터 도달", 11, OK, KR, "start", 600)

# 카드 3 특성 행들
hnsw_attrs = [
    ("탐색 방식", "최상층부터 아래층으로"),
    ("정확도", "IVF처럼 근사"),
    ("최상층", "노드 적음"),
    ("적용 라이브러리", "Faiss · pgvector"),
]
for j, (lbl, val) in enumerate(hnsw_attrs):
    ay = PY + 168 + j * 24
    d.t(x3 + 20, ay, lbl, 12, SOFT, KR, "start")
    d.t(x3 + CW - 20, ay, val, 12, INK, KR, "end", 600 if j == 1 else 400)

# 하단 공통 요약 박스
d.box(X0, PY + PH - 38, W - X0 * 2, 32, PAPER2, RULE, 0.8)
d.t(W / 2, PY + PH - 18, "많은 벡터 DB 가 IVF 와 HNSW 를 구현 (Faiss 는 각각 여러 변형, pgvector 는 둘 다 지원)", 12, MUTED, KR, "middle")

d.legend(LEG, [("전수 탐색 인덱스", INFO), ("탐색이 닿는 곳", OK), ("다층 그래프 구조 (핵심)", ACC), ("속도 지연 요소", WARN)])
d.save("04-06.vector-index.svg")
