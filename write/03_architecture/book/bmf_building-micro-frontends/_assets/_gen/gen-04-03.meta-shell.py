# 04-03 §3 — 계정 관리 뷰의 메타 셸. MyAccountMFE 는 셸에게는 리모트이고 두 조각에게는 호스트다.
# 조각 이름과 소유 팀은 원문 그대로다.
# 타입 스펙: type-architecture — 논리 경계(호스트 단계)로 묶은 구성요소와 그 사이 연결.
#           accent 는 호스트이면서 리모트인 단 하나의 상자.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, KR, MONO

W = 1200
Z_X, Z_W = 40, 1120
ZONES = [("HOST · APPLICATION SHELL", 104, 100), ("HOST + REMOTE · META SHELL", 246, 108), ("REMOTES", 396, 116)]
LEGEND_Y = 396 + 116 + 30
H = LEGEND_Y + 44

d = D(W, H, "BUILDING MICRO-FRONTENDS · 04-03 §3",
      "메타 셸은 리모트이면서 호스트다",
      "계정 관리 뷰는 두 팀의 조각이 만나는 자리라 가벼운 셸을 하나 더 둔다. 색이 붙은 상자가 위에서 보면 리모트이고 아래에서 보면 호스트다.",
      "위에서 아래로 로드가 일어납니다")

for label, y, h in ZONES:
    d.o.append(f'<rect x="{Z_X}" y="{y}" width="{Z_W}" height="{h}" rx="8" '
               f'fill="{INK}03" stroke="{INK}30" stroke-width="1.0" stroke-dasharray="4 4"/>')
    tw = len(label) * 5.6 + 14
    d.o.append(f'<rect x="{Z_X + 14}" y="{y - 8}" width="{tw}" height="16" fill="{PAPER}"/>')
    d.t(Z_X + 20, y + 4, label, 8, SOFT, MONO, "start")

def node(x, y, w, h, name, sub, note, focal=False):
    if focal:
        d.tone(x, y, w, h, ACC, 6, "12", 1.4)
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + 18, y + 26, name, 13, ACC if focal else INK, KR, "start", 600)
    d.t(x + 18, y + 44, sub, 9, ACC if focal else MUTED, MONO, "start")
    d.t(x + 18, y + 62, note, 10, MUTED, KR, "start")

node(400, 118, 400, 72, "애플리케이션 셸", "shell", "팀 사사즈시")
node(400, 260, 400, 80, "MyAccount 메타 셸", "MyAccountMFE", "팀 니기리가 소유권을 갖는다", focal=True)
node(120, 412, 440, 84, "사용자 상세 조각", "UserDetailsMFE · react17 스코프", "팀 사시미 · React 17.0.2")
node(640, 412, 440, 84, "결제 수단 조각", "UserPaymentMethodsMFE", "팀 니기리 · React 18.2.0")

d.arrow([(600, 190), (600, 260)], INFO, "info", 1.4)
d.t(614, 230, "loadRemote", 8.5, INFO, MONO, "start")
d.arrow([(540, 340), (540, 376), (340, 376), (340, 412)], INFO, "info", 1.4)
d.arrow([(660, 340), (660, 376), (860, 376), (860, 412)], INFO, "info", 1.4)
d.o.append(f'<rect x="484" y="356" width="232" height="16" fill="{PAPER}"/>')
d.t(600, 368, "registerRemotes · loadRemote", 8.5, INFO, MONO)

d.legend(LEGEND_Y, [("리모트이면서 호스트인 상자", ACC), ("런타임 로드", INFO)])
d.save("04-03.meta-shell.svg")
print("h 필요:", LEGEND_Y + 40, " 실제:", H)
