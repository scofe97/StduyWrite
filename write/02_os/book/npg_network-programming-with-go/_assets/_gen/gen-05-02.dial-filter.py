# 타입 스펙: type-flowchart
# 05-02 Dial 로 연결된 UDP 소켓의 송신자 필터링 분기
# 사실 출처: NPG Ch.5 Listing 5-6~5-8 (p.114-115)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 480
d = D(W, H, "NPG CH.5 — UDP DIAL FILTER",
      "Dial 한 UDP 소켓의 송신자 필터링 흐름",
      "net.Dial 수신 소켓의 발신 주소 대조와 패킷 전달 분기")

# 1. Two incoming datagrams (Top level)
# Interloper datagram
d.box(160, 100, 180, 44, fill=PAPER2, stroke=WARN, r=6)
d.t(250, 119, '제3자: "pardon me"', 11, WARN, MONO, "middle", 600)
d.t(250, 134, "발신: interloper.LocalAddr()", 11, MUTED, KR, "middle")

# Echo server datagram
d.box(500, 100, 180, 44, fill=PAPER2, stroke=INFO, r=6)
d.t(590, 119, '에코 서버: "ping"', 11, INFO, MONO, "middle", 600)
d.t(590, 134, "발신: serverAddr", 11, MUTED, KR, "middle")

# Lines to Dial Socket (Merge point at y=170, no arrowhead on incoming branches)
d.path("M 250 144 L 250 170 L 420 170", WARN, 1.4)
d.path("M 590 144 L 590 170 L 420 170", INFO, 1.4)

# Merge point dot
d.o.append(f'<circle cx="420" cy="170" r="4" fill="{INK}"/>')

# 2. Socket receive step
d.arrow([(420, 170), (420, 196)], MUTED, "ar")
d.box(300, 196, 240, 40, fill=PAPER2, stroke=RULE, r=6)
d.t(420, 213, 'net.Dial("udp", serverAddr)', 11, INK, MONO, "middle", 600)
d.t(420, 228, "클라이언트 소켓 도달", 11, MUTED, KR, "middle")

# 3. Decision Diamond
d.arrow([(420, 236), (420, 260)], MUTED, "ar")
cx, cy, dw, dh = 420, 290, 130, 30
pts = f"{cx},{cy-dh} {cx+dw},{cy} {cx},{cy+dh} {cx-dw},{cy}"
d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{ACC}" stroke-width="1.2"/>')
d.t(cx, cy + 4, "발신 주소 == serverAddr ?", 11, ACC, KR, "middle", 600)

# Branch 1: No (Left arrow to discard)
d.arrow([(cx - dw, cy), (160, cy)], BAD, "bad")
d.t(225, cy - 8, "불일치 (No)", 11, BAD, KR, "middle")

d.box(50, cy - 24, 110, 48, fill=PAPER2, stroke=BAD, r=20)
d.t(105, cy + 4, "전달되지 않음", 11, BAD, KR, "middle", 600)

# Branch 2: Yes (Down arrow to Read)
d.arrow([(cx, cy + dh), (cx, 370)], OK, "ok")
d.t(cx + 42, 342, "일치 (Yes)", 11, OK, KR, "middle")

d.box(320, 370, 200, 44, fill=PAPER2, stroke=OK, r=6)
d.t(420, 389, 'client.Read(buf)', 11, OK, MONO, "middle", 600)
d.t(420, 404, '"ping" 정상 전달 (n=4)', 11, INK, KR, "middle")

# Legend
d.legend(440, [("제3자 패킷", WARN), ("서버 패킷", INFO), ("대조 기준", ACC), ("수신 성공", OK), ("전달 안 됨", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-02.dial-filter.svg"))
d.save(out)
print(f"saved: {out}")
