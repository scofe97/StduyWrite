# 10-01 개요 — 선형성 정의(§1), 구성 규칙(§2), 직렬화 가능성 비교(§3), 필요한 상황(§4), 복제 방법별 가능성(§5) 전체 지도.
# 사실 출처: 10-01 본문 서두(L16~L18), §1(L23~L32), §2(L35~L50), §3(L53~L71), §4(L74~L83), §5(L86~L96).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
PY = 156
PH = 244
LEG = PY + PH + 28
H = LEG + 52

d = D(W, H, "10-01 · CHAPTER OVERVIEW", "선형성 개념과 구성 원리 전체 지도",
      "선형성 정의(§1), 구성 규칙(§2), 직렬성 비교(§3), 필요 상황(§4), 복제 방법(§5)의 체계.",
      "단일 복사본 착각 · 원자적 flip 시점 · 격리 vs 최신성 · 분산 락과 유일성 · 합의와 복제 방식")

# 상단 공통 전제 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "선형성의 본질: 물리적 다중 복제본을 단일 복사본처럼 추상화하는 최신성 보장", 12, INK, KR, "middle", 600)

X0 = 28
CW = 156
GAP = 12

cards = [
    ("§1", "선형성 정의", "단일 복사본 착각",
     [("최신성 보장", "쓰기 직후 즉시 반영"),
      ("외부 일관성", "시스템 외부 관찰 기준"),
      ("역전 방지", "새 값 확인 뒤 역전 금지")],
     INFO, False),
    ("§2", "구성 규칙", "원자적 flip 시점",
     [("선형화 포인트", "0에서 1로 바뀌는 순간"),
      ("동시 쓰기 중 읽기", "구 값 또는 신 값 반환"),
      ("CAS 조건부 쓰기", "경쟁 시 단 하나만 성공")],
     ACC, True),
    ("§3", "직렬성 비교", "격리 vs 최신성",
     [("직렬화 가능성", "다중 객체 트랜잭션 격리"),
      ("선형성", "단일 객체 최신성 보장"),
      ("엄격한 직렬화", "실제 시간 순서 준수")],
     INFO, False),
    ("§4", "필요한 상황", "순서 정합성 요구",
     [("리더 선출·분산 락", "스플릿 브레인 방지"),
      ("유일성 제약", "중복 방지 원자적 검증"),
      ("교차 채널 의존", "저장소·메시지 큐 경합")],
     WARN, False),
    ("§5", "복제 구현", "알고리즘별 가능성",
     [("합의 알고리즘", "쿼럼 투표 기반 선형화"),
      ("단일 리더", "리더에서만 처리 시 가능"),
      ("다중·리더리스", "충돌 쓰기·클럭 스큐")],
     OK, False),
]

for idx, (sec, title, role, items, card_c, is_focal) in enumerate(cards):
    x = X0 + idx * (CW + GAP)
    y = PY

    if is_focal:
        d.box(x, y, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, y, CW, PH, PAPER2, RULE, 0.9)

    # 카드 상단 헤더: 절 칩 + 제목 + 부제목
    d.chip(x + 28, y + 20, sec, card_c, 11)
    d.t(x + 50, y + 24, title, 13, INK, KR, "start", 600)
    d.t(x + 14, y + 46, role, 11, SOFT, KR, "start")

    d.line(x + 10, y + 58, x + CW - 10, y + 58, RULE, 0.8)

    # 3개 항목
    iy0 = y + 80
    for i_idx, (head, sub) in enumerate(items):
        iy = iy0 + i_idx * 52
        d.box(x + 8, iy - 14, CW - 16, 44, PAPER, RULE, 0.6)
        d.t(x + 14, iy + 2, head, 12, INK, KR, "start", 600)
        d.t(x + 14, iy + 20, sub, 11, MUTED, KR, "start")

d.legend(LEG, [
    ("핵심 규칙 (focal)", ACC),
    ("안전 보장", OK),
    ("구조·정의", INFO),
    ("제약·의존", WARN),
])

d.save("10-01.chapter-overview.svg")
