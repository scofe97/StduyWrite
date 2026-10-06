# 03-02 Go 의 TCP 연결 — Listen · Accept · Dial 호출 시퀀스와 패킷 교환
# 사실 출처: NPG Ch.3 Listing 3-1, 3-2, 3-3 (p.8-12)
# 타입 스펙: type-sequence — 서버와 클라이언트 고루틴의 소켓 호출과 TCP 세그먼트 시퀀스
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 840, 600

class SeqGo(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None):
        x1, x2 = s.LX[a], s.LX[b]
        s.path(f"M {x1} {y} L {x2} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 8, label, 11, c, MONO, "middle", 600)

    def note(s, a, txt, y, c, align="start"):
        x = s.LX[a]
        offset = 55 if align == "start" else -55
        s.chip(x + offset, y, txt, c, 11)

d = SeqGo(W, H, "NPG CHAPTER 3 — LISTENING AND DIALING",
          "Go 의 TCP 연결 수립과 종료 시퀀스",
          "소켓 호출과 패킷 왕복 시퀀스",
          "클라이언트 Close 시 서버 Read 에 io.EOF 반환")

lanes = d.lanes([
    ("서버 고루틴", "Listen · Accept"),
    ("클라이언트 고루틴", "Dial · Close")
], y0=95, lane_w=200)

d.rails(530)

# 1. Listen
y = 170
d.note("서버 고루틴", "net.Listen", y, OK, "start")

# 2. Accept
y = 205
d.note("서버 고루틴", "Accept 대기", y, WARN, "start")

# 3. Dial
y = 235
d.note("클라이언트 고루틴", "net.Dial", y, INFO, "end")

# 4. Handshake
y = 270
d.msg("클라이언트 고루틴", "서버 고루틴", "1. SYN", y, INFO, "info")

y = 300
d.msg("서버 고루틴", "클라이언트 고루틴", "2. SYN / ACK", y, WARN, "warn")

y = 330
d.msg("클라이언트 고루틴", "서버 고루틴", "3. ACK", y, INFO, "info")

# 5. Established & Read
y = 365
d.note("서버 고루틴", "Read 대기", y, SOFT, "start")

# 6. Close
y = 395
d.note("클라이언트 고루틴", "conn.Close", y, BAD, "end")

# 7. FIN exchange
y = 430
d.msg("클라이언트 고루틴", "서버 고루틴", "FIN", y, BAD, "bad")

y = 455
d.msg("서버 고루틴", "클라이언트 고루틴", "ACK", y, MUTED, "ar")

y = 485
d.note("서버 고루틴", "io.EOF 반환", y, WARN, "start")

y = 510
d.msg("서버 고루틴", "클라이언트 고루틴", "FIN", y, MUTED, "ar")

# Legend
d.legend(555, [("수립 (SYN)", INFO), ("대기·수신", WARN), ("종료 (FIN)", BAD)])

out = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "03-02.listen-accept-dial.svg"))
d.save(out)
print(f"saved: {out}")
