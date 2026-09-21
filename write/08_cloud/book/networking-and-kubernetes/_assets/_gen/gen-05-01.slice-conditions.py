# 05-01.slice-conditions — 서비스의 조건이 주소와 상태로 내려온다
# 본문 요구: Service 는 selector 라는 *조건*만 적고, 그 조건에 맞는 Pod 의 주소와 상태가
#           EndpointSlice 의 endpoints[].addresses · endpoints[].conditions.ready 로 나타난다.
#           ready 는 readiness probe 하나의 결과가 아니라 "serving 이면서 terminating 이 아님"의
#           줄임이다. 근거: K8s EndpointSlices — "The ready condition is essentially a shortcut
#           for checking serving and not terminating."
# 타입 스펙: type-flowchart.md — 조건 하나가 주소 목록과 두 갈래 상태로 내려가는 분기가 요점이라
#           갈림을 형태로 둔다. 같은 편의 tree · process · dp-security-matrix 와 겹치지 않는다.
# 좌표: 분기 y=232(ready) · y=372(ready=false). 띠(104~440) 아래 y=460 에 조회 명령을 얹는다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 612
d = D(W, H, "SERVICE CONDITION · ADDRESSES AND STATE",
      "서비스의 조건이 실제 대상 주소와 상태로 내려온다",
      "Service 에 적는 것은 selector 라는 조건뿐이고, 그 조건에 맞는 Pod 의 주소와 상태는 "
      "EndpointSlice 에 적힌다. 트래픽이 가는 곳은 ready 인 endpoint 다.",
      lead="Service = 조건 · EndpointSlice = 지금 그 조건에 맞는 주소와 상태")
ddx.band(d, 104, 440, "selector → Pod label → 주소 · 조건")

def box(cx, cy, w, h, t1, t2, t3, c=None):
    x, y = cx - w // 2, cy - h // 2
    d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 16, ddx.fit(t1, 13, w - 18, t1), 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 6, ddx.fit(t2, 12, w - 16, t2), 12, MUTED,
        MONO if all(ord(ch) < 128 or ch in '.·-[]… ' for ch in t2) else KR)
    if t3: d.t(cx, cy + 28, ddx.fit(t3, 12, w - 14, t3), 12, SOFT, KR)

box(132, 300, 196, 100, "Service", "spec.selector", "조건만 적는다")
box(468, 300, 248, 100, "EndpointSlice", "endpoints[].addresses", "조건에 맞는 Pod 주소")
d.path("M 230 300 L 340 300", ACC, 1.5, m="ar")
d.t(285, 284, "label 일치", 12, MUTED, KR)

box(832, 232, 280, 88, "conditions.ready · true", "트래픽 수신", None, OK)
box(832, 372, 280, 88, "conditions.ready · false", "대상에서 제외 · Pod 는 실행 중", None, BAD)
d.path("M 592 276 L 640 276 L 640 232 L 688 232", OK, 1.5, m="ok")
d.path("M 592 324 L 640 324 L 640 372 L 688 372", BAD, 1.5, m="bad")

# 조회 · 진단 순서
d.box(32, 460, 936, 84, PAPER, RULE, 0.9, 8)
d.t(52, 486, "kubectl get endpointslice -l kubernetes.io/service-name=<서비스명> -o yaml", 12, ACC, MONO, "start", 600)
d.t(52, 512, "주소가 없다 · selector 와 Pod label 대조", 12, MUTED, KR, "start")
d.t(520, 512, "ready=false · readiness 실패 또는 종료 중 확인", 12, MUTED, KR, "start")
d.legend(564, [("대상에 오름", OK), ("대상에서 빠짐", BAD), ("조건을 적는 자리", ACC)])
d.save("05-01.slice-conditions.svg"); print("ok slice-conditions")
