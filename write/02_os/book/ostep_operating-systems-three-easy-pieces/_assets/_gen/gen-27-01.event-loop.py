# 27-01 ### 1 — 이벤트 루프는 한 바퀴마다 관심 있는 fd 를 담고 select() 로 기다리다가, 준비된 fd 의 핸들러를 하나씩 끝까지 돌린 뒤 처음으로 돌아간다.
# 본문 근거: 이 노트 ### 1 「이벤트 루프와 select()」.
# 검증 근거: macOS(Darwin 25.6)와 Linux 7.2.12 에서 evsrv.c(select 이벤트 루프 서버)를 돌려, 연결만 열고 말이 없는 클라이언트가 있어도 다른 클라이언트의 TIME 이 0~1 ms 에 답하는 것을 확인.
# 공식 근거: Linux man-pages 6.19 select(2) — FD_ZERO·FD_SET 으로 집합을 만들고 select() 가 준비된 fd 만 남기며, 준비됨은 막히지 않고 I/O 를 할 수 있다는 뜻.
# 타입 스펙: type-flowchart — 네 노드가 한 줄로 이어지고 마지막이 처음으로 돌아오는 폐곡선.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 304
d = D(W, H, "OSTEP · 27-01 §1",
      "이벤트 루프는 한 바퀴에 이벤트를 하나씩 끝까지 처리한다",
      "루프는 fd 집합을 비우고 관심 있는 fd 를 담은 뒤 select() 로 기다린다. 준비된 fd 를 FD_ISSET 으로 골라 핸들러가 하나씩 끝까지 처리하고, 처리가 끝나면 처음으로 돌아가 같은 일을 반복한다. "
      "핸들러가 도는 동안은 다른 이벤트가 처리되지 않으므로 다음에 무엇을 처리할지 고르는 일이 곧 스케줄링이다.",
      "핸들러가 도는 동안 시스템에서 도는 활동은 그 핸들러 하나입니다")

BW, BH, PITCH, X0 = 180, 76, 212, 24
BY = 120
RY = BY + BH + 36          # 되돌아가는 선의 높이

steps = [
    ("FD_ZERO · FD_SET", "관심 있는 fd 담기", SOFT),
    ("select()", "준비될 때까지 대기", INFO),
    ("FD_ISSET", "준비된 fd 고르기", SOFT),
    ("handle()", "이벤트 하나를 끝까지", ACC),
]
for i, (title, sub, c) in enumerate(steps):
    x = X0 + i * PITCH
    d.tone(x, BY, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, BY + 32, title, 12.5, INK, KR, "middle", 600)
    d.t(x + BW / 2, BY + 56, sub, 12, MUTED, KR)
    if i < len(steps) - 1:
        d.path(f"M {x + BW + 2} {BY + BH / 2} L {x + PITCH - 2} {BY + BH / 2}", MUTED, 1.4, m="ar")

x_last = X0 + 3 * PITCH + BW / 2
x_first = X0 + BW / 2
d.arrow([(x_last, BY + BH + 2), (x_last, RY), (x_first, RY), (x_first, BY + BH + 4)], MUTED, "ar", 1.4)
d.chip((x_last + x_first) / 2, RY, "다음 반복", MUTED, 12)

d.legend(RY + 32, [("fd 를 다루는 준비", SOFT), ("커널에서 기다리는 자리", INFO), ("하나씩 끝까지 도는 핸들러", ACC)])
d.save("27-01.event-loop.svg")
