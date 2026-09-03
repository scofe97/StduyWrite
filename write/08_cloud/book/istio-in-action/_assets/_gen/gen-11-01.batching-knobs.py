# 11-01 §7 배칭과 스로틀링을 정하는 환경변수 넷.
# 본문(원문 11.3.4): PILOT_DEBOUNCE_AFTER 는 이벤트를 푸시 큐에 넣는 것을 미루는 시간이고 기본 100ms 다.
#       PILOT_DEBOUNCE_MAX 는 디바운싱이 허용되는 최대 시간이고 기본 10초다. PILOT_ENABLE_EDS_DEBOUNCE 는
#       엔드포인트 갱신도 디바운스 규칙을 따를지이며 기본 true 다. PILOT_PUSH_THROTTLE 은 istiod 가 동시에
#       처리하는 푸시 요청 수이고 기본 100 이다.
# 디바운스 실험의 기준선은 700 이 아니라 135 다 — 메시 전역 Sidecar 가 아직 깔린 상태이고 저자는 그것을
#       장 맨 끝에서야 걷어낸다. 700 은 사이드카 이전 값이라 그것과 비교하면 두 손잡이의 이득이 겹쳐 세어진다.
# 앞의 셋은 언제 큐에 넣을지를, 마지막 하나는 큐에서 얼마나 꺼낼지를 정한다 — 축이 둘로 갈린다.
# 타입 스펙: type-tree — 뿌리 하나에서 두 축으로 갈라지고 그 아래 변수가 잎이 된다.
#           깊이 3, 최대 폭 2, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1000, 600
d = D(W, H, "ISTIO IN ACTION · 11-01 §7",
      "언제 넣을지와 얼마나 꺼낼지가 갈린다",
      "환경변수 넷은 두 축으로 갈린다. 앞의 셋은 이벤트를 언제 푸시 큐에 넣을지를 정하고, 마지막 하나는 "
      "큐에서 동시에 몇 개를 꺼낼지를 정한다. 색이 붙은 쪽이 저자가 실험으로 푸시를 다섯 배 줄여 보인 축이다.",
      "저자의 지침은 갱신을 빨리 퍼뜨리려면 둘을 같은 방향으로 함께 움직이라는 것입니다")

NW, NH = 380, 52
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 22, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 11, MUTED, KR)

ROOT_X, ROOT_Y, ROOT_W = 310, 112, 380
d.box(ROOT_X, ROOT_Y, ROOT_W, 56, PAPER2, RULE, 1.0, 6)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 24, "istiod 가 자신을 지키는 두 방법", 13, INK, KR, "middle", 600)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 44, "debounce · throttle", 9, MUTED, MONO)

BUS_Y = 212
XS = [48, 572]
MID_Y, LEAF_Y = 252, 368
d.line(ROOT_X + ROOT_W / 2, ROOT_Y + 56, ROOT_X + ROOT_W / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[1] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 0 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.4 if i == 0 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.4 if i == 0 else 1.0)

node(XS[0], MID_Y, "언제 큐에 넣을까", "묶어서 일을 줄인다", focal=True)
node(XS[1], MID_Y, "큐에서 얼마나 꺼낼까", "동시 처리 수를 정한다")

def leaf(x, y, lines, focal=False):
    h = 24 + len(lines) * 22
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{h}" rx="6" fill="{ACC}0C" stroke="{ACC}88" stroke-width="1"/>')
    else:
        d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 30 + j * 22, ln, 11, MUTED, MONO, "start")

leaf(XS[0], LEAF_Y, ["PILOT_DEBOUNCE_AFTER      100ms",
                     "PILOT_DEBOUNCE_MAX        10s",
                     "PILOT_ENABLE_EDS_DEBOUNCE true"], focal=True)
leaf(XS[1], LEAF_Y, ["PILOT_PUSH_THROTTLE       100",
                     "",
                     "CPU 가 남으면 올린다"])

d.t(32, 484, "저자의 실험 — 사이드카가 깔린 135 에서 디바운스를 2.5초로 올려 27 로 떨어뜨렸고 프로덕션에서는 하지 말라고 못 박는다", 11, SOFT, KR, "start")
d.t(32, 508, "지연 지표는 큐 진입 이후만 세므로 디바운스로 늘어난 시간은 지표에 나타나지 않는다", 11, MUTED, KR, "start")
d.legend(536, [("일을 줄이는 축", ACC), ("진행을 빠르게 하는 축", MUTED)])
d.save("11-01.batching-knobs.svg")
