# 13-01 §4 준비성 프로브가 도는 고리 — 원문 그림 13.6.
# 본문(원문 13.1.2): 애플리케이션의 트래픽 수신 준비 상태를 istio-agent 가 WorkloadGroup 정의에 따라
#       주기적으로 검사하고, 상태가 건강에서 불건강으로 또는 그 반대로 "바뀔 때" istiod 에 보고한다.
#       컨트롤 플레인은 그 상태로 트래픽을 그 워크로드에 보낼지 정한다 — 건강하면 데이터 플레인에 VM 의
#       엔드포인트가 설정되고, 불건강하면 그 엔드포인트가 데이터 플레인에서 제거된다.
#       생존성은 메시의 관심사가 아니라 워크로드가 도는 플랫폼의 기능이다(클라우드의 인스턴스 자동 복구).
#       주기와 경로는 원문 13.3.2 의 probe 정의에서 가져왔다 — periodSeconds 5 · httpGet /api/healthz.
#       기록 필드 이름은 원문 13.3.5 의 WorkloadEntry status 출력에서 그대로 가져왔다.
# 타입 스펙: type-loop — 마지막 단계가 첫 단계로 돌아가고 공통 중심 하나가 상태를 쌓는다.
#           스테이션 5(5~8) · 허브 1 · 링은 하나의 원 위 시계방향 호 · 스포크는 방사 점선.
#           축약 1: 스펙은 스포크를 허브로 쓰는 일방향 화살표로 두지만, 이 고리에서 엔드포인트 갱신과
#           라우팅은 그 기록을 읽는 쪽이다. 방향을 지어내지 않으려고 화살촉 없는 점선으로 두고
#           범례에서 "주고받는 것" 이라 밝힌다.
#           축약 2: 저자가 구간별 소요 시간을 적지 않아 호의 길이는 시간이 아니라 순서만 나타낸다.
import sys, math
sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 1040, 848
CX, CY, R = 520, 452, 300
SW, SH = 176, 64
HW, HH = 224, 104
N = 5

d = D(W, H, "ISTIO IN ACTION · 13-01 §4",
      "한 바퀴가 기록을 고치고 그 기록이 다음 바퀴를 정한다",
      "istio-agent 가 애플리케이션을 찌르고, 상태가 바뀔 때만 istiod 에 알리고, istiod 가 엔드포인트를 "
      "넣거나 뺀다. 가운데 기록이 매 바퀴 갱신되며 색이 붙은 자리가 저자가 조건을 단 지점이다.",
      "생존성 고리는 이 밖에서 클라우드가 따로 돌립니다")

stations = [
    ("프로브", "istio-agent · 5 초마다", "lastProbeTime"),
    ("응답", "성공인가 실패인가", None),
    ("보고", "바뀔 때만 istiod 로", "status · lastTransitionTime"),
    ("엔드포인트", "istiod 가 넣고 뺀다", "건강 상태를 근거로"),
    ("라우팅", "트래픽이 가거나 안 간다", None),
]
FOCAL = 2

def q4(v): return round(v / 4) * 4

theta = [math.radians(-90 + k * 360 / N) for k in range(N)]
P = [(CX + R * math.cos(t), CY + R * math.sin(t)) for t in theta]
BOX = [(q4(px - SW / 2), q4(py - SH / 2)) for px, py in P]

def intersections(k):
    bx, by = BOX[k]
    x1, x2, y1, y2 = bx, bx + SW, by, by + SH
    pts = []
    for xe in (x1, x2):
        s = R * R - (xe - CX) ** 2
        if s >= 0:
            for y in (CY + math.sqrt(s), CY - math.sqrt(s)):
                if y1 <= y <= y2: pts.append((xe, y))
    for ye in (y1, y2):
        s = R * R - (ye - CY) ** 2
        if s >= 0:
            for x in (CX + math.sqrt(s), CX - math.sqrt(s)):
                if x1 <= x <= x2: pts.append((x, ye))
    uniq = []
    for p in pts:
        if not any(abs(p[0] - u[0]) < 0.01 and abs(p[1] - u[1]) < 0.01 for u in uniq):
            uniq.append(p)
    return uniq

