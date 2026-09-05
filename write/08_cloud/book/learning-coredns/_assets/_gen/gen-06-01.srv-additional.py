# 06-01 §6 — SRV 응답의 ADDITIONAL 구간이 뒤따를 A 조회를 없앤다.
# 원문 근거: "The ADDITIONAL SECTION of the result from the SRV query contains the A records referred
#            to by the SRV record's targets. This allows them to be used immediately without any
#            additional lookups for those names." / 원서 Example 6-5 의 엔드포인트는 넷이다.
# 타입 스펙: type-sequence — 두 주체 사이의 시간순 왕복이고, 없어진 왕복 넷이 논지다.
#           프리미티브의 mono 하드코딩을 SeqKR 로 덮는다(계약 §프리미티브가 한글을 mono 로 내보내는 자리).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, OK, INK, PAPER2, RULE, KR, MONO, PAPER


def _kr(txt):
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


W, H = 880, 600
d = SeqKR(W, H, "LEARNING COREDNS · 06-01 §6",
          "SRV 한 번이 A 조회까지 끝낸다",
          "SRV 응답의 ADDITIONAL 구간이 대상 이름의 A 레코드를 함께 싣는다. "
          "엔드포인트가 넷이면 뒤따랐을 A 질의 넷이 통째로 사라진다.",
          "붉은 점선이 이 설계가 없앤 왕복입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("파드 안 클라이언트", "dnstools"),
         ("클러스터 DNS", "CoreDNS")], y0=104, lane_w=300)
d.rails(408)

d.msg("파드 안 클라이언트", "클러스터 DNS", "SRV 질의 한 번", 192, MUTED,
      sub="_http._tcp.headless.default.svc.cluster.local")
d.msg("클러스터 DNS", "파드 안 클라이언트", "응답 한 통 · ANSWER 구간", 252, MUTED,
      sub="SRV 넷 — 0 25 80 <대상 이름>")
d.msg("클러스터 DNS", "파드 안 클라이언트", "같은 응답 · ADDITIONAL 구간", 316, ACC, mk="acc",
      sub="A 넷 — 대상 이름의 주소")
d.msg("파드 안 클라이언트", "클러스터 DNS", "없었다면 A 질의 넷", 384, BAD, mk="bad", dash="5 4")

chip("파드 안 클라이언트", "추가 조회 없이 접속", 452, OK)

d.t(20, 496, "SRV 는 대상 이름만 주므로 원래대로면 이름마다 A 를 한 번 더 물어야 한다", 13, MUTED, KR, "start")
d.t(20, 520, "ADDITIONAL 이 그 답을 미리 실어 보내 왕복이 하나로 끝난다", 13, MUTED, KR, "start")

d.legend(544, [("같은 응답에 실려 오는 것", ACC), ("이 설계가 없앤 왕복", BAD), ("클라이언트가 도달한 상태", OK)])
d.save("06-01.srv-additional.svg")
