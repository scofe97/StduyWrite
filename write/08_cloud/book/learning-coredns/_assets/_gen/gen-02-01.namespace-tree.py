# 02-01 §1 — 이름공간은 루트를 위에 둔 역트리이고, 노드에서 루트까지의 레이블 경로가 곧 도메인 이름이다.
# 원문 근거: "DNS's namespace is an inverted tree, with the root node at the top", 레이블 최대 63 ASCII 자,
#            루트만 길이 0 의 null 레이블, 한 노드의 자식 레이블은 서로 달라야 한다,
#            "A node's domain name is the list of labels on the path from that node upward to the root".
#            노드 이름은 원서 Figure 2-1·2-2 의 (반)가공 이름공간을 따른다.
# 타입 스펙: type-tree — 부모에서 자식으로 갈라지는 계보이고 루트까지의 경로가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 940, 580
d = D(W, H, "LEARNING COREDNS · 02-01 §1",
      "레이블을 루트까지 이어 붙인 것이 도메인 이름",
      "이름공간은 루트를 맨 위에 둔 뒤집힌 트리다. 레이블은 노드를 형제와 구분할 뿐이고, "
      "그 노드를 이름공간 전체에서 가리키려면 루트까지의 레이블을 점으로 이어 붙여야 한다.",
      "색이 붙은 노드의 이름이 www.baz.example 입니다")

NW, NH = 176, 52
ROOT_Y, T2_Y, T3_Y, T4_Y = 96, 192, 288, 384
CX3 = [180, 470, 760]

d.line(470, ROOT_Y + NH, 470, T2_Y, MUTED, 1.0)
d.line(470, T2_Y + NH, 470, 264, MUTED, 1.0)
d.line(CX3[0], 264, CX3[2], 264, MUTED, 1.0)
for cx in CX3:
    d.line(cx, 264, cx, T3_Y, MUTED, 1.0)
d.line(760, T3_Y + NH, 760, T4_Y, MUTED, 1.0)

def node(cx, y, name, sub, focal=False):
    if focal:
        d.tone(cx - NW / 2, y, NW, NH, ACC, 6, "12", 1.4)
    else:
        d.box(cx - NW / 2, y, NW, NH, PAPER2, RULE, 1.0)
    d.t(cx, y + 24, name, 14, ACC if focal else INK, MONO, "middle", 600)
    d.t(cx, y + 44, sub, 12, MUTED)

node(470, ROOT_Y, ".", "null 레이블 · 길이 0")
node(470, T2_Y, "example", "레이블 최대 63자")
node(CX3[0], T3_Y, "foo", "")
node(CX3[1], T3_Y, "bar", "")
node(CX3[2], T3_Y, "baz", "형제끼리 레이블이 달라야")
node(760, T4_Y, "www", "", focal=True)

d.t(12, ROOT_Y + 30, "루트", 12, SOFT, KR, "start")
d.t(12, T2_Y + 30, "1단계", 12, SOFT, KR, "start")
d.t(12, T3_Y + 30, "2단계", 12, SOFT, KR, "start")
d.t(12, T4_Y + 30, "3단계", 12, SOFT, KR, "start")

d.path("M 856 404 L 892 404 L 892 118 L 566 118", ACC, 1.2, m="acc", dash="5 4")
d.t(470, 460, "www . baz . example", 16, ACC, MONO, "middle", 600)
d.t(470, 482, "아래에서 위로 읽어 점으로 잇는다", 13, MUTED, KR)

d.legend(512, [("이름을 물은 노드", ACC)])
d.save("02-01.namespace-tree.svg")
