# 타입 스펙: type-sequence
# 05-01 UDP 에코 서버의 ReadFrom 과 WriteTo 주소 전달 시퀀스
# 사실 출처: NPG Ch.5 Listing 5-1, 5-2 (p.109-111)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 840, 480
d = Seq(W, H, "NPG CH.5 — UDP READFROM & WRITETO",
        "UDP ReadFrom 과 WriteTo 주소 전달 시퀀스",
        "클라이언트와 에코 서버의 데이터그램 송수신 및 주소 재사용")

lanes = d.lanes([
    ("클라이언트", "net.PacketConn"),
    ("에코 서버", "net.PacketConn")
], y0=95, lane_w=200)

d.rails(420)

def msg_touch(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    x1, x2 = s.LX[a], s.LX[b]
    s.path(f"M {x1} {y} L {x2} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    s.t(mx, y - 9, label, 11, c, MONO, "middle", 600)
    if sub: s.t(mx, y + 17, sub, 11, MUTED)

d.msg = lambda a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None: msg_touch(d, a, b, label, y, c, mk, dash, sub)

# 1. Server listens & ReadFrom blocks
y1 = 160
d.state("에코 서버", "ReadFrom 대기", y1, WARN)

# 2. Client WriteTo(serverAddr)
y2 = 210
d.msg("클라이언트", "에코 서버", 'WriteTo(serverAddr, "ping")', y2, INFO, "info")
d.chip((d.LX["클라이언트"] + d.LX["에코 서버"]) / 2, y2 + 22, '데이터그램: "ping" [발신: clientAddr]', INFO)

# 3. Server receives (n, clientAddr)
y3 = 270
d.state("에코 서버", "(4, clientAddr) 반환", y3, OK)

# 4. Server WriteTo(clientAddr)
y4 = 320
d.msg("에코 서버", "클라이언트", 'WriteTo(clientAddr, "ping")', y4, OK, "ok")
d.chip((d.LX["클라이언트"] + d.LX["에코 서버"]) / 2, y4 + 22, '데이터그램: "ping" [발신: serverAddr]', OK)

# 5. Client ReadFrom receives echo
y5 = 380
d.state("클라이언트", "(4, serverAddr) 수신", y5, ACC)

# Legend
d.legend(440, [("송신 호출", INFO), ("수신·반환", OK), ("클라이언트 완료", ACC)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "05-01.readfrom-writeto.svg"))
d.save(out)
print(f"saved: {out}")
