# 06-01.alb-ingress-flow — 어노테이션이 실제 AWS 자원이 되기까지
# 타입 스펙: type-architecture.md — 컨트롤러가 만드는 실재 AWS 자원(ALB · 대상 그룹 · 리스너 · 규칙)의 구성도. 단계 머리가 만들어지는 순서를 맡는다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO
W, H = 1000, 560
d = D(W, H, "ANNOTATIONS BECOME REAL AWS RESOURCES",
      "어노테이션 몇 줄이 실제 AWS 자원이 되기까지",
      "컨트롤러가 Ingress 를 보고 ALB·Target Group·Rule 을 실제로 만든다. YAML 몇 줄이 과금되는 자원이 된다.",
      lead="YAML 몇 줄이 실제로 만들어지고 과금되는 AWS 자원이 된다")
ddx.band(d, 104, 496, "만드는 것은 컨트롤러이고, 만들어지는 것은 진짜 AWS 자원이다")
ddx.stage_chain(d, 316,
  ["① 감시", "② ALB", "③ 대상과 리스너", "④ 규칙"],
  [("이벤트 감시", "API 서버 watch", "Ingress 생성 감지", None),
   ("ALB 생성", "internal · external", "AWS 실자원", ACC),
   ("대상·리스너", "서비스마다 Target Group", "헬스체크용 NodePort 포함", None),
   ("규칙", "경로마다 Rule", "path → 서비스 매핑", None)],
  ["조건 충족", "그 안에", "마지막"])
d.t(36, 468, "Ingress 오브젝트를 지우면 이 자원들도 함께 지워진다 — 수명이 YAML 에 묶여 있다",
     12, MUTED, KR, "start")
d.legend(512, [("과금되는 실자원", ACC)])
d.save("06-01.alb-ingress-flow.svg"); print("ok alb-ingress-flow")
