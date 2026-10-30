# 04-02 §4 — size-tiered와 leveled compaction의 계층 구조 및 읽기·쓰기 trade-off 비교.
# 사실 출처: 04-02 본문 §4(L84~L88) — size-tiered의 누적 병합과 높은 쓰기 처리량, leveled의 L0~L2 키 범위 분할과 읽기 효율성.
# 수치·키 범위는 원서 §Compaction strategies 예: 256 MB SSTable 넷 → 898 MB 하나, L1 의 a–m · n–z. L2 칸의 범위 경계는 분할 모양을 보이는 예시다.
# 타입 스펙: type-layers
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 96
PH = 392
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-02 · §4 COMPACTION STRATEGIES", "size-tiered와 leveled compaction 구조 비교",
      "size-tiered는 소형 세그먼트를 대형 세그먼트로 누적 병합하고, leveled는 고정 크기 세그먼트를 레벨별 키 범위로 분할 관리한다.",
      "쓰기 최적화 size-tiered(누적 병합) · 읽기 최적화 leveled(키 범위 분할)")

PW = 400
X_LEFT = 28
X_RIGHT = 452

# 좌측 패널: size-tiered compaction
d.box(X_LEFT, PY, PW, PH, PAPER2, RULE, 1.0)
d.chip(X_LEFT + 80, PY + 22, "size-tiered", INFO, 12)
d.t(X_LEFT + 148, PY + 22, "크기 기준 누적 병합 · 쓰기 위주 최적화", 12, MUTED, KR, "start")

# 1. Tier 0: 소형 SSTable (수 MB) 4개
d.box(X_LEFT + 16, PY + 42, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_LEFT + 28, PY + 60, "Tier 0 (신규 세그먼트)", 12, INK, KR, "start", 600)
for k in range(4):
    d.box(X_LEFT + 28 + k * 88, PY + 70, 80, 26, PAPER2, INFO, 0.8, r=3)
    d.t(X_LEFT + 68 + k * 88, PY + 87, "256 MB", 11, INFO, MONO, "middle")

# 병합 화살표 1
d.arrow([(X_LEFT + PW / 2, PY + 106), (X_LEFT + PW / 2, PY + 128)], MUTED, "ar", 1.2)
d.t(X_LEFT + PW / 2 + 10, PY + 120, "누적 순차 병합", 11, MUTED, KR, "start")

# 2. Tier 1: 중형 SSTable (수십 MB) 2개
d.box(X_LEFT + 16, PY + 130, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_LEFT + 28, PY + 148, "Tier 1 (중간 세그먼트)", 12, INK, KR, "start", 600)
d.box(X_LEFT + 28, PY + 158, 348, 26, PAPER2, RULE, 0.8, r=3)
d.t(X_LEFT + 202, PY + 175, "898 MB SSTable · 삭제·덮어쓰기로 1,024 MB 미만", 11, INK, KR, "middle")

# 병합 화살표 2
d.arrow([(X_LEFT + PW / 2, PY + 194), (X_LEFT + PW / 2, PY + 216)], MUTED, "ar", 1.2)
d.t(X_LEFT + PW / 2 + 10, PY + 208, "누적 대형 병합", 11, MUTED, KR, "start")

# 3. Tier 2: 대형 SSTable (수백 MB) 1개
d.box(X_LEFT + 16, PY + 218, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_LEFT + 28, PY + 236, "Tier 2 (오래된 데이터)", 12, INK, KR, "start", 600)
d.box(X_LEFT + 28, PY + 246, PW - 56, 26, PAPER2, WARN, 0.9, r=3)
d.t(X_LEFT + PW / 2, PY + 263, "더 크고 오래된 SSTable", 11, WARN, KR, "middle")

# 특성 요약 박스
d.box(X_LEFT + 16, PY + 292, PW - 32, 88, PAPER, RULE, 0.8)
d.t(X_LEFT + 28, PY + 312, "설계 장단점 및 특성", 12, INK, KR, "start", 600)
d.t(X_LEFT + 28, PY + 332, "장점: 큰 순차 쓰기로 높은 쓰기 처리량 달성", 11, OK, KR, "start")
d.t(X_LEFT + 28, PY + 350, "단점: 병합 시 여유 디스크 공간 많이 소모", 11, WARN, KR, "start")
d.t(X_LEFT + 28, PY + 368, "적합: 쓰기 비중이 압도적인 워크로드", 11, MUTED, KR, "start")


