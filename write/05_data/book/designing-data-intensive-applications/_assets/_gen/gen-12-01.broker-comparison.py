# 12-01 §4 — AMQP/JMS 메시지 브로커와 로그 기반 브로커의 핵심 설계 특성 및 트레이드오프 비교 격자.
# 사실 출처: 12-01 §2·§4(L39~L50, L86~L101), 원서 p.7(큐가 길면 throughput 저하), p.13(컨슈머 노드 수 ≤ shard 수), p.16(낙오 컨슈머·큐 누적 메모리)
# 타입 스펙: type-dp-security-matrix
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
LX, LW = 24, 140
CX0, CW, GAP = 180, 332, 16
HY, HH = 104, 56
RY0, RSTR, RH = 176, 56, 48
FOCAL = 1

cols = [
    ("AMQP/JMS 브로커", "RabbitMQ · ActiveMQ · Service Bus", WARN),
    ("로그 기반 브로커", "Apache Kafka · Amazon Kinesis", ACC),
]

rows = [
    ("메시지 삭제 시점",
     [("ACK 확인 후 즉시 삭제", "파괴적 소비 (destructive)", WARN),
      ("보존 기간 만료 후 순환 삭제", "비파괴적 추가 전용 로그 유지", OK)]),
    ("과거 메시지 재처리",
     [("재처리 불가", "소비 즉시 큐에서 삭제", BAD),
      ("오프셋 되감기로 재처리 가능", "배치와 동일한 불변 입력 원칙", OK)]),
    ("병렬 처리 단위",
     [("메시지 단위 병렬화", "메시지마다 컨슈머 하나에 전달", OK),
      ("파티션 단위 병렬화", "컨슈머 수 ≤ 파티션 수", WARN)]),
    ("순서 보장 범위",
     [("재전달 시 순서 역전 가능", "로드 밸런싱과 장애 결합 시 발생", WARN),
      ("파티션 내부 완전 순서 보장", "단조 증가 오프셋 기반 정렬", OK)]),
    ("컨슈머 낙오 영향",
     [("큐 누적으로 메모리 압박", "느린 컨슈머 시 브로커 성능 저하", WARN),
      ("오프셋 격차만 증가 (무영향)", "대형 디스크 버퍼 기반 독립 보관", OK)]),
    ("대표 적합 사례",
     [("개별 처리 비용 큰 비동기 태스크", "순서 의존성 없는 작업 큐", OK),
      ("높은 처리량 · 순서 중요 스트림", "동일 로그 다중 분석 및 파생 재구축", ACC)]),
]

LEG = RY0 + len(rows) * RSTR + 16
H = LEG + 56

d = D(W, H, "12-01 · §4 BROKER COMPARISON MATRIX", "AMQP/JMS 대 로그 기반 브로커 특성 비교",
      "소비 후 삭제 방식의 AMQP/JMS 브로커와 불변 로그 기반 브로커의 삭제 시점, 재처리, 병렬화, 순서, 낙오 영향, 적합 사례 비교.",
      "소비 후 삭제 대 로그 보존 · 오프셋 되감기 재처리 · 메시지 단위 대 파티션 단위 · 순서 역전 대 파티션 순서")

# 컬럼 헤더
for k, (name, sub, col_c) in enumerate(cols):
    x = CX0 + k * (CW + GAP)
    is_focal = (k == FOCAL)
    d.box(x, HY, CW, HH, PAPER2, ACC if is_focal else RULE, 1.4 if is_focal else 1.0)
    d.t(x + CW / 2, HY + 24, name, 13.5, INK, KR, "middle", 600)
    d.t(x + CW / 2, HY + 42, sub, 11.5, col_c, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)

# 행 데이터
for r, (label, vals) in enumerate(rows):
    y = RY0 + r * RSTR
    d.box(LX, y, LW, RH, PAPER2, RULE, 0.8)
    d.t(LX + LW / 2, y + 28, label, 12, INK, KR, "middle", 600)
    for k, (main_v, sub_v, cell_c) in enumerate(vals):
        x = CX0 + k * (CW + GAP)
        is_focal = (k == FOCAL and cell_c == ACC)
        d.box(x, y, CW, RH, PAPER2, cell_c if is_focal else RULE, 1.2 if is_focal else 0.8)
        d.tone(x + 6, y + 6, CW - 12, RH - 12, cell_c, 4, "12", 0.8)
        d.t(x + CW / 2, y + 21, main_v, 12, INK, KR, "middle", 600)
        d.t(x + CW / 2, y + 36, sub_v, 11.5, MUTED, KR, "middle")

# 범례
d.legend(LEG, [
    ("안전·보장·적합", OK),
    ("제약·주의·비용", WARN),
    ("불가·위험", BAD),
    ("핵심 적합 사례 (focal)", ACC)
])

d.save("12-01.broker-comparison.svg")
