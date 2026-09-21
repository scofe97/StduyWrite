# 05-01 §5 — OFFER 는 예약이 아니다. 서버가 같은 주소를 두 클라이언트에게 제안하고,
# 먼저 도착한 REQUEST 만 장부에 적혀 ACK 를 받는다. 근거는 RFC 2131 §3.1 2·4단계와 원문 REQUEST 설명.
# 타입 스펙: type-sequence — 주체 셋(클라이언트 A · 서버 · 클라이언트 B) 사이의 시간순 메시지.
#           headline(accent)은 장부에 적힌 뒤 나가는 A 의 ACK 하나. 늦은 B 의 NAK 은 warn.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, BAD, PAPER, RULE, KR, MONO

def _kr(t): return KR if any("가" <= c <= "힣" for c in str(t)) else MONO
def _w(t, size): return sum(size if "가" <= c <= "힣" else size * 0.62 for c in str(t))
class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]; dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub: s.t(mx, y + 18, sub, 12, MUTED, KR)
    def lanes(s, names, y0=104, lane_w=210):
        LX = Seq.lanes(s, [(nm, "") for nm, _ in names], y0, lane_w)
        for nm, sub in names:  # 서브라벨만 한글 스택으로 다시 찍는다
            s.t(LX[nm], y0 + 37, sub, 12, MUTED, _kr(sub))
        return LX
    def state(s, a, txt, y, c):
        x = s.LX[a]; w = _w(txt, 12) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{PAPER}"/>')  # 레인 점선 가림
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 12, c, _kr(txt))

W, H = 940, 668
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §5",
          "OFFER 는 예약이 아니다",
          "서버가 장부에 적지 않은 채 같은 주소를 두 클라이언트에게 제안한다. 둘 다 그 주소로 REQUEST 를 보내면 먼저 도착한 A 만 장부에 적혀 ACK 를 받고, 늦은 B 는 NAK 을 받아 찾기부터 다시 시작한다.",
          "장부에 이름이 적히는 때는 OFFER 가 아니라 REQUEST 가 도착한 뒤입니다")

d.lanes([("클라이언트 A", "UDP 68"), ("서버", "UDP 67"), ("클라이언트 B", "UDP 68")], y0=104, lane_w=220)
d.rails(588)

d.msg("서버", "클라이언트 A", "OFFER", 200, INFO, "info", sub="yiaddr = 주소 X")
d.msg("서버", "클라이언트 B", "OFFER", 256, INFO, "info", sub="yiaddr = 같은 주소 X")
d.state("서버", "장부 비어 있음", 300, SOFT)
d.msg("클라이언트 A", "서버", "REQUEST", 348, MUTED, "ar", sub="옵션 50 = X · 먼저 도착")
d.state("서버", "장부에 A 기록", 392, OK)
d.msg("서버", "클라이언트 A", "ACK", 440, ACC, "acc", sub="X 확정")
d.msg("클라이언트 B", "서버", "REQUEST", 496, MUTED, "ar", sub="옵션 50 = X · 늦게 도착")
d.msg("서버", "클라이언트 B", "NAK", 552, WARN, "warn", sub="이미 할당된 주소")
d.state("클라이언트 B", "DISCOVER 부터 다시", 588, WARN)

d.legend(H - 56, [("장부에 적힌 뒤의 확정", ACC), ("제안", INFO), ("장부 상태", OK), ("거절 · 재시작", WARN)])
d.save("05-01.offer-not-reserved.svg")
