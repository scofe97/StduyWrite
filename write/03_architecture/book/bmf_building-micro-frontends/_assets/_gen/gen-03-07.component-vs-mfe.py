# 03-07 §2 — 웹 컴포넌트가 컴포넌트와 조각 양쪽에 쓰이기 때문에 선이 흐려진다.
# 두 집합의 성질은 저자의 문장 그대로다 — "컴포넌트는 확장에 열려 있어야 하고,
# 조각은 확장에 닫혀 있되 통신에 열려 있어야 한다".
# 타입 스펙: type-venn — 두 집합의 겹침이 논지다. accent 는 초점이 되는 교집합 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W = 1020
CY, R = 306, 180
AX, BX = 400, 620
LEGEND_Y = CY + R + 60
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-07 §2",
      "웹 컴포넌트는 두 집합에 걸쳐 있다",
      "왼쪽은 재사용을 위한 기술 해법이고 오른쪽은 서브도메인의 비즈니스 표현이다. 색이 붙은 겹침이 선이 흐려지는 자리다.",
      "겹치는 부분이 웹 컴포넌트가 조각의 래퍼로 쓰일 때입니다")

d.o.append(f'<circle cx="{AX}" cy="{CY}" r="{R}" fill="{INK}0A" stroke="{INK}" stroke-width="1.0"/>')
d.o.append(f'<circle cx="{BX}" cy="{CY}" r="{R}" fill="{MUTED}0D" stroke="{MUTED}" stroke-width="1.0"/>')

# 집합 라벨 — 원 바깥, 획을 건드리지 않는다
d.t(300, 108, "COMPONENT", 8, SOFT, MONO)
d.t(300, 130, "컴포넌트", 15, INK, KR, "middle", 600)
d.t(720, 108, "MICRO-FRONTEND", 8, SOFT, MONO)
d.t(720, 130, "마이크로 프론트엔드", 15, INK, KR, "middle", 600)

for i, line in enumerate(["확장에 열려 있다", "속성으로 동작을 바꾼다", "재사용을 위한 기술 해법"]):
    d.t(322, 262 + i * 30, line, 11.5, MUTED, KR)
for i, line in enumerate(["확장에 닫혀 있다", "통신에는 열려 있다", "서브도메인의 비즈니스 표현"]):
    d.t(700, 262 + i * 30, line, 11.5, MUTED, KR)

# 교집합 — 렌즈 안에 칩 하나만 두고 설명은 아래로 뺀다
d.chip(510, CY, "웹 컴포넌트", ACC, 10)
d.line(510, CY + 12, 510, CY + R + 18, ACC, 1.0, "4 4")
d.t(510, CY + R + 38, "래퍼가 동작을 커스터마이즈하게 두면 도메인 로직이 밖으로 샌다", 11, ACC, KR)

d.legend(LEGEND_Y, [("선이 흐려지는 자리", ACC)])
d.save("03-07.component-vs-mfe.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
