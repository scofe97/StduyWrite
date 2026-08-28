# 13-01 §2 — 관문이 둘이고 보는 것이 다르다
# 본문이 "스키마는 모양을 강제해도 행동은 강제하지 못한다"를 요점으로 둔다. 그러니 한 필드가
# 지나는 경로 위에 관문 둘을 세우고, 둘째 관문에서 조용히 사라지는 갈래를 focal 로 잡는다.
# 타입 스펙: type-flowchart.md — 관문 둘을 지나 갈리는 판단 — 스키마는 모양만 보고 통과시키고, 컨트롤러가 구현하지 않으면
#           에러 없이 조용히 지나간다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1240, 640, "KUBERNETES IN ACTION · 13-01",
      "스키마는 모양을 보고, 컨트롤러는 행동을 한다",
      "지원하지 않는 필드를 적어도 예외가 나지 않는다. 스키마 관문은 그 필드가 있는지와 타입이 맞는지까지 "
      "보고, 그대로 행동하는지는 검사 범위 밖이다.",
      "구현이 지원하지 않는 필터를 하나 적었다고 하자")

ddx.node(d, 150, 300, "apply 한 필드", "filters: - type: ...", 210, 84, INFO)
d.box(370, 236, 230, 128, PAPER2, RULE, 1.2, 8)
d.t(485, 268, "관문 1 — CRD 스키마", 12, INK, KR, "middle", 600)
d.t(485, 294, "그 필드가 있는가", 11, MUTED, KR)
d.t(485, 314, "타입이 맞는가", 11, MUTED, KR)
d.t(485, 344, "행동은 보지 않는다", 10, SOFT, KR)
d.path("M 258 300 L 364 300", MUTED, 1.5, m="ar")

ddx.node(d, 720, 300, "저장된다", "get 으로 조회해도 정상", 210, 84, OK)
d.path("M 606 300 L 608 300 L 608 300 L 610 300", MUTED, 1.5)
d.path("M 606 300 L 610 300", MUTED, 1.5, m="ar")

d.box(850, 236, 230, 128, PAPER2, RULE, 1.2, 8)
d.t(965, 268, "관문 2 — 컨트롤러", 12, INK, KR, "middle", 600)
d.t(965, 294, "이 구현이", 11, MUTED, KR)
d.t(965, 314, "그 필드를 구현했는가", 11, MUTED, KR)
d.path("M 828 300 L 844 300", MUTED, 1.5, m="ar")

d.path("M 1082 276 L 1102 276 L 1102 216 L 1120 216", OK, 1.5, m="ok")
ddx.tag(d, 1160, 200, "프록시 설정에 반영", OK, 150)
d.path("M 1082 324 L 1102 324 L 1102 384 L 1120 384", ACC, 1.5, m="acc")
ddx.focal_tag(d, 1160, 400, "조용히 지나간다", 150)
d.t(1160, 434, "예외도 에러 로그도 없다", 10, ACC, KR)

d.t(24, 486, "그래서 두 축이 각각 다른 관문을 보장한다.", 11, MUTED, KR, "start")
for i, (t, s) in enumerate((("release channel", "내가 쓴 YAML 이 다음 버전에서도 유효한가 — 첫 관문을 계속 통과하는가"),
                            ("support level", "구현을 바꿔도 같게 동작하는가 — 둘째 관문을 통과하는가"))):
    d.t(24, 512 + i * 22, f"· {t} — {s}", 11, MUTED, KR, "start")
d.t(24, 566, "헷갈리는 자리는 standard + extended 다. 채널이 같으니 스키마 검사는 똑같이 통과시키지만, "
             "이 구현이 지원하는지는 여전히 별개다.", 11, SOFT, KR, "start")
d.legend(586, [("통과한 상태", OK), ("사라지는 갈래", ACC)])
d.save("13-01-schema-shape-not-behavior.svg")
print("ok")
