# 04-01.nat-free-promise — 포트 제약에서 3가지 약속, 그리고 그 대가까지
# 본문 요구: "IP를 Pod마다 주는 동기는 포트 제약 제거 … 세 요구사항 … 대가는 명확합니다 —
#           Pod마다 IP를 할당하고 라우팅하는 일이 클러스터에 상당한 복잡성을 더합니다"
# 타입 스펙: type-architecture.md — 상자에 든 것은 컴포넌트가 아니라 제약 · 선택 · 약속 · 대가라는 논지의 마디다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import dd, ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, WARN, INFO, PAPER2, KR, MONO

W, H = 1000, 464
d = D(W, H, "IP-PER-POD · WHY AND AT WHAT COST",
      "포트 제약을 없앤 대가로 클러스터가 떠안은 것",
      "주소·포트·프로토콜 조합에 하나만 바인딩되므로 Pod 마다 IP 를 준다. 그 대신 할당과 라우팅이 클러스터 몫이 된다.",
      lead="NAT 를 없앤 것이 공짜가 아니라 자리를 옮긴 것이라는 게 이 절의 요지")

BY, BH, BW = 152, 168, 200
CX = [136, 384, 632, 880]
def box(cx, title, lines, c, focal=False):
    x = cx - BW // 2
    if focal:
        d.tone(x, BY, BW, BH, ACC, 6, "12", 1.4); tc = ACC
    else:
        d.box(x, BY, BW, BH, PAPER2, c, 1.1, 6); tc = c
    d.t(cx, BY + 34, ddx.fit(title, 13, BW - 20, title), 13, tc, KR, "middle", 600)
    for i, ln in enumerate(lines):
        d.t(cx, BY + 66 + i * 24, ddx.fit(ln, 11, BW - 16, ln), 11, MUTED, KR)

box(CX[0], "포트 제약", ["주소·포트·프로토콜", "조합에 프로그램 하나", "두 웹 서버가 80 을", "두고 다툰다"], WARN)
box(CX[1], "IP-per-Pod", ["Pod 마다 고유 IP", "포트 플래그·DNAT·", "리버스 프록시 없이", "그냥 각자 쓴다"], INFO)
box(CX[2], "NAT 없음 3가지 약속", ["컨테이너끼리", "노드 ↔ 컨테이너", "안에서 본 자기 IP =", "밖에서 본 그 IP"], INFO)
box(CX[3], "떠안은 복잡성", ["Pod 마다 IP 할당", "그 IP 를 라우팅", "클러스터의 몫이 된다"], ACC, focal=True)

for i, lab in enumerate(["없애려고", "약속으로", "대가로"]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.path(f"M {a+8} {BY+84} L {b-10} {BY+84}", MUTED, 1.5, m="ar")
    d.t((a + b) // 2, BY + 72, lab, 11, MUTED, KR)

d.t(36, 372, "Borg 는 포트를 공유하는 쪽을 골랐고 Kubernetes 는 IP 를 나눠 주는 쪽을 골랐다 — 편의를 사고 복잡성을 지불한 거래다",
    12, MUTED, KR, "start")
d.legend(384, [("없애려던 제약", WARN), ("선택과 약속", INFO), ("지불한 값", ACC)])
d.save("04-01.nat-free-promise.svg")
print("ok nat-free-promise")
