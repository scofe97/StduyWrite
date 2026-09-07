# 타입 스펙: type-scatter — 두 변수의 분포. I·Q 평면 위의 심볼 배치가 곧 성상도다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.2 Figure 7.14 · Figure 7.15 · Figure 7.16 —
#   심볼 개수와 심볼당 비트 수, 그리고 잡음이 오판을 만드는 방식은 원문 그대로
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, BAD, KR, MONO

W, H = 940, 572
d = D(W, H, "SECTION 7.2.2 · CONSTELLATION DIAGRAMS",
      "점을 촘촘히 놓을수록 많이 싣고 쉽게 틀립니다",
      "성상도의 한 점이 심볼 하나다. 점이 늘면 심볼당 비트가 늘지만 이웃과의 거리가 좁아진다.",
      "심볼 수와 심볼당 비트 수는 원문 Figure 7.15 의 것입니다")

PANELS = [
    (32, "QPSK · 4-QAM", 4, 2, INFO),
    (336, "16-QAM", 16, 4, OK),
    (640, "64-QAM", 64, 6, ACC),
]
PW, PY, PH = 268, 118, 268


def grid_points(n):
    side = int(round(math.sqrt(n)))
    step = 200.0 / (side - 1) if side > 1 else 0
    return [(-100 + c * step, -100 + r * step) for r in range(side) for c in range(side)]


for px, name, n, bits, c in PANELS:
    d.box(px, PY, PW, PH, PAPER2, RULE, 1.0)
    cx, cy = px + PW / 2, PY + PH / 2 + 8
    d.t(px + PW / 2, PY + 26, name, 13, c, KR, "middle", 600)
    d.line(cx - 116, cy, cx + 116, cy, RULE, 0.9)
    d.line(cx, cy - 116, cx, cy + 116, RULE, 0.9)
    d.t(cx + 122, cy + 4, "I", 10, SOFT, MONO, "start")
    d.t(cx + 10, cy - 104, "Q", 10, SOFT, MONO, "start")
    if n == 4:
        pts = [(70.7 * sx, 70.7 * sy) for sx in (-1, 1) for sy in (-1, 1)]
    else:
        pts = grid_points(n)
    r = 4.5 if n <= 16 else 2.8
    for dx, dy in pts:
        d.o.append(f'<circle cx="{cx + dx * 0.5:.1f}" cy="{cy - dy * 0.5:.1f}" r="{r}" fill="{c}"/>')
    d.t(px + PW / 2, PY + PH - 14, f"심볼 {n} 개 · 심볼당 {bits} 비트", 11, MUTED, KR)

# 잡음 산포 — 16-QAM 패널의 오른쪽 위 심볼 하나 주변
NP = PANELS[1]
ncx, ncy = NP[0] + PW / 2, PY + PH / 2 + 8
tx, ty = ncx + 100 * 0.5, ncy - 100 * 0.5
JITTER = [(6, -5), (-9, 7), (12, 9), (-4, -12), (15, -3), (-13, -6), (8, 14), (-26, 4)]
for jx, jy in JITTER:
    d.o.append(f'<circle cx="{tx + jx}" cy="{ty + jy}" r="3" fill="{ACC}" opacity="0.85"/>')
d.o.append(f'<circle cx="{tx - 26}" cy="{ty + 4}" r="5.5" fill="none" stroke="{BAD}" stroke-width="1.8"/>')
d.line(tx - 33.3, ty, tx - 26, ty + 4, BAD, 0.9, "2 3")
d.t(ncx, PY + 52, "잡음이 실제 수신점을 흩뿌립니다", 10, ACC, KR)

BY = PY + PH + 26
d.box(24, BY, 880, 92, PAPER2, RULE, 1.0)
d.t(44, BY + 26, "점 하나가 어긋나면 심볼 하나를 틀리게 읽습니다", 12, INK, KR, "start", 600)
LINES = [
    "16-QAM 에서 1111 을 보냈는데 수신점 하나가 이웃 1011 쪽으로 넘어가면 수신기는 1011 로 읽습니다.",
    "점이 촘촘할수록 그런 넘어감이 잦아지므로, 심볼 오류율과 비트 오류율이 함께 올라갑니다.",
]
for i, ln in enumerate(LINES):
    d.t(44, BY + 52 + i * 20, ln, 11, MUTED, KR, "start")

d.legend(BY + 112, [("QPSK", INFO), ("16-QAM", OK), ("64-QAM 과 잡음 산포", ACC), ("이웃으로 넘어간 점", BAD)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-02.constellations.svg"
d.save(out)
print("→", out)
