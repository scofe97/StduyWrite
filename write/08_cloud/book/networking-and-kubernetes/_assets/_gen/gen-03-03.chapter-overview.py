# 03-03.chapter-overview — 네 단계 지도
# 타입 스펙: type-data-flow.md — 단계 머리를 세우고 그 아래 한 칸씩 — 편 전체를 한 줄로 잇는 지도
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
