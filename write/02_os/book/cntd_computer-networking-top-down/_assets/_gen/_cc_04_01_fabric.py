# 04-01 §5 공용 골격 — 세 스위칭 방식을 같은 무대에서 t1·t2·t3 스냅샷으로 그린다.
# 무대는 셋 다 같다: 왼쪽 입력 포트 셋 · 가운데 패브릭 · 오른쪽 출력 포트 셋.
# 달라지는 것은 "한 스냅샷에 패킷이 몇 개, 어디에 있는가" 뿐이고 그 차이가 곧 세 방식의 논지다.
#
# 04-02 의 _cc_04_02_slots 와 같은 방식이다 — 패킷을 도형으로 두고 개수와 위치로 말한다.
# 상태 이름을 칸에 적지 않는다. 적으면 그림이 아니라 표가 된다.
from dd import D, ACC, MUTED, SOFT, INK, OK, WARN, BAD, INFO, PAPER2, RULE, KR, MONO

W, H = 880, 452

IN_X, IN_W, IN_H = 16, 88, 34       # 입력 포트 셋
OUT_X, OUT_W, OUT_H = 776, 88, 34   # 출력 포트 셋 — 높이는 입력과 같다
PORT_Y0, PORT_STRIDE = 150, 46

FAB_X, FAB_W = 132, 636             # 패브릭 무대 (스냅샷 셋이 이 안에 들어간다)
FAB_Y, FAB_H = 132, 168

PW, PH, PGAP = 26, 18, 5            # 패킷 한 개 — 04-02 와 같은 치수
LEGEND_Y = H - 44

SNAPS = 3
SNAP_W = (FAB_W - 24 * (SNAPS - 1)) / SNAPS


def snap_x(i):
    """스냅샷 i 의 왼쪽 x."""
    return FAB_X + (SNAP_W + 24) * i


def frame(title, lead, desc, fabric_label):
    """입력 포트 셋 · 스냅샷 칸 셋 · 출력 포트 셋까지 그린 무대."""
    d = D(W, H, "COMPUTER NETWORKING TOP-DOWN · 04-01 §5", title, desc, lead)

    for k in range(3):
        y = PORT_Y0 + PORT_STRIDE * k
        d.box(IN_X, y, IN_W, IN_H, PAPER2, RULE, 1.0, 5)
        d.t(IN_X + IN_W / 2, y + 22, f"입력 {k + 1}", 13, INK, KR)
        d.box(OUT_X, y, OUT_W, OUT_H, PAPER2, RULE, 1.0, 5)
        d.t(OUT_X + OUT_W / 2, y + 22, f"출력 {k + 1}", 13, INK, KR)

    d.t(FAB_X + FAB_W / 2, FAB_Y - 18, fabric_label, 13, SOFT, KR)

    for i in range(SNAPS):
        x = snap_x(i)
        d.box(x, FAB_Y, SNAP_W, FAB_H, PAPER2, RULE, 0.9, 5)
        d.t(x + SNAP_W / 2, FAB_Y + FAB_H + 20, f"t{i + 1}", 11, SOFT, MONO)
    return d


def packet(d, x, y, c, tag=None):
    """패킷 한 개. 같은 도형이 스냅샷마다 자리를 옮긴다."""
    d.tone(x, y, PW, PH, c, 3, "22", 1.1)
    if tag:
        d.t(x + PW / 2, y + 13, tag, 10, c, MONO)


def train(d, x, y, n, c, cap=6):
    """패킷 n 개를 가로로 편다 — 개수가 곧 양이다."""
    shown = min(n, cap)
    for i in range(shown):
        packet(d, x + i * (PW + PGAP), y, c)
    if n > cap:
        d.t(x + shown * (PW + PGAP) + 4, y + 13, f"+{n - cap}", 11, c, MONO, "start", 600)


def lane_y(k):
    """입력 k 의 세로 중심 — 패킷이 그 줄을 따라 간다."""
    return PORT_Y0 + PORT_STRIDE * k + (IN_H - PH) / 2


def note(d, i, text, c=SOFT):
    """스냅샷 칸 아래 한 마디. 명사구만 — 종결어미를 쓰지 않는다."""
    d.t(snap_x(i) + SNAP_W / 2, FAB_Y + FAB_H + 40, text, 13, c, KR)
