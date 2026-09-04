# 06-01 §4 — clusterIP 필드 하나가 부하 분산의 자리를 옮긴다.
# 원문 근거: "The headless service looks exactly like a cluster IP service, except that the clusterIP
#            field is set to None ... In this case, there is no VIP, and kube-proxy ignores the service.
#            Instead, any load balancing is done in the client itself, using DNS to find all of the IP
#            addresses" / ClusterIP 쪽은 kube-proxy 가 "manipulates the netfilter tables of the node
#            using the standard Linux iptables, so that traffic bound for the VIP is randomly redirected".
# 타입 스펙: type-flowchart — 조건 하나로 갈리는 판단 논리이고 분기마다 라벨을 단다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, INFO, KR, MONO

W, H = 880, 724
d = D(W, H, "LEARNING COREDNS · 06-01 §4",
      "clusterIP 한 필드가 가르는 두 경로",
      "두 Service 는 생김새가 거의 같고 clusterIP 값만 다르다. 그 한 필드가 가상 IP 의 유무, "
      "kube-proxy 의 관여 여부, 응답하는 A 레코드의 개수를 한꺼번에 바꾼다.",
      "주황 마름모 하나가 아래 여섯 칸을 전부 결정합니다")

LX, RX = 216, 664
BW, BH = 336, 64


def step(cx, y, title, sub, c=INK):
    d.box(cx - BW / 2, y, BW, BH, PAPER2, RULE, 1.0)
    d.t(cx, y + 26, title, 15, c, KR, "middle", 600)
    d.t(cx, y + 48, sub, 12, MUTED, KR)


def oval(cx, y, w, h, txt, c):
    d.o.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="20" fill="{c}12" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, y + h / 2 + 5, txt, 15, c, KR, "middle", 600)


oval(440, 104, 300, 48, "Service 를 선언한다", MUTED)

DW, DH = 300, 84
DY = 188
d.path(f"M 440 152 L 440 {DY - 2}", MUTED, 1.4, m="ar")
d.o.append(f'<path d="M 440 {DY} L {440 + DW / 2} {DY + DH / 2} L 440 {DY + DH} L {440 - DW / 2} {DY + DH / 2} Z" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(440, DY + 38, "clusterIP 를", 14, ACC, KR, "middle", 600)
d.t(440, DY + 58, "None 으로 두었나", 14, ACC, KR, "middle", 600)

d.path(f"M {440 - DW / 2} {DY + DH / 2} L {LX} {DY + DH / 2} L {LX} 316", MUTED, 1.4, m="ar")
d.t(LX + 12, DY + 30, "아니다", 13, MUTED, KR, "start")
d.path(f"M {440 + DW / 2} {DY + DH / 2} L {RX} {DY + DH / 2} L {RX} 316", MUTED, 1.4, m="ar")
d.t(RX - 12, DY + 30, "그렇다", 13, MUTED, KR, "end")

rows = [
    (318, "가상 IP 를 하나 받는다", "클러스터 전역에서 안정적", "가상 IP 가 없다", "이름이 곧 주소 집합"),
    (410, "kube-proxy 가 관여한다", "iptables 로 netfilter 를 고친다", "kube-proxy 가 무시한다", "노드에는 규칙이 안 생긴다"),
    (502, "A 레코드가 하나", "그 가상 IP", "A 레코드가 엔드포인트 수만큼", "같은 이름이 주소 여럿"),
]
for y, lt, ls, rt, rs in rows:
    step(LX, y, lt, ls)
    step(RX, y, rt, rs)
    if y != 502:
        d.path(f"M {LX} {y + BH} L {LX} {y + 90}", MUTED, 1.4, m="ar")
        d.path(f"M {RX} {y + BH} L {RX} {y + 90}", MUTED, 1.4, m="ar")

d.path(f"M {LX} 566 L {LX} 592", MUTED, 1.4, m="ar")
d.path(f"M {RX} 566 L {RX} 592", MUTED, 1.4, m="ar")
oval(LX, 594, 320, 48, "노드에서 무작위로 나눈다", INFO)
oval(RX, 594, 320, 48, "클라이언트가 직접 고른다", OK)

d.legend(664, [("이 값 하나가 갈림길", ACC), ("분배가 노드에서", INFO), ("분배가 클라이언트에서", OK)])
d.save("06-01.service-branch.svg")
