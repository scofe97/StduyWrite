# 타입 스펙: type-process.md — 단계 머리 + 한 줄 체인. 칸마다 같은 의미 슬롯(절 번호 · 이름 ·
#           한 줄 요약 · 꼬리표)이 같은 자리에 반복된다(semantic-patterns 의 "Stage framework
#           with semantic slots"). 화살표는 데이터가 아니라 읽는 순서를 나른다.
#           2026-08-28 type-data-flow 에서 옮겼다 — data-flow 정본은 "who does what at each
#           stage" 와 role-scoped lane 을 전제로 하는데, 편 지도에는 주체도 레인도 없다.
#           엄밀히는 두 정본 다 주체 기반이라 편 지도는 표의 공백에 가깝고, 주체 없이도 맞는
#           유일한 라우팅 규칙이 위 semantic-patterns 한 줄이라 그쪽을 따랐다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
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
  ["그 위에", "반대편", "접으면"], sizes=(14, 11, 11))
d.t(36, 468, "서브넷이 무엇을 경계로 삼느냐가 셋 다 달라, 한 클라우드의 설계를 그대로 옮기면 어긋난다",
     12, MUTED, KR, "start")
d.legend(512, [("반대 방향 기본값", WARN), ("이 편의 결론", ACC)])
d.save("06-02.chapter-overview.svg"); print("ok 06-02.chapter-overview")
