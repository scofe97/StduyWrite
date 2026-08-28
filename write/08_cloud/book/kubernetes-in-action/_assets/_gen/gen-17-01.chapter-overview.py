# 17-01 전체 지도 — 노드 수가 기준이 된다
# 본문이 "색이 붙은 곳은 두 군데뿐이고 둘 다 주의 표시"라 서술하고, 2 단계와 4 단계의 앰버 띠가
# 각각 무엇을 뜻하는지 적는다. 둘 다 앰버다 — 붉은 띠는 없다.
# 타입 스펙: type-process.md — 절마다 같은 의미 슬롯(절 번호·요점·주의)이 세로로 반복된다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
#           38개 메뉴의 공백이라 visual-diagram-selection 의 "알려진 공백" 에 같이 적어 두었다.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, MUTED, KR
import ddx

d = D(1180, 664, "KUBERNETES IN ACTION · 17-01",
      "노드 수가 기준이 된다",
      "ReplicaSet 이 replica 수를 맞춘다면 DaemonSet 은 노드 수를 맞춘다. 그래서 노드가 늘면 파드가 "
      "따라 늘고, 대상 노드를 좁히는 일도 replica 가 아니라 노드 쪽에서 한다.",
      "§1 이해 · §2 배포 · §3 범위 · §4 업데이트 · §5 삭제")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  이해", "replica 수 대신 노드 수가 기준이 된다", None, None),
    ("§2  배포", "노드가 셋인데 파드가 둘인 이유를 taint 로 푼다",
     "taint 중 일부는 컨트롤러가 알아서 tolerate 한다", WARN),
    ("§3  범위", "node selector 로 대상 노드를 좁힌다", None, None),
    ("§4  업데이트", "Deployment 와 기본값이 다른 이유를 본다",
     "maxSurge 를 0 보다 크게 두면 데몬이 lock 충돌로 ready 가 안 된다", WARN),
    ("§5  삭제", "파드를 남길지 함께 지울지 정한다", None, None),
])

d.t(24, 584, "노드마다 하나라는 제약이 DaemonSet 의 기본값을 Deployment 와 다르게 만든다 — "
             "같은 노드에 두 세대를 동시에 둘 수 없기 때문이다.", 11, MUTED, KR, "start")
d.legend(608, [("주의할 자리", WARN)])
d.save("17-01.chapter-overview.svg")
print("ok")
