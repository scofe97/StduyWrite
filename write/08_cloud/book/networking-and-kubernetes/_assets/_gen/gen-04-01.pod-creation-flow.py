# 04-01.pod-creation-flow — 스케줄러는 이름만 적는다
# 본문 요구: 세 구간 — 스케줄러가 이름만 / Kubelet 이 자기 몫 발견 / CRI·CNI 로 실제 생성
# 타입 스펙: type-sequence.md — 실제로 만드는 쪽이 누구인지가 요점이라
#           만드는 구간에만 focal 을 건다.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 672
d = Seq(W, H, "POD CREATION · WHO ACTUALLY BUILDS IT",
        "스케줄러는 이름만 적고, 만드는 일은 그 노드의 Kubelet 이 한다",
        "스케줄러가 하는 일은 nodeName 한 줄을 적는 것뿐이다. 컨테이너와 네트워크는 그 노드의 Kubelet 이 CRI 와 CNI 를 불러 만든다.",
        lead="스케줄러가 하는 일은 nodeName 한 줄 · 만드는 일은 그 노드의 Kubelet")

LX = ddx.lanes(d, [("API 서버", "상태를 쥔다"), ("스케줄러", "이름만 적는다"),
                   ("kubelet", "실제로 만든다"), ("CNI", "주소와 경로")], y0=104, lane_w=196)
API, SCH, KUB, CNI = (int(LX[k]) for k in ("API 서버", "스케줄러", "kubelet", "CNI"))
SEGS = [(164, 292, "1 스케줄러는 노드 이름만 적는다", False),
        (308, 396, "2 Kubelet 이 자기 몫을 발견한다", False),
        (412, 556, "3 CRI 로 컨테이너, CNI 로 네트워크", True)]
Y_END = 576
for a, b, lab, f in SEGS: ddx.band(d, a, b, lab, focal=f)
d.rails(Y_END)

def msg(a, b, y, label, c, mk, dash=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    d.t((a + b) // 2, y - 12, label, 11, c, KR, "middle", 600)

msg(API, SCH, 226, "노드 미정 Pod", INFO, "info")
msg(SCH, API, 268, "nodeName = node-1", MUTED, "ar", "6 5")
msg(API, KUB, 356, "node-1 에 할당됨", INFO, "info")
msg(KUB, CNI, 470, "ADD — netns·주소 요청", ACC, "acc")
msg(CNI, KUB, 520, "IP·경로 완료", MUTED, "ar", "6 5")

d.t(36, 606, "스케줄러는 Pod 를 만들지 않는다 — 어느 노드인지만 적고, 그 뒤는 그 노드가 스스로 한다",
     12, MUTED, KR, "start")
d.legend(Y_END + 54, [("API 흐름", INFO), ("실제로 만드는 구간", ACC)])
d.save("04-01.pod-creation-flow.svg")
print("ok pod-creation-flow")
