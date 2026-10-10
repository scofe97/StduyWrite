# 타입 스펙: type-line — 경과 시간(t)에 따른 CUBIC 혼잡 창 W(t) 삼차 함수 성장 곡선 (계산 예시).
# 사실 출처: ch16.txt 2350~2480행, RFC 9438, net/ipv4/tcp_cubic.c — C=0.4, β=0.7, Wmax=1000, K=9.1초.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-04 §4",
      "CUBIC 의 시간 기반 혼잡 창 성장 곡선 (계산 예시)",
      "CUBIC은 W(t)=C(t-K)³+Wmax 공식에 따라 손실 직후 오목하게 빠르게 복구하고, 직전 최대치 Wmax 근처에서 평탄하게 안정성을 유지한 뒤, 볼록하게 가속하며 새 대역폭을 탐색한다(비교선: RTT 100ms 가정).",
      "오목한 복구와 볼록한 탐색 사이 평탄한 안정 구간이 네트워크를 보호합니다")

PX0, PX1 = 100, 840
PY0, PY1 = 120, 420

# 파라미터 (RFC 9438 및 Linux tcp_cubic.c)
C = 0.4
BETA = 0.7
W_MAX = 1000.0
W_START = W_MAX * BETA  # 700
# K = ((W_MAX * (1 - BETA)) / C) ** (1/3) = (300 / 0.4) ** (1/3) = 750 ** (1/3) ≈ 9.0856
K = (300.0 / C) ** (1.0 / 3.0)

T_MAX = 18.0
Y_MIN = 400.0
Y_MAX = 1400.0

def x(t): return PX0 + t * (PX1 - PX0) / T_MAX
def y(w): return PY1 - (w - Y_MIN) * (PY1 - PY0) / (Y_MAX - Y_MIN)

# Y축 격자선
for val in [400, 600, 800, 1000, 1200, 1400]:
    y_pos = y(val)
    d.line(PX0, y_pos, PX1, y_pos, RULE, 0.6)
    d.t(PX0 - 12, y_pos + 4, f"{val}", 11, SOFT, MONO, "end")
d.t(PX0, PY0 - 12, "창 크기 W(t) (패킷)", 11, MUTED, KR, "start")

# X축 레이블
for sec in [0, 3, 6, 9, 12, 15, 18]:
    x_pos = x(sec)
    d.line(x_pos, PY1, x_pos, PY1 + 6, RULE, 0.8)
    d.t(x_pos, PY1 + 20, f"{sec}s", 11, SOFT, MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "손실 발생 후 경과 시간 t (초)", 12, MUTED, KR, "middle")

# Wmax 기준선 (가로 점선)
d.line(PX0, y(W_MAX), PX1, y(W_MAX), WARN, 1.0, "4 4")
d.t(PX1 - 10, y(W_MAX) + 16, "Wmax = 1,000 (직전 손실 지점)", 11, WARN, KR, "end", 600)

# K 시점 기준선 (세로 점선)
d.line(x(K), PY0, x(K), PY1, WARN, 1.0, "4 4")
d.t(x(K), PY0 - 8, f"K = {K:.1f}s (Wmax 도달 시점)", 11, WARN, KR, "middle", 600)

# 계열 1: CUBIC 곡선 W(t) = C*(t-K)^3 + Wmax
cubic_pts = []
STEPS = 90
for i in range(STEPS + 1):
    t_val = i * T_MAX / STEPS
    w_val = C * ((t_val - K) ** 3) + W_MAX
    cubic_pts.append((x(t_val), y(w_val)))
poly_cubic = " ".join(f"{px:.1f},{py:.1f}" for px, py in cubic_pts)
d.o.append(f'<polyline points="{poly_cubic}" fill="none" stroke="{ACC}" stroke-width="2.6" stroke-linejoin="round"/>')

# 계열 2: 표준 Reno 선형 비교군 (RTT=100ms 기준, 1초당 10패킷 증가)
reno_pts = []
for i in range(STEPS + 1):
    t_val = i * T_MAX / STEPS
    w_val = W_MAX * 0.5 + t_val * 10.0  # Reno 는 손실 시 절반(500)에서 출발, RTT 100ms -> +10/sec
    reno_pts.append((x(t_val), y(w_val)))
poly_reno = " ".join(f"{px:.1f},{py:.1f}" for px, py in reno_pts)
d.o.append(f'<polyline points="{poly_reno}" fill="none" stroke="{INFO}" stroke-width="1.6" stroke-dasharray="4 4" stroke-linejoin="round"/>')

# 주요 지점 마커
# t = 0: 시작점 W = 700
d.o.append(f'<circle cx="{x(0):.1f}" cy="{y(W_START):.1f}" r="4.5" fill="{ACC}"/>')
d.t(x(0) + 14, y(W_START) + 16, "손실 직후 (β·Wmax = 700)", 11, ACC, KR, "start")

# t = K: Wmax 도달 지점 (변곡점)
d.o.append(f'<circle cx="{x(K):.1f}" cy="{y(W_MAX):.1f}" r="4.5" fill="{WARN}"/>')
d.t(x(K) - 14, y(W_MAX) - 14, "안정 평탄 지대 (증가율 0 수렴)", 11, WARN, KR, "end", 600)

# t = 2K ≈ 18.2: 볼록 탐색 지점
w_2k = C * ((18.0 - K) ** 3) + W_MAX
d.o.append(f'<circle cx="{x(18.0):.1f}" cy="{y(w_2k):.1f}" r="4.5" fill="{ACC}"/>')
d.t(x(18.0) - 14, y(w_2k) - 14, "볼록 탐색 (가속 Probing)", 11, ACC, KR, "end", 600)

# 영역 라벨
d.t(x(4.0), y(860), "오목 구간 (빠른 수렴)", 11, MUTED, KR, "middle")
d.t(x(13.5), y(1110), "볼록 구간 (새 대역폭 탐색)", 11, MUTED, KR, "middle")

d.legend(H - 44, [
    ("CUBIC (삼차 곡선, 초점)", ACC),
    ("Reno 선형 모델 (RTT 100ms 가정)", INFO),
    ("임계값 (Wmax · K)", WARN),
])

d.save("16-04.cubic-growth-curve.svg")
