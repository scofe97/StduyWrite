# 03-07 §3 — 웹 컴포넌트끼리 라이브러리를 공유하려고 전역 window 에 올릴 때 생기는 일.
# 저자의 이커머스 예(상품 목록 · 장바구니 · 체크아웃)를 그대로 쓴다. window 는 라이브러리마다 한 버전만 담는다.
# 타입 스펙: type-dependency — 트리로 못 그리는 fan-in 이 논지다. 되돌아오는 간선은 없으므로 accent 는 충돌 지점 하나에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1060
NW, NH = 300, 64
R0_Y, R1_Y = 124, 252
mfes = [("상품 목록", "MobX 6", 40), ("장바구니", "MobX 6", 380), ("체크아웃", "MobX 5", 720)]
GX, GW = 340, 380
LEGEND_Y = R1_Y + NH + 54
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-07 §3",
      "전역 window 는 라이브러리마다 한 버전만 담는다",
      "세 조각이 같은 자리에 자기 라이브러리를 올리려 한다. 색이 붙은 곳이 버전이 갈릴 때 부딪히는 지점이다.",
      "아래로 내려가는 화살표가 같은 자리에 올린다는 뜻입니다")

def node(x, y, w, name, sub, fanin, focal=False):
    if focal:
        d.tone(x, y, w, NH, ACC, 6, "14", 1.4)
    else:
        d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, y + 28, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 46, sub, 9.5, ACC if focal else MUTED, MONO, "start")
    bw = 34
    d.o.append(f'<rect x="{x + w - bw - 12}" y="{y + 10}" width="{bw}" height="15" rx="2" '
               f'fill="{PAPER}" stroke="{ACC if focal else RULE}" stroke-width="0.8"/>')
    d.t(x + w - bw / 2 - 12, y + 21, f"{fanin} in", 8, ACC if focal else SOFT, MONO)

for name, sub, x in mfes:
    node(x, R0_Y, NW, name, sub, 0)
node(GX, R1_Y, GW, "window 전역 객체", "라이브러리마다 한 버전", 3, True)

my = (R0_Y + NH + R1_Y) / 2
for (_, _, x), ax in zip(mfes, (GX + 70, GX + GW / 2, GX + GW - 70)):
    cx = x + NW / 2
    if abs(cx - ax) < 2:
        d.arrow([(cx, R0_Y + NH), (ax, R1_Y)], MUTED, "ar", 1.4)
    else:
        d.arrow([(cx, R0_Y + NH), (cx, my), (ax, my), (ax, R1_Y)], MUTED, "ar", 1.4)

d.t(W / 2, R1_Y + NH + 32, "버전이 갈리면 나중에 올린 쪽이 이기고, 진 쪽은 예상 못한 동작을 만난다", 10.5, MUTED, KR)
d.legend(LEGEND_Y, [("버전이 하나만 남는 자리", ACC), ("같은 자리에 올린다", MUTED)])
d.save("03-07.global-window.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
