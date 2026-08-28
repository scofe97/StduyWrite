# 03-01.chapter-overview — 네 단계 지도
# 타입 스펙: type-process.md — 단계 머리 + 한 줄 체인. 칸마다 같은 의미 슬롯(절 번호 · 이름 ·
#           한 줄 요약 · 꼬리표)이 같은 자리에 반복된다(semantic-patterns 의 "Stage framework
#           with semantic slots"). 화살표는 데이터가 아니라 읽는 순서를 나른다.
#           2026-08-28 type-data-flow 에서 옮겼다 — data-flow 정본은 "who does what at each
#           stage" 와 role-scoped lane 을 전제로 하는데, 편 지도에는 주체도 레인도 없다.
#           엄밀히는 두 정본 다 주체 기반이라 편 지도는 표의 공백에 가깝고, 주체 없이도 맞는
#           유일한 라우팅 규칙이 위 semantic-patterns 한 줄이라 그쪽을 따랐다.
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
