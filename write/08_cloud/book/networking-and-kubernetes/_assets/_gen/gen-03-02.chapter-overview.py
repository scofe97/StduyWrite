# 03-02.chapter-overview — 네 단계 지도
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
