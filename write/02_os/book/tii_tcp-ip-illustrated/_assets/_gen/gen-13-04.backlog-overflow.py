# 13-04 §2 — 원서 Listing 13-10: backlog 1 로 accept 를 미루는 FreeBSD 서버에 리눅스 클라이언트가 연달아 접속한다.
# 사실 출처: 원서 §13.7.4. 서버 sock -s -v -q1 -O30000 6666 (169.229.62.97:6666), 클라이언트 63.203.76.212.
#   1–3 포트 2461 handshake 완료, 4–6 포트 2462 handshake 완료(서버 애플리케이션은 둘 다 아직 accept 하지 않음).
#   7 포트 2463 SYN 21:28:47.446 → 응답 없음. 8–12 같은 ISN 2991331729 로 재전송:
#   50.446(+3s) 56.445(+6s) 29:08.443(+12s) 29:32.439(+24s) 30:20.432(+48s). FreeBSD·Solaris 는 큐가 차면 SYN 을 무시한다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 12개. 클라이언트 레인 바깥 글자가 포트와 간격이다.
#           축약: 스펙의 out-of-scope "lost message" 를 서버 레일 앞에서 끝나는 점선과 ✕ 로 그린다(무시된 SYN).
#           focal 은 셋째 연결의 첫 SYN 을 무시하는 서버 칩 하나.
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

W, H = 920, 724
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-04 §2",
          "수락 큐가 차면 FreeBSD 는 SYN 을 무시한다",
          "원서 Listing 13-10 의 순서다. backlog 를 1 로 두고 accept 를 오래 미루는 FreeBSD 서버에 리눅스 클라이언트가 연달아 접속한다. "
          "포트 2461 과 2462 의 handshake 는 서버 TCP 가 곧바로 끝내 두 클라이언트의 connect 가 성공하지만, 서버 애플리케이션은 아직 어느 연결도 받지 않았다. "
          "포트 2463 의 SYN 에는 응답이 없고, 클라이언트는 같은 SYN 을 3·6·12·24·48초 간격으로 다시 보낸다.",
          "handshake 는 TCP 가 끝내고, 애플리케이션은 아직 아무것도 받지 않았습니다")

C, S = "리눅스 클라이언트", "FreeBSD 서버"
d.lanes([(C, "63.203.76.212"), (S, "169.229.62.97:6666 · -q1")], y0=100, lane_w=300)
d.rails(656)
xc, xs = d.LX[C], d.LX[S]

def left(y, txt, c=SOFT, w=600):
    d.t(xc - 24, y + 4, txt, 12, c, _kr(txt), "end", w)
def right(y, txt, c=SOFT, w=600):
    d.t(xs + 24, y + 4, txt, 12, c, _kr(txt), "start", w)

y = 188
for port in ("2461", "2462"):
    left(y, "포트 " + port, INK)
    d.msg(C, S, "SYN", y, INFO, "info")
    d.msg(S, C, "SYN, ACK", y + 32, OK, "ok")
    d.msg(C, S, "ACK", y + 64, MUTED, "ar")
    right(y + 64, "accept 대기", OK)
    left(y + 64, "connect 성공", OK, 400)
    y += 112

def ignored(yy, label):
    mid = xs - 70
    d.path(f"M {xc + 10} {yy} L {mid} {yy}", INFO, 1.5, dash="5 4")
    d.t(mid + 10, yy + 5, "✕", 15, BAD, KR, "start", 700)
    d.t((xc + mid) / 2, yy - 9, label, 12, INFO, _kr(label), "middle", 600)

left(y, "포트 2463", INK)
ignored(y, "SYN 2991331729")
w = 132
d.o.append(f'<rect x="{xs + 20}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(xs + 20 + w / 2, y + 5, "큐 가득 · 무시", 12, ACC, KR, "middle", 600)
for gap in (3, 6, 12, 24, 48):
    y += 44
    left(y, f"+{gap}s", SOFT)
    ignored(y, "SYN 재전송")

d.legend(H - 56, [("SYN 무시", ACC), ("무시된 SYN", BAD), ("handshake 완료", OK), ("SYN", INFO)])
d.save("13-04.backlog-overflow.svg")
