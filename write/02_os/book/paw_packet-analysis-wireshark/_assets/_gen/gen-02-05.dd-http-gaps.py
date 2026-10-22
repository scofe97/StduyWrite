# 02-05 §5 — -t dd 는 바로 앞에 표시된 패킷과의 간격을 찍는다. HTTP 만 남기면 5→6 과 13→14 는 요청→응답이라 응답 시간이고, 6→13 은 다른 연결 사이라 응답 시간이 아니다.
# 타입 스펙: type-gantt — 막대 길이가 곧 구간. 표시된 HTTP 프레임 사이 간격을 시간축 위 막대로 그린다. focal 은 2초 가까이 걸린 13→14.
# 사실 출처: 노트 L284~L306 (-t dd 출력 L291~L294, 시각 L246~L253, http.time L304~L305)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

def q(v): return int(round(v / 4)) * 4

TX, PITCH = 200, 360          # 시간축 시작 x, 1초당 px
Y_AX, Y0, ROW_H = 120, 148, 64
# (구간, 프레임 내용, 시작초, 끝초, dd 값, 판정, 색)
ROWS = [
    ("#5 → #6", "GET → 200 OK", 0.110, 0.180, "0.070000", "응답 시간", OK),
    ("#6 → #13", "200 OK → GET /slow", 0.180, 0.510, "0.330000", "응답 시간 아님", WARN),
    ("#13 → #14", "GET /slow → 200 OK", 0.510, 2.010, "1.500000", "응답 시간", ACC),
]
W = 1000
H = Y0 + len(ROWS) * ROW_H + 96
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-05 §5",
      "-t dd 가 찍는 HTTP 간격",
      "HTTP 만 남긴 줄 사이의 간격이다. 요청 바로 뒤 응답일 때만 응답 시간이고 다른 연결의 응답이 끼면 틀어진다.",
      "막대 하나가 표시된 두 줄 사이의 dd 값입니다")

d.t(24, Y_AX, "Time 열 (초)", 11, SOFT, KR, "start", 600)
for t in (0, 0.5, 1.0, 1.5, 2.0):
    x = TX + t * PITCH
    d.t(x, Y_AX, f"{t:g}", 11, SOFT, MONO)
    d.line(x, Y_AX + 12, x, Y0 + len(ROWS) * ROW_H - 4, RULE, 0.8, "3 6")
d.line(24, Y_AX + 12, W - 24, Y_AX + 12, RULE, 0.8)

for i, (span, what, t0, t1, dd, verdict, c) in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.t(24, y + 22, span, 13, INK, MONO, "start", 600)
    d.t(24, y + 40, what, 11, MUTED, MONO, "start")
    x, w = q(TX + t0 * PITCH), q((t1 - t0) * PITCH)
    focal = c == ACC
    if focal:
        d.o.append(f'<rect x="{x}" y="{y + 8}" width="{w}" height="24" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(x + 12, y + 25, f"{dd} · {verdict}", 12, ACC, KR, "start", 600)
    else:
        d.tone(x, y + 8, w, 24, c, 4)
        d.t(x + w + 12, y + 25, f"{dd} · {verdict}", 12, c, KR, "start", 600)
    d.t(x, y + 52, f"{t0:.3f} → {t1:.3f}", 11, MUTED, MONO, "start")

d.legend(H - 72, [("응답 시간", OK), ("느린 응답", ACC), ("응답 시간 아님", WARN)])
d.save("02-05.dd-http-gaps.svg")
