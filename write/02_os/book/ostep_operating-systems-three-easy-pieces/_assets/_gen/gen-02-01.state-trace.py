# 02-01 「시간마다 프로세스 둘의 상태를 따라가면」 — CPU 만 쓰는 둘은 차례로 끝나고, 한쪽이 I/O 로 Blocked 가 되면 다른 쪽이 그 틈에 CPU 를 쓴다.
# 본문 근거: 이 노트 「4. Running·Ready·Blocked 전이」 의 「시간 순서로 따라가기」.
# 값 근거: 위 패널은 원서 그림 4.3, 아래 패널은 원서 그림 4.4 의 표를 칸 그대로 옮겼다(시각 1~8 과 1~10).
# 공식 근거: OSTEP 4장 §4.4 그림 4.3·4.4.
# 타입 스펙: type-gantt — 작업과 국면을 시간축 위에, 칸 하나가 시각 하나다. 상태색은 Running(초록)·Ready(파랑)·Blocked(노랑), 코랄은 I/O 대기 구간 한 곳에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INK, MUTED, SOFT, RULE, PAPER2, OK, WARN, INFO, KR, MONO

W, H = 920, 556
GX, CW, RH = 168, 64, 32
COLOR = {"Running": OK, "Ready": INFO, "Blocked": WARN}
d = D(W, H, "OSTEP · 02-01 §4",
      "한쪽이 I/O 를 기다리는 동안 다른 쪽이 CPU 를 쓴다",
      "위 표는 CPU 만 쓰는 두 프로세스로, Process0 이 시각 4 에 끝난 뒤에야 Process1 이 시각 5~8 에 돈다. "
      "아래 표는 Process0 이 시각 3 에 I/O 를 시작해 4~6 동안 Blocked 이고 그동안 Process1 이 돌며, 시각 7 에 I/O 가 끝나 Process0 은 Ready 가 된다.")


def panel(y0, name, ticks, rows, notes, accent=None):
    d.t(24, y0 - 20, name, 13, INK, KR, "start", 600)
    for k in range(1, ticks + 1):
        d.t(GX + (k - 0.5) * CW, y0 - 4, str(k), 12, MUTED, MONO, "middle")
    for r, (pname, seq) in enumerate(rows):
        y = y0 + r * (RH + 8)
        d.t(24, y + 21, pname, 12, INK, MONO, "start", 600)
        for k, st in enumerate(seq):
            if st is None:
                continue
            c = COLOR[st]
            d.tone(GX + k * CW + 2, y, CW - 4, RH, c, 4, "22", 1.0)
            d.t(GX + (k + 0.5) * CW, y + 21, st, 12, INK, MONO, "middle")
    yb = y0 + len(rows) * (RH + 8)
    for k, txt in notes:
        d.t(GX + (k - 0.5) * CW, yb + 14, txt, 12, MUTED, KR, "middle")
    if accent:
        a, b = accent
        d.o.append(f'<rect x="{GX + (a - 1) * CW}" y="{y0 - 2}" width="{(b - a + 1) * CW}" height="{len(rows) * (RH + 8) - 4}" rx="6" fill="none" stroke="{ACC}" stroke-width="1.4"/>')


R, Y, B = "Running", "Ready", "Blocked"
panel(136, "CPU 만 쓰는 둘", 8,
      [("Process0", [R, R, R, R, None, None, None, None]),
       ("Process1", [Y, Y, Y, Y, R, R, R, R])],
      [(4, "P0 끝"), (8, "P1 끝")])
panel(328, "한쪽이 I/O 를 하는 둘", 10,
      [("Process0", [R, R, R, B, B, B, Y, Y, R, R]),
       ("Process1", [Y, Y, Y, R, R, R, R, R, None, None])],
      [(3, "I/O 시작"), (7, "I/O 끝"), (8, "P1 끝"), (10, "P0 끝")],
      accent=(4, 6))
d.chip(GX + 3.5 * CW, 452, "CPU 가 놀지 않음", ACC, 12, 8)

d.legend(H - 56, [("Running", OK), ("Ready", INFO), ("Blocked", WARN), ("I/O 대기 구간", ACC)])
d.save("02-01.state-trace.svg")
print("ok 02-01 state-trace")
