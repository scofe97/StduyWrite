# 13-03 §6 — 원서 Listing 13-7·13-8 의 half-open 연결 실험을 시간순으로.
# 사실 출처: 원서 §13.6.3(PDF 45–48쪽). 10.0.0.1.1310 > 10.0.0.7.sunrpc(111).
#   1–3 handshake, 4 P 1:6(5) "foo"(CR LF 포함 5바이트), 5 ack 6. 서버 케이블 분리 · 재부팅 · 재연결(약 90초).
#   6–13 ARP. 14 P 6:11(5) "bar", 15 서버 R 2093796388:2093796388(0) win 0 — ACK 비트 없음.
#   Telnet 은 "Connection closed by remote host". 2093796388 은 서버 ISN 2093796387 + 1 이고 bar 세그먼트의 ACK 번호(상대 1)와 같다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 7개와 서버 쪽 재부팅 구간 하나.
#           축약: 재부팅 구간은 스펙의 activation bar 대신 서버 레인에 걸친 bad 색 띠로, ARP 6–13 은 화살표 없이 한 줄 주석으로 줄인다.
#           focal 은 기록 없는 서버가 bar 에 답하는 RST 하나.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, INFO, WARN, PAPER, PAPER2 as s_PAPER2, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 12, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}; n = len(names); span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, s_PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
            s.t(x, y0 + 37, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

W, H = 920, 700
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-03 §6",
          "half-open — 한쪽만 연결을 기억할 때",
          "원서 Listing 13-8 의 순서다. 클라이언트가 foo 5바이트를 보내고 ACK 를 받은 뒤 서버는 케이블을 뽑힌 채 재부팅해 연결 기록을 잃는다. "
          "클라이언트는 그 사이 아무것도 보내지 않아 여전히 ESTABLISHED 로 안다. 재부팅 뒤의 ARP 는 TCP 회복이 아니며, "
          "클라이언트가 같은 연결로 bar 를 보내자 그 4-tuple 을 모르는 서버가 ACK 비트 없는 RST 로 답한다.",
          "데이터를 보내기 전까지 살아 있는 쪽은 상대가 사라진 줄 모릅니다")

C, S = "Telnet 클라이언트", "sunrpc 서버"
d.lanes([(C, "10.0.0.1:1310"), (S, "10.0.0.7:111")], y0=100, lane_w=300)
d.rails(640)
xc, xs = d.LX[C], d.LX[S]

def st(side, y, txt, c=SOFT):
    if side == C: d.t(xc - 24, y + 4, txt, 12, c, _kr(txt), "end", 600)
    else: d.t(xs + 24, y + 4, txt, 12, c, _kr(txt), "start", 600)

d.msg(C, S, "SYN", 188, INFO, "info")
d.msg(S, C, "SYN, ACK", 220, OK, "ok")
d.msg(C, S, "ACK", 252, MUTED, "ar")
st(C, 252, "ESTABLISHED"); st(S, 252, "ESTABLISHED")
d.msg(C, S, "foo · 1:6(5)", 300, INFO, "info")
d.msg(S, C, "ACK 6", 348, MUTED, "ar")

# 서버 재부팅 구간
B0, B1 = 376, 452
d.tone(xs - 16, B0, 32, B1 - B0, BAD, 4, "22", 1.2)
d.t(xs - 28, B0 + 30, "케이블 분리 · 재부팅", 12, BAD, KR, "end", 600)
d.t(xs - 28, B0 + 52, "약 90초", 12, BAD, KR, "end")
st(S, B0 + 30, "연결 기록 없음", BAD)
st(C, B0 + 30, "ESTABLISHED 그대로")

d.t((xc + xs) / 2, 484, "ARP 6–13 · TCP 세그먼트 아님", 11, SOFT, KR, "middle")

d.msg(C, S, "bar · 6:11(5)", 528, INFO, "info")
d.msg(S, C, "R 2093796388", 580, ACC, "acc", sub="ACK 비트 없음 · 데이터 없음")
st(C, 580, "CLOSED", OK)
d.chip(xc + 140, 624, "Connection closed by remote host", MUTED, 11)

d.legend(H - 56, [("기록 없는 쪽의 RST", ACC), ("재부팅 구간", BAD), ("데이터", INFO)])
d.save("13-03.half-open.svg")
