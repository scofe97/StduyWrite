# 13-03 §2 — 마지막 ACK 가 사라졌을 때 TIME_WAIT 가 하는 일.
# 사실 출처: 원서 §13.5.2(PDF 32–33쪽) — "The final ACK is resent not because the TCP retransmits ACKs ...
#   but because the other side will retransmit its FIN ... TCP will always retransmit FINs until it receives a final ACK."
#   능동 닫기 쪽은 마지막 ACK 를 보낸 뒤 2MSL 동안 TIME_WAIT 에 머문다. 상태 이름은 원서 Figure 13-9 의 닫기 경로.
#   원서는 이 장면을 그림으로 두지 않았다. 본문 문장을 시간순 메시지로 옮긴 것이다.
# 타입 스펙: type-sequence — 주체 둘 사이의 시간순 메시지 6개. 레인 바깥 글자가 그 시점의 상태다.
#           축약: 스펙의 out-of-scope "lost message" 를 끊긴 선 끝의 ✕ 로 그린다(12-01 ack-loss-ambiguity 관례).
#           왼쪽 레인 옆 괄호가 TIME_WAIT 구간이고, 위쪽 FIN_WAIT_2 · CLOSE_WAIT 줄은 §3 이 다시 가리킨다.
#           focal 은 재전송된 FIN 에 답하는 두 번째 ACK 하나 — TIME_WAIT 가 남아 있는 첫째 이유.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, BAD, WARN, PAPER, PAPER2 as s_PAPER2, RULE, KR, MONO

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

W, H = 920, 640
d = SeqKR(W, H, "TCP/IP ILLUSTRATED VOL.1 · 13-03 §2",
          "마지막 ACK 가 사라지면 FIN 이 다시 온다",
          "능동 닫기 쪽이 보낸 마지막 ACK 가 길에서 사라졌다. 수동 닫기 쪽은 LAST_ACK 에서 확인을 못 받아 자기 FIN 을 다시 보낸다. "
          "능동 닫기 쪽은 아직 TIME_WAIT 에 연결 기록을 갖고 있어 그 FIN 에 ACK 를 다시 보낼 수 있고, 2MSL 이 지난 뒤에야 CLOSED 가 된다. "
          "TCP 는 ACK 자체를 재전송하지 않으므로, ACK 를 다시 보내게 만드는 것은 상대의 FIN 재전송이다.",
          "ACK 는 재전송되지 않습니다 — 상대의 FIN 재전송에 다시 답할 뿐입니다")

A, P = "능동 닫기 쪽", "수동 닫기 쪽"
d.lanes([(A, "먼저 close()"), (P, "FIN 을 받은 쪽")], y0=100, lane_w=300)
d.rails(568)
xa, xp = d.LX[A], d.LX[P]

def st(side, y, txt, c=SOFT):
    if side == A: d.t(xa - 32, y + 4, txt, 12, c, _kr(txt), "end", 600)
    else: d.t(xp + 24, y + 4, txt, 12, c, _kr(txt), "start", 600)

Y_FIN1, Y_ACK1, Y_FIN2, Y_LOST, Y_REFIN, Y_REACK, Y_END = 196, 248, 300, 352, 436, 488, 548

d.msg(A, P, "FIN", Y_FIN1, WARN, "warn")
st(A, Y_FIN1, "FIN_WAIT_1")
d.msg(P, A, "ACK", Y_ACK1, MUTED, "ar")
st(A, Y_ACK1, "FIN_WAIT_2")
st(P, Y_ACK1, "CLOSE_WAIT")
d.t(xp + 24, Y_ACK1 + 22, "close() 호출 전까지", 11, MUTED, KR, "start")
d.msg(P, A, "FIN", Y_FIN2, WARN, "warn")
st(P, Y_FIN2, "LAST_ACK")

# 마지막 ACK — 길에서 사라짐
mid = (xa + xp) / 2
d.path(f"M {xa + 10} {Y_LOST} L {mid} {Y_LOST}", MUTED, 1.5, dash="5 4")
d.t(mid + 10, Y_LOST + 5, "✕", 15, BAD, KR, "start", 700)
d.t(mid - 60, Y_LOST - 9, "마지막 ACK", 12, MUTED, KR, "middle", 600)
d.t(mid + 70, Y_LOST + 22, "유실", 11, BAD, KR, "middle")

# 수동 닫기 쪽 재전송 타이머 괄호
d.path(f"M {xp + 14} {Y_FIN2 + 12} H {xp + 22} V {Y_REFIN - 12} H {xp + 14}", SOFT, 1.2)
d.t(xp + 32, (Y_FIN2 + Y_REFIN) / 2 + 4, "FIN 재전송 타이머", 12, SOFT, KR, "start")

d.msg(P, A, "FIN 재전송", Y_REFIN, WARN, "warn")
d.msg(A, P, "ACK 다시", Y_REACK, ACC, "acc", sub="TIME_WAIT 의 기록으로 답함")
st(P, Y_REACK + 28, "CLOSED", OK)

# 능동 닫기 쪽 TIME_WAIT 괄호
TW0, TW1 = Y_LOST + 8, Y_END - 8
d.path(f"M {xa - 14} {TW0} H {xa - 22} V {TW1} H {xa - 14}", ACC, 1.4)
d.t(xa - 32, (TW0 + TW1) / 2 - 4, "TIME_WAIT", 12, ACC, MONO, "end", 600)
d.t(xa - 32, (TW0 + TW1) / 2 + 14, "2MSL", 12, ACC, MONO, "end", 600)
st(A, Y_END + 8, "CLOSED", OK)

d.legend(H - 56, [("TIME_WAIT 가 다시 답함", ACC), ("FIN", WARN), ("유실", BAD), ("닫힘", OK)])
d.save("13-03.time-wait-last-ack.svg")
