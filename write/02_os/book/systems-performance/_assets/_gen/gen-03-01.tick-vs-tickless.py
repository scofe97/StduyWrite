# 03-01 §6 — tick 지연(100Hz 에서 1ms 타이머가 10ms 까지 기다림)과 tick 오버헤드(idle CPU 를 4ms 마다 깨움).
# 타입 스펙: type-timeline — 0~20ms 시간축 위에 사건(만료·실행·깨어남)을 정직한 눈금으로 놓는다.
#           축약: 한 줄 baseline 대신 경우 네 줄을 같은 눈금으로 쌓는다. 눈금은 1ms = 32px 고정.
#           100Hz·1ms 타이머는 원서 3.2.5 의 tick 지연 예, 250Hz 는 원서가 적은 Linux 의 보통 CONFIG_HZ.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 976, 556
X0, PX = 212, 32            # 0ms 위치, 1ms 당 px
ROW0, STRIDE = 176, 76
AX = ROW0 + 4 * STRIDE - 12  # 눈금 축

def X(ms): return X0 + ms * PX

d = DK(W, H, "SYSTEMS PERFORMANCE · 03-01 §6",
       "tick 지연과 tick 오버헤드",
       "위 두 줄: 1ms 뒤 만료될 타이머가 100Hz tick 에서는 10ms tick 까지 기다리고, 고해상도 타이머는 1ms 에 바로 실행된다. 아래 두 줄: 할 일 없는 CPU 를 250Hz tick 이 4ms 마다 깨우고, tickless 는 다음 인터럽트까지 잠들게 둔다.",
       "정해진 간격으로 깨어나면 늦게 깨고, 쓸데없이도 깹니다")

def row(i, name, sub):
    y = ROW0 + i * STRIDE
    d.t(X0 - 24, y - 2, name, 14, INK, KR, "end", 600)
    d.t(X0 - 24, y + 16, sub, 12, MUTED, KR, "end")
    d.line(X(0), y, X(20), y, RULE, 1.0)
    return y

def dot(x, y, c, r=5):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"/>')

# 1) 100Hz tick — 타이머 만료 1ms, 실행은 10ms tick
y = row(0, "100Hz tick", "타이머 확인 10ms 마다")
for ms in (0, 10, 20): dot(X(ms), y, MUTED, 4)
d.line(X(1), y - 16, X(1), y + 16, WARN, 1.4)
d.t(X(1), y - 22, "만료 1ms", 12, WARN, KR)
d.tone(X(1), y - 6, X(10) - X(1), 12, ACC, 3)
dot(X(10), y, ACC, 6)
d.t(X(10) + 12, y - 12, "실행 10ms", 13, ACC, KR, "start", 600)
d.t((X(1) + X(10)) / 2, y + 26, "tick 지연 9ms", 13, ACC, KR, "middle", 600)

# 2) 고해상도 타이머 — 1ms 에 바로
y = row(1, "고해상도 타이머", "만료 시각에 인터럽트")
d.line(X(1), y - 16, X(1), y + 16, WARN, 1.4)
dot(X(1), y, OK, 6)
d.t(X(1) + 12, y - 12, "실행 1ms", 13, OK, KR, "start", 600)

# 3) 250Hz tick · idle CPU — 4ms 마다 깨어남
y = row(2, "250Hz tick", "idle CPU")
d.tone(X(0), y - 6, X(20) - X(0), 12, INFO, 3, "10", 0.8)
for ms in range(0, 21, 4): dot(X(ms), y, WARN, 5)
d.t(X(20) + 12, y + 5, "깨어남 6번", 13, WARN, KR, "start", 600)

# 4) tickless · idle CPU — 계속 잠
y = row(3, "tickless", "idle CPU · NO_HZ")
d.tone(X(0), y - 6, X(20) - X(0), 12, INFO, 3, "22", 1.0)
d.t(X(20) + 12, y + 5, "계속 잠", 13, INFO, KR, "start", 600)

# 눈금
d.line(X(0), AX, X(20), AX, MUTED, 1.0)
for ms in range(0, 21, 2):
    d.line(X(ms), AX - 4, X(ms), AX + 4, MUTED, 1.0)
    if ms % 4 == 0 or ms in (10,): d.t(X(ms), AX + 20, f"{ms}ms", 12, SOFT, MONO)

d.legend(AX + 40, [("tick 지연", ACC), ("즉시 실행", OK), ("idle 중 깨어남", WARN), ("잠든 구간", INFO)])
d.save("03-01.tick-vs-tickless.svg")
