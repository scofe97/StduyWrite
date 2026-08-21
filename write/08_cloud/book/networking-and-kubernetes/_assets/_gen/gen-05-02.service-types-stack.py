# 05-02.service-types-stack — 위 유형이 아래 유형을 품는다
# 본문 요구: 호출자가 층마다 다르고, Headless 는 ClusterIP 에서 LB 를 뺀 변형
# 타입 스펙: type-nested.md — 포함 관계가 요점이라 겹으로 그린다. 호출자는 링 밖에서
#           자기 층으로 들어온다. coral 은 가장 안쪽 한 겹에만.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 668
d = D(W, H, "SERVICE TYPES · EACH CONTAINS THE NEXT",
      "위 유형이 아래 유형을 품는다 — 호출자는 층마다 다르다",
      "LoadBalancer 는 NodePort 를 품고, NodePort 는 ClusterIP 를 품는다. 호출자가 어디서 오느냐가 어느 층으로 들어올지를 정한다.",
      lead="LoadBalancer 는 NodePort 를, NodePort 는 ClusterIP 를 품는다")

CW, CH = 168, 88
CALL = [(126, 262, "외부 클라이언트", "인터넷에서"),
        (126, 386, "외부 LB", "노드 IP 를 앎"),
        (126, 510, "안쪽 워크로드", "다른 Pod 에서")]
LB   = (248, 208, 462, 344)
NP   = (288, 268, 382, 224)
CIP  = (328, 328, 302, 104)
HL   = (760, 380, 200, 104)

def box(cx, cy, w, h, t, s, tag, c=None, focal=False, dash=False):
    x, y = cx - w // 2, cy - h // 2
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" '
                   f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{PAPER2}" '
                   f'stroke="{c or RULE}" stroke-width="1.1"{" stroke-dasharray=\"6 5\"" if dash else ""}/>')
        tc = c or INK
    d.t(cx, cy - 14, ddx.fit(t, 13, w - 18, t), 13, tc, KR, "middle", 600)
    d.t(cx, cy + 8, ddx.fit(s, 11, w - 16, s), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in ':~' for ch in s) else KR)
    if tag: d.t(cx, cy + 30, ddx.fit(tag, 10, w - 14, tag), 10, SOFT, KR)

ddx.band(d, 104, 608, "안쪽에서 부르면 ClusterIP 로 끝나고, 밖에서 오면 겹을 하나씩 더 지난다")
for (rx, ry, rw, rh), lab, sub, c in [
        (LB, "LoadBalancer", "클라우드 LB · MetalLB · L4 외부 통합", INFO),
        (NP, "NodePort", "30000~32767 · 모든 노드에 고정 포트", WARN)]:
    d.o.append(f'<rect x="{rx}" y="{ry}" width="{rw}" height="{rh}" rx="8" '
               f'fill="{c}06" stroke="{c}" stroke-width="1.2" stroke-dasharray="7 6"/>')
    ddx.ring_label(d, rx, ry, f"{lab} — {sub}", 11, c, off=16)

box(CIP[0] + CIP[2] // 2, CIP[1] + CIP[3] // 2, CIP[2], CIP[3],
    "ClusterIP", "가상 IP", "kube-proxy 가 DNAT", focal=True)
box(HL[0] + HL[2] // 2, HL[1] + HL[3] // 2, HL[2], HL[3],
    "Headless", "clusterIP: None", "DNS 가 명단을 반환", OK, dash=True)
d.path(f"M {CIP[0]+CIP[2]+6} {CIP[1]+CIP[3]//2} L {HL[0]-10} {HL[1]+HL[3]//2}", OK, 1.4, m="ok", dash="6 5")
d.t(HL[0] + HL[2] // 2, HL[1] - 14, "LB 를 뺀 변형", 10, OK, KR)

for cx, cy, t, s in CALL: box(cx, cy, CW, CH, t, s, "", INFO)
for (cx, cy, *_), tx in zip(CALL, [LB[0], NP[0], CIP[0]]):
    d.path(f"M {cx+CW//2+6} {cy} L {tx-10} {cy}", MUTED, 1.5, m="ar")

d.t(36, 580, "Headless 는 아래 유형이 아니라 옆으로 난 변형이다 — 가상 IP 를 두지 않고 "
             "DNS 가 Pod 명단을 그대로 돌려준다", 12, MUTED, KR, "start")
d.legend(624, [("호출자 · 바깥 층", INFO), ("노드 포트 층", WARN), ("가장 안쪽", ACC), ("변형", OK)])
d.save("05-02.service-types-stack.svg")
print("ok service-types-stack")
