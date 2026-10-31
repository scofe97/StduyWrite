# 12-01 개요 — 이벤트 스트림 정의(§1), AMQP/JMS 브로커(§2), 로그 기반 브로커(§3), 두 방식의 비교(§4) 전체 지도.
# 사실 출처: 12-01 본문 서두(L13~L19), §1(L24~L30), §2(L32~L53), §3(L55~L69), §4(L71~L88), 원서 Ch.12 (PDF p.1~15)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 96
BANNER_H = 44
CARD_Y = 160
CARD_H = 248
LEG = 432
H = LEG + 56

d = D(W, H, "12-01 · CHAPTER OVERVIEW", "스트림 전송과 메시지 브로커 전체 지도",
      "이벤트 스트림의 표현부터 AMQP/JMS 브로커와 로그 기반 브로커의 내부 구조, 내구성과 재처리 트레이드오프 비교.",
      "불변 이벤트 스트림 · 소비 후 삭제 대 로그 보존 · 파티션과 오프셋 · 재처리 가능성 트레이드오프")

# 상단 공통 전제 배너
d.tone(24, BANNER_Y, W - 48, BANNER_H, INFO, 6, "14", 1.0)
d.t(W / 2, BANNER_Y + 18, "스트림 전송 체계: 연속 도착 이벤트와 브로커 아키텍처", 13, INK, KR, "middle", 600)
d.t(W / 2, BANNER_Y + 34, "소비 후 삭제 방식(AMQP/JMS) 대 비파괴적 로그 보존 방식(Kafka/Kinesis)", 12, MUTED, KR, "middle")

# 4개 컬럼 기하 (CW=196, GAP=16, X0=24)
CW = 196
GAP = 16
X0 = 24
cx = [X0 + i * (CW + GAP) + CW / 2 for i in range(4)]

# 루트 배너 → 4개 카드 배선 버스
BUS_Y = 150
d.line(W / 2, BANNER_Y + BANNER_H, W / 2, BUS_Y, RULE, 1.2)
d.line(cx[0], BUS_Y, cx[3], BUS_Y, RULE, 1.2)
for i in range(4):
    d.line(cx[i], BUS_Y, cx[i], CARD_Y, ACC if i == 2 else RULE, 1.2)

cards = [
    ("이벤트 스트림", "§1", [
        "불변 사건 객체·타임스탬프",
        "프로듀서와 컨슈머 분리",
        "토픽 기반 이벤트 논리 묶음",
        "능동 알림 시스템"
    ], INFO, False),
    ("AMQP/JMS 브로커", "§2", [
        "소비 확인(ACK) 후 즉시 삭제",
        "로드 밸런싱과 팬아웃",
        "장애 재전달 시 순서 역전",
        "반복 실패 메시지 DLQ 격리"
    ], WARN, False),
    ("로그 기반 브로커", "§3", [
        "추가 전용 파티션 샤드 분할",
        "단조 증가 오프셋 순서 보장",
        "컨슈머 그룹 독립 오프셋 추적",
        "비파괴 소비와 계층 스토리지"
    ], ACC, True),
    ("브로커 특성 비교", "§4", [
        "메시지 단위 vs 파티션 병렬화",
        "오프셋 되감기 과거 재처리",
        "낙오 컨슈머 격리와 불변 입력",
        "작업 큐 대 고처리량 로그"
    ], OK, False),
]

for i, (title, sec_chip, items, color, is_focal) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    if is_focal:
        d.tone(x, CARD_Y, CW, CARD_H, color, 6, "14", 1.4)
    else:
        d.box(x, CARD_Y, CW, CARD_H, PAPER2, RULE, 1.0)

    # 섹션 칩과 제목
    chip_x = x + 30
    d.chip(chip_x, CARD_Y + 22, sec_chip, color, 12, pad=5)
    d.t(x + CW / 2 + 16, CARD_Y + 26, title, 13, INK, KR, "middle", 600)
    d.line(x + 10, CARD_Y + 42, x + CW - 10, CARD_Y + 42, RULE, 0.8)

    # 4개 항목
    for j, it in enumerate(items):
        iy = CARD_Y + 62 + j * 44
        d.box(x + 8, iy - 13, CW - 16, 30, PAPER, RULE, 0.6, r=4)
        d.t(x + CW / 2, iy + 6, it, 12, INK if not is_focal else color, KR, "middle")

# 범례
d.legend(LEG, [
    ("이벤트 스트림", INFO),
    ("소비 후 삭제", WARN),
    ("로그 기반 (focal)", ACC),
    ("특성 비교", OK)
])

d.save("12-01.chapter-overview.svg")
