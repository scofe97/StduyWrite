# 타입 스펙: type-state — 알림 한 건이 start 에서 pending·sent·delivered 를 거쳐 click 이나 unsubscribe 로 끝나고, pending 과 sent 에서 failed 로 빠진 알림은 큐로 되돌아간다.
# 사실 출처: 추출본 v2.txt 2913~2917행(열람률·클릭률 추적)과 PDF 162쪽 상태 그림(start·pending·sent·deliver·click·unsubscribe·error)에서 deliver→delivered, error→failed 로 적었다, PDF 163쪽 그림의 send pending(알림 서버)·sent(작업자)·click tracking(기기)·retry on error,
#   추출본 2927~2929행(실패하면 큐로 되돌리고 정해진 횟수만큼 재시도)·2901~2902행(계속되면 개발자에게 경보). 상태 이름은 메인 창 지정(pending→sent→delivered/failed)과 Twilio 상태 이름(delivered·failed)에 맞췄다.
# Layout conventions: 상태 상자 폭 128·높이 56, 중심선 y=204, x stride 232(200·432·664), 오른쪽 둘은 x=840 에 세로 쌓음. 모든 좌표 4의 배수. 화살표는 수평·수직만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, KR, MONO

W, H = 1000, 536
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 10-01 §6",
      "알림 한 건의 상태는 기록하는 자리가 다르다",
      "알림 서버가 pending, 작업자가 sent 를 남기고 기기에서 click 이 돌아오며, 실패한 알림은 큐로 되돌아가 정해진 횟수만 다시 시도한다.",
      "상태 이름 아래는 그 상태를 기록하는 자리")


def fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in txt) else MONO


def state(x, y, w, name, sub, c, focal=False):
    if focal:
        d.tone(x, y, w, 56, ACC, 6, "12", 1.4)
    else:
        d.tone(x, y, w, 56, c, 6, "10", 1.1)
    d.t(x + w / 2, y + 24, name, 14, INK, MONO, "middle", 600)
    if sub:
        d.t(x + w / 2, y + 44, sub, 13, MUTED, fam(sub))


Y = 176
state(24, Y, 100, "start", "", MUTED)
state(200, Y, 128, "pending", "알림 서버", INFO)
state(432, Y, 128, "sent", "작업자", INFO)
state(664, Y, 128, "delivered", "", OK)
state(840, 104, 136, "click", "기기 → 분석", OK)
state(840, 248, 136, "unsubscribe", "", WARN)
state(316, 344, 128, "failed", "", BAD, focal=True)

# 정상 경로 — 수평
d.arrow([(128, 204), (196, 204)], MUTED, "ar", 1.5)
d.arrow([(332, 204), (428, 204)], MUTED, "ar", 1.5)
d.chip(380, 184, "전송", MUTED, 13)
d.arrow([(564, 204), (660, 204)], MUTED, "ar", 1.5)
d.chip(612, 184, "전달", MUTED, 13)
# delivered 에서 갈라짐 — 버스 x=816
d.arrow([(796, 204), (816, 204), (816, 132), (836, 132)], MUTED, "ar", 1.5)
d.arrow([(816, 204), (816, 276), (836, 276)], MUTED, "ar", 1.5)

# 실패 — pending·sent 에서 아래로
d.arrow([(232, 236), (232, 372), (312, 372)], BAD, "bad", 1.5)
d.chip(176, 304, "전송 실패", BAD, 13)
d.arrow([(496, 236), (496, 372), (448, 372)], BAD, "bad", 1.5)
d.chip(560, 304, "전달 실패", BAD, 13)
# 재시도 — failed 위쪽에서 pending 아래로
d.arrow([(332, 344), (332, 300), (296, 300), (296, 236)], WARN, "warn", 1.5, "5 4")
d.chip(404, 292, "큐로 되돌림", WARN, 13)
d.t(404, 328, "정해진 횟수", 13, MUTED, KR)
# 계속되면 경보
d.arrow([(380, 400), (380, 448)], BAD, "bad", 1.5)
d.chip(380, 468, "개발자에게 경보", BAD, 13)

d.legend(H - 44, [("진행 상태", INFO), ("전달 뒤 상태", OK), ("수신 거부", WARN), ("실패 경로", BAD), ("failed 상태", ACC)])
d.save("10-01.notification-states.svg")
