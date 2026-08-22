# 03-02.chapter-overview — 네 단계 지도
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "03-02 · MODES AND CNI",
      "격리를 얼마나 포기하는가에서 시작해 표준이 갈리는 곳까지",
      "모드는 격리를 얼마나 내주느냐의 눈금이다. 그 눈금을 따라가면 호스트를 넘는 방법과 표준의 갈림길이 나온다.",
      lead="모드는 격리를 얼마나 내주느냐의 눈금 · 그 끝에 표준의 갈림길이 있다")
ddx.band(d, 104, 496, "무엇을 포기하면 무엇을 얻는지가 모드마다 다르다")
ddx.stage_chain(d, 316,
  ["§1 모드 7종", "§2·§3 Docker 방식", "§4 호스트 넘기", "§5 표준 갈림길"],
  [("격리 눈금", "None → Host", "무엇을 포기하나", None),
   ("Docker 배선", "docker0 · CNM", "sandbox·endpoint", None),
   ("호스트 넘기", "MAC-in-UDP", "VTEP 가 감싸고 벗김", None),
   ("표준 갈림", "CNM 아닌 CNI", "Kubernetes 의 선택", ACC)],
  ["실측하면", "호스트 밖", "표준은"])
d.t(36, 468, "Kubernetes 가 CNM 을 두고 CNI 를 고른 자리가 이 편의 끝이다 — 그 선택이 다음 장을 연다",
     12, MUTED, KR, "start")
d.legend(512, [("표준이 갈리는 자리", ACC)])
d.save("03-02.chapter-overview.svg"); print("ok 03-02.chapter-overview")
