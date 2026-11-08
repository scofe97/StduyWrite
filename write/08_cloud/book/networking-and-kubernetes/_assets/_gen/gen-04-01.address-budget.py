# 04-01.address-budget — 두 컴포넌트가 정하는 주소 예산의 포함 관계
# 본문 요구: "--cluster-cidr 는 Pod IP 를 할당할 대역 / --node-cidr-mask-size 는 노드별 마스크(기본 IPv4 /24)이고
#           노드마다 2^(32-마스크)개 — 둘 다 kube-controller-manager / --service-cluster-ip-range 는 kube-apiserver 가
#           ClusterIP 를 주는 대역이고 ServiceCIDR 오브젝트로 늘릴 수 있다" — 앞 둘은 포함 관계, 셋째는 다른 컴포넌트의 별개 축.
# 타입 스펙: type-nested. 공식 없는 타입이라 stride 로 배치.
#           2026-11-08 소유자를 갈랐다 — Service 대역은 kube-controller-manager 가 아니라 kube-apiserver 몫이다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 472
d = D(W, H, "ADDRESS BUDGET · WHO OWNS WHICH RANGE",
      "Pod 대역은 컨트롤러 매니저가, Service 대역은 API 서버가 정한다",
      "cluster-cidr 안을 노드별 CIDR 로 쪼개는 일은 kube-controller-manager 가 하고, ClusterIP 대역은 kube-apiserver 가 따로 정한다.",
      lead="Pod 대역은 노드별 /24 조각으로 나뉘고 Service 대역은 소유자와 축이 다르다")

OX, OY, OW, OH = 32, 112, 616, 248
d.box(OX, OY, OW, OH, PAPER2, INFO, 1.1, 8)
d.t(OX + 20, OY + 28, "kube-controller-manager · --cluster-cidr", 12, INFO, MONO, "start", 600)
d.t(OX + 20, OY + 48, "Pod IP 할당 대역 · --allocate-node-cidrs=true 전제", 12, MUTED, KR, "start")

NW, NY, NH = 168, OY + 72, 92
for i, nm in enumerate(["노드 1", "노드 2", "노드 N"]):
    x = 56 + i * (NW + 32)
    d.box(x, NY, NW, NH, PAPER, RULE, 0.9, 6)
    d.t(x + NW // 2, NY + 38, nm, 12, MUTED, KR, "middle", 600)
    d.t(x + NW // 2, NY + 62, "/24 한 조각", 12, SOFT, KR)

FY = NY + NH + 16
d.tone(56, FY, 568, 56, ACC, 6, "12", 1.4)
d.t(56 + 284, FY + 34, "--node-cidr-mask-size 기본 /24 → 노드마다 2^(32-24) = 256 개",
    12, ACC, KR)

d.box(696, OY, 272, OH, PAPER2, WARN, 1.1, 8)
d.t(696 + 136, OY + 28, "kube-apiserver", 12, WARN, MONO, "middle", 600)
d.t(696 + 136, OY + 52, "--service-cluster-ip-range", 12, WARN, MONO, "middle", 600)
for i, ln in ((0, "ClusterIP 할당 대역"), (1, "ServiceCIDR 오브젝트 kubernetes"), (2, "오브젝트로 대역 추가·삭제"), (3, "Pod 대역과 겹치지 않는 별개 축")):
    d.t(696 + 136, OY + 100 + i * 28, ddx.fit(ln, 12, 240, ln), 12, MUTED, KR if i != 1 else KR)

d.legend(408, [("Pod 주소 예산", INFO), ("Service 주소 예산", WARN), ("노드 한 조각의 크기", ACC)])
d.save("04-01.address-budget.svg")
print("ok address-budget")
