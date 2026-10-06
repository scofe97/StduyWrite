# 03-03 하트비트와 수신 데이터로 데드라인 연장 (Heartbeat & Advance Deadline)
# 사실 출처: NPG Ch.3 Listing 3-12 (ping_test.go, p.30-32), 1초 핑 · 5초 시한 · 4초 PONG · 9초 만료
# 타입 스펙: type-line — Listing 3-12 측정 시각 기준 남은 데드라인 시간의 톱니 꺾은선
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 510
d = D(W, H, "NPG CHAPTER 3 — DEADLINE SAWTOOTH LINE",
      "남은 데드라인 시간의 톱니 추이",
      "Listing 3-12 의 실제 시각 기준 데드라인 연장 꺾은선",
      "PONG 수신 시 5초 재설정, 9초에 세션 최종 만료")

# Plot boundaries
px0, px1 = 90, 770
py_top, py_bot = 110, 390
t_max = 9.0
dl_max = 5.0

def tx(sec):
    return px0 + (sec / t_max) * (px1 - px0)

def ty(dl_sec):
    return py_bot - (dl_sec / dl_max) * (py_bot - py_top)

# Y Gridlines (0s to 5s)
for dl in range(6):
    y = ty(dl)
    d.line(px0, y, px1, y, RULE, 0.8)
    d.t(px0 - 12, y + 4, f"{dl}s", 11, SOFT, MONO, "end")

d.t(px0 - 45, (py_top + py_bot) / 2, "남은 시간", 11, MUTED, KR, "middle")

# X Axis Ticks (0s to 9s)
d.line(px0, py_bot, px1, py_bot, RULE, 1.2)
for s in range(10):
    x = tx(s)
    d.line(x, py_bot, x, py_bot + 6, RULE, 1.0)
    d.t(x, py_bot + 20, f"{s}s", 11, SOFT, MONO, "middle")

d.t((px0 + px1) / 2, py_bot + 40, "경과 시간 (초)", 11, MUTED, KR, "middle")

# Data lines
# Segment 1: (0, 5) -> (4, 1)
pts1 = [(tx(0), ty(5)), (tx(4), ty(1))]
d.arrow(pts1, c=WARN, m="warn", sw=2.2)

# Vert jump at 4s: (4, 1) -> (4, 5)
d.line(tx(4), ty(1), tx(4), ty(5), OK, sw=2.0, dash="3 3")
d.chip(tx(4), ty(5) - 15, "PONG (5s 리셋)", OK, 11)

# Segment 2: (4, 5) -> (9, 0)
pts2 = [(tx(4), ty(5)), (tx(9), ty(0))]
d.arrow(pts2, c=WARN, m="warn", sw=2.2)

# Ping points dots
ping_times = [1, 2, 3, 4, 5, 6, 7, 8]
for pt in ping_times:
    dl_val = (5 - pt) if pt < 4 else (5 - (pt - 4))
    cx, cy = tx(pt), ty(dl_val)
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="4" fill="{INFO}"/>')

# 9s Termination point
d.o.append(f'<circle cx="{tx(9)}" cy="{ty(0)}" r="5" fill="{BAD}"/>')
# Leader line from empty upper-right space (7~9s, between 4s and 5s gridlines) to 9s termination point
d.arrow([(750, 150), (768, 384)], c=BAD, m="bad", sw=1.1, dash="3 2")
d.chip(730, 140, "io.EOF (종료)", BAD, 11)

# Legend
d.legend(465, [("데드라인 소진", WARN), ("PONG 리셋", OK), ("핑 발생점", INFO), ("최종 만료", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-03.heartbeat-deadline.svg"))
d.save(out)
print(f"saved: {out}")
