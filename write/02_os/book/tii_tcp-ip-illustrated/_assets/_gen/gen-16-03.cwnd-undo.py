# 타입 스펙: type-line — 사건 7~11의 혼잡 창(cwnd)과 임계값(ssthresh) 변화 추이.
# 사실 출처: ch16.txt 1845~2032행 — 사건 6~11의 cwnd 및 ssthresh 수치, 되돌리기(Undo), maxburst 완화.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-03",
      "사건 7~11의 혼잡 창 축소와 되돌리기 추이",
      "헛 타임아웃 감지 시 창을 즉시 복원하고 급작스러운 패킷 분출을 막기 위해 완화 규칙을 적용합니다.",
      "TSOPT 에코 증거로 두 차례 창을 되돌리고 세 번째 실제 손실에서만 느린 시작을 밟습니다")

X0, X1 = 80, 800
Y0, Y_TOP = 380, 130

def get_x(t):
    return X0 + ((t - 58.0) / (92.0 - 58.0)) * (X1 - X0)

def get_y(w):
    return Y0 - (w / 22.0) * (Y0 - Y_TOP)

# 축
d.line(X0, Y0, X1, Y0, RULE, 1.2)
d.line(X0, Y0, X0, Y_TOP - 10, RULE, 1.2)

# Y 눈금
for w in [0, 5, 10, 15, 20]:
    y = get_y(w)
    d.line(X0, y, X1, y, RULE, 0.6, dash="3 3")
    d.t(X0 - 10, y + 4, f"{w} pkts", 10, SOFT, MONO, "end")

# X 눈금
for t in [60, 65, 70, 75, 80, 85, 90]:
    x = get_x(t)
    d.line(x, Y0, x, Y0 + 5, RULE, 1.0)
    d.t(x, Y0 + 18, f"{t}s", 10, SOFT, MONO, "middle")

d.t(16, Y_TOP - 16, "창 크기 (패킷)", 11, INK, KR, "start", 600)
d.t(X1 + 14, Y0 + 4, "시간 (초)", 11, INK, KR, "start", 600)

# ssthresh 선 (WARN 점선) — 계단 함수
SSTHRESH_PTS = [
    (58.0, 10),
    (62.486, 10),
    (62.486, 5),
    (62.757, 5),
    (62.757, 10),
    (67.550, 10),
    (67.550, 5),
    (77.121, 5),
    (77.121, 9),
    (88.929, 9),
    (88.929, 5),
    (92.0, 5),
]
ssthresh_str = " ".join(("M" if i == 0 else "L") + f" {get_x(t):.1f} {get_y(w):.1f}" for i, (t, w) in enumerate(SSTHRESH_PTS))
d.path(ssthresh_str, WARN, 1.4, dash="4 4")

# cwnd 선 (ACC 실선) — CWR 감축, RTO 수직 강등, 되돌리기 수직 점프
CWND_PTS = [
    (58.0, 19),
    (59.652, 19),
    (62.486, 10),
    (62.486, 1),
    (62.757, 1),
    (62.757, 10),
    (67.550, 10),
    (67.916, 5),
    (77.121, 18),
    (78.515, 8),
    (78.515, 1),
    (80.093, 1),
    (80.093, 7),
    (88.929, 7),
    (88.929, 1),
    (89.434, 5),
    (92.0, 6.5),
]
cwnd_str = " ".join(("M" if i == 0 else "L") + f" {get_x(t):.1f} {get_y(w):.1f}" for i, (t, w) in enumerate(CWND_PTS))
d.path(cwnd_str, ACC, 2.0)

# 핵심 사건 마커 및 라벨 (그리드 선과 데이터 선을 회피한 안전 좌표)

# 1. 사건 7 되돌리기 마커 (62.757s, 10) 및 라벨 (w=12.5)
d.o.append(f'<circle cx="{get_x(62.757):.1f}" cy="{get_y(10):.1f}" r="4.5" fill="{OK}"/>')
d.t(get_x(62.757) + 10, get_y(12.5), "사건 7: 헛 RTO (10 복원)", 11, OK, KR, "start")

# 2. 사건 8 수축 마커 (67.916s, 5) 및 라벨 (w=2.5)
d.o.append(f'<circle cx="{get_x(67.916):.1f}" cy="{get_y(5):.1f}" r="4.5" fill="{BAD}"/>')
d.t(get_x(67.916), get_y(2.5), "사건 8: cwnd 5 수축", 11, MUTED, KR, "middle")

# 3. 사건 9 CWR 진입 마커 (77.121s, 18) 및 라벨 (w=21.2)
d.o.append(f'<circle cx="{get_x(77.121):.1f}" cy="{get_y(18):.1f}" r="4.5" fill="{WARN}"/>')
d.t(get_x(77.121), get_y(21.2), "사건 9: cwnd 18 CWR 진입", 11, WARN, KR, "middle")

# 4. 사건 10 완화 되돌리기 마커 (80.093s, 7) 및 라벨 (w=12.5)
d.o.append(f'<circle cx="{get_x(80.093):.1f}" cy="{get_y(7):.1f}" r="4.5" fill="{OK}"/>')
d.t(get_x(80.093) + 8, get_y(15.5), "사건 10: 완화 복원 (cwnd 7)", 11, OK, KR, "start")

# 5. 사건 11 실제 RTO 마커 (88.929s, 1) 및 라벨 (w=12.5)
d.o.append(f'<circle cx="{get_x(88.929):.1f}" cy="{get_y(1):.1f}" r="4.5" fill="{BAD}"/>')
d.t(get_x(88.929), get_y(12.5), "사건 11: 실제 RTO (느린 시작)", 11, BAD, KR, "middle")

d.t(X0, Y0 + 38, "계산 예시: 사건 10 이후 cwnd 7 유지 · 미공개: 사건 11 직전 값", 11, SOFT, KR, "start")

d.legend(H - 44, [
    ("혼잡 창 (cwnd)", ACC),
    ("임계값 (ssthresh)", WARN),
    ("되돌리기 복원", OK),
    ("손실·수축 지점", BAD),
])

d.save("16-03.cwnd-undo.svg")
