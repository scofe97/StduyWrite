# 타입 스펙: type-line — 큐잉 지연으로 인한 추정 RTT 변화 추이.
# 사실 출처: ch16.txt 1084(최소 15.9ms), 1509-1511(seq 340k 부근 RTT 감소 시작, 값 없음), 1525(하한 약 17ms), 1642(seq 720k 6.5s, 안정 2.0s), 1889행(사건 7 RTO 전 800ms).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-03",
      "라우터 큐잉 지연에 따른 추정 RTT 변화",
      "송신 속도가 병목 용량을 초과하면 버퍼가 차올라 RTT가 치솟고, 송신이 멎으면 큐가 비워집니다.",
      "표시한 점과 기준선만 관측값이며, 점 사이의 개형은 그리지 않았습니다")

X0, X1 = 80, 800
Y0, Y_TOP = 380, 130

def get_x(seq):
    return X0 + (seq / 2621440.0) * (X1 - X0)

def get_y(rtt):
    return Y0 - (rtt / 7.0) * (Y0 - Y_TOP)

# 축 및 그리드
d.line(X0, Y0, X1, Y0, RULE, 1.2)
d.line(X0, Y0, X0, Y_TOP - 10, RULE, 1.2)

# Y 눈금
for rtt, lab in [(0, "0s"), (2.0, "2.0s"), (4.0, "4.0s"), (6.5, "6.5s")]:
    y = get_y(rtt)
    d.line(X0, y, X1, y, RULE, 0.6, dash="3 3")
    d.t(X0 - 10, y + 4, lab, 10, SOFT, MONO, "end")

# X 눈금
for seq, lab in [(0, "0"), (500000, "500k"), (1000000, "1000k"), (1500000, "1500k"), (2000000, "2000k"), (2621440, "2621k")]:
    x = get_x(seq)
    d.line(x, Y0, x, Y0 + 5, RULE, 1.0)
    d.t(x, Y0 + 18, lab, 10, SOFT, MONO, "middle")

d.t(16, Y_TOP - 16, "추정 RTT (초)", 11, INK, KR, "start", 600)
d.t(X1 + 14, Y0 + 4, "누적 바이트", 11, INK, KR, "start", 600)

# 기준선 1: 물리 최소 RTT 15.9ms (전 구간 기준선)
y_min = get_y(0.016)
d.line(X0, y_min, X1, y_min, OK, 1.2, dash="4 4")
d.t(get_x(340000) + 10, y_min - 8, "경로 최소 RTT 15.9ms", 11, OK, KR, "start")

# 기준선 2: 720k 이전 안정 RTT 약 2s (전 구간 기준선)
y_stable = get_y(2.0)
d.line(X0, y_stable, get_x(720000), y_stable, INFO, 1.2, dash="4 4")
d.t(get_x(340000) + 10, y_stable - 8, "720k 이전 안정 RTT 약 2s", 11, INFO, KR, "start")

# 관측값 세 점만 표시하고 점 사이는 잇지 않는다(개형은 알려지지 않음)
# 1. seq 340k 부근: RTT 가 줄기 시작 (값 미기재 → 화살표만)
x_340 = get_x(340000)
d.line(x_340, Y0, x_340, y_stable - 70, WARN, 1.2, dash="2 4")
d.t(x_340 + 8, y_stable - 56, "seq 340k 부근: 송신이 멈추자 RTT 감소 시작", 11, WARN, KR, "start")

# 2. seq 720k: 약 6.5s
x_720, y_720 = get_x(720000), get_y(6.5)
d.o.append(f'<circle cx="{x_720:.1f}" cy="{y_720:.1f}" r="5" fill="{BAD}"/>')
d.t(x_720 + 12, y_720 - 8, "seq 720k: RTT 약 6.5s (안정 시 약 2s의 3배 이상)", 11, BAD, KR, "start", 600)

# 3. seq 1774k: 사건 7 직전 약 800ms
x_1774, y_1774 = get_x(1773801), get_y(0.8)
d.o.append(f'<circle cx="{x_1774:.1f}" cy="{y_1774:.1f}" r="4.5" fill="{INFO}"/>')
d.t(x_1774, y_1774 + 20, "seq 1774k: RTT 약 800ms (사건 7)", 11, INFO, KR, "middle")

# 범례 (단축하여 가로 폭 920 이내 보장)
d.legend(H - 44, [
        ("안정 약 2s", INFO),
    ("최소 15.9ms", OK),
    ("폭증 6.5s", BAD),
    ("RTT 감소 시작", WARN),
])

d.save("16-03.estimated-rtt.svg")
