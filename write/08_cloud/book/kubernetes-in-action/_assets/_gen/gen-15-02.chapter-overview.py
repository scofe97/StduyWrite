# 15-02 전체 지도 — 무엇이 교체 속도를 정하는가
# 본문이 "색이 붙은 곳은 두 군데뿐이고 둘 다 다운타임에 관한 경고"라 서술하고 앰버·붉은 띠가
# 각각 무엇을 가리키는지 적는다. 그 규격을 지킨다 — 임의로 칠하면 본문이 틀려진다.
# 타입 스펙: type-process.md — 절마다 같은 의미 슬롯이 세로로 반복된다.
#           2026-08-29 덧붙임: type-process 정본의 입력 계약도 역할 레인 1~6 이 전제인데 이 그림에
#           레인은 없다. 그래도 process 를 두는 것은, 주체를 요구하지 않는 유일한 라우팅 규칙이
#           semantic-patterns 의 "Stage framework with semantic slots" 한 줄이기 때문이다.
#           38개 메뉴의 공백이라 visual-diagram-selection 의 "알려진 공백" 에 같이 적어 두었다.
import sys; sys.path.insert(0, ".")
from dd import D, WARN, BAD, MUTED, KR
import ddx

d = D(1180, 592, "KUBERNETES IN ACTION · 15-02",
      "무엇이 교체 속도를 정하는가",
      "Pod 템플릿을 바꾸면 교체가 시작된다. 얼마나 빨리, 몇 개씩 바뀌는지는 strategy 와 두 파라미터가 "
      "정하고, 설정이 옳아도 준비 판정이 틀리면 그 계산이 무너진다.",
      "§1 시작 조건 · §2·§3 두 전략 · §4 두 파라미터 · §5·§6 한계")

ddx.chapter_map(d, 108, x=24, w=1132, rows=[
    ("§1  시작 조건", "Pod 템플릿을 바꾸면 교체가 시작되고, 방식은 strategy 가 정한다", None, None),
    ("§2·§3  두 전략", "Recreate 는 동시에 전부, RollingUpdate 는 하나씩 바꾼다",
     "Recreate 는 가용 파드 0 인 구간을 만든다", WARN),
    ("§4  두 파라미터", "maxSurge 와 maxUnavailable 이 한 번에 움직일 보폭을 정한다", None, None),
    ("§5·§6  한계", "설정이 옳아도 준비 판정이 틀리면 끊기고, 롤아웃 중 재롤아웃은 방향만 튼다",
     "maxUnavailable: 0 이어도 readiness 가 부정확하면 요청이 끊긴다", BAD),
])

d.t(24, 512, "두 파라미터가 정하는 것은 보폭이지 안전이 아니다. 실제로 요청이 끊기느냐는 "
             "readiness probe 가 '이 파드가 받을 수 있다'를 정확히 답하느냐에 달렸다.", 11, MUTED, KR, "start")
d.legend(536, [("다운타임이 생기는 구간", WARN), ("설정으로 못 막는 자리", BAD)])
d.save("15-02.chapter-overview.svg")
print("ok")
