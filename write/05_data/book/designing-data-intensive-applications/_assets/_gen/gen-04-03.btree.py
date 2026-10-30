# 04-03 §1 — 고정 크기 페이지로 구성된 B-tree 구조와 키 251 조회 시 루트에서 리프로 이어지는 계층 탐색 경로.
# 사실 출처: 04-03 본문 §1(L35~L46) — 4~16 KiB 고정 크기 페이지, 루트 페이지, 키 251 조회 시 200–300 범위 분기, 리프 페이지 도달, 분기 계수 수백, O(log n) 깊이.
# 경계 키는 원서 Figure 4-5(p.12): 루트 100·200·300·400·500, 200–300 페이지 210·230·250·270·290, 100–200 페이지 111·135·152·169·190, 리프 250·251·252… 값은 원서처럼 val.
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 464
LEG = 416

d = D(W, H, "04-03 · B-TREE PAGE TREE", "B-tree 고정 크기 페이지 계층 트리",
      "4 KiB 고정 크기 페이지를 키 범위로 분할하고 루트에서 리프로 포인터를 따라 키 251을 탐색한다.",
      "루트 노드 · 내부 노드 · 리프 노드와 키 251 조회 경로")

# 1. 특성 배지 (우측 상단)
d.box(624, 104, 232, 72, PAPER2, RULE, 0.9)
d.t(636, 126, "B-tree 구조 특성", 12, INK, KR, "start", 600)
d.t(636, 146, "분기 계수: 수백 개 자식 참조", 12, MUTED, KR, "start")
d.t(636, 164, "대개 3~4 레벨 · 4레벨에 최대 250 TB", 12, MUTED, KR, "start")

# 2. Level 0: 루트 페이지 (Page 1)
RX, RY, RW, RH = 220, 104, 380, 72
d.box(RX, RY, RW, RH, PAPER2, INFO, 1.2)
d.t(RX + 16, RY + 24, "루트 페이지 (4 KiB)", 12, INFO, KR, "start", 600)

# 루트 슬롯 4개
slots_r = [
    ("< 100", RX + 14, 76, False),
    ("100–200", RX + 98, 84, False),
    ("200–300", RX + 190, 92, True),   # 키 251 경로
    ("300–400", RX + 290, 76, False)
]
for txt, sx, sw, is_path in slots_r:
    if is_path:
        d.tone(sx, RY + 36, sw, 26, ACC, 4, "20", 1.4)
        d.t(sx + sw / 2, RY + 53, txt, 11, ACC, MONO, "middle", 600)
    else:
        d.box(sx, RY + 36, sw, 26, PAPER, RULE, 0.8, 4)
        d.t(sx + sw / 2, RY + 53, txt, 11, MUTED, MONO, "middle")

# 3. 루트 -> 내부 노드 연결선 (직각)
# 좌측 자식 (Page 12)
d.arrow([(RX + 140, RY + RH), (RX + 140, RY + RH + 16), (124, RY + RH + 16), (124, 216)], SOFT, "soft", 1.2)
# 중앙 자식 (Page 24 - 키 251 경로)
d.arrow([(RX + 236, RY + RH), (RX + 236, 216)], ACC, "acc", 1.6)
# 우측 자식 (Page 35)
d.arrow([(RX + 328, RY + RH), (RX + 328, RY + RH + 16), (756, RY + RH + 16), (756, 216)], SOFT, "soft", 1.2)

# 4. Level 1: 내부 페이지들
# 좌측 내부 페이지
d.box(24, 216, 200, 68, PAPER2, RULE, 0.9)
d.t(36, 236, "내부 페이지 (100–200)", 12, INK, KR, "start", 600)
d.box(36, 248, 176, 24, PAPER, RULE, 0.8, 4)
d.t(124, 264, "111·135·152·169·190", 11, MUTED, MONO, "middle")

# 중앙 내부 페이지 (Page 24 - 키 251 포함)
CX, CY, CW, CH = 260, 216, 360, 68
d.box(CX, CY, CW, CH, PAPER2, INFO, 1.2)
d.t(CX + 16, CY + 22, "내부 페이지 (200–300)", 12, INFO, KR, "start", 600)

