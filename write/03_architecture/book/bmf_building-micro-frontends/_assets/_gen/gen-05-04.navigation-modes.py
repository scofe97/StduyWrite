# 05-04 §3 — 존 안에서 움직일 때와 존을 건널 때 내비게이션이 갈린다. 저자가 적은 두 상태와 그 방아쇠다.
# 타입 스펙: type-state — 유한한 상태와 그 사이 전이. accent 는 독자가 알아채야 할 상태 하나.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
SW, SH, SY = 320, 80, 176
XS = (140, 780)
MY = SY + SH / 2
BACK_Y = SY + SH + 92
LEGEND_Y = BACK_Y + 166
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 05-04 §3",
      "존을 건너면 페이지가 다시 뜬다",
      "같은 존 안의 이동은 Next.js 가 처리해 빠르다. 존 경계를 넘는 순간 리소스가 통째로 갈리고, 색이 붙은 상태가 그 대가를 치르는 자리다.",
      "화살표 위 글이 그 전이를 일으키는 방아쇠입니다")

d.o.append(f'<circle cx="46" cy="{MY}" r="6" fill="{INK}"/>')
d.arrow([(54, MY), (XS[0] - 2, MY)], MUTED, "ar", 1.4)

d.arrow([(XS[0] + SW, MY), (XS[1] - 2, MY)], ACC, "acc", 1.5)
d.t((XS[0] + SW + XS[1]) / 2, MY - 30, "존 경계를 넘는 링크를 누른다", 10.5, ACC, KR)
d.t((XS[0] + SW + XS[1]) / 2, MY - 12, "/ 에서 /dashboard 로", 9.5, ACC, MONO)
d.path(f"M {XS[1] + SW / 2} {SY + SH} V {BACK_Y} H {XS[0] + SW / 2} V {SY + SH + 2}", MUTED, 1.4, m="ar")
d.t((XS[0] + XS[1]) / 2 + SW / 2, BACK_Y + 20, "새 존 안에서는 다시 소프트 내비게이션으로 돌아간다", 10, MUTED, KR)

states = [
    ("소프트 내비게이션", "Next.js 가 처리한다 · 전체 리로드 없음", False),
    ("하드 내비게이션", "현재 존 리소스를 내리고 새 존을 로드한다", True),
]
for x, (name, sub, focal) in zip(XS, states):
    if focal:
        d.tone(x, SY, SW, SH, ACC, 8, "14", 1.4)
        d.t(x + SW / 2, SY + 34, name, 15, ACC, KR, "middle", 600)
        d.t(x + SW / 2, SY + 58, sub, 10, ACC, KR)
    else:
        d.box(x, SY, SW, SH, PAPER2, RULE, 1.0, 8)
        d.t(x + SW / 2, SY + 34, name, 15, INK, KR, "middle", 600)
        d.t(x + SW / 2, SY + 58, sub, 10, MUTED, KR)

# 대가를 줄이는 네 가지 — 상태가 아니라 주석 띠로 둔다
d.box(140, BACK_Y + 44, 960, 62, f"{INK}05", RULE, 0.8, 6)
d.t(160, BACK_Y + 68, "줄이는 법", 11, INK, KR, "start", 600)
d.t(250, BACK_Y + 68, "prefetch · prerender · 존을 건너는 링크는 <a> 태그로", 10.5, MUTED, KR, "start")
d.t(250, BACK_Y + 90, "자주 함께 가는 존은 한 애플리케이션으로 묶는다 · rewrites 와 middleware 로 라우팅을 다듬는다", 10.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("대가를 치르는 상태", ACC)])
d.save("05-04.navigation-modes.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
