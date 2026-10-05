# 14-02 §3 — 원서 Figure 14-11 을 대신한다. 첫 SACK 이 실은 누적 ACK 23801 과 SACK 블록 [25201, 26601).
# 사실 출처: 원서 §14.6.3 — ACK 23801 이 SACK 블록 [25201,26601] 을 실어 수신자의 구멍을 알린다. 수신자에게 없는 범위는 [23801,25200],
#   23801 에서 시작하는 1400바이트 패킷 하나다. SACK 블록의 두 번호는 연속 블록의 첫 순서 번호와 마지막 순서 번호 + 1(§14.6).
#   23801 앞은 누적 ACK 가 이미 연속으로 확인했다. 축 왼쪽 끝 22401 은 1400바이트 한 칸을 보이려고 고른 그리기 범위다.
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대, 막대 길이 = 구간. 가로 축은 시간이 아니라 바이트 번호다.
#           12-01.cumulative-ack-hole 과 같은 축 문법을 쓴다. focal 은 누적 ACK 가 말하지 못하는 섬을 알리는 SACK 블록.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, WARN, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 464
LX, TX0, TX1 = 20, 232, 872
ROW_H, BAR_H = 56, 28
B0, B1 = 22401, 26600
PITCH = (TX1 - TX0) / (B1 - B0 + 1)
def bx(b): return TX0 + (b - B0) * PITCH      # 바이트 b 의 왼쪽 끝

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-02 §3",
      "누적 ACK 23801 과 SACK 블록 하나",
      "수신자는 23800 까지 연속으로 받았고 23801–25200 의 1400바이트가 비었으며 그 뒤 25201–26600 을 따로 갖고 있다. 누적 ACK 는 23801 에서 멈추고, "
      "SACK 블록 [25201, 26601) 이 섬을 알린다. 오른쪽 경계 26601 은 마지막 받은 바이트가 아니라 그 다음 번호다. 송신자는 두 정보 사이의 구멍만 다시 보내면 된다.",
      "SACK 은 구멍 너머에 무엇이 있는지 알려 구멍의 크기를 정합니다")

Y_AX = 116
for b, lab in ((23801, "23801"), (25201, "25201"), (26601, "26601 · 다음 번호")):
    x = bx(b)
    d.t(x, Y_AX, lab, 11, SOFT, KR if b == 26601 else MONO, "end" if b == 26601 else "middle")
    d.line(x, Y_AX + 8, x, 136 + 4 * ROW_H, RULE, 0.6, "2 4")

ROWS = ["수신 버퍼", "누적 ACK 가 말함", "SACK 블록이 말함", "송신자가 다시 보낼 것"]
Y0 = 136
for i, lab in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 30, lab, 13, INK, KR, "start", 600)

def bar(i, b0, b1, c, label, focal=False, dash=False):
    y = Y0 + i * ROW_H + 10
    x, w = bx(b0), bx(b1 + 1) - bx(b0)
    if focal:
        d.o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    elif dash:
        d.o.append(f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{BAR_H}" rx="4" fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    else:
        d.tone(x, y, w, BAR_H, c, 4, "14", 1.0)
    d.t(x + w / 2, y + 19, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)

bar(0, 22401, 23800, OK, "23800 까지 연속")
bar(0, 23801, 25200, BAD, "구멍 · 1400B", dash=True)
bar(0, 25201, 26600, INFO, "섬 · 25201–26600")
ay = Y0 + 1 * ROW_H
xk = bx(23801)
d.line(xk, ay + 6, xk, ay + ROW_H - 14, MUTED, 2.0)
d.t(xk + 10, ay + 30, "ACK 23801 · 여기서 멈춤", 12, MUTED, KR, "start", 600)
bar(2, 25201, 26600, INFO, "[25201, 26601)", focal=True)
bar(3, 23801, 25200, BAD, "23801–25200")

d.legend(H - 56, [("SACK 블록", ACC), ("연속 수신", OK), ("순서 밖 수신", INFO), ("빠진 구간", BAD)])
d.save("14-02.sack-block.svg")