slots_c = [
    ("230–250", CX + 16, 96, False),
    ("250–270", CX + 120, 120, True),   # 키 251 경로
    ("270–290", CX + 248, 96, False)
]
for txt, sx, sw, is_path in slots_c:
    if is_path:
        d.tone(sx, CY + 32, sw, 26, ACC, 4, "20", 1.4)
        d.t(sx + sw / 2, CY + 49, txt, 11, ACC, MONO, "middle", 600)
    else:
        d.box(sx, CY + 32, sw, 26, PAPER, RULE, 0.8, 4)
        d.t(sx + sw / 2, CY + 49, txt, 11, MUTED, MONO, "middle")

# 우측 내부 페이지
d.box(656, 216, 200, 68, PAPER2, RULE, 0.9)
d.t(668, 236, "내부 페이지 (300–400)", 12, INK, KR, "start", 600)
d.box(668, 248, 176, 24, PAPER, RULE, 0.8, 4)
d.t(756, 264, "…", 11, MUTED, MONO, "middle")

# 5. 내부 노드 -> 리프 노드 연결선 (직각)
# 좌측 리프 (Page 51)
d.arrow([(CX + 64, CY + CH), (CX + 64, CY + CH + 16), (134, CY + CH + 16), (134, 320)], SOFT, "soft", 1.2)
# 중앙 리프 (Page 52 - 키 251 대상)
d.arrow([(CX + 180, CY + CH), (CX + 180, 320)], ACC, "acc", 1.6)
# 우측 리프 (Page 53)
d.arrow([(CX + 296, CY + CH), (CX + 296, CY + CH + 16), (746, CY + CH + 16), (746, 320)], SOFT, "soft", 1.2)

# 6. Level 2: 리프 페이지들
# Leaf 1 (Page 51)
d.box(24, 320, 220, 72, PAPER2, RULE, 0.9)
d.t(36, 342, "리프 페이지 (230–250)", 12, INK, KR, "start", 600)
d.box(36, 354, 196, 26, PAPER, RULE, 0.8, 4)
d.t(134, 371, "…", 11, MUTED, MONO, "middle")

# Leaf 2 (Page 52 - FOCAL)
FX, FY, FW, FH = 280, 320, 320, 72
d.tone(FX, FY, FW, FH, ACC, 6, "14", 1.5)
d.t(FX + 16, FY + 22, "리프 페이지 (250–270)", 12, ACC, KR, "start", 600)

# 레코드 3개
d.box(FX + 16, FY + 34, 76, 28, PAPER, RULE, 0.8, 4)
d.t(FX + 54, FY + 52, "250: val", 11, MUTED, MONO, "middle")

d.tone(FX + 98, FY + 34, 128, 28, OK, 4, "20", 1.2)
d.t(FX + 162, FY + 52, "251: val", 11, OK, MONO, "middle", 600)

d.box(FX + 232, FY + 34, 72, 28, PAPER, RULE, 0.8, 4)
d.t(FX + 268, FY + 52, "252: val", 11, MUTED, MONO, "middle")

# Leaf 3 (Page 53)
d.box(636, 320, 220, 72, PAPER2, RULE, 0.9)
d.t(648, 342, "리프 페이지 (270–290)", 12, INK, KR, "start", 600)
d.box(648, 354, 196, 26, PAPER, RULE, 0.8, 4)
d.t(746, 371, "…", 11, MUTED, MONO, "middle")

# 7. 형제 포인터 연결 (Leaf 1 -> Leaf 2 -> Leaf 3)
d.arrow([(244, 356), (280, 356)], SOFT, "soft", 1.2, "3 3")
d.arrow([(600, 356), (636, 356)], SOFT, "soft", 1.2, "3 3")

d.legend(LEG, [
    ("키 251 조회 경로", ACC),
    ("고정 페이지 노드", INFO),
    ("조회 성공 레코드", OK),
    ("형제 순차 포인터", SOFT)
])

d.save("04-03.btree.svg")
