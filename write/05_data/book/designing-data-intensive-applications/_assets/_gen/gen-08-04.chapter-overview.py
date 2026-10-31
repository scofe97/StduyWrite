# 08-04 개요 — 분산 원자 커밋 문제와 2PC·XA 한계, NewSQL 합의와 멱등성 대안, 8장 전체 종합을 잇는 전체 지도.
# 검증(10-31 cc-ddia-dverify08): §4 본문 "코디네이터와 데이터 샤드 간 직접 통신"에 맞춤
# 사실 출처: 08-04 서두(L13~L18), §1(L23~L29), §2(L31~L43), §3(L45~L59), §4(L61~L73), §5(L75~L90), §6(L92~L116)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
PY = 100
LEG = 432
H = LEG + 56

d = D(W, H, "08-04 · CHAPTER OVERVIEW", "분산 트랜잭션과 2PC 전체 지도",
      "분산 원자 커밋 문제와 2PC 프로토콜의 한계, 이기종 XA와 동종 NewSQL 및 멱등성 대안, 8장 종합을 잇는다.",
      "단일 노드 원자성에서 다중 노드 원자 커밋으로의 확장 · 2PC와 XA 한계 · 현대적 대안과 8장 전체 종합")

# 루트 노드: 분산 트랜잭션의 원자성 달성과 대안
RX, RY, RW, RH = 220, 100, 440, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 122, "분산 트랜잭션의 원자 커밋과 대안", 14, INK, KR, "middle", 600)
d.t(440, 138, "모든 노드의 동시 커밋 또는 동시 중단 보장", 12, MUTED, KR, "middle")

# 4개 카드 컬럼 기하 (CW=198, GAP=14, X0=25)
CW = 198
GAP = 14
X0 = 25
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]

# 루트 → 4개 컬럼 배선 버스
BUS_Y = 166
d.line(440, RY + RH, 440, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(4):
    d.line(cx[i], BUS_Y, cx[i], 182, RULE if i != 1 else WARN, 1.2)

Y_CARD = 182
H_CARD = 224

cards = [
    ("원자 커밋 과제", "§1", [
        "다중 노드 독립 커밋 불가",
        "일부 커밋 시 영구 불일치",
        "타 트랜잭션 가시화 후",
        "소급 롤백 불가능 위험"
    ], INFO, False),
    ("2PC와 XA 한계", "§2·§3", [
        "준비 질의와 커밋 약속",
        "코디네이터 커밋 포인트",
        "코디네이터 장애 의심 상태",
        "잠금 무기한 블록 · SPoF"
    ], WARN, True),
    ("현대적 분산 대안", "§4·§5", [
        "NewSQL 내부 합의 복제",
        "코디네이터·샤드 직접 통신",
        "고유 메시지 ID 기록",
        "단일 DB 멱등 처리"
    ], OK, False),
    ("8장 전체 종합", "§6", [
        "이상 현상 방지 사다리",
        "직렬 실행 · 2PL · SSI",
        "에러 처리와 트레이드오프",
        "9장 분산 시스템 결함"
    ], ACC, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, color, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)

    # 섹션 칩 (좌측 여백 넉넉히)
    chip_x = x + 34 if len(sec_chip) <= 3 else x + 40
    d.chip(chip_x, Y_CARD + 24, sec_chip, color, 12, pad=6)
    d.t(x + CW / 2 + 22, Y_CARD + 28, title, 13, INK, KR, "middle", 600)
    d.line(x + 12, Y_CARD + 46, x + CW - 12, Y_CARD + 46, RULE, 0.8)

    for j, it in enumerate(items):
        iy = Y_CARD + 70 + j * 38
        d.box(x + 10, iy - 14, CW - 20, 28, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 4, it, 12, INK if not is_focal else color, KR, "middle")

# 범례: 노드 뜻에 맞추고 색상 중복 없음
d.legend(LEG, [
    ("원자 커밋 과제", INFO),
    ("2PC·XA 한계", WARN),
    ("현대적 대안", OK),
    ("8장 전체 종합", ACC)
])

d.save("08-04.chapter-overview.svg")
