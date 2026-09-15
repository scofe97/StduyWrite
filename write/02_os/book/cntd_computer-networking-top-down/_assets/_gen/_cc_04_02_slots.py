# 04-02 §1·§2 공용 골격 — 슬롯마다 "도착 → 패브릭 통과 → 큐에 남음" 을 한 칸에 담아 세 슬롯을 가로로 편다.
# 왼쪽에 입력 포트 셋, 슬롯 칸마다 통과분(초록)과 잔류분(노랑)을 패킷 단위로 세워, 줄이 자라는 것이 눈에 보이게 한다.
# 두 장이 같은 stride·여백을 쓰도록 좌표를 여기 한 곳에 둔다. 달라지는 것은 슬롯당 통과 개수뿐이다.
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 396

IN_X, IN_W, IN_H = 16, 132, 40      # 입력 포트 상자 셋
IN_Y0, IN_STRIDE = 150, 52

SX, SW, SGAP = 196, 208, 20         # 슬롯 칸
SY, SH = 126, 196
SLOTS = 3

OUT_X, OUT_W = 892, 96              # 출력 링크 — 슬롯 3 칸(끝 860)과 32px 띄운다
OUT_Y, OUT_H = 190, 64

PW, PH, PGAP = 24, 20, 5            # 패킷 한 개
LEGEND_Y = H - 44


def slot_x(i):
    return SX + (SW + SGAP) * i


def frame(title, lead, desc):
    """입력 포트 셋 · 슬롯 칸 셋 · 출력 링크까지 그린 캔버스."""
    d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-02 §1-2", title, desc, lead)

    # 입력 포트
    d.t(IN_X, IN_Y0 - 26, "입력 포트", 13, SOFT, KR, "start", 600)
    for k in range(3):
        y = IN_Y0 + IN_STRIDE * k
        d.box(IN_X, y, IN_W, IN_H, PAPER2, RULE, 1.0, 6)
        d.t(IN_X + IN_W / 2, y + 25, f"입력 {k + 1}", 13, INK, KR, "middle", 600)
    d.t(IN_X + IN_W / 2, IN_Y0 + IN_STRIDE * 3 + 18, "슬롯마다 1개씩", 13, SOFT, KR)

    # 입력 → 첫 슬롯
    my = IN_Y0 + IN_STRIDE + IN_H / 2
    d.path(f"M {IN_X + IN_W + 4} {my} L {SX - 8} {my}", MUTED, 1.3, m="ar")

    # 슬롯 칸
    for i in range(SLOTS):
        x = slot_x(i)
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 6)
        d.t(x + SW / 2, SY - 12, f"슬롯 {i + 1}", 13, MUTED, KR, "middle", 600)
        if i:
            d.path(f"M {x - SGAP + 4} {SY + SH / 2} L {x - 6} {SY + SH / 2}", MUTED, 1.2, m="ar")

    # 출력 링크
    d.tone(OUT_X, OUT_Y, OUT_W, OUT_H, ACC, 6, "14", 1.4)
    d.t(OUT_X + OUT_W / 2, OUT_Y + 28, "출력", 14, ACC, KR, "middle", 600)
    d.t(OUT_X + OUT_W / 2, OUT_Y + 48, "R_line", 12, SOFT, MONO)
    return d


def _row(d, x, y, n, c, per=4, rows=2):
    """패킷 n 개를 가로로 편다. per 개마다 줄을 바꾼다.

    2026-09-14: 한 줄에 다 펴고 넘치면 `+N` 을 붙이던 방식이 슬롯 3 에서 깨졌다.
    잔류 6 개는 `cap=4` 로 접어도 4 개(끝 x=840) + `+2` 가 출력 상자(x=872)를
    파고들었다. 개수가 곧 논지라 개수를 줄일 수는 없으므로 **아래로 접는다.**
    dd-lint 는 이 겹침을 못 잡는다 — text-* 규칙은 글자만 보는데 여기 겹친 것은
    d.tone 으로 그린 도형이다."""
    shown = min(n, per * rows)
    for i in range(shown):
        r, c_i = divmod(i, per)
        d.tone(x + c_i * (PW + PGAP), y + r * (PH + 4), PW, PH, c, 3, "22", 1.1)
    if n > shown:
        r, c_i = divmod(shown, per)
        d.t(x + c_i * (PW + PGAP) + 4, y + r * (PH + 4) + 15,
            f"+{n - shown}", 12, c, MONO, "start", 600)


def slot(d, i, crossed, left, focal=False):
    """슬롯 i 의 장면 — 도착 3개 · 패브릭 통과 crossed 개 · 큐에 남은 left 개."""
    x = slot_x(i) + 14
    inner = SW - 28

    d.t(x, SY + 26, "도착", 13, SOFT, KR, "start")
    _row(d, x + 42, SY + 12, 3, MUTED)

    d.t(x, SY + 74, "통과", 13, OK, KR, "start")
    _row(d, x + 42, SY + 60, crossed, OK)

    cq = ACC if focal else WARN
    d.t(x, SY + 122, "잔류", 12, cq, KR, "start")
    if left == 0:
        d.t(x + 42, SY + 122, "없음", 13, OK, KR, "start", 600)
    else:
        _row(d, x + 42, SY + 104, left, cq)

    # 슬롯이 끝난 뒤 큐 합계
    by = SY + SH - 40
    if focal:
        d.tone(x - 6, by, inner + 12, 32, ACC, 5, "14", 1.4)
    else:
        d.line(x - 6, by - 4, x + inner + 6, by - 4, RULE, 0.8)
    d.t(x + inner / 2, by + 21, f"큐 합계 {left} 개", 13, ACC if focal else cq, KR, "middle", 600)


def out_arrow(d, i, c=OK):
    """슬롯 i 의 통과분이 출력으로 나가는 화살표 — 슬롯 오른쪽에서 출력 왼쪽으로 수평."""
    y = OUT_Y + OUT_H / 2
    d.path(f"M {slot_x(i) + SW + 6} {y} L {OUT_X - 4} {y}", c, 1.4, m="ok")
