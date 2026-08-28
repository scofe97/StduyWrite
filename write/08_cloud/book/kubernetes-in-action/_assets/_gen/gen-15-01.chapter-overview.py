# 15-01 전체 지도 — 간접 구조가 무엇을 가능하게 하는가
# 본문이 이 도식을 두고 "색이 붙은 곳은 두 군데뿐이고 나머지는 전부 회색"이라 서술하고,
# 앰버 띠와 붉은 띠가 각각 무엇을 가리키는지까지 적는다. 그 규격을 그대로 지킨다.
# 타입 스펙: type-process.md — 절마다 같은 의미 슬롯(절 번호 · 이름 · 한 줄)이 같은 자리에 반복된다. 가로 체인이 아니라
#           세로로 쌓았을 뿐 판단은 같다 — semantic-patterns 의 Stage framework with semantic slots.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
#           38개 메뉴의 공백이라 visual-diagram-selection 의 "알려진 공백" 에 같이 적어 두었다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, KR
import ddx

d = D(1180, 592, "KUBERNETES IN ACTION · 15-01",
      "간접 구조가 무엇을 가능하게 하는가",
      "Deployment 는 파드를 직접 만들지 않고 ReplicaSet 을 사이에 둔다. 그 한 겹이 세대를 구분하고, "
      "삭제가 어디까지 내려갈지도 그 계층을 따라 정해진다.",
      "§1 관계 · §2·§3 생성과 조회 · §4 해시 · §5·§6 스케일과 삭제")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  관계", "Deployment 는 파드를 직접 만들지 않고 ReplicaSet 을 사이에 둔다", None, None),
    ("§2·§3  생성과 조회", "spec 은 ReplicaSet 에 strategy 하나가 더해진 모양이다", None, None),
    ("§4  pod-template-hash", "그 간접 구조가 세대를 어떻게 구분하는지 보인다",
     "해시가 이름과 label 양쪽에 붙어야 옛 ReplicaSet 이 새 파드를 안 잡는다", WARN),
    ("§5·§6  스케일과 삭제", "두 작업 모두 같은 계층을 따라 아래로 전달된다",
     "--cascade=orphan 은 바로 아래 한 단계만 끊는다 — 파드는 그대로 남는다", BAD),
])

d.t(24, 512, "각 층은 바로 아래만 알고 그 아래는 모른다. 이 무지가 층을 나눈 이유이고, "
             "ReplicaSet 에 업데이트를 넣지 않고 그런 ReplicaSet 을 둘 두는 쪽을 택한 이유다.",
     11, MUTED, KR, "start")
d.legend(536, [("주의할 자리", WARN), ("잘못 읽기 쉬운 자리", BAD)])
d.save("15-01.chapter-overview.svg")
print("ok")
