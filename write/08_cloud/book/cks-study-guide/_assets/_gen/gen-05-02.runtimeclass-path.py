# 05-02 §2 — 파드의 runtimeClassName 이 RuntimeClass 의 handler 를 거쳐 containerd 의 runsc 런타임으로 이어진다.
# 본문 근거: 이 노트 ### 2 「2. 런타임 샌드박스로 커널 나누기」.
# 검증 근거: kind v1.35.0 에서 RuntimeClass(handler: runsc)와 runtimeClassName 을 쓴 파드 매니페스트가 서버 dry-run 을 통과.
#            runsc 가 설정되지 않은 노드에서는 파드가 FailedCreatePodSandBox 이벤트
#            (no runtime for "runsc" is configured)로 멈추는 것을 확인. gVisor 자체는 이 기기에서 돌리지 못해 공식 문서로 대조.
# 공식 근거: kubernetes.io 「Runtime Class」, gvisor.dev 「Containerd Quick Start」.
# 타입 스펙: type-swimlane — API 오브젝트 레인과 워커 노드 레인, 노드 레인 끝에 격리 경계.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 424
d = D(W, H, "CKS STUDY GUIDE · 05-02 §2",
      "파드에서 gVisor 샌드박스까지",
      "파드의 runtimeClassName 이 RuntimeClass 의 handler 를 가리키고, 그 이름이 워커 노드 containerd 설정의 runsc 런타임을 거쳐 "
      "gVisor 가 컨테이너를 실행하며, 컨테이너와 호스트 커널 사이에 gVisor 가 놓이는 흐름을 두 레인으로 그린 도식이다.",
      "파드는 이름만 적고, 이름이 가리키는 런타임은 노드에 먼저 설정돼 있어야 합니다")

BW, BH, PITCH, X0 = 190, 76, 212, 24
LANE_X, LANE_W, LANE_H = 12, 856, 120
API_Y, NODE_Y = 96, 240


def col(i):
    return X0 + i * PITCH


def lane(y, name, c=SOFT):
    d.o.append(f'<rect x="{LANE_X}" y="{y}" width="{LANE_W}" height="{LANE_H}" rx="8" fill="{c}0A" stroke="{c}" stroke-width="0.9"/>')
    d.t(LANE_X + 12, y + 20, name, 12, MUTED, KR, "start", 600)


def box(i, y, title, sub, c, mono=True):
    x, by = col(i), y + 34
    d.tone(x, by, BW, BH, c, 6, "14", 1.4 if c == ACC else 1.1)
    d.t(x + BW / 2, by + 32, title, 13, INK, KR, "middle", 600)
    d.t(x + BW / 2, by + 56, sub, 11, MUTED, MONO if mono else KR)


def right(i, y, c=MUTED, mk="ar", sw=1.4):
    my = y + 34 + BH / 2
    d.path(f"M {col(i) + BW + 2} {my} L {col(i + 1) - 2} {my}", c, sw, m=mk)


lane(API_Y, "클러스터 API 오브젝트")
box(0, API_Y, "파드", "runtimeClassName: gvisor", INFO)
box(1, API_Y, "RuntimeClass", "handler: runsc", INFO)
right(0, API_Y)

lane(NODE_Y, "워커 노드")
box(1, NODE_Y, "containerd", "runtimes.runsc", SOFT)
box(2, NODE_Y, "gVisor (runsc)", "사용자 공간 커널", ACC, False)
box(3, NODE_Y, "호스트 커널", "컨테이너와 직접 닿지 않음", SOFT, False)
right(1, NODE_Y)
right(2, NODE_Y, ACC, "acc", 1.8)

# RuntimeClass → containerd (레인 넘기기)
cx = col(1) + BW / 2
d.path(f"M {cx} {API_Y + 34 + BH + 2} L {cx} {NODE_Y + 34 - 2}", MUTED, 1.4, m="ar")
d.chip(cx + 60, API_Y + LANE_H + 10, "kubelet 이 handler 이름 전달", MUTED, 11)
d.chip(col(2) + BW + 11, NODE_Y + 34 - 14, "격리 경계", ACC, 11)

d.legend(384, [("API 오브젝트", INFO), ("노드 설정", SOFT), ("샌드박스 경계", ACC)])
d.save("05-02.runtimeclass-path.svg")
