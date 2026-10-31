# 13-01 §3 — 분산 트랜잭션(2PC/XA)과 로그 기반 파생 데이터의 5대 핵심 특성 비교 아키텍처.
# 사실 출처: 13-01 §3 본문 표(L59~L65)의 다섯 항목(본문 정리). 원서 Derived data versus distributed transactions(장 PDF p.4)는 atomic commit vs deterministic retry·idempotence, read-your-writes 차이, XA 한계, "most promising approach" 만 말한다.
# 2026-10-31 검증(cc-ddia-dverify13): "결국 일관성 허용 필요"(본문 L67 은 이 말이 충분한 지침이 아니라고 함)·"2PC 분산 잠금"·"토픽 파티션"·"대규모" 를 본문 표 낱말로 바꾸고, 2PC 머리 칸을 범례 '주의·비용' 색에서 중립으로, 로그 쪽 운영 비용 '낮음' 을 장점 색으로 바꿨다.
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
Y0 = 104
ROW_H = 46
ROW_GAP = 10
ROWS_Y0 = Y0 + 44
BOTTOM_Y = ROWS_Y0 + 5 * (ROW_H + ROW_GAP) + 6
LEG = BOTTOM_Y + 40
H = LEG + 52

d = D(W, H, "13-01 · §3 DERIVED DATA VS DISTRIBUTED TRANSACTIONS", "분산 트랜잭션과 로그 기반 파생 데이터 비교",
      "분산 트랜잭션의 원자적 커밋 방식과 로그 기반 파생 데이터의 비동기 동기화 방식을 다섯 가지 특성으로 견준다.",
      "일관성 달성 방식 · 읽기 최신성 · 이종 시스템 통합 · 장애 격리 · 운영 복잡도")

# Column X and Width definitions
C1_X, C1_W = 24, 116
C2_X, C2_W = 150, 344
C3_X, C3_W = 504, 352

# Column Header Boxes
d.box(C1_X, Y0, C1_W, 34, PAPER2, RULE, 0.8)
d.t(C1_X + C1_W / 2, Y0 + 22, "비교 축", 12, SOFT, KR, "middle", 600)

d.box(C2_X, Y0, C2_W, 34, PAPER2, RULE, 1.0)
d.chip(C2_X + 28, Y0 + 17, "2PC", MUTED, 11, pad=3)
d.t(C2_X + C2_W / 2 + 10, Y0 + 22, "분산 트랜잭션 (XA / 2PC)", 12, INK, KR, "middle", 600)

d.box(C3_X, Y0, C3_W, 34, PAPER2, ACC, 1.3)
d.chip(C3_X + 28, Y0 + 17, "로그", ACC, 11, pad=3)
d.t(C3_X + C3_W / 2 + 10, Y0 + 22, "로그 기반 파생 (CDC / 이벤트 로그)", 12, ACC, KR, "middle", 600)

# Comparison Rows
rows = [
    ("일관성 달성",
     ("원자적 커밋 프로토콜", "함께 적용 또는 함께 롤백", INFO),
     ("결정론적 재처리 + 멱등성", "같은 로그·같은 코드 → 같은 결과", OK)),
    ("읽기 최신성",
     ("커밋 즉시 최신 읽기", "자신이 쓴 값 바로 읽기", OK),
     ("비동기 — 지연 가능", "기본으로 최신 읽기 보장 없음", WARN)),
    ("이종 통합",
     ("표준 프로토콜 없어 어려움", "XA: 내결함성·성능 취약", WARN),
     ("이벤트 로그로 연결", "이종 시스템을 로그로 잇기", OK)),
    ("장애 격리",
     ("참여자 하나 실패 시 전체 중단", "한 곳 장애가 전체로 전파", BAD),
     ("장애 국소화와 독립 복구", "소비자마다 독립 복구", OK)),
    ("운영 비용",
     ("운영 복잡도 높음", "2PC 코디네이터 관리", WARN),
     ("운영 복잡도 낮음", "브로커·토픽 운영", OK)),
]

for idx, (axis, (c2_head, c2_sub, c2_c), (c3_head, c3_sub, c3_c)) in enumerate(rows):
    ry = ROWS_Y0 + idx * (ROW_H + ROW_GAP)

    # Col 1: 비교 축 레이블
    d.box(C1_X, ry, C1_W, ROW_H, PAPER, RULE, 0.7)
    d.t(C1_X + C1_W / 2, ry + 27, axis, 12, INK, KR, "middle", 600)

    # Col 2: 분산 트랜잭션
    d.box(C2_X, ry, C2_W, ROW_H, PAPER, c2_c, 0.8)
    d.t(C2_X + 16, ry + 19, c2_head, 12, INK, KR, "start", 600)
    d.t(C2_X + 16, ry + 36, c2_sub, 11, c2_c, KR, "start")

    # Col 3: 로그 기반 파생
    d.box(C3_X, ry, C3_W, ROW_H, PAPER, c3_c, 0.9)
    d.t(C3_X + 16, ry + 19, c3_head, 12, INK, KR, "start", 600)
    d.t(C3_X + 16, ry + 36, c3_sub, 11, c3_c, KR, "start")

# Bottom Summary Panel
d.box(C1_X, BOTTOM_Y, W - 48, 30, PAPER2, RULE, 0.9, 4)
d.t(W / 2, BOTTOM_Y + 19, "결론: 로그 기반 파생 데이터 = 이종 시스템 통합에 가장 현실적인 접근법", 11, INK, KR, "middle", 600)

d.legend(LEG, [
    ("로그 파생 (focal)", ACC),
    ("장점·보장", OK),
    ("주의·비용", WARN),
    ("중단 위험", BAD),
    ("방식 (중립)", INFO),
])

d.save("13-01.distributed-tx-vs-derived-data.svg")
