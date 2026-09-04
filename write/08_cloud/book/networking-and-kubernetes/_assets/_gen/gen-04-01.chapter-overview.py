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
d = D(W, H, "04-01 · POD NETWORKING MODEL", "주소를 어떻게 줄지 정하고, 그 결정을 실행하는 컴포넌트로 내려간다", "3가지 약속에서 시작해 배치를 고르고, 그 결정을 실행하는 컴포넌트까지 내려간 뒤 자격 판정으로 닫는다.", lead="3가지 약속 → 배치 선택 → 그 결정을 실행하는 컴포넌트 → 자격 판정")
ddx.band(d, 104, 496, "무엇을 약속했느냐가 배치를 고르게 하고, 배치가 컴포넌트의 일을 정한다")
ddx.stage_chain(d, 316,
  ["§1 모델", "§2 레이아웃", "§3·§4 배정과 생성", "§5 자격 판정"],
  [("3가지 약속", "NAT 없음", "Pod 마다 고유 IP", ACC),
   ("레이아웃", "격리·평면·섬", "Pod IP 를 보일까", None),
   ("컴포넌트", "CIDR · Kubelet", "CRI 와 CNI 를 부림", None),
   ("프로브", "liveness·readiness", "실패 시 무엇을 하나", INFO)],
  ["배치는", "누가 정하나", "다 뜨면"], bw=180, gap=76, x0=26)
d.t(36, 468, "3가지 약속이 이 편의 출발점이다 — 그것을 지키려고 나머지가 따라 나온다", 12, MUTED, KR, "start")
d.legend(512, [("출발점이 되는 약속", ACC), ("자격 판정", INFO)])
d.save("04-01.chapter-overview.svg"); print("ok 04-01")
