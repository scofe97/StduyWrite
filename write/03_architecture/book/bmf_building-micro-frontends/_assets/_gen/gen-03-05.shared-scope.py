# 03-05 §3 — 같은 라이브러리를 여럿이 쓸 때 Module Federation 이 무엇을 보고 갈라지는가.
# 타입 스펙: type-flowchart — 조건에 따라 갈라지는 판단. 모양이 종류를 나르고 색은 한 갈래에만 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1000
S_Y, D_CY, B_Y, R_Y = 104, 216, 312, 400
NH, RH = 52, 52
LEFT, RIGHT = 250, 750
LEGEND_Y = R_Y + RH + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 03-05 §3",
      "버전이 같으냐가 갈림길이다",
      "여러 조각이 같은 라이브러리를 쓸 때 Module Federation 이 버전을 보고 두 길로 나눈다. 색이 붙은 갈래가 성능을 버는 쪽이다.",
      "마름모가 판단이고 사각형이 그 결과입니다")

# 연결선 먼저
d.arrow([(500, S_Y + NH), (500, D_CY - 46)], MUTED, "ar", 1.4)
d.arrow([(370, D_CY), (LEFT, D_CY), (LEFT, B_Y)], ACC, "acc", 1.5)
d.arrow([(630, D_CY), (RIGHT, D_CY), (RIGHT, B_Y)], MUTED, "ar", 1.4)
d.arrow([(LEFT, B_Y + NH), (LEFT, R_Y)], MUTED, "ar", 1.4)
d.arrow([(RIGHT, B_Y + NH), (RIGHT, R_Y)], MUTED, "ar", 1.4)

# 시작
d.box(500 - 170, S_Y, 340, NH, PAPER2, RULE, 1.0, 6)
d.t(500, S_Y + 24, "여러 조각이 같은 라이브러리를 쓴다", 12.5, INK, KR, "middle", 600)
d.t(500, S_Y + 41, "설정에서 shared 로 선언", 9, MUTED, MONO)

# 판단 — 마름모
d.o.append(f'<polygon points="500,{D_CY-46} 630,{D_CY} 500,{D_CY+46} 370,{D_CY}" '
           f'fill="{PAPER2}" stroke="{MUTED}" stroke-width="1.2"/>')
d.t(500, D_CY + 5, "버전이 같은가", 12.5, INK, KR, "middle", 600)
d.t(LEFT + 14, D_CY + 46, "같다", 9.5, ACC, MONO, "start")
d.t(RIGHT + 14, D_CY + 46, "다르다", 9.5, MUTED, MONO, "start")

# 두 갈래
d.tone(LEFT - 145, B_Y, 290, NH, ACC, 6, "14", 1.3)
d.t(LEFT, B_Y + 24, "싱글턴으로 묶는다", 12.5, ACC, KR, "middle", 600)
d.t(LEFT, B_Y + 41, "shared singleton", 9, ACC, MONO)

d.box(RIGHT - 145, B_Y, 290, NH, PAPER2, RULE, 1.0, 6)
d.t(RIGHT, B_Y + 24, "컨테이너로 감싼다", 12.5, INK, KR, "middle", 600)
d.t(RIGHT, B_Y + 41, "container scope", 9, MUTED, MONO)

# 결과
d.box(LEFT - 145, R_Y, 290, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(LEFT, R_Y + 24, "런타임에 한 번만 로드", 12, INK, KR, "middle", 600)
d.t(LEFT, R_Y + 41, "내려받는 양이 준다", 9.5, MUTED, KR)

d.box(RIGHT - 145, R_Y, 290, RH, f"{INK}08", MUTED, 0.8, 6)
d.t(RIGHT, R_Y + 24, "버전마다 따로 로드", 12, INK, KR, "middle", 600)
d.t(RIGHT, R_Y + 41, "충돌은 없지만 양은 는다", 9.5, MUTED, KR)

d.legend(LEGEND_Y, [("성능을 버는 갈래", ACC)])
d.save("03-05.shared-scope.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
