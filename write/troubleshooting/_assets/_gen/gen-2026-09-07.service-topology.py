# 2026-09-07 B 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "이름으로 부르는 길과 주소로 부르는 길이 어떻게 다른가"이지 어디가 끊겼는가가 아니다.
# 끊긴 지점은 원인 분석 절의 service-name-path 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. 두 경로를 나란히 놓아 대비한다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 800, 404
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 B",
      "두 가지로 부르는 같은 대상",
      "클라이언트 Pod 가 결제 Pod 를 두 방법으로 부른다. 주소로 직접 부르면 닿고 "
      "이름으로 부르면 시간만 흐른다. 같은 대상인데 경로가 다르다.",
      lead="한쪽만 실패하므로 두 경로의 차이가 곧 후보입니다")

d.box(40, 176, 148, 74, PAPER2, RULE, 0.9, 6)
d.t(114, 206, "클라이언트 Pod", 13, INK, KR, "middle", 600)
d.t(114, 230, "같은 네임스페이스", 11, SOFT, MONO, "middle")

d.tone(240, 118, 300, 68, OK, 6)
d.t(390, 144, "Pod IP 로 직접", 13, OK, KR, "middle", 600)
d.t(390, 168, "10.244.2.17:8080 · 200 ok", 12, SOFT, MONO, "middle")
d.arrow([(188, 198), (212, 198), (212, 152), (236, 152)], OK, "ok", 1.4)

d.tone(240, 236, 300, 88, BAD, 6)
d.t(390, 262, "Service 이름으로", 13, BAD, KR, "middle", 600)
d.t(390, 286, "payment:8080 · timeout", 12, SOFT, MONO, "middle")
d.t(390, 308, "이름 해석 → ClusterIP → 대상", 11, MUTED, KR, "middle")
d.arrow([(188, 228), (212, 228), (212, 280), (236, 280)], BAD, "bad", 1.4)

d.box(592, 176, 168, 74, PAPER2, RULE, 0.9, 6)
d.t(676, 206, "결제 Pod", 13, INK, KR, "middle", 600)
d.t(676, 230, "Running · Ready 1/1", 11, SOFT, MONO, "middle")
d.arrow([(540, 152), (566, 152), (566, 200), (592, 200)], OK, "ok", 1.4)
d.path("M 540 280 L 566 280 L 566 236 L 576 236", BAD, 1.4, dash="5 5")
d.t(584, 240, "?", 14, BAD, MONO, "start", 600)

d.t(W // 2, 372, "이름 경로에는 해석 단계와 대상 선정 단계가 더 있습니다", 13, MUTED, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-07.service-topology.svg"))
print("ok")
