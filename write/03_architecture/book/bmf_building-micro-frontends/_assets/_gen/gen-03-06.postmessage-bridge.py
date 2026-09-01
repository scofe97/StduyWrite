# 03-06 §3 — iframe 안의 조각이 바깥과 말하는 유일한 길. 저자가 적은 것만 그린다.
# postMessage 로 호스트에 알리고, 호스트가 event emitter 를 contentWindow 에 붙여 다른 조각에 전달한다.
# 저장소도 호스트에 두라는 저자의 규약을 self 메시지로 표시한다.
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 메시지. 레인 · 레일 · 메시지 문법 그대로.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, PAPER, RULE, KR, MONO

W, H = 1140, 560
d = Seq(W, H, "BUILDING MICRO-FRONTENDS · 03-06 §3",
        "iframe 은 postMessage 로만 바깥과 말한다",
        "샌드박스가 막아 놓은 자리를 저자는 postMessage 와 contentWindow 에 붙인 이벤트 이미터로 넘는다. 웹 스토리지는 호스트에 둔다.",
        "가운데 레인이 호스트 페이지이고 양쪽이 iframe 안의 조각입니다")

d.lanes([("조각 A", "iframe"),
         ("호스트 페이지", "application shell"),
         ("조각 B", "iframe")], y0=104, lane_w=270)
d.rails(468)
d.msg("조각 A", "호스트 페이지", "postMessage(event)", 214, ACC, "acc",
      sub="iframe 안에서 사용자가 무언가를 눌렀다")
d.selfmsg("호스트 페이지", "read/write storage", 282, MUTED,
          sub="쿠키와 웹 스토리지는 호스트 한 곳에 둔다")
d.msg("호스트 페이지", "조각 B", "emitter.dispatch", 356, ACC, "acc",
      sub="이미터 인스턴스를 contentWindow 에 붙여 둔다")
d.state("조각 B", "listen · react", 424, OK)
d.legend(492, [("iframe 경계를 넘는 통신", ACC), ("호스트가 대신 맡는 일", MUTED)])
d.save("03-06.postmessage-bridge.svg")
print("h 필요:", 492 + 40, " 실제:", H)
