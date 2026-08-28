# 12-01 §2 — 컨트롤러와 프록시는 별개다
# 본문이 "흔히 한 덩어리로 부르지만 둘은 별개 컴포넌트"라고 못박는다. 그러니 한 상자로
# 그리면 안 되고, 설정이 만들어지는 길과 트래픽이 지나는 길을 갈라 놓아야 한다.
# 타입 스펙: type-architecture.md — API 서버 · 컨트롤러 · 프록시 · 파드라는 컴포넌트 구성도. 두 밴드가 설정 경로와 트래픽 경로다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, KR, MONO
import ddx

d = D(1200, 668, "KUBERNETES IN ACTION · 12-01",
      "설정을 만드는 쪽과 트래픽을 나르는 쪽",
      "컨트롤러는 API 서버를 감시해 프록시 설정을 만들고, 프록시는 그 설정으로 HTTP 를 처리한다. "
      "둘을 한 덩어리로 부르는 습관이 이 분업을 가린다.",
      "11 장과 골격이 같다 — 선언 · 감시자 · 집행자")

ddx.band(d, 100, 314, "설정이 만들어지는 길 — 요청과 무관하게 돈다", x=24, w=1152)
ddx.node(d, 200, 216, "API 서버", "Ingress · Service · EndpointSlice", 260, 88, INFO)
ddx.node(d, 570, 216, "Ingress 컨트롤러", "감시한 것을 설정으로 옮긴다", 260, 88)
ddx.node(d, 940, 216, "nginx.conf", "server_name · location · upstream", 260, 88)
d.path("M 336 216 L 434 216", MUTED, 1.5, m="ar"); d.t(385, 202, "watch", 11, SOFT, MONO)
d.path("M 706 216 L 804 216", MUTED, 1.5, m="ar"); d.t(755, 202, "쓰고 reload", 11, SOFT, KR)

ddx.band(d, 338, 552, "트래픽이 지나는 길 — 요청마다 돈다", x=24, w=1152)
ddx.node(d, 200, 454, "클라이언트", "GET /quote", 260, 88)
ddx.node(d, 570, 454, "L7 프록시", "설정대로 파싱해 넘긴다", 260, 88, focal=True)
ddx.node(d, 940, 454, "파드", "10.244.1.10:80", 260, 88, OK)
d.path("M 336 454 L 434 454", MUTED, 1.5, m="ar")
d.path("M 706 454 L 804 454", OK, 1.5, m="ok"); d.t(755, 440, "upstream 으로", 11, OK, KR)

d.path("M 940 264 L 940 340 L 700 340 L 700 406", ACC, 1.4, m="acc", dash="6 5")
d.t(930, 330, "이 설정을 읽는 것이 아래의 프록시다", 11, ACC, KR, "end")

d.t(24, 596, "kube-proxy 는 Ingress 를 감시하지 않는다. 심을 수 있는 규칙이 '목적지 IP:port 가 X 면 Y 로' 뿐이라 "
             "'경로가 /quote 면'을 적을 자리가 없다.", 11, MUTED, KR, "start")
d.legend(620, [("선언된 것", INFO), ("트래픽을 나르는 자", ACC), ("목적지", OK)])
d.save("12-01-ingress-controller-role.svg")
print("ok")
