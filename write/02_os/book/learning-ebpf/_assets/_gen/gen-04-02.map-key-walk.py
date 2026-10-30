# 타입 스펙: type-loop — 안쪽 고리. 다섯 단계가 직전 키 허브를 갱신하며 ENOENT 까지 돈다(허브 하나, 스테이션 다섯, 정확한 원호).
# 사실 출처: 추출본 ebpf4.txt 971~1023행(BPF_MAP_GET_NEXT_KEY {map_fd=3, key=NULL} → BPF_MAP_LOOKUP_ELEM → "key": 0 "Hey root!" → GET_NEXT_KEY → "key": 501 "Hi user 501!" → -1 ENOENT),
#   linux v7.2 tools/bpf/bpftool/map.c 826~877행(map_dump: prev_key = NULL → bpf_map_get_next_key(fd, prev_key, key) → ENOENT 면 끝 → dump_map_elem 의 bpf_map_lookup_elem → prev_key = key).
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
      "직전 키를 넘겨 다음 키를 받고 값을 읽는다",
      "bpftool 은 key=NULL 로 첫 키 0 을 받아 값을 읽어 출력하고, 그 키를 직전 키로 넘겨 다음 키 501 을 받는다. 501 다음 GET_NEXT_KEY 가 ENOENT 를 돌려주면 끝난다.",
      "키 몰라도 전 원소 순회")

STATIONS = [
    ("prev_key = key", "0 → 501", False),
    ("BPF_MAP_GET_NEXT_KEY", "key=NULL → 0 → 501", True),
    ("ENOENT?", "501 다음에 ENOENT", False),
    ("BPF_MAP_LOOKUP_ELEM", "map_fd=3 · key=0, 501", False),
    ("0 → \"Hey root!\"", "501 → \"Hi user 501!\"", False),
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


# 2) 스포크 — 직전 키를 갱신하는 스테이션 0 하나만 허브로 되돌린다
def box_dist(ux, uy, a, b):
    ds = []
    if abs(ux) > 1e-9: ds.append(a / abs(ux))
    if abs(uy) > 1e-9: ds.append(b / abs(uy))
    return min(ds)


K = 0
ux, uy = math.cos(theta[K]), math.sin(theta[K])
ds = box_dist(ux, uy, SW / 2, SH / 2)
dh = box_dist(ux, uy, HW / 2, HH / 2)
sx, sy = P[K][0] - ds * ux, P[K][1] - ds * uy
hx, hy = CX + (dh + 6) * ux, CY + (dh + 6) * uy
d.arrow([(sx, sy), (hx, hy)], SOFT, "soft", 1.2, "5 4")

# 3) 종료 — 스테이션 2(ENOENT?) 오른쪽으로 빠진다
bx1, by1 = BOX[2]
d.arrow([(bx1 + SW + 2, by1 + SH // 2), (bx1 + SW + 40, by1 + SH // 2)], WARN, "warn", 1.5)
d.chip(bx1 + SW + 40 + 62, by1 + SH // 2, "순회 끝", WARN, 13)

# 4) 스테이션
for k, (title, sub, focal) in enumerate(STATIONS):
    x, y = BOX[k]
    if focal:
        d.tone(x, y, SW, SH, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, SW, SH, PAPER2, MUTED, 1.2, 6)
    kr = any("가" <= ch <= "힣" for ch in title)
    d.t(x + SW / 2, y + 28, title, 13, ACC if focal else INK, KR if kr else MONO, "middle", 600)
    d.t(x + SW / 2, y + 48, sub, 13, MUTED, KR if any("가" <= ch <= "힣" for ch in sub) else MONO)

# 5) 허브 — 짙은 요소는 이것 하나
d.box(CX - HW // 2, CY - HH // 2, HW, HH, INK, INK, 1.2, 6)
d.t(CX, CY - 4, "직전 키", 14, PAPER, KR, "middle", 600)
d.t(CX, CY + 18, "NULL → 0 → 501", 12, PAPER2, MONO)

d.legend(H - 56, [("한 바퀴", MUTED), ("커서 갱신", SOFT), ("다음 키 요청", ACC), ("순회 종료", WARN)])
d.save("04-02.map-key-walk.svg")
