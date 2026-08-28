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
d = D(W, H, "04-03 · POLICY AND NAMES", "누가 통할 수 있는지를 정하고, 그 통신의 이름과 주소로 4장을 닫는다", "정책은 선택되는 순간부터 판정을 시작한다. 문법의 대시 하나가 범위를 바꾸고, 그다음이 이름과 주소다.", lead="정책은 선택되는 순간 잠긴다 · 문법의 대시 하나가 범위를 바꾼다")
ddx.band(d, 104, 496, "기본은 전부 허용이고, 선택되는 순간 기본이 뒤집힌다")
ddx.stage_chain(d, 316, ["§1 동작 모델", "§2·§3 문법", "§4 Cilium", "§5·§6 이름과 주소"], [("잠기는 순간", "선택되면 차단", "기본은 전부 허용", ACC),
   ("문법", "셀렉터·peer", "대시 하나가 갈림", None),
   ("L7 정책", "경로 단위로", "Cilium 확장", None),
   ("이름·주소", "CoreDNS·dual-stack", "검색 경로의 비용", INFO)], ["무엇으로", "더 좁히면", "그다음"])
d.t(36, 468, "선택되지 않은 Pod 는 아무 제한도 받지 않는다 — 그래서 '선택되었는가'가 첫 관문이다", 12, MUTED, KR, "start")
d.legend(512, [("기본이 뒤집히는 순간", ACC), ("4 장을 닫는 자리", INFO)])
d.save("04-03.chapter-overview.svg"); print("ok 04-03")
