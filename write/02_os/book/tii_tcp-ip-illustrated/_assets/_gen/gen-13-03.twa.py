# 13-03 §7 — 원서 Figure 13-10 의 TIME-WAIT Assassination(TWA).
# 사실 출처: 원서 §13.6.4(PDF 48–49쪽). 서버는 연결 역할을 끝내고 상태를 지웠고 클라이언트만 TIME_WAIT 에 남았다.
#   FIN 교환이 끝났을 때 클라이언트의 다음 순서 번호 K, 서버의 다음 번호 L. 서버에서 클라이언트로 늦게 도착한 세그먼트는
#   seq=L-100, ack=K-200. 클라이언트는 두 값이 모두 옛 값이라 판단하고 현재 값 seq=K, ack=L 로 ACK 한다.
#   연결을 모르는 서버는 RST 로 답하고, 클라이언트는 TIME_WAIT 에서 CLOSED 로 조기 전이한다.
#   대부분의 시스템은 TIME_WAIT 에서 RST 에 반응하지 않아 이를 피한다(RFC 1337).
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 3개와 클라이언트 레인의 TIME_WAIT 구간.
#           축약: 남았어야 할 대기 구간을 점선 괄호로 이어 그려, 잘려 나간 길이가 보이게 한다.
#           focal 은 RST 를 받고 CLOSED 로 끝나 버리는 클라이언트 칩 하나.
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

W, H = 920, 620
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-03 §7",
          "TIME-WAIT Assassination — RST 가 대기를 끊는다",
          "원서 Figure 13-10 의 상황이다. 서버는 이미 연결 기록을 지웠고 클라이언트만 TIME_WAIT 에 남아 있다. 서버 쪽에서 늦게 도착한 옛 세그먼트 "
          "seq=L-100, ack=K-200 을 받은 클라이언트는 현재 값 seq=K, ack=L 로 ACK 한다. 연결을 모르는 서버가 RST 로 답하고, 클라이언트가 그 RST 를 받아들이면 "
          "2MSL 을 다 채우지 못한 채 CLOSED 로 간다. 많은 시스템은 TIME_WAIT 에서 RST 에 반응하지 않는다.",
          "옛 세그먼트를 막으려던 대기가 옛 세그먼트 때문에 끝납니다")

C, S = "클라이언트", "서버"
d.lanes([(C, "다음 seq K"), (S, "다음 seq 였던 L")], y0=100, lane_w=300)
d.rails(560)
xc, xs = d.LX[C], d.LX[S]

def st(side, y, txt, c=SOFT):
    if side == C: d.t(xc - 32, y + 4, txt, 12, c, _kr(txt), "end", 600)
    else: d.t(xs + 24, y + 4, txt, 12, c, _kr(txt), "start", 600)

st(S, 180, "기록 지움", MUTED)
d.msg(S, C, "seq=L−100 · ack=K−200", 220, MUTED, "ar", dash="5 4", sub="늦게 도착한 옛 세그먼트")
d.msg(C, S, "ACK seq=K · ack=L", 292, INFO, "info", sub="옛 번호에 현재 번호로 답함")
st(S, 292, "연결 모름", BAD)
d.msg(S, C, "RST", 364, BAD, "bad")

# TIME_WAIT 괄호 — 실제로 머문 구간(실선)과 남았어야 할 구간(점선)
T0, T1, T2 = 176, 368, 536
d.path(f"M {xc - 14} {T0} H {xc - 22} V {T1}", WARN, 1.4)
d.t(xc - 32, (T0 + T1) / 2 + 4, "TIME_WAIT", 12, WARN, MONO, "end", 600)
d.path(f"M {xc - 22} {T1} V {T2} H {xc - 14}", SOFT, 1.2, dash="4 4")
d.t(xc - 32, (T1 + T2) / 2 + 4, "남았어야 할 2MSL", 12, SOFT, KR, "end")

w = 148
d.o.append(f'<rect x="{xc + 24}" y="{T1 + 28}" width="{w}" height="24" rx="4" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(xc + 24 + w / 2, T1 + 45, "CLOSED · 조기 종료", 12, ACC, KR, "middle", 600)

d.chip((xc + xs) / 2 + 60, 480, "대응 · TIME_WAIT 에서 RST 무시", OK, 12)

d.legend(H - 56, [("조기 종료", ACC), ("TIME_WAIT", WARN), ("RST", BAD), ("대응", OK)])
d.save("13-03.twa.svg")
