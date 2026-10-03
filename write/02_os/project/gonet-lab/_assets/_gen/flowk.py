# 흐름 격자 공용 도우미 — 단계 열(stage) × 경우 행(lane) 격자에 실제 값(바이트·번호·주소)을 채운다.
# 노드 사슬이 아니라 "같은 데이터가 단계마다 어떤 모양으로 바뀌는가"를 보이려는 도식에 쓴다.
# 좌표는 열 수로 폭을 나누는 stride 규칙으로 정한다.
from dd import D, INK, MUTED, SOFT, RULE, MONO, KR
from ddk import harrow

LABEL_W, X0, GAP, HEAD_Y = 118, 24, 26, 104


def _w(txt, size=12):
    return sum(size * (1.0 if "가" <= ch <= "힣" else 0.62) for ch in str(txt)) + 16


def flow_grid(out, eyebrow, title, desc, lead, stages, lanes, arrows=None, legend=None, lane_h=112, W=960, link=True):
    """stages: [(열 제목, 부제)]
    lanes: [(행 이름, 행 부제, [칸마다 (items, 주석, 주석색)])]  items: [(글자, 색 또는 None)]
    arrows: 열 사이 화살표 라벨 [str] (len = 열 수 - 1)
    link: False 면 열 사이 화살표를 그리지 않는다 (열이 단계가 아니라 경우 구분일 때)"""
    n = len(stages)
    cw = (W - X0 * 2 - LABEL_W - GAP * (n - 1)) / n
    top = HEAD_Y + 40
    H = top + lane_h * len(lanes) + (64 if legend else 24)
    d = D(W, H, eyebrow, title, desc, lead=lead)
    xs = [X0 + LABEL_W + k * (cw + GAP) for k in range(n)]
    for x, (t, sub) in zip(xs, stages):
        d.t(x + cw / 2, HEAD_Y + 12, t, 12, INK, KR if any("가" <= c <= "힣" for c in t) else MONO, "middle", 600)
        if sub:
            d.t(x + cw / 2, HEAD_Y + 28, sub, 11, MUTED, KR if any("가" <= c <= "힣" for c in sub) else MONO, "middle")
    for r, (name, sub, cells) in enumerate(lanes):
        y = top + r * lane_h
        d.t(X0, y + 34, name, 13, INK, KR if any("가" <= c <= "힣" for c in name) else MONO, "start", 600)
        if sub:
            d.t(X0, y + 52, sub, 11, MUTED, KR, "start")
        box_h = lane_h - 34
        for k, (x, cell) in enumerate(zip(xs, cells)):
            items, note, note_c = cell
            d.box(x, y, cw, box_h, fill="#11161D", stroke=RULE, sw=0.8)
            ih = 22
            tot = max(0, len(items) * ih + (len(items) - 1) * 4)
            iy = y + (box_h - tot) / 2 - (7 if note else 0)
            for t, c in items:
                fs = 12
                while _w(t, fs) > cw - 8 and fs > 10:
                    fs -= 1
                w = min(_w(t, fs), cw - 6)
                ix = x + (cw - w) / 2
                if c:
                    d.tone(ix, iy, w, ih, c, 4, "14", 1.1)
                else:
                    d.box(ix, iy, w, ih, sw=0.9, r=4)
                d.t(ix + w / 2, iy + 15, t, fs, c or INK, KR if any("가" <= ch <= "힣" for ch in t) else MONO, "middle", 600)
                iy += ih + 4
            if note:
                ny = y + box_h - 8 if items else y + box_h / 2 + 4
                d.t(x + cw / 2, ny, note, 11, note_c or MUTED, KR, "middle")
            if link and k < n - 1:
                harrow(d, x + cw + 3, x + cw + GAP - 3, y + box_h / 2)
    if legend:
        d.legend(H - 40, legend)
    d.save(out)
    return out
