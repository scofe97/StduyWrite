# 12-04 §3 — 내결함성과 Exactly-Once 의미론: 마이크로배치, 체크포인트, 원자적 커밋, 멱등성 4대 복구 전략 비교.
# 사실 출처: 12-04 본문 §3(L56~L80), DDIA 2판 Ch.12 "Fault Tolerance" (PDF p.50~54: p.51 barriers in the message stream, p.53 monotonically increasing offset·Storm's Trident).
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
BANNER_Y = 104
BANNER_H = 36
Y1 = 156
CARD_H = 144
Y2 = Y1 + CARD_H + 16
PANEL_Y = Y2 + CARD_H + 16
LEG = PANEL_Y + 48 + 18
H = LEG + 52

d = D(W, H, "12-04 · §3 FAULT TOLERANCE", "스트림 처리 Exactly-Once 4대 달성 전략",
      "스트림은 무한하여 배치처럼 출력을 단순히 버릴 수 없으므로, 마이크로배치·체크포인트·원자적 커밋·멱등성이 각각 다른 방식으로 exactly-once 의미론을 달성하는 구조를 비교한다.",
      "소블록 분할 · 주기적 상태 스냅샷 · 단일 트랜잭션 묶음 · 단조 오프셋 멱등성")

# 상단 배경 배너
d.tone(28, BANNER_Y, W - 56, BANNER_H, INFO, 4, "14", 1.0)
d.t(W / 2, BANNER_Y + 23, "스트림 내결함성의 본질: 무한 입력 환경에서 내부 상태 복구와 외부 부수 효과 제어로 effectively-once 보장", 11.5, INK, KR, "middle", 600)

CARD_W = 398
GAP_X = 28

cards = [
    # (x, y, title, sub, tag, color, item1_h, item1_d, item2_h, item2_d)
    (28, Y1, "마이크로배치 (Microbatching)", "소블록 단위 배치 분할", "Spark", INFO,
     "동작 메커니즘", "스트림을 약 1초 소블록 단위로 분할 처리",
     "가시성 및 제약", "블록 완료 시 일괄 가시화 및 윈도우 크기 제약"),
    (28 + CARD_W + GAP_X, Y1, "체크포인트 (Checkpointing)", "주기적 연산자 상태 스냅샷", "Flink", OK,
     "동작 메커니즘", "메시지 베리어 기반 주기적 상태 스냅샷 저장",
     "복구 및 제약", "최근 체크포인트부터 재생 및 멱등성 보완 필요"),
    (28, Y2, "원자적 커밋 (Atomic Commit)", "단일 트랜잭션 일괄 영속화", "Kafka", ACC,
     "동작 메커니즘", "출력 쓰기 · 메시지 발행 · 상태 갱신 단일 묶음",
     "가시성 및 제약", "성공 시 일괄 반영 및 내부 트랜잭션 관리"),
    (28 + CARD_W + GAP_X, Y2, "멱등성 연산 (Idempotence)", "중복 연산 결과 불변성", "Trident", WARN,
     "동작 메커니즘", "단조 증가 오프셋 메타데이터 저장소 병기",
     "복구 및 제약", "중복 갱신 무효화 및 결정론적 처리 전제"),
]

for (cx, cy, c_title, c_sub, c_tag, c_color, h1, d1, h2, d2) in cards:
    d.box(cx, cy, CARD_W, CARD_H, PAPER2, c_color, 1.2)
    d.t(cx + 16, cy + 24, c_title, 12.5, INK, KR, "start", 600)
    d.chip(cx + CARD_W - 48, cy + 20, c_tag, c_color, 11)
    d.t(cx + 16, cy + 44, c_sub, 11, MUTED, KR, "start")
    d.line(cx + 12, cy + 54, cx + CARD_W - 12, cy + 54, RULE, 0.8)

    # 항목 1
    d.box(cx + 12, cy + 62, CARD_W - 24, 34, PAPER, RULE, 0.8)
    d.t(cx + 22, cy + 83, h1, 11, c_color, KR, "start", 600)
    d.t(cx + 104, cy + 83, d1, 11, INK, KR, "start")

    # 항목 2
    d.box(cx + 12, cy + 102, CARD_W - 24, 34, PAPER, RULE, 0.8)
    d.t(cx + 22, cy + 123, h2, 11, c_color, KR, "start", 600)
    d.t(cx + 104, cy + 123, d2, 11, MUTED, KR, "start")

# 하단 종합 통찰 패널 (명사구 형태)
d.tone(28, PANEL_Y, W - 56, 44, ACC, 4, "14", 1.0)
d.t(W / 2, PANEL_Y + 26, "체크포인트와 크래시 사이 이벤트는 중복 처리될 수 있어 멱등성이나 트랜잭션으로 보완", 11.5, INK, KR, "middle", 600)

d.legend(LEG, [
    ("마이크로배치 (§3)", INFO),
    ("체크포인트 (§3)", OK),
    ("원자적 커밋 (§3)", ACC),
    ("멱등성 연산 (§3)", WARN)
])

d.save("12-04.exactly-once-strategies.svg")
