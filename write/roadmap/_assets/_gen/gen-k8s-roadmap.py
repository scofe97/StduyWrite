# write/roadmap/k8s-roadmap.md §학습 순서 — Kubernetes 학습 로드맵.
#
# 판형은 roadmap.sh 계열이다 — 세로 척추에 단계를 걸고 개념을 좌우로 뻗되,
#   노드마다 우선순위 점을 찍는다. 단계에만 배지를 달던 앞 판은 한 단계 안에서
#   무엇이 뼈대이고 무엇이 곁가지인지 말하지 못했다.
#
# 노드의 주인공은 개념이고 책은 그 개념을 다루는 자리다. 책 줄이 비면 아직 자료가 없다는 뜻이고,
#   소장 목록이 늘면 그 줄만 채운다. 정독 노트 편수는 도식에 적지 않는다 —
#   "어디를 펴야 하는가"에 답하지 않는 정보다. 노트 링크는 본문 단계 표가 맡는다.
#
# 대체(ACC)는 같은 자리를 두 자료가 대신 채우는 경우다. 둘 다 읽으라는 뜻이 아니다.
# 타입 스펙: type-tree — 부모(단계)에서 자식(개념)으로 갈라지는 계층.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

SX = 500
W = 1000
NODE_W, NODE_H = 320, 52
CH_W, CH_H, CH_GAP = 268, 46, 10
BUS, ROW_GAP, PHASE_GAP = 184, 44, 40
NOTE_H = 76
ELBOW = 14

MARK = {"필수": INFO, "추천": OK, "선택": SOFT, "대체": ACC}

# (단계 제목, 단계 부제, [왼쪽], [오른쪽])
#   개념 노드 = (개념, 책 챕터 — 없으면 빈 문자열, 우선순위)
stages = [
    ("1 · 오브젝트", "선언과 생애주기",
     [("API resource · 매니페스트 구조", "Kubernetes in Action 4장", "필수"),
      ("metadata · spec · status", "Kubernetes in Action 4장", "필수"),
      ("Pod · 컨테이너 그룹화 · 사이드카", "Kubernetes in Action 5장", "필수"),
      ("phase · conditions · 컨테이너 상태", "Kubernetes in Action 6장", "필수"),
      ("probe 셋 — liveness · startup", "K8s Patterns 4장", "필수"),
      ("lifecycle hook · 종료 흐름", "K8s Patterns 5장", "필수")],
     [("namespace · label · selector", "Kubernetes in Action 7장", "필수"),
      ("annotation · field selector", "Kubernetes in Action 7장", "추천"),
      ("command · args · 환경변수", "Kubernetes in Action 8장", "필수"),
      ("ConfigMap · Secret · Downward", "K8s Patterns 19~22장", "필수"),
      ("kubectl 기본 조회", "K8s Up and Running 4장", "필수"),
      ("컨테이너 격리 — namespace · cgroup", "Kubernetes in Action 2장", "추천")]),

    ("2 · 워크로드", "무엇이 Pod 를 만들고 지키는가",
     [("ReplicaSet · reconciliation", "Kubernetes in Action 14장", "필수"),
      ("Deployment · pod-template-hash", "Kubernetes in Action 15장", "필수"),
      ("RollingUpdate · maxSurge", "K8s Patterns 3장", "필수"),
      ("rollout 제어 · pause · rollback", "Kubernetes in Action 15장", "필수"),
      ("배포 전략 다섯", "Kubernetes in Action 15장", "추천")],
     [("StatefulSet · ordinal · headless", "K8s Patterns 12장", "필수"),
      ("DaemonSet · hostNetwork", "K8s Patterns 9장", "필수"),
      ("Job · CronJob · 병렬 · work queue", "K8s Patterns 7·8장", "추천"),
      ("init container · sidecar", "K8s Patterns 15·16장", "추천"),
      ("adapter · ambassador", "K8s Patterns 17·18장", "선택")]),

    ("3 · 연결", "오브젝트가 트래픽을 받는 방법",
     [("Service · ClusterIP · 어피니티", "Kubernetes in Action 11장", "필수"),
      ("NodePort · LoadBalancer", "Kubernetes in Action 11장", "필수"),
      ("Endpoint · EndpointSlice", "Kubernetes in Action 11장", "필수"),
      ("클러스터 DNS · Service FQDN", "Kubernetes in Action 11장", "필수")],
     [("Ingress · IngressClass · TLS", "Kubernetes in Action 12장", "필수"),
      ("Gateway API · HTTPRoute · 필터", "Kubernetes in Action 13장", "필수"),
      ("크로스 네임스페이스 · mesh 연동", "Kubernetes in Action 13장", "추천"),
      ("Gateway API Inference Extension", "", "선택")]),

    ("4 · 자원과 저장", "무엇을 얼마나 쓰고 어디에 남기는가",
     [("requests · limits · QoS", "K8s Patterns 2장", "필수"),
      ("taint · toleration · affinity", "K8s Patterns 6장", "필수"),
      ("토폴로지 분산 · PDB", "", "추천"),
      ("PriorityClass · eviction", "", "추천")],
     [("Volume · emptyDir · projected", "Kubernetes in Action 9장", "필수"),
      ("PV · PVC · StorageClass", "Kubernetes in Action 10장", "필수"),
      ("CSI · 스냅샷 · ephemeral", "Production Kubernetes 4장", "추천"),
      ("HPA · VPA · Cluster Autoscaler", "Production Kubernetes 13장", "추천")]),

    ("5 · 내부 구조", "apply 이후 누가 무엇을 결정하는가",
     [("API Server · etcd · Scheduler", "Kubernetes in Action 1장", "필수"),
      ("Controller Manager · kubelet", "Production Kubernetes 3장", "필수"),
      ("CRI · CNI · CSI · containerd", "Production Kubernetes 3장", "필수"),
      ("조정 루프 · watch · informer", "Programming Kubernetes 3장", "필수")],
     [("authn · authz · admission", "Production Kubernetes 8장", "필수"),
      ("TLS · PKI · 인증서 수명", "", "필수"),
      ("etcd quorum · Raft · 백업 · 복구", "", "필수"),
      ("클러스터 업그레이드", "", "추천")]),

    ("6 · 보안과 확장", "누가 무엇을 할 수 있는가",
     [("RBAC · Role · ServiceAccount", "K8s Up and Running 14장", "필수"),
      ("SecurityContext · seccomp", "K8s Patterns 23장", "필수"),
      ("Pod Security Admission", "CKS Study Guide 3장", "필수"),
      ("NetworkPolicy · 네트워크 분할", "K8s Patterns 24장", "추천"),
      ("Secret 관리 · 외부 저장소", "Production Kubernetes 7장", "추천")],
     [("CRD · custom resource", "Programming Kubernetes 4장", "추천"),
      ("Operator · finalizer", "Programming Kubernetes 6장", "추천"),
      ("status subresource · 코드 생성", "Programming Kubernetes 5·9장", "선택"),
      ("어드미션 웹훅 · Gatekeeper", "Policy as Code 7·8장", "추천"),
      ("공급망 보안 · 이미지 서명", "CKS Study Guide 6장", "선택")]),

    ("7 · 운영", "무엇이 잘못됐는지 어떻게 좁히는가",
     [("이벤트 · 로그 · 지표를 한 시간축에", "", "필수"),
      ("kubectl 고급 조회 · JSONPath", "", "필수"),
      ("OOMKilled · CPU throttling", "", "필수"),
      ("종료 지연 · SIGTERM · PreStop", "", "필수"),
      ("멀티테넌시", "Production Kubernetes 12장", "추천")],
     [("Helm · Kustomize", "", "추천"),
      ("GitOps · ArgoCD", "K8s Best Practices 18장", "추천"),
      ("멀티클러스터 세 모델", "K8s Up and Running 21장", "추천"),
      ("서비스 메시를 쓸 것인가", "K8s Up and Running 15장", "선택"),
      ("CKA 대비와 문제 풀이", "", "선택")]),
]

