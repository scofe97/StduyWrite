# 02-01 §6 — 재귀를 지는 것은 질의를 받은 첫 서버 하나이고, 나머지는 참조만 돌려준다.
# 원문 근거: "the process the first DNS server followed ... is called recursion",
#            "the root DNS server doesn't query the top-level zone's DNS servers on behalf of
#             the first DNS server. The root DNS server simply replies with NS records",
#            리졸버는 재귀 질의를, DNS 서버끼리는 기본적으로 비재귀(반복) 질의를 보낸다.
# 예시 이름은 §7 캐시 사다리와 같은 www.google.com AAAA — 이 도식의 첫 줄이 사다리의 맨 윗 막대다.
# 2026-09-23 신설: 옛 server-decision(판단 순서 흐름도)을 대체한다. 절의 물음이 "누가 재귀를 지는가"라
#                  판단 분기보다 주체 사이의 왕복이 요점이다(적대적 검증 지적).
# 타입 스펙: type-sequence — 주체 다섯 사이의 시간순 메시지이고, 한 레인만 일을 떠맡는 비대칭이 논지다.
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, OK, INK, PAPER, PAPER2, RULE, KR, MONO


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

W, H = 896, 690
d = SeqKR(W, H, "LEARNING COREDNS · 02-01 §6",
        "재귀는 첫 서버 혼자 진다",
        "리졸버의 재귀 질의를 받은 서버가 루트, com, google.com 서버에 차례로 반복 질의를 보낸다. "
        "루트와 com 서버는 다음 서버를 가리키는 NS 참조만 돌려주고, 권한 서버에 닿아야 답이 온다.",
        "참조를 돌려주는 두 서버는 한 번씩 답하고 끝납니다")


def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("리졸버", "OS 안 · stub"),
         ("재귀 서버", "recursion"),
         ("루트 서버", "."),
         ("com 서버", "TLD"),
         ("google.com 서버", "authoritative")], y0=104, lane_w=152)
d.rails(596)

d.msg("리졸버", "재귀 서버", "재귀 질의", 196, MUTED, sub="www.google.com AAAA")
chip("재귀 서버", "재귀를 지는 유일한 서버", 248, ACC)
d.msg("재귀 서버", "루트 서버", "반복 질의", 300, MUTED)
d.msg("루트 서버", "재귀 서버", "참조 · com NS", 344, MUTED, dash="5 4")
d.msg("재귀 서버", "com 서버", "반복 질의", 392, MUTED)
d.msg("com 서버", "재귀 서버", "참조 · google.com NS", 436, MUTED, dash="5 4")
d.msg("재귀 서버", "google.com 서버", "반복 질의", 484, MUTED)
d.msg("google.com 서버", "재귀 서버", "답 · AAAA", 528, OK, mk="ok", dash="5 4")
d.msg("재귀 서버", "리졸버", "답", 576, ACC, mk="acc")

d.legend(624, [("재귀를 지는 서버", ACC), ("권한 있는 답", OK)])
d.save("02-01.referral-chain.svg")
