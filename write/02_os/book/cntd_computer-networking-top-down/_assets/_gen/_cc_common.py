# 03-04 §4 세 시나리오 공용 — 위쪽 좁은 띠에 토폴로지, 아래에 type-line 곡선. 여기서 import 만 한다.
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

def host(d, x, y, name, c=INK):
    d.box(x - 22, y - 13, 44, 26, PAPER2, RULE, 0.9, 5)
    d.t(x, y + 4, name, 11, c, MONO, "middle", 600)

def router(d, x, y, name, sub=None, c=MUTED):
    d.o.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{PAPER2}" stroke="{c}" stroke-width="1.1"/>')
    d.t(x, y + 4, name, 10, c, MONO, "middle", 600)
    if sub: d.t(x, y + 32, sub, 11, c, KR)

def fan_in(d, xs, ys, xm, ym, x2):
    """여러 출발점이 x=xm 의 수직 버스로 모여 (x2,ym) 로 들어간다 — 직교 연결."""
    for x, y in zip(xs, ys):
        d.path(f"M {x} {y} L {xm} {y} L {xm} {ym}", MUTED, 1.3)
    d.path(f"M {xm} {ym} L {x2} {ym}", MUTED, 1.3, m="ar")

def fan_out(d, x1, ym, xm, ys, x2):
    """(x1,ym) 에서 x=xm 의 수직 버스로 갈라져 각 y 로 나간다 — 직교 연결."""
    d.path(f"M {x1} {ym} L {xm} {ym}", MUTED, 1.3)
    for y in ys:
        d.path(f"M {xm} {ym} L {xm} {y} L {x2} {y}", MUTED, 1.3, m="ar")

def link(d, x1, y1, x2, y2, c=MUTED, label=None, ly=-8):
    d.path(f"M {x1} {y1} L {x2} {y2}", c, 1.3, m="ar" if c is MUTED else ("acc" if c is ACC else "bad"))
    if label: d.t((x1 + x2) / 2, (y1 + y2) / 2 + ly, label, 11, c, KR)

class Chart:
    """type-line 관례: 여백 left 80 · bottom 60 · top 40 · right 40, 격자 4~6, 초점 계열만 점."""
    def __init__(s, d, x0, y0, w, h, xlab, ylab, xt, yt):
        s.d, s.x0, s.y0, s.w, s.h = d, x0, y0, w, h
        s.L, s.R, s.T, s.B = x0 + 80, x0 + w - 40, y0 + 40, y0 + h - 60
        s.xt, s.yt = xt, yt                      # (값, 라벨) 눈금 — 값은 0..1 정규화
        for v, lab in yt:
            y = s.py(v); d.line(s.L, y, s.R, y, RULE, 0.7, "2 5")
            kr = any("가" <= ch <= "힣" for ch in lab)
            d.t(s.L - 10, y + 4, lab, 11 if kr else 9, MUTED, KR if kr else MONO, "end")
        for v, lab in xt:
            x = s.px(v)
            kr = any("가" <= ch <= "힣" for ch in lab)
            d.t(x, s.B + 18, lab, 11 if kr else 9, MUTED, KR if kr else MONO)
        d.line(s.L, s.B, s.R, s.B, RULE, 1.0); d.line(s.L, s.T, s.L, s.B, RULE, 1.0)
        d.t((s.L + s.R) / 2, s.B + 40, xlab, 11, SOFT, KR)
        d.o.append(f'<text x="{x0 + 22}" y="{(s.T + s.B) / 2}" transform="rotate(-90 {x0 + 22} {(s.T + s.B) / 2})" text-anchor="middle" font-family="{KR}" font-size="11" fill="{SOFT}">{ylab}</text>')
    def px(s, v): return s.L + (s.R - s.L) * v
    def py(s, v): return s.B - (s.B - s.T) * v
    def series(s, pts, c, focal=False, dash=None):
        p = " ".join(f"{s.px(x):.1f},{s.py(y):.1f}" for x, y in pts)
        dd = f' stroke-dasharray="{dash}"' if dash else ""
        s.d.o.append(f'<polyline points="{p}" fill="none" stroke="{c}" stroke-width="{1.8 if focal else 1.2}" stroke-linejoin="round"{dd}/>')
        if focal:
            for x, y in pts: s.d.o.append(f'<circle cx="{s.px(x):.1f}" cy="{s.py(y):.1f}" r="3.5" fill="{c}"/>')
    def note(s, x, y, txt, c=MUTED, anchor="start"): s.d.t(s.px(x), s.py(y), txt, 11, c, KR, anchor)
