# 타입 스펙: type-timeline — 사건이 시간 위에 놓이고 세대가 바꾼 것이 드러난다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.3.2 Table 7.2 —
#   표준명·세대·연도·이론 최대 속도·대역·PHY 는 표의 값 그대로
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 616
d = D(W, H, "SECTION 7.3.2 · EVOLUTION OF 802.11",
      "속도만 늘린 것이 아니라 목표가 바뀌었습니다",
      "세대마다 최대 속도가 올랐지만, 최근 세대가 겨냥한 것은 한 사람의 속도가 아니라 밀집한 다수다.",
      "표준명·연도·속도·대역·PHY 는 원문 Table 7.2 의 값입니다")

AXIS_Y = 292
X0, X1 = 96, 856
Y0, Y1 = 1999, 2026
ROWS = [
    ("802.11b", "", 1999, "11 Mbps", "2.4 GHz", "직접 시퀀스 확산", MUTED),
    ("802.11g", "", 2003, "54 Mbps", "2.4 GHz", "OFDM", MUTED),
    ("802.11n", "WiFi 4", 2009, "600 Mbps", "2.4 · 5 GHz", "OFDM", INFO),
    ("802.11ac", "WiFi 5", 2013, "6.9 Gbps", "5 GHz", "OFDM · MIMO", INFO),
    ("802.11ax", "WiFi 6", 2020, "9.5 Gbps", "2.4 · 5 GHz", "OFDM · OFDMA · MIMO", ACC),
    ("802.11be", "WiFi 7", 2024, "30 Gbps 이상", "2.4 · 5 · 6 GHz", "OFDM · OFDMA · MIMO", ACC),
]
CW, CH = 152, 108
d.line(X0, AXIS_Y, X1, AXIS_Y, RULE, 1.2)
for yr in (2000, 2005, 2010, 2015, 2020, 2025):
    x = X0 + (X1 - X0) * (yr - Y0) / (Y1 - Y0)
    d.line(x, AXIS_Y - 5, x, AXIS_Y + 5, RULE, 1.0)
    d.t(x, AXIS_Y + 22, str(yr), 10, SOFT, MONO)

for i, (std, gen, yr, rate, band, phy, c) in enumerate(ROWS):
    mx = X0 + (X1 - X0) * (yr - Y0) / (Y1 - Y0)
    above = (i % 2 == 0)
    cx = min(max(mx - CW / 2, 24), W - 24 - CW)
    cy = AXIS_Y - 60 - CH if above else AXIS_Y + 60
    d.tone(cx, cy, CW, CH, c, 6, "12", 1.2)
    d.t(cx + CW / 2, cy + 24, std, 12, c, KR, "middle", 600)
    d.t(cx + CW / 2, cy + 44, f"{yr}" + (f" · {gen}" if gen else ""), 10, SOFT, MONO)
    d.t(cx + CW / 2, cy + 64, rate, 11, INK, KR)
    d.t(cx + CW / 2, cy + 82, band, 10, MUTED, KR)
    d.t(cx + CW / 2, cy + 98, phy, 10, MUTED, KR)
    stem_a = cy + CH if above else cy
    d.line(mx, stem_a, mx, AXIS_Y, c, 1.2, "3 4")
    d.o.append(f'<circle cx="{mx}" cy="{AXIS_Y}" r="4.5" fill="{c}"/>')

PY = 476
d.box(24, PY, 880, 82, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "원문이 표에서 뽑는 것은 속도가 아닙니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "초기에는 한 사용자의 최대 처리량이 목표였지만, 지금 개발을 이끄는 것은 밀집 배치입니다.",
    "기업·공항·경기장처럼 많은 사용자가 동시에 주고받는 곳에서 효율이 관심사가 됐습니다.",
]):
    d.t(44, PY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(576, [("브랜딩 이전", MUTED), ("WiFi 4 · 5", INFO), ("OFDMA 세대", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-03.wifi-generations.svg"
d.save(out)
print("→", out)
