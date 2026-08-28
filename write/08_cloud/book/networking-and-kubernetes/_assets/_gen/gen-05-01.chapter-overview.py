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
d = D(W, H, "05-01 · MATERIALS OF A SERVICE",
      "서비스가 쓰는 재료 셋 — 이름, 주소 목록, 그리고 그 목록을 쪼갠 이유",
      "이름과 순서가 있고, 준비된 주소만 모이고, 그 목록이 커지면 쪼갠다. 쪼갠 이유가 이 편의 결론이다.",
      lead="이름과 순서 → 준비된 주소 → 커지면 병목 → 그래서 쪼갠다")
ddx.band(d, 104, 496, "쪼갠 이유를 알면 EndpointSlice 가 왜 기본값이 됐는지가 따라온다")
ddx.stage_chain(d, 316,
  ["§1 StatefulSet", "§2 Endpoints", "§3 병목", "§3 EndpointSlice"],
  [("이름·순서", "StatefulSet", "Pod 마다 DNS 레코드", None),
   ("준비된 주소", "Endpoints", "ready 만 트래픽", None),
   ("규모의 병목", "객체 전체 재전송", "노드 수천 × 변경 빈도", BAD),
   ("쪼개기", "EndpointSlice", "바뀐 slice 만", ACC)],
  ["누가 준비됐나", "커지면", "그래서"], bw=176, gap=84, x0=22)
d.t(36, 468, "주소 하나가 바뀔 때 무엇이 얼마나 오가느냐가 규모의 한계를 정한다", 12, MUTED, KR, "start")
d.legend(512, [("규모의 병목", BAD), ("그래서 나온 것", ACC)])
d.save("05-01.chapter-overview.svg"); print("ok 05-01.chapter-overview")
