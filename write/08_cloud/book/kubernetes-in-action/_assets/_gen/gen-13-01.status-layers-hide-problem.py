# 13-01 §5 — 같은 True 를 어떻게 읽느냐에서 갈린다
# 앞 도식이 채워지는 순서를 따라갔다면 이쪽은 반대 방향이다. 404 를 만난 뒤 조회가 갈라지는
# 지점이 주제라, 공통 구간을 하나 두고 그 뒤를 두 갈래로 벌린다. 원인을 찾는 갈래가 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1200, 620, "KUBERNETES IN ACTION · 13-01",
      "PROGRAMMED: True 는 '입구가 열렸다'까지다",
      "그 True 의 뜻은 설정이 생성돼 게이트웨이에 닿을 수 있다는 것이지 라우팅이 완성됐다는 뜻이 아니다. "
      "입구는 열렸고 안내판이 없는 상태로 읽으면 맞는다.",
      "게이트웨이에 접속했더니 404 가 났다")

ddx.node(d, 150, 300, "404 를 만났다", "게이트웨이는 응답한다", 210, 84, BAD)
ddx.node(d, 460, 300, "kubectl get gtw", "PROGRAMMED: True", 240, 84)
d.path("M 258 300 L 334 300", MUTED, 1.5, m="ar")
d.t(360, 348, "여기까지는 누구나 같다", 10, SOFT, KR)

d.path("M 584 276 L 680 200", BAD, 1.5, m="bad")
d.box(700, 158, 420, 84, PAPER2, BAD, 1.1, 6)
d.t(910, 190, "초록불로 읽고 멈춘다", 13, BAD, KR, "middle", 600)
d.t(910, 214, "게이트웨이 바깥을 뒤지게 된다 — 서비스·파드·DNS", 11, MUTED, KR)

d.path("M 584 324 L 680 400", ACC, 1.5, m="acc")
d.o.append(f'<rect x="700" y="358" width="420" height="112" rx="6" '
           f'fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
d.t(910, 388, "3 층을 따로 조회한다", 13, ACC, KR, "middle", 600)
d.t(910, 414, "kubectl get gtw kiada -o jsonpath=", 10, MUTED, MONO)
d.t(910, 430, "'{.status.listeners[*].attachedRoutes}'", 10, MUTED, MONO)
d.t(910, 456, "0  ← Route 가 하나도 안 붙었다", 11, ACC, KR)

d.t(24, 512, "흔히 쓰는 명령이 위 두 층만 보여 준다. Gateway 전체 conditions 는 초록불인데 원인은 "
             "listener 층의 attachedRoutes 에 있다.", 11, MUTED, KR, "start")
d.t(24, 534, "그래서 게이트웨이로 접속되지 않으면 Gateway status 뿐 아니라 해당 listener 의 status 도 확인한다.",
     11, MUTED, KR, "start")
d.legend(556, [("막다른 갈래", BAD), ("원인에 닿는 갈래", ACC)])
d.save("13-01-status-layers-hide-problem.svg")
print("ok")
