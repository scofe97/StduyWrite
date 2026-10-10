# 타입 스펙: type-line — RED 의 평균 큐 길이에 따른 패킷 버림·마킹 확률 함수 (계산 예시).
# 사실 출처: Sally Floyd & Van Jacobson (1993), ch16.txt 2945~2965행 — min_th·max_th 임계값, MaxP 최대 확률, 평균 큐 기반 조기 감지(계산 예시: min_th=20, max_th=60, MaxP=0.1, 물리 버퍼=80).
# 계산 공식: avg < min_th: p=0; min_th <= avg < max_th: p = max_p * (avg - min_th)/(max_th - min_th); avg >= max_th: p = 1.0 (전량 드롭).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-05 §2",
      "평균 큐 길이에 따른 RED 패킷 버림·마킹 확률 (계산 예시)",
      "단기 버스트로 인한 일시적 큐 증가는 버리지 않고 수용하되, 지속적 혼잡으로 평균 큐 길이가 min_th(20)를 넘으면 확률적으로 패킷을 선제 마킹·폐기합니다. max_th(60)를 넘으면 강제 폐기(1.0)로 전환하여 버퍼 완전 고갈을 차단합니다.",
      "순간 큐의 버스트는 받아들이고, 평균 큐의 지속 혼잡만 선제적으로 솎아냅니다")

PX0, PX1 = 110, 840
PY0, PY1 = 120, 420

MIN_X, MAX_X = 0, 100
def get_x(q):
    return PX0 + (q - MIN_X) / (MAX_X - MIN_X) * (PX1 - PX0)

def get_y(prob):
    return PY1 - prob * (PY1 - PY0)

# Y축 눈금 및 격자선 (0%, 10%, 25%, 50%, 75%, 100%)
Y_TICKS = [(0.0, "0%"), (0.1, "10% (MaxP)"), (0.25, "25%"), (0.5, "50%"), (0.75, "75%"), (1.0, "100%")]
for p_val, p_lab in Y_TICKS:
    y_pos = get_y(p_val)
    d.line(PX0, y_pos, PX1, y_pos, RULE, 0.6)
    d.t(PX0 - 12, y_pos + 4, p_lab, 11, SOFT, MONO if "%" in p_lab else KR, "end")
d.t(PX0 - 12, PY0 - 10, "버림·마킹 확률", 11, MUTED, KR, "end")

# X축 눈금 및 수직 안내선
X_TICKS = [(0, "0"), (20, "20 (min_th)"), (40, "40"), (60, "60 (max_th)"), (80, "80 (물리 버퍼)"), (100, "100")]
for q_val, q_lab in X_TICKS:
    x_pos = get_x(q_val)
    d.line(x_pos, PY1, x_pos, PY1 + 6, RULE, 0.8)
    d.t(x_pos, PY1 + 20, q_lab, 11, SOFT, KR if "(" in q_lab else MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "평균 큐 길이 avg (패킷 수, 계산 예시)", 12, MUTED, KR, "middle")

# 임계값 세로 가이드선
x_min = get_x(20)
x_max = get_x(60)
x_buf = get_x(80)

d.line(x_min, PY0, x_min, PY1, OK, 0.9, "4 4")
d.line(x_max, PY0, x_max, PY1, WARN, 0.9, "4 4")
d.line(x_buf, PY0, x_buf, PY1, BAD, 0.9, "4 4")

# 계열 1: RED 조기 감지 확률 곡선 (초점)
# avg 0~20: 0%
# avg 20~60: 0% -> 10% 선형 증가
# avg 60~100: 100% 수직 상승 (강제 폐기)
pts_red = [
    (get_x(0), get_y(0.0)),
    (get_x(20), get_y(0.0)),
    (get_x(60), get_y(0.1)),
    (get_x(60), get_y(1.0)),
    (get_x(100), get_y(1.0))
]
pts_red_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_red)
d.o.append(f'<polyline points="{pts_red_str}" fill="none" stroke="{ACC}" stroke-width="2.4" stroke-linejoin="round"/>')
for px, py in pts_red:
    d.o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4" fill="{PAPER}" stroke="{ACC}" stroke-width="1.4"/>')

# 계열 2: 전통적 테일 드롭 (비교군: 80패킷 버퍼 고갈 시 100% 드롭)
pts_td = [
    (get_x(0), get_y(0.0)),
    (get_x(80), get_y(0.0)),
    (get_x(80), get_y(1.0)),
    (get_x(100), get_y(1.0))
]
pts_td_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts_td)
d.o.append(f'<polyline points="{pts_td_str}" fill="none" stroke="{BAD}" stroke-width="1.6" stroke-dasharray="5 4" stroke-linejoin="round"/>')
d.o.append(f'<circle cx="{get_x(80):.1f}" cy="{get_y(1.0):.1f}" r="3.5" fill="{PAPER}" stroke="{BAD}" stroke-width="1.2"/>')

# 구간 주석 레이블 (선 관통 방지 배치)
d.t(get_x(10), get_y(0.02) - 10, "무손실 버스트 수용", 11, OK, KR, "middle", 600)
d.t(get_x(40), 368, "선제 마킹·버림 (0 → MaxP)", 11, ACC, KR, "middle", 600)
d.t(get_x(75), get_y(1.0) - 12, "강제 폐기 구간 (100%)", 11, WARN, KR, "middle", 600)
d.t(get_x(80) + 10, 368, "테일 드롭 한계선 (80)", 11, BAD, KR, "start")

d.legend(H - 48, [
    ("RED 선제 확률", ACC),
    ("테일 드롭", BAD),
    ("최소 임계 min_th", OK),
    ("최대 임계 max_th", WARN),
])

d.save("16-05.red-drop-probability.svg")
