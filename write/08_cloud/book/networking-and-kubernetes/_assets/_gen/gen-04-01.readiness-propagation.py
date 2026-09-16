# 04-01.readiness-propagation — 프로브 실패가 네 주체를 거쳐 다른 노드의 규칙을 바꾼다
# 본문 요구: "Kubelet 이 Ready: False 를 쓰고 … EndpointSlice 컨트롤러가 명단에서 제외 … 각 노드의 kube-proxy 가
#           그 Pod 줄을 빼고 확률을 다시 계산 … 그 Pod 를 아무도 건드리지 않습니다"
# 타입 스펙: type-process — 주체 넷이 상태 한 조각을 넘겨가며 순서대로 처리한다. 아래 두 칸은
#           그 흐름의 결과가 어디에 남고 어디에 안 남는지를 대조한다.
#           손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 456
d = D(W, H, "READINESS · HOW A FAILED PROBE REACHES THE RULES",
      "readiness 실패는 그 Pod 가 아니라 남의 노드 규칙을 바꾼다",
      "Kubelet 의 프로브 실패가 API 서버와 EndpointSlice 컨트롤러를 거쳐 각 노드 kube-proxy 의 규칙 재작성으로 "
      "이어지며, 그 Pod 자신의 네트워크는 어느 단계에서도 바뀌지 않는다.",
      lead="네 주체를 거쳐 내려가지만 그 Pod 의 네트워크는 어느 단계에서도 그대로")

BW, BH, STRIDE, X0 = 208, 80, 248, 24
BY = 136
CX = [X0 + BW // 2 + i * STRIDE for i in range(4)]        # 128 376 624 872
ACTORS = ["Kubelet · 그 노드", "API 서버", "EndpointSlice 컨트롤러", "kube-proxy · 모든 노드"]
STEPS = [("프로브 3회 연속 실패", "failureThreshold: 3", INFO),
         ("Pod 상태 기록", "Ready: False", None),
         ("명단에서 제외 표시", "ready: false", None),
         ("서비스 체인 재작성", "그 Pod 줄 삭제", ACC)]

for i, (cx, actor, (t, s, c)) in enumerate(zip(CX, ACTORS, STEPS)):
    d.t(cx, BY - 16, actor, 12, SOFT, KR, "middle", 600)
    x = cx - BW // 2
    if c is ACC:
        d.tone(x, BY, BW, BH, ACC, 6, "12", 1.4); tc = ACC
    else:
        d.box(x, BY, BW, BH, PAPER2, c or RULE, 1.1, 6); tc = INK
    d.t(x + 14, BY + 22, str(i + 1), 12, tc if c else SOFT, MONO, "start", 600)
    d.t(cx, BY + 36, ddx.fit(t, 13, BW - 24, t), 13, tc, KR, "middle", 600)
    mono = all(ord(ch) < 128 for ch in s)
    d.t(cx, BY + 60, s, 12, MUTED, MONO if mono else KR)

for i, lab in enumerate(["write", "watch", "watch"]):
    a, b = CX[i] + BW // 2, CX[i + 1] - BW // 2
    d.arrow([(a + 4, BY + BH // 2), (b - 8, BY + BH // 2)], MUTED, "ar", 1.5)
    d.t((a + b) // 2, BY + BH + 20, lab, 12, SOFT, MONO)

RY, RH, RW = 264, 104, 464
d.box(24, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(48, RY + 32, "그대로인 곳 · 그 Pod", 14, INK, KR, "start", 600)
d.t(48, RY + 60, "라우팅 · 인터페이스 변화 없음", 12, MUTED, KR, "start")
d.t(48, RY + 84, "커넥션 풀 초기화 계속", 12, MUTED, KR, "start")

d.box(512, RY, RW, RH, PAPER2, RULE, 1.1, 8)
d.t(536, RY + 32, "바뀌는 곳 · 다른 노드의 규칙", 14, INK, KR, "start", 600)
d.t(536, RY + 60, "그 Pod 를 가리키던 줄 삭제", 12, MUTED, KR, "start")
d.t(536, RY + 84, "남은 줄의 확률 재계산", 12, MUTED, KR, "start")

d.legend(408, [("상태가 전파되는 단계", INFO), ("규칙이 실제로 바뀌는 자리", ACC)])
d.save("04-01.readiness-propagation.svg")
print("ok readiness-propagation")
