# 03-02.chapter-overview — 컨테이너에 네트워크가 붙기까지 다섯 단계 지도
# 타입 스펙: type-process.md — 단계 머리 + 한 줄 체인. 칸마다 같은 의미 슬롯(절 번호 · 단계 이름 ·
#           그 단계에서 다루는 실제 이름 · 주체)이 같은 자리에 반복된다(semantic-patterns 의
#           "Stage framework with semantic slots"). 화살표는 데이터가 아니라 읽는 순서를 나른다.
#           2026-08-28 type-data-flow 에서 옮겼다 — data-flow 정본은 role-scoped lane 을 전제로
#           하는데 편 지도에는 레인이 없다.
# 이력: 2026-11-18 네 칸을 다섯 칸으로 — 본문 「컨테이너에 네트워크가 붙기까지」 절의 표(단계·주체·
#       받치는 개념)와 칸 수를 맞췄다. 칸의 셋째 줄을 그 단계의 주체로 통일했다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 452
d = D(W, H, "03-02 · FROM MODE TO STANDARD",
      "컨테이너에 네트워크가 붙기까지 — 모드에서 표준까지",
      "모드를 고르고, Docker 가 한 호스트 안을 배선하고, 그 배선을 CNM 으로 묶고, VXLAN 으로 호스트를 넘고, "
      "마지막에 배선을 CNI 플러그인에 맡기는 다섯 단계.",
      lead="왼쪽 세 칸은 한 호스트 안 · 넷째 칸에서 호스트를 넘고 · 다섯째 칸에서 표준이 갈립니다")
ddx.band(d, 104, 372, "단계마다 맡는 쪽이 다르다")
ddx.stage_chain(d, 268,
  ["§1 모드", "§2 한 호스트 배선", "§3 모델", "§4 호스트 넘기", "§5 표준"],
  [("모드 고르기", "none → host", "운영자", None),
   ("Docker 의 배선", "veth · docker0", "bridge 드라이버", None),
   ("CNM 으로 묶기", "sandbox · endpoint", "libnetwork", None),
   ("VXLAN 터널", "MAC-in-UDP · 4789", "양 끝의 VTEP", None),
   ("CNI 로 맡기기", "ADD · DEL", "런타임과 플러그인", ACC)],
  ["기본값", "추상화", "밖으로", "표준화"],
  bw=148, gap=50)
d.legend(388, [("표준이 갈리는 자리", ACC)])
d.save("03-02.chapter-overview.svg"); print("ok 03-02.chapter-overview")
