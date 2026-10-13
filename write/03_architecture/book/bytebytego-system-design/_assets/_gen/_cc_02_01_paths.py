# 02-01 의 읽기·쓰기 경로 두 장이 함께 쓰는 격자 골격. 좌표는 여기 한 곳에 두고 행 데이터만 장마다 넘긴다.
# 타입 스펙은 호출하는 생성기가 적는다(type-dp-security-matrix §2 공식: left_pad 12, header_h 36, row_h 48, stride 56).
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER2, RULE, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP = 12, 176, 12, 128, 12
HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 96, 36, 144, 48, 56
NSTEP = 5
ACTOR = {"앱": INFO, "캐시": OK, "DB": MUTED}


def col_x(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)


def build(eyebrow, title, lead, rows, focal, focal_label, out):
    """rows: [(이름, 부제, [(주체, 연산) | None × 5])], focal: (행, 열)."""
    w = LEFT + COMP_W + GAP0 + NSTEP * ROLE_W + (NSTEP - 1) * ROLE_GAP + 48
    h = ROW0 + (len(rows) - 1) * STRIDE + ROW_H + 20 + 44
    d = D(w, h, eyebrow, title, lead, lead)
    d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
    d.t(LEFT + COMP_W / 2, HDR_Y + 23, "전략 × 순서", 12, INK, KR, "middle", 600)
    for j in range(NSTEP):
        d.box(col_x(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
        d.t(col_x(j) + ROLE_W / 2, HDR_Y + 23, str(j + 1), 13, INK, MONO, "middle", 600)
    for i, (name, sub, cells) in enumerate(rows):
        y = ROW0 + i * STRIDE
        d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
        d.t(LEFT + 12, y + 20, name, 13, INK, KR, "start", 600)
        d.t(LEFT + 12, y + 38, sub, 12, MUTED, KR, "start")
        for j, cell in enumerate(cells):
            if cell is None:
                continue
            actor, op = cell
            x = col_x(j)
            c = ACC if (i, j) == focal else ACTOR[actor]
            if actor == "DB" and (i, j) != focal:
                d.box(x, y, ROLE_W, ROW_H, PAPER2, RULE, 0.9, 4)
            else:
                d.tone(x, y, ROLE_W, ROW_H, c, 4, "14" if (i, j) == focal else "10", 1.4 if (i, j) == focal else 0.9)
            d.t(x + ROLE_W / 2, y + 20, actor, 12, c, KR, "middle", 600)
            d.t(x + ROLE_W / 2, y + 38, op, 12, INK, MONO, "middle")
    items = [("앱이 실행", INFO), ("캐시가 실행", OK)]
    if any(c and c[0] == "DB" for _, _, cells in rows for c in cells):
        items.append(("DB 가 응답", MUTED))
    d.legend(h - 44, items + [(focal_label, ACC)])
    d.save(out)
