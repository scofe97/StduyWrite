"""Shift+Tab 단축키를 통한 6단계 권한 모드 순환 루프.

# 타입 스펙: type-loop
"""
import math
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parent))

from dd import D, ACC, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 680
CX, CY, R = 480, 364, 224
SW, SH = 188, 56
HW, HH = 148, 76
MARK = 1.2   # 화살촉 돌출 보정 (type-loop §2.2)

d = D(
    W, H,
    "PERMISSION CYCLE · REINFORCING LOOP",
    "Shift+Tab 단축키를 통한 권한 모드 순환 전이",
    "대화 세션 내에서 Shift+Tab 입력 시 기본 순환 manual·acceptEdits·plan 에 조건부 모드가 끼어드는 구조",
    lead="bypassPermissions·auto 는 사용 가능할 때만 순환에 들어오며, 폐쇄 모드인 dontAsk 는 순환에서 제외됩니다"
)

STATIONS = [
    ("manual", "파일 읽기만 자동 허용", False),
    ("acceptEdits", "파일 수정 자동 승인", False),
    ("plan", "읽기 전용 · 쓰기 차단", False),
    ("bypassPermissions", "조건부 · 전체 자동 승인 (위험)", False),
    ("auto", "조건부 · 안전 분류기 자율 심사", True),     # focal! 본문 05-02:265 순서: plan → bypassPermissions → auto
]
N = len(STATIONS)
COND_IDX = {3, 4}   # bypassPermissions·auto: 사용 가능할 때만 순환에 포함

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
            s = math.sqrt(max(0.0, R * R - dx * dx))
            for y in (CY - s, CY + s):
                if by - 1e-6 <= y <= by + SH + 1e-6:
                    pts.append((xe, y))
    for ye in (by, by + SH):
        dy = ye - CY
        if abs(dy) <= R:
            s = math.sqrt(max(0.0, R * R - dy * dy))
            for x in (CX - s, CX + s):
                if bx - 1e-6 <= x <= bx + SW + 1e-6:
                    pts.append((x, ye))
    return pts

def ang(pt):
    return math.atan2(pt[1] - CY, pt[0] - CX)

def split(k):
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

# 1) 원호 (Ring flow) — 시계 방향 A R R 0 0 1, 노드 뒤에 배치
for k in range(N):
    j = (k + 1) % N
    qx, qy = HITS[k][1]
    ent = HITS[j][0]
    phi = ang(ent) - MARK / R
    ex, ey = CX + R * math.cos(phi), CY + R * math.sin(phi)
    is_focal_edge = (j == 4)
    c = ACC if is_focal_edge else MUTED
    mk = "acc" if is_focal_edge else "ar"
    sw = 1.6 if is_focal_edge else 1.2
    cond_edge = k in COND_IDX or j in COND_IDX
    d.path(f"M {qx:.3f} {qy:.3f} A {R} {R} 0 0 1 {ex:.3f} {ey:.3f}", c, sw, m=mk, dash="5 4" if cond_edge else None)

# 2) 점선 스포크 (Write-back spokes) — 각 스테이션에서 중앙 허브로
def box_dist(ux, uy, a, b):
    ds = []
    if abs(ux) > 1e-9:
        ds.append(a / abs(ux))
    if abs(uy) > 1e-9:
        ds.append(b / abs(uy))
    return min(ds)

for k in range(N):
    ux, uy = math.cos(theta[k]), math.sin(theta[k])
    ds = box_dist(ux, uy, SW / 2, SH / 2)
    dh = box_dist(ux, uy, HW / 2, HH / 2)
    sx, sy = P[k][0] - ds * ux, P[k][1] - ds * uy
    hx, hy = CX + (dh + 6) * ux, CY + (dh + 6) * uy
    d.arrow([(sx, sy), (hx, hy)], SOFT, "soft", 1.2, "5 4")

# 3) 스테이션 상자 (Z-order: 원호 위에 얹는다)
for k, (title, sub, focal) in enumerate(STATIONS):
    x, y = BOX[k]
    cond = k in COND_IDX
    if cond:
        fill, stroke, sw_ = (f"{ACC}14", ACC, 1.4) if focal else (PAPER2, MUTED, 1.0)
        d.o.append(
            f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="6" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{sw_}" stroke-dasharray="5 4"/>'
        )
    elif focal:
        d.tone(x, y, SW, SH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 6)

    tc = ACC if focal else INK
    sc = ACC if focal else MUTED
    d.t(x + SW / 2, y + 25, title, 13, tc, MONO, "middle", 600)
    d.t(x + SW / 2, y + 45, sub, 11, sc, KR, "middle")

# 4) 중앙 허브 (세션 권한 상태 관리)
d.box(CX - HW // 2, CY - HH // 2, HW, HH, INK, INK, 1.2, 6)
d.t(CX, CY - 6, "세션 권한 상태", 13.5, PAPER, KR, "middle", 600)
d.t(CX, CY + 16, "Shift+Tab 런타임 갱신", 11, PAPER2, KR, "middle")

# 5) 순환 제외 모드 안내 (dontAsk)
d.box(748, 104, 188, 52, fill=PAPER2, stroke=WARN, sw=1.0, r=6)
d.t(842, 126, "dontAsk (순환 제외)", 12, WARN, MONO, "middle", 600)
d.t(842, 144, "사전 승인 도구 전용 폐쇄", 11, MUTED, KR, "middle")

# 범례
d.legend(620, [
    ("Shift+Tab 순환", MUTED),
    ("자동 모드 (focal)", ACC),
    ("권한 갱신", SOFT),
    ("순환 제외", WARN),
    ("점선: 사용 가능할 때만", SOFT),
])

d.save("05-02.permission-cycle.svg")
