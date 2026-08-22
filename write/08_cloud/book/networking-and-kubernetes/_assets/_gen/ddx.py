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


def textw_tight(txt, size):
    """마스크·배경 박스를 텍스트에 바짝 붙일 때 쓰는 실측 근사.
    fit() 의 textw 는 일부러 넉넉하게(넘침을 못 잡느니 헛경보가 낫다) 잡지만,
    마스크에 그 값을 쓰면 띠가 글자보다 한참 길어져 테두리를 과하게 끊는다."""
    w = 0.0
    for c in str(txt):
        if c == ' ': w += size * 0.30
        elif '가' <= c <= '힣' or 'ㄱ' <= c <= 'ㆎ': w += size * 1.0
        else: w += size * 0.56
    return w

def ring_label(d, x, y, txt, size=11, c=None, off=24):
    """type-nested — 링 라벨은 paper 마스크를 테두리 위에 얹고 그 위에 쓴다."""
    from dd import PAPER, ACC
    c = c or ACC
    w = textw_tight(txt, size) + 20
    d.o.append(f'<rect x="{x+off}" y="{y-9}" width="{w:.0f}" height="18" fill="{PAPER}"/>')
    d.t(x + off + 10, y + 4, txt, size, c, KR, "start", 600)


def bracket(d, x, y0, y1, label, c=None, w=10, size=11):
    """가시 범위를 표시하는 대괄호. 오른쪽으로 열린다."""
    from dd import MUTED
    c = c or MUTED
    d.path(f"M {x+w} {y0} L {x} {y0} L {x} {y1} L {x+w} {y1}", c, 1.2)
    d.line(x, (y0 + y1) / 2, x + w + 6, (y0 + y1) / 2, c, 1.2)
    d.t(x + w + 12, (y0 + y1) / 2 + 4, label, size, c, KR, "start")


