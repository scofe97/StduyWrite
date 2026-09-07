# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고, 매 바퀴가 가운데 표에 기록을 남긴다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.2.2 거리 벡터 알고리즘 의사코드 9~19행
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, KR, MONO

W, H = 1000, 780
CX, CY, R = 500, 400, 250
SW, SH = 184, 58
HW, HH = 190, 96
MARKER_OVERHANG, MARKER_GAP = 1.2, 6

d = D(W, H, "SECTION 5.2.2 · DISTANCE-VECTOR LOOP",
      "바퀴는 표를 고쳐 쓰며 돕니다",
      "거리 벡터 알고리즘의 주 루프. 다섯 정거장이 시계 방향으로 돌고, 그중 셋이 가운데 거리 벡터 표에 기록을 남긴다. 표가 더 바뀌지 않으면 전파가 멈추고 루프는 스스로 조용해진다.",
      "멈추라는 신호가 따로 없습니다 — 보낼 것이 없어지면 그냥 멈춥니다")

STATIONS = [
    ("대기", "변화가 올 때까지", None),
    ("이웃 벡터 수신", "이웃 w 의 벡터 도착", "이웃 벡터 저장"),
    ("벨만-포드 재계산", "더해 보고 최소를 고릅니다", "내 벡터 갱신"),
    ("다음 홉 갱신", "최소를 낸 이웃이 v*", "전달 표 기록"),
    ("이웃에 전파", "바뀌었을 때만 보냅니다", None),
]
N = len(STATIONS)
FOCAL = 2


def snap(v):
    return round(v / 4) * 4


geo = []
for k in range(N):
    th = math.radians(-90 + k * (360 / N))
    ux, uy = math.cos(th), math.sin(th)
    bx, by = snap(CX + R * ux - SW / 2), snap(CY + R * uy - SH / 2)
    geo.append(dict(th=th, u=(ux, uy), box=(bx, by, bx + SW, by + SH)))


def circle_box_points(box):
    x0, y0, x1, y1 = box
    pts = []
    for xe in (x0, x1):
        if abs(xe - CX) <= R:
            dy = math.sqrt(R * R - (xe - CX) ** 2)
            for y in (CY - dy, CY + dy):
                if y0 - 0.01 <= y <= y1 + 0.01:
                    pts.append((xe, y))
    for ye in (y0, y1):
        if abs(ye - CY) <= R:
            dx = math.sqrt(R * R - (ye - CY) ** 2)
            for x in (CX - dx, CX + dx):
                if x0 - 0.01 <= x <= x1 + 0.01:
                    pts.append((x, ye))
    uniq = []
    for p in pts:
        if not any(abs(p[0] - q[0]) < 0.5 and abs(p[1] - q[1]) < 0.5 for q in uniq):
            uniq.append(p)
    return uniq


def split_entry_exit(k):
    pts = circle_box_points(geo[k]["box"])
    assert len(pts) == 2, (k, pts)
    out = {}
    for px, py in pts:
        phi = math.atan2(py - CY, px - CX)
        delta = (math.degrees(phi - geo[k]["th"]) + 180) % 360 - 180
        out["exit" if delta > 0 else "entry"] = (px, py, phi)
    assert set(out) == {"entry", "exit"}, (k, out)
    return out


ends = [split_entry_exit(k) for k in range(N)]

# 고리 — 같은 원 위의 시계 방향 호
for k in range(N):
    j = (k + 1) % N
    ex, ey, _ = ends[k]["exit"]
    _, _, phi_in = ends[j]["entry"]
    phi_end = phi_in - MARKER_OVERHANG / R
    qx, qy = CX + R * math.cos(phi_end), CY + R * math.sin(phi_end)
    d.path(f"M {ex:.3f} {ey:.3f} A {R} {R} 0 0 1 {qx:.3f} {qy:.3f}", MUTED, 1.2, m="ar")

# 되쓰기 바큇살 — 정거장 안쪽 모서리에서 표 바깥으로
def box_distance(u, hw, hh):
    cands = []
    if abs(u[0]) > 1e-9:
        cands.append(hw / abs(u[0]))
    if abs(u[1]) > 1e-9:
        cands.append(hh / abs(u[1]))
    return min(cands)


for k, (_, _, spoke) in enumerate(STATIONS):
    if not spoke:
        continue
    ux, uy = geo[k]["u"]
    ds = box_distance((ux, uy), SW / 2, SH / 2)
    dh = box_distance((ux, uy), HW / 2, HH / 2)
    sx, sy = CX + R * ux - ds * ux, CY + R * uy - ds * uy
    tx, ty = CX + (dh + MARKER_GAP) * ux, CY + (dh + MARKER_GAP) * uy
    d.path(f"M {sx:.2f} {sy:.2f} L {tx:.2f} {ty:.2f}", ACC, 1.1, m="acc", dash="4 4")
    if abs(uy) < 0.5:
        # 거의 수평인 바큇살 — 라벨을 허브 쪽에 두면 허브 테두리를 덮는다. 정거장 쪽 아래로 뺀다
        lx, ly = sx + 10, sy + 24
        d.o.append(f'<rect x="{lx - 5}" y="{ly - 13}" width="{len(spoke) * 11 + 10}" height="17" rx="3" fill="{PAPER}"/>')
        d.t(lx, ly, spoke, 11, ACC, KR, "start")
    else:
        mx, my = (sx + tx) / 2, (sy + ty) / 2
        d.o.append(f'<rect x="{mx - 44}" y="{my - 18}" width="88" height="17" rx="3" fill="{PAPER}"/>')
        d.t(mx, my - 6, spoke, 11, ACC, KR)

# 허브
d.tone(CX - HW / 2, CY - HH / 2, HW, HH, ACC, 8, "12", 1.6)
d.t(CX, CY - 20, "거리 벡터 표", 13, ACC, KR, "middle", 600)
d.t(CX, CY + 2, "내 벡터", 11, MUTED, KR)
d.t(CX, CY + 20, "이웃들의 벡터", 11, MUTED, KR)
d.t(CX, CY + 38, "목적지마다의 다음 홉", 11, MUTED, KR)

# 정거장
for k, (name, sub, _) in enumerate(STATIONS):
    x0, y0, x1, y1 = geo[k]["box"]
    hot = k == FOCAL
    d.box(x0, y0, SW, SH, PAPER2, ACC if hot else RULE, 1.5 if hot else 1.0, 7)
    d.t((x0 + x1) / 2, y0 + 24, name, 12, ACC if hot else INK, KR, "middle", 600)
    d.t((x0 + x1) / 2, y0 + 43, sub, 11, MUTED, KR)

d.t(30, 674, "대기와 전파는 표를 읽기만 합니다. 표를 고쳐 쓰는 것은 가운데로 향한 세 바큇살뿐이고, "
             "그 셋이 아무것도 바꾸지 못하는 바퀴가 오면 전파가 멈춥니다.", 11, MUTED, KR, "start")

d.legend(700, [("표를 고쳐 쓰는 단계", ACC), ("바퀴의 진행", MUTED)])
d.t(960, 748, "KUROSE-ROSS 9E DV PSEUDOCODE L9-L19", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-01.dv-loop.svg"
d.save(out)
print(f"정거장 {N} · 바큇살 {sum(1 for s in STATIONS if s[2])} →", out)
