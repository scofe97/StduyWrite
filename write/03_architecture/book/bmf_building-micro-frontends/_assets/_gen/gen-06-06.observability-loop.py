# 06-06 §4 — 프로덕션에서 돌아오는 신호가 루프를 닫는다 (원문 Observability).
# 도구가 하는 셋(여정 회수 · 스택 트레이스 수집 · 에러 그룹화)과 사용자 컨텍스트는 원문 서술 그대로다.
# 가운데 허브는 그 도구가 쌓는 컨텍스트다. 이것이 없으면 재현에 몇 시간을 쓰게 된다는 것이 저자의 인과다.
# 타입 스펙: type-loop — 마지막 단계가 첫 단계를 먹이고 공유 허브에 상태가 쌓이는 순환. 점선 스포크가 그 기록이다.
#           §1 입력 계약: stations 6 · hub 1 · focal 1. §2 공식 theta_k = -90 + k*(360/N) 로 좌표 산출.
#           축약: 06-01.review-loop 의 station_w 184 · radius 300 을 그대로 승계한다(같은 타입 첫 장의 stride 승계).
import sys, math; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
CX, CY, R = 500, 448, 300
SW, SH = 184, 64
HW, HH = 240, 112
N = 6
LEGEND_Y = CY + R + SH // 2 + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-06 §4",
      "프로덕션에서 돌아오는 신호",
      "시계 방향으로 한 바퀴가 돌 때마다 사용자 컨텍스트가 가운데에 쌓이고, 그 기록이 다음 조사의 출발점이 된다.",
      "점선은 매 바퀴가 관측 도구에 남기는 기록입니다")

stations = [
    ("사용자가 버그를 만난다", "프로덕션에서 일어난다", None),
    ("조각이 에러를 보고한다", "커스텀과 일반 모두", "에러"),
    ("여정과 스택을 모은다", "에러를 그룹으로 묶는다", None),
    ("알림이 팀에 간다", "PagerDuty 연동", None),
    ("컨텍스트로 좁힌다", "브라우저 · OS · 국가", "조사 경로"),
    ("고쳐서 배포한다", "재현에 시간을 안 쓴다", None),
]
FOCAL = 1

def center(k):
    a = math.radians(-90 + k * (360 / N))
    return round(CX + R * math.cos(a)), round(CY + R * math.sin(a))

def clip(dx, dy, a, b):
    tx = a / abs(dx) if abs(dx) > 1e-9 else 1e9
    ty = b / abs(dy) if abs(dy) > 1e-9 else 1e9
    return min(tx, ty)

GAP = 20
for k in range(N):
    a1 = math.radians(-90 + k * (360 / N) + GAP)
    a2 = math.radians(-90 + (k + 1) * (360 / N) - GAP)
    x1, y1 = CX + R * math.cos(a1), CY + R * math.sin(a1)
    x2, y2 = CX + R * math.cos(a2), CY + R * math.sin(a2)
    d.path(f"M {x1:.1f} {y1:.1f} A {R} {R} 0 0 1 {x2:.1f} {y2:.1f}", MUTED, 1.4, m="ar")

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

d.box(CX - HW / 2, CY - HH / 2, HW, HH, PAPER2, RULE, 1.2, 8)
d.t(CX, CY - 18, "쌓인 사용자 컨텍스트", 13, INK, KR, "middle", 600)
d.t(CX, CY + 6, "Sentry · New Relic", 10, MUTED, MONO)
d.t(CX, CY + 26, "없으면 루프가 안 닫힌다", 10.5, MUTED)

for k, (name, sub, _) in enumerate(stations):
    px, py = center(k)
    x, y = px - SW / 2, py - SH / 2
    if k == FOCAL:
        d.o.append(f'<rect x="{x}" y="{y}" width="{SW}" height="{SH}" rx="8" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, SW, SH, PAPER2, RULE, 1.0, 8)
    d.t(px, py - 6, name, 11.5, ACC if k == FOCAL else INK, KR, "middle", 600)
    d.t(px, py + 14, sub, 9, MUTED)

d.legend(LEGEND_Y, [("모든 조각이 해야 할 일", ACC)])
d.save("06-06.observability-loop.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 좌우:", center(5)[0] - SW // 2, center(1)[0] + SW // 2)
