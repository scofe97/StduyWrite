# 05-01 §3 — 등록은 API 로 즉시 끝나지만 클라이언트는 TTL 이 만료될 때까지 옛 주소를 쓴다.
# 원문 근거: "Even with this dynamic, API-based registration, clients do not find out about service
#            location changes. They must still rely on a TTL and requery the service discovery to find
#            out whether a service has moved" / "DNS does not provide any push-based functionality today."
# 타입 스펙: type-sequence — 주체 셋 사이의 시간순 왕복이고, 가운데의 빈 구간이 논지다.
#           프리미티브의 mono 하드코딩을 SeqKR 로 덮는다(계약 §프리미티브가 한글을 mono 로 내보내는 자리).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, OK, INK, PAPER2, RULE, KR, MONO, PAPER


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


W, H = 880, 616
d = SeqKR(W, H, "LEARNING COREDNS · 05-01 §3",
          "등록은 즉시, 조회는 TTL 이 끝나야",
          "새 인스턴스는 API 한 번으로 레지스트리에 실린다. 그 사실이 클라이언트에 닿는 경로가 없어서, "
          "클라이언트는 캐시의 TTL 이 만료될 때까지 옛 주소를 계속 쓴다.",
          "붉은 점선이 DNS 에 없는 경로입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("서비스 인스턴스", "self-register"),
         ("레지스트리와 DNS", "registry · dns"),
         ("클라이언트", "resolver cache")], y0=104, lane_w=248)
d.rails(452)

d.msg("서비스 인스턴스", "레지스트리와 DNS", "등록 API 호출", 196, MUTED, sub="자기 이름과 위치를 알린다")
chip("레지스트리와 DNS", "새 주소를 안다", 252, OK)
d.msg("레지스트리와 DNS", "클라이언트", "밀어 줄 경로가 없다", 312, BAD, mk="bad", dash="5 4")
chip("클라이언트", "옛 주소를 계속 쓴다", 372, BAD)
d.msg("클라이언트", "레지스트리와 DNS", "TTL 만료 후 재질의", 428, ACC, mk="acc")

d.t(20, 492, "이 공백을 없애려고 Consul 같은 제품은 DNS 밖에 별도 프로토콜을 얹는다", 13, MUTED, KR, "start")
d.t(20, 516, "CoreDNS 는 gRPC 의 푸시로 같은 것을 실험했지만 현재 버전에는 그 기능이 없다", 13, MUTED, KR, "start")

d.legend(544, [("레지스트리가 아는 시점", OK), ("DNS 에 없는 경로", BAD), ("클라이언트가 아는 시점", ACC)])
d.save("05-01.push-gap.svg")
