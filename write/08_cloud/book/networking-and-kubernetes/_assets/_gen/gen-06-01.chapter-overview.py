import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 544
d = D(W, H, "06-01 · AWS AND EKS",
      "VPC 부품에서 시작해 Pod IP 가 VPC 주소가 되는 데까지",
      "부품을 알고 관문을 알면, EKS 가 그 위에 무엇을 얹었는지가 보인다. 끝은 Pod IP 가 VPC 주소가 되는 자리다.",
      lead="부품 → 경계와 관문 → EKS 가 얹은 것 → Pod IP 가 VPC 주소가 되는 자리")
ddx.band(d, 104, 496, "Pod IP 가 VPC 주소라는 한 줄이 이 편의 결론이다")
ddx.stage_chain(d, 316,
  ["§1 부품", "§2·§3 경계와 관문", "§4·§5 EKS", "§6·§7 직결"],
  [("부품", "VPC·서브넷·ENI", "Pod IP 도 여기서", None),
   ("경계·관문", "SG·NACL·NAT·ELB", "사고의 단골 지점", WARN),
   ("EKS", "두 VPC · 세 모드", "노드당 Pod 상한", None),
   ("직결", "VPC CNI · ALB", "Pod IP 로 바로", ACC)],
  ["그 위에", "얹으면", "그래서"])
d.t(36, 468, "Pod 가 VPC 주소를 그대로 쓰기 때문에 SG 도 ALB 도 Pod 를 직접 가리킬 수 있다",
     12, MUTED, KR, "start")
d.legend(512, [("사고의 단골 지점", WARN), ("이 편의 결론", ACC)])
d.save("06-01.chapter-overview.svg"); print("ok 06-01.chapter-overview")
