# 06-01.vpc-parts — VPC 부품의 포함 관계
# 본문 요구: "VPC 는 리전당 정의 · 한 리전에 여럿 두되 VPC 하나는 한 리전에만 · 겹치지 않는
#           CIDR 여럿 · 리전은 여러 AZ 로 구성 · 라우팅 테이블은 서브넷마다 정확히 하나".
# 타입 스펙: type-nested. 공식 없는 타입이라 stride 로 배치.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 512
d = D(W, H, "AWS VPC · WHAT CONTAINS WHAT",
      "리전 안에 VPC, VPC 안에 AZ 별 서브넷",
      "VPC 는 한 리전에만 존재하고 서브넷마다 라우팅 테이블이 정확히 하나 붙는다.",
      lead="Pod IP 도 결국 이 VPC CIDR 에서 나온다는 것이 이 편의 복선")

OX, OY, OW, OH = 32, 152, 936, 232
d.box(OX, OY, OW, OH, PAPER2, INFO, 1.1, 8)
d.t(OX + 20, OY + 28, "VPC", 13, INFO, MONO, "start", 600)
d.t(OX + 20, OY + 48, "계정 전용 · 리전당 정의 · 겹치지 않는 CIDR 을 여럿 붙일 수 있다", 11, MUTED, KR, "start")

SW, SY, SH = 288, OY + 72, 132
for i, az in enumerate(["AZ a", "AZ b", "AZ c"]):
    x = 56 + i * (SW + 12)
    d.box(x, SY, SW, SH, PAPER, RULE, 0.9, 6)
    d.t(x + SW // 2, SY + 28, az, 12, SOFT, KR, "middle", 600)
    d.t(x + SW // 2, SY + 56, "서브넷", 12, INK, KR)
    if i == 1:
        d.tone(x + 24, SY + 74, SW - 48, 40, ACC, 6, "12", 1.4)
        d.t(x + SW // 2, SY + 100, "라우팅 테이블 정확히 하나", 11, ACC, KR)
    else:
        d.box(x + 24, SY + 74, SW - 48, 40, PAPER2, RULE, 0.9, 6)
        d.t(x + SW // 2, SY + 100, "라우팅 테이블 정확히 하나", 11, MUTED, KR)

d.t(36, OY + OH + 44, "명시하지 않으면 main 테이블이 붙고 그 테이블은 삭제할 수 없다 · 경로 중에서는 local 이 가장 구체적이다",
    12, MUTED, KR, "start")
d.t(36, OY + OH + 70, "ENI 는 속성을 유지한 채 인스턴스를 옮겨 다니는 가상 NIC 이고, EIP 는 인스턴스보다 그 ENI 에 붙이는 쪽이 낫다",
    12, MUTED, KR, "start")
d.legend(OY + OH + 84, [("포함 관계", INFO), ("서브넷마다 하나", ACC)])
d.save("06-01.vpc-parts.svg")
print("ok vpc-parts")
