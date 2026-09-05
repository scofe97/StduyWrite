# 09-02 §4 — 뮤테이터가 진짜 소켓 대신 nonwriter 를 넘겨 아래의 응답을 가로챈다.
# 원문 근거: "the ServeDNS method will sometimes use the 'nonwriter' ResponseWriter ... in order
#            to capture a downstream plug-in's response and manipulate it." / "the response will
#            be stored in the Msg field of the nonwriter we passed in ... The result of that
#            function is simply written back to the client by calling WriteMsg on the original
#            ResponseWriter that was passed into our ServeDNS."
# 타입 스펙: type-sequence — 무엇을 누구에게 넘기느냐가 시간 순서 위에서만 보이고, 가짜를
#           넘긴 결과가 나중에 돌아오는 것이 논지다. Seq.msg 의 MONO 고정을 SeqKR 로 푼다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, BAD, OK, KR, MONO


def _kr(txt):
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class SeqKR(Seq):
    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dd = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * dd} {y} L {x2 - 12 * dd} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 11, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 11, MUTED, _kr(sub))


W, H = 880, 610
d = SeqKR(W, H, "LEARNING COREDNS · 09-02 §4",
          "nonwriter 가 응답을 가로채는 자리",
          "아래 플러그인에게 진짜 소켓을 그냥 넘기면 그쪽이 클라이언트에게 직접 써 버린다. "
          "가짜를 대신 넘기면 그 응답이 내 손에 남는다.",
          "주황이 진짜 대신 가짜를 넘기는 자리입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("클라이언트", "dns.ResponseWriter"),
         ("onlyone", "mutator"),
         ("아래 플러그인", "backend")], y0=104, lane_w=200)
d.rails(444)

d.msg("클라이언트", "onlyone", "질의 · w 를 함께 넘긴다", 192, INK)
chip("onlyone", "존이 내 것인가", 232, MUTED)
chip("onlyone", "nonwriter.New(w)", 272, ACC)
d.msg("onlyone", "아래 플러그인", "질의 · nw 를 넘긴다", 314, ACC,
      sub="진짜 w 는 내가 쥐고 있는다")
d.msg("아래 플러그인", "onlyone", "nw.Msg 에 쓴다", 362, ACC,
      sub="클라이언트로는 안 나간다")
chip("onlyone", "trimRecords", 402, ACC)
d.msg("onlyone", "클라이언트", "w.WriteMsg(다듬은 응답)", 440, OK)

d.box(20, 472, 410, 62, PAPER, RULE, 1.0)
d.t(36, 496, "존이 내 것이 아니면", 12, INK, KR, "start", 600)
d.t(36, 518, "손대지 않고 w 를 그대로 넘겨 결과를 돌려준다", 11, MUTED, KR, "start")

d.box(450, 472, 410, 62, PAPER, ACC, 1.0)
d.t(466, 496, "가짜를 넘기는 것이 요점", 12, ACC, KR, "start", 600)
d.t(466, 518, "아래는 자기가 클라이언트에 쓴 줄 안다", 11, MUTED, KR, "start")

d.legend(548, [("가짜 소켓이 오가는 구간", ACC), ("진짜 소켓에 쓰는 순간", OK)])
d.save("09-02.nonwriter.svg")
