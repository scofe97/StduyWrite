# 06-05 §5 — 세 방식이 무엇을 어디서 띄우나 (원문 Testing Technical Recommendations).
# 존 안의 항목이 그 방식에서 실제로 서 있는 것이고, 아래 띠가 저자가 각 방식에 붙인 대가다.
# 타입 스펙: type-deployment — 소프트웨어가 어디서 도는가. 존마다 그 안에서 도는 것과 그 값이 붙는다.
#           축약: 06-02.environments 의 존 배치를 승계하되 넷이 아니라 셋이라 폭을 넓혔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO

W = 1240
ZW, ZH, GAP, X0, Y = 368, 268, 32, 48, 116
LEGEND_Y = Y + ZH + 36
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-05 §5",
      "세 방식이 무엇을 어디서 띄우나",
      "존 안이 그 방식에서 실제로 서 있는 것이고 맨 아래 줄이 저자가 붙인 대가다. 색이 붙은 존이 외부 의존을 없애는 방식이다.",
      "존마다 우리가 띄우는 것과 빌려 오는 것이 갈립니다")

zones = [
    ("STABLE ENVIRONMENT", "안정 환경", "모든 조각이 존재하는 환경에서 전부 돈다",
     [("우리가 띄운다", "모든 조각"), ("빌려 온다", "없음")],
     "피드백 루프가 늦어진다", False),
    ("ON-DEMAND", "온디맨드 환경", "시나리오에 필요한 자원을 한자리에 모은다",
     [("우리가 띄운다", "테스트에 필요한 전부"), ("빌려 온다", "없음")],
     "크면 복잡해지고 잘못 구성하면 비싸다", False),
    ("PROXY SERVER", "프록시 서버", "내 조각만 띄우고 나머지는 환경에서 로드한다",
     [("우리가 띄운다", "우리 팀의 조각"), ("빌려 온다", "셸과 남의 조각 · 스테이징이나 프로덕션")],
     "관리할 외부 의존이 없어진다", True),
]

for i, (eyebrow, name, desc, rows, cost, focal) in enumerate(zones):
    x = X0 + i * (ZW + GAP)
    if focal:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{ZW}" height="{ZH}" rx="8" fill="{ACC}0A" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.o.append(f'<rect x="{x}" y="{Y}" width="{ZW}" height="{ZH}" rx="8" fill="{INK}04" stroke="{INK}30" stroke-width="1.0"/>')
    lw = len(eyebrow) * 6.4 + 16
    d.o.append(f'<rect x="{x + 20}" y="{Y - 6}" width="{lw}" height="12" rx="2" fill="{PAPER}"/>')
    d.t(x + 20 + lw / 2, Y + 3, eyebrow, 7.5, ACC if focal else SOFT, MONO)
    d.t(x + 20, Y + 34, name, 14, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, Y + 56, desc, 10, MUTED, KR, "start")
    for j, (k, v) in enumerate(rows):
        by = Y + 76 + j * 56
        d.box(x + 20, by, ZW - 40, 48, PAPER2, RULE, 0.9, 5)
        d.t(x + 32, by + 20, k, 9.5, SOFT, KR, "start", 600)
        d.t(x + 32, by + 38, v, 10, MUTED, KR, "start")
    d.line(x + 20, Y + 200, x + ZW - 20, Y + 200, RULE, 0.8)
    d.t(x + 20, Y + 224, "치르는 값", 9, SOFT, MONO, "start")
    d.t(x + 20, Y + 246, cost, 10.5, ACC if focal else MUTED, KR, "start", 600 if focal else 400)

d.legend(LEGEND_Y, [("외부 의존을 없애는 방식", ACC)])
d.save("06-05.three-options.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H, " 우측끝:", X0 + 3 * ZW + 2 * GAP)
