# 14-03 §5 — 원서 §14.10 Telnet 재패킷화 실험을 바이트 구간으로 그린다(원서 tcpdump 출력 대신).
# 사실 출처(ch14.txt §14.10): 'hello there' 13바이트(CR·LF 포함)가 먼저 가고 확인된다. 다음 줄은 케이블을 뺀 사이 사라진다.
#   재연결 뒤 순서 밖 세그먼트가 상대 순서 번호 29 에서 시작해 'and 3' 7바이트를 싣고 간다. 돌아온 ACK 는 ACK 번호 14 와
#   SACK 블록 {29,36} 을 싣는다. 송신자는 14:36 을 하나의 22바이트 세그먼트로 재전송하고, 이 세그먼트는 SACK 구간과 겹치며 FIN 도 싣는다.
# 축약: 유실 구간의 끝은 SACK 왼쪽 끝 29 로만 정했다(원서 본문의 '14바이트' 와 순서 번호가 한 바이트 어긋나 길이를 적지 않는다).
# 타입 스펙: type-gantt — 왼쪽 라벨 열 + 가로 축 + 행마다 막대, 막대 길이 = 구간.
#           축약: 가로 축이 시간이 아니라 상대 순서 번호(1–36)다. 12-01 cumulative-ack-hole 과 같은 축 문법이다.
#           focal 은 14–35 를 한 번에 다시 싣는 22바이트 재전송 막대.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 376
LX, TX0, TX1 = 20, 232, 872
ROW_H, BAR_H = 56, 28
TOTAL = 35                       # 바이트 1–35
PITCH = (TX1 - TX0) / TOTAL
def bx(b): return TX0 + (b - 1) * PITCH      # 바이트 b 의 왼쪽 끝 (b=36 이면 오른쪽 끝)

d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 14-03 §5",
      "재전송은 원래 세그먼트 경계를 따르지 않는다",
      "Telnet 으로 hello there 13바이트를 보내 확인받은 뒤, 다음 줄은 케이블을 뺀 사이 사라지고 재연결 뒤 and 3 이 순서 번호 29 부터 도착했다. "
      "수신자는 ACK 14 와 SACK [29,36) 을 보낸다. 송신자는 14 부터 35 까지를 22바이트 세그먼트 하나로 다시 보냈고, 이 세그먼트는 SACK 으로 알려진 구간과 겹치며 FIN 도 싣는다.",
      "순서 번호가 바이트 단위라 다시 묶어 보내도 같은 데이터입니다")

Y_AX = 116
for b in (1, 14, 29, 36):
    x = bx(b)
    d.t(x, Y_AX, str(b), 11, SOFT, MONO)
    d.line(x, Y_AX + 8, x, 136 + 3 * ROW_H, RULE, 0.6, "2 4")

ROWS = ["처음 보낸 세그먼트", "수신자가 알린 것", "재전송 세그먼트"]
Y0 = 136
for i, lab in enumerate(ROWS):
    y = Y0 + i * ROW_H
    d.box(LX - 8, y, W - 40 - (LX - 8), ROW_H - 8, PAPER2, RULE, 0.8, 6)
    d.t(LX + 4, y + 30, lab, 13, INK, KR, "start", 600)

def bar(i, b0, b1, c, label, focal=False, dash=False):
    y = Y0 + i * ROW_H + 10
    x, w = bx(b0), bx(b1) - bx(b0)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        c = ACC
    elif dash:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{BAR_H}" rx="4" fill="none" stroke="{c}" stroke-width="1.1" stroke-dasharray="5 4"/>')
    else:
        d.tone(x, y, w, BAR_H, c, 4, "14", 1.0)
    d.t(x + w / 2, y + 19, label, 12, c, MONO if all(ord(ch) < 128 for ch in label) else KR, "middle", 600)

bar(0, 1, 14, OK, "hello there · 13B")
bar(0, 14, 29, BAD, "유실", dash=True)
bar(0, 29, 36, INFO, "and 3 · 7B")
ay = Y0 + ROW_H
xk = bx(14)
d.line(xk, ay + 6, xk, ay + ROW_H - 14, MUTED, 2.0)
d.t(xk + 10, ay + 30, "ACK 14", 12, MUTED, MONO, "start", 600)
bar(1, 29, 36, INFO, "SACK [29,36)")
bar(2, 14, 36, ACC, "14–35 · 22B · FIN", focal=True)

d.legend(H - 56, [("다시 묶은 재전송", ACC), ("확인된 구간", OK), ("순서 밖 도착·SACK", INFO), ("유실 구간", BAD)])
d.save("14-03.repacketization.svg")
