# 10-01 §5 클러스터 이름 한 줄이 질의 조건 넷이다 — 원문 그림 10.9.
# 본문(원문 10.3.2): "We can only print clusters using the following istioctl proxy-config clusters flags:
#       direction, fqdn, port, and subset. The information for all the flags is contained within the
#       cluster name we retrieved earlier." 파이프로 나뉜 네 조각이 그대로 네 플래그다.
# 잎의 값은 저자가 출력에서 얻은 클러스터 이름 그대로다.
# 타입 스펙: type-tree — 뿌리 하나(클러스터 이름)에서 네 조각으로 갈라지고 그 아래 플래그가 잎이 된다.
#           깊이 3, 최대 폭 4, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1240, 616
d = D(W, H, "ISTIO IN ACTION · 10-01 §5",
      "이름 한 줄을 파이프로 끊으면 질의 조건이 된다",
      "클러스터 이름은 방향 · 포트 · subset · FQDN 네 조각을 파이프로 이은 것이고, 그 넷이 그대로 "
      "istioctl 의 질의 플래그다. 색이 붙은 조각이 없어서 이 장의 요청이 전부 실패한다.",
      "이름을 읽을 줄 알면 어느 플래그로 좁혀야 하는지가 함께 정해집니다")

NW, NH = 264, 52
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 22, name, 12, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 40, sub, 9, MUTED, MONO)

ROOT_X, ROOT_Y, ROOT_W = 120, 112, 1000
d.box(ROOT_X, ROOT_Y, ROOT_W, 60, PAPER2, RULE, 1.0, 6)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 26, "인그레스 게이트웨이가 라우트에서 지목한 클러스터 이름", 12, INK, KR, "middle", 600)
d.t(ROOT_X + ROOT_W / 2, ROOT_Y + 46, "outbound|80|version-v1|catalog.istioinaction.svc.cluster.local", 11, MUTED, MONO)

BUS_Y = 216
XS = [32, 336, 640, 944]
MID_Y, LEAF_Y = 256, 372
d.line(ROOT_X + ROOT_W / 2, ROOT_Y + 60, ROOT_X + ROOT_W / 2, BUS_Y, MUTED, 1.0)
d.line(XS[0] + NW / 2, BUS_Y, XS[3] + NW / 2, BUS_Y, MUTED, 1.0)
for i, x in enumerate(XS):
    c = ACC if i == 2 else MUTED
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, c, 1.2 if i == 2 else 1.0)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, c, 1.2 if i == 2 else 1.0)

node(XS[0], MID_Y, "방향", "outbound")
node(XS[1], MID_Y, "포트", "80")
node(XS[2], MID_Y, "subset", "version-v1", focal=True)
node(XS[3], MID_Y, "FQDN", "catalog.istioinaction.svc…")

def leaf(x, y, lines, focal=False):
    h = 24 + len(lines) * 20
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{NW}" height="{h}" rx="6" fill="{ACC}0C" stroke="{ACC}88" stroke-width="1"/>')
    else:
        d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 28 + j * 20, ln, 10, MUTED, MONO, "start")

leaf(XS[0], LEAF_Y, ["--direction outbound", "나가는 쪽인지 들어오는 쪽인지"])
leaf(XS[1], LEAF_Y, ["--port 80", "서비스가 노출한 포트"])
leaf(XS[2], LEAF_Y, ["--subset version-v1", "DestinationRule 이 만든다"], focal=True)
leaf(XS[3], LEAF_Y, ["--fqdn catalog.istioinaction…", "쿠버네티스 서비스 이름"])

d.t(32, 490, "네 플래그로 좁힌 질의가 빈 표를 돌려주면 그 클러스터는 존재하지 않는다는 뜻이다", 11, SOFT, KR, "start")
d.t(32, 514, "고치는 리소스는 적용 전에 istioctl analyze 로 파일째 검증할 수 있다", 11, MUTED, KR, "start")
d.legend(544, [("예제에 없던 조각", ACC), ("이름에서 그대로 읽히는 조각", MUTED)])
d.save("10-01.cluster-name.svg")
