# 타입 스펙: type-tree
import sys

sys.path.insert(0, ".")

from dd import ACC, INFO, INK, KR, MONO, MUTED, OK, PAPER, PAPER2, RULE, SOFT, D

W = 1000
SX = 500
TOP = 164
STRIDE = 156
STAGE_W = 300
STAGE_H = 64
SIDE_W = 300
SIDE_H = 92

stages = [
    ("1", "오브젝트", "필수", INFO,
     ["API · manifest · Pod", "ConfigMap · Secret", "probe · lifecycle"],
     ["Pod 상태와 이벤트에서", "멈춘 지점을 찾습니다"]),
    ("2", "워크로드", "필수", INFO,
     ["Deployment · ReplicaSet", "StatefulSet · DaemonSet", "Job · CronJob · rollout"],
     ["목적에 맞는 컨트롤러와", "배포 전략을 선택합니다"]),
    ("3", "연결", "필수", INFO,
     ["Service · EndpointSlice · DNS", "Ingress · Gateway API", "NetworkPolicy · CNI"],
     ["연결 실패를 오브젝트와", "데이터패스로 나눕니다"]),
    ("4", "자원과 저장", "필수", ACC,
     ["request · limit · QoS", "scheduling · autoscaling", "PV · PVC · CSI"],
     ["Pending과 저장 문제를", "배치와 볼륨 조건에서 찾습니다"]),
    ("5", "내부 구조", "필수", INFO,
     ["API Server · etcd", "Scheduler · Controller · kubelet", "CRI · CNI · CSI · TLS"],
     ["apply 이후 각 구성 요소의", "결정을 순서대로 설명합니다"]),
    ("6", "보안과 확장", "추천", OK,
     ["RBAC · SecurityContext", "Admission · CRD", "Controller · Operator · finalizer"],
     ["권한을 줄이고 원하는 상태를", "반복 조정하는 구조를 만듭니다"]),
    ("7", "운영", "필수", INFO,
     ["event · log · metric", "OOMKilled · CPU throttling", "SIGTERM · PDB · recovery"],
     ["증거를 같은 시간축으로 이어", "장애 원인을 좁힙니다"]),
]

H = TOP + STRIDE * len(stages) + 92
d = D(W, H, "WRITE · KUBERNETES ROADMAP", "Kubernetes 학습 로드맵",
      "오브젝트에서 워크로드, 연결, 자원과 저장, 내부 구조, 보안과 확장, 운영으로 이어지는 일곱 단계입니다.",
      "왼쪽은 핵심 키워드, 가운데는 단계, 오른쪽은 완료 기준입니다")

d.box(SX - 116, 96, 232, 44, PAPER2, RULE, 1.0)
d.t(SX, 123, "일곱 단계를 순서대로 봅니다", 14, INK, KR, "middle", 600)
d.line(SX, 140, SX, TOP + STRIDE * (len(stages) - 1) + STAGE_H, RULE, 1.4)

for index, (number, title, priority, color, keywords, completion) in enumerate(stages):
    y = TOP + index * STRIDE
    mid = y + STAGE_H / 2
    side_y = mid - SIDE_H / 2
    d.line(330, mid, SX - STAGE_W / 2, mid, RULE, 1.0)
    d.line(SX + STAGE_W / 2, mid, 670, mid, RULE, 1.0)
    d.box(30, side_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(46, side_y + 20, "핵심 키워드", 13, SOFT, KR, "start", 600)
    for line_index, keyword in enumerate(keywords):
        d.t(46, side_y + 42 + line_index * 18, keyword, 13, MUTED, KR, "start")
    if index == 3:
        d.tone(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, ACC, 6, "14", 1.4)
    else:
        d.box(SX - STAGE_W / 2, y, STAGE_W, STAGE_H, PAPER, color, 1.2)
    d.t(SX - 128, y + 25, number, 12, color, MONO, "start", 600)
    d.t(SX + 6, y + 26, title, 15, ACC if index == 3 else INK, KR, "middle", 600)
    d.t(SX + 6, y + 49, priority, 13, color, KR)
    d.box(670, side_y, SIDE_W, SIDE_H, PAPER2, RULE, 0.9)
    d.t(686, side_y + 20, "완료 기준", 13, SOFT, KR, "start", 600)
    for line_index, line in enumerate(completion):
        d.t(686, side_y + 48 + line_index * 20, line, 13, MUTED, KR, "start")

d.legend(H - 52, [("필수", INFO), ("추천", OK), ("운영 핵심", ACC)])
d.save("k8s-roadmap.svg")
