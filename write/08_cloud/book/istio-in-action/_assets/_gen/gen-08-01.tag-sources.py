# 08-01 §6 커스텀 태그 값을 어디서 끌어오는가.
# 본문: "At the time of writing, you can configure three different types of custom tags:
#       Explicitly specifying a value / Pulling a value from environment variables /
#       Pulling a value from request headers." 저자가 든 세 갈래를 그대로 잎으로 둔다.
# 요청 헤더 갈래만 값의 가짓수를 우리가 통제하지 못한다. 그 대가는 시계열이 아니라 스팬 저장소로 간다.
# 타입 스펙: type-tree — 뿌리 하나에서 값의 출처로 갈라지고 그 아래 설정 필드가 잎이 된다.
#           깊이 3, 최대 폭 3, 연결선은 직각 엘보(대각선 금지), coral 은 잎 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1120, 572
d = D(W, H, "ISTIO IN ACTION · 08-01 §6",
      "태그 값이 오는 곳은 셋이다",
      "customTags 아래에 태그 이름을 두고, 그 값을 어디서 끌어올지 고른다. 색이 붙은 갈래만 값의 "
      "가짓수를 우리가 정하지 못한다. 저자는 세 갈래를 나열할 뿐 이 차이를 짚지 않는다.",
      "설정이 들어가는 자리는 §4 의 세 번째 자리, 곧 워크로드 애노테이션입니다")

NW, NH = 260, 52
def node(x, y, name, sub, focal=False, w=NW):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{NH}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, NH, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 22, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 9, MUTED, MONO)

ROOT_X, ROOT_Y = 430, 116
BUS_Y = 216
XS = [64, 430, 796]
MID_Y, LEAF_Y = 264, 388

# 연결선 먼저
d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[2] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 2 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.2 if i == 2 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.2 if i == 2 else 1.0)

node(ROOT_X, ROOT_Y, "customTags · custom_tag", "proxy.istio.io/config")
node(XS[0], MID_Y, "값을 직접 쓴다", "literal")
node(XS[1], MID_Y, "환경 변수에서 읽는다", "environment")
node(XS[2], MID_Y, "요청 헤더에서 뽑는다", "header", focal=True)
node(XS[0], LEAF_Y, 'value: "Test Tag"', "저자가 든 예", w=NW)
node(XS[1], LEAF_Y, "프록시 컨테이너의 값", "배포 시점에 고정", w=NW)
node(XS[2], LEAF_Y, "요청마다 달라진다", "가짓수를 우리가 못 정한다", focal=True, w=NW)

d.t(32, 474, "7 장의 차원은 시계열 개수를 늘렸고, 여기의 태그는 스팬 저장소 크기와 검색 비용을 늘린다", 11, SOFT, KR, "start")
d.t(32, 498, "저자는 이 대비를 하지 않는다 — 이 줄은 노트의 읽기다", 11, MUTED, KR, "start")
d.legend(522, [("값의 가짓수를 통제하지 못하는 갈래", ACC)])
d.save("08-01.tag-sources.svg")
