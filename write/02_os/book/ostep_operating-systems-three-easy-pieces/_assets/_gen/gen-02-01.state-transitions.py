# 02-01 「세 상태와 네 전이」 — Ready 와 Running 사이는 운영체제가 정하고, Running 에서 Blocked 로는 I/O 시작으로, Blocked 에서 Ready 로는 I/O 완료로 옮겨진다.
# 본문 근거: 이 노트 「4. Running·Ready·Blocked 전이」 의 「세 상태와 네 전이」.
# 값 근거: 개념 도식이라 값은 없다.
# 공식 근거: OSTEP 4장 §4.4 와 그림 4.2 — 전이 이름은 scheduled, descheduled, I/O: initiate, I/O: done 이다.
# 타입 스펙: type-state — 주체 하나의 상태 전이. 노드 셋, 화살표 넷이고 모든 화살표는 직각이다. 상태색은 Ready(INFO)·Running(OK)·Blocked(WARN)로 맞춘다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, WARN, INFO, KR, MONO

W, H = 880, 520
d = D(W, H, "OSTEP · 02-01 §4",
      "프로세스는 Ready · Running · Blocked 셋 사이를 옮겨 다닌다",
      "Ready 와 Running 사이의 전이 scheduled 와 descheduled 는 운영체제가 정한다. Running 에서 I/O 를 시작하면 Blocked 가 되고, "
      "I/O 가 끝나면 Blocked 에서 Ready 로 돌아가며 바로 Running 으로 이어질 수도 있다.")


def state(x, y, name, sub, c):
    d.tone(x, y, 208, 72, c, 6, "22", 1.4 if c == ACC else 1.1)
    d.t(x + 104, y + 30, name, 15, c if c == ACC else INK, MONO, "middle", 600)
    d.t(x + 104, y + 54, sub, 12, MUTED, KR)


state(96, 128, "Ready", "실행할 수 있지만 대기", INFO)
state(576, 128, "Running", "프로세서에서 명령 실행", OK)
state(336, 336, "Blocked", "어떤 사건을 기다림", WARN)

# Ready -> Running
d.arrow([(304, 152), (576, 152)], INFO, "info", 1.6)
d.t(440, 142, "scheduled", 13, INFO, MONO, "middle", 600)
# Running -> Ready
d.arrow([(576, 176), (304, 176)], MUTED, "ar", 1.6)
d.t(440, 198, "descheduled", 13, MUTED, MONO, "middle", 600)
d.t(440, 112, "운영체제가 정한다", 12, MUTED, KR, "middle", 600)
# Running -> Blocked
d.arrow([(680, 200), (680, 372), (544, 372)], WARN, "warn", 1.6)
d.t(696, 290, "I/O: initiate", 13, WARN, MONO, "start", 600)
# Blocked -> Ready
d.arrow([(336, 372), (200, 372), (200, 200)], OK, "ok", 1.6)
d.t(184, 290, "I/O: done", 13, OK, MONO, "end", 600)
d.t(440, 436, "I/O 완료 같은 사건이 일어날 때까지 Blocked 유지", 12, MUTED, KR, "middle", 600)

d.legend(H - 56, [("실행 대기", INFO), ("실행 중", OK), ("사건 대기", WARN)])
d.save("02-01.state-transitions.svg")
print("ok 02-01 state-transitions")
