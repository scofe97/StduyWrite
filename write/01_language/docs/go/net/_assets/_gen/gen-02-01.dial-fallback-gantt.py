# 사실 출처: go1.25.1 src/net/dial.go:269,571,585,624,659, go doc net.Dialer.DialContext, RFC 6555
# 타입 스펙: type-gantt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "DIALER TIMEOUT SPREAD AND FAST FALLBACK",
      "주소 순차 분할과 IPv6/IPv4 Fast Fallback",
      "주소 4개의 15초 순차 타임아웃 분배와 300ms 지연 후 IPv4 병렬 경합",
      "총 1분 예산에서 주소당 15초를 배분하며 300ms 뒤 IPv4 가 출발해 먼저 연결을 맺습니다")

# 축 정의: 0s ~ 30s (0~3초 구간 강조 및 15초 눈금)
LX = 28
TX, TW = 230, 680
TMAX = 30.0
AXIS_Y = 118
ROWH = 38

def X(sec):
    return TX + (sec / TMAX) * TW

# 시간축 눈금 (0s, 0.3s, 5s, 10s, 15s, 20s, 25s, 30s)
ticks = [0.0, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0]
for tick in ticks:
    x = X(tick)
    d.line(x, AXIS_Y - 6, x, 400, RULE, 0.7, "2 4")
    d.t(x, AXIS_Y - 12, f"{tick:g}s", 9, SOFT, fam=MONO)

# 300ms (0.3s) 전용 보조 눈금선
x_300 = X(0.3)
d.line(x_300, AXIS_Y - 6, x_300, 400, INFO, 0.9, "3 3")
d.t(x_300, AXIS_Y - 12, "0.3s", 9, INFO, fam=MONO)

d.line(TX, AXIS_Y, TX + TW, AXIS_Y, RULE, 1.0)

# 국면 1: IPv6 (Primaries)
P1_TOP = 136
d.box(LX, P1_TOP, W - LX - 24, 104, fill="rgba(245,245,245,0.02)", stroke=RULE, sw=0.8, r=6)
d.t(LX + 12, P1_TOP + 18, "IPv6 주소군 (Primaries · 1차 시도)", 10, SOFT, fam=MONO, anchor="start")

# Row 0: IPv6 #1 (0s ~ 15s) 타임아웃
y0 = P1_TOP + 28
d.t(LX + 16, y0 + 17, "2001:db8::1", 11, INK, fam=MONO, anchor="start", weight=600)
w0 = X(15.0) - X(0.0)
d.box(X(0.0), y0 + 2, w0, 22, fill="rgba(240,97,109,0.12)", stroke=BAD, sw=1.0, r=4)
d.t(X(0.0) + 8, y0 + 17, "15s 할당 (연결 지연)", 10, BAD, fam=KR, anchor="start")

# Row 1: IPv6 #2 (15s ~ 30s)
y1 = y0 + ROWH
d.t(LX + 16, y1 + 17, "2001:db8::2", 11, MUTED, fam=MONO, anchor="start")
w1 = X(30.0) - X(15.0)
d.o.append(f'<rect x="{X(15.0)}" y="{y1 + 2}" width="{w1}" height="22" rx="4" fill="rgba(139,152,169,0.08)" stroke="{MUTED}" stroke-width="0.9" stroke-dasharray="3 3"/>')
d.t(X(15.0) + 8, y1 + 17, "대기 (이전 주소 만료 시 기동)", 10, MUTED, fam=KR, anchor="start")

# 국면 2: IPv4 (Fallbacks)
P2_TOP = 256
d.box(LX, P2_TOP, W - LX - 24, 104, fill="rgba(245,245,245,0.02)", stroke=RULE, sw=0.8, r=6)
d.t(LX + 12, P2_TOP + 18, "IPv4 주소군 (Fallbacks · 300ms 지연 기동)", 10, INFO, fam=MONO, anchor="start")

# Row 2: IPv4 #1 (0.3s ~ 1.2s) - FOCAL SUCCESS
y2 = P2_TOP + 28
d.t(LX + 16, y2 + 17, "198.51.100.1", 11, ACC, fam=MONO, anchor="start", weight=600)
# 0~0.3s 대기 갭
w_wait = X(0.3) - X(0.0)
d.o.append(f'<rect x="{X(0.0)}" y="{y2 + 2}" width="{w_wait}" height="22" rx="4" fill="rgba(106,149,216,0.12)" stroke="{INFO}" stroke-width="0.9" stroke-dasharray="2 2"/>')
d.t(X(0.0) + 4, y2 + 17, "지연", 9, INFO, fam=KR, anchor="start")

# 0.3s ~ 1.2s 연결 성공
w2 = X(1.2) - X(0.3)
d.box(X(0.3), y2 + 2, w2, 22, fill=f"{ACC}22", stroke=ACC, sw=1.3, r=4)
d.t(X(1.2) + 8, y2 + 17, "0.9s 소요 · 연결 성공 (focal)", 10, ACC, fam=KR, anchor="start", weight=600)

# Row 3: IPv4 #2
y3 = y2 + ROWH
d.t(LX + 16, y3 + 17, "198.51.100.2", 11, MUTED, fam=MONO, anchor="start")
d.t(X(0.3), y3 + 17, "미실행 (선행 연결 성공으로 전체 종료)", 10, MUTED, fam=KR, anchor="start")

# 마커 및 안내선: 300ms FallbackDelay 발동 시점
d.line(x_300, y0 + 26, x_300, y2 + 2, INFO, 1.2, "3 2")
d.chip(x_300 + 48, y1 + 14, "FallbackDelay 300ms", INFO, size=10)

# 마커: 1.2s 연결 성공 시점 -> 나머지 고루틴 및 타임아웃 정리
x_succ = X(1.2)
d.line(x_succ, y2 + 24, x_succ, 395, ACC, 1.2, "3 2")
d.chip(x_succ + 52, 385, "승자 확정 · 경합 종료", ACC, size=10)

# 범례
d.legend(425, [
    ("FallbackDelay 대기", INFO),
    ("15초 분할 시도", BAD),
    ("대기 / 미실행", MUTED),
    ("선행 연결 성공 (focal)", ACC)
])

d.save("write/01_language/docs/go/net/_assets/02-01.dial-fallback-gantt.svg")
