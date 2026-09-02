# 06-05 §4 — 한 뷰의 최종 출력에 여러 팀이 기여한다 (원문 Horizontal-Split End-to-End Testing Challenges).
# 원문은 결제 팀의 조각이 여러 뷰에 있다는 것과, 다른 팀이 조각을 바꾸는 순간 테스트가 무효가 되거나 깨진다는 것을 적는다.
# 뷰 이름은 원문이 밝힌 둘(결제 수단을 고르는 뷰 · 거래를 수행하는 다음 뷰)만 쓴다.
# 타입 스펙: type-dependency — 무엇이 무엇에 의존하나. 여러 팀이 한 뷰로 모이는 fan-in 과 되돌아오는 파괴 경로가 논지다.
#           축약: 06-04.polyrepo-contracts 의 배지 표기를 승계하고, 되돌아오는 점선에 파괴 라벨을 붙였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, BAD, PAPER, PAPER2, RULE, KR, MONO

W = 1240
TW, TH, TGAP, TX0, TY = 340, 92, 48, 88, 140
VW, VH, VGAP, VX0, VY = 400, 96, 40, 200, 316
EW, EH, EX, EY = 400, 88, 420, 492
LEGEND_Y = EY + EH + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-05 §4",
      "한 뷰의 최종 출력에 여러 팀이 기여한다",
      "위가 조각을 대는 팀들이고 가운데가 그 조각이 함께 나타나는 뷰다. 색이 붙은 팀의 조각이 여러 뷰에 걸쳐 있다.",
      "붉은 점선은 다른 팀이 조각을 바꾸는 순간 일어나는 일입니다")

def badge(x, y, txt, c):
    bw = len(txt) * 7.0 + 16
    d.o.append(f'<rect x="{x - bw}" y="{y}" width="{bw}" height="20" rx="4" fill="{PAPER}" stroke="{c}" stroke-width="0.9"/>')
    d.t(x - bw / 2, y + 14, txt, 9, c, MONO)

teams = [
    ("카탈로그 팀", "자기 조각을 뷰에 얹는다", False),
    ("결제 팀", "결제에 필요한 모든 조각", True),
    ("그 밖의 팀", "같은 뷰에 함께 기여한다", False),
]
views = [
    ("결제 수단을 고르는 뷰", "payment option 조각이 안내한다"),
    ("거래를 수행하는 다음 뷰", "선택한 수단으로 금전 거래"),
]

# 간선 먼저 — z-order. 강조 간선은 나중에 그려야 회색 간선에 덮이지 않는다.
for i in sorted(range(len(teams)), key=lambda k: teams[k][2]):
    tx = TX0 + i * (TW + TGAP) + TW / 2
    for j in range(len(views)):
        vx = VX0 + j * (VW + VGAP) + VW / 2
        c = ACC if teams[i][2] else MUTED
        d.arrow([(tx, TY + TH), (tx, VY - 26), (vx, VY - 26), (vx, VY - 2)], c, "acc" if teams[i][2] else "ar", 1.2)

for j in range(len(views)):
    vx = VX0 + j * (VW + VGAP) + VW / 2
    d.arrow([(vx, VY + VH), (vx, EY - 20), (EX + EW / 2, EY - 20), (EX + EW / 2, EY - 2)], MUTED, "ar", 1.2)

# 되돌아오는 파괴 경로 — 라벨은 세로 구간이 아니라 가로 구간에 얹는다(좌측 이탈 방지)
COR = 48
d.path(f"M {EX} {EY + EH / 2} L {COR} {EY + EH / 2} L {COR} {TY + TH / 2} L {TX0 - 2} {TY + TH / 2}", BAD, 1.3, m="bad", dash="5 5")
lbl, lx = "바뀌면 무효가 되거나 깨진다", (COR + EX) / 2
lw = len(lbl) * 9.4 + 16
d.o.append(f'<rect x="{lx - lw / 2}" y="{EY + EH / 2 - 22}" width="{lw}" height="16" fill="{PAPER}"/>')
d.t(lx, EY + EH / 2 - 10, lbl, 9, BAD, KR, "middle", 600)

for i, (name, sub, focal) in enumerate(teams):
    x = TX0 + i * (TW + TGAP)
    if focal:
        d.o.append(f'<rect x="{x}" y="{TY}" width="{TW}" height="{TH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, TY, TW, TH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, TY + 36, name, 12.5, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, TY + 58, sub, 10, MUTED, KR, "start")

for j, (name, sub) in enumerate(views):
    x = VX0 + j * (VW + VGAP)
    d.box(x, VY, VW, VH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, VY + 38, name, 12.5, INK, KR, "start", 600)
    d.t(x + 20, VY + 62, sub, 10, MUTED, KR, "start")
    badge(x + VW - 16, VY + 16, "3 in", MUTED)

d.box(EX, EY, EW, EH, PAPER2, RULE, 1.0, 6)
d.t(EX + EW / 2, EY + 36, "그 뷰의 E2E 테스트", 12.5, INK, KR, "middle", 600)
d.t(EX + EW / 2, EY + 60, "누가 쓰고 누가 고치는지 정해야 한다", 10, MUTED)

d.legend(LEGEND_Y, [("여러 뷰에 걸친 조각을 대는 팀", ACC), ("테스트를 깨뜨리는 경로", BAD)])
d.save("06-05.horizontal-e2e.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", TX0 + 3 * TW + 2 * TGAP)
