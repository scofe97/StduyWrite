# 타입 스펙: type-radar — 여러 대상을 3~5개 기준으로 채점. 세 축 중 둘만 강조된다는 것이 논점이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.6.3 Figure 7.51 —
#   세 축(커버리지·저에너지·데이터율)과 "어느 기술도 셋 다 강조하지 못한다"는 결론은 원문 그대로.
#   각 기술의 점수는 원문이 수치로 주지 않으므로, 원문이 묶은 세 그룹의 강조 축 둘만 표시한다.
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 604
d = D(W, H, "SECTION 7.6.3 · IOT NETWORKING",
      "셋 중 둘만 고를 수 있습니다",
      "IoT 기술은 넓은 커버리지와 낮은 에너지와 높은 데이터율 가운데 둘을 강조한다. 셋을 다 강조하는 것은 없다.",
      "세 축과 그룹 구분은 원문 Figure 7.51 의 것입니다")

CX, CY, R = 290, 290, 128
AXES = [("넓은 커버리지", -90), ("높은 데이터율", 30), ("낮은 에너지", 150)]
for lvl in (0.34, 0.67, 1.0):
    pts = [(CX + R * lvl * math.cos(math.radians(a)), CY + R * lvl * math.sin(math.radians(a)))
           for _, a in AXES]
    dd = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts)) + " Z"
    d.path(dd, RULE, 0.8)
for name, a in AXES:
    x2 = CX + R * math.cos(math.radians(a))
    y2 = CY + R * math.sin(math.radians(a))
    d.line(CX, CY, x2, y2, RULE, 0.9)
    lx = CX + (R + 44) * math.cos(math.radians(a))
    ly = CY + (R + 30) * math.sin(math.radians(a))
    d.t(lx, ly, name, 11, SOFT, KR)

GROUPS = [
    ("짧은 거리 · 저에너지", INFO, (0.24, 0.40, 0.94), "802.11ah · BLE · Zigbee"),
    ("넓은 지역 · 저에너지", OK, (0.94, 0.22, 0.88), "LoRaWAN · NB-IoT"),
    ("넓은 지역 · 고속", ACC, (0.90, 0.92, 0.26), "LTE-M · 5G"),
]
for name, c, vals, members in GROUPS:
    pts = [(CX + R * v * math.cos(math.radians(a)), CY + R * v * math.sin(math.radians(a)))
           for v, (_, a) in zip(vals, AXES)]
    dd = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts)) + " Z"
    d.o.append(f'<path d="{dd}" fill="{c}22" stroke="{c}" stroke-width="1.8"/>')

PX, PW = 560, 344
d.box(PX, 138, PW, 268, PAPER2, RULE, 1.0)
d.t(PX + 20, 164, "원문이 묶은 세 그룹", 12, INK, KR, "start", 600)
d.line(PX + 20, 176, PX + PW - 20, 176, RULE, 0.8)
gy = 200
DETAIL = [
    (INFO, "짧은 거리 · 저에너지", ["802.11ah — 100 kbps 대에서 5~10 Mbps,", "900 MHz 비면허, 중계로 1 km 까지",
                            "BLE · Zigbee — 802.15.4 위에서 저속"]),
    (OK, "넓은 지역 · 저에너지", ["LoRaWAN — 채널당 0.3~50 kbit/s,", "902~928 MHz, 별의 별 위상",
                          "NB-IoT — 200 kHz 채널, 약 250 kbps"]),
    (ACC, "넓은 지역 · 고속", ["LTE-M — NB-IoT 의 다섯 배 채널 폭,", "기지국 간 이동성을 받칩니다"]),
]
for c, name, lines in DETAIL:
    d.t(PX + 20, gy, name, 11, c, KR, "start", 600)
    for j, ln in enumerate(lines):
        d.t(PX + 20, gy + 18 + j * 17, ln, 10, MUTED, KR, "start")
    gy += 18 + len(lines) * 17 + 14

NY = 436
d.box(24, NY, 880, 82, PAPER2, RULE, 1.0)
d.t(44, NY + 26, "그래서 승자 독식이 안 됩니다", 12, INK, KR, "start", 600)
for i, ln in enumerate([
    "어느 기술도 세 축을 다 강조하지 못하므로, 맥락에 따라 다른 답이 채택될 것으로 원문은 봅니다.",
    "쓰임이 워낙 갈리고 시장이 커서 경쟁 기술이 여럿 남아 있습니다.",
]):
    d.t(44, NY + 50 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(542, [("짧은 거리 · 저에너지", INFO), ("넓은 지역 · 저에너지", OK), ("넓은 지역 · 고속", ACC)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-05.iot-tradeoff.svg"
d.save(out)
print("→", out)
