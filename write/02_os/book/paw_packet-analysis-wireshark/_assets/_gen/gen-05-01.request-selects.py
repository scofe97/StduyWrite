# 05-01 §5 — REQUEST 한 번의 브로드캐스트가 선택과 거절을 겸한다. 서버 둘이 각자 OFFER 를 보내고,
# 클라이언트는 옵션 54 로 서버 1 을 지목한 REQUEST 를 한 번만 브로드캐스트한다. 근거는 RFC 2131 §3.1 4단계.
# 타입 스펙: type-sequence — 주체 셋(서버 1 · 클라이언트 · 서버 2) 사이의 시간순 메시지.
#           같은 y 에 좌우로 나가는 REQUEST 두 화살표가 "한 번의 브로드캐스트"다. headline 은 서버 1 의 ACK.
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

W, H = 940, 540
d = SeqKR(W, H, "PACKET ANALYSIS WITH WIRESHARK · 05-01 §5",
          "REQUEST 한 번이 선택과 거절을 겸한다",
          "서버 둘이 각자 OFFER 를 보낸다. 클라이언트는 옵션 54 에 서버 1 을 적은 REQUEST 를 한 번 브로드캐스트하고, 서버 1 에게는 요청이, 서버 2 에게는 제안을 거절했다는 통지가 된다.",
          "고르지 않은 서버에게 따로 거절을 보내지 않습니다 — 같은 브로드캐스트가 그 몫을 합니다")

d.lanes([("서버 1", "옵션 54 = 서버 1"), ("클라이언트", "UDP 68"), ("서버 2", "옵션 54 = 서버 2")], y0=104, lane_w=220)
d.rails(460)

d.msg("서버 1", "클라이언트", "OFFER", 200, INFO, "info", sub="서버 1 의 제안")
d.msg("서버 2", "클라이언트", "OFFER", 256, INFO, "info", sub="서버 2 의 제안")
d.state("클라이언트", "서버 1 을 고름", 300, SOFT)
d.msg("클라이언트", "서버 1", "REQUEST", 348, MUTED, "ar", sub="내 식별자 · 요청")
d.msg("클라이언트", "서버 2", "REQUEST", 348, MUTED, "ar", sub="남의 식별자 · 거절 통지")
d.msg("서버 1", "클라이언트", "ACK", 412, ACC, "acc", sub="바인딩 기록 후 확정")
d.state("서버 2", "제안을 거둠", 412, WARN)

d.legend(H - 56, [("선택된 서버의 확정", ACC), ("제안", INFO), ("거절로 받음", WARN)])
d.save("05-01.request-selects.svg")
