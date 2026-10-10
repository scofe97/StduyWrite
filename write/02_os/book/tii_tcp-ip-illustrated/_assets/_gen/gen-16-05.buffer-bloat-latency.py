# 타입 스펙: type-line — 버퍼 크기별 최대 큐 지연과 링크 속도별 계열 (지연 = 버퍼 / 대역폭 계산 예시, 로그-로그 축).
# 사실 출처: ch16.txt 2868~2896행 — 업로드 대역폭 256Kb/s~10Mb/s, 버퍼 크기 16KB~2MB, 초 단위 지연, ITU-T G.114 150ms 대화형 한계.
# 계산 공식: 지연(초) = (버퍼 크기 바이트 * 8) / (대역폭 bps).
import math
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 540
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 16-05 §1",
      "버퍼 크기와 링크 속도별 큐 지연 추세 (계산 예시)",
      "버퍼 용량이 커질수록 패킷 손실은 줄어들지만 대기열이 가득 차면 큐잉 지연이 초 단위로 누적됩니다. 특히 저속 업로드 링크에서 수백 킬로바이트 버퍼는 대화형 트래픽 허용 기준선인 150ms 를 크게 초과합니다.",
      "대용량 버퍼는 손실을 막는 대신 초 단위 큐 지연을 일으킵니다")

PX0, PX1 = 110, 840
PY0, PY1 = 120, 420

# X축: 4KB ~ 2048KB (log2 기준: 2 ~ 11)
MIN_LOG_X, MAX_LOG_X = 2.0, 11.0
def get_x(kb):
    lx = math.log2(kb)
    return PX0 + (lx - MIN_LOG_X) / (MAX_LOG_X - MIN_LOG_X) * (PX1 - PX0)

# Y축: 0.001초(1ms) ~ 100초 (log10 기준: -3.0 ~ 2.0, 클램프 없이 전 구간 직선 유지)
MIN_LOG_Y, MAX_LOG_Y = -3.0, 2.0
def get_y(sec):
    ly = math.log10(sec)
    return PY1 - (ly - MIN_LOG_Y) / (MAX_LOG_Y - MIN_LOG_Y) * (PY1 - PY0)

# Y축 격자선 (1ms, 10ms, 100ms, 1초, 10초, 100초)
Y_TICKS = [(0.001, "1ms"), (0.01, "10ms"), (0.1, "100ms"), (1.0, "1초"), (10.0, "10초"), (100.0, "100초")]
for s_val, s_lab in Y_TICKS:
    y_pos = get_y(s_val)
    d.line(PX0, y_pos, PX1, y_pos, RULE, 0.6)
    d.t(PX0 - 12, y_pos + 4, s_lab, 11, SOFT, KR if "초" in s_lab else MONO, "end")
d.t(PX0 - 12, PY0 - 10, "최대 큐 지연", 11, MUTED, KR, "end")

# X축 눈금 (4KB, 16KB, 64KB, 256KB, 1MB, 2MB)
X_TICKS = [(4, "4 KB"), (16, "16 KB"), (64, "64 KB"), (256, "256 KB"), (1024, "1 MB"), (2048, "2 MB")]
for kb_val, kb_lab in X_TICKS:
    x_pos = get_x(kb_val)
    d.line(x_pos, PY1, x_pos, PY1 + 6, RULE, 0.8)
    d.t(x_pos, PY1 + 20, kb_lab, 11, SOFT, MONO, "middle")
d.t((PX0 + PX1) / 2, PY1 + 42, "버퍼 크기 (로그 스케일)", 12, MUTED, KR, "middle")

# 150ms 대화형 서비스 품질 한계 기준선 (ITU-T G.114)
Y_150MS = get_y(0.15)
d.line(PX0, Y_150MS, PX1, Y_150MS, WARN, 1.2, "5 4")
d.t(PX1 - 12, Y_150MS - 8, "대화형 지연 한계 150ms (ITU-T G.114)", 11, WARN, KR, "end", 600)

# 링크 속도별 계열 데이터
KB_POINTS = [4, 16, 64, 256, 1024, 2048]
SERIES = [
    ("256 Kbps (DSL 하한)", 256, BAD, 2.0, None),
    ("1 Mbps (업로드 보급)", 1000, ACC, 2.4, None),
    ("4 Mbps (케이블 상위)", 4000, WARN, 1.8, "4 3"),
    ("10 Mbps (고속 업로드)", 10000, OK, 1.8, "5 4"),
]

for name, bw_kbps, col, sw, dash in SERIES:
    pts = []
    for kb in KB_POINTS:
        sec = (kb * 8.0) / bw_kbps
        pts.append((get_x(kb), get_y(sec)))
    
    pts_str = " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)
    d_attr = f' stroke-dasharray="{dash}"' if dash else ""
    d.o.append(f'<polyline points="{pts_str}" fill="none" stroke="{col}" stroke-width="{sw}"{d_attr} stroke-linejoin="round"/>')
    for px, py in pts:
        d.o.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{PAPER}" stroke="{col}" stroke-width="1.2"/>')

# 주요 지점 주석 (점 바로 옆 배치 및 선 관통 회피)
x_256k = get_x(256)
y_256_256k = get_y((256 * 8.0) / 256)
d.t(x_256k, y_256_256k - 18, "256KB @ 256Kbps → 8초", 11, BAD, KR, "middle", 600)

y_256_1m = get_y((256 * 8.0) / 1000)
d.t(x_256k + 8, y_256_1m - 24, "256KB: 2.05초", 11, ACC, KR, "start", 600)

x_16k = get_x(16)
y_16_1m = get_y((16 * 8.0) / 1000)
d.t(x_16k + 14, y_16_1m + 19, "128ms", 11, ACC, KR, "start", 600)

d.legend(H - 48, [
    ("256 Kbps 링크", BAD),
    ("1 Mbps 링크 (초점)", ACC),
    ("4 Mbps 링크", WARN),
    ("10 Mbps 링크", OK),
])

d.save("16-05.buffer-bloat-latency.svg")
