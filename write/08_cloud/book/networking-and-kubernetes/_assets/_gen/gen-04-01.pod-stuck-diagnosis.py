# 04-01.pod-stuck-diagnosis — NODE 칸 하나가 스케줄러와 kubelet 을 가른다
# 본문 요구: "Pending 인데 NODE 가 <none> 이면 스케줄러가 못 정한 것이고 CNI 가 없어 노드가 NotReady 인 경우도 여기 든다 /
#           NODE 가 정해졌는데 ContainerCreating 이면 kubelet 쪽이고 이벤트에 failed to setup network for sandbox 가 남는다"
# 타입 스펙: type-flowchart.md — 질문 둘로 갈리는 판정 흐름이라 순서도로 그린다. 가장 많은 것을 가르는 첫 질문에만 focal 을 건다.
#           값은 kind v1.37.0 실측(2026-11-08)에서 가져왔다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 548
d = D(W, H, "STUCK POD · WHICH SIDE TO LOOK AT",
      "NODE 칸이 정해졌는지가 스케줄러 쪽과 kubelet 쪽을 가른다",
      "kubectl get pod -o wide 의 NODE 가 none 이면 스케줄러가 노드를 못 정한 것이고, 노드가 정해졌는데 ContainerCreating 이면 그 노드의 kubelet 쪽에서 멈춘 것이다.",
      lead="CNI 가 없을 때는 노드가 NotReady 가 되어 앞쪽(스케줄러)에서 멈춘다")


def oval(cx, cy, w, h, txt):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, RULE, 1.1, h // 2)
    d.t(cx, cy + 4, txt, 12, INK, KR, "middle", 600)


def diamond(cx, cy, w, h, l1, l2, focal=False):
    pts = f"M {cx} {cy-h//2} L {cx+w//2} {cy} L {cx} {cy+h//2} L {cx-w//2} {cy} Z"
    if focal:
        d.o.append(f'<path d="{pts}" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>'); tc = ACC
    else:
        d.o.append(f'<path d="{pts}" fill="{PAPER2}" stroke="{RULE}" stroke-width="1.1"/>'); tc = INK
    d.t(cx, cy - 4, l1, 12, tc, KR, "middle", 600)
    d.t(cx, cy + 14, l2, 12, tc, KR, "middle", 600)


def rect(cx, cy, w, h, l1, l2, c, mono2=False):
    d.box(cx - w // 2, cy - h // 2, w, h, PAPER2, c, 1.1, 6)
    d.t(cx, cy - 4, ddx.fit(l1, 12, w - 16, l1), 12, c, KR, "middle", 600)
    d.t(cx, cy + 14, ddx.fit(l2, 11, w - 16, l2), 11, MUTED, MONO if mono2 else KR)


oval(260, 132, 200, 36, "Pod 가 안 뜬다")
d.arrow([(260, 150), (260, 186)], MUTED, "ar", 1.4)
diamond(260, 236, 220, 96, "NODE 칸이", "<none> 인가?", focal=True)

# 예 — 스케줄러 쪽
d.arrow([(370, 236), (490, 236)], MUTED, "ar", 1.4); d.t(430, 226, "예", 11, MUTED, KR)
rect(640, 236, 300, 56, "Pending · 스케줄러가 노드를 못 정함", "FailedScheduling", INFO, True)
d.arrow([(640, 264), (640, 302)], MUTED, "ar", 1.4)
diamond(640, 350, 240, 96, "untolerated taint 가", "not-ready 인가?")
d.arrow([(760, 350), (780, 350)], MUTED, "ar", 1.4); d.t(770, 340, "예", 11, MUTED, KR)
rect(880, 350, 200, 56, "노드가 NotReady", "흔한 원인 · CNI 부재", INFO)
d.arrow([(640, 398), (640, 428)], MUTED, "ar", 1.4); d.t(652, 418, "아니오", 11, MUTED, KR, "start")
rect(640, 452, 300, 48, "자원 부족 · affinity · PVC 확인", "describe pod 이벤트", INFO)

# 아니오 — kubelet 쪽
d.arrow([(260, 284), (260, 312)], MUTED, "ar", 1.4); d.t(272, 302, "아니오", 11, MUTED, KR, "start")
rect(260, 340, 300, 56, "ContainerCreating · kubelet 쪽에서 멈춤", "NODE 가 정해진 뒤", OK)
d.arrow([(260, 368), (260, 428)], MUTED, "ar", 1.4)
rect(260, 452, 300, 48, "CNI 가 주소를 못 줌 · 이미지·볼륨도 확인", "failed to setup network for sandbox", OK, True)

d.legend(492, [("스케줄러 쪽", INFO), ("kubelet 쪽", OK), ("가르는 첫 질문", ACC)])
d.save("04-01.pod-stuck-diagnosis.svg")
print("ok pod-stuck-diagnosis")
