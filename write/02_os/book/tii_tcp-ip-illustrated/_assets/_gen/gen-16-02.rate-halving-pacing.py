# 타입 스펙: type-line — 회복 중 ACK 순서별 누적 송신 패킷 수 (Reno vs Rate Halving) (계산 예시).
# 사실 출처: RFC 9937 · RFC 6937 · Mathis & Mahdavi 1996 · ch16.txt 811~897행
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-02 §3", "손실 회복 중 ACK 순서별 누적 송신 패킷 (계산 예시)",
      "초기 창 W = 16 에서 1개 손실 후 목표 cwnd = 8 로 줄어드는 1 RTT 복구 구간이다(최대 15개 중복 ACK). Reno 는 앞쪽 8개 중복 ACK 동안 송신을 멈췄다가 9번째부터 ACK마다 1개씩(총 7개) 몰아서 보낸다. Rate Halving 은 2 ACK 마다 1 패킷을 보내 전송을 고르게 편다.",
      "Reno 는 멈췄다 몰아치고 Rate Halving 은 2 ACK 당 1 패킷으로 페이싱합니다")

PX0, PX1 = 100, 860
PY0, PY1 = 120, 400

def x(k):
    return PX0 + k * (PX1 - PX0) / 15

def y(v):
    return PY1 - v * (PY1 - PY0) / 8

# Y축 격자선 (0 ~ 8 세그먼트)
for v in range(0, 9, 2):
    d.line(PX0, y(v), PX1, y(v), RULE, 0.6)
    d.t(PX0 - 14, y(v) + 4, f"{v} seg", 11, SOFT, MONO, "end")

# X축 레이블 (0 ~ 15 ACK)
for k in range(0, 16):
    if k % 3 == 0 or k == 15:
        d.line(x(k), PY0, x(k), PY1, RULE, 0.6)
        d.t(x(k), PY1 + 20, str(k), 11, SOFT, MONO)
d.t((PX0 + PX1)/2, PY1 + 42, "회복 중 도착한 중복 ACK 개수 (k)", 12, MUTED, KR)

# Reno 데이터 (0~8 ACK는 0, 9~15 ACK는 1~7 증가)
reno = [0]*9 + [i for i in range(1, 8)]
pts_reno = " ".join(f"{x(k):.1f},{y(v):.1f}" for k, v in enumerate(reno))
d.o.append(f'<polyline points="{pts_reno}" fill="none" stroke="{INFO}" stroke-width="1.8" stroke-linejoin="round"/>')
for k, v in enumerate(reno):
    d.o.append(f'<circle cx="{x(k):.1f}" cy="{y(v):.1f}" r="3" fill="{PAPER}" stroke="{INFO}" stroke-width="1.2"/>')

# Rate Halving 데이터 (k // 2, 0~15 ACK)
rh = [k // 2 for k in range(16)]
pts_rh = " ".join(f"{x(k):.1f},{y(v):.1f}" for k, v in enumerate(rh))
d.o.append(f'<polyline points="{pts_rh}" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-linejoin="round"/>')
for k, v in enumerate(rh):
    d.o.append(f'<circle cx="{x(k):.1f}" cy="{y(v):.1f}" r="3.5" fill="{ACC}"/>')

# 강조 메모
# 1. Reno 침묵 구간 (상단 여백에 상자 배치 후 지시 화살표)
d.box(PX0 + 40, y(7) - 14, 180, 28, PAPER2, INFO, 0.8, 4)
d.t(PX0 + 130, y(7), "Reno 침묵 (약 0.5 RTT)", 12, INFO, KR, "middle", 600)
d.arrow([(PX0 + 130, y(7) + 16), (x(4), y(0) - 8)], INFO, "info", 1.2)

# 2. Reno 몰아치기 버스트 (우하단 여백에 상자 배치 후 지시 화살표)
d.box(x(11) - 20, y(1) - 14, 180, 28, PAPER2, INFO, 0.8, 4)
d.t(x(11) + 70, y(1), "Reno 후반 몰아치기 (7개)", 12, INFO, KR, "middle", 600)
d.arrow([(x(11) + 70, y(1) - 16), (x(12), y(4) + 8)], INFO, "info", 1.2)

# 3. Rate Halving 균일 페이싱
d.t(x(6), y(5) - 8, "2 ACK 당 1 패킷 송신", 12, ACC, KR, "middle", 600)
d.t(x(10), y(7) - 8, "균일 분산 (Pacing)", 12, ACC, KR, "middle", 600)

d.legend(H - 44, [
    ("Rate Halving (RHBP / PRR) · 균일 분산", ACC),
    ("Reno (전반부 침묵 후 후반부 몰아치기)", INFO)
])

d.save("16-02.rate-halving-pacing.svg")
