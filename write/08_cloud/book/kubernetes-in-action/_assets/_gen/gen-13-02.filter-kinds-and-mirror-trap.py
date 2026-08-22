# 13-02 §4 — 흐름 구조로 가른 세 갈래
# 짝 도식이 '무엇을 고치는가'를 맡으므로 이쪽은 흐름 모양만 그린다. 갈래마다 화살표 개수가
# 달라야 세 갈래라는 말이 눈에 보인다. 부수효과 함정이 이 도식의 focal.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 754, "KUBERNETES IN ACTION · 13-02",
      "흐름이 하나냐, 둘이냐, 없냐",
      "필터 여섯은 트래픽 흐름 구조로 세 갈래가 된다. 화살표가 몇 개 나가는지가 그 갈래를 정한다.",
      "게이트웨이에서 백엔드로 가는 모양")

def lane(y0, h, label, filters, c):
    ddx.band(d, y0, y0 + h, label, x=24, w=1172)
    d.t(52, y0 + 52, filters, 10, c, MONO, "start")

# 갈래 1 — 흐름 하나
lane(100, 176, "요청 하나 → 목적지 하나", "Header 2 종 · URLRewrite · ExtensionRef", SOFT)
ddx.node(d, 320, 214, "게이트웨이", "요청을 고친다", 200, 62, INFO)
ddx.node(d, 700, 214, "백엔드", "응답을 돌려준다", 200, 62, OK)
d.path("M 422 214 L 596 214", MUTED, 1.5, m="ar")

# 갈래 2 — 흐름 복제
lane(300, 232, "흐름 복제 — RequestMirror", "복사본 응답은 버려진다", ACC)
ddx.node(d, 320, 440, "게이트웨이", "복사본을 하나 더 만든다", 200, 62, INFO)
ddx.node(d, 700, 400, "kiada-stable", "이 응답만 클라이언트로", 200, 62, OK)
ddx.node(d, 700, 486, "kiada-new", "응답은 버려진다", 200, 62, ACC)
d.path("M 422 428 L 500 428 L 500 400 L 596 400", MUTED, 1.5, m="ar")
d.path("M 422 452 L 520 452 L 520 486 L 596 486", ACC, 1.5, m="acc", dash="6 5")
ddx.focal_tag(d, 1000, 486, "부수효과는 두 번 일어난다", 260)
d.t(1000, 518, "복사본을 받은 백엔드는 복사본인 줄 모른다", 10, ACC, KR)

# 갈래 3 — 백엔드 없음
lane(556, 132, "백엔드 없음 — RequestRedirect", "backendRefs 가 필요 없다", WARN)
ddx.node(d, 320, 634, "게이트웨이", "301 로 직접 답한다", 200, 62, INFO)
ddx.node(d, 700, 634, "백엔드", "가지 않는다", 200, 62, dim=True)
d.path("M 422 634 L 596 634", MUTED, 1.4, m="ar", dash="5 5")
d.path("M 320 604 L 320 588", WARN, 1.5, m="warn")
d.t(340, 596, "클라이언트로 되돌아간다", 11, WARN, KR, "start")

d.legend(706, [("게이트웨이", INFO), ("응답을 주는 쪽", OK), ("복제·함정", ACC), ("되돌린다", WARN)])
d.save("13-02-filter-kinds-and-mirror-trap.svg")
print("ok")
