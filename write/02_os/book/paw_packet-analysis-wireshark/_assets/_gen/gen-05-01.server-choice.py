# 05-01 §2 — 서버가 여럿일 때 클라이언트가 고르는 것은 주소가 아니라 서버다. 두 서버가 각자 ADVERTISE 를 보내고,
# 클라이언트는 Preference 값으로 서버 1 을 골라 그 식별자를 REQUEST 에 넣는다. 근거는 RFC 8415 §18.2.9·§21.8·§16.4.
# 원문 pcap 에는 서버가 하나뿐이라 두 번째 서버는 구조를 보이기 위한 예시이고, 주소·xid 같은 값은 적지 않는다.
# 타입 스펙: type-sequence — 주체 셋(서버 1 · 클라이언트 · 서버 2) 사이의 시간순 메시지.
#           같은 y 에 좌우로 나가는 두 화살표가 멀티캐스트 한 번이다. headline 은 서버 1 의 REPLY.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, OK, INFO, WARN, PAPER, RULE, KR, MONO

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

W, H = 940, 596
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §2",
          "서버마다 제안하고, 클라이언트는 서버를 고른다",
          "SOLICIT 은 멀티캐스트라 링크의 두 서버가 모두 듣고 각자 ADVERTISE 로 제안한다. 클라이언트는 Preference 값이 높은 서버 1 을 골라 그 서버 식별자를 넣은 REQUEST 를 보내고, 식별자가 다른 서버 2 는 그 REQUEST 를 버린다.",
          "고르는 대상은 주소 목록이 아니라 서버입니다 — Preference 옵션이 기준입니다")

d.lanes([("서버 1", "UDP 547"), ("클라이언트", "UDP 546"), ("서버 2", "UDP 547")], y0=104, lane_w=220)
d.rails(516)

d.msg("클라이언트", "서버 1", "SOLICIT", 200, INFO, "info", sub="ff02::1:2 멀티캐스트")
d.msg("클라이언트", "서버 2", "SOLICIT", 200, INFO, "info", sub="같은 메시지를 함께 들음")
d.msg("서버 1", "클라이언트", "ADVERTISE", 256, INFO, "info", sub="서버 1 의 제안 · Preference 높음")
d.msg("서버 2", "클라이언트", "ADVERTISE", 312, INFO, "info", sub="서버 2 의 제안 · Preference 낮음")
d.state("클라이언트", "서버 1 을 고름", 356, SOFT)
d.msg("클라이언트", "서버 1", "REQUEST", 404, MUTED, "ar", sub="서버 식별자 = 서버 1")
d.msg("클라이언트", "서버 2", "REQUEST", 404, MUTED, "ar", sub="남의 식별자")
d.msg("서버 1", "클라이언트", "REPLY", 468, ACC, "acc", sub="바인딩 기록 후 확정")
d.state("서버 2", "REQUEST 를 버림", 468, WARN)

d.legend(H - 56, [("고른 서버의 확정", ACC), ("찾기 · 제안", INFO), ("식별자 불일치", WARN)])
d.save("05-01.server-choice.svg")
