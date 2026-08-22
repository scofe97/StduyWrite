# 03-01.chapter-overview — 네 단계 지도
# 타입 스펙: type-data-flow.md §2 격자 — 단계 머리 + 한 줄 체인 (ddx.stage_chain)
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "03-01 · CONTAINER BIRTH",
      "컨테이너를 분해했다가 손으로 다시 조립하는 순서",
      "왜 컨테이너가 필요했는지에서 시작해, 그것을 만드는 커널 프리미티브까지 내려간 뒤 손으로 배선한다.",
      lead="왜 필요했나 → 무엇으로 만드나 → 직접 해 보면 무엇이 남나")
ddx.band(d, 104, 496, "직접 배선해 보면 런타임이 대신해 주던 일이 드러난다")
ddx.stage_chain(d, 316,
  ["§1 진화", "§2 계보", "§3·§4 프리미티브", "§5 맨손 배선"],
  [("스택 수", "1개 → N개", "포트 충돌", None),
   ("계보", "engine · runtime", "OCI 가 묶음", None),
   ("두 축", "cgroup · namespace", "runC 가 만듦", ACC),
   ("손 배선", "netns·veth·br0", "CNI 의 이유", INFO)],
  ["남은 문제", "분해하면", "직접 하면"])
d.t(36, 468, "커널 프리미티브 둘이 이 편의 한가운데다 — 앞은 그것이 왜 필요했나이고, "
             "뒤는 그것을 손으로 다루면 무엇이 남나다", 12, MUTED, KR, "start")
d.legend(512, [("이 편의 한가운데", ACC), ("다음 편으로", INFO)])
d.save("03-01.chapter-overview.svg"); print("ok 03-01.chapter-overview")
