# 05-02.service-type-stack — 아래층이 위층의 토대가 된다
# 본문 요구: "트래픽 흐름은 3층 스택 그대로입니다 — LB 공인 IP:80(port) → ClusterIP →
#           컨테이너 8080(targetPort)" + "로드밸런서와 워크로드가 1:1 이라 그 비용이 다음 편
#           Ingress 의 존재 이유".
# 타입 스펙: type-layers.md — 위층이 아래층을 토대로 얹히는 3층 스택 — 순서축이 형태로 존재한다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 560   # 층 3개가 448 에서 끝난다
d = D(W, H, "SERVICE TYPES · A STACK, NOT A LIST",
      "위층은 아래층을 토대로 얹힌다",
      "LoadBalancer 는 NodePort 를, NodePort 는 ClusterIP 를 딛고 선다. 트래픽도 그 순서로 내려온다.",
      lead="다섯 유형이 나란한 선택지가 아니라 세 층이 쌓인 구조라는 것이 이 편의 뼈대")

SX, SW = 32, 460
LAYERS = [("LoadBalancer", "외부 장비를 NodePort 앞에 세운다 · 워크로드와 1:1", ACC),
          ("NodePort", "모든 노드에 같은 포트를 연다", INFO),
          ("ClusterIP", "휘발성 Pod IP 앞의 안정된 가상 주소", INFO)]
LY, LH, LG = 152, 88, 16
for i, (nm, sub, c) in enumerate(LAYERS):
    y = LY + i * (LH + LG)
    if c is ACC:
        d.tone(SX, y, SW, LH, ACC, 6, "12", 1.4)
    else:
        d.box(SX, y, SW, LH, PAPER2, c, 1.1, 6)
    d.t(SX + SW // 2, y + 36, nm, 14, c, MONO, "middle", 600)
    d.t(SX + SW // 2, y + 62, ddx.fit(sub, 12, SW - 24, sub), 12, MUTED, KR)

PX, PW = 552, 416
d.box(PX, LY, PW, 3 * LH + 2 * LG, PAPER2, RULE, 0.9, 8)
d.t(PX + 16, LY + 26, "요청 하나가 내려오는 순서", 12, SOFT, KR, "start")
HOPS = [("LB 공인 IP:80", "port"), ("ClusterIP", "서비스 가상 주소"), ("컨테이너 8080", "targetPort")]
for i, (a, b) in enumerate(HOPS):
    cy = LY + 66 + i * 68
    d.t(PX + PW // 2, cy, a, 13, INK, MONO, "middle", 600)
    d.t(PX + PW // 2, cy + 20, b, 11, MUTED, KR)
    if i < 2:
        d.path(f"M {PX+PW//2} {cy+30} L {PX+PW//2} {cy+50}", MUTED, 1.4, m="ar")

d.t(36, 476, "Headless 와 ExternalName 은 이 스택에 얹히지 않는다 — 하나는 가상 IP 를 포기하고 하나는 DNS 별칭이다",
    12, MUTED, KR, "start")
d.legend(488, [("토대가 되는 층", INFO), ("워크로드와 1:1 이라 비싼 층", ACC)])
d.save("05-02.service-type-stack.svg")
print("ok service-type-stack")
