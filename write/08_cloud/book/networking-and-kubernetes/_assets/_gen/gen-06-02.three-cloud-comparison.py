# 타입 스펙: type-dp-security-matrix.md — 행이 항목, 열이 3사 — 용어 대응표가 곧 이 장의 요약이다
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 604
d = D(W, H, "THREE CLOUDS · WHERE THE SUBNET ENDS",
      "서브넷 경계가 셋 다 달라 설계 이식이 어긋난다",
      "VPC 가 리전 자원인지 글로벌 자원인지, 서브넷이 AZ 하나인지 여럿인지가 셋 다 다르다.",
      lead="VPC 의 범위도, 서브넷의 경계도 셋 다 다르다")
ddx.band(d, 104, 548, "옮길 때 어긋나는 것은 이름이 아니라 이 경계다")
ddx.matrix(d, 44,
  [(280, "VPC 의 범위"), (320, "서브넷의 경계"), (292, "기본 통신")],
  [([("AWS", "VPC — 리전 자원"), ("서브넷 = 단일 AZ", "라우팅 범위 = 서브넷"),
     ("기본 닫힘", "EKS · ALB")], INFO),
   ([("Azure", "Vnet — 리전 자원"), ("서브넷이 AZ 를 가로지름", "라우팅 범위 = 서브넷"),
     ("기본 열림", "AKS · Azure CNI")], WARN),
   ([("GCP", "VPC — 글로벌 자원"), ("서브넷 = 리전", "라우팅 범위 = VPC"),
     ("기본 닫힘", "GKE · NEG")], OK)],
  hdr_y=200, row_h=88, gap=12, focal_col=1)
d.t(36, 524, "서브넷이 AZ 하나인지 여럿인지가 가용성 설계를 바꾼다 — 같은 그림을 옮기면 그 지점이 어긋난다",
     12, MUTED, KR, "start")
d.legend(564, [("AWS", INFO), ("Azure", WARN), ("GCP", OK)])
d.save("06-02.three-cloud-comparison.svg"); print("ok three-cloud-comparison")
