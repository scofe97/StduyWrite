# 04-01.address-budget — 플래그 셋이 정하는 주소 예산의 포함 관계
# 본문 요구: "--cluster-CIDR 는 Pod IP 를 할당할 대역 / --node-CIDR-mask-size 는 노드별
#           마스크(기본 IPv4 /24)이고 노드마다 2^(32-마스크)개 / --service-cluster-ip-range
#           는 서비스 ClusterIP 대역" — 앞 둘은 포함 관계, 셋째는 별개 축.
# 타입 스펙: type-nested. 공식 없는 타입이라 stride 로 배치.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 520
d = D(W, H, "kube-controller-manager · ADDRESS BUDGET",
      "플래그 셋이 클러스터의 주소 예산을 정한다",
      "cluster-CIDR 안을 노드별 CIDR 로 쪼개고, 서비스 대역은 그와 별개로 잡는다.",
      lead="앞의 둘은 포함 관계이고 서비스 대역만 축이 다르다")

OX, OY, OW, OH = 32, 160, 616, 248
d.box(OX, OY, OW, OH, PAPER2, INFO, 1.1, 8)
d.t(OX + 20, OY + 28, "--cluster-CIDR", 12, INFO, MONO, "start", 600)
d.t(OX + 20, OY + 48, "Pod IP 를 할당할 대역 · --allocate-node-cidrs=true 가 전제", 11, MUTED, KR, "start")

NW, NY, NH = 168, OY + 72, 92
for i, nm in enumerate(["노드 1", "노드 2", "노드 N"]):
    x = 56 + i * (NW + 32)
    d.box(x, NY, NW, NH, PAPER, RULE, 0.9, 6)
    d.t(x + NW // 2, NY + 38, nm, 12, MUTED, KR, "middle", 600)
    d.t(x + NW // 2, NY + 62, "/24 한 조각", 11, SOFT, KR)

FY = NY + NH + 16
d.tone(56, FY, 568, 56, ACC, 6, "12", 1.4)
d.t(56 + 284, FY + 34, "--node-CIDR-mask-size 기본 /24 → 노드마다 2^(32-24) = 256 개",
    12, ACC, KR)

d.box(696, OY, 272, OH, PAPER2, WARN, 1.1, 8)
d.t(696 + 136, OY + 48, "--service-cluster-ip-range", 12, WARN, MONO, "middle", 600)
for i, ln in ((0, "서비스 ClusterIP 를"), (1, "할당할 대역"), (2, "Pod 대역과 겹치지 않는"), (3, "별개 축이다")):
    d.t(696 + 136, OY + 96 + i * 26, ddx.fit(ln, 12, 240, ln), 12, MUTED, KR)

d.t(36, 444, "dual-stack 이면 cluster-CIDR 에 IPv4·IPv6 쌍을 콤마로 주고, IPv6 마스크 기본값은 /64 다",
    12, MUTED, KR, "start")
d.legend(456, [("Pod 주소 예산", INFO), ("서비스 주소 예산", WARN), ("노드 한 조각의 크기", ACC)])
d.save("04-01.address-budget.svg")
print("ok address-budget")
