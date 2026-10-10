# 타입 스펙: type-line — 시간에 따른 광고 창 크기 추세 (지연 없는 정상 소비 vs 20초 지연 소비).
# 사실 출처: 원서 §15.5.4.1 실측치 — 초기 1460B, 2×MSS(2824B)씩 증가(10712, 13536, 16360, 19184), 0.678s 피크 33304B, 패킷 117 0 창, 20.043s 앱 읽기 재개, 최대 67808B.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 440
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 15-03 §2",
      "수신 애플리케이션 소비 지연에 따른 광고 창 크기 변화",
      "리눅스 수신자는 ACK 마다 창을 2×MSS 씩 키우지만, 애플리케이션이 20초간 읽기를 멈추면 버퍼가 가득 차 0 창으로 닫힌다. 20.043초에 읽기를 재개하면 창이 다시 열려 최대 67808바이트까지 확장된다.",
      "소비 지연 시 버퍼 포화로 창이 닫히고 읽기 재개 후 최대 67,808B로 복원됩니다")

X0, Y0 = 130, 330
XLEN, YLEN = 710, 200

# 좌표 축
d.line(X0, Y0, X0 + XLEN, Y0, RULE, 1.2)
d.line(X0, Y0, X0, Y0 - YLEN, RULE, 1.2)

d.t(X0 - 10, Y0 - YLEN - 12, "광고 창(바이트)", 12, MUTED, KR, "middle")
d.t(X0 + XLEN, Y0 + 36, "경과 시간(초) →", 12, MUTED, KR, "end")

# Y 축 눈금 (0, 16KB, 32KB, 48KB, 64KB, 68KB)
y_ticks = [
    (0, "0"),
    (16384, "16KB"),
    (33304, "33KB"),
    (49152, "48KB"),
    (67808, "68KB"),
]

for val, lab in y_ticks:
    y_pos = Y0 - (val / 70000.0) * YLEN
    d.line(X0 - 6, y_pos, X0, y_pos, RULE, 0.8)
    d.t(X0 - 12, y_pos + 4, lab, 11, SOFT, MONO, "end")
    if val > 0:
        d.line(X0, y_pos, X0 + XLEN, y_pos, RULE, 0.5, dash="3 5")

# X 축 눈금 (0s, 5s, 10s, 15s, 20s, 25s)
for sec in range(0, 26, 5):
    x_pos = X0 + (sec / 25.0) * XLEN
    d.line(x_pos, Y0, x_pos, Y0 + 6, RULE, 0.8)
    d.t(x_pos, Y0 + 22, f"{sec}s", 11, SOFT, MONO, "middle")

def to_xy(sec, b):
    x = X0 + (sec / 25.0) * XLEN
    y = Y0 - (b / 70000.0) * YLEN
    return x, y

# 계열 1: 정상 소비 (앱 즉시 읽기 가정 추세선)
pts_norm = [
    (0.0, 1460),
    (0.4, 16360),
    (0.8, 33304),
    (1.5, 50248),
    (2.5, 67808),
    (25.0, 67808),
]
norm_coords = [to_xy(s, b) for s, b in pts_norm]
for i in range(len(norm_coords) - 1):
    d.line(norm_coords[i][0], norm_coords[i][1], norm_coords[i+1][0], norm_coords[i+1][1], INFO, 1.8, dash="5 3")

# 계열 2: 관측값 연결(사이 시각은 근사) (버퍼 포화 후 0 창 및 20.043s 재개)
pts_delay = [
    (0.0, 1460),
    (0.3, 16360),
    (0.678, 33304),
    (1.0, 0),
    (20.043, 0),
    (20.5, 16360),
    (21.2, 33304),
    (22.2, 50248),
    (23.2, 67808),
    (25.0, 67808),
]
delay_coords = [to_xy(s, b) for s, b in pts_delay]
for i in range(len(delay_coords) - 1):
    d.line(delay_coords[i][0], delay_coords[i][1], delay_coords[i+1][0], delay_coords[i+1][1], WARN, 2.2)

# 핵심 지점 마커 및 칩
# 1. 0.678s 피크 33,304B
px, py = to_xy(0.678, 33304)
d.o.append(f'<circle cx="{px}" cy="{py}" r="4" fill="{WARN}" stroke="{PAPER}" stroke-width="2"/>')
d.line(px + 4, py + 4, px + 36, py + 36, RULE, 0.8)
d.chip(px + 120, py + 36, "0.678s · 33,304B 피크", WARN, 11)

# 2. 0 창 고착 (패킷 117 ~ 20.043s 구간 중앙: cx=370)
px1, py1 = to_xy(1.0, 0)
px2, py2 = to_xy(20.043, 0)
d.chip(370, py1 - 18, "버퍼 포화 0 창 광고 (패킷 117)", BAD, 11)

# 3. 20.043s 재개 지점 (곡선 관통 방지를 위해 왼쪽으로 지시선 인출)
d.o.append(f'<circle cx="{px2}" cy="{py2}" r="4" fill="{OK}" stroke="{PAPER}" stroke-width="2"/>')
d.line(px2 - 4, py2 - 4, px2 - 36, py2 - 24, RULE, 0.8)
d.chip(px2 - 110, py2 - 24, "20.043s 앱 읽기 시작", OK, 11)

# 4. 최대 창 67,808B 도달 지점
px_max, py_max = to_xy(23.2, 67808)
d.o.append(f'<circle cx="{px_max}" cy="{py_max}" r="4" fill="{OK}" stroke="{PAPER}" stroke-width="2"/>')
d.chip(px_max - 86, py_max - 30, "최대 창 67,808B 도달", OK, 11)

d.legend(H - 46, [("정상 소비(계산 예시)", INFO), ("관측값 연결(사이 시각은 근사)", WARN), ("읽기 재개·최대치", OK), ("0 창 중단", BAD)])
d.save("15-03.autotuning-window.svg")

