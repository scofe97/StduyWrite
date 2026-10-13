# 07-03 의 결제 시퀀스 도식이 쓰는 레인·메시지 프리미티브. Seq 가 한글을 mono 로 내보내는 자리를 서브클래스로 고친다.
import sys; sys.path.insert(0, ".")
from dd import Seq, MUTED, INK, PAPER2, RULE, KR, MONO


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
            s.t(x, y0 + 20, nm, 13, INK, _kr(nm), "middle", 600)
            s.t(x, y0 + 37, sub, 13, MUTED, _kr(sub))
        s.lane_top = y0 + 44
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None, sw=1.5, dx=0):
        x1, x2 = s.LX[a], s.LX[b]
        d_ = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d_} {y} L {x2 - 12 * d_} {y}", c, sw, m=mk, dash=dash)
        mx = (x1 + x2) / 2 + dx
        s.t(mx, y - 9, label, 13, c, _kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 17, sub, 13, MUTED, _kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None, left=False):
        x = s.LX[a]
        k = -1 if left else 1
        s.path(f"M {x + 10 * k} {y - 10} L {x + 58 * k} {y - 10} L {x + 58 * k} {y + 10} L {x + 13 * k} {y + 10}", c, 1.4, m="ar")
        s.t(x + 68 * k, y - 2, label, 13, c, _kr(label), "end" if left else "start", 600)
        if sub:
            s.t(x + 68 * k, y + 15, sub, 13, MUTED, _kr(sub), "end" if left else "start")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        kr = any("가" <= ch <= "힣" for ch in txt)
        w = len(txt) * (12.5 if kr else 7.4) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 12}" width="{w}" height="24" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 4, txt, 13, c, _kr(txt), "middle", 600)

    def divider(s, y, txt, c=MUTED):
        s.line(24, y, s.w - 24, y, c, 0.8, "6 5")
        kr = any("가" <= ch <= "힣" for ch in txt)
        w = len(txt) * (12.5 if kr else 7.4) + 24
        s.o.append(f'<rect x="{s.w / 2 - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="#0D1117" stroke="{c}" stroke-width="0.8"/>')
        s.t(s.w / 2, y + 4, txt, 13, c, _kr(txt), "middle")
