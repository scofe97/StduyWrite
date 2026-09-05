# 06-02 §3 — 파드 하나의 상태 변화가 Endpoints 객체 전체 전송을 부른다.
# 원문 근거: "a single Endpoints resource contains all of the endpoint addresses, both ready and not,
#            for a single service" / "watch will send the resource data whenever the resource changes.
#            For Endpoints, this means that every time a pod for the specific service is create,
#            destroyed, or transitions between ready and not ready, the entire Endpoints object will
#            be sent." / "larger Endpoints are sent to watchers more often than smaller Endpoints" /
#            규모는 "very large services containing several thousand backends" 로만 적혀 있어
#            구체적인 수를 지어내지 않고 "수천" 으로 둔다.
# 타입 스펙: type-sequence — 세 주체 사이의 시간순 전달이고, 되풀이되는 전체 전송이 논지다.
#           프리미티브의 mono 하드코딩을 SeqKR 로 덮는다(계약 §프리미티브가 한글을 mono 로 내보내는 자리).
import sys; sys.path.insert(0, ".")
from dd import Seq, ACC, MUTED, BAD, WARN, INK, PAPER2, RULE, KR, MONO, PAPER


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


W, H = 880, 620
d = SeqKR(W, H, "LEARNING COREDNS · 06-02 §3",
          "하나가 바뀌면 객체가 통째로 온다",
          "Endpoints 자원 하나가 서비스 하나의 주소를 준비 여부와 무관하게 전부 담는다. "
          "그 안의 파드가 하나만 바뀌어도 watch 는 객체 전체를 다시 보낸다.",
          "붉은 화살표 하나가 객체 전체입니다")


# dd.state 는 상자 폭을 ASCII 기준(len*7px)으로 잡아 한글(11px)이 상자를 넘치고,
# 채움이 반투명이라 레인 점선이 글자 사이로 비친다. 이 책에서는 아래로 대신한다.
def chip(a, txt, y, c):
    x = d.LX[a]
    w = sum(11.0 if "\uac00" <= ch <= "\ud7a3" else 6.6 for ch in txt) + 20
    for f, st, sw in ((PAPER, "none", 0), (c + "22", c, 1.1)):
        d.o.append(f'<rect x="{x - w / 2}" y="{y - 10}" width="{w}" height="20" rx="4" '
                   f'fill="{f}" stroke="{st}" stroke-width="{sw}"/>')
    d.t(x, y + 4, txt, 11, c, KR)


d.lanes([("백엔드 파드 하나", "backend #1"),
         ("Endpoints 컨트롤러", "endpoints"),
         ("CoreDNS", "kubernetes plugin")], y0=104, lane_w=240)
d.rails(444)

d.msg("백엔드 파드 하나", "Endpoints 컨트롤러", "ready 로 바뀜", 196, MUTED, sub="주소 하나의 상태만 달라졌다")
chip("Endpoints 컨트롤러", "객체를 다시 쓴다", 252, WARN)
d.msg("Endpoints 컨트롤러", "CoreDNS", "수천 개 주소 전부", 312, BAD, mk="bad",
      sub="바뀐 하나가 아니라 객체 전체")
d.msg("백엔드 파드 하나", "Endpoints 컨트롤러", "다른 파드가 또 바뀜", 380, MUTED, dash="5 4",
      sub="백엔드가 많을수록 이 일이 잦다")
chip("CoreDNS", "메모리와 CPU 를 더 쓴다", 424, BAD)

d.t(20, 488, "객체가 커지는 축과 자주 바뀌는 축이 같은 방향으로 나빠져서 큰 서비스일수록 비용이 겹쳐 는다", 13, MUTED, KR, "start")
d.t(20, 512, "헤드리스를 아무도 안 쓰면 noendpoints 로 이 watch 자체를 끌 수 있다", 13, MUTED, KR, "start")

d.legend(540, [("컨트롤러가 다시 쓰는 지점", WARN), ("전체가 전송되는 경로", BAD)])
d.save("06-02.endpoints-watch.svg")
