# 01-01 §2 애플리케이션 네트워킹 패턴 여덟.
# 본문: 저자가 든 여덟을 그대로 잎으로 두고, 무엇을 막는지에 따라 셋으로 묶었다. 묶음 이름은 노트가 붙인 것이다.
#       저자는 이 패턴들이 네트워킹 하위 계층의 유사 구성요소와 겹치지만 패킷이 아니라 메시지 계층에서
#       동작한다는 점이 다르다고 선을 긋는다.
# 재시도에 단서가 붙는다 — 이미 과부하면 재시도가 하류 문제를 키우고, 이전 시도의 성공 여부도 알 수 없다.
# 타입 스펙: type-tree — 뿌리 하나에서 막으려는 것으로 갈라지고 그 아래 패턴이 잎이 된다.
#           깊이 3, 최대 폭 3, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1200, 616
d = D(W, H, "ISTIO IN ACTION · 01-01 §2",
      "여덟 패턴이 막으려는 것은 셋이다",
      "저자가 든 여덟을 무엇을 막는지로 묶었다. 색이 붙은 갈래만 저자가 단서를 답니다 — 재시도는 "
      "이미 과부하인 하류의 문제를 키울 수 있어 예산이라는 별도 패턴이 따라붙는다.",
      "패킷이 아니라 메시지 계층에서 동작한다는 점이 하위 계층 구성요소와 다릅니다")

NW, NH = 320, 48
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 20, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 38, sub, 9, MUTED, MONO)

ROOT_X, ROOT_Y = 420, 112
BUS_Y = 196
XS = [40, 420, 800]
MID_Y, LEAF_Y = 232, 336

d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[2] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 2 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.2 if i == 2 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.2 if i == 2 else 1.0)

node(ROOT_X, ROOT_Y, "애플리케이션 네트워킹", "패턴 여덟")
node(XS[0], MID_Y, "어디로 보낼지 고른다", "routing")
node(XS[1], MID_Y, "언제 포기할지 정한다", "give up")
node(XS[2], MID_Y, "번지지 않게 막는다", "containment", focal=True)

def leaf(x, y, lines, focal=False):
    h = 20 + len(lines) * 22
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{h}" rx="6" fill="{ACC}0C" stroke="{ACC}88" stroke-width="1"/>')
    else:
        d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 28 + j * 22, ln, 10, MUTED, KR, "start")

leaf(XS[0], LEAF_Y, ["클라이언트 사이드 로드밸런싱", "서비스 디스커버리"])
leaf(XS[1], LEAF_Y, ["타임아웃", "데드라인", "재시도"])
leaf(XS[2], LEAF_Y, ["서킷 브레이킹", "벌크헤딩", "재시도 예산"], focal=True)

d.t(32, 508, "재시도는 두 갈래에 걸친다 — 다시 보내는 일은 가운데, 그 횟수를 묶는 예산은 오른쪽이다", 11, SOFT, KR, "start")
d.t(32, 532, "이미 과부하라면 재시도가 하류 문제를 키우고, 이전 시도가 실패했다고 확신할 수도 없다", 11, MUTED, KR, "start")
d.legend(560, [("저자가 단서를 다는 갈래", ACC), ("나머지 갈래", MUTED)])
d.save("01-01.patterns-eight.svg")
