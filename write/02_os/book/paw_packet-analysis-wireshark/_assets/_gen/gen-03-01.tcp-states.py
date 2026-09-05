# 03-01 학습 목표 뒤 전체 지도 — 이 편의 절들이 TCP 상태 전이를 따라간다.
# 원문의 상태 표와 세 handshake 표에 적힌 전이만 그린다. 없는 전이를 채우지 않는다.
# 타입 스펙: type-state — 주체 하나의 상태 전이. 전이 라벨은 무엇이 오갔는지(플래그)를 적고,
#           focal 은 애플리케이션 버그로 갇히는 상태 하나(CLOSE_WAIT).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, OK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 568
d = D(W, H, "PACKET ANALYSIS WITH WIRESHARK · 03-01",
      "TCP 연결의 상태 전이",
      "원문이 표로 적은 상태 전이를 한 장으로 이은 것. 윗줄이 연결을 여는 경로이고, 아래 두 줄이 닫는 경로다. 먼저 FIN 을 보낸 쪽과 받은 쪽이 서로 다른 상태를 지난다.",
      "닫는 경로가 둘로 갈립니다 — 누가 먼저 FIN 을 보냈는지가 그 갈림길입니다")

X = [72, 304, 536, 768]          # 가로 stride 232
SW, SH = 208, 52
Y1, Y2, Y3 = 120, 264, 408       # 세로 stride 144
BUS_A, BUS_P = 220, 36           # 능동 분기 corridor y, 수동 분기 좌측 x

def state(col, y, name, sub, c=None, focal=False):
    x = X[col]
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    elif c:
        d.tone(x, y, SW, SH, c, 8)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    col_c = ACC if focal else (c if c else INK)
    d.t(x + SW / 2, y + 22, name, 13, col_c, MONO, "middle", 600)
    d.t(x + SW / 2, y + 40, sub, 11, MUTED, KR)

def right(c1, c2, y, label, col=MUTED, mk="ar"):
    d.arrow([(X[c1] + SW, y + SH / 2), (X[c2] - 4, y + SH / 2)], col, mk, 1.4)
    d.t((X[c1] + SW + X[c2]) / 2, y - 12, label, 11, col, MONO)

# 전이선을 먼저 — z-order
right(0, 1, Y1, "SYN 송신")
right(1, 2, Y1, "SYN,ACK 수신")
# 능동 종료 분기 — corridor 를 타고 왼쪽 끝으로
d.arrow([(X[2] + SW / 2 - 48, Y1 + SH), (X[2] + SW / 2 - 48, BUS_A),
         (X[0] + SW / 2, BUS_A), (X[0] + SW / 2, Y2 - 4)], MUTED, "ar", 1.4)
d.t(X[1] + SW / 2, BUS_A - 10, "내가 먼저 FIN 송신", 11, MUTED, KR)
right(0, 1, Y2, "ACK 수신")
right(1, 2, Y2, "FIN 수신 · ACK 송신")
right(2, 3, Y2, "2×MSL 경과")
# 수동 종료 분기 — 좌측 여백을 타고 내려간다
d.arrow([(X[2] + SW / 2 + 48, Y1 + SH), (X[2] + SW / 2 + 48, BUS_A + 24),
         (BUS_P, BUS_A + 24), (BUS_P, Y3 + SH / 2), (X[0] - 4, Y3 + SH / 2)], INFO, "info", 1.4)
d.t(BUS_P + 132, 348, "상대가 먼저 FIN 송신", 11, INFO, KR)
right(0, 1, Y3, "FIN 송신", INFO, "info")
right(1, 2, Y3, "ACK 수신", INFO, "info")

state(0, Y1, "CLOSED", "원문이 \"가상의 상태\"라 적습니다")
state(1, Y1, "SYN_SENT", "클라이언트가 연결을 시작했습니다")
state(2, Y1, "ESTABLISHED", "데이터를 주고받습니다", c=OK)
state(0, Y2, "FIN_WAIT-1", "소켓을 닫았습니다")
state(1, Y2, "FIN_WAIT-2", "상대의 FIN 을 기다립니다")
state(2, Y2, "TIME_WAIT", "2×MSL 동안 머무릅니다")
state(3, Y2, "CLOSED", "능동 종료 끝", c=OK)
state(0, Y3, "CLOSE_WAIT", "애플리케이션이 안 닫았습니다", focal=True)
state(1, Y3, "LAST_ACK", "마지막 ACK 를 기다립니다")
state(2, Y3, "CLOSED", "수동 종료 끝", c=OK)

d.t(X[3] + 24, Y3 - 8, "능동 종료", 11, SOFT, KR, "start", 600)
d.t(X[3] + 24, Y3 + 10, "= 먼저 FIN 을 보낸 쪽", 11, MUTED, KR, "start")
d.t(X[3] + 24, Y3 + 34, "수동 종료", 11, INFO, KR, "start", 600)
d.t(X[3] + 24, Y3 + 52, "= FIN 을 받은 쪽", 11, MUTED, KR, "start")

d.legend(H - 72, [("애플리케이션이 안 닫으면 갇힙니다", ACC), ("정상 종점", OK), ("수동 종료 경로", INFO)])
d.save("03-01.tcp-states.svg")
