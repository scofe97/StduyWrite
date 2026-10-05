# 12-01 §7 — 원문 12.3 의 예: 1–1024 를 받았고 다음 세그먼트가 2049–3072 를 싣고 왔다면,
#   수신자는 보통의 ACK 번호 칸으로는 이 새 세그먼트를 받았다고 알릴 수 없다. ACK 번호는 순서대로 받은 가장 큰 바이트 + 1.
#   현대 TCP 의 SACK 옵션은 순서 밖으로 제대로 받은 데이터를 송신자에게 알린다.
#   원문 12.2.2: 바이트 스트림이라 수신 TCP 는 빠진 낮은 번호(구멍)가 채워질 때까지 큰 번호 데이터를 애플리케이션에 주지 않고 쥐고 있다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대, 막대 길이 = 구간.
#           축약: 가로 축이 시간이 아니라 바이트 번호(1–3072)다. 행은 "누가 이 구간을 무엇이라 말하는가" 넷이다.
#           byte-stream 도식과 같은 축 문법을 쓴다. focal 은 ACK 칸이 말하지 못하는 구간을 대신 말하는 SACK 막대.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 464
LX, TX0, TX1 = 20, 232, 872
ROW_H, BAR_H = 56, 28
TOTAL = 3072
PITCH = (TX1 - TX0) / TOTAL
def bx(b): return TX0 + (b - 1) * PITCH      # 바이트 b 의 왼쪽 끝

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §7",
      "누적 ACK 가 말하지 못하는 구간",
      "수신자가 1–1024 와 2049–3072 를 받았고 그 사이 1025–2048 이 아직 오지 않았다. ACK 번호는 순서대로 받은 끝까지만 셀 수 있어 1025 에서 멈추고, "
      "애플리케이션도 1024 까지만 받는다. 뒤쪽 2049–3072 를 받았다는 사실은 SACK 옵션이 따로 알려야 한다.",
      "ACK 번호는 하나의 경계선이라, 구멍 뒤의 섬은 그 칸으로 표현되지 않습니다")

Y_AX = 116
for b in (1, 1025, 2049, 3072):
    x = bx(b) if b != 3072 else TX1
    d.t(x, Y_AX, str(b), 11, SOFT, MONO)
    d.line(x, Y_AX + 8, x, 140 + 4 * ROW_H, RULE, 0.6, "2 4")

ROWS = ["수신 버퍼에 도착", "ACK 번호가 말함", "애플리케이션에 넘김", "SACK 블록이 더 말함"]
Y0 = 136
for i, lab in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 30, lab, 13, INK, KR, "start", 600)

def bar(i, b0, b1, c, label, focal=False, dash=False):
    y = Y0 + i * ROW_H + 10
    x, w = bx(b0), bx(b1 + 1) - bx(b0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    elif dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    else:
        d.tone(x, y, w, BAR_H, c, 4, "14", 1.0)
    d.t(x + w / 2, y + 19, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)

bar(0, 1, 1024, OK, "1–1024")
bar(0, 1025, 2048, BAD, "구멍 · 아직 안 옴", dash=True)
bar(0, 2049, 3072, INFO, "2049–3072")
# ACK 번호 — 경계선 하나
ay = Y0 + 1 * ROW_H
xk = bx(1025)
d.line(xk, ay + 6, xk, ay + ROW_H - 14, MUTED, 2.0)
d.t(xk + 10, ay + 30, "ACK 1025 · 1024 까지 받음", 12, MUTED, KR, "start", 600)
bar(2, 1, 1024, OK, "1–1024")
bar(2, 2049, 3072, INFO, "쥐고 기다림", dash=True)
bar(3, 2049, 3072, INFO, "2049–3072 받음", focal=True)

d.legend(H - 56, [("ACK 대신 알리는 SACK", ACC), ("순서대로 받은 구간", OK), ("순서 밖으로 받은 구간", INFO), ("빠진 구간", BAD)])
d.save("12-01.cumulative-ack-hole.svg")
