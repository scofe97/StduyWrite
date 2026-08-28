# 17-02 §3 — hostNetwork 파드가 받는 경로
# 앞 도식과 같은 골격에서 무엇이 사라졌는지가 요점이다. DNAT 도 veth 도 없고, 대신 노드 포트를
# 점유해 두 번째 레플리카와 충돌한다는 결과가 따라 나온다.
# 타입 스펙: type-architecture.md — 노드 netns 가 경계 상자이고 그 안에서 패킷이 왼쪽에서 오른쪽으로 간다. 짝 도식과 같은
#           골격이라 사라진 구성 요소(DNAT · veth)가 대비로 읽힌다.
#           type-data-flow 는 역할 레인 1~4 × 단계 열 × 타입 있는 페이로드 칩이 입력 계약인
#           데이터 플랫폼 전용 타입이라 여기엔 맞지 않는다. type-architecture 의 Best for 에
#           "data-flow diagrams" 가 그대로 들어 있다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, INFO, OK, WARN, BAD, MUTED, SOFT, INK, PAPER, PAPER2, RULE, KR, MONO
import ddx

d = D(1220, 656, "KUBERNETES IN ACTION · 17-02",
      "hostNetwork 파드 — 변환도 건널목도 없다",
      "파드가 노드의 네트워크 네임스페이스를 그대로 쓴다. 자기 IP 가 없어 DNAT 할 것도 없고 건널 veth 도 "
      "없다. 대신 그 포트를 노드에서 점유한다.",
      "FORWARD 가 아니라 INPUT 으로 올라간다")

d.box(60, 176, 1100, 220, PAPER, RULE, 0.9, 8)
d.t(610, 204, "노드 netns — 파드가 이 안에 있다", 11, SOFT, KR)
ddx.node(d, 200, 300, "노드 IP:8080", "패킷이 들어온다", 240, 76, INFO)
ddx.node(d, 640, 300, "에이전트 프로세스", "노드 소켓에 바로 닿는다", 280, 76, ACC)
d.path("M 322 300 L 498 300", ACC, 1.6, m="acc")
d.t(410, 280, "변환 없음 · veth 없음", 10, ACC, KR)
d.t(940, 292, "파드가 자기 IP 를", 11, SOFT, KR)
d.t(940, 314, "갖지 않는다", 11, SOFT, KR)

d.box(60, 424, 1100, 116, PAPER2, BAD, 1.1, 8)
d.t(610, 452, "그래서 생기는 일 — 노드 포트를 점유한다", 12, BAD, KR, "middle", 600)
d.t(340, 486, "레플리카 1  포트 8080 잡음", 11, OK, MONO)
d.t(880, 486, "레플리카 2  같은 포트 → 충돌", 11, BAD, MONO)
d.t(610, 514, "한 노드에 둘을 둘 수 없다 — DaemonSet 이 자연스러운 짝인 이유다", 11, MUTED, KR)

d.t(24, 584, "이름 해석도 노드 쪽을 따라간다. dnsPolicy 를 ClusterFirstWithHostNet 으로 두지 않으면 "
             "클러스터 DNS 가 아니라 노드의 resolv.conf 를 쓴다.", 11, MUTED, KR, "start")
d.legend(608, [("들어오는 자리", INFO), ("직접 닿는다", ACC), ("충돌하는 자리", BAD)])
d.save("17-02-hostnetwork-node.svg")
print("ok")
