# 타입 스펙: type-line — 패킷 손실률(p)에 따른 혼잡 창 크기(w) 응답 함수 비교 (로그-로그 계산 예시).
# 사실 출처: ch16.txt 2140~2250행, RFC 3649 — 표준 TCP(w=1.22/√p)와 HSTCP(w=0.12/p^0.835, S=-0.835) 응답 곡선.
import sys; sys.path.insert(0, ".")
import math
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 520
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-04 §3",
      "표준 TCP 와 HighSpeed TCP 응답 곡선 비교 (계산 예시)",
      "손실률 p가 낮아질수록 표준 TCP(w=1.22/√p)는 창 크기가 완만하게 증가하지만, HSTCP는 p ≤ 10⁻³ 구간에서 기울기 S=-0.835의 가파른 곡선으로 창을 대폭 키워 고속 대역폭을 채운다.",
      "손실률 10⁻³ 이하에서 응답 함수가 갈라져 고속 대역폭을 확보합니다")

PX0, PX1 = 100, 840
PY0, PY1 = 120, 420

# 로그 축 범위: log10(p) = -7 ~ -1 (X), log10(w) = 0 ~ 5 (Y)
MIN_LOG_P, MAX_LOG_P = -7.0, -1.0
MIN_LOG_W, MAX_LOG_W = 0.0, 5.0

def x_from_log_p(lp):
    return PX0 + (lp - MIN_LOG_P) * (PX1 - PX0) / (MAX_LOG_P - MIN_LOG_P)

def y_from_log_w(lw):
    return PY1 - (lw - MIN_LOG_W) * (PY1 - PY0) / (MAX_LOG_W - MIN_LOG_W)

# Y축 격자선 (log10 w = 0, 1, 2, 3, 4, 5)
w_labels = [(0, "1"), (1, "10"), (2, "10² (100)"), (3, "10³ (1,000)"), (4, "10⁴ (10,000)"), (5, "10⁵ (100,000)")]
for exp_val, txt in w_labels:
    y_pos = y_from_log_w(exp_val)
    d.line(PX0, y_pos, PX1, y_pos, RULE, 0.6)
    d.t(PX0 - 12, y_pos + 4, txt, 11, SOFT, MONO, "end")
d.t(PX0, PY0 - 24, "창 크기 w (패킷)", 11, MUTED, KR, "start")

# X축 레이블 (log10 p = -7, -6, -5, -4, -3, -2, -1)
p_labels = [(-7, "10⁻⁷"), (-6, "10⁻⁶"), (-5, "10⁻⁵"), (-4, "10⁻⁴"), (-3, "10⁻³"), (-2, "10⁻²"), (-1, "10⁻¹")]
for exp_val, txt in p_labels:
    x_pos = x_from_log_p(exp_val)
    d.line(x_pos, PY1, x_pos, PY1 + 6, RULE, 0.8)
    d.t(x_pos, PY1 + 20, txt, 11, SOFT, MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "패킷 손실률 p (로그 축)", 12, MUTED, KR, "middle")

# 전환 임계선 p = 10^-3 (세로 점선)
x_trans = x_from_log_p(-3.0)
d.line(x_trans, PY0, x_trans, PY1, WARN, 1.0, "4 4")
d.t(x_trans, PY0 - 8, "전환 지점 (P₀ = 10⁻³, W₀ ≈ 38)", 11, WARN, KR, "middle", 600)

# 계열 1: 표준 TCP 응답 곡선 w = 1.22 / sqrt(p)
# log10(w) = log10(1.22) - 0.5 * log10(p) ≈ 0.0864 - 0.5 * lp
std_pts = []
for i in range(61):
    lp = MIN_LOG_P + i * (MAX_LOG_P - MIN_LOG_P) / 60.0
    lw = 0.0864 - 0.5 * lp
    std_pts.append((x_from_log_p(lp), y_from_log_w(lw)))
poly_std = " ".join(f"{x:.1f},{y:.1f}" for x, y in std_pts)
d.o.append(f'<polyline points="{poly_std}" fill="none" stroke="{INFO}" stroke-width="2.0" stroke-linejoin="round"/>')

# 계열 2: HighSpeed TCP 응답 곡선 (RFC 3649: S = -0.835)
# lp >= -3: 표준과 동일
# lp < -3: log10(w) = log10(38) + (-0.83482) * (lp - (-3)) ≈ 1.5798 - 0.83482 * (lp + 3)
# at lp = -7: lw = 1.5798 + 3.3393 = 4.9191 (w ≈ 83,000)
hstcp_pts = []
for i in range(61):
    lp = MIN_LOG_P + i * (MAX_LOG_P - MIN_LOG_P) / 60.0
    if lp >= -3.0:
        lw = 0.0864 - 0.5 * lp
    else:
        lw = 1.5798 - 0.83482 * (lp + 3.0)
    hstcp_pts.append((x_from_log_p(lp), y_from_log_w(lw)))
poly_hstcp = " ".join(f"{x:.1f},{y:.1f}" for x, y in hstcp_pts)
d.o.append(f'<polyline points="{poly_hstcp}" fill="none" stroke="{ACC}" stroke-width="2.4" stroke-linejoin="round"/>')

# 주요 수치 지점 점 표기
# 표준: p=10^-7 -> w=3,873 (lw=3.588)
d.o.append(f'<circle cx="{x_from_log_p(-7.0):.1f}" cy="{y_from_log_w(3.588):.1f}" r="4" fill="{INFO}"/>')
d.t(x_from_log_p(-7.0) + 14, y_from_log_w(3.588) - 10, "표준 TCP (w ≈ 3,873)", 11, INFO, KR, "start")

# HSTCP: p=10^-7 -> w≈83,000 (lw=4.919)
d.o.append(f'<circle cx="{x_from_log_p(-7.0):.1f}" cy="{y_from_log_w(4.919):.1f}" r="4" fill="{ACC}"/>')
d.t(x_from_log_p(-7.0) + 14, PY0 - 10, "HSTCP (w ≈ 83,000)", 11, ACC, KR, "start", 600)

# 합류 지점 p=10^-3, w=38
d.o.append(f'<circle cx="{x_trans:.1f}" cy="{y_from_log_w(1.58):.1f}" r="4" fill="{WARN}"/>')
d.t(x_trans - 14, y_from_log_w(1.58) + 16, "합류 지점 (w = 38)", 11, WARN, KR, "end")

# 공통 구간 설명 (곡선 위 빈 영역에 배치해 겹침 방지)
d.t(x_from_log_p(-1.8), y_from_log_w(1.6), "동일 AIMD 동작 구간", 11, MUTED, KR, "middle")

d.legend(H - 44, [
    ("HSTCP (S = -0.835)", ACC),
    ("표준 Reno (S = -0.5)", INFO),
    ("전환 임계 (p = 10⁻³)", WARN),
])

d.save("16-04.hstcp-response-curve.svg")