CUT_AFTER = 3          # 4단계 뒤에 "쓰는 쪽" ↔ "만드는 쪽" 절단선
NOTES = {
    3: "1~4단계는 클러스터를 쓰는 쪽이고 5단계부터는 클러스터를 만들고 지키는 쪽이다.",
    6: "패킷이 실제로 어떤 경로로 가는지는 network-roadmap 이 여덟 단계로 맡는다.",
}


def row_h(left, right):
    n = max(len(left), len(right))
    return max(NODE_H, n * CH_H + (n - 1) * CH_GAP) + 28


ROOT_Y = 116 + 190
y = ROOT_Y + 52 + PHASE_GAP
for i, (_t, _s, left, right) in enumerate(stages):
    y += row_h(left, right) + ROW_GAP
    if i in NOTES:
        y += NOTE_H
    if i == CUT_AFTER:
        y += 56
H = y + 84

d = D(W, H, "WRITE · KUBERNETES ROADMAP",
      "Kubernetes 학습 로드맵",
      "애플리케이션이 여는 socket 에서 커널 패킷 경로로 내려간 뒤 Kubernetes 데이터패스로 다시 "
      "올라간다. 척추에 단계 여덟을 걸고 개념을 좌우로 뻗었다. 노드의 주인공은 개념이고 아래 줄은 "
      "그 개념을 다루는 책의 장이다. 점 색이 우선순위이고, 책 줄이 비면 아직 자료가 없는 자리다.",
      "노드는 개념, 아래 줄은 그 개념을 다루는 책의 장입니다")

