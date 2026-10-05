# 14-01 §1 — 원서 Figure 14-1 을 대신한다. 서버를 격리한 뒤 18바이트 HTTP 요청이 ACK 없이 재전송되는 시각.
# 사실 출처: 원서 §14.2 본문과 Figure 14-1 캡션 — 첫 전송(세그먼트 4) 42.748s, 재전송 42.954 · 43.374 · 44.215 · 45.895 · 49.255s,
#   간격 0.206 · 0.420 · 0.841 · 1.680 · 3.360s. 연결 종료까지 약 15.5분(그림 밖).
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 시간축 + 행마다 막대, 막대 길이 = 기다린 구간.
#           행은 "몇 번째 재전송을 기다린 구간" 다섯. 시간축은 실제 초 단위로 정직하게 둔다(눈금 1초).
#           focal 은 가장 긴 마지막 대기 3.36s — 두 배씩 늘어난 결과가 쌓인 자리.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, WARN, INFO, PAPER2, RULE, KR, MONO

SENDS = [42.748, 42.954, 43.374, 44.215, 45.895, 49.255]
GAPS = ["206ms", "420ms", "841ms", "1.68s", "3.36s"]

W, H = 920, 452
LX, TX0, TX1 = 20, 232, 872
T0, T1 = 42.6, 49.4
ROW_H, BAR_H = 48, 24
def tx(t): return TX0 + (t - T0) * (TX1 - TX0) / (T1 - T0)

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-01 §1",
      "ACK 없이 같은 요청을 다시 보내는 간격",
      "서버를 격리한 뒤 클라이언트가 18바이트 요청을 42.748초에 처음 보냈다. ACK 가 오지 않자 206ms 뒤 재전송했고, 그 뒤 간격은 420ms · 841ms · 1.68초 · 3.36초로 매번 거의 두 배가 됐다. "
      "막대 하나가 직전 전송에서 다음 재전송까지 기다린 구간이고, 가로축은 캡처 시각(초)이다.",
      "같은 세그먼트를 다시 보낼 때마다 기다림이 두 배로 늘어납니다")

# 시간축 — 1초 눈금
Y_AX = 108
for s in range(43, 50):
    x = tx(s)
    d.t(x, Y_AX, f"{s}s", 11, SOFT, MONO)
    d.line(x, Y_AX + 8, x, 128 + 5 * ROW_H, RULE, 0.6, "2 4")
xf = tx(SENDS[0])

Y0 = 128
for i in range(5):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 25, f"재전송 {i + 1}", 13, INK, KR, "start", 600)
    d.t(LX + 76, y + 25, f"{SENDS[i + 1]:.3f}s", 12, MUTED, MONO, "start")
    x0, x1 = tx(SENDS[i]), tx(SENDS[i + 1])
    by = y + 8
    if i == 4:
        d.o.append(f'<rect x="{x0:.1f}" y="{by}" width="{x1 - x0:.1f}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    else:
        d.tone(x0, by, x1 - x0, BAR_H, WARN, 4, "14", 1.0)
        c = WARN
    if i == 4: d.t(x0 - 8, by + 17, GAPS[i], 12, c, MONO, "end", 600)   # 마지막 막대는 오른쪽 여백이 없어 왼쪽에 단다
    else: d.t(x1 + 8, by + 17, GAPS[i], 12, c, MONO, "start", 600)

# 첫 전송 시각 — 행 위에 겹쳐 그린다
d.line(xf, Y_AX + 8, xf, Y0 + 5 * ROW_H, INFO, 1.0)

d.t(xf + 6, Y0 + 5 * ROW_H + 12, "첫 전송 42.748s", 12, INFO, KR, "start", 600)

d.legend(H - 56, [("가장 긴 대기", ACC), ("재전송 전 대기", WARN), ("첫 전송", INFO)])
d.save("14-01.rto-backoff.svg")
