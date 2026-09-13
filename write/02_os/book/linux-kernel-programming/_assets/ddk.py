"""이 책 폴더 공용 확장 — dd.py 는 폴더마다 사본이 갈리므로 고치지 않고(계약) 여기서 감싼다.

두 가지를 고친다.
1. lead·legend·chip 의 한글이 dd.py 에서 11px 하드코딩이라 본문 삽입 폭에서 1.3% 미달로 뭉갠다.
2. Seq.msg·Seq.state·Seq.lanes 가 font-family 를 MONO 로 하드코딩해, 한글을 넘기면 자간이 벌어진다.
   제품명·명령·경로·수치는 그대로 mono 로 두고 한글일 때만 KR 로 갈라 쓴다.
"""
from dd import D, Seq, esc, SOFT, MUTED, INK, RULE, PAPER, KR, MONO


def kfont(txt):
    """한글이 섞였으면 KR, 아니면 MONO. 제품명·수치는 mono 를 유지한다."""
    return KR if any("가" <= c <= "힣" for c in str(txt)) else MONO


class DK(D):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, None)
        if lead:
            s.o.append(f'<text x="12" y="76" font-family="{KR}" font-size="13" fill="{MUTED}">{esc(lead)}</text>')

    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 100
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y + 11}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 22, y + 23, lab, 13, MUTED, KR, "start")
            x += 48 + len(lab) * 15

    def chip(s, cx, cy, txt, c=MUTED, size=13, pad=8):
        kr = any("가" <= ch <= "힣" for ch in str(txt))
        w = len(str(txt)) * (size * 1.0 if kr else size * 0.62) + pad * 2
        s.o.append(f'<rect x="{cx - w / 2}" y="{cy - 11}" width="{w}" height="22" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.8"/>')
        s.t(cx, cy + 5, txt, size, c, KR if kr else MONO)


class SeqK(Seq, DK):
    """DK 의 lead·legend·chip 과 Seq 의 레인·메시지를 합치고, 한글 라벨의 폰트를 갈라 쓴다."""

    def lanes(s, names, y0=104, lane_w=210):
        s.LX = {}
        n = len(names)
        span = (s.w - 48 - 24) - lane_w
        for i, (nm, sub) in enumerate(names):
            x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
            s.LX[nm] = x
            s.box(x - lane_w / 2, y0, lane_w, 48, "#161B22", RULE, 1.0)
            s.t(x, y0 + 21, nm, 13, INK, KR, "middle", 600)
            s.t(x, y0 + 40, sub, 12, MUTED, kfont(sub))
        s.lane_top = y0 + 48
        return s.LX

    def msg(s, a, b, label, y, c=MUTED, mk="ar", dash=None, sub=None):
        x1, x2 = s.LX[a], s.LX[b]
        d = 1 if x2 > x1 else -1
        s.path(f"M {x1 + 10 * d} {y} L {x2 - 12 * d} {y}", c, 1.5, m=mk, dash=dash)
        mx = (x1 + x2) / 2
        s.t(mx, y - 10, label, 13, c, kfont(label), "middle", 600)
        if sub:
            s.t(mx, y + 19, sub, 13, MUTED, kfont(sub))

    def selfmsg(s, a, label, y, c=MUTED, sub=None):
        x = s.LX[a]
        s.path(f"M {x + 10} {y - 12} L {x + 62} {y - 12} L {x + 62} {y + 12} L {x + 13} {y + 12}", c, 1.4, m="ar")
        s.t(x + 72, y - 5, label, 13, c, kfont(label), "start")
        if sub:
            s.t(x + 72, y + 15, sub, 13, MUTED, KR, "start")

    def state(s, a, txt, y, c):
        x = s.LX[a]
        kr = any("가" <= ch <= "힣" for ch in str(txt))
        w = len(str(txt)) * (13.0 if kr else 8.0) + 20
        s.o.append(f'<rect x="{x - w / 2}" y="{y - 11}" width="{w}" height="22" rx="4" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
        s.t(x, y + 5, txt, 13, c, KR if kr else MONO)
