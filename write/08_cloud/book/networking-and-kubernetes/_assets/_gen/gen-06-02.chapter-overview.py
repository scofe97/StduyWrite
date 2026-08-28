# 타입 스펙: type-data-flow.md — 단계 머리를 세우고 그 아래 한 칸씩 — 편 전체를 한 줄로 잇는 지도
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "06-02 · SAME PROBLEM, DIFFERENT DEFAULTS",
      "같은 문제를 세 클라우드가 다른 기본값으로 푼다",
      "글로벌인가 리전인가, 기본이 열려 있는가 닫혀 있는가. 그 기본값 차이가 설계 이식을 어긋나게 한다.",
      lead="기본값이 다르다는 사실이 설계 이식을 어긋나게 한다")
ddx.band(d, 104, 496, "IP 설계가 곧 용량 설계다 — 그 경계가 셋 다 다르다")
ddx.stage_chain(d, 316,
  ["§1 GCP 망", "§2 GKE", "§3·§4 Azure", "§5 3사 비교"],
  [("글로벌 기본", "VPC 가 글로벌 자원", "방화벽·라우트도", None),
   ("GKE", "VPC-native · NEG", "LB 가 Pod 직결", None),
   ("열린 기본", "지울 수 없는 라우트", "AKS 는 kubenet 기본", WARN),
   ("한 표로", "서브넷 경계가 다름", "IP 설계 = 용량 설계", ACC)],
  ["그 위에", "반대편", "접으면"])
d.t(36, 468, "서브넷이 무엇을 경계로 삼느냐가 셋 다 달라, 한 클라우드의 설계를 그대로 옮기면 어긋난다",
     12, MUTED, KR, "start")
d.legend(512, [("반대 방향 기본값", WARN), ("이 편의 결론", ACC)])
d.save("06-02.chapter-overview.svg"); print("ok 06-02.chapter-overview")
