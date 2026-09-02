# 06-01 §5 — 자동화 책임이 갈리는 자리 (원문 Empower Your Teams · Define Your Guardrails).
# 노드 이름과 소유 항목은 원문 서술 그대로다. "배포는 같고 빌드는 다르다"는 아래 각주 띠로 옮겼다.
# 타입 스펙: type-org-chart — 노드가 조직이고 물어야 할 것이 "누가 무엇을 갖는가"다. accent 는 권한이 내려간 쪽.
#           축약: 03-04.team-ownership 의 RW/NW/BUS 기하를 승계하되 자식이 둘이라 XS 를 두 칸으로 줄였다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W = 1240
RW, RH, RY = 480, 100, 108
NW, NH, NY = 480, 132, 268
XS = (100, 660)
BUS_Y = RY + RH + 32
FOOT_Y = NY + NH + 40
LEGEND_Y = FOOT_Y + 76
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 06-01 §5",
      "자동화 책임이 갈리는 자리",
      "위가 경계를 정하는 쪽이고 아래가 그 안에서 움직이는 두 조직이다. 색이 붙은 쪽이 저자가 권한을 내려보내라고 한 자리다.",
      "노드마다 그 조직이 소유하는 것이 붙습니다")

# 연결선 먼저 — z-order
d.line(W / 2, RY + RH, W / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[1] + NW / 2, BUS_Y, MUTED, 1.0)
for x in XS:
    d.line(x + NW / 2, BUS_Y, x + NW / 2, NY, MUTED, 1.0)

# 뿌리 — 경계를 정하는 쪽
d.box((W - RW) / 2, RY, RW, RH, PAPER2, RULE, 1.0, 6)
d.t(W / 2, RY + 32, "기술 리더십", 14, INK, KR, "middle", 600)
d.t(W / 2, RY + 52, "tech leadership", 9, MUTED, MONO)
d.t(W / 2, RY + 76, "아키텍트 · 플랫폼 · 클라우드 엔지니어가 함께 가드레일을 정한다", 10.5, MUTED)

orgs = [
    ("플랫폼 팀", "platform", False,
     ["자동화 전략을 돌리는 도구", "지속 전달에 쓰는 배포 대시보드", "아키텍처 특성을 강제하는 피트니스 함수"]),
    ("개발 팀", "product team", True,
     ["아티팩트를 만드는 스크립트와 단계", "자기 조각의 빌드 도구와 최적화", "그 코드로 최적화하는 최선을 아는 쪽"]),
]
for x, (name, en, focal, lines) in zip(XS, orgs):
    if focal:
        d.o.append(f'<rect x="{x}" y="{NY}" width="{NW}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, NY, NW, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, NY + 30, name, 13.5, ACC if focal else INK, KR, "start", 600)
    d.t(x + 20, NY + 48, en, 9, MUTED, MONO, "start")
    for i, ln in enumerate(lines):
        d.t(x + 20, NY + 74 + i * 20, "· " + ln, 10.5, MUTED, KR, "start")

# 각주 띠 — 무엇이 같고 무엇이 갈리는가
d.box(100, FOOT_Y, W - 200, 60, f"{INK}05", RULE, 0.8, 6)
d.t(120, FOOT_Y + 24, "배포 단계", 11, INK, KR, "start", 600)
d.t(230, FOOT_Y + 24, "프로젝트의 모든 조각에서 같다", 10.5, MUTED, KR, "start")
d.t(120, FOOT_Y + 46, "빌드 파이프라인", 11, INK, KR, "start", 600)
d.t(230, FOOT_Y + 46, "조각마다 다른 도구나 최적화를 쓸 수 있다 · 중앙화하면 결과가 나빠질 수 있다", 10.5, MUTED, KR, "start")

d.legend(LEGEND_Y, [("권한을 내려보내라고 한 자리", ACC)])
d.save("06-01.ownership.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
