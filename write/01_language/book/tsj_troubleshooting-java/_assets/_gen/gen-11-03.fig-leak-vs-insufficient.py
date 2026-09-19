# 11-03 §3 — 누수와 부족의 구별. 본문의 논지는 "회수 여부가 아니라 *잔량의 추세*가
# 갈림길" 이고, 원서가 "회수되니 누수가 아니다" 로 단정한 것을 고친 자리다.
# 두 곡선을 한 축에 겹치면 톱니끼리 엉켜 정작 논지인 바닥선이 안 보인다. 그래서
# 위아래 두 판으로 갈라 같은 축척으로 놓고, 각 판에서 강조는 톱니가 아니라 **바닥선**에
# 건다 — 누수는 바닥이 오르고 부족은 평평하다. 회수 자체는 둘 다 일어난다.
# focal 은 위 판의 오르는 바닥선 — 본문이 유일한 판별 근거로 지목한 것.
# 타입 스펙: type-line — 시간에 따른 연속 추세. 두 시나리오를 같은 축척의 두 판으로 견준다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 800, 536

d = D(W, H, "TROUBLESHOOTING JAVA · 11-03 §3",
      "갈림길은 회수가 아니라 바닥입니다",
      "메모리 누수와 메모리 부족을 힙 사용 곡선 두 판으로 가른 그림. 두 경우 모두 GC 가 회수하므로 "
      "톱니 모양 자체는 판별 근거가 되지 못한다. 갈라지는 것은 수집 직후 남는 잔량, 곧 바닥선이다. "
      "위 판의 누수는 회차마다 바닥이 오르고(900 → 980 → 1050) 아래 판의 부족은 바닥이 평평하다. "
      "다만 로그 몇 줄로는 어느 쪽도 증명되지 않아 긴 구간의 추세나 힙 덤프가 필요하다.",
      lead="둘 다 회수는 됩니다 — 수집 직후 남는 양이 오르는지만 봅니다")

PX, PW = 92, 620
N = 7
SEG = PW / N
PANEL_H = 124


def poly(pts, c, sw, dash=None):
    dd = f' stroke-dasharray="{dash}"' if dash else ""
    p = " ".join(("M" if i == 0 else "L") + f" {x:.1f} {y:.1f}" for i, (x, y) in enumerate(pts))
    d.o.append(f'<path d="{p}" fill="none" stroke="{c}" stroke-width="{sw}"{dd}/>')


def panel(top, title, note, colour, floor_at, focal):
    """한 판: 축 + 톱니 + 바닥 추세선."""
    base = top + PANEL_H
    peak = top + 16
    d.box(44, top - 28, 712, PANEL_H + 56, PAPER2, RULE, 0.9, 6)
    d.t(64, top - 8, title, 13, colour, KR, "start", 600)
    d.t(736, top - 8, note, 12, MUTED, KR, "end")
    # 축
    d.line(PX, top, PX, base, RULE, 1.0)
    d.line(PX, base, PX + PW, base, RULE, 1.0)
    d.t(PX - 10, top + 8, "힙", 12, SOFT, KR, "end")
    # 톱니 — 회수는 둘 다 일어난다
    pts = []
    for i in range(N):
        x0 = PX + i * SEG
        pts.append((x0, floor_at(i)))
        pts.append((x0 + SEG * 0.84, peak))
        pts.append((x0 + SEG * 0.88, floor_at(i + 1)))
    poly(pts, colour, 1.6)
    # 바닥 추세선 — 논지
    poly([(PX, floor_at(0)), (PX + PW, floor_at(N))], colour, 2.6 if focal else 1.6, "6 4")
    return base


# ── 위 판: 누수 — 바닥이 오른다 (focal)
T1 = 130
RISE = 11
BASE1 = T1 + PANEL_H


def leak_floor(i):
    return BASE1 - 22 - i * RISE


panel(T1, "누수 — 바닥이 회차마다 오릅니다", "full GC 도 추세를 못 되돌립니다", ACC, leak_floor, True)
for i, v in enumerate(("900M", "980M", "1050M")):
    d.t(PX + 8 + i * SEG, leak_floor(i) + 18, v, 11, ACC, MONO, "start")

# ── 아래 판: 부족 — 바닥이 평평
T2 = 312
BASE2 = T2 + PANEL_H
flat = BASE2 - 22
panel(T2, "부족 — 바닥이 대체로 평평합니다", "회수가 되고 바닥이 제자리입니다", INFO, lambda i: flat, False)
d.t(PX + 8, flat + 18, "8192M → 6100M → 5800M → 5600M", 11, INFO, MONO, "start")

# ── 판별 규칙 한 줄
d.t(44, 478, "판별에 쓰지 않는 것 — 톱니 모양 · full GC 한 줄의 회수율", 12, SOFT, KR, "start")
d.t(756, 478, "확정은 힙 덤프(10장)", 12, MUTED, KR, "end")

d.legend(H - 40, [("바닥이 오릅니다 — 누수 근거", ACC), ("바닥이 평평합니다 — 부족", INFO)])
d.save(os.path.join(os.path.dirname(__file__), "..", "11-03.fig-leak-vs-insufficient.svg"))
print("ok leak-vs-insufficient")
