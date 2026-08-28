# 11-01 §7 — 이름이 주소가 되고, 주소가 다시 주소가 된다
# 값이 두 번 바뀌는 사슬이라 stage_chain. 변환의 성격이 다르다는 게 요점이므로
# 화살표 아래에 '누가 바꾸는지'를 따로 적었다. 가운데 가상 주소가 focal.
# 타입 스펙: type-architecture.md — 상자에 든 것은 컴포넌트가 아니라 목적지 주소이고, 그것을 바꾸는 주체는 단계 머리에 있다.
#           38개 메뉴에 이 형태(주체 레인 없는 값·단계 사슬)를 담을 타입이 없다 —
#           layout 문법만 architecture 를 따르고 그 사실을 여기 적어 둔다.
#           2026-08-29 정정: type-data-flow 로 적었으나 그 정본은 역할 레인 1~4 × 단계 열 ×
#           타입 있는 페이로드 칩이 입력 계약인 데이터 플랫폼 전용 타입이다. 이 그림에 레인은 없다.
#           type-architecture 의 Best for 에 "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, MUTED, SOFT, KR, MONO
import ddx

d = D(1060, 424, "KUBERNETES IN ACTION · 11-01",
      "이름이 주소가 되고, 주소가 다시 주소가 된다",
      "quiz 한 단어가 실제 파드에 닿기까지 성격이 다른 변환을 두 번 거친다. 앞은 이름을 주소로 바꾸는 해석이고, "
      "뒤는 주소를 다른 주소로 바꾸는 변환이다. 가운데 값은 어느 인터페이스에도 붙어 있지 않다.",
      "curl http://quiz 한 줄이 지나는 두 단계")

CX = ddx.stage_chain(
    d, cy=250,
    stages=["애플리케이션이 쓴 것", "DNS 가 답한 것", "커널이 바꾼 것"],
    nodes=[
        ("quiz", "Service 이름", "점이 없는 짧은 이름", None),
        ("10.96.136.190", "ClusterIP", "어느 인터페이스에도 없다", ACC),
        ("10.244.2.9", "파드 IP", "실제 인터페이스", None),
    ],
    edges=["이름 해석", "주소 변환"],
    bw=190, gap=210, x0=30)

for a, b, who in ((CX[0], CX[1], "CoreDNS 가 A 레코드로 답한다"),
                  (CX[1], CX[2], "노드 커널이 목적지를 바꾼다")):
    d.t((a + b) // 2, 272, ddx.fit(who, 11, 206, who), 11, SOFT, KR)

d.t(24, 350, "DNS 응답은 파드 IP 가 아니다. resolver 의 일은 ClusterIP 를 돌려주는 데서 끝나고, "
             "거기서부터는 Service 데이터패스가 목적지를 실제 파드로 바꾼다.", 11, MUTED, KR, "start")
d.legend(376, [("붙지 않은 가상 주소", ACC)])
d.save("11-01-dns-dnat-two-stage.svg")
print("ok")
