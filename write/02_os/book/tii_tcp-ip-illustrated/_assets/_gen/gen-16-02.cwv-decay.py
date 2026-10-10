# 타입 스펙: type-line — 유휴 경과 시간에 따른 cwnd 지수 감쇠 및 ssthresh 보존 (계산 예시).
# 사실 출처: RFC 2861 §3 · RFC 7661 · ch16.txt 921~1001행
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02 §5", "유휴 시간에 따른 혼잡 창 감쇠와 문턱 보존 (계산 예시)",
      "초기 cwnd = 32 SMSS, 직전 ssthresh = 16 SMSS 에서 1 RTO 이상의 유휴가 발생한 상황이다. CWV(RFC 2861)는 ssthresh 를 max(ssthresh, 3/4·cwnd) = 24 SMSS 로 보존하고, 유휴 1 RTO(RTT 상한)마다 cwnd 를 반감해 5 RTO 뒤 하한선 1 SMSS 에 도달한다.",
      "유휴 RTO 마다 cwnd 는 반감되고 이전 기억은 ssthresh 가 보존합니다")

PX0, PX1 = 100, 860
PY0, PY1 = 120, 400

def x(rtt):
    return PX0 + rtt * (PX1 - PX0) / 5

def y(v):
    return PY1 - v * (PY1 - PY0) / 36

# Y축 격자선 (0 ~ 36 SMSS)
for v in range(0, 37, 6):
    d.line(PX0, y(v), PX1, y(v), RULE, 0.6)
    d.t(PX0 - 14, y(v) + 4, f"{v}", 11, SOFT, MONO, "end")
d.t(PX0 - 14, PY0 - 10, "SMSS", 11, MUTED, MONO, "end")

# X축 격자선 및 레이블 (0 ~ 5 RTO)
for rtt in range(0, 6):
    d.line(x(rtt), PY0, x(rtt), PY1, RULE, 0.6)
    d.t(x(rtt), PY1 + 20, f"{rtt} RTO", 11, SOFT, MONO)
d.t((PX0 + PX1)/2, PY1 + 42, "유휴 경과 시간 (1 RTO 단위, RTT 상한)", 12, MUTED, KR)

# ssthresh 갱신 보존선 (24 SMSS)
d.line(PX0, y(24), PX1, y(24), OK, 1.4, "6 4")
d.t(PX1 - 10, y(24) - 12, "ssthresh = 24 SMSS 보존 (3/4 · cwnd)", 12, OK, KR, "end", 600)

# 이전 ssthresh 선 (16 SMSS)
d.line(PX0, y(16), PX1, y(16), SOFT, 1.0, "3 4")
d.t(PX1 - 10, y(16) + 18, "이전 ssthresh = 16 SMSS", 12, SOFT, KR, "end")

# 하한선 1 SMSS 기준선
d.line(PX0, y(1), PX1, y(1), SOFT, 1.0, "2 3")
d.t(PX0 + 14, y(1) - 8, "하한선 cwnd = 1 SMSS (느린 시작 진입)", 11, SOFT, KR, "start", 600)

# cwnd 감쇠 곡선 데이터 (32, 16, 8, 4, 2, 1)
cwnds = [32, 16, 8, 4, 2, 1]
pts_cwnd = " ".join(f"{x(rtt):.1f},{y(v):.1f}" for rtt, v in enumerate(cwnds))
d.o.append(f'<polyline points="{pts_cwnd}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linejoin="round"/>')
for rtt, v in enumerate(cwnds):
    d.o.append(f'<circle cx="{x(rtt):.1f}" cy="{y(v):.1f}" r="4" fill="{ACC}"/>')
    if v == 4:
        d.t(x(rtt) + 12, y(v) + 14, f"{v}", 11, ACC, MONO, "start", 600)
    elif v == 16:
        d.t(x(rtt) - 14, y(v) + 16, f"{v}", 11, ACC, MONO, "end", 600)
    else:
        d.t(x(rtt) + 12, y(v) - 10, f"{v}", 11, ACC, MONO, "start", 600)

# 강조 설명 (중간 상단 여백에 상자 배치: y=225~247 로 y=213 및 y=260 격자선 회피)
d.box(350, 226, 160, 22, PAPER2, ACC, 0.8, 4)
d.t(430, 241, "RTO 마다 50% 반감 감쇠", 11, ACC, KR, "middle", 600)

d.legend(H - 44, [
    ("cwnd (유휴 지수 감쇠)", ACC),
    ("ssthresh (이전 문턱 기억)", OK),
    ("기준선 (이전 문턱 · 하한선)", SOFT)
])

d.save("16-02.cwv-decay.svg")
