# 01-01 §5 데이터 플레인과 컨트롤 플레인.
# 본문: 데이터 플레인은 서비스 프록시들이 이루며 메시를 통과하는 트래픽을 수립·보안·제어한다.
#       컨트롤 플레인은 메시의 두뇌로 데이터 플레인의 동작을 설정하고 운영자에게 API 를 노출한다.
#       둘이 함께 제공하는 것은 레질리언스·관측성 신호·트래픽 제어·보안·정책 강제 다섯이다.
# 타입 스펙: type-architecture — 구성요소(운영자 · 컨트롤 플레인 · 프록시 셋)와 연결. 존 2, 초점 1(설정이 내려가는 경로).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1000, 620
d = D(W, H, "ISTIO IN ACTION · 01-01 §5",
      "설정은 위에서 내려오고 트래픽은 아래에서 흐른다",
      "프록시가 늘어나면 그 집단을 설정하고 관리하는 일이 새 문제가 된다. 여기서 두 평면이 갈린다. "
      "색이 붙은 경로가 컨트롤 플레인이 하는 일이고, 아래 가로 흐름이 데이터 플레인이 하는 일이다.",
      "트래픽이 전부 메시를 지나므로 운영자가 명시적으로 통제할 수 있게 됩니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, name, sub):
    d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 28, name, 13, INK, KR, "middle", 600)
    d.t(x + w / 2, y + 48, sub, 11, MUTED, MONO)

zone(52, 132, 892, 104, "CONTROL PLANE")
zone(52, 300, 892, 116, "DATA PLANE")

node(332, 156, 332, 64, "컨트롤 플레인", "동작을 설정하고 API 를 노출")
node(92, 324, 240, 72, "app + proxy", "webapp")
node(380, 324, 240, 72, "app + proxy", "catalog")
node(668, 324, 240, 72, "app + proxy", "orders")

# 설정이 내려가는 경로 — 컨트롤 플레인 한 곳에서 갈라져 워크로드 셋으로 내려간다.
# 좌표는 상자에서 산출한다. 워크로드는 x=92·380·668 에 폭 240 이므로 중앙은 212·500·788,
# 컨트롤 플레인은 x=332 에 폭 332 이므로 중앙은 498 이고 가운데 내림선(500)과 사실상 겹친다.
APP_CX = (212, 500, 788)
BUS_Y = 268
d.path(f"M 500 220 L 500 {BUS_Y}", ACC, 1.4)
d.path(f"M {APP_CX[0]} {BUS_Y} L {APP_CX[-1]} {BUS_Y}", ACC, 1.4)
for cx in APP_CX:
    d.path(f"M {cx} {BUS_Y} L {cx} 322", ACC, 1.4, m="acc")
d.t(516, 258, "설정을 내려보낸다", 11, ACC, KR, "start", 600)

# 트래픽이 흐르는 방향
d.arrow([(332, 360), (380, 360)], MUTED, "ar", 1.4)
d.arrow([(620, 360), (664, 360)], MUTED, "ar", 1.4)
d.t(356, 344, "요청", 11, MUTED, KR, "middle")
d.t(644, 344, "요청", 11, MUTED, KR, "middle")

# 운영자
d.box(52, 156, 240, 64, PAPER2, RULE, 1.0, 6)
d.t(172, 184, "운영자", 13, INK, KR, "middle", 600)
d.t(172, 204, "의도를 적는다", 11, MUTED, MONO)
d.arrow([(292, 188), (332, 188)], INFO, "info", 1.3)

BY = 452
d.box(52, BY, 892, 60, PAPER2, RULE, 1.0, 6)
d.t(72, BY + 26, "둘이 함께 제공하는 것", 11, ACC, KR, "start", 600)
d.t(72, BY + 46, "서비스 레질리언스  ·  관측성 신호  ·  트래픽 제어  ·  보안  ·  정책 강제", 11, INK, MONO, "start")

d.t(28, 552, "통신 양 끝을 모두 통제하므로 상호 인증을 동반한 전송 계층 암호화를 강제할 수 있다", 11, SOFT, KR, "start")
d.legend(576, [("컨트롤 플레인이 하는 일", ACC), ("운영자가 넣는 의도", INFO)])
d.save("01-01.two-planes.svg")
