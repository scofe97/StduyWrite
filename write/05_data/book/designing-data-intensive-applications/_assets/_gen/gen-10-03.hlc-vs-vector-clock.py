# 10-03 §4 — 하이브리드 논리 시계(HLC)와 벡터 클럭 특성 및 트레이드오프 비교
# 사실 출처: 10-03 본문 §4(L71~L81), 원서 DDIA 2nd Edition Ch. 10 p.26~28
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 368
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "10-03 · §4 HLC VS VECTOR CLOCK", "하이브리드 논리 시계(HLC)와 벡터 클럭 비교",
      "물리 시각과 결합해 전순서를 만드는 HLC와 동시성을 탐지하는 벡터 클럭의 대조",
      "타임스탬프 구성 · 순서 보장 체계 · 동시성 탐지 능력 · 공간 오버헤드 · 주요 적용 시스템")

# 상단 공통 문제 배경 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "인과성 추적의 두 갈래: 물리 시각을 결합한 HLC 대 동시성을 탐지하는 벡터 클럭", 12, INK, KR, "middle", 600)

CW = 404
GAP = 24
X0 = 24

cols = [
    ("하이브리드 논리 시계 (HLC)", "물리 시각 결합 · 전순서", INFO, [
        ("구성", "물리 시각(ms) + Lamport 논리 카운터", "작은 고정 크기 · 벽시계 형태 판독 가능"),
        ("순서", "전순서(Total Order) 제공", "happens-before 와 일관"),
        ("동시성", "동시(concurrent) 이벤트 직접 식별 불가", "임의 순서화 · 동시 여부 판별 한계"),
        ("비용", "고정 크기 타임스탬프", "벡터보다 공간 적음"),
        ("활용", "CockroachDB 분산 트랜잭션 타임스탬프", "인과적 일관성 갖춘 MVCC 스냅샷 ID"),
    ]),
    ("벡터 클럭 (Vector Clock)", "동시성 탐지 · 부분 순서", OK, [
        ("구성", "노드별 카운터 배열 [N₁, N₂, …]", "노드 수(N)에 비례하는 정수 벡터 크기"),
        ("순서", "부분 순서(Partial Order) 제공", "인과 선행과 동시 사건 구분"),
        ("동시성", "동시(concurrent) 이벤트 탐지", "어느 쪽도 앞서지 않는 독립 분기 식별"),
        ("비용", "노드 수 비례 공간 오버헤드 O(N)", "대규모 노드 환경에서 메시지 크기 부담"),
        ("활용", "다중 리더 복제 쓰기 충돌 감지", "06-05 참조"),
    ]),
]

for i, (title, subtitle, col_c, rows) in enumerate(cols):
    x = X0 + i * (CW + GAP)

    # 열 외곽 상자
    d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)

    # 열 헤더
    d.chip(x + 48, PY + 25, "HLC" if i == 0 else "VECTOR", col_c, 11)
    d.t(x + CW / 2 + 20, PY + 28, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 48, subtitle, 11, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)

    # 5개 행 비교 항목
    for j, (dim, top_txt, bot_txt) in enumerate(rows):
        iy = PY + 66 + j * 58
        is_focal_cell = (i == 1 and j == 2)  # Vector Clock 동시성 탐지 완벽
        is_hlc_focal = (i == 0 and j == 4)   # CockroachDB MVCC 스냅샷

        if is_focal_cell:
            d.tone(x + 10, iy, CW - 20, 50, ACC, 5, "22", 1.3)
            d.chip(x + 46, iy + 25, dim, ACC, 11)
            d.t(x + 82, iy + 20, top_txt, 11, ACC, KR, "start", 600)
            d.t(x + 82, iy + 38, bot_txt, 11, INK, KR, "start")
        elif is_hlc_focal:
            d.tone(x + 10, iy, CW - 20, 50, INFO, 5, "18", 1.2)
            d.chip(x + 46, iy + 25, dim, INFO, 11)
            d.t(x + 82, iy + 20, top_txt, 11, INFO, KR, "start", 600)
            d.t(x + 82, iy + 38, bot_txt, 11, INK, KR, "start")
        else:
            d.box(x + 10, iy, CW - 20, 50, PAPER, RULE, 0.8)
            d.chip(x + 46, iy + 25, dim, col_c if j == 0 else SOFT, 11)
            d.t(x + 82, iy + 20, top_txt, 11, INK, KR, "start", 600)
            d.t(x + 82, iy + 38, bot_txt, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("HLC 특성", INFO),
    ("벡터 클럭 특성", OK),
    ("동시성 탐지 (focal)", ACC),
])

d.save("10-03.hlc-vs-vector-clock.svg")
