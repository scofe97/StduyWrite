# 타입 스펙: type-sequence
# 07-01 unixgram 양방향 바인딩과 주소 전달 시퀀스
# 사실 출처: NPG Ch.7 Listing 7-7·7-8·7-9 (sSocket, cSocket, ListenPacket, WriteTo, ReadFrom)
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, OK, INFO, ACC, MUTED, MONO

W, H = 840, 480
d = Seq(W, H, "NPG CH.7 — UNIXGRAM DUAL BINDING",
        "unixgram 양방향 바인딩 시퀀스",
        "서버와 클라이언트의 소켓 파일 바인딩과 WriteTo/ReadFrom 주소 교환")

lanes = d.lanes([
    ("클라이언트", "c<pid>.sock"),
    ("에코 서버", "s<pid>.sock")
], y0=95, lane_w=200)

d.rails(415)

def msg_touch(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
    x1, x2 = s.LX[a], s.LX[b]
    s.path(f"M {x1} {y} L {x2} {y}", c, 1.5, m=mk, dash=dash)
    mx = (x1 + x2) / 2
    s.t(mx, y - 9, label, 11, c, MONO, "middle", 600)
    if sub:
        s.t(mx, y + 17, sub, 10, MUTED, MONO)

d.msg = lambda a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None: msg_touch(d, a, b, label, y, c, mk, dash, sub)

# 1. 각자 소켓 파일 바인딩
y1 = 175
d.state("클라이언트", "ListenPacket(cSocket)", y1, INFO)
d.state("에코 서버", "ListenPacket(sSocket)", y1, OK)

# 2. 클라이언트 -> 서버: WriteTo(msg, serverAddr)
y2 = 235
d.msg("클라이언트", "에코 서버", 'WriteTo("ping", serverAddr)', y2, INFO, "info")

# 3. 서버: ReadFrom -> clientAddr 획득
y3 = 285
d.state("에코 서버", "ReadFrom → clientAddr", y3, OK)

# 4. 서버 -> 클라이언트: WriteTo(msg, clientAddr)
y4 = 335
d.msg("에코 서버", "클라이언트", 'WriteTo("ping", clientAddr)', y4, OK, "ok", dash="4 4")

# 5. 클라이언트: ReadFrom -> serverAddr 검증
y5 = 385
d.state("클라이언트", "ReadFrom → serverAddr", y5, ACC)

# 범례
d.legend(435, [("클라이언트 바인딩·호출", INFO), ("서버 바인딩·응답", OK), ("클라이언트 수신", ACC)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "07-01.unixgram-bind.svg"))
d.save(out)
print(f"saved: {out}")
