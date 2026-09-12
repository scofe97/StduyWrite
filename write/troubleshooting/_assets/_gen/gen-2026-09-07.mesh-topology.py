# 2026-09-07 C 문항 · 문제 소개 — 어떤 구조에서 일어난 일인가.
# 논지는 "메시 안에서 호출이 어느 프록시를 거치나"이지 누가 503 을 냈는가가 아니다.
# 거절의 주체는 원인 분석 절의 tomcat-connection-life 가 맡는다.
# 타입 스펙: type-architecture — 구성요소와 연결. Pod 경계로 사이드카 위치를 보인다.
import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from dd import D, ACC, MUTED, SOFT, INK, BAD, OK, PAPER2, RULE, KR, MONO

W, H = 816, 396
d = D(W, H, "TROUBLESHOOTING DRILL · 2026-09-07 C",
      "메시 안의 호출 경로",
      "주문 서비스가 결제 서비스를 부른다. 메시라 양쪽 Pod 에 사이드카 프록시가 붙어 있고, "
      "요청은 두 프록시를 거쳐 결제 앱에 닿는다.",
      lead="앱 로그가 조용하다면 앱 앞의 누군가가 답한 것입니다")

PY_ = 130
d.box(40, PY_, 300, 152, PAPER2, RULE, 1.0, 8)
d.t(56, PY_ + 22, "주문 Pod — 2/2", 12, SOFT, KR, "start", 600)
d.box(60, PY_ + 40, 118, 92, PAPER2, RULE, 0.9, 6)
d.t(119, PY_ + 74, "주문 앱", 13, INK, KR, "middle", 600)
d.t(119, PY_ + 96, "호출하는 쪽", 11, SOFT, KR, "middle")
d.tone(198, PY_ + 40, 122, 92, ACC, 6)
d.t(259, PY_ + 74, "사이드카", 13, ACC, KR, "middle", 600)
d.t(259, PY_ + 96, "Envoy", 11, SOFT, MONO, "middle")
d.arrow([(178, PY_ + 86), (194, PY_ + 86)], MUTED, "ar", 1.3)

d.arrow([(340, PY_ + 86), (396, PY_ + 86)], MUTED, "ar", 1.4)
d.t(368, PY_ + 68, "mTLS", 11, SOFT, MONO, "middle")

d.box(400, PY_, 300, 152, PAPER2, RULE, 1.0, 8)
d.t(416, PY_ + 22, "결제 Pod — 2/2 · 세 대", 12, SOFT, KR, "start", 600)
d.tone(420, PY_ + 40, 122, 92, ACC, 6)
d.t(481, PY_ + 74, "사이드카", 13, ACC, KR, "middle", 600)
d.t(481, PY_ + 96, "Envoy", 11, SOFT, MONO, "middle")
d.box(562, PY_ + 40, 118, 92, PAPER2, RULE, 0.9, 6)
d.t(621, PY_ + 74, "결제 앱", 13, INK, KR, "middle", 600)
d.t(621, PY_ + 96, "로그 조용함", 11, BAD, KR, "middle")
d.arrow([(542, PY_ + 86), (558, PY_ + 86)], MUTED, "ar", 1.3)

d.t(W // 2, 324, "Pod IP 로 직접 부르면 200 이 옵니다 — 대상 자체는 멀쩡합니다",
    13, OK, KR, "middle")
d.t(W // 2, 350, "503 은 트래픽이 오를 때만 섞이고 실패율이 트래픽을 따라 오르내립니다",
    12, MUTED, KR, "middle")

d.save(os.path.join(os.path.dirname(__file__), "..", "2026-09-07.mesh-topology.svg"))
print("ok")
