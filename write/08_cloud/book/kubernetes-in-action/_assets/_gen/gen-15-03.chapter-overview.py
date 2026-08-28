# 15-03 전체 지도 — 롤아웃을 사람이 어디까지 잡는가
# 본문이 "색이 붙은 곳은 두 군데뿐이고 둘 다 오해하기 쉬운 지점"이라 서술하고 두 띠의 뜻을
# 적는다. 앰버는 §2 의 available 오해, 붉은은 §3 의 undo 부작용이다.
# 타입 스펙: type-process.md — 절마다 같은 의미 슬롯이 세로로 반복된다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
#           38개 메뉴의 공백이라 visual-diagram-selection 의 "알려진 공백" 에 같이 적어 두었다.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, BAD, MUTED, KR
import ddx

d = D(1180, 592, "KUBERNETES IN ACTION · 15-03",
      "롤아웃을 사람이 어디까지 잡는가",
      "멈춰 세워 눈으로 보는 것부터, 사람 없이 자동으로 막는 것, 이미 벌어진 일을 되돌리는 것까지. "
      "Deployment 가 못 하는 전략은 다른 리소스로 만든다.",
      "§1 pause · §2 minReadySeconds · §3 undo · §4 배포 전략")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  pause", "사람이 롤아웃을 멈추고 눈으로 확인한다", None, None),
    ("§2  minReadySeconds", "사람 없이 결함 버전을 자동으로 막는다",
     "available 은 롤아웃 진행 판단에만 쓰인다 — 트래픽 수신 여부를 가르지 않는다", WARN),
    ("§3  rollout undo", "이미 벌어진 일을 되돌린다",
     "minReadySeconds 가 ReplicaSet 에 저장돼, undo 가 그 값까지 되돌린다", BAD),
    ("§4  배포 전략", "Deployment 가 지원하지 않는 전략을 다른 리소스로 만든다", None, None),
])

d.t(24, 512, "앞의 셋은 같은 축의 눈금이다 — 사람이 얼마나 개입하느냐. pause 는 전부, "
             "minReadySeconds 는 조건만, undo 는 사후에 개입한다.", 11, MUTED, KR, "start")
d.legend(536, [("오해하기 쉬운 판정", WARN), ("되돌릴 때 딸려 오는 것", BAD)])
d.save("15-03.chapter-overview.svg")
print("ok")
