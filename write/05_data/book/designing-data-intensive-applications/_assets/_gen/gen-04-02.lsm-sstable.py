# 04-02 §1 — 키로 정렬된 SSTable 파일 구조와 인메모리 sparse(희소) 인덱스 검색 메커니즘.
# 사실 출처: 04-02 본문 §1(L33~L39) — handbag·handsome 인덱스 엔트리, handiwork seek & scan 예시, 블록 압축.
# 키·byte offset 은 원서 Figure 4-2(p.5) 의 sparse index(handbag 102134 · handsome 104667 · hangout 106812)와 블록 키를 따른다. 값은 원서처럼 … 로 둔다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY = 100
PH = 384
LEG = PY + PH + 28
H = LEG + 56

d = D(W, H, "04-02 · §1 SSTABLE & SPARSE INDEX", "SSTable과 희소 인덱스 구조",
      "인메모리 희소 인덱스는 블록의 첫 키만 유지하고, 디스크 SSTable의 키 정렬 블록을 seek 및 순차 스캔하여 키를 조회한다.",
      "인메모리 희소 인덱스(첫 키 유지) · 디스크 불변 블록(정렬 데이터 및 압축)")

# 상단: 인메모리 희소 인덱스 영역
d.box(28, PY, 824, 96, PAPER2, INFO, 1.2)
d.chip(108, PY + 22, "인메모리 희소 인덱스", INFO, 12)
d.t(216, PY + 22, "블록 첫 키와 디스크 offset 만 메모리에 유지", 12, MUTED, KR, "start")

IX0 = 48
IW = 244
IGAP = 24
for i, (k, off) in enumerate([("handbag", "102134"), ("handsome", "104667"), ("hangout", "106812")]):
    ix = IX0 + i * (IW + IGAP)
    is_target = (i == 0)
    bc = ACC if is_target else RULE
    d.box(ix, PY + 42, IW, 42, PAPER, bc, 1.2 if is_target else 0.8)
    d.t(ix + 16, PY + 68, k, 13, INK, MONO, "start", 600)
    d.chip(ix + IW - 48, PY + 63, off, SOFT, 11)

# 하단: 디스크 SSTable 불변 파일 영역
d.box(28, 216, 824, 140, PAPER2, RULE, 1.0)
d.chip(104, 238, "디스크 SSTable 파일", MUTED, 12)
d.t(216, 238, "키로 정렬된 불변 데이터 블록 · 개별 블록 압축", 12, MUTED, KR, "start")

# 디스크 블록 3개
blocks = [
    ("블록 (offset 102134)", [("handbag", "…"), ("handful", "…")], [("handiwork", "…"), ("handoff", "…")], ACC, True),
    ("블록 (offset 104667)", [("handsome", "…"), ("handwaving", "…")], [("handwriting", "…")], RULE, False),
    ("블록 (offset 106812)", [("hangout", "…")], [], RULE, False),
]

for i, (b_title, row1, row2, bc, is_hit) in enumerate(blocks):
    bx = IX0 + i * (IW + IGAP)
    d.box(bx, 256, IW, 88, PAPER, bc, 1.4 if is_hit else 0.8)
    d.t(bx + 12, 276, b_title, 12, INK, KR, "start", 600)
    
    # 2행 분할 레코드
    r1_str = " · ".join(f"{k}:{v}" for k, v in row1)
    r2_str = " · ".join(f"{k}:{v}" for k, v in row2)
    d.t(bx + 12, 296, r1_str, 11, MUTED, MONO, "start")
    d.t(bx + 12, 314, r2_str, 11, OK if is_hit else MUTED, MONO, "start")
    
    # 압축 상태
    sub_tag = "handiwork 포함 · 압축 해제 스캔" if is_hit else "압축 데이터 블록"
    d.t(bx + 12, 332, sub_tag, 11, OK if is_hit else SOFT, KR, "start")

# 인덱스 -> 블록 연결 화살표
d.arrow([(IX0 + IW / 2, PY + 84), (IX0 + IW / 2, 254)], ACC, "acc", 1.4)
d.arrow([(IX0 + IW + IGAP + IW / 2, PY + 84), (IX0 + IW + IGAP + IW / 2, 254)], MUTED, "ar", 1.0)
d.arrow([(IX0 + (IW + IGAP) * 2 + IW / 2, PY + 84), (IX0 + (IW + IGAP) * 2 + IW / 2, 254)], MUTED, "ar", 1.0)

# 최하단: handiwork 검색 쿼리 트레이스
d.box(28, 376, 824, 96, PAPER2, ACC, 1.4)
d.chip(108, 398, "handiwork 검색 흐름", ACC, 12)

# 3컬럼 트레이스
d.t(48, 426, "1. 희소 인덱스 범위 확인", 13, INK, KR, "start", 600)
d.t(48, 448, "handbag ≤ handiwork < handsome", 12, MUTED, MONO, "start")

d.arrow([(292, 436), (320, 436)], ACC, "acc", 1.2)

d.t(336, 426, "2. handbag 블록 seek", 13, INK, KR, "start", 600)
d.t(336, 448, "offset 102134 이동 · 압축 해제", 12, MUTED, KR, "start")

d.arrow([(580, 436), (608, 436)], ACC, "acc", 1.2)

d.t(624, 426, "3. 블록 내 순차 스캔", 13, OK, KR, "start", 600)
d.t(624, 448, "정렬 순회로 handiwork 반환", 12, OK, KR, "start")

d.legend(LEG, [
    ("인메모리 인덱스", INFO),
    ("검색 경로 · 타깃 블록", ACC),
    ("스캔 성공 · 반환", OK),
    ("디스크 데이터 블록", RULE),
])

d.save("04-02.lsm-sstable.svg")
