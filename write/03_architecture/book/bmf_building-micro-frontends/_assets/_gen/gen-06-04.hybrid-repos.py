# 06-04 §3 — 서브도메인으로 묶는 하이브리드 (원문 Figure 6-3 과 A Possible Future 절).
# 저장소 경계를 팀이 아니라 바운디드 컨텍스트에 맞춘다. 같은 서브도메인 안은 모노레포처럼, 사이는 계약으로.
# 타입 스펙: type-tree — 부모에서 자식으로 내려가는 포함 관계. 형제 사이의 계약은 점선으로 따로 표시한다.
#           축약: 스펙의 트리는 형제 사이 간선을 두지 않지만, 이 절의 논지가 "형제는 계약으로 잇는다"라서
#           형제 간선 하나를 점선으로 더했다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
RX, RY, RW, RH = 380, 108, 480, 84
L1Y, L1W, L1H = 256, 480, 92
L1X = (100, 660)
L2Y, L2W, L2H, L2GAP = 388, 140, 72, 20
BUS_Y = RY + RH + 32
LEGEND_Y = L2Y + L2H + 40
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-04 §3",
      "서브도메인으로 묶는 하이브리드",
      "저장소 경계를 팀이 아니라 바운디드 컨텍스트에 맞춘다. 색이 붙은 점선이 서브도메인 사이를 잇는 유일한 경로다.",
      "같은 서브도메인 안은 모노레포처럼, 사이는 계약으로 일합니다")

# 간선 먼저 — z-order
d.line(W / 2, RY + RH, W / 2, BUS_Y, MUTED, 1.0)
d.line(L1X[0] + L1W / 2, BUS_Y, L1X[1] + L1W / 2, BUS_Y, MUTED, 1.0)
for x in L1X:
    d.line(x + L1W / 2, BUS_Y, x + L1W / 2, L1Y, MUTED, 1.0)

subs = [
    ("카탈로그 서브도메인", "bounded context", ["상품 목록", "상품 상세", "검색"]),
    ("체크아웃 서브도메인", "bounded context", ["장바구니", "결제 수단", "주문 확인"]),
]
for x, (name, en, projects) in zip(L1X, subs):
    for j in range(len(projects)):
        px = x + 10 + j * (L2W + L2GAP)
        d.line(px + L2W / 2, L1Y + L1H, px + L2W / 2, L2Y, MUTED, 0.9)

# 뿌리
d.box(RX, RY, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(W / 2, RY + 34, "도메인 주도 설계로 나눈 시스템", 13.5, INK, KR, "middle", 600)
d.t(W / 2, RY + 58, "서브도메인과 바운디드 컨텍스트의 구분을 그대로 따른다", 10.5, MUTED)

# 서브도메인 저장소
for x, (name, en, projects) in zip(L1X, subs):
    d.box(x, L1Y, L1W, L1H, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, L1Y + 34, name, 13, INK, KR, "start", 600)
    d.t(x + 20, L1Y + 56, en, 9, MUTED, MONO, "start")
    d.t(x + L1W - 20, L1Y + 34, "저장소 하나", 10.5, MUTED, KR, "end", 600)
    d.t(x + L1W - 20, L1Y + 56, "안에서는 모노레포의 강점", 9.5, SOFT, KR, "end")
    for j, p in enumerate(projects):
        px = x + 10 + j * (L2W + L2GAP)
        d.box(px, L2Y, L2W, L2H, PAPER2, RULE, 0.9, 5)
        d.t(px + L2W / 2, L2Y + 42, p, 11, MUTED, KR, "middle", 600)

# 형제 사이의 계약 — 이 절의 논지
MID_Y = L1Y + L1H / 2
d.path(f"M {L1X[0] + L1W} {MID_Y} L {L1X[1] - 2} {MID_Y}", ACC, 1.4, m="acc", dash="5 5")
lw = 66
d.o.append(f'<rect x="{(L1X[0] + L1W + L1X[1]) / 2 - lw / 2}" y="{MID_Y - 22}" width="{lw}" height="16" fill="{PAPER}"/>')
d.t((L1X[0] + L1W + L1X[1]) / 2, MID_Y - 10, "계약", 10, ACC, KR, "middle", 600)

d.legend(LEGEND_Y, [("서브도메인 사이를 잇는 유일한 경로", ACC)])
d.save("06-04.hybrid-repos.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", L1X[1] + L1W)
