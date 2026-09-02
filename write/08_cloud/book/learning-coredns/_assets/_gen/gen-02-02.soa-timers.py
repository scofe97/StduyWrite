# 02-02 §7 — SOA 의 refresh · retry · expire 가 보조 서버의 상태를 옮긴다.
# 원문 근거: refresh 마다 마스터의 시리얼을 확인하고, 더 높으면 존 전송을 요청한다.
#            확인이 실패하면 retry 간격으로 계속 확인하고, expire 동안 내내 실패하면
#            존 데이터가 낡았다고 보고 존을 만료시킨다. 만료 뒤에는 그 존 질의에
#            Server Failed 응답 코드로 답한다.
# 타입 스펙: type-state — 주체 하나(보조 서버)의 상태 전이와 재시도와 종료가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, OK, KR, MONO

W, H = 940, 520
d = D(W, H, "LEARNING COREDNS · 02-02 §7",
      "세 타이머가 보조 서버를 옮겨 다니게 한다",
      "refresh 는 확인 주기, retry 는 확인이 실패했을 때의 재시도 주기, expire 는 포기하는 시점이다. "
      "세 값이 함께 보조 서버가 언제부터 답을 못 하게 되는지를 정한다.",
      "색이 붙은 상태에서 질의는 Server Failed 로 돌아옵니다")

def state(x, y, w, nm, sub, focal=False):
    if focal:
        d.tone(x, y, w, 64, ACC, 8, "12", 1.4)
    else:
        d.box(x, y, w, 64, PAPER2, RULE, 1.0, 8)
    d.t(x + w / 2, y + 28, nm, 14, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 12, MUTED)

d.o.append(f'<circle cx="40" cy="180" r="6" fill="{INK}"/>')
d.path("M 48 180 L 108 180", MUTED, 1.4, m="ar")

state(116, 148, 216, "존 데이터 보유", "질의에 정상 응답")
state(412, 148, 216, "마스터에 확인", "시리얼 비교")
state(412, 300, 216, "재시도 대기", "retry 간격")
state(692, 300, 180, "존 만료", "SERVFAIL 응답", focal=True)

d.path("M 332 168 L 404 168", MUTED, 1.4, m="ar")
d.t(368, 156, "refresh", 12, MUTED, MONO)

d.path("M 520 148 C 520 92 224 92 224 140", MUTED, 1.4, m="ar")
d.t(372, 100, "시리얼이 더 높다 / 존 전송", 12, MUTED, KR)
d.t(372, 120, "같으면 그대로 유지", 12, SOFT, KR)

d.path("M 520 212 L 520 292", MUTED, 1.4, m="ar")
d.t(532, 258, "확인 실패", 12, MUTED, KR, "start")

d.path("M 412 332 C 356 332 356 212 404 200", MUTED, 1.4, m="ar", dash="5 4")
d.t(300, 268, "retry 경과 / 다시 확인", 12, MUTED, KR)

d.path("M 628 332 L 684 332", ACC, 1.6, m="acc")
d.t(656, 320, "expire", 12, ACC, MONO)

d.o.append(f'<circle cx="904" cy="332" r="8" fill="none" stroke="{ACC}" stroke-width="1.4"/>')
d.o.append(f'<circle cx="904" cy="332" r="5" fill="{ACC}"/>')
d.path("M 872 332 L 894 332", ACC, 1.4)

d.t(20, 420, "refresh 는 한 시간 안팎이 무난하고, retry 는 그 절반이나 4분의 1, expire 는 적어도 일주일을 둔다", 13, MUTED, KR, "start")
d.t(20, 442, "NOTIFY 가 생긴 뒤로 refresh 의 비중은 줄었지만, 확인 한 번의 비용이 질의 하나라 여전히 값싸다", 13, MUTED, KR, "start")

d.legend(462, [("존 질의가 실패하기 시작하는 상태", ACC)])
d.save("02-02.soa-timers.svg")
