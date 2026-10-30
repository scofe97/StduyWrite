# 04-03 §3 — B-tree와 LSM의 읽기·쓰기 성능 특성 및 SSD 하드웨어 동작 비교 격자.
# 사실 출처: 04-03 본문 §3(L54~L60) — B-tree 레벨당 1페이지 예측성, 범위 쿼리 단순·빠름, LSM Bloom 필터 완화, 전 세그먼트 스캔, 순차 vs 랜덤 쓰기 처리량, SSD flash 페이지 쓰기·블록 지우기 GC 마모.
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LX, LW = 24, 140
CX0, CW, CGAP = 184, 328, 16
HY, HH = 104, 52
RY0, RSTR, RH = 168, 64, 52
LEG = 440
H = LEG + 56

d = D(W, H, "04-03 · READ AND WRITE COMPARISON", "B-tree와 LSM 읽기·쓰기 동작 비교",
      "읽기 예측성과 범위 쿼리는 B-tree가 우수하고, 순차 쓰기 처리량과 SSD 마모 완화는 LSM이 우수하다.",
      "단건 조회 · 범위 쿼리 · 디스크 쓰기 패턴 · SSD 하드웨어 영향 4대 축 비교")

cols = [
    ("B-tree", "고정 페이지 제자리 갱신", INFO),
    ("LSM-tree", "불변 세그먼트 순차 쓰기", ACC),
]

rows = [
    ("단건 키 조회",
     [("레벨당 1페이지 탐색", "3~4 레벨로 빠르고 예측 가능", OK),
      ("Memtable 및 다중 SSTable", "Bloom 필터로 불필요 I/O 완화", WARN)]),
    ("범위 쿼리",
     [("정렬 리프 순차 스캔", "형제 포인터 순회로 단순·빠름", OK),
      ("전 세그먼트 병렬 스캔 병합", "Bloom 필터 효과 미미", WARN)]),
    ("디스크 쓰기",
     [("키 분산 랜덤 쓰기", "흩어진 페이지 덮어쓰기·낮은 처리량", WARN),
      ("세그먼트 통째 순차 쓰기", "높은 쓰기 대역폭 활용", OK)]),
    ("SSD 하드웨어",
     [("페이지 쓰기 · 블록 단위 소거", "랜덤 쓰기 GC 부담 · 마모 가속", WARN),
      ("세그먼트 순차 쓰기", "GC 부담 적음 · 마모 덜함", OK)]),
]

# 열 헤더
for k, (name, sub, c) in enumerate(cols):
    x = CX0 + k * (CW + CGAP)
    is_focal = (k == 1)
    if is_focal:
        d.box(x, HY, CW, HH, PAPER2, ACC, 1.4)
        d.t(x + CW / 2, HY + 22, name, 13, ACC, MONO, "middle", 600)
        d.t(x + CW / 2, HY + 40, sub, 12, MUTED, KR, "middle")
    else:
        d.box(x, HY, CW, HH, PAPER2, RULE, 1.0)
        d.t(x + CW / 2, HY + 22, name, 13, INK, MONO, "middle", 600)
        d.t(x + CW / 2, HY + 40, sub, 12, MUTED, KR, "middle")

# 데이터 행
for r, (label, cells) in enumerate(rows):
    y = RY0 + r * RSTR
    d.t(LX, y + 30, label, 13, INK, KR, "start", 600)
    for k, (main_txt, sub_txt, status_c) in enumerate(cells):
        x = CX0 + k * (CW + CGAP)
        is_focal_cell = (k == 1 and r == 2)  # LSM 순차 쓰기가 핵심 논점
        if is_focal_cell:
            d.tone(x, y, CW, RH, ACC, 6, "20", 1.4)
            d.t(x + CW / 2, y + 22, main_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, y + 40, sub_txt, 11, ACC, KR, "middle")
        else:
            d.box(x, y, CW, RH, PAPER, RULE, 0.9)
            d.t(x + CW / 2, y + 22, main_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, y + 40, sub_txt, 11, status_c, KR, "middle")

d.legend(LEG, [
    ("핵심 성능 우위 (순차 쓰기)", ACC),
    ("구조적 적합·유리", OK),
    ("추가 비용·완화 필요", WARN),
    ("엔진 식별", INFO)
])

d.save("04-03.read-write-tradeoff.svg")
