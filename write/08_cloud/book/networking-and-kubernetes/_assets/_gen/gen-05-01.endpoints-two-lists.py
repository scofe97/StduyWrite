# 05-01.endpoints-two-lists — readiness 의 결과가 두 목록으로 갈린다
# 본문 요구: "readiness 검사를 통과한 주소는 `.addresses` 에, 통과하지 못한 주소는
#           `.notReadyAddresses` 에 오릅니다. 앞 장 Probe 에서 본 'readiness 실패 → 트래픽 제외'의
#           실체가 바로 이 두 목록입니다." 그리고 라벨 실험에서 "두 컨트롤러가 동시에 반응합니다 —
#           endpoints 컨트롤러는 Endpoints 에서 빼고, ReplicaSet 컨트롤러는 새 Pod 를 만듭니다."
# 타입 스펙: type-flowchart.md — 한 검사의 통과·실패가 서로 다른 자리로 갈리는 분기가 요점이라
#           갈림을 형태로 둔다. 같은 편의 tree · process · dp-security-matrix 와 겹치지 않는다.
# 좌표: 분기 y=236(통과) · y=372(실패). 띠(104~440) 아래 y=456 에 라벨 제거 실험을 따로 얹는다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 630
d = D(W, H, "ENDPOINTS · ONE PROBE, TWO LISTS",
      "readiness 의 결과가 두 목록으로 갈린다",
      "Pod 마다 도는 readiness 검사의 통과·실패가 Endpoints 객체의 두 주소 목록으로 나뉜다. "
      "서비스가 트래픽을 보내는 곳은 ready 목록뿐이고, 실패한 주소는 살아 있는 채로 빠진다.",
      lead="통과하면 .addresses · 실패하면 .notReadyAddresses — 트래픽은 앞쪽에만 간다")
ddx.band(d, 104, 440, "서비스는 조건을 적을 뿐이고, 지금 누가 받고 있는지는 이 객체에 적힌다")

def box(cx, cy, w, h, t1, t2, t3, c=None):
    x, y = cx - w // 2, cy - h // 2
    d.box(x, y, w, h, PAPER2, c or RULE, 1.1, 6)
    d.t(cx, cy - 16, ddx.fit(t1, 13, w - 18, t1), 13, c or INK, KR, "middle", 600)
    d.t(cx, cy + 6, ddx.fit(t2, 11, w - 16, t2), 11, MUTED,
        MONO if all(ord(ch) < 128 or ch in '.·- ' for ch in t2) else KR)
    if t3: d.t(cx, cy + 28, ddx.fit(t3, 11, w - 14, t3), 11, SOFT, KR)

box(136, 300, 196, 100, "readiness 검사", "Pod 마다 돈다", "앞 장 Probe 의 결과")
box(486, 236, 260, 92, ".addresses", "통과한 주소", "ready 목록", OK)
box(486, 372, 260, 92, ".notReadyAddresses", "통과 못 한 주소", "notReady 목록", BAD)
box(830, 236, 220, 92, "트래픽이 온다", "서비스가 여기로만", None, OK)
box(830, 372, 220, 92, "트래픽에서 빠진다", "Pod 는 살아 있다", None, BAD)

d.path("M 236 276 L 300 276 L 300 236 L 354 236", OK, 1.5, m="ok")
d.path("M 236 324 L 300 324 L 300 372 L 354 372", BAD, 1.5, m="bad")
d.t(300, 220, "통과", 11, OK, KR)
d.t(300, 402, "실패", 11, BAD, KR)
d.path("M 618 236 L 718 236", OK, 1.5, m="ok")
d.path("M 618 372 L 718 372", BAD, 1.5, m="bad")

# 라벨 제거 실험 — 두 컨트롤러가 동시에 반응한다
d.box(32, 456, 936, 88, PAPER, RULE, 0.9, 8)
d.t(52, 482, "라벨을 떼면 (kubectl label pod … app=nope --overwrite)", 12, ACC, KR, "start", 600)
d.t(52, 508, "endpoints 컨트롤러 — 그 주소를 목록에서 뺀다", 11, MUTED, KR, "start")
d.t(520, 508, "ReplicaSet 컨트롤러 — 부족해진 만큼 새 Pod 를 만든다", 11, MUTED, KR, "start")
d.t(36, 574, "그래서 문제 Pod 는 트래픽에서 빠진 채 살아 있다 — 서비스는 멀쩡히 두고 그 하나만 붙잡아 조사한다",
    12, MUTED, KR, "start")
d.legend(588, [("트래픽이 가는 목록", OK), ("빠지는 목록", BAD), ("떼어 내는 손잡이", ACC)])
d.save("05-01.endpoints-two-lists.svg"); print("ok endpoints-two-lists")
