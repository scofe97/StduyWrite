# 05-03.mesh-relocation — 메시의 본질은 기능의 자리 이동이다
# 본문 요구: 일곱 기능(디스커버리·로드밸런싱·복원력·보안 mTLS·관측·라우팅 제어·API) + 구조
#           셋(게이트웨이·사이드카·컨트롤 플레인) + "컨트롤 플레인이 죽어도 데이터 플레인은 돈다".
# 타입 스펙: type-architecture.md — 앱 코드와 사이드카 프록시라는 두 자리를 잇는다. 같은 기능이 어느 컴포넌트에 사는지가 논지다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, PAPER, KR, MONO

W, H = 1000, 576   # 범례가 536 까지 내려간다
d = D(W, H, "SERVICE MESH · WHERE THE FUNCTION LIVES",
      "같은 기능이 앱 코드에서 사이드카로 옮겨 간다",
      "디스커버리·복원력·mTLS·관측을 앱마다 구현하던 것을 프록시가 대신 맡는다.",
      lead="새 기능이 생긴 것이 아니라 있던 기능의 자리가 바뀐 것이다")

BX, BW, BY, BH = 32, 368, 152, 208   # 사이 200px 를 라벨 자리로 남긴다
d.box(BX, BY, BW, BH, PAPER2, WARN, 1.1, 8)
d.t(BX + BW // 2, BY + 34, "앱 코드 안", 14, WARN, KR, "middle", 600)
for i, ln in enumerate(["서비스마다 직접 구현", "재시도·타임아웃을 코드로", "평문 통신 · 모니터링 개별 구성"]):
    d.t(BX + BW // 2, BY + 76 + i * 30, ddx.fit(ln, 12, BW - 24, ln), 12, MUTED, KR)

RX, RW = 600, 368
d.box(RX, BY, RW, BH, PAPER2, INFO, 1.1, 8)
d.t(RX + RW // 2, BY + 34, "사이드카 프록시", 14, INFO, KR, "middle", 600)
for i, ln in enumerate(["게이트웨이 — 클러스터를 드나드는 트래픽", "사이드카 — 서비스 간 트래픽을 mTLS 로", "컨트롤 플레인 — 이 둘을 설정"]):
    d.t(RX + RW // 2, BY + 76 + i * 30, ddx.fit(ln, 12, RW - 24, ln), 12, MUTED, KR)

MX = BX + BW
d.path(f"M {MX+16} {BY+BH//2} L {RX-18} {BY+BH//2}", MUTED, 1.6, m="ar")
for i, ln in enumerate(["디스커버리 · 로드밸런싱", "복원력 · 보안 · 관측", "라우팅 제어 · API"]):
    # 라벨은 화살표선(BY+104) 위로 16px 띄운다 — 닿으면 lint 가 text-line 으로 잡는다
    d.t((MX + RX) // 2, BY + 44 + i * 22, ddx.fit(ln, 11, RX - MX - 24, ln), 11, MUTED, KR)

FY = BY + BH + 32
d.tone(BX, FY, RX + RW - BX, 60, ACC, 6, "12", 1.4)
d.t(500, FY + 38, "컨트롤 플레인이 죽어도 사이드카는 받아 둔 설정으로 계속 돈다 — 운영 안정성의 근거", 13, ACC, KR)

d.t(36, FY + 108, "옮겼다고 공짜는 아니다 — Pod 마다 프록시가 하나씩 늘고, 그만큼 자원과 지연이 붙는다",
    12, MUTED, KR, "start")
d.legend(FY + 120, [("있던 자리", WARN), ("옮겨 간 자리", INFO), ("자리 이동이 만든 성질", ACC)])
d.save("05-03.mesh-relocation.svg")
print("ok mesh-relocation")
