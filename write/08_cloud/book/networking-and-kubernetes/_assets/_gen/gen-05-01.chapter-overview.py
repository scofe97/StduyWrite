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
d = D(W, H, "05-01 · MATERIALS OF A SERVICE",
      "안정된 이름과 서비스의 실제 대상 목록 — 두 역할과 그 목록이 쪼개진 이유",
      "이름을 고정하는 쪽과 대상 주소를 표현하는 쪽은 서로 다른 일을 한다. 그 목록이 커지면서 갱신 단위가 쪼개졌다.",
      lead="이름을 고정한다 · 대상을 표현한다 · 커지면 갱신 단위를 쪼갠다")
ddx.band(d, 104, 496, "두 역할 · 그리고 목록이 쪼개진 이유")
ddx.stage_chain(d, 316,
  ["§1 StatefulSet", "§2 EndpointSlice", "§3 병목", "§3 분할"],
  [("안정된 이름", "StatefulSet", "재생성을 넘는 정체성", None),
   ("대상 주소·상태", "EndpointSlice", "addresses · ready", None),
   ("규모의 병목", "객체 전체 재전송", "노드 수천 × 변경 빈도", BAD),
   ("갱신 범위 축소", "부분집합 분할", "바뀐 slice 만", ACC)],
  ["다른 역할", "커지면", "그래서"], bw=172, gap=84, x0=24, sizes=(14, 12, 12))
d.legend(512, [("규모의 병목", BAD), ("그래서 나온 것", ACC)])
d.save("05-01.chapter-overview.svg"); print("ok 05-01.chapter-overview")
