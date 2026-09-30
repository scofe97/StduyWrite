# gonet-lab 도식 공용 도우미 — dd.py 프리미티브 위에 한글 폰트 분기와 노드·화살표 모양만 얹는다.
from dd import D, Seq, INK, MUTED, SOFT, RULE, PAPER2, KR, MONO


def kr(t):
    return KR if any("가" <= c <= "힣" for c in str(t)) else MONO


def node(d, x, y, w, h, title, sub=None, c=None, focal=False, size=14):
    """상자 하나. c 가 있으면 상태색 톤, focal 이면 테두리를 굵게."""
    if c:
        d.tone(x, y, w, h, c, 6, "14" if focal else "10", 1.6 if focal else 1.0)
    else:
        d.box(x, y, w, h)
    fill = c or INK
    cx = x + w / 2
    if sub:
        d.t(cx, y + h / 2 - 3, title, size, fill, kr(title), "middle", 600)
        d.t(cx, y + h / 2 + 16, sub, 12, MUTED, kr(sub), "middle")
    else:
        d.t(cx, y + h / 2 + 5, title, size, fill, kr(title), "middle", 600)


def harrow(d, x1, x2, y, c=SOFT, m="soft", label=None, lc=None):
    d.arrow([(x1, y), (x2, y)], c, m, 1.3)
    if label:
        d.t((x1 + x2) / 2, y - 8, label, 12, lc or MUTED, kr(label), "middle")


def varrow(d, x, y1, y2, c=SOFT, m="soft", label=None, lc=None):
    d.arrow([(x, y1), (x, y2)], c, m, 1.3)
    if label:
        d.t(x + 8, (y1 + y2) / 2 + 4, label, 12, lc or MUTED, kr(label), "start")


class SeqKR(Seq):
    """Seq 의 라벨 폰트를 한글이면 한글 스택으로 갈라 쓴다(계약 §프리미티브가 한글을 mono 로 내보내는 자리)."""
    def lanes(s, names, y0=104, lane_w=210):
        LX = Seq.lanes(s, [(n, "") for n, _ in names], y0, lane_w)
        for n, sub in names:
            s.t(LX[n], y0 + 37, sub, 11, MUTED, kr(sub))
        return LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        dr = 1 if x2 > x1 else -1
        s.path(f"M {x1+10*dr} {y} L {x2-12*dr} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 9, label, 13, c, kr(label), "middle", 600)
        if sub:
            s.t(mx, y + 19, sub, 12, MUTED, kr(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x+10} {y-10} L {x+52} {y-10} L {x+52} {y+10} L {x+13} {y+10}", c, 1.4, m="ar")
        s.t(x + 62, y - 2, label, 13, c, kr(label), "start", 600)
        if sub:
            s.t(x + 62, y + 16, sub, 12, MUTED, kr(sub), "start")
