# 06-01.eks-two-vpc — 컨트롤 플레인과 워커는 다른 VPC 에 산다
# 타입 스펙: type-nested.md 경계 링 둘 + 사이를 잇는 다리 하나. 다리가 요점이라 focal.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 596
d = D(W, H, "EKS · TWO VPCs, ONE BRIDGE",
      "컨트롤 플레인과 워커는 다른 VPC 에 산다",
      "API 서버는 AWS 소유 VPC 에 있고 워커는 고객 VPC 에 있다. 둘을 잇는 것은 cross-account ENI 몇 개뿐이다.",
      lead="둘을 잇는 것은 cross-account ENI 몇 개뿐이다")

EKS = (40, 216, 300, 262)
CUS = (620, 216, 340, 262)
API, ENI = (190, 347), (480, 347)
NODE, POD = (790, 278), (790, 414)                                # 세로 간격 24px 확보

def box(cx, cy, w, h, t, s, tag, c=None, focal=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6); tc = c or INK
    d.t(cx, cy - 16, ddx.fit(t, 13, w - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 4, ddx.fit(s, 11, w - 16, s), 11, MUTED, KR)
    d.t(cx, cy + 26, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 548, "다리가 몇 개뿐이라 그 수가 곧 관리 경로의 여유다")
for (rx, ry, rw, rh), lab, c in [(EKS, "EKS 소유 VPC — AWS 가 운영", INFO),
                                 (CUS, "고객 VPC — 내가 운영", WARN)]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, lab, 11, c, off=16)

box(*API, 240, 104, "API 서버", "etcd 와 함께", "AWS 가 운영", INFO)
box(*ENI, 220, 104, "cross-account ENI", "최대 4 개", "두 VPC 를 잇는 다리", focal=True)
box(*NODE, 280, 96, "워커 노드", "Kubelet 이 등록", "EC2 인스턴스", WARN)
box(*POD, 280, 96, "Pod", "IP = ENI 보조 IP", "Pod 수 공식의 근거", WARN)

d.path(f"M {API[0]+120+6} {API[1]} L {ENI[0]-110-10} {ENI[1]}", ACC, 1.6, m="acc")
d.t((API[0] + 120 + ENI[0] - 110) // 2, API[1] - 16, "관리 방향", 10, ACC, KR)
d.path(f"M {ENI[0]+110+6} {ENI[1]} L {NODE[0]-140-10} {NODE[1]+24}", ACC, 1.6, m="acc")
d.t(CUS[0] - 6, ENI[1] - 16, "등록 방향", 10, ACC, KR, "end")
d.path(f"M {NODE[0]} {NODE[1]+48+6} L {POD[0]} {POD[1]-48-10}", MUTED, 1.4, m="ar")

d.t(36, 508, "Pod IP 가 ENI 보조 IP 라서 고객 VPC 주소를 그대로 쓴다 — 노드당 Pod 상한이 "
             "여기서 나온다", 12, MUTED, KR, "start")
d.legend(564, [("AWS 쪽", INFO), ("내 쪽", WARN), ("두 VPC 를 잇는 다리", ACC)])
d.save("06-01.eks-two-vpc.svg"); print("ok eks-two-vpc")
