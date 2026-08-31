# 02-01 §1 컨트롤 플레인이 지는 아홉 가지 책임.
# 본문: 저자가 든 아홉을 그대로 잎으로 두고, 성격이 같은 것끼리 넷으로 묶었다. 묶음 이름은 노트가 붙인 것이다.
# 이 목록이 "서비스 메시를 도입하면 무엇을 위임하게 되는가"의 구체적 답이고, 그 대부분이 istiod 하나에 있다.
# 타입 스펙: type-tree — 뿌리 하나(istiod)에서 성격별로 갈라지고 그 아래 개별 책임이 잎이 된다.
#           깊이 3, 최대 폭 4, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 600
d = D(W, H, "ISTIO IN ACTION · 02-01 §1",
      "아홉 가지를 한 컴포넌트에 맡기는 결정",
      "저자가 든 컨트롤 플레인의 책임 아홉을 성격별로 묶었다. 대부분이 istiod 라는 단일 컴포넌트에 "
      "구현돼 있다. 색이 붙은 묶음이 1 장의 단점 셋 중 \"또 하나의 계층\"이 무엇을 뜻하는지 보이는 자리다.",
      "묶음 이름은 노트가 붙인 것이고 잎 아홉은 저자의 목록 그대로입니다")

NW, NH = 268, 48
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 20, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 38, sub, 9, MUTED, MONO)

ROOT_X, ROOT_Y = 486, 112
BUS_Y = 196
XS = [36, 336, 636, 936]
MID_Y, LEAF_Y = 232, 336

d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[3] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 3 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.2 if i == 3 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.2 if i == 3 else 1.0)

node(ROOT_X, ROOT_Y, "istiod", "대부분이 여기 한 컴포넌트에")
node(XS[0], MID_Y, "설정을 받는 자리", "API")
node(XS[1], MID_Y, "무엇이 어디 있는지", "discovery")
node(XS[2], MID_Y, "누구인지 증명", "identity")
node(XS[3], MID_Y, "메시 자신을 돌보는 일", "operations", focal=True)

def leaf(x, y, lines, focal=False):
    h = 20 + len(lines) * 20
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{h}" rx="6" fill="{ACC}0C" stroke="{ACC}88" stroke-width="1"/>')
    else:
        d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 26 + j * 20, ln, 10, MUTED, KR, "start")

leaf(XS[0], LEAF_Y, ["운영자용 라우팅·레질리언스 API", "데이터 플레인용 설정 API", "사용 정책 지정 API"])
leaf(XS[1], LEAF_Y, ["서비스 디스커버리 추상화", "네트워크 경계와 접근 방법 명세"])
leaf(XS[2], LEAF_Y, ["인증서 발급과 순환", "워크로드 아이덴티티 할당"])
leaf(XS[3], LEAF_Y, ["통합 텔레메트리 수집", "사이드카 주입"], focal=True)

d.t(32, 496, "1 장이 \"메시의 두뇌\"라고만 한 것을 2 장이 목록으로 편다", 11, SOFT, KR, "start")
d.t(32, 520, "이 목록이 도입할 때 위임하게 되는 것의 구체적 답이다", 11, MUTED, KR, "start")
d.legend(548, [("메시가 자기를 돌보려고 지는 일", ACC), ("애플리케이션을 위해 지는 일", MUTED)])
d.save("02-01.control-plane-duties.svg")
