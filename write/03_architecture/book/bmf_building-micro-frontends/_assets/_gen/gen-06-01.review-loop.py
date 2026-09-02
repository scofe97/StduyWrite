# 06-01 §4 — 파이프라인을 다시 보는 순환 (원문 Iterate Often).
# 8~10분 임계와 두 검토 주기(느리면 월 1회 · 건강하면 3~4개월)는 원문 수치 그대로다.
# 가운데 허브는 저자가 요구한 대시보드다. 매 바퀴가 소요 시간을 여기에 쌓고, 그 기록이 다음 바퀴의 대상을 정한다.
# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고 공유 허브에 상태가 쌓이는 순환. 점선 스포크가 그 기록이다.
#           §1 입력 계약: stations 6 · hub 1 · focal 1. §2 공식 theta_k = -90 + k*(360/N), P_k = C + R*u_k 로 좌표 산출.
#           축약: station_w 는 한글 라벨을 담으려고 스펙 기본 160 대신 184 를 썼고 radius 는 240 대신 300 으로 늘렸다
#           (반경을 그대로 두면 상자 사이 각도가 좁아 링 화살표가 안 보인다).
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
CX, CY, R = 500, 448, 300
SW, SH = 184, 64          # station
HW, HH = 240, 112         # hub
N = 6
LEGEND_Y = CY + R + SH // 2 + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-01 §4",
      "파이프라인을 다시 보는 순환",
      "시계 방향으로 한 바퀴가 돌 때마다 소요 시간이 가운데 대시보드에 쌓이고, 그 기록이 다음 바퀴에서 고칠 단계를 정한다.",
      "점선은 매 바퀴가 대시보드에 남기는 기록입니다")

stations = [
    ("파이프라인이 돈다", "머지마다 실행된다", None),
    ("소요를 기록한다", "빌드 시간이 남는다", "소요 시간"),
    ("8~10분을 넘는가", "재검토를 여는 신호", None),
    ("느린 단계를 고른다", "병렬과 직렬을 가른다", None),
    ("고쳐서 짧게 만든다", "그 단계를 최적화한다", None),
    ("주기를 정해 다시 본다", "느리면 월 1회", "검토 주기"),
]
FOCAL = 2

def center(k):
    a = math.radians(-90 + k * (360 / N))
    return round(CX + R * math.cos(a)), round(CY + R * math.sin(a))

def clip(dx, dy, a, b):
    tx = a / abs(dx) if abs(dx) > 1e-9 else 1e9
    ty = b / abs(dy) if abs(dy) > 1e-9 else 1e9
    return min(tx, ty)

# 1) 링 화살표 — 상자 사이 각도만큼 비켜서 그린다
GAP = 20
for k in range(N):
    a1 = math.radians(-90 + k * (360 / N) + GAP)
    a2 = math.radians(-90 + (k + 1) * (360 / N) - GAP)
    x1, y1 = CX + R * math.cos(a1), CY + R * math.sin(a1)
    x2, y2 = CX + R * math.cos(a2), CY + R * math.sin(a2)
    d.path(f"M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}", MUTED, 1.4, m="ar")

# 2) 점선 스포크 — 모든 정거장이 허브에 기록을 남긴다
for k in range(N):
    px, py = center(k)
    vx, vy = CX - px, CY - py
    ln = math.hypot(vx, vy); ux, uy = vx / ln, vy / ln
    sx = px + ux * clip(ux, uy, SW / 2, SH / 2)
    sy = py + uy * clip(ux, uy, SW / 2, SH / 2)
    ex = CX - ux * clip(ux, uy, HW / 2, HH / 2)
    ey = CY - uy * clip(ux, uy, HW / 2, HH / 2)
    d.line(sx, sy, ex, ey, SOFT, 0.9, "3 6")
    label = stations[k][2]
    if label:   # 점선이 글자를 관통하지 않게 배경 마스크를 깔고 올린다
        mx, my = (sx + ex) / 2, (sy + ey) / 2 - 6
        lw = len(label) * 8.0 + 12
        d.o.append(f'<rect x="{mx - lw / 2:.1f}" y="{my - 10}" width="{lw:.1f}" height="14" fill="{PAPER}"/>')
        d.t(mx, my, label, 8.5, SOFT, MONO)

# 3) 허브
d.box(CX - HW / 2, CY - HH / 2, HW, HH, PAPER2, RULE, 1.2, 8)
d.t(CX, CY - 18, "대시보드에 쌓인 기록", 13, INK, KR, "middle", 600)
d.t(CX, CY + 6, "어느 단계가 느린지", 10.5, MUTED)
d.t(CX, CY + 26, "여기서만 보인다", 10.5, MUTED)

# 4) 정거장
for k, (name, sub, _) in enumerate(stations):
    px, py = center(k)
    x, y = px - SW / 2, py - SH / 2
    if k == FOCAL:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(px, py - 6, name, 11.5, ACC if k == FOCAL else INK, KR, "middle", 600)
    d.t(px, py + 14, sub, 9, MUTED)

d.legend(LEGEND_Y, [("재검토를 여는 신호", ACC)])
d.save("06-01.review-loop.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 좌우:", center(5)[0] - SW // 2, center(1)[0] + SW // 2)
