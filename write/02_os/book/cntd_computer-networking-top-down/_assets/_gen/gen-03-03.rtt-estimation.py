# 03-03 §4 — 원문 3.5.3 의 세 공식을 실제 왕복 시간 표본에 돌린 결과.
# 표본은 이 기계에서 원문 그림이 쓰는 서버(gaia.cs.umass.edu)까지 ping -c 30 으로 실측한 값이다.
# ICMP 왕복 시간이라 TCP 의 SampleRTT 와 완전히 같지는 않지만 공식의 반응은 그대로 보인다 — 본문에도 이 유보를 적어 두었다.
# 타입 스펙: type-line — 연속 지표 위의 추세. 꺾은선으로 그리고 초점 계열에만 꼭짓점을 찍는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

SAMPLES = [202.63, 204.03, 202.29, 201.43, 212.92, 202.29, 203.28, 205.47, 201.71, 204.90,
           210.97, 201.91, 201.91, 201.45, 201.70, 205.41, 206.15, 201.86, 201.59, 205.51,
           201.79, 202.05, 208.13, 201.98, 201.57, 205.36, 202.68, 202.86, 201.32, 204.21]
EST = [202.63, 202.80, 202.74, 202.58, 203.87, 203.67, 203.62, 203.85, 203.58, 203.75,
       204.65, 204.31, 204.01, 203.69, 203.44, 203.69, 203.99, 203.73, 203.46, 203.72,
       203.48, 203.30, 203.90, 203.66, 203.40, 203.65, 203.52, 203.44, 203.18, 203.30]

W, H = 1000, 604
PX0, PX1, PY0, PY1 = 150, 900, 140, 396
YMIN, YMAX = 200.0, 214.0

d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 03-03 §4",
      "표본은 튀고 추정은 눌립니다",
      "원문 Figure 3.31 과 같은 그림을 실측으로. gaia.cs.umass.edu 까지 왕복 시간 30회와 그 위에서 도는 EstimatedRTT.",
      "α = 0.125 로 계산했습니다 — 표본 하나가 튀어도 추정치는 조금만 움직입니다")

def xp(i): return PX0 + i / (len(SAMPLES) - 1) * (PX1 - PX0)
def yp(v): return PY1 - (v - YMIN) / (YMAX - YMIN) * (PY1 - PY0)

for g in (200, 203, 206, 209, 212):
    y = yp(g)
    d.line(PX0, y, PX1, y, RULE, 0.8)
    d.t(PX0 - 12, y + 4, f"{g}", 11, MUTED, MONO, "end")
d.line(PX0, PY0, PX0, PY1, RULE, 1.0)
d.line(PX0, PY1, PX1, PY1, MUTED, 1.0)
d.t(PX0 - 12, PY0 - 16, "왕복 시간 (ms)", 11, SOFT, KR, "end")
d.t((PX0 + PX1) / 2, PY1 + 28, "표본 번호 — 30회", 11, SOFT, KR)

pts = " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, v in enumerate(SAMPLES))
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{MUTED}" stroke-width="1.2" stroke-dasharray="4 3"/>')
pts = " ".join(f"{xp(i):.1f},{yp(v):.1f}" for i, v in enumerate(EST))
d.o.append(f'<polyline points="{pts}" fill="none" stroke="{ACC}" stroke-width="1.8" stroke-linejoin="round"/>')
for i in (0, 4, 10, 22, 29):
    d.o.append(f'<circle cx="{xp(i):.1f}" cy="{yp(EST[i]):.1f}" r="4" fill="{ACC}"/>')

# 튀는 표본 하나를 짚는다
d.line(xp(4), yp(212.92), xp(4), yp(212.92) - 30, SOFT, 0.8, "3 3")
d.t(xp(4) + 8, yp(212.92) - 34, "표본 212.92 — 추정치는 203.87 로만 움직입니다", 11, SOFT, KR, "start")

d.box(PX0 - 130, 440, 700, 82, PAPER2, RULE, 0.9, 6)
d.t(PX0 - 112, 466, "TimeoutInterval = EstimatedRTT + 4 · DevRTT", 12, INK, MONO, "start", 600)
d.t(PX0 - 112, 490, "607.89 ms (1회) → 208.92 ms (30회) 로 수렴 · DevRTT 는 101.31 → 1.40", 11, ACC, MONO, "start")
d.t(PX0 - 112, 512, "경로가 안정적일수록 타임아웃이 왕복 시간에 바짝 붙습니다", 11, SOFT, KR, "start")

d.legend(H - 44, [("EstimatedRTT", ACC), ("SampleRTT", MUTED)])
d.save("03-03.rtt-estimation.svg")
