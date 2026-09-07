# 타입 스펙: type-line — 시간이 아닌 두 변수의 연속 추세. 대역폭과 SNR 이 용량에 다르게 붙는다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §7.2.1 섀넌 용량 정리와
#   그 아래 두 결론(대역폭에 선형, 높은 SNR 에서 로그). SNR 최소값은 원문의 [Meraki 2023] 인용
import math, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, INFO, OK, KR, MONO

W, H = 940, 568
d = D(W, H, "SECTION 7.2.1 · SHANNON CAPACITY",
      "폭은 정직하게 갚고, 세기는 갈수록 인색합니다",
      "섀넌 용량은 대역폭에 비례하지만 SNR 에는 로그로만 늘어난다. 그래서 투자할 곳이 갈린다.",
      "가로축은 dB 가 아니라 선형 비입니다. 원문이 sublinearly 라 적은 기준이 이쪽입니다")

YB, YT = 336, 148
CMAX = 280.0


def fy(c):
    return YB - (c / CMAX) * (YB - YT)


def axes(x0, x1, ticks, span, xlabel):
    d.line(x0, YB, x1, YB, RULE, 1.0)
    d.line(x0, YB, x0, YT - 8, RULE, 1.0)
    for v, lab in ticks:
        x = x0 + (x1 - x0) * v / span
        d.line(x, YB, x, YB + 6, RULE, 1.0)
        d.t(x, YB + 22, lab, 10, SOFT, MONO)
    d.t((x0 + x1) / 2, YB + 44, xlabel, 11, MUTED, KR)
    for c in (0, 70, 140, 210, 280):
        d.line(x0 - 6, fy(c), x0, fy(c), RULE, 1.0)
        d.t(x0 - 12, fy(c) + 4, str(c), 10, SOFT, MONO, "end")


AX0, AX1 = 88, 430
BX0, BX1 = 540, 884
SPAN_B = 1000.0
axes(AX0, AX1, [(0, "0"), (10, "10"), (20, "20"), (30, "30"), (40, "40")], 40.0,
     "채널 대역폭 B (MHz) · SNR 비 100 고정")
axes(BX0, BX1, [(0, "0"), (250, "250"), (500, "500"), (750, "750"), (1000, "1000")], SPAN_B,
     "신호 대 잡음 비 (선형) · 대역폭 20 MHz 고정")
d.t(40, YT - 26, "용량 C (Mbps)", 11, MUTED, KR, "start")

# 왼쪽 — C = B·log2(1+100), B 에 선형
ptsA = [(AX0 + (AX1 - AX0) * b / 40.0, fy(b * math.log2(101.0))) for b in range(0, 41)]
d.path(" ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(ptsA)), INFO, 2.0)

# 오른쪽 — C = 20·log2(1+r), 신호 대 잡음 비 r 에 로그
ptsB = [(BX0 + (BX1 - BX0) * r / SPAN_B, fy(20.0 * math.log2(1.0 + r)))
        for r in [i * 4.0 for i in range(0, 251)]]
d.path(" ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(ptsB)), INFO, 2.0)

# focal — 비를 100 에서 1000 으로 열 배 올려도 용량은 1.5 배에 못 미친다
seg = [p for p in ptsB if p[0] >= BX0 + (BX1 - BX0) * 100.0 / SPAN_B]
d.path(" ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(seg)), ACC, 3.0)
for r, lab, lx, ly, anc in ((100.0, "비 100 · 133 Mbps", 12, YB - 28, "start"),
                            (1000.0, "비 1000 · 199 Mbps", -8, YB - 28, "end")):
    x = BX0 + (BX1 - BX0) * r / SPAN_B
    y = fy(20.0 * math.log2(1.0 + r))
    d.line(x, y, x, YB, ACC, 0.9, "3 5")
    d.t(x + lx, ly, lab, 10, ACC, KR, anc)
d.t(BX0 + 16, fy(268), "비를 열 배 올려도 용량은 1.5 배가 안 됩니다", 11, ACC, KR, "start", 600)

d.t(AX0 + 16, fy(240), "B 를 두 배 하면 C 도 두 배", 11, INFO, KR, "start", 600)

PY = 418
d.box(24, PY, 880, 80, PAPER2, RULE, 1.0)
d.t(44, PY + 26, "C = B · log₂(1 + 수신 신호 전력 / 잡음 전력)", 13, INK, MONO, "start", 600)
d.t(44, PY + 52, "이 값은 상한입니다. 아무리 영리하게 부호화하고 변조해도 이보다 많이 받을 수 없습니다.",
    11, MUTED, KR, "start")
d.t(44, PY + 70, "원문이 든 실무 최소 SNR — WiFi 는 20 dB 안팎, LTE 는 변조 방식에 따라 −5 에서 18 dB.",
    11, OK, KR, "start")

d.legend(518, [("용량 곡선", INFO), ("더 밀어도 안 느는 구간", ACC), ("실무 최소 SNR", OK)])

out = pathlib.Path(__file__).resolve().parent.parent / "07-01.shannon-limits.svg"
d.save(out)
print("→", out)
