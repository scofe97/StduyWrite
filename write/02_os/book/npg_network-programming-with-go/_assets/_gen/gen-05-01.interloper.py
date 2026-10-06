# 타입 스펙: type-data-flow
# 05-01 단일 UDP 리스너 소켓에 도달하는 다중 송신자 데이터그램 흐름
# 사실 출처: NPG Ch.5 Listing 5-4, 5-5 (p.112-113)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 480
d = D(W, H, "NPG CH.5 — UDP INTERLOPER",
      "단일 UDP 소켓으로 몰리는 다중 송신자 데이터그램",
      "interloper 와 에코 서버의 패킷이 단일 클라이언트 소켓에 도달하는 흐름")

# 1. Senders (Left column)
x_send = 60
w_send = 180

# Sender 1: Interloper
y_int = 140
d.box(x_send, y_int, w_send, 60, fill=PAPER2, stroke=WARN, sw=1.2, r=6)
d.t(x_send + w_send / 2, y_int + 26, "제3자 (interloper)", 12, WARN, KR, "middle", 600)
d.t(x_send + w_send / 2, y_int + 46, "interloper.LocalAddr()", 11, SOFT, MONO, "middle")

# Datagram 1 orthogonal path to client socket slot 1 (y=200)
d.arrow([(x_send + w_send, y_int + 30), (360, y_int + 30), (360, 200), (440, 200)], c=WARN, m="warn")
d.chip(310, y_int + 15, '"pardon me"', WARN, 11)

# Sender 2: Echo Server
y_srv = 280
d.box(x_send, y_srv, w_send, 60, fill=PAPER2, stroke=INFO, sw=1.2, r=6)
d.t(x_send + w_send / 2, y_srv + 26, "정상 서버 (serverAddr)", 12, INFO, KR, "middle", 600)
d.t(x_send + w_send / 2, y_srv + 46, "echoServerUDP", 11, SOFT, MONO, "middle")

# Datagram 2 orthogonal path to client socket slot 2 (y=280)
d.arrow([(x_send + w_send, y_srv + 30), (360, y_srv + 30), (360, 280), (440, 280)], c=INFO, m="info")
d.chip(310, y_srv + 15, '"ping"', INFO, 11)

# 2. Convergence point (Client Socket)
x_cli = 440
y_cli = 140
w_cli = 340
h_cli = 200

# Client Socket boundary
d.box(x_cli, y_cli, w_cli, h_cli, fill=PAPER2, stroke=RULE, sw=1.2, r=8)
d.t(x_cli + 16, y_cli + 28, "클라이언트 소켓 (client.LocalAddr())", 12, INK, KR, "start", 600)
d.t(x_cli + 16, y_cli + 46, "단일 net.PacketConn 수신 큐", 11, SOFT, KR, "start")

# Received queue slots
x_q = x_cli + 20
w_q = w_cli - 40

# Slot 1: Interloper packet arrived first
y_q1 = y_cli + 60
d.box(x_q, y_q1, w_q, 52, fill=f"{WARN}18", stroke=WARN, sw=1.0, r=4)
d.t(x_q + 14, y_q1 + 22, '1차 ReadFrom: "pardon me"', 11, WARN, MONO, "start", 600)
d.t(x_q + 14, y_q1 + 40, "발신 주소: interloper.LocalAddr()", 11, MUTED, KR, "start")

# Slot 2: Echo packet arrived second
y_q2 = y_cli + 128
d.box(x_q, y_q2, w_q, 52, fill=f"{INFO}18", stroke=INFO, sw=1.0, r=4)
d.t(x_q + 14, y_q2 + 22, '2차 ReadFrom: "ping"', 11, INFO, MONO, "start", 600)
d.t(x_q + 14, y_q2 + 40, "발신 주소: serverAddr", 11, MUTED, KR, "start")

# Legend
d.legend(420, [("제3자 데이터그램", WARN), ("에코 서버 데이터그램", INFO), ("수신 소켓", SOFT)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-01.interloper.svg"))
d.save(out)
print(f"saved: {out}")
