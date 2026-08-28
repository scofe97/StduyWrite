# 11-01 §3 — 누가 IP 를 만들고 누가 명단에 적는가
# 캡션이 '준비 단계와 실제 요청 경로' 둘을 요구한다. 띠 둘로 나누고, 준비 중 요청 때 실제로
# 쓰이는 둘만 대괄호로 묶어 아래 띠로 내린다. 세로로 1:1 정렬하지 않는다 — 대응이 아니다.
# 타입 스펙: type-data-flow.md — 단계마다 *누가* 무엇을 만드는지가 논지다 — 제목이 "누가 IP를 만들고 누가 명단에 적는가"다.
#           위 밴드에서 만들어진 것(IP·명단·규칙)이 아래 요청 경로에서 쓰인다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1080, 620, "KUBERNETES IN ACTION · 11-01",
      "누가 IP를 만들고 누가 명단에 적는가",
      "네 컴포넌트가 각각 한 가지만 맡는다. 스케줄러는 노드를, CNI는 IP를, EndpointSlice 컨트롤러는 명단을, "
      "kube-proxy는 길을 맡는다. 이 준비는 요청이 오기 전에 끝나 있고, 요청 때 실제로 도는 것은 커널의 변환뿐이다.",
      "IP를 실제로 만드는 것은 CNI 하나뿐")

# 준비 — 요청 전에 끝나 있다
ddx.band(d, 100, 316, "준비 — 요청이 오기 전에 끝나 있다", x=24, w=1032)
PREP = [("스케줄러", "노드를 정한다", "IP 에 관여하지 않음"),
        ("CNI 플러그인", "IP 를 만든다", "10.244.2.9 발급"),
        ("EndpointSlice 컨트롤러", "명단에 적는다", "ready 파드만"),
        ("kube-proxy", "길을 놓는다", "각 노드에 규칙 설치")]
BW, GP = 232, 24
X0 = (1080 - (4 * BW + 3 * GP)) // 2
CX = [X0 + BW // 2 + i * (BW + GP) for i in range(4)]
for cx, (t, s, g) in zip(CX, PREP):
    d.box(cx - BW // 2, 154, BW, 108, PAPER2, RULE, 1.1, 6)
    d.t(cx, 186, ddx.fit(t, 13, BW - 18, t), 13, INK, KR, "middle", 600)
    d.t(cx, 212, ddx.fit(s, 12, BW - 16, s), 12, MUTED, KR)
    d.t(cx, 240, ddx.fit(g, 10, BW - 14, g), 10, SOFT, KR)
for a, b in zip(CX, CX[1:]):
    d.path(f"M {a+BW//2+6} 208 L {b-BW//2-10} 208", MUTED, 1.3, m="ar")

# 이 둘만 요청 경로에 쓰인다
LX, RX = CX[2] - BW // 2, CX[3] + BW // 2
MIDX = (LX + RX) // 2
d.path(f"M {LX} 276 L {LX} 284 L {RX} 284 L {RX} 276", ACC, 1.2)
d.path(f"M {MIDX} 284 L {MIDX} 330 L 540 330 L 540 400", ACC, 1.5, m="acc", dash="5 5")
d.t(MIDX + 12, 306, "요청 때 실제로 쓰이는 준비는 이 둘", 11, ACC, KR, "start")

# 요청 — 그때 일어나는 일
ddx.band(d, 368, 548, "요청 — 그때 일어나는 일", x=24, w=1032)
ddx.node(d, 190, 452, "클라이언트 파드", "curl http://quote", 210, 76, INFO)
ddx.node(d, 540, 452, "노드 커널", "명단에서 하나 골라 DNAT", 260, 76, focal=True)
ddx.node(d, 890, 452, "파드", "10.244.2.9:80", 210, 76, INFO)
d.path("M 301 452 L 400 452", MUTED, 1.5, m="ar")
d.path("M 676 452 L 775 452", MUTED, 1.5, m="ar")
d.chip(350, 424, "dst 10.96.74.151", SOFT, 9)
d.chip(726, 424, "dst 10.244.2.9", SOFT, 9)
d.t(540, 522, "스케줄러·CNI 는 이 경로에 등장하지 않는다 — 이미 끝난 일이다", 11, SOFT, KR)

d.legend(568, [("준비의 산물", INFO), ("요청 때 도는 것", ACC)])
d.save("11-01-service-component-responsibilities.svg")
print("ok")
