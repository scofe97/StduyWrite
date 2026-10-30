# 05-05 §2 — 메시지 브로커의 큐(Queue)와 토픽(Topic) 분배 패턴 및 비동기 데이터 흐름.
# 사실 출처: 05-05 본문 §2(L49~L61) · 원서 Event-Driven Architectures(PDF p.31) — 메시지 브로커 중개(버퍼·재전달), 큐(한 메시지 한 소비자) vs 토픽(모든 구독자 수신), 스키마 레지스트리.
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, OK, BAD, WARN, KR, MONO

W = 880
LEG = 512
H = LEG + 56

d = D(W, H, "05-05 §2 · MESSAGE BROKER PATTERNS", "메시지 브로커의 큐와 토픽 분배 패턴",
      "메시지 브로커가 비동기 버퍼로 송수신자를 분리하고, 큐(1:1 경쟁 소비자)와 토픽(1:N 발행·구독) 두 가지 분배 패턴으로 메시지를 전달한다.",
      "비동기 버퍼링 · 단일 소비자 큐 패턴 vs 다중 구독자 토픽 패턴")

# ==========================================
# 1. 큐 패턴 (Point-to-Point · 1:1 전달)
# ==========================================
d.box(20, 96, 840, 164, PAPER, RULE, 0.9)
d.t(36, 120, "큐 패턴 (Point-to-Point · 경쟁 소비자)", 13, INK, KR, "start", 600)
d.chip(716, 118, "한 메시지를 한 소비자가 수신", INFO, 11)

# 생산자
d.box(36, 140, 140, 96, PAPER2, RULE, 1.0)
d.t(106, 168, "생산자 (Producer)", 12, INK, KR, "middle", 600)
d.t(106, 188, "비동기 발행", 12, MUTED, KR, "middle")
d.chip(106, 214, "Task Msg", INFO, 11)

# 생산자 → 브로커 화살표
d.arrow([(176, 188), (236, 188)], MUTED, "ar", 1.4)
d.t(206, 176, "전송", 12, MUTED, KR, "middle")

# 브로커 큐 (버퍼)
d.box(240, 140, 280, 96, PAPER2, INFO, 1.2)
d.t(380, 164, "브로커 큐 (Queue 버퍼)", 13, INFO, KR, "middle", 600)
d.t(380, 184, "임시 보관 · 과부하 완충 · 자동 재전달", 12, MUTED, KR, "middle")

# 큐 내부 슬롯
d.box(256, 198, 70, 26, PAPER, RULE, 0.8)
d.t(291, 215, "Msg 3", 11, MUTED, MONO, "middle")
d.box(334, 198, 70, 26, PAPER, RULE, 0.8)
d.t(369, 215, "Msg 2", 11, MUTED, MONO, "middle")
d.box(412, 198, 70, 26, PAPER, RULE, 0.8)
d.t(447, 215, "Msg 1", 11, INK, MONO, "middle", 600)

# 브로커 → 소비자 화살표
d.arrow([(520, 164), (592, 164)], OK, "ok", 1.4)
d.t(556, 152, "1:1 전달", 12, OK, KR, "middle")

d.arrow([(520, 210), (592, 210)], MUTED, "ar", 1.4, dash="4 3")
d.t(556, 198, "대기", 12, MUTED, KR, "middle")

# 소비자 1 & 2
d.box(596, 144, 240, 42, PAPER2, OK, 1.0)
d.t(716, 161, "소비자 A (메시지 처리)", 12, INK, KR, "middle", 600)
d.t(716, 177, "Msg 1 소비 완료 후 제거", 12, MUTED, KR, "middle")

d.box(596, 192, 240, 42, PAPER2, RULE, 0.8)
d.t(716, 209, "소비자 B (경쟁 소비자)", 12, MUTED, KR, "middle")
d.t(716, 225, "다음 메시지 수신 대기", 12, MUTED, KR, "middle")

# ==========================================
# 2. 토픽 패턴 (Pub/Sub · 1:N 전달 — Focal ACC)
# ==========================================
d.tone(20, 272, 840, 168, ACC, 6, "0c", 1.2)
d.t(36, 296, "토픽 패턴 (Publish-Subscribe · 다중 구독자)", 13, ACC, KR, "start", 600)
d.chip(716, 294, "모든 구독자 수신 (팬아웃)", ACC, 11)

# 생산자
d.box(36, 314, 140, 110, PAPER2, RULE, 1.0)
d.t(106, 346, "생산자 (Producer)", 12, INK, KR, "middle", 600)
d.t(106, 368, "이벤트 발행", 12, MUTED, KR, "middle")
d.chip(106, 396, "Event Msg", ACC, 11)

# 생산자 → 브로커 화살표
d.arrow([(176, 368), (236, 368)], ACC, "acc", 1.4)
d.t(206, 356, "발행", 12, ACC, KR, "middle")

# 브로커 토픽 (버퍼)
d.box(240, 314, 280, 110, PAPER2, ACC, 1.2)
d.t(380, 338, "브로커 토픽 (Topic 버퍼)", 13, ACC, KR, "middle", 600)
d.t(380, 360, "디스크에 써 크래시에 견딤", 12, MUTED, KR, "middle")
d.chip(380, 392, "Kafka · RabbitMQ · Pub/Sub", ACC, 11)

# 브로커 → 3개 구독자 팬아웃 화살표
sub_y = [330, 368, 406]
for y in sub_y:
    d.arrow([(520, 368), (556, 368), (556, y), (592, y)], ACC, "acc", 1.2)

# 3개 구독자
d.box(596, 314, 240, 34, PAPER2, ACC, 0.9)
d.t(716, 335, "구독자 1 · 같은 메시지 수신", 12, INK, KR, "middle")

d.box(596, 352, 240, 34, PAPER2, ACC, 0.9)
d.t(716, 373, "구독자 2 · 같은 메시지 수신", 12, INK, KR, "middle")

d.box(596, 390, 240, 34, PAPER2, ACC, 0.9)
d.t(716, 411, "구독자 3 · 같은 메시지 수신", 12, INK, KR, "middle")

# ==========================================
# 3. 하단 스키마 레지스트리 (보조 연계)
# ==========================================
d.box(20, 452, 840, 44, PAPER2, OK, 1.0)
d.t(140, 478, "스키마 레지스트리 (브로커 옆)", 12, OK, KR, "middle", 600)
d.t(490, 478, "Protobuf · Avro · JSON 메시지의 호환성 검사 · 다시 발행할 땐 미지 필드 보존", 12, INK, KR, "middle")

d.legend(LEG, [
    ("단일 소비자 전달 (큐 패턴)", INFO),
    ("다중 구독자 전달 (토픽 패턴)", ACC),
    ("소비 완료 및 스키마 검증", OK)
])
d.save("05-05.event-driven.svg")
