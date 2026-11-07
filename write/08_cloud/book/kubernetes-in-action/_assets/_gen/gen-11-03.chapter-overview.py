# 11-03 전체 지도 — 요청이 살아 있는 목적지에만 닿게 한다
# 이 편의 네 덩어리가 명단 → 이름 → 경로 → 편입 순으로 이어지므로 체인.
# 마지막 칸 readiness probe 가 명단에 들어올 자격을 정하는 관문이라 그곳만 focal 로 둔다.
# 타입 스펙: type-process.md — 단계마다 같은 의미 슬롯이 반복되고 화살표는 읽는 순서를 나른다.
#           (11-01·11-02 chapter-overview 와 같은 근거. 역할 레인이 없는 그림의 라우팅은
#           visual-diagram-selection 의 "알려진 공백" 에 적힌 대로다.)
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, KR
import ddx

d = D(1000, 400, "KUBERNETES IN ACTION · 11-03",
      "요청이 살아 있는 목적지에만 닿게 한다",
      "Service 뒤의 EndpointSlice 가 명단을 들고, DNS 가 그 명단을 이름으로 보여 주며, "
      "토폴로지 설정이 가까운 쪽으로 기울이고, readiness probe 가 준비된 파드만 명단에 들인다.",
      "명단에서 편입까지")

ddx.stage_chain(
    d, cy=232,
    stages=["명단", "이름", "경로", "편입"],
    nodes=[
        ("EndpointSlice", "조각당 기본 100개", "Service 뒤의 명단", None),
        ("DNS 레코드", "A · SRV · CNAME", "headless 는 파드 IP 전부", None),
        ("가까운 엔드포인트", "trafficDistribution", "같은 노드·존을 먼저", None),
        ("readiness probe", "통과해야 편입", "준비된 파드만 명단에", ACC),
    ],
    edges=["이름으로 찾음", "가까이 보냄", "준비된 것만"],
    bw=176, gap=78, x0=31, sizes=(12, 11, 11))

d.legend(330, [("명단 자격을 정하는 관문", ACC)])
d.save("11-03.chapter-overview.svg")
print("ok")
