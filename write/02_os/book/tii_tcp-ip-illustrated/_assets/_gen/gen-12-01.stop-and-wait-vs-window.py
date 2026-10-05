# 12-01 §2 — 같은 RTT 두 번 동안 정지-대기는 패킷 2개, 창 3 은 패킷 6개를 보낸다.
# 원문 12.1.1: 정지-대기의 처리량은 M/R 에 비례(M 패킷 크기, R RTT). 12.1.3: 창 W 면 SW/R 에 비례.
#              조립 라인 비유 — 한 제품이 다 나와야 다음 일이 들어가면 라인 대부분이 논다.
# 타입 스펙: type-sequence — 주체 둘(송신자·수신자) 사이의 시간순 메시지를 두 판으로 나란히 놓는다.
#           축약: 전파 지연이 논지라 메시지를 수평 화살표가 아니라 아래로 기운 선(line, 화살촉 없음)으로 그린다.
#           시간은 아래로만 흐르므로 기울기가 곧 방향이다. 왕복 시간 R 은 레인 옆 괄호로 잰다.
#           두 판은 같은 R(=160px)과 같은 전송 간격(16px)을 쓰고 창 크기만 1 과 3 으로 다르다 — 그 차이가 논지.
#           focal 은 오른쪽 판의 "RTT 두 번에 6개" 칩 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 680
d = D(W, H, "TCP/IP ILLUSTRATED VOL.1 · 12-01 §2",
      "멈춰 기다리기와 창 3 — 같은 RTT 동안 보내는 양",
      "왼쪽은 패킷 하나를 보내고 ACK 가 올 때까지 멈추는 정지-대기, 오른쪽은 ACK 없이 세 개까지 띄우는 창 방식이다. "
      "두 판 모두 왕복 시간 R 은 같고 아래로 기운 선이 패킷(파랑)과 ACK(회색)의 이동이다. RTT 두 번 동안 왼쪽은 2개, 오른쪽은 6개를 보낸다.",
      "링크 속도는 그대로인데 한 번에 띄우는 개수만 바꿨습니다")

R, TX, T0 = 160, 16, 160          # 왕복 시간 160px, 전송 간격 16px, 시작 시각
PW = 424
Y_LANE, Y_BOT = 108, T0 + 2 * R + 40

def panel(px, title, win, focal):
    sx, rx = px + 88, px + PW - 64
    d.t(px + PW / 2, 100 - 0, title, 13, INK, KR, "middle", 600)
    for x, nm in ((sx, "송신자"), (rx, "수신자")):
        d.box(x - 56, Y_LANE + 12, 112, 32, PAPER2, RULE, 1.0, 6)
        d.t(x, Y_LANE + 33, nm, 13, INK, KR, "middle", 600)
        d.line(x, Y_LANE + 48, x, Y_BOT, RULE, 1.0, "3 6")
    n = 0
    for rtt in range(2):
        base = T0 + rtt * R
        for i in range(win):
            t = base + i * TX
            n += 1
            d.line(sx, t, rx, t + R / 2, INFO, 1.6)                    # 패킷
            d.line(rx, t + R / 2, sx, t + R, MUTED, 1.2, "4 3")        # ACK
            d.t(sx - 8, t + 4, f"P{n}", 11, INFO, MONO, "end", 600)
    # RTT 괄호
    bx = sx - 44
    for k in range(2):
        y0, y1 = T0 + k * R, T0 + (k + 1) * R
        d.path(f"M {bx + 6} {y0} H {bx} V {y1 - 4} H {bx + 6}", SOFT, 1.1)
        d.t(bx - 6, (y0 + y1) / 2 + 4, "R", 12, SOFT, MONO, "end", 600)
    label = f"RTT 두 번에 {2 * win}개"
    cy = Y_BOT + 28
    if focal:
        w = 180
        d.o.append(f'<rect x="{px + PW / 2 - w / 2}" y="{cy - 13}" width="{w}" height="26" rx="5" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        d.t(px + PW / 2, cy + 5, label, 13, ACC, KR, "middle", 600)
    else:
        d.chip(px + PW / 2, cy, label, MUTED, 13)
    d.t(px + PW / 2, cy + 36, "처리량 ∝ S·W / R" if win > 1 else "처리량 ∝ M / R", 12, MUTED, MONO)

panel(24, "정지-대기 · 창 1", 1, False)
panel(472, "슬라이딩 윈도 · 창 3", 3, True)
d.line(W / 2, 84, W / 2, Y_BOT + 64, RULE, 0.8)

d.legend(Y_BOT + 104, [("창이 바꾼 결과", ACC), ("패킷", INFO), ("ACK", MUTED)])
d.save("12-01.stop-and-wait-vs-window.svg")
