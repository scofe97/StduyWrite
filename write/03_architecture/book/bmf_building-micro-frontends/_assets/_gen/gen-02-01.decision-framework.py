# 02-01 §1 — 결정 프레임워크 네 영역. 저자는 "첫 결정이 나머지에 큰 영향을 준다"고 못 박으므로
# 넷을 나란히 놓지 않고 정의를 뿌리로 두고 나머지 셋을 그 아래에 단다.
# 타입 스펙: type-tree — 부모(정의) → 자식(조합 · 라우팅 · 통신) 관계. 뿌리 하나에만 accent 를 준다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1080, 416
NW, NH = 176, 52
d = D(W, H, "BUILDING MICRO-FRONTENDS · 02-01 §1",
      "먼저 정해야 나머지가 굳는다 — 결정 네 영역",
      "저자가 든 네 가지 선결 결정. 정의가 뿌리이고 조합·라우팅·통신이 그 아래에서 갈린다.",
      "위가 첫 결정이고 아래 셋이 그 결정에 매달립니다")

ROOT_X, ROOT_Y = (W - NW) / 2, 108
CHILD_Y = 260
kids = [("조합", "composing", "어디서 합칠 것인가"),
        ("라우팅", "routing", "어디서 고를 것인가"),
        ("통신", "communicating", "무엇으로 주고받을 것인가")]
GAP = 72
X0 = (W - (3 * NW + 2 * GAP)) / 2
def kx(i): return X0 + i * (NW + GAP)

# 연결선 먼저 — 직각 엘보, 대각선 금지
BUS_Y = 212
d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, MUTED, 1.1)
d.line(kx(0) + NW / 2, BUS_Y, kx(2) + NW / 2, BUS_Y, MUTED, 1.1)
for i in range(3):
    d.arrow([(kx(i) + NW / 2, BUS_Y), (kx(i) + NW / 2, CHILD_Y - 2)], MUTED, "ar", 1.1)

d.o.append(f'<rect x="{ROOT_X}" y="{ROOT_Y}" width="{NW}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(ROOT_X + NW / 2, ROOT_Y + 24, "정의", 14, ACC, KR, "middle", 600)
d.t(ROOT_X + NW / 2, ROOT_Y + 42, "defining", 9, SOFT, MONO)
# 캡션을 가운데 두면 아래로 내려가는 연결선이 글자를 관통한다. 상자 오른쪽으로 뺀다.
d.t(ROOT_X + NW + 20, ROOT_Y + 32, "무엇을 하나의 마이크로 프론트엔드로 볼 것인가", 12, MUTED, KR, "start")

for i, (ko, en, q) in enumerate(kids):
    x = kx(i)
    d.box(x, CHILD_Y, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + NW / 2, CHILD_Y + 24, ko, 14, INK, KR, "middle", 600)
    d.t(x + NW / 2, CHILD_Y + 42, en, 9, SOFT, MONO)
    d.t(x + NW / 2, CHILD_Y + 72, q, 11, MUTED, KR)

LEGEND_Y = CHILD_Y + 72 + 24          # 질문 글자 아래 24px — 관통 방지
d.legend(LEGEND_Y, [("나머지를 구속하는 첫 결정", ACC)])
d.save("02-01.decision-framework.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
