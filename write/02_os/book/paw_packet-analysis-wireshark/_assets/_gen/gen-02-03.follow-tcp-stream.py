# 02-03 §4 — Follow TCP Stream 이 무엇을 모아 보여주는가. 목록에서는 흩어진 패킷이 한 대화로 묶인다.
# 타입 스펙: type-sequence — 주체 여럿 사이의 시간순 메시지. 요청은 클라이언트에서, 응답은 서버에서
#           오고, headline 은 원문이 예로 든 packet#35 의 HTTP 200 OK 하나.
#           프리미티브의 Seq.msg 가 한글 라벨을 MONO 로 하드코딩하므로 계약대로 서브클래스로 감싼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO

class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 17, sub, 11, MUTED, KR)

W, H = 880, 512
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 02-03 §4",
          "Follow TCP Stream 이 묶는 것",
          "Packet List 에서는 다른 대화와 섞여 흩어져 있던 요청과 응답이, 스트림 단위로 모여 한 창에 순서대로 나타난다. 원문의 예는 packet#35 의 HTTP 200 OK 를 기점으로 스트림을 여는 것이다.",
          "목록에서 흩어져 있던 세그먼트가 한 대화로 순서대로 이어집니다")

d.lanes([("클라이언트", "10.0.0.221"), ("Wireshark", "http_01.pcap"), ("서버", "122.167.99.148")],
        y0=104, lane_w=224)
d.rails(408)

d.msg("클라이언트", "서버", "GET /", 196, INFO, "info", sub="요청 한 줄")
d.msg("서버", "클라이언트", "HTTP/1.1 200 OK", 252, ACC, "acc", dash=None, sub="packet#35 — 원문이 스트림을 여는 기점")
d.msg("서버", "클라이언트", "Continuation", 308, MUTED, "ar", dash="4,3", sub="본문이 여러 세그먼트로 옵니다")
d.selfmsg("Wireshark", "Follow TCP Stream", 366, ACC,
          sub="같은 스트림의 세그먼트를 순서대로 이어 붙입니다")

d.legend(436, [("요청", INFO), ("응답 · 스트림 재조립", ACC)])
d.save("02-03.follow-tcp-stream.svg")
