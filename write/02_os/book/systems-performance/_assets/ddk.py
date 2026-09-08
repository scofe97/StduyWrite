"""이 책 폴더 공용 확장 — dd.py 는 폴더마다 사본이 갈리므로 고치지 않고(계약) 여기서 감싼다.
lead·legend 의 한글이 dd.py 에서 11px 하드코딩이라 본문 삽입 폭에서 1.3% 미달로 뭉갠다."""
from dd import D, esc, SOFT, MUTED, RULE, KR, MONO

class DK(D):
    def __init__(s, w, h, eyebrow, title, desc, lead=None):
        super().__init__(w, h, eyebrow, title, desc, None)
        if lead:
            s.o.append(f'<text x="12" y="74" font-family="{KR}" font-size="13" fill="{MUTED}">{esc(lead)}</text>')
    def legend(s, y, items):
        s.line(12, y, s.w - 48, y, RULE, 0.8)
        s.t(12, y + 22, "LEGEND", 8, SOFT, MONO, "start")
        x = 100
        for lab, c in items:
            s.o.append(f'<rect x="{x}" y="{y + 11}" width="14" height="14" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
            s.t(x + 22, y + 23, lab, 13, MUTED, KR, "start")
            x += 48 + len(lab) * 15
