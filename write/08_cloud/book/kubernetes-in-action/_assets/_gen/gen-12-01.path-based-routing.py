# 12-01 §5 — 같은 호스트, 갈라지는 경로
# 규칙과 요청을 마주 놓고 어느 쪽이 잡히는지를 보인다. pathType 이 판정을 바꾸는 축이라
# 규칙 칩에 함께 박았다. 요소 단위 비교라는 함정은 아래 산문이 맡는다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 620, "KUBERNETES IN ACTION · 12-01",
      "한 호스트 아래에서 경로가 가른다",
      "api.example.com 으로 온 요청을 프록시가 열어 경로를 읽고 규칙에 맞춘다. "
      "무엇에 맞느냐는 path 뿐 아니라 pathType 이 함께 정한다.",
      "host: api.example.com")

REQ = [("GET /quote", "정확히 그 경로", 190),
       ("GET /questions/5", "그 아래 경로", 300),
       ("GET /quotes", "복수형 오타", 410)]
for t, s, y in REQ:
    ddx.node(d, 170, y, t, s, 260, 76, INFO)

d.path(f"M 344 {REQ[0][2]} L 344 {REQ[-1][2]}", MUTED, 1.4)
d.path("M 344 300 L 386 300", MUTED, 1.4, m="ar")
ddx.node(d, 500, 300, "L7 프록시", "경로를 읽어 맞춘다", 220, 92)
for _, _, y in REQ:
    d.path(f"M 302 {y} L 344 {y}", MUTED, 1.4)

RULE = [("path: /quote", "pathType: Exact", "quote", OK, 190),
        ("path: /questions", "pathType: Prefix", "quiz", OK, 300),
        (None, None, "어느 규칙에도 안 맞는다", BAD, 410)]
# 규칙마다 색이 갈리므로 줄기는 중립색으로 둔다.
d.path("M 612 300 L 668 300", MUTED, 1.2)
d.path(f"M 668 {RULE[0][4]} L 668 {RULE[-1][4]}", MUTED, 1.2)
for t, s, svc, c, y in RULE:
    if t:
        d.box(760, y - 32, 240, 64, PAPER2, c, 1.1, 6)
        d.t(880, y - 8, t, 12, c, MONO, "middle", 600)
        d.t(880, y + 14, s, 10, MUTED, MONO)
        d.path(f"M 668 {y} L 754 {y}", c, 1.4, m="ok")
        ddx.node(d, 1120, y, svc, "ClusterIP", 160, 64, c)
        d.path(f"M 1002 {y} L 1034 {y}", c, 1.3, m="ok")
    else:
        d.path(f"M 668 {y} L 790 {y}", c, 1.4, m="bad", dash="5 5")
        ddx.tag(d, 960, y, svc, c, 300)

ddx.focal_tag(d, 500, 452, "Exact 가 Prefix 를 이긴다 — 순서가 아니라 구체성", 340)

d.t(24, 520, "Prefix 는 문자열 접두사가 아니라 경로 요소들의 접두사다. /foo 는 /foo/bar 에는 맞지만 "
             "/foobar 에는 맞지 않는다 — 요소가 통째로 다르기 때문이다.", 11, MUTED, KR, "start")
d.t(24, 542, "구체성이 이기므로 선언 순서를 바꿔도 결과가 같고, '일반 규칙 + 예외' 패턴이 성립한다.",
     11, MUTED, KR, "start")
d.legend(562, [("들어온 요청", INFO), ("잡히는 규칙", OK), ("안 잡히는 요청", BAD), ("판정 기준", ACC)])
d.save("12-01-path-based-routing.svg")
print("ok")
