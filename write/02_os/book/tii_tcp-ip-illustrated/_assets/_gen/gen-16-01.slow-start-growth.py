# 타입 스펙: type-line — 왕복 횟수(RTT)에 따른 cwnd 크기 추세. 느린 시작의 지수 증가와 혼잡 회피의 선형 증가를 계산 예시로 견준다.
# 사실 출처: ch16.txt 380~480행 — 느린 시작(2^k 지수 증가), ssthresh 전환, 혼잡 회피(왕복당 1 SMSS 선형 증가), 지연 ACK 완만화.
# 계산 공식: IW=1, ssthresh=16 SMSS 기준. RTT 0~4 지수(1→2→4→8→16), RTT 5~10 선형(+1/RTT).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-01 §3",
      "왕복 횟수별 혼잡 창(cwnd) 증가 추세 (계산 예시)",
      "초기 창 IW=1 에서 시작해 ssthresh=16 에 도달할 때까지 매 왕복마다 cwnd 가 두 배로 급증한다. ssthresh 에 도달하면 혼잡 회피로 전환되어 왕복당 1 SMSS 씩 선형 증가한다. 지연 ACK 환경에서는 증가율이 완만해진다.",
      "임계값 전에는 지수적으로 급등하고, 임계값 이후에는 선형으로 다듬어집니다")

PX0, PX1, PY0, PY1 = 80, 860, 120, 430
X_MAX = 10
Y_MAX = 36

def x(rtt): return PX0 + rtt * (PX1 - PX0) / X_MAX
def y(val): return PY1 - val * (PY1 - PY0) / Y_MAX

# Y축 격자선
for val in [0, 8, 16, 24, 32]:
    d.line(PX0, y(val), PX1, y(val), RULE, 0.6)
    d.t(PX0 - 12, y(val) + 4, f"{val}", 11, SOFT, MONO, "end")
d.t(PX0, PY0 - 12, "cwnd (SMSS)", 11, MUTED, KR, "start")

# X축 레이블
for rtt in range(0, 11):
    d.line(x(rtt), PY1, x(rtt), PY1 + 6, RULE, 0.8)
    d.t(x(rtt), PY1 + 20, f"{rtt}", 11, SOFT, MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "왕복 횟수 (RTT)", 12, MUTED, KR, "middle")

# ssthresh 기준선 (가로 점선)
d.line(PX0, y(16), PX1, y(16), WARN, 1.0, "5 4")
d.t(x(1) + 80, y(16) - 8, "ssthresh = 16 SMSS (전환 기준)", 11, WARN, KR, "start", 600)

# 계열 1: 표준 복합 경로 (초점: 느린 시작 → 혼잡 회피)
# RTT 0~4: 1, 2, 4, 8, 16
# RTT 5~10: 17, 18, 19, 20, 21, 22
data_standard = [1, 2, 4, 8, 16, 17, 18, 19, 20, 21, 22]
pts_std = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(data_standard))
d.o.append(f'<polyline points="{pts_std}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linejoin="round"/>')
for i, v in enumerate(data_standard):
    d.o.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="4" fill="{ACC}"/>')

# 계열 2: 순수 지수 증가 계속 시 (가상 상한 없는 경로, RTT 0~5)
data_pure_ss = [1, 2, 4, 8, 16, 32]
pts_ss = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(data_pure_ss))
d.o.append(f'<polyline points="{pts_ss}" fill="none" stroke="{INFO}" stroke-width="1.4" stroke-dasharray="4 4" stroke-linejoin="round"/>')
d.o.append(f'<circle cx="{x(5):.1f}" cy="{y(32):.1f}" r="3.5" fill="{PAPER}" stroke="{INFO}" stroke-width="1.2"/>')

# 계열 3: 지연 ACK 환경 (RTT당 ~1.5배 증가, 올림 규칙 일관 적용 및 CA 구간 +0.5)
# RTT 0~6 느린 시작: 1, 2, 3, 5, 8, 12, 16(ssthresh 도달)
# RTT 7~10 혼잡 회피: 16.5, 17, 17.5, 18 (+0.5/RTT)
data_del_ack = [1, 2, 3, 5, 8, 12, 16, 16.5, 17, 17.5, 18]
pts_del = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(data_del_ack))
d.o.append(f'<polyline points="{pts_del}" fill="none" stroke="{OK}" stroke-width="1.6" stroke-linejoin="round"/>')
for i, v in enumerate(data_del_ack):
    d.o.append(f'<circle cx="{x(i):.1f}" cy="{y(v):.1f}" r="3" fill="{PAPER}" stroke="{OK}" stroke-width="1.2"/>')

# 주석 레이블 (간격 겹침 및 선 관통 없이 배치)
d.t(x(2), y(10), "느린 시작 (지수 증가)", 11, ACC, KR, "middle", 600)
d.t(x(7), y(19) - 14, "혼잡 회피 (선형 +1)", 11, ACC, KR, "middle", 600)
d.t(x(5) + 8, y(32) - 10, "이론상 지수 폭증 (2^k)", 11, INFO, KR, "start")
d.t(x(4) + 18, y(5), "지연 ACK (완만한 증가)", 11, OK, KR, "start")

d.legend(H - 48, [
    ("표준 복합", ACC),
    ("지연 ACK", OK),
    ("무제한 지수", INFO),
    ("ssthresh", WARN),
])

d.save("16-01.slow-start-growth.svg")
