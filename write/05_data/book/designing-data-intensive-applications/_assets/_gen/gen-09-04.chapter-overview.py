# 09-04 개요 — 분산 시스템 검증 3대 접근법·결정론 원리와 9장 전체 불신뢰 3요소 종합 지도.
# 사실 출처: 09-04 본문 서두(L13~L16), §1(L21~L30), §2(L33~L40), §3(L43~L56), §4(L59~L70), §5(L73~L99).
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, BAD, KR, MONO

W = 880
PY = 96
LEG = 432
H = LEG + 56

d = D(W, H, "09-04 · CHAPTER OVERVIEW", "분산 시스템 검증과 9장 종합 전체 지도",
      "분산 알고리즘 형식 검증과 결함 주입, 결정론적 시뮬레이션(DST) 및 결정론 원리와 9장 불신뢰 현실 종합을 조망한다.",
      "형식 검증 · 결함 주입 · 결정론적 시뮬레이션(DST) · 결정론 원리 · 9장 불신뢰 현실 종합")

# 루트 노드: 분산 시스템 검증 체계와 9장 현실 종합
RX, RY, RW, RH = 220, 96, 440, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 118, "분산 시스템 검증 체계와 9장 현실 종합", 14, INK, KR, "middle", 600)
d.t(440, 134, "비결정론적 결함 검증 접근법과 세 가지 불신뢰 요소 대응", 12, MUTED, KR, "middle")

# 4개 카드 컬럼 기하 (CW=198, GAP=14, X0=25)
CW = 198
GAP = 14
X0 = 25
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]

# 루트 → 4개 컬럼 직각 버스 배선
BUS_Y = 164
d.line(440, RY + RH, 440, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(4):
    d.line(cx[i], BUS_Y, cx[i], 180, RULE if i != 3 else ACC, 1.2 if i != 3 else 1.4)

Y_CARD = 180
H_CARD = 224

cards = [
    ("형식 검증 모델", "§1", [
        "올바름 속성 수학적 정의",
        "TLA+ · FizzBee 모델",
        "상태 공간 체계적 탐색",
        "명세와 실제 구현 간 괴리"
    ], INFO, False),
    ("결함 주입 · 시뮬레이션", "§2·§3", [
        "카오스 장애 주입 테스트",
        "Chaos Monkey · Jepsen",
        "모의 클럭 · 가상 네트워크",
        "앱 · 런타임 · 머신 3수준"
    ], OK, False),
    ("결정론의 활용", "§4", [
        "비결정론 소스 완전 제거",
        "이벤트 소싱 로그 재생",
        "Durable Execution 내구성",
        "상태 머신 복제(SMR)"
    ], WARN, False),
    ("9장 종합 현실", "§5", [
        "네트워크 패킷 유실·지연",
        "GC · VM 프로세스 중단",
        "쿼츠 드리프트와 클럭 점프",
        "동적 타임아웃 · 쿼럼 · 펜싱"
    ], ACC, True),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, color, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)

    # 섹션 칩 (좌측 여백 넉넉히)
    chip_x = x + 30
    d.chip(chip_x, Y_CARD + 24, sec_chip, color, 11, pad=4)
    d.t(x + CW / 2 + 20, Y_CARD + 28, title, 13, INK, KR, "middle", 600)
    d.line(x + 12, Y_CARD + 46, x + CW - 12, Y_CARD + 46, RULE, 0.8)

    for j, it in enumerate(items):
        iy = Y_CARD + 70 + j * 38
        d.box(x + 10, iy - 14, CW - 20, 28, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 4, it, 12, INK if not is_focal else color, KR, "middle")

# 범례: 노드 뜻에 맞추고 색상 중복 없음
d.legend(LEG, [
    ("형식 검증 명세", INFO),
    ("실증 결함 주입·DST", OK),
    ("결정론 아키텍처", WARN),
    ("9장 현실 종합 (focal)", ACC)
])

d.save("09-04.chapter-overview.svg")
