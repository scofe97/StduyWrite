# 사실 출처: go1.25.1 src/net/dial.go:269,571,585,624,659, go doc net.Dialer.DialContext, RFC 6555
# 타입 스펙: type-gantt
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 960, 480

d = D(W, H,
      "DIALER TIMEOUT SPREAD AND FAST FALLBACK",
      "주소 순차 분할과 IPv6/IPv4 Fast Fallback",
      "IPv6·IPv4 각 2주소에 1분 예산: 레이서마다 첫 주소에 30초 배정, 300ms 지연 후 IPv4 병렬 경합, 승자 확정 시 IPv6 레이서 취소",
      "레이서마다 자기 계열 2주소로 1분을 나눠 첫 주소에 30초, 300ms 뒤 IPv4 가 출발해 먼저 연결을 맺습니다")

# 사실 출처: go1.25.1 src/net/dial.go:572 partition, :602-606 레이서별 dialSerial,
#   :620 defer primaryCancel, :623 fallbackTimer, :671 partialDeadline(len(ras)-i)
# 축: 0~1.5s 를 확대(320px/s)하고, 끊김 표시 뒤 1.5~30s 를 압축한다.
#   경합은 1.2s 안에 끝나므로 선형 30s 축이면 0.3s·1.2s 가 눈금과 겹친다.
LX = 28
TX = 230
ZOOM_END, ZW = 1.5, 480          # 0~1.5s → 230~710
BRK = 30                          # 끊김 폭 710~740
CW, TMAX = 170, 30.0              # 1.5~30s → 740~910
AXIS_Y = 118

def X(sec):
    if sec <= ZOOM_END:
        return TX + sec / ZOOM_END * ZW
    return TX + ZW + BRK + (sec - ZOOM_END) / (TMAX - ZOOM_END) * CW

# 시간축 — 눈금은 축 아래 짧은 틱만 둔다(행 글자를 가로지르지 않게)
d.line(TX, AXIS_Y, X(ZOOM_END), AXIS_Y, RULE, 1.0)
d.line(X(ZOOM_END) + BRK, AXIS_Y, X(TMAX), AXIS_Y, RULE, 1.0)
for bx in (X(ZOOM_END) + 11, X(ZOOM_END) + 19):
    d.line(bx - 3, AXIS_Y + 5, bx + 3, AXIS_Y - 5, SOFT, 1.0)
for tick in (0.0, 0.3, 0.6, 0.9, 1.2, 1.5, 15.0, 30.0):
    x = X(tick)
    c = INFO if tick == 0.3 else (ACC if tick == 1.2 else SOFT)
    d.line(x, AXIS_Y - 4, x, AXIS_Y + 4, c, 1.0)
    d.t(x, AXIS_Y - 10, f"{tick:g}s", 10, c, fam=MONO)

# 국면 1: IPv6 (Primaries)
P1_TOP = 136
ROWH = 38
d.box(LX, P1_TOP, W - LX - 24, 104, fill="rgba(245,245,245,0.02)", stroke=RULE, sw=0.8, r=6)
d.t(LX + 12, P1_TOP + 18, "IPv6 주소군 (Primaries · 즉시 출발)", 11, SOFT, fam=KR, anchor="start")

# Row 0: IPv6 #1 — 0~1.2s 시도, 1.2s 에 primaryCancel 로 취소. 배정 30s 의 나머지는 쓰이지 않는다
y0 = P1_TOP + 28
d.t(LX + 16, y0 + 17, "2001:db8::1", 11, INK, fam=MONO, anchor="start", weight=600)
d.box(X(0.0), y0 + 2, X(1.2) - X(0.0), 22, fill="rgba(240,97,109,0.12)", stroke=BAD, sw=1.0, r=4)
d.t(X(0.3) + 8, y0 + 17, "연결 지연 (응답 없음)", 11, BAD, fam=KR, anchor="start")
d.o.append(f'<rect x="{X(1.2)}" y="{y0 + 2}" width="{X(30.0) - X(1.2)}" height="22" rx="4" fill="none" stroke="{MUTED}" stroke-width="0.9" stroke-dasharray="3 3"/>')
d.t(X(1.2) + 8, y0 + 17, "배정 30s 중 남은 몫 · 취소로 폐기", 11, MUTED, fam=KR, anchor="start")

# Row 1: IPv6 #2 — 레이서가 취소되어 기동하지 않는다
y1 = y0 + ROWH
d.t(LX + 16, y1 + 17, "2001:db8::2", 11, MUTED, fam=MONO, anchor="start")
d.t(X(0.3) + 8, y1 + 17, "미실행 (IPv6 레이서 취소)", 11, MUTED, fam=KR, anchor="start")

# 국면 2: IPv4 (Fallbacks)
P2_TOP = 256
d.box(LX, P2_TOP, W - LX - 24, 104, fill="rgba(245,245,245,0.02)", stroke=RULE, sw=0.8, r=6)
d.t(LX + 12, P2_TOP + 18, "IPv4 주소군 (Fallbacks · 300ms 뒤 출발)", 11, INFO, fam=KR, anchor="start")

# Row 2: IPv4 #1 — 0~0.3s FallbackDelay 대기, 0.3~1.2s 연결 성공 (focal)
y2 = P2_TOP + 28
d.t(LX + 16, y2 + 17, "198.51.100.1", 11, ACC, fam=MONO, anchor="start", weight=600)
d.o.append(f'<rect x="{X(0.0)}" y="{y2 + 2}" width="{X(0.3) - X(0.0)}" height="22" rx="4" fill="rgba(106,149,216,0.12)" stroke="{INFO}" stroke-width="0.9" stroke-dasharray="2 2"/>')
d.t((X(0.0) + X(0.3)) / 2, y2 + 17, "300ms 대기", 11, INFO, fam=KR)
d.box(X(0.3), y2 + 2, X(1.2) - X(0.3), 22, fill=f"{ACC}22", stroke=ACC, sw=1.3, r=4)
d.t(X(1.2) + 8, y2 + 17, "0.9s 소요 · 연결 성공 (focal)", 11, ACC, fam=KR, anchor="start", weight=600)

# Row 3: IPv4 #2
y3 = y2 + ROWH
d.t(LX + 16, y3 + 17, "198.51.100.2", 11, MUTED, fam=MONO, anchor="start")
d.t(X(0.3) + 8, y3 + 17, "미실행 (선행 연결 성공으로 경합 종료)", 11, MUTED, fam=KR, anchor="start")

# 1.2s 승자 확정 — 이 순간 dialParallel 이 반환하며 primaryCancel 이 IPv6 레이서를 취소한다
x_succ = X(1.2)
d.line(x_succ, y2 + 24, x_succ, 376, ACC, 1.2, "3 2")
d.chip(x_succ, 388, "승자 확정 · IPv6 레이서 취소", ACC, size=11)

# 범례
d.legend(425, [
    ("FallbackDelay 대기", INFO),
    ("IPv6 시도 → 취소", BAD),
    ("미사용 배정 · 미실행", MUTED),
    ("선행 연결 성공 (focal)", ACC)
])

out_name = "02-01.dial-fallback-gantt.svg"
out_path = os.path.join(os.path.dirname(__file__), "..", out_name)
d.save(out_path if os.path.exists(os.path.dirname(out_path)) else out_name)
