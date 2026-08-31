# 02-03 §4 — 이벤트 버스로 조각끼리 알리는 흐름 (원문 Figure 2-6).
# 저자가 적은 것만 그린다 — 컨테이너나 애플리케이션 셸이 버스를 만들어 각 조각에 주입하고,
# 관심 있는 조각만 듣고 반응한다. 전역 상태는 쓰지 않는다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1100, 560
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 02-03 §4",
        "이벤트 버스로 알리는 흐름",
        "애플리케이션 셸이 이벤트 버스를 만들어 각 조각에 주입하고, 한 조각이 발행한 이벤트를 관심 있는 조각만 듣는다.",
        "가운데 굵은 화살표가 발행이고, 듣지 않는 조각은 아무 일도 하지 않습니다")

d.lanes([("애플리케이션 셸", "container"),
         ("마이크로 프론트엔드 A", "publisher"),
         ("마이크로 프론트엔드 B", "subscriber")], y0=104, lane_w=250)
d.rails(452)
d.msg("애플리케이션 셸", "마이크로 프론트엔드 A", "inject(eventBus)", 210, MUTED, sub="셸이 버스를 만들어 넣어 준다")
d.msg("애플리케이션 셸", "마이크로 프론트엔드 B", "inject(eventBus)", 270, MUTED, sub="같은 버스를 모두가 받는다")
d.selfmsg("마이크로 프론트엔드 A", "emit(event)", 336, ACC, sub="자기 도메인에서 일이 일어났다")
d.msg("마이크로 프론트엔드 A", "마이크로 프론트엔드 B", "notify", 402, ACC, sub="관심 있는 조각만 듣고 반응한다")
d.state("마이크로 프론트엔드 B", "listen · react", 440, OK)

d.legend(492, [("이벤트가 오가는 경로", ACC), ("듣고 반응하는 상태", OK)])
d.save("02-03.event-bus.svg")
print("h 필요:", 492 + 40, " 실제:", H)