def lane_pair(d, CX, top_cy, bot_cy, bw, bh, top_label, bot_label,
              top_cells, bot_cells, links, top_c=None, bot_c=None,
              top_mono=False, x0=40, x1=960, sizes=(13, 11, 10)):
    """레인 둘 — 가로는 순서, 세로는 대응. 02 장이 반복해 쓰는 형태.
    top_cells/bot_cells 는 (제목, 부제, 꼬리표) 세 쪽. links 는 세로 화살표 라벨."""
    from dd import INFO, ACC
    top_c = top_c or INFO; bot_c = bot_c or ACC
    ts, ss, gs = sizes
    for cy, lab, c in ((top_cy, top_label, top_c), (bot_cy, bot_label, bot_c)):
        y0 = cy - bh // 2 - 26
        d.o.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{bh+38}" rx="8" '
                   f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
        ring_label(d, x0, y0, lab, 11, c, off=16)

    def cell(cx, cy, t, s, tag, c, mono):
        d.box(cx - bw // 2, cy - bh // 2, bw, bh, PAPER2, c, 1.1, 6)
        d.t(cx, cy - 20, fit(t, ts, bw - 16, t), ts, c,
            MONO if mono else KR, "middle", 600)
        d.t(cx, cy + 2, fit(s, ss, bw - 14, s), ss, MUTED,
            MONO if all(ord(ch) < 128 or ch in '·' for ch in s) else KR)
        d.t(cx, cy + 26, fit(tag, gs, bw - 12, tag), gs, SOFT,
            MONO if all(ord(ch) < 128 or ch in '·:' for ch in tag) else KR)

    for cx, c in zip(CX, top_cells): cell(cx, top_cy, *c, top_c, top_mono)
    for cx, b in zip(CX, bot_cells): cell(cx, bot_cy, *b, bot_c, False)
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+bw//2+6} {top_cy} L {b-bw//2-10} {top_cy}", MUTED, 1.4, m="ar")
    for cx, lab in zip(CX, links):
        d.path(f"M {cx} {top_cy+bh//2+6} L {cx} {bot_cy-bh//2-10}", bot_c, 1.5, m="acc")
        # 중간 높이에 두면 아래 레인의 라벨 마스크와 겹친다 — 위 레인 바로 밑에 붙인다
        if lab: d.t(cx + 12, top_cy + bh // 2 + 22, lab, 11, bot_c, KR, "start")


def stage_chain(d, cy, stages, nodes, edges, bw=190, gap=60, x0=30,
                stage_y=None, sizes=(14, 11, 10)):
    """단계 머리 + 한 줄 체인. 각 장 chapter-overview 가 반복해 쓰는 형태.
    nodes 는 (제목, 부제, 꼬리표, 색|None|ACC). ACC 면 focal 로 그린다.
    코리도어 라벨은 실제 코리도어 폭으로 fit 한다 — 넉넉한 값을 넘기면 가드가 통과시킨다."""
    from dd import INK, ACC, PAPER2, RULE
    n = len(nodes); bh = 116
    CX = [x0 + bw // 2 + i * (bw + gap) for i in range(n)]
    ts, ss, gs = sizes
    if stage_y is None: stage_y = cy - bh // 2 - 42
    for cx, s in zip(CX, stages):
        d.t(cx, stage_y, s, 12, SOFT, KR, "middle", 600)
    for cx, (t, sub, tag, c) in zip(CX, nodes):
        x, y = cx - bw // 2, cy - bh // 2
        if c is ACC:
            d.o.append(f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="6" '
                       f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
        else:
            d.box(x, y, bw, bh, PAPER2, c or RULE, 1.1, 6); tc = c or INK
        d.t(cx, cy - 24, fit(t, ts, bw - 18, t), ts, tc, KR, "middle", 600)
        d.t(cx, cy + 2, fit(sub, ss, bw - 16, sub), ss, MUTED,
            MONO if all(ord(ch) < 128 or ch in '·→' for ch in sub) else KR)
        d.t(cx, cy + 30, fit(tag, gs, bw - 14, tag), gs, SOFT,
            MONO if all(ord(ch) < 128 or ch in '·' for ch in tag) else KR)
    for i, lab in enumerate(edges):
        a, b = CX[i] + bw // 2, CX[i + 1] - bw // 2
        d.path(f"M {a+6} {cy} L {b-10} {cy}", MUTED, 1.5, m="ar")
        # textw 는 일부러 넉넉히 잡으므로 여유를 4px 만 둔다 (6px 이면 정상 라벨도 걸린다)
        d.t((a + b) // 2, cy - 16, fit(lab, 11, gap - 4, f"corridor {lab}"), 11, MUTED, KR)
    return CX


def matrix(d, x0, cols, rows, hdr_y, row_h=84, gap=12, focal_col=None, sizes=(13, 11)):
    """행렬 — 행은 항목, 열은 축. 값이 몇 줄뿐이어도 행렬은 행렬로 그린다.
    cols 는 (폭, 머리글). rows 는 (셀 목록, 행 색). 셀은 (윗줄, 아랫줄) 또는 (한 줄,).
    focal_col 열은 행 색으로 칠해 그 열이 판정 축임을 드러낸다."""
    from dd import INK, PAPER, PAPER2, RULE
    ts, ss = sizes
    XS, x = [], x0
    for w, name in cols:
        XS.append((x, w))
        d.t(x + w // 2, hdr_y, name, 11, SOFT, KR, "middle", 600)
        x += w + gap
    for r, (cells, rc) in enumerate(rows):
        y = hdr_y + 24 + r * (row_h + gap)
        for i, (cx0, cw) in enumerate(XS):
            hit = (i == focal_col)
            d.o.append(f'<rect x="{cx0}" y="{y}" width="{cw}" height="{row_h}" rx="6" '
                       f'fill="{rc+"12" if hit else PAPER2}" stroke="{rc if hit else RULE}" '
                       f'stroke-width="{1.4 if hit else 1.1}"/>')
            cell = cells[i]
            if len(cell) == 1:
                d.t(cx0 + cw // 2, y + row_h // 2 + 6, cell[0], 15, rc if hit else INK, KR, "middle", 600)
            else:
                d.t(cx0 + 20, y + 34, fit(cell[0], ts, cw - 40, cell[0]), ts,
                    rc if hit else INK,
                    MONO if all(ord(ch) < 128 for ch in cell[0]) else KR, "start", 600)
                d.t(cx0 + 20, y + 58, fit(cell[1], ss, cw - 40, cell[1]), ss, MUTED,
                    MONO if all(ord(ch) < 128 for ch in cell[1]) else KR, "start")
    return XS


def elbow(x1, y1, x2, y2):
    """가로 중간에서 한 번 꺾는 직각 경로. 통로를 혼자 쓰는 연결선에만 쓴다 —
    한 점에서 여러 갈래가 뻗으면 세로 구간이 겹치므로 줄기를 세워야 한다."""
    xb = (x1 + x2) // 2
    return f"M {x1} {y1} L {xb} {y1} L {xb} {y2} L {x2} {y2}"
