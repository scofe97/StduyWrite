# 04-01.pod-creation-flow — 스케줄러는 이름만 적고 네트워크는 런타임이 CNI 를 불러 만든다
# 본문 요구: 세 구간 — 스케줄러가 이름만 / kubelet 이 자기 몫 발견 / 런타임이 샌드박스와 네트워크(CNI ADD)를 만든 뒤 컨테이너 시작
# 타입 스펙: type-sequence.md — 실제로 만드는 쪽이 누구인지가 요점이라
#           만드는 구간에만 focal 을 건다. 참여자는 다섯(상한)이다.
#           2026-11-08 CNI 를 부르는 쪽을 kubelet 에서 컨테이너 런타임으로 바로잡았다 —
#           kubelet 은 CRI 로 RunPodSandbox 만 부르고, 런타임(containerd)이 CNI 플러그인을 부른다.
import dd, ddx
from dd import D, Seq, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 704
d = Seq(W, H, "POD CREATION · WHO ACTUALLY BUILDS IT",
        "스케줄러는 이름만 적고, 네트워크는 런타임이 CNI 를 불러 만든다",
        "스케줄러가 하는 일은 nodeName 한 줄을 적는 것뿐이다. 그 노드의 kubelet 이 CRI 로 샌드박스를 요청하면 컨테이너 런타임이 CNI 플러그인을 불러 네트워크를 만든 뒤 컨테이너를 시작한다.",
        lead="스케줄러가 하는 일은 nodeName 한 줄 · 네트워크를 만드는 일은 런타임이 CNI 를 불러서")

LX = ddx.lanes(d, [("API 서버", "상태 보관"), ("스케줄러", "노드 이름 기록"),
                   ("kubelet", "노드의 관리자"), ("컨테이너 런타임", "CRI 를 받는 쪽"),
                   ("CNI 플러그인", "주소와 경로")], y0=104, lane_w=172)
API, SCH, KUB, RT, CNI = (int(LX[k]) for k in ("API 서버", "스케줄러", "kubelet", "컨테이너 런타임", "CNI 플러그인"))
SEGS = [(164, 284, "1 · 스케줄러 · 노드 이름만 기록", False),
        (296, 360, "2 · kubelet · 자기 몫 발견", False),
        (372, 604, "3 · 런타임 · 샌드박스와 CNI 가 먼저, 컨테이너는 그다음", True)]
Y_END = 612
for a, b, lab, f in SEGS: ddx.band(d, a, b, lab, focal=f)
d.rails(Y_END)

def msg(a, b, y, label, c, mk, dash=None, sub=None):
    dirn = 1 if b > a else -1
    d.path(f"M {a+10*dirn} {y} L {b-12*dirn} {y}", c, 1.5, m=mk, dash=dash)
    d.t((a + b) // 2, y - 12, label, 11, c, KR, "middle", 600)
    if sub: d.t((a + b) // 2, y + 18, sub, 11, MUTED, KR)

msg(API, SCH, 224, "노드 미정 Pod", INFO, "info")
msg(SCH, API, 264, "nodeName = node-1", MUTED, "ar", "6 5")
msg(API, KUB, 340, "node-1 에 할당됨", INFO, "info")
msg(KUB, RT, 428, "RunPodSandbox", ACC, "acc")
msg(RT, CNI, 468, "ADD — netns·주소 요청", ACC, "acc")
msg(CNI, RT, 508, "IP·경로 완료", MUTED, "ar", "6 5")
msg(RT, KUB, 548, "샌드박스 준비 · PodReadyToStartContainers = True", MUTED, "ar", "6 5")
msg(KUB, RT, 588, "이미지 받기 · 컨테이너 시작", ACC, "acc")

d.legend(Y_END + 24, [("API 흐름", INFO), ("실제로 만드는 구간", ACC)])
d.save("04-01.pod-creation-flow.svg")
print("ok pod-creation-flow")
