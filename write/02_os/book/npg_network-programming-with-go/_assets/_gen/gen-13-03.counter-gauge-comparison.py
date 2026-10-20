# 타입 스펙: type-line
# 사실 출처: NPG Ch.13 Counters & Gauges (Listing 13-20, 13-21), Prometheus 공식 문서 Data Types
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, INFO, KR, MONO

W, H = 920, 520
d = D(W, H, "LINE · COUNTER VS GAUGE",
      "카운터의 단조 증가와 게이지의 오르내림 추이 비교",
      "카운터는 오르기만 하므로 비율을 계산하고 게이지는 현재 활성 상태의 높낮이를 가리킵니다",
      "동일 시간축(0~4초) 부하 시나리오 기준 메트릭 값 변화 (예시)")

px0, px1 = 120, 800
py_top, py_bot = 125, 390

# X Axis: 0 to 4 seconds
def tx(s):
    return px0 + (s / 4.0) * (px1 - px0)

# Y1 Axis (Left): Counter 0 to 50,000
def ty_counter(v):
    return py_bot - (v / 50000.0) * (py_bot - py_top)

# Y2 Axis (Right): Gauge 0 to 600
def ty_gauge(v):
    return py_bot - (v / 600.0) * (py_bot - py_top)

# Gridlines
for c_val in [0, 12500, 25000, 37500, 50000]:
    y = ty_counter(c_val)
    d.line(px0, y, px1, y, RULE, 0.8)
    d.t(px0 - 10, y + 4, f"{c_val:,}", 11, ACC, MONO, "end")

# Right Y axis labels (Gauge)
for g_val in [0, 150, 300, 450, 600]:
    y = ty_gauge(g_val)
    d.t(px1 + 10, y + 4, f"{g_val}", 11, INFO, MONO, "start")

# Axis Titles well above points (py_top - 38 avoids collision with top data chip)
d.t(px0, py_top - 38, "누적 요청 수 (좌측 Y)", 11, ACC, KR, "start", 600)
d.t(px1, py_top - 38, "열린 연결 수 (우측 Y)", 11, INFO, KR, "end", 600)

# X Axis Line and Ticks
d.line(px0, py_bot, px1, py_bot, RULE, 1.2)
for s in range(5):
    x = tx(s)
    d.line(x, py_bot, x, py_bot + 6, RULE, 1.0)
    d.t(x, py_bot + 22, f"{s}s", 11, SOFT, MONO, "middle")

d.t((px0 + px1) / 2, py_bot + 44, "부하 시험 경과 시간 (초)", 11, MUTED, KR, "middle")

# Counter Data Points (Monotonic increase: 0 -> 12500 -> 25000 -> 37500 -> 50000)
c_pts = [
    (tx(0), ty_counter(0)),
    (tx(1), ty_counter(12500)),
    (tx(2), ty_counter(25000)),
    (tx(3), ty_counter(37500)),
    (tx(4), ty_counter(50000)),
]
d.arrow(c_pts, c=ACC, m="acc", sw=2.4)
for cx, cy in c_pts:
    d.o.append(f'<circle cx="{cx}" cy="{cy}" r="4.5" fill="{ACC}"/>')

# Gauge Data Points (Fluctuation: 0 -> 320 -> 500 -> 380 -> 500)
g_pts = [
    (tx(0), ty_gauge(0)),
    (tx(1), ty_gauge(320)),
    (tx(2), ty_gauge(500)),
    (tx(3), ty_gauge(380)),
    (tx(4), ty_gauge(500)),
]
d.arrow(g_pts, c=INFO, m="info", sw=2.4)
for gx, gy in g_pts:
    d.o.append(f'<circle cx="{gx}" cy="{gy}" r="4.5" fill="{INFO}"/>')

# Value chips (size 11 for legibility)
d.chip(tx(1) + 20, ty_counter(12500) - 16, "Requests 12,500 (예시)", ACC, 11)
d.chip(tx(2) - 30, ty_gauge(500) - 16, "OpenConn 500 (예시)", INFO, 11)
d.chip(tx(3) + 20, ty_gauge(380) + 18, "연결 유휴 전환 (예시)", INFO, 11)
d.chip(tx(4) - 85, ty_counter(50000) - 20, "최종 50,000 도달", ACC, 11)

# Legend (placed at y=465, leaving 55px margin to H=520)
d.legend(465, [
    ("카운터: Requests (단조 증가)", ACC),
    ("게이지: OpenConnections (오르내림)", INFO),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "13-03.counter-gauge-comparison.svg"))
d.save(out_path)
print("saved:", out_path)
