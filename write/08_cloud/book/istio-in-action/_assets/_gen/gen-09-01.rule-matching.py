# 09-01 §6 규칙 하나가 걸리는 조건.
# 본문(저자 9.3.9): from 에 정의된 출처 하나와 to 에 정의된 작업 하나가 AND 로 묶이고, 거기에 when 의
#       조건 전부가 다시 AND 로 묶인다. 같은 묶음 안의 항목끼리는 OR 이고, 작업 하나 안의 속성은 다시 AND 다.
# 잎은 저자의 예제(9.3.9)에서 그대로 가져왔다.
# 타입 스펙: type-tree — 뿌리 하나(rule)에서 세 묶음으로 갈라지고 그 아래 항목이 잎이 된다.
#           깊이 3, 최대 폭 3, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1200, 640
d = D(W, H, "ISTIO IN ACTION · 09-01 §6",
      "묶음 사이는 AND, 묶음 안은 OR",
      "규칙 하나가 발동하려면 출처 하나와 작업 하나가 맞고 조건이 전부 맞아야 한다. 색이 붙은 묶음만 "
      "전부 맞아야 하고 나머지 둘은 하나만 맞으면 된다. 작업 하나 안의 속성은 다시 전부 맞아야 한다.",
      "from 을 빼면 출처를 따지지 않아 인증되지 않은 요청도 들어옵니다")

NW, NH = 300, 52
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 22, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 11, MUTED, MONO)

ROOT_X, ROOT_Y = 450, 116
BUS_Y = 210
XS = [60, 450, 840]
MID_Y, LEAF_Y = 256, 380

d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[2] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 2 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.2 if i == 2 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.2 if i == 2 else 1.0)

node(ROOT_X, ROOT_Y, "rule 하나", "셋이 모두 맞아야 발동")
node(XS[0], MID_Y, "from — 출처", "하나만 맞으면 된다 · OR")
node(XS[1], MID_Y, "to — 작업", "하나만 맞으면 된다 · OR")
node(XS[2], MID_Y, "when — 조건", "전부 맞아야 한다 · AND", focal=True)

def leaf(x, y, lines, focal=False):
    h = 24 + len(lines) * 20
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{h}" rx="6" fill="{ACC}0C" stroke="{ACC}88" stroke-width="1"/>')
    else:
        d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 28 + j * 20, ln, 11, MUTED, MONO, "start")

leaf(XS[0], LEAF_Y, ["principals: [ … /sa/webapp ]", "namespaces: [\"default\"]", "ipBlocks: [ CIDR ]"])
leaf(XS[1], LEAF_Y, ["methods: [\"GET\"]  paths: [\"/users*\"]", "methods: [\"POST\"] paths: [\"/data\"]", "한 작업 안의 두 속성은 AND"])
leaf(XS[2], LEAF_Y, ["key: request.auth.claims[group]", "values: [beta-tester, admin, …]", "조건이 여럿이면 전부 AND"], focal=True)

d.t(32, 530, "앞의 둘은 상호 인증이 되어 있어야 작동한다 — 출처를 상대 SVID 에서 꺼내 오기 때문이다", 11, SOFT, KR, "start")
d.t(32, 554, "값 비교는 완전 일치 · 접두 · 접미 · 존재 확인 넷을 쓴다", 11, MUTED, KR, "start")
d.legend(584, [("전부 맞아야 하는 묶음", ACC), ("하나만 맞으면 되는 묶음", MUTED)])
d.save("09-01.rule-matching.svg")