def ang(p): return math.atan2(p[1] - CY, p[0] - CX)
def cw_gap(a, b): return (a - b) % (2 * math.pi)

EXIT, ENTRY = [], []
for k in range(N):
    pts = intersections(k)
    assert len(pts) == 2, (k, pts)
    a0, a1 = ang(pts[0]), ang(pts[1])
    if cw_gap(a0, theta[k]) < cw_gap(a1, theta[k]):
        EXIT.append(pts[0]); ENTRY.append(pts[1])
    else:
        EXIT.append(pts[1]); ENTRY.append(pts[0])

OVERHANG = 1.2
for k in range(N):
    j = (k + 1) % N
    phi = ang(ENTRY[j]) - OVERHANG / R
    ex, ey = CX + R * math.cos(phi), CY + R * math.sin(phi)
    sx, sy = EXIT[k]
    focal = (j == FOCAL)
    d.path(f"M {sx:.3f} {sy:.3f} A {R} {R} 0 0 1 {ex:.3f} {ey:.3f}",
           ACC if focal else MUTED, 1.5 if focal else 1.2, m="acc" if focal else "ar")

def box_dist(ux, uy, hw, hh):
    cands = []
    if abs(ux) > 1e-9: cands.append(hw / abs(ux))
    if abs(uy) > 1e-9: cands.append(hh / abs(uy))
    return min(cands)

for k in range(N):
    ux, uy = math.cos(theta[k]), math.sin(theta[k])
    ds = box_dist(ux, uy, SW / 2, SH / 2)
    dh = box_dist(ux, uy, HW / 2, HH / 2)
    s = (P[k][0] - ds * ux, P[k][1] - ds * uy)
    e = (CX + (dh + 8) * ux, CY + (dh + 8) * uy)
    d.line(s[0], s[1], e[0], e[1], SOFT, 1.0, "4 4")
    lab = stations[k][2]
    if lab:
        mx, my = (s[0] + e[0]) / 2, (s[1] + e[1]) / 2
        tw = len(lab) * 5.6 + 12
        d.o.append(f'<rect x="{mx - tw / 2:.2f}" y="{my - 8}" width="{tw:.2f}" height="14" rx="3" fill="{PAPER}"/>')
        d.t(mx, my + 3, lab, 8, SOFT, MONO, "middle", 600)

d.o.append(f'<rect x="{CX - HW / 2}" y="{CY - HH / 2}" width="{HW}" height="{HH}" rx="8" '
           f'fill="{PAPER2}" stroke="{INK}44" stroke-width="1.2"/>')
d.t(CX, CY - 22, "HUB", 8, SOFT, MONO, "middle", 600)
d.t(CX, CY + 2, "WorkloadEntry 의 status", 13, INK, KR, "middle", 600)
d.t(CX, CY + 24, "conditions · lastProbeTime", 9, MUTED, MONO)
d.t(CX, CY + 40, "lastTransitionTime", 9, MUTED, MONO)

for k in range(N):
    bx, by = BOX[k]
    focal = (k == FOCAL)
    if focal:
        d.o.append(f'<rect x="{bx}" y="{by}" width="{SW}" height="{SH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(bx, by, SW, SH, PAPER2, RULE, 1.0, 6)
    d.t(bx + SW / 2, by + 28, stations[k][0], 13, ACC if focal else INK, KR, "middle", 600)
    d.t(bx + SW / 2, by + 48, stations[k][1], 9, MUTED, KR, "middle")

d.t(24, 764, "생존성 고리는 이 밖에서 따로 돈다 — 클라우드의 자동 복구는 실패한 기계를 새 인스턴스로 갈아 끼운다", 11, SOFT, KR, "start")
d.t(24, 788, "저자의 어림 규칙 — 준비성 프로브가 항상 생존성 프로브보다 먼저 실패해야 한다", 11, MUTED, KR, "start")
d.legend(806, [("저자가 조건을 단 지점", ACC), ("한 바퀴가 기록과 주고받는 것", SOFT)])
d.save("13-01.readiness-loop.svg")
