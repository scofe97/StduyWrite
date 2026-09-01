# 04-01 §2 — 사용자 흐름이 팀 경계를 건너간다 (원문 Figure 4-1 + 팀 배정 목록).
# 팀 이름과 담당 서브도메인은 저자의 목록 그대로다. 마지막 화면만 두 팀의 조각이 함께 놓인다.
# 타입 스펙: type-swimlane — 주체를 가로 레인으로 두고 단계가 레인을 건너간다.
#           레인을 건너는 화살표가 논지이고, 한 화면을 둘이 나눠 갖는 마지막 갈래에만 accent 를 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1360
LABEL_W, LANE_H, LANE_Y = 154, 104, 112
BW, BH, GAP, X0 = 190, 62, 44, 178
LANES = [("팀 사시미", "HOME · AUTH · ACCOUNT DETAILS"),
         ("팀 마키", "CATALOG"),
         ("팀 니기리", "PAYMENTS")]
LANE_BOT = LANE_Y + len(LANES) * LANE_H
LEGEND_Y = LANE_BOT + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-01 §2",
      "사용자 흐름이 팀 경계를 건너간다",
      "왼쪽에서 오른쪽이 사용자가 밟는 순서이고 세로가 그 화면을 소유한 팀이다. 색이 붙은 갈래가 한 화면을 두 팀이 나눠 갖는 자리다.",
      "레인을 건너는 화살표가 팀이 바뀌는 지점입니다")

for k, (name, eyebrow) in enumerate(LANES):
    y = LANE_Y + k * LANE_H
    if k % 2 == 0:
        d.o.append(f'<rect x="{LABEL_W}" y="{y}" width="{W - LABEL_W - 12}" height="{LANE_H}" fill="{INK}05"/>')
    d.line(0, y, W - 12, y, RULE, 0.8)
    d.t(LABEL_W / 2, y + LANE_H / 2 - 4, name, 12, INK, KR, "middle", 600)
    d.t(LABEL_W / 2, y + LANE_H / 2 + 15, eyebrow, 7, SOFT, MONO)
d.line(0, LANE_BOT, W - 12, LANE_BOT, RULE, 0.8)
d.line(LABEL_W, LANE_Y, LABEL_W, LANE_BOT, RULE, 1.0)

def bx(c): return X0 + c * (BW + GAP)
def by(l): return LANE_Y + l * LANE_H + (LANE_H - BH) / 2

steps = [   # (col, lane, 제목, 부제)
    (0, 0, "홈 페이지", "vertical split"),
    (1, 0, "로그인", "중앙 인증 · AD 연동"),
    (2, 1, "카탈로그", "vertical split"),
    (3, 1, "상품 상세", "지역 라우팅"),
    (4, 0, "계정 상세", "horizontal split"),
    (4, 2, "결제 수단", "horizontal split"),
]

def cross(i, j, acc=False):
    (c1, l1, *_), (c2, l2, *_) = steps[i], steps[j]
    x1, x2 = bx(c1) + BW, bx(c2)
    y1c, y2c = by(l1) + BH / 2, by(l2) + BH / 2
    c, m = (ACC, "acc") if acc else (MUTED, "ar")
    if l1 == l2:
        d.arrow([(x1, y1c), (x2 - 2, y2c)], c, m, 1.4)
    else:
        mx = x1 + GAP / 2
        d.arrow([(x1, y1c), (mx, y1c), (mx, y2c), (x2 - 2, y2c)], c, m, 1.4)

cross(0, 1); cross(1, 2); cross(2, 3); cross(3, 4, True); cross(3, 5, True)

# 마지막 열 두 조각이 한 화면이라는 표시 — 단계 상자가 아니라 묶음 주석이다
gx, gy = bx(4) - 12, by(0) - 14
gh = by(2) + BH + 14 - gy
d.o.append(f'<rect x="{gx}" y="{gy}" width="{BW + 24}" height="{gh}" rx="8" fill="none" '
           f'stroke="{ACC}" stroke-width="1.1" stroke-dasharray="5 4"/>')
lw = len("ONE VIEW") * 6.4 + 16
d.o.append(f'<rect x="{gx + 18}" y="{gy - 7}" width="{lw}" height="14" rx="2" fill="{PAPER}"/>')
d.t(gx + 18 + lw / 2, gy + 3, "ONE VIEW", 7.5, ACC, MONO)

for c, l, title, sub in steps:
    x, y = bx(c), by(l)
    d.box(x, y, BW, BH, PAPER2, RULE, 1.0, 6)
    d.t(x + 14, y + 25, title, 12.5, INK, KR, "start", 600)
    d.t(x + 14, y + 45, sub, 9, MUTED, MONO, "start")

d.legend(LEGEND_Y, [("한 화면을 두 팀이 나눠 갖는 자리", ACC), ("팀이 바뀌는 지점", MUTED)])
d.save("04-01.team-flow.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", bx(4) + BW)
