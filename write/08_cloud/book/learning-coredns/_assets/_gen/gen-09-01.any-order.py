# 09-01 §5 — 같은 ANY 질의가 plugin.cfg 의 줄 위치에 따라 다른 답을 받는다.
# 원문 근거: "Since the any plug-in comes before the forward plug-in in plugin.cfg, it takes the
#            query and replies, never passing the request down the chain to the forward plug-in."
#            / 옮긴 뒤: ";; flags: qr rd ra ad; QUERY: 1, ANSWER: 18" / "Of course, any is
#            essentially useless when built this way because almost all other plug-ins come
#            before it."
# 타입 스펙: type-sequence — 같은 질의가 체인을 지나는 시간 순서가 논지이고, 어디서 멈추느냐가
#           두 경우를 가른다. Seq.msg 는 라벨 글꼴이 MONO 고정이라 KR 판별을 얹은 SeqKR 로 쓴다.
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


W, H = 880, 622
d = SeqKR(W, H, "LEARNING COREDNS · 09-01 §5",
          "같은 ANY 질의가 줄 위치에 따라 갈린다",
          "Corefile 은 그대로 두고 plugin.cfg 의 any 줄만 옮긴다. 위쪽에 있으면 any 가 답하고 "
          "forward 뒤로 옮기면 forward 가 먼저 가져간다.",
          "빨강이 any 가 요청을 못 보는 경우입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("클라이언트", "dig -t ANY"),
         ("any", "plugin"),
         ("forward", "plugin")], y0=104, lane_w=200)
d.rails(452)

d.t(20, 186, "any 가 앞줄일 때", 12, OK, KR, "start", 600)
d.msg("클라이언트", "any", "ANY example.com", 214, INK)
chip("any", "여기서 답한다", 258, OK)
d.msg("any", "클라이언트", "HINFO 하나 · ANSWER 1", 300, OK,
      sub="\"ANY obsoleted\" \"See RFC 8482\"")

d.line(20, 336, 860, 336, RULE, 0.8, "4 4")

d.t(20, 372, "any 를 forward 뒤로 옮겼을 때", 12, BAD, KR, "start", 600)
d.msg("클라이언트", "forward", "ANY example.com", 400, INK,
      sub="any 까지 닿지 않는다")
d.msg("forward", "클라이언트", "상류의 답 · ANSWER 18", 448, BAD)

d.box(20, 480, 840, 84, PAPER, RULE, 0.8)
d.t(36, 504, "Corefile 은 두 경우에 완전히 같다", 12, INK, KR, "start", 600)
d.t(36, 528, "바뀐 것은 plugin.cfg 의 줄 하나 위치뿐이고, 그것을 바꾸려면 다시 빌드해야 한다",
     11, MUTED, KR, "start")
d.t(36, 550, "저자들의 결론 — 이렇게 빌드하면 any 는 사실상 쓸모가 없다", 11, BAD, KR, "start")

d.legend(578, [("any 가 답하는 경우", OK), ("any 가 못 보는 경우", BAD)])
d.save("09-01.any-order.svg")
