"""01-03 장 공용 헬퍼 — dd.py 프리미티브 위에 이 장이 반복해 쓰는 형태만 얹는다.
좌표는 넘기는 쪽에서 공식으로 산출한다. 여기서는 그리기만 한다."""
from dd import INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

BAND_X, BAND_W = 24, 952

def band(d, y0, y1, label, x=BAND_X, w=BAND_W, focal=False):
    """focal=True 면 왼쪽 모서리에 accent 막대를 세운다 — 도식당 한 곳만."""
    d.box(x, y0, w, y1 - y0, PAPER2, RULE, 0.9, 8)
    if focal:
        d.o.append(f'<rect x="{x}" y="{y0}" width="4" height="{y1-y0}" rx="2" fill="{ACC}"/>')
    d.t(x + 14, y0 + 20, label, 12, ACC if focal else SOFT, KR, "start")

def node(d, cx, cy, title, sub, w=112, h=56, c=None, focal=False, dim=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc, sc = ACC, ACC
    elif dim:
        d.box(x, y, w, h, PAPER, RULE, 0.8, 6)
        tc, sc = SOFT, SOFT
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6)
        tc, sc = (c or INK), MUTED
    d.t(cx, cy - 2, title, 12, tc, KR, "middle", 600)
    if sub: d.t(cx, cy + 16, sub, 11, sc, KR)

def hop(d, cx1, cx2, y, c=MUTED, mk="ar", dash=None, half=56, gap=8):
    d.path(f"M {cx1+half+gap} {y} L {cx2-half-gap-2} {y}", c, 1.5, m=mk, dash=dash)

def tag(d, cx, cy, txt, c, w):
    """상태색 라운드 라벨 — chip 보다 크고 한글 12px 이 들어간다."""
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-13}" width="{w}" height="26" rx="5" '
               f'fill="{c}14" stroke="{c}" stroke-width="1.0"/>')
    d.t(cx, cy + 4, txt, 12, c, KR)

def focal_tag(d, cx, cy, txt, w):
    d.o.append(f'<rect x="{cx-w/2}" y="{cy-14}" width="{w}" height="28" rx="6" '
               f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    d.t(cx, cy + 5, txt, 12, ACC, KR)


def textw(txt, size, mono=False):
    """전각 1em · 라틴 0.62em 예산. dd.chip 과 같은 계산."""
    return sum(size * (1.0 if '가' <= c <= '힣' or 'ㄱ' <= c <= 'ㆎ' else 0.62)
               for c in str(txt))

def fit(txt, size, avail, where=""):
    """박스 안쪽 넘침을 기계로 잡는다 — overflow-check.py 는 viewBox 밖만 본다."""
    w = textw(txt, size)
    if w > avail:
        raise AssertionError(f"박스 넘침 {where}: '{txt}' 추정 {w:.0f}px > 가용 {avail}px")
    return txt


def lanes(d, names, y0=104, lane_w=212):
    """Seq.lanes 와 같은 배치. 다만 부제 글꼴을 내용으로 고른다 —
    한글 서술을 mono 로 찍으면 자간이 벌어져 읽기 나빠진다(스타일 계약 타이포그래피)."""
    d.LX = {}; n = len(names)
    span = (d.w - 48 - 24) - lane_w
    for i, (nm, sub) in enumerate(names):
        x = 24 + lane_w / 2 + (span * i / (n - 1) if n > 1 else 0)
        d.LX[nm] = x
        d.box(x - lane_w / 2, y0, lane_w, 44, PAPER2, RULE, 1.0)
        d.t(x, y0 + 20, nm, 12, INK, KR, "middle", 600)
        ascii_only = all(ord(c) < 128 for c in sub)
        d.t(x, y0 + 37, sub, 9 if ascii_only else 11, MUTED, MONO if ascii_only else KR)
    d.lane_top = y0 + 44
    return d.LX
