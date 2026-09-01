# 04-03 §4 — 이벤트 이미터로 조각이 셸의 토스트를 띄우는 흐름 (원문 Figure 4-5 + 코드).
# 이벤트 이름과 페이로드 필드는 저자의 코드 그대로다 — notification · type · title · message.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1220, 620
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 04-03 §4",
        "조각은 셸을 모른 채 셸의 토스트를 띄운다",
        "이미터는 Object.freeze 로 굳힌 싱글턴이고 조각에 주입된다. 조각은 상대가 누구인지 모르고 이벤트만 던진다.",
        "가운데 레인이 조각 어디에도 속하지 않는 이미터입니다")

d.lanes([("결제 수단 조각", "UserPaymentMethodsMFE"),
         ("이벤트 이미터", "Object.freeze 싱글턴"),
         ("셸의 토스트", "NotificationModal")], y0=104, lane_w=300)
d.rails(528)
d.msg("셸의 토스트", "이벤트 이미터", "on('notification')", 208, MUTED,
      sub="셸이 먼저 듣기 시작한다")
d.selfmsg("결제 수단 조각", "handleMakeDefault", 272, MUTED, sub="기본 결제 수단을 바꾼다")
d.msg("결제 수단 조각", "이벤트 이미터", "emit('notification', p)", 344, ACC, "acc",
      sub="type · title · message 세 필드")
d.msg("이벤트 이미터", "셸의 토스트", "handleNotification(p)", 408, ACC, "acc",
      sub="듣고 있던 콜백이 불린다")
d.state("셸의 토스트", "토스트 표시", 464, OK)
d.msg("셸의 토스트", "이벤트 이미터", "off('notification')", 512, MUTED,
      sub="언마운트될 때 구독을 거둔다")
d.legend(552, [("도메인 경계를 건너는 이벤트", ACC), ("구독을 걸고 거두는 일", MUTED)])
d.save("04-03.emitter-notification.svg")
print("h 필요:", 552 + 40, " 실제:", H)
