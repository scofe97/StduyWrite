# 11-03 §4 — 무엇을 묻느냐가 장애 범위를 정한다
# 같은 사건에서 갈리는 두 결말이라 같은 골격의 체인 둘. 치르는 값(전면 장애)이 focal.
# 타입 스펙: type-flowchart.md — readiness 가 외부 의존을 검사하느냐 자기 상태를 검사하느냐 — 조건 하나에서 두 결말로 갈린다.
#           같은 지연이 전면 장애도 되고 부분 응답도 되는 것이 그 분기의 값이다.

#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, KR
import ddx

d = D(1200, 664, "KUBERNETES IN ACTION · 11-03",
      "무엇을 묻느냐가 장애 범위를 정한다",
      "파드 열 개가 같은 Quote 를 보고 있으니, 그 Quote 가 느려지면 열 개가 같은 시각에 같은 답을 낸다. "
      "동시 실패는 운 나쁜 예외가 아니라 공유 의존이 부르는 필연이다.",
      "Quote 서비스가 1 초 지연됐을 때")

CX = [165, 455, 745, 1035]

def chain(y0, label, nodes, arrow_c, focal_idx):
    ddx.band(d, y0, y0 + 210, label, x=24, w=1152)
    cy = y0 + 118
    for i, (cx, (t, s)) in enumerate(zip(CX, nodes)):
        ddx.node(d, cx, cy, t, s, 230, 88, c=None if i != focal_idx else None,
                 focal=(i == focal_idx))
    for a, b in zip(CX, CX[1:]):
        d.path(f"M {a+121} {cy} L {b-125} {cy}", arrow_c, 1.5,
               m="bad" if arrow_c is BAD else "ok")

chain(100, "readiness 가 외부 의존을 검사할 때",
      [("Quote 1 초 지연", "남의 서비스가 느려졌다"),
       ("파드 10 개 전부 실패", "같은 의존을 보니 같은 답"),
       ("명단이 빈다", "받을 파드가 없다"),
       ("전면 장애", "회복까지 10 초 넘게")], BAD, 3)

chain(334, "readiness 가 자기 상태만 검사할 때",
      [("Quote 1 초 지연", "남의 서비스가 느려졌다"),
       ("파드 10 개 그대로 ready", "자기 응답 여부만 본다"),
       ("명단 10 개 유지", "받을 파드가 그대로"),
       ("부분 응답", "인용구만 비운다")], OK, None)

d.t(24, 574, "위쪽에서 실제로 벌어진 일은 남의 장애를 자기 장애로 승격시킨 것이다. readiness 는 "
             "'이 파드가 요청을 받을 수 있는가'만 묻고, '좋은 응답을 만들 수 있는가'는 모니터링이 볼 몫이다.",
     11, MUTED, KR, "start")
d.legend(618, [("무너지는 길", BAD), ("버티는 길", OK), ("치르는 값", ACC)])
d.save("11-03-readiness-external-dependency-cascade.svg")
print("ok")
