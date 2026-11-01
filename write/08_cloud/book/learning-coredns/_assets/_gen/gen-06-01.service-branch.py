# 06-01 §4 — clusterIP 필드 하나가 부하 분산의 자리를 옮긴다.
# 본문 근거: 이 노트 §4 「clusterIP 한 필드가 부하 분산의 자리를 옮긴다」 및 「헤드리스는 그 가상 IP 를 포기합니다」.
# 원서 쪽: p.4 "Cluster IP Services solve exactly the problem we described earlier: they create a stable,
#          cluster-wide virtual IP address... kube-proxy manipulates the netfilter tables of the node
#          using standard Linux iptables, so that traffic bound for the VIP is randomly redirected" /
#          p.5 "The headless service looks exactly like a cluster IP service, except that the clusterIP
#          field is set to None... In this case, there is no VIP, and kube-proxy ignores the service.
#          Instead, any load balancing is done in the client itself, using DNS".
#          Example 6-1(p.5, hello-world, clusterIP: 10.0.0.100) · Example 6-2(p.5, headless, clusterIP: None).
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


oval(440, 104, 300, 48, "Service 선언", MUTED)

DW, DH = 300, 84
DY = 188
d.path(f"M 440 152 L 440 {DY - 2}", MUTED, 1.4, m="ar")
d.o.append(f'<path d="M 440 {DY} L {440 + DW / 2} {DY + DH / 2} L 440 {DY + DH} L {440 - DW / 2} {DY + DH / 2} Z" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(440, DY + 38, "clusterIP 필드값", 14, ACC, KR, "middle", 600)
d.t(440, DY + 58, "None 설정 여부", 14, ACC, KR, "middle", 600)

d.path(f"M {440 - DW / 2} {DY + DH / 2} L {LX} {DY + DH / 2} L {LX} 316", MUTED, 1.4, m="ar")
d.t(LX + 12, DY + 30, "아니요", 13, MUTED, KR, "start")
d.path(f"M {440 + DW / 2} {DY + DH / 2} L {RX} {DY + DH / 2} L {RX} 316", MUTED, 1.4, m="ar")
d.t(RX - 12, DY + 30, "예", 13, MUTED, KR, "end")

rows = [
    (318, "가상 IP(VIP) 할당", "클러스터 전역 안정 주소", "가상 IP(VIP) 미할당", "엔드포인트 주소 목록 반환"),
    (410, "kube-proxy 규칙 조작", "iptables 기반 netfilter 무작위 분배", "kube-proxy 가 무시", "netfilter 규칙 없음"),
    (502, "단일 A 레코드 반환", "할당된 가상 IP 1개", "다중 A 레코드 반환", "Ready 엔드포인트마다 1개"),
]
for y, lt, ls, rt, rs in rows:
    step(LX, y, lt, ls)
    step(RX, y, rt, rs)
    if y != 502:
        d.path(f"M {LX} {y + BH} L {LX} {y + 90}", MUTED, 1.4, m="ar")
        d.path(f"M {RX} {y + BH} L {RX} {y + 90}", MUTED, 1.4, m="ar")

d.path(f"M {LX} 566 L {LX} 592", MUTED, 1.4, m="ar")
d.path(f"M {RX} 566 L {RX} 592", MUTED, 1.4, m="ar")
oval(LX, 594, 320, 48, "노드(커널) 무작위 분배", INFO)
oval(RX, 594, 320, 48, "클라이언트 측 부하 분산", OK)

d.legend(664, [("분기 판단 필드", ACC), ("노드(커널) 분배", INFO), ("클라이언트 분배", OK)])
d.save("06-01.service-branch.svg")
