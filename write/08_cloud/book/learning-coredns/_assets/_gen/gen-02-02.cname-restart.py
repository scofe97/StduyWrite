# 02-02 §3 — 재귀 서버가 별칭에 붙은 CNAME 을 받으면 정규 이름으로 질의를 다시 시작한다.
# 원문 근거: "a recursive DNS server looking up alias.foo.example's AAAA records ... would receive
#            the record ... The recursive DNS server would then restart the query, this time looking
#            for AAAA records for canonicalname.foo.example. If attaching a AAAA record directly to
#            alias.foo.example were permitted, the results ... would be ambiguous."
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 왕복이고, 가운데의 재시작이 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, INK, PAPER2, RULE, KR, MONO, PAPER


def _kr(txt):
    """한글이 섞인 라벨은 한글 스택으로 — mono 에 넣으면 자간이 벌어진다(스타일 계약 §타이포그래피)."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
            s.t(x, y0 + 20, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 38, sub, 11, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dr} {y} L {x2 - 12 * dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 14.0 + 26
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))


W, H = 880, 560
d = SeqKR(W, H, "LEARNING COREDNS · 02-02 §3",
          "별칭을 받으면 질의를 다시 시작한다",
          "재귀 서버는 별칭에 붙은 CNAME 을 받고 나서 정규 이름으로 질의를 새로 던진다. "
          "이 재시작 때문에 별칭에 다른 타입을 직접 붙이는 것이 금지된다.",
          "붉은 칩이 이 규칙을 필요하게 만든 지점입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("재귀 DNS 서버", "recursive"),
         ("foo.example 권한 서버", "authoritative")], y0=104, lane_w=280)
d.rails(420)

d.msg("재귀 DNS 서버", "foo.example 권한 서버", "AAAA 질의", 196, MUTED, sub="alias.foo.example")
d.msg("foo.example 권한 서버", "재귀 DNS 서버", "CNAME 응답", 248, MUTED, dash="5 4",
      sub="canonicalname.foo.example")
chip("재귀 DNS 서버", "질의를 다시 시작한다", 304, BAD)
d.msg("재귀 DNS 서버", "foo.example 권한 서버", "AAAA 질의", 356, MUTED, sub="canonicalname.foo.example")
d.msg("foo.example 권한 서버", "재귀 DNS 서버", "AAAA 응답", 408, ACC, mk="acc")

d.t(20, 462, "별칭에 AAAA 를 직접 붙이는 것이 허용된다면 alias.foo.example 의 AAAA 조회 결과가 모호해진다", 13, MUTED, KR, "start")
d.t(20, 484, "그래서 별칭인 도메인 이름에는 다른 타입의 레코드를 붙일 수 없다", 13, MUTED, KR, "start")

d.legend(504, [("재시작을 부르는 지점", BAD), ("최종 응답", ACC)])
d.save("02-02.cname-restart.svg")
