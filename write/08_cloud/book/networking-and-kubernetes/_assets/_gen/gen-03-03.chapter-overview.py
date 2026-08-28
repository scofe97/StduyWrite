# 03-03.chapter-overview — 네 단계 지도
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
d = D(W, H, "03-03 · KNOCK FROM EVERY SIDE",
      "이미지를 만들어 띄우고 사방에서 두드려 규칙을 찾는 순서",
      "여섯 방향에서 두드려 보면 무엇이 되고 무엇이 안 되는지가 갈리고, 안 되는 쪽이 다음 기술의 이유가 된다.",
      lead="되는 쪽보다 안 되는 쪽이 다음 기술의 이유를 말해 준다")
ddx.band(d, 104, 496, "안 되는 자리 둘이 Pod 와 오버레이가 필요한 이유다")
ddx.stage_chain(d, 316,
  ["§1 이미지", "§2 같은 호스트", "§2 컨테이너끼리", "§3 다른 호스트"],
  [("이미지", "multistage 빌드", "레이어가 곧 크기", None),
   ("여섯 방향", "-p 80:8080", "안은 8080 밖은 80", None),
   ("lo 불통", "각자 별개 스택", "Pod 가 필요한 이유", ACC),
   ("경로 없음", "No route to host", "오버레이·CNI 의 이유", BAD)],
  ["띄우고", "서로는", "밖에서는"])
d.t(36, 468, "같은 호스트인데도 lo 로 서로 못 닿는다 — 그 한 줄이 Pod 라는 묶음을 낳았다",
     12, MUTED, KR, "start")
d.legend(512, [("Pod 가 필요한 이유", ACC), ("오버레이가 필요한 이유", BAD)])
d.save("03-03.chapter-overview.svg"); print("ok 03-03.chapter-overview")
