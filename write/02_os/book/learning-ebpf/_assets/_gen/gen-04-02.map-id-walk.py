# 타입 스펙: type-loop — 바깥 고리. 다섯 호출이 start_id 허브를 갱신하며 ENOENT 까지 돈다(허브 하나, 스테이션 다섯, 정확한 원호).
# 사실 출처: 추출본 ebpf4.txt 922~964행(BPF_MAP_GET_NEXT_ID {start_id=0} → BPF_MAP_GET_FD_BY_ID {map_id=48} = 3 → BPF_OBJ_GET_INFO_BY_FD {bpf_fd=3} · start_id=48 → map_id=116 · start_id=133 → -1 ENOENT),
#   linux v7.2 tools/bpf/bpftool/common.c 973~1011행(map_fd_by_name: get_next_id → 읽기 전용 fd → get_info_by_fd → strncmp(name, info.name) → 다르면 close(fd) · ENOENT 면 종료).
# Layout conventions(type-loop §2): 스테이션 다섯, R=200, 스테이션 192×64, 허브 160×84, 중심 (480, 372), 12시에서 시계 방향. 원호는 모두 A R R 0 0 1, 스포크는 반지름 방향. 모든 좌표 4의 배수.
import math
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 660
CX, CY, R = 480, 372, 200
SW, SH = 192, 64
HW, HH = 160, 84
MARK = 1.2   # 화살촉 돌출분(type-loop §2.2)

d = D(W, H, "LEARNING EBPF · 04-02 §4",
      "맵 ID 를 하나씩 넘기며 이름을 비교한다",
      "bpftool 은 start_id 를 넘겨 다음 맵 ID 를 받고, fd 를 열어 이름을 읽어 config 인지 비교하고, 아니면 fd 를 닫아 다음 ID 로 간다. start_id=133 에서 ENOENT 가 오면 끝난다.",
      "ID 마다 fd 열고 이름 비교")

STATIONS = [
    ("BPF_MAP_GET_NEXT_ID", "start_id=0 → 48 → 116", False),
    ("BPF_MAP_GET_FD_BY_ID", "map_id=48 → fd 3", False),
    ("BPF_OBJ_GET_INFO_BY_FD", "bpf_fd=3 · info.name", False),
    ("name == \"config\"?", "다르면 닫고 다음으로", True),
    ("close(fd 3)", "같은 fd 번호를 되씀", False),
]
N = len(STATIONS)


def r4(v):
    return int(round(v / 4.0)) * 4


theta = [math.radians(-90 + k * 360.0 / N) for k in range(N)]
P = [(CX + R * math.cos(t), CY + R * math.sin(t)) for t in theta]
BOX = [(r4(px - SW / 2), r4(py - SH / 2)) for px, py in P]


def circle_hits(bx, by):
    pts = []
    for xe in (bx, bx + SW):
        dx = xe - CX
        if abs(dx) <= R:
            s = math.sqrt(R * R - dx * dx)
            for y in (CY - s, CY + s):
                if by - 1e-6 <= y <= by + SH + 1e-6:
                    pts.append((xe, y))
    for ye in (by, by + SH):
        dy = ye - CY
        if abs(dy) <= R:
            s = math.sqrt(R * R - dy * dy)
            for x in (CX - s, CX + s):
                if bx - 1e-6 <= x <= bx + SW + 1e-6:
                    pts.append((x, ye))
    return pts


def ang(pt):
    return math.atan2(pt[1] - CY, pt[0] - CX)


def split(k):
    """스테이션 k 의 상자와 원이 만나는 점을 (진입, 이탈)로 나눈다."""
    t = theta[k]
    ent = ext = None
    for pt in circle_hits(*BOX[k]):
        dl = (ang(pt) - t + math.pi) % (2 * math.pi) - math.pi
        if dl < 0 and (ent is None or dl > (ang(ent) - t + math.pi) % (2 * math.pi) - math.pi):
            ent = pt
        if dl > 0 and (ext is None or dl < (ang(ext) - t + math.pi) % (2 * math.pi) - math.pi):
            ext = pt
    return ent, ext


HITS = [split(k) for k in range(N)]

# 1) 원호 — 가장 먼저 그려 스테이션 뒤로 보낸다
for k in range(N):
    j = (k + 1) % N
    qx, qy = HITS[k][1]
    ent = HITS[j][0]
    phi = ang(ent) - MARK / R
    ex, ey = CX + R * math.cos(phi), CY + R * math.sin(phi)
    d.path(f"M {qx:.3f} {qy:.3f} A {R} {R} 0 0 1 {ex:.3f} {ey:.3f}", MUTED, 1.2, m="ar")

# 2) 스포크 — start_id 를 갱신하는 스테이션 0 하나만 허브로 되돌린다
def box_dist(ux, uy, a, b):
    ds = []
    if abs(ux) > 1e-9: ds.append(a / abs(ux))
    if abs(uy) > 1e-9: ds.append(b / abs(uy))
    return min(ds)


ux, uy = math.cos(theta[0]), math.sin(theta[0])
ds = box_dist(ux, uy, SW / 2, SH / 2)
dh = box_dist(ux, uy, HW / 2, HH / 2)
sx, sy = P[0][0] - ds * ux, P[0][1] - ds * uy
hx, hy = CX + (dh + 6) * ux, CY + (dh + 6) * uy
d.arrow([(sx, sy), (hx, hy)], SOFT, "soft", 1.2, "5 4")

# 3) 종료 — ENOENT
bx0, by0 = BOX[0]
d.arrow([(bx0 + SW // 2, by0 - 2), (bx0 + SW // 2, by0 - 36)], WARN, "warn", 1.5)
d.chip(bx0 + SW // 2, by0 - 48, "start_id=133 → ENOENT", WARN, 12)

# 4) 스테이션
for k, (title, sub, focal) in enumerate(STATIONS):
    x, y = BOX[k]
    c = ACC if focal else MUTED
    if focal:
        d.tone(x, y, SW, SH, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, SW, SH, PAPER2, MUTED, 1.2, 6)
    kr = any("가" <= ch <= "힣" for ch in title)
    d.t(x + SW / 2, y + 28, title, 13, ACC if focal else INK, KR if kr else MONO, "middle", 600)
    d.t(x + SW / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)

# 5) 허브 — 짙은 요소는 이것 하나
d.box(CX - HW // 2, CY - HH // 2, HW, HH, INK, INK, 1.2, 6)
d.t(CX, CY - 4, "start_id", 14, PAPER, MONO, "middle", 600)
d.t(CX, CY + 18, "0 → 48 → … → 133", 12, PAPER2, MONO)

d.legend(H - 56, [("한 바퀴", MUTED), ("커서 갱신", SOFT), ("이름 비교", ACC), ("순회 종료", WARN)])
d.save("04-02.map-id-walk.svg")
