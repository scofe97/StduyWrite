# 타입 스펙: type-line — 손실 발생 후 Tahoe 와 Reno 의 cwnd 변화 추세 비교 (계산 예시).
# 사실 출처: ch16.txt 570~670행 — Tahoe(손실 시 cwnd=1 및 느린 시작 재개), Reno(빠른 회복, cwnd=ssthresh=FlightSize/2 에서 혼잡 회피 재개).
# 계산 공식: IW=1, 초기 ssthresh=16, RTT 8에서 cwnd=20 시 손실(FlightSize=20). 신규 ssthresh=10.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-01 §5",
      "손실 발생 후 Tahoe 와 Reno 의 cwnd 변화 추세 (계산 예시)",
      "동일하게 RTT 8에서 cwnd=20 시점에 3개 중복 ACK 손실이 발생했을 때의 비교다. Tahoe 는 cwnd=1 로 떨어져 느린 시작을 다시 밟지만 Reno 는 빠른 회복을 거쳐 절반인 cwnd=10 에서 곧바로 혼잡 회피를 재개한다.",
      "Tahoe 는 파이프를 비우고, Reno 는 파이프를 채운 채 절반에서 다시 시작합니다")

PX0, PX1, PY0, PY1 = 80, 860, 120, 430
X_MAX = 15
Y_MAX = 24

def x(rtt): return PX0 + rtt * (PX1 - PX0) / X_MAX
def y(val): return PY1 - val * (PY1 - PY0) / Y_MAX

# Y축 격자선
for val in [0, 5, 10, 15, 20]:
    d.line(PX0, y(val), PX1, y(val), RULE, 0.6)
    d.t(PX0 - 12, y(val) + 4, f"{val}", 11, SOFT, MONO, "end")
d.t(PX0, PY0 - 12, "cwnd (SMSS)", 11, MUTED, KR, "start")

# X축 레이블
for rtt in range(0, 16):
    d.line(x(rtt), PY1, x(rtt), PY1 + 6, RULE, 0.8)
    d.t(x(rtt), PY1 + 20, f"{rtt}", 11, SOFT, MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "시간 경과 (RTT)", 12, MUTED, KR, "middle")

# 손실 시점 수직선 (RTT 8)
d.line(x(8), PY0, x(8), PY1, WARN, 1.0, "4 4")
d.t(x(8), PY0 - 8, "손실 발생 (중복 ACK 3개)", 11, WARN, KR, "middle", 600)

# ssthresh 기준선
# 1) 초기 ssthresh = 16 (손실 전 RTT 0~8 적용)
d.line(PX0, y(16), x(8), y(16), OK, 0.9, "3 3")
d.t(x(1) + 20, y(16) - 8, "초기 ssthresh = 16 SMSS", 11, OK, KR, "start", 600)

# 2) 신규 ssthresh = 10 (손실 후 RTT 8~15 적용)
d.line(x(8), y(10), PX1, y(10), OK, 0.9, "3 3")
d.t(x(9) + 8, y(10) + 18, "신규 ssthresh = 10 SMSS", 11, OK, KR, "start", 600)

# RTT 0~8 공통 구간: [1, 2, 4, 8, 16, 17, 18, 19, 20]
common_data = [1, 2, 4, 8, 16, 17, 18, 19, 20]
pts_com = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(common_data))
d.o.append(f'<polyline points="{pts_com}" fill="none" stroke="{SOFT}" stroke-width="1.8" stroke-linejoin="round"/>')
for i, v in enumerate(common_data):
    d.o.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3.5" fill="{SOFT}"/>')

# RTT 8~15 Reno 계열 (초점): [20, 10, 11, 12, 13, 14, 15, 16]
reno_data = [(8, 20), (9, 10), (10, 11), (11, 12), (12, 13), (13, 14), (14, 15), (15, 16)]
pts_reno = " ".join(f"{x(r):.1f},{y(v):.1f}" for r, v in reno_data)
d.o.append(f'<polyline points="{pts_reno}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linejoin="round"/>')
for r, v in reno_data:
    d.o.append(f'<circle cx="{x(r):.1f}" cy="{y(v):.1f}" r="4" fill="{ACC}"/>')

# RTT 8~15 Tahoe 계열: [20, 1, 2, 4, 8, 10, 11, 12]
tahoe_data = [(8, 20), (9, 1), (10, 2), (11, 4), (12, 8), (13, 10), (14, 11), (15, 12)]
pts_tahoe = " ".join(f"{x(r):.1f},{y(v):.1f}" for r, v in tahoe_data)
d.o.append(f'<polyline points="{pts_tahoe}" fill="none" stroke="{INFO}" stroke-width="1.8" stroke-dasharray="5 3" stroke-linejoin="round"/>')
for r, v in tahoe_data:
    d.o.append(f'<circle cx="{x(r):.1f}" cy="{y(v):.1f}" r="3.5" fill="{PAPER}" stroke="{INFO}" stroke-width="1.2"/>')

# 곡선 위 주석 레이블 (선 관통 없이 배치)
d.t(x(2), y(8), "초기 느린 시작", 11, SOFT, KR, "middle", 600)
d.t(x(6), y(21.5), "혼잡 회피 (선형 증가)", 11, SOFT, KR, "middle", 600)
d.t(x(12), y(16) - 14, "Reno · 절반(10)에서 선형 재개", 11, ACC, KR, "middle", 600)
d.t(x(9) + 6, y(7), "Tahoe · 1부터 느린 시작 재개", 11, INFO, KR, "start", 600)

d.legend(H - 48, [
    ("TCP Reno", ACC),
    ("TCP Tahoe", INFO),
    ("손실 시점", WARN),
    ("ssthresh", OK),
])

d.save("16-01.tahoe-vs-reno.svg")