# 우측 패널: leveled compaction (focal: ACC)
d.box(X_RIGHT, PY, PW, PH, PAPER2, ACC, 1.4)
d.chip(X_RIGHT + 64, PY + 22, "leveled", ACC, 12)
d.t(X_RIGHT + 124, PY + 22, "레벨별 키 범위 분할 · 읽기 위주 최적화", 12, MUTED, KR, "start")

# 1. Level 0: 최근 flush 세그먼트 (키 중첩 허용)
d.box(X_RIGHT + 16, PY + 42, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_RIGHT + 28, PY + 60, "L0 (가장 최근 데이터)", 12, INK, KR, "start", 600)
for k in range(3):
    d.box(X_RIGHT + 28 + k * 118, PY + 70, 110, 26, PAPER2, ACC, 0.8, r=3)
    d.t(X_RIGHT + 83 + k * 118, PY + 87, f"L0-{k+1}", 11, ACC, KR, "middle")

# 병합 화살표 1
d.arrow([(X_RIGHT + PW / 2, PY + 106), (X_RIGHT + PW / 2, PY + 128)], ACC, "acc", 1.2)
d.t(X_RIGHT + PW / 2 + 10, PY + 120, "키 범위별 분할 병합", 11, ACC, KR, "start")

# 2. Level 1: 10MB 고정 크기 (키 범위 비중첩)
d.box(X_RIGHT + 16, PY + 130, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_RIGHT + 28, PY + 148, "L1 (고정 크기 · 키 범위 분할)", 12, INK, KR, "start", 600)
l1_ranges = ["a ~ m", "n ~ z"]
for k, rng in enumerate(l1_ranges):
    d.box(X_RIGHT + 28 + k * 118, PY + 158, 110, 26, PAPER2, OK, 0.8, r=3)
    d.t(X_RIGHT + 83 + k * 118, PY + 175, f"[{rng}]", 11, OK, MONO, "middle")

# 병합 화살표 2
d.arrow([(X_RIGHT + PW / 2, PY + 194), (X_RIGHT + PW / 2, PY + 216)], ACC, "acc", 1.2)
d.t(X_RIGHT + PW / 2 + 10, PY + 208, "임계 초과 시 하위 레벨 전이", 11, ACC, KR, "start")

# 3. Level 2: 100MB 레벨 (키 범위 비중첩)
d.box(X_RIGHT + 16, PY + 218, PW - 32, 64, PAPER, RULE, 0.9)
d.t(X_RIGHT + 28, PY + 236, "L2 (L1 보다 큰 크기 한도)", 12, INK, KR, "start", 600)
l2_ranges = ["a ~ d", "e ~ k", "l ~ s", "t ~ z"]
for k, rng in enumerate(l2_ranges):
    d.box(X_RIGHT + 24 + k * 88, PY + 246, 82, 26, PAPER2, RULE, 0.8, r=3)
    d.t(X_RIGHT + 65 + k * 88, PY + 263, f"[{rng}]", 10, INK, MONO, "middle")

# 특성 요약 박스
d.box(X_RIGHT + 16, PY + 292, PW - 32, 88, PAPER, RULE, 0.8)
d.t(X_RIGHT + 28, PY + 312, "설계 장단점 및 특성", 12, INK, KR, "start", 600)
d.t(X_RIGHT + 28, PY + 332, "장점: 키 확인에 더 적은 SSTable 읽기", 11, OK, KR, "start")
d.t(X_RIGHT + 28, PY + 350, "장점: 점진적 병합 · size-tiered 보다 디스크 덜 사용", 11, OK, KR, "start")
d.t(X_RIGHT + 28, PY + 368, "적합: 읽기 비중이 지배적인 워크로드", 11, MUTED, KR, "start")

d.legend(LEG, [
    ("size-tiered", INFO),
    ("leveled (focal)", ACC),
    ("키 범위 격리", OK),
    ("대용량 부담", WARN),
])

d.save("04-02.compaction-strategies.svg")