LX, LY, LW, LH = 40, 96, 380, 190
d.box(LX, LY, LW, LH, PAPER2, RULE, 1.0)
d.t(LX + 16, LY + 24, "읽는 법", 13, INK, KR, "start", 600)
for i, (lab, txt) in enumerate([("필수", "빼면 뒤가 막힙니다"),
                                ("추천", "빼도 되지만 손해가 큽니다"),
                                ("선택", "목표가 생겼을 때만"),
                                ("대체", "같은 자리 — 하나만 고릅니다")]):
    cy = LY + 54 + i * 26
    c = MARK[lab]
    d.o.append(f'<circle cx="{LX + 24}" cy="{cy}" r="5" fill="{c}"/>')
    d.t(LX + 40, cy + 4, lab, 12, c, KR, "start", 600)
    d.t(LX + 78, cy + 4, txt, 12, MUTED, KR, "start")
d.t(LX + 16, LY + 172, "책 줄이 비면 아직 자료가 없는 자리 — 개념이 먼저입니다", 12, SOFT, KR, "start")

RX, RY, RW, RH = 580, 96, 380, 190
d.box(RX, RY, RW, RH, PAPER, RULE, 0.9)
d.o.append(f'<rect x="{RX}" y="{RY}" width="{RW}" height="{RH}" rx="6" fill="none" '
           f'stroke="{SOFT}" stroke-width="0.9" stroke-dasharray="4 4"/>')
d.t(RX + 16, RY + 24, "여기서 다루지 않는 것", 13, INK, KR, "start", 600)
for i, (who, what) in enumerate([
        ("network-roadmap", "패킷 경로 · CNI 데이터패스 · eBPF"),
        ("os-roadmap", "cgroup · namespace 의 커널 구현"),
        ("06_observability", "Prometheus · Grafana · OpenTelemetry"),
        ("07_devops", "이미지 빌드 · CI 파이프라인")]):
    cy = RY + 56 + i * 33
    d.t(RX + 16, cy, who, 13, MUTED, KR, "start", 600)
    d.t(RX + 16, cy + 16, what, 12, SOFT, KR, "start")

d.box(SX - 130, ROOT_Y, 260, 52, PAPER2, RULE, 1.0)
d.t(SX, ROOT_Y + 32, "여기서 시작합니다", 14, INK, KR, "middle", 600)
d.line(SX, ROOT_Y + 52, SX, H - 120, RULE, 1.4)


def draw_stage(title, sub, left, right, y):
    h = row_h(left, right)
    mid = y + h / 2
    for side, items in (("left", left), ("right", right)):
        sign = -1 if side == "left" else 1
        bus = SX + sign * BUS
        top = mid - (len(items) * CH_H + (len(items) - 1) * CH_GAP) / 2
        d.line(SX + sign * (NODE_W / 2), mid, bus, mid, RULE, 1.0)
        for i, (concept, book, mark) in enumerate(items):
            cy = top + i * (CH_H + CH_GAP) + CH_H / 2
            bx = bus + (sign * ELBOW) - (CH_W if side == "left" else 0)
            c = MARK[mark]
            d.line(bus, mid, bus, cy, RULE, 1.0)
            d.line(bus, cy, bus + sign * ELBOW, cy, RULE, 1.0)
            d.box(bx, cy - CH_H / 2, CH_W, CH_H, PAPER2, RULE, 0.9)
            d.o.append(f'<circle cx="{bx + 15}" cy="{cy - 8}" r="4.5" fill="{c}"/>')
            d.t(bx + 28, cy - 4, concept, 12, INK, KR, "start")
            d.t(bx + 28, cy + 14, book if book else "책 없음 — 채울 자리", 10,
                SOFT if book else MARK["선택"], MONO, "start")
    d.box(SX - NODE_W / 2, mid - NODE_H / 2, NODE_W, NODE_H, PAPER, INFO, 1.2)
    d.t(SX, mid - 4, title, 14, INK, KR, "middle", 600)
    d.t(SX, mid + 16, sub, 11, SOFT, KR)
    return h


def draw_note(text, y):
    d.o.append(f'<rect x="110" y="{y}" width="780" height="{NOTE_H - 12}" rx="6" '
               f'fill="{PAPER}" stroke="{RULE}" stroke-width="0.9" stroke-dasharray="2 4"/>')
    d.t(130, y + 26, "메모", 11, SOFT, MONO, "start")
    d.t(130, y + 46, text, 13, MUTED, KR, "start")
    return NOTE_H


y = ROOT_Y + 52 + PHASE_GAP
for i, (title, sub, left, right) in enumerate(stages):
    y += draw_stage(title, sub, left, right, y) + ROW_GAP
    if i in NOTES:
        y += draw_note(NOTES[i], y)
    if i == CUT_AFTER:
        d.line(40, y + 12, W - 40, y + 12, WARN, 1.4, "6 5")
        d.o.append(f'<rect x="{SX - 235}" y="{y}" width="470" height="22" rx="4" fill="{PAPER}"/>')
        d.t(SX, y + 17, "1~4단계는 쓰는 쪽 · 5단계부터는 만들고 지키는 쪽", 13, WARN, KR)
        y += 56

d.legend(H - 60, [("필수", INFO), ("추천", OK), ("선택", SOFT), ("대체 선택지", ACC),
                  ("쓰는 쪽과 만드는 쪽의 경계", WARN)])
d.save("k8s-roadmap.svg")
