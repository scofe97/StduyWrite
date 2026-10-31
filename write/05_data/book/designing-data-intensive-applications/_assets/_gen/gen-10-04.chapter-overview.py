# 10-04 개요 — 합의의 정의와 동치 문제(§1)부터 에포크·쿼럼(§2), 공유 로그와 상태 머신 복제(§3), 비용과 한계(§4), 코디네이션 서비스(§5)를 잇는 전체 지도.
# 사실 출처: 10-04 서두(L13~L18), §1(L23~L38), §2(L40~L54), §3(L56~L66), §4(L68~L80), §5(L82~L102), 원서 Ch.10 (PDF p.32~51)
# 타입 스펙: type-tree
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, WARN, KR, MONO

W = 880
LEG = 432
H = LEG + 56

d = D(W, H, "10-04 · CHAPTER OVERVIEW", "합의와 코디네이션 서비스 전체 지도",
      "분산 합의의 이론적 정의와 환원 동치 관계부터 2라운드 쿼럼 복제, 상태 머신 복제와 운영 인프라로의 전개.",
      "단일 값 합의 정의와 동치 · 에포크 기반 2라운드 쿼럼 · 공유 로그와 SMR · 비용 한계와 코디네이션 인프라")

# 루트 노드: 분산 합의와 코디네이션 인프라
RX, RY, RW, RH = 180, 96, 520, 48
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.2)
d.t(440, 118, "분산 합의와 코디네이션 서비스 체계", 14, INK, KR, "middle", 600)
d.t(440, 134, "합의의 정의에서 쿼럼 투표, 공유 로그, 비용, 코디네이션 서비스까지", 11, MUTED, KR, "middle")

# 5개 카드 컬럼 기하 (CW=156, GAP=14, X0=24)
CW = 156
GAP = 14
X0 = 24
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(5)]

# 루트 → 5개 컬럼 배선 버스
BUS_Y = 162
d.line(440, RY + RH, 440, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[4], BUS_Y, RULE, 1.2)
for i in range(5):
    d.line(cx[i], BUS_Y, cx[i], 178, RULE if i != 1 else ACC, 1.2)

Y_CARD = 178
H_CARD = 230

cards = [
    ("합의와 동치", "§1", [
        "균일 합의·무결성·유효성",
        "종료와 FLP 불가능성",
        "선형화 CAS 상호 변환",
        "원자 커밋(2PC) 비교"
    ], INFO, False),
    ("에포크와 쿼럼", "§2", [
        "단조 증가 에포크 번호",
        "1라운드 리더 선출",
        "2라운드 로그 항목 복제",
        "두 쿼럼 교집합 안전성"
    ], ACC, True),
    ("공유 로그·SMR", "§3", [
        "신뢰 전달과 전체 순서",
        "결정론적 상태 머신 복제",
        "단일 값 합의 상호 변환",
        "이벤트 소싱·KV 스토어"
    ], OK, False),
    ("비용과 한계", "§4", [
        "과반수 (n+1)/2 필수",
        "노드 늘려도 처리량 정체",
        "타임아웃 튜닝 민감성",
        "지리 분산 왕복 지연"
    ], WARN, False),
    ("코디네이션", "§5", [
        "소량 메타데이터 인메모리",
        "분산 락과 펜싱 토큰",
        "에페머럴 노드 장애 탐지",
        "Watch 이벤트 알림"
    ], INFO, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, Y_CARD, CW, H_CARD, color, 6, "14", 1.4)
    else:
        d.box(x, Y_CARD, CW, H_CARD, PAPER2, RULE, 1.0)

    # 섹션 칩
    chip_x = x + 30
    d.chip(chip_x, Y_CARD + 24, sec_chip, color, 11, pad=5)
    d.t(x + CW / 2 + 16, Y_CARD + 28, title, 12, INK, KR, "middle", 600)
    d.line(x + 10, Y_CARD + 44, x + CW - 10, Y_CARD + 44, RULE, 0.8)

    for j, it in enumerate(items):
        iy = Y_CARD + 66 + j * 40
        d.box(x + 8, iy - 13, CW - 16, 26, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 4, it, 11, INK if not is_focal else color, KR, "middle")

# 범례
d.legend(LEG, [
    ("합의 이론과 인프라", INFO),
    ("에포크·쿼럼 (focal)", ACC),
    ("공유 로그와 복제", OK),
    ("비용과 한계", WARN)
])

d.save("10-04.chapter-overview.svg")
