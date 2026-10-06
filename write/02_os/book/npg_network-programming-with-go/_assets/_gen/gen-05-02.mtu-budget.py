# 타입 스펙: type-waterfall
# 05-02 이더넷 MTU 와 헤더 예산 분해
# 사실 출처: NPG Ch.5 p.115-116, Listing 5-9·5-10 (MTU 1,500, IP 20B, ICMP/UDP 8B, Payload 1,472B)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 500
d = D(W, H, "NPG CH.5 — UDP MTU BUDGET",
      "이더넷 MTU 와 패킷 헤더 예산 분해",
      "MTU 1,500 바이트에서 IP 와 ICMP·UDP 헤더를 뺀 최대 페이로드 도출")

# Chart dimensions
# Domain 1400 to 1500 (100 units). Scale = 200 / 100 = 2.0 px/unit
# Baseline at y = 380 (1400 level). Top at y = 180 (1500 level, height = 200)
baseline = 380.0
axis_min = 1400.0
scale = 200.0 / 100.0  # 2.0 px/unit

# Y-axis (broken axis at bottom)
d.line(80, 160, 80, baseline + 8, RULE, 1.0)
# Axis break marks (//) on Y-axis
d.line(74, 394, 86, 388, MUTED, 1.2)
d.line(74, 400, 86, 394, MUTED, 1.2)
# Axis foot below break to zero
d.line(80, 400, 80, 408, RULE, 1.0)
d.line(76, 408, 80, 408, RULE, 1.0)
d.t(72, 411, "0", 9, SOFT, MONO, "end")

# Baseline (1400 level)
d.line(80, baseline, 780, baseline, RULE, 1.0)
d.t(72, baseline + 3, "1400", 9, SOFT, MONO, "end")

# Horizontal gridlines
for val in [1420, 1440, 1460]:
    y_grid = baseline - (val - axis_min) * scale
    d.line(80, y_grid, 780, y_grid, f"{RULE}", 0.6, dash="3 3")
    d.t(72, y_grid + 3, str(val), 9, SOFT, MONO, "end")

# Bar specifications
# pitch = 160, bar_w = 90
# 1. Start total: 1500
# 2. Bridge 1: -20 (IP Header) -> 1480
# 3. Bridge 2: -8 (ICMP/UDP Header) -> 1472
# 4. End total: 1472 (Payload)

bar_w = 90
gap = 70
x1 = 120
x2 = x1 + bar_w + gap  # 280
x3 = x2 + bar_w + gap  # 440
x4 = x3 + bar_w + gap  # 600

# Values & Levels
v1 = 1500
y1 = baseline - (v1 - axis_min) * scale  # 180.0
h1 = (v1 - axis_min) * scale             # 200.0

delta1 = -20
v2_level = v1 + delta1                   # 1480
y2 = y1                                  # 180.0
h2 = (-delta1) * scale                   # 40.0
b2 = y2 + h2                             # 220.0

delta2 = -8
v3_level = v2_level + delta2             # 1472
y3 = b2                                  # 220.0
h3 = (-delta2) * scale                   # 16.0
b3 = y3 + h3                             # 236.0

v4 = 1472
y4 = baseline - (v4 - axis_min) * scale  # 236.0
h4 = (v4 - axis_min) * scale             # 144.0

# Carries (drawn before bars)
# Carry 1 (1500): between bar 1 and bar 2
d.o.append(f'<line x1="{x1+bar_w}" y1="{y1:.2f}" x2="{x2}" y2="{y1:.2f}" stroke="{MUTED}" stroke-width="1" data-carry="1500"/>')

# Carry 2 (1480): between bar 2 and bar 3
d.o.append(f'<line x1="{x2+bar_w}" y1="{b2:.2f}" x2="{x3}" y2="{b2:.2f}" stroke="{MUTED}" stroke-width="1" data-carry="1480"/>')

# Carry 3 (1472): between bar 3 and bar 4
d.o.append(f'<line x1="{x3+bar_w}" y1="{b3:.2f}" x2="{x4}" y2="{b3:.2f}" stroke="{MUTED}" stroke-width="1" data-carry="1472"/>')

# Bars
# Bar 1: Start Total (Ethernet MTU)
d.o.append(f'<rect x="{x1}" y="{y1:.2f}" width="{bar_w}" height="{h1:.2f}" fill="{PAPER2}" stroke="{INFO}" stroke-width="1.2" data-role="total" data-value="1500" data-name="이더넷 MTU"/>')
d.o.append(f'<text x="{x1+bar_w/2}" y="{y1-8:.2f}" fill="{INFO}" font-size="9" font-family="{MONO}" text-anchor="middle" font-weight="600">1500</text>')

# Bar 2: Bridge 1 (-20 B IP Header)
d.o.append(f'<rect x="{x2}" y="{y2:.2f}" width="{bar_w}" height="{h2:.2f}" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.2" data-role="delta" data-value="-20" data-name="IP 헤더"/>')
d.o.append(f'<text x="{x2+bar_w/2}" y="{b2+12:.2f}" fill="{WARN}" font-size="9" font-family="{MONO}" text-anchor="middle" font-weight="600">-20</text>')

# Bar 3: Bridge 2 (-8 B ICMP/UDP Header)
d.o.append(f'<rect x="{x3}" y="{y3:.2f}" width="{bar_w}" height="{h3:.2f}" fill="{PAPER}" stroke="{MUTED}" stroke-width="1.2" data-role="delta" data-value="-8" data-name="헤더"/>')
d.o.append(f'<text x="{x3+bar_w/2}" y="{b3+12:.2f}" fill="{WARN}" font-size="9" font-family="{MONO}" text-anchor="middle" font-weight="600">-8</text>')

# Bar 4: End Total (Max Payload 1472)
d.o.append(f'<rect x="{x4}" y="{y4:.2f}" width="{bar_w}" height="{h4:.2f}" fill="{f"{OK}18"}" stroke="{OK}" stroke-width="1.2" data-role="total" data-value="1472" data-name="페이로드"/>')
d.o.append(f'<text x="{x4+bar_w/2}" y="{y4-8:.2f}" fill="{OK}" font-size="9" font-family="{MONO}" text-anchor="middle" font-weight="600">1472</text>')

# Category labels below baseline (y = 422)
d.t(x1 + bar_w / 2, 422, "이더넷 MTU", 11, INK, KR, "middle", 600)
d.t(x2 + bar_w / 2, 422, "IP 헤더 (20B)", 11, MUTED, KR, "middle")
d.t(x3 + bar_w / 2, 422, "UDP·ICMP 헤더 (8B)", 11, MUTED, KR, "middle")
d.t(x4 + bar_w / 2, 422, "최대 페이로드", 11, OK, KR, "middle", 600)

# Legend
d.legend(455, [("MTU 상한", INFO), ("헤더 차감", WARN), ("비단편화 상한", OK)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-02.mtu-budget.svg"))
d.save(out)
print(f"saved: {out}")
