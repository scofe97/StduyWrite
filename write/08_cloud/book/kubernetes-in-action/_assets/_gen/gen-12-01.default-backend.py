# 12-01 §7 — 안 맞은 요청이 가는 곳
# 규칙 판정에서 떨어진 요청의 행선지가 주제다. 기본 404 와 defaultBackend 를 나란히 놓고,
# 서비스를 하나 두는 쓸모 셋을 그 아래 붙인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO
import ddx

d = D(1180, 600, "KUBERNETES IN ACTION · 12-01",
      "규칙에서 떨어진 요청을 누가 받나",
      "어떤 규칙에도 맞지 않는 요청은 기본적으로 프록시의 밋밋한 404 로 끝난다. "
      "defaultBackend 를 두면 그 요청이 서비스 하나로 모여, 버려지는 대신 쓸 수 있는 것이 된다.",
      "GET /quotes — 복수형 오타로 온 요청")

ddx.node(d, 160, 280, "안 맞은 요청", "GET /quotes", 220, 84, INFO)
ddx.node(d, 470, 280, "규칙 판정", "host · path 모두 불일치", 240, 84)
d.path("M 272 280 L 344 280", MUTED, 1.5, m="ar")

d.path("M 592 258 L 700 196", WARN, 1.4, m="warn", dash="5 5")
ddx.node(d, 850, 196, "프록시 기본 404", "텍스트 한 줄로 끝난다", 260, 76, WARN)
d.t(660, 178, "defaultBackend 가 없으면", 10, WARN, KR)

d.path("M 592 302 L 700 380", ACC, 1.5, m="acc")
ddx.node(d, 850, 380, "defaultBackend", "fun404 서비스로", 260, 76, focal=True)
d.t(660, 372, "두면", 10, ACC, KR)

USE = ["친절한 404 페이지 — 밋밋한 텍스트 대신",
       "오타·구버전 경로 흡수 — 안내하거나 리다이렉트",
       "관측 — 규칙이 빠진 경로를 대시보드로 안다"]
d.t(24, 470, "서비스를 하나 두는 쓸모 셋", 12, SOFT, KR, "start")
for i, u in enumerate(USE):
    d.t(24, 494 + i * 22, f"· {u}", 11, MUTED, KR, "start")

d.legend(560, [("떨어진 요청", INFO), ("두지 않았을 때", WARN), ("catch-all", ACC)])
d.save("12-01-default-backend.svg")
print("ok")
