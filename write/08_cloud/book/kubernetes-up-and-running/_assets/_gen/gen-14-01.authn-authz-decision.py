# 14-01 §인증과 인가 — 요청이 거치는 두 관문
# 흔한 그림은 인증에서 거부 화살표를 빼내지만 본문은 그 반대를 못 박는다.
# "결과가 신원 없음이어도 인증은 끝난 것" 이고 system:unauthenticated 그룹이 붙어 인가로 간다.
# 그래서 인증에서 나가는 길은 둘이되 둘 다 인가로 합류해야 한다 — 이 합류가 뒤에 나올
# 익명 접근 구멍의 출발점이므로 초점으로 둔다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, BAD, MUTED, SOFT, INK, PAPER2, PAPER, RULE, KR, MONO
import ddx

W, H = 1240, 530
d = D(W, H, "KUBERNETES UP AND RUNNING · 14-01",
      "신원이 없어도 인증은 끝난 것이다",
      "모든 요청은 신원을 확립하는 인증을 먼저 지나고, 그 신원으로 무엇을 할 수 있는지 따지는 "
      "인가를 그다음에 지난다.",
      "거부는 인가에서만 나온다 — 인증은 아무도 돌려보내지 않는다")

CY = 234
ddx.node(d, 94, CY, "API 요청", "", w=140, h=68)
ddx.node(d, 309, CY, "인증", "누구인지 확정한다", w=190, h=76)

def outcome(x, w, y0, y1, title, sub, c=None, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y0}" width="{w}" height="{y1-y0}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
        tc = sc = ACC
    else:
        d.box(x, y0, w, y1 - y0, PAPER2, c or RULE, 1.1, 6)
        tc, sc = (c or INK), MUTED
    cx = x + w / 2
    d.t(cx, (y0 + y1) / 2 - 2, ddx.fit(title, 12, w - 24, title), 12, tc, KR, "middle", 600)
    if sub:
        d.t(cx, (y0 + y1) / 2 + 18, ddx.fit(sub, 11, w - 24, sub), 11, sc, KR)

outcome(454, 270, 176, 228, "신원 있음", "user 와 groups 를 얻는다")
outcome(454, 270, 240, 292, "신원 없음", "system:unauthenticated 그룹", focal=True)

# 두 길은 인증의 오른쪽 변에서 각자 나간다. 한 점에서 같이 나가면 뒤에 그리는 초점색이
# 공유 구간을 덮어, 신원 있음이 신원 없음 경로에서 갈라진 가지처럼 읽힌다.
d.path("M 404 216 L 429 216 L 429 202 L 450 202", MUTED, 1.4, m="ar")
d.path("M 404 252 L 429 252 L 429 266 L 450 266", ACC, 1.4, m="acc")
d.path("M 724 202 L 754 202 L 754 234 L 780 234", MUTED, 1.4, m="ar")
d.path("M 724 266 L 754 266 L 754 234", ACC, 1.4)
d.t(754, 322, "둘 다 인가로 간다", 11, ACC, KR)

d.box(784, 162, 200, 144, PAPER2, RULE, 1.1, 6)
d.t(884, 188, "인가", 13, INK, KR, "middle", 600)
for i, (lab, sub) in enumerate((("신원", ""), ("리소스", "사실상 HTTP 경로"), ("동사", ""))):
    yy = 210 + i * 32
    d.o.append(f'<rect x="802" y="{yy}" width="164" height="24" rx="4" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.8"/>')
    d.t(812, yy + 16, lab, 11, INK, KR, "start")
    if sub: d.t(958, yy + 16, sub, 9, SOFT, KR, "end")

outcome(1044, 172, 176, 228, "요청이 진행된다", "", c=OK)
outcome(1044, 172, 240, 292, "HTTP 403", "", c=BAD)
d.path("M 984 202 L 1040 202", OK, 1.4, m="ok")
d.path("M 984 266 L 1040 266", BAD, 1.4, m="bad")
d.t(1012, 190, "규칙과 맞는다", 9, SOFT, KR)
d.t(1012, 254, "맞지 않는다", 9, SOFT, KR)

d.t(309, 348, "쿠버네티스는 자체 신원 저장소가 없다", 10, SOFT, KR)
d.t(309, 366, "사용자와 그룹은 인증 제공자가 공급한다", 10, SOFT, KR)
d.t(884, 348, "셋의 조합이 허용된 규칙과 맞아야 한다", 10, SOFT, KR)

BT, BB = 390, 452
d.box(12, BT, W - 36, BB - BT, PAPER, RULE, 1.0, 8)
d.t(W / 2, BT + 26,
    "RBAC 은 방어의 한 겹일 뿐이다. 클러스터 안에서 임의의 코드를 실행할 수 있는 사람은 사실상 전체 root 권한에 닿는다.",
    11, MUTED, KR)
d.t(W / 2, BT + 46,
    "서로 신뢰하지 않는 테넌트를 한 클러스터에 태운다면 하이퍼바이저 격리나 컨테이너 샌드박스가 더 필요하다.",
    11, MUTED, KR)

d.legend(BB + 24, [("신원 없음도 인증의 결과", ACC), ("진행", OK), ("거부", BAD)])
d.save("14-01.authn-authz-decision.svg")
print("h 필요:", BB + 24 + 48, " 실제:", H)
