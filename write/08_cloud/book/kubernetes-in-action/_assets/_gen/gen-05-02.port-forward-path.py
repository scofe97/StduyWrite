# 05-02 §방법 ③ — 속의 긴 경로
# 본문: "curl 프로세스가 프록시에 연결하고, 프록시가 API 서버에, API 서버가 Pod 를 호스팅하는
#        노드의 Kubelet 에, Kubelet 이 Pod 의 loopback 장치(localhost)를 통해 컨테이너에
#        연결합니다." / "통신이 여러 컴포넌트를 거치므로 경로 어딘가가 깨지면 Pod 자체는
#        정상이어도 통신이 안 될 수 있습니다."
# 타입 스펙: type-architecture.md — 다섯 칸 한 줄 사슬. 코리도어가 24px 뿐이라 문장 라벨이 안 들어가므로 번호 칩만
#           얹고 설명은 아래 산문이 맡는다 — 05-02 의 다른 장들과 같은 규약.
#           curl → 프록시 → API 서버 → kubelet → 컨테이너 다섯 칸을 지나는 경로도다.
#           지나가는 것이 주체의 동작이 아니라 구성 요소라 process 가 아니라 architecture 다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO
import ddx

W, H = 1000, 540
d = D(W, H, "KUBERNETES IN ACTION · 05-02",
      "속에서는 네 홉을 거친다 — 어느 하나가 깨져도 안 된다",
      "curl 이 프록시에, 프록시가 API 서버에, API 서버가 kubelet 에, kubelet 이 Pod 의 "
      "loopback 을 통해 컨테이너에 붙는다. Pod 가 멀쩡해도 경로 어딘가가 깨지면 통신이 막힌다.",
      lead="마지막 홉이 Pod 자신의 lo 라서 Client IP 가 127.0.0.1 이 된다")

ddx.band(d, 104, 484, "애플리케이션이 lo 에 바인딩돼 있어야 kubelet 이 도달한다 — eth0 만 듣고 있으면 닿지 않는다")

CX = ddx.stage_chain(
    d, cy=300, stage_y=204, bw=164, gap=28, x0=34, sizes=(12, 10, 9),
    stages=["내 컴퓨터", "로컬 프록시", "Control Plane", "워커 노드", "Pod"],
    nodes=[("curl", "요청을 낸다", "원래 요청자", INFO),
           ("port-forward", "127.0.0.1:8080", "로컬에 선다", None),
           ("API 서버", "인증·중계", "", None),
           ("kubelet", "노드 에이전트", "", None),
           ("컨테이너", "lo 127.0.0.1", "여기로 붙는다", ACC)],
    edges=["", "", "", ""])
for i, num in enumerate("①②③④"):
    d.chip((CX[i] + CX[i + 1]) // 2, 300, num, MUTED, 11)

d.t(36, 412, "① curl → 프록시   ② 프록시 → API 서버   ③ API 서버 → kubelet   "
             "④ kubelet → Pod 의 loopback", 12, MUTED, KR, "start")
d.t(36, 436, "홉이 넷이라 실패 지점도 넷이다 — port-forward 가 안 될 때 Pod 만 보면 원인을 못 찾는다.",
     12, MUTED, KR, "start")
d.legend(500, [("원래 요청자", INFO), ("마지막으로 붙는 자리", ACC)])
d.save("05-02-port-forward-path.svg")
print("ok port-forward-path")
