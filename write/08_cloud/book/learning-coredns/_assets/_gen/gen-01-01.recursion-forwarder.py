# 01-01 §5 — 재귀를 스스로 못 하는 CoreDNS 가 질의를 포워더에 넘기는 경로.
# 원문 근거: "CoreDNS can't process a query by starting at the root of a DNS namespace,
#            querying a root DNS server and following referrals until it gets an answer from
#            one of the authoritative DNS servers. Instead, it relies on other DNS servers
#            -- usually called forwarders -- for that."
# 타입 스펙: type-sequence — 주체 다섯 사이의 시간순 메시지이고, 어느 구간을 CoreDNS 가 못 하는지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, INK, PAPER, PAPER2, RULE, KR, MONO


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
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 12, MUTED, _kr(sub))

    def state(s, a, txt, y, c):
        x = s.LX[a]
        w = len(txt) * 14.0 + 26
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, _kr(txt))

W, H = 896, 680
d = SeqKR(W, H, "LEARNING COREDNS · 01-01 §5",
        "재귀는 포워더가 하고 CoreDNS 는 넘긴다",
        "CoreDNS 는 루트 서버부터 참조를 따라가는 완전 재귀를 수행하지 못한다. "
        "그래서 질의를 포워더에 넘기고, 루트에서 권한 서버까지 내려가는 구간은 포워더가 대신 밟는다.",
        "붉은 칩이 CoreDNS 가 스스로 못 하는 지점입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("클라이언트", "stub resolver"),
         ("CoreDNS", "forwarders 의존"),
         ("포워더", "재귀 수행"),
         ("루트 · 상위 서버", "referral"),
         ("권한 서버", "authoritative")], y0=104, lane_w=152)
d.rails(584)

d.msg("클라이언트", "CoreDNS", "질의", 196, MUTED, sub="www.example.com A")
chip("CoreDNS", "루트부터 따라갈 수 없다", 248, BAD)
d.msg("CoreDNS", "포워더", "질의 전달", 300, MUTED, sub="포워딩 플러그인")
d.msg("포워더", "루트 · 상위 서버", "루트부터 질의", 352, MUTED)
d.msg("루트 · 상위 서버", "포워더", "referral", 396, MUTED, dash="5 4")
d.msg("포워더", "권한 서버", "참조를 따라 질의", 440, MUTED)
d.msg("권한 서버", "포워더", "응답", 484, MUTED, dash="5 4")
d.msg("포워더", "CoreDNS", "응답", 528, MUTED, dash="5 4")
d.msg("CoreDNS", "클라이언트", "응답", 572, ACC, mk="acc")

d.legend(608, [("CoreDNS 가 스스로 못 하는 구간", BAD), ("클라이언트가 받는 답", ACC)])
d.save("01-01.recursion-forwarder.svg")
