# 11-03 §1 — 잡 오케스트레이터 구성요소(스케줄러, 리소스 매니저, 태스크 실행기)와 요청 실행 흐름.
# 사실 출처: 11-03 §1(L26~L41), 원서 Ch.11 "Distributed Job Orchestration"(PDF p.12~13).
# 요청 메타데이터 7항목과 "10 tasks · Docker image" 예는 원서 p.12~13. 클러스터 상태 저장소는 원서 p.13 "YARN uses ZooKeeper, Kubernetes uses etcd".
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 414
H = LEG + 48

d = D(W, H, "11-03 · §1 DISTRIBUTED JOB ORCHESTRATION", "잡 오케스트레이터 구성요소와 요청 실행 흐름",
      "클라이언트 요청 메타데이터를 수신한 중앙 스케줄러와 서브스케줄러가 리소스 매니저의 클러스터 상태를 참조해 노드별 태스크 실행기에 작업을 배치한다.",
      "잡 요청 메타데이터 제출 · 리소스 매니저 전역 상태 조회 · 서브스케줄러 노드 배치 지시 · 노드별 cgroups 격리 실행 및 하트비트 보고")

# 1. 좌측 영역: 클라이언트 잡 요청 (Job Request)
Z1_X, Z1_Y, Z1_W, Z1_H = 24, 102, 214, 286
d.box(Z1_X, Z1_Y, Z1_W, Z1_H, PAPER2, RULE, 1.0)
d.chip(Z1_X + 28, Z1_Y + 20, "입력", WARN, 11, pad=4)
d.t(Z1_X + 118, Z1_Y + 24, "클라이언트 잡 요청", 13, INK, KR, "middle", 600)
d.line(Z1_X + 10, Z1_Y + 38, Z1_X + Z1_W - 10, Z1_Y + 38, RULE, 0.6)

d.box(Z1_X + 12, Z1_Y + 50, Z1_W - 24, 178, PAPER, RULE, 0.8)
d.t(Z1_X + Z1_W / 2, Z1_Y + 70, "요청 메타데이터", 12, WARN, KR, "middle", 600)
d.line(Z1_X + 22, Z1_Y + 80, Z1_X + Z1_W - 22, Z1_Y + 80, RULE, 0.5)

d.t(Z1_X + 24, Z1_Y + 102, "태스크 수: 10개", 11, INK, KR, "start")
d.t(Z1_X + 24, Z1_Y + 124, "요구 자원: CPU · 메모리", 11, INK, KR, "start")
d.t(Z1_X + 24, Z1_Y + 146, "잡 식별자: Job ID", 11, INK, KR, "start")
d.t(Z1_X + 24, Z1_Y + 168, "잡 파라미터: 입출력 데이터", 11, INK, KR, "start")
d.t(Z1_X + 24, Z1_Y + 190, "실행 코드: Docker 이미지", 11, INK, KR, "start")
d.t(Z1_X + 24, Z1_Y + 212, "인증: 접근 자격증명", 11, SOFT, KR, "start")

d.t(Z1_X + Z1_W / 2, Z1_Y + 258, "분산 OS 커널에 잡 등록", 11, MUTED, KR, "middle")

# 2. 중앙 영역: 오케스트레이터 제어 계층 (Resource Manager & Scheduler)
Z2_X, Z2_Y, Z2_W, Z2_H = 262, 102, 310, 286
d.box(Z2_X, Z2_Y, Z2_W, Z2_H, PAPER2, RULE, 1.0)
d.t(Z2_X + Z2_W / 2, Z2_Y + 22, "오케스트레이터 중앙 제어", 13, INK, KR, "middle", 600)
d.line(Z2_X + 10, Z2_Y + 34, Z2_X + Z2_W - 10, Z2_Y + 34, RULE, 0.6)

# 2-A. 상단: 리소스 매니저 (Global State)
RM_X, RM_Y, RM_W, RM_H = Z2_X + 12, Z2_Y + 44, Z2_W - 24, 76
d.box(RM_X, RM_Y, RM_W, RM_H, PAPER, INFO, 1.1)
d.chip(RM_X + 26, RM_Y + 18, "상태", INFO, 11, pad=4)
d.t(RM_X + 130, RM_Y + 22, "리소스 매니저 (RM)", 12, INFO, KR, "middle", 600)
d.t(RM_X + RM_W / 2, RM_Y + 44, "상태 저장: YARN은 ZooKeeper · K8s는 etcd", 11, INK, KR, "middle")
d.t(RM_X + RM_W / 2, RM_Y + 64, "노드별 CPU·메모리·디스크 상태 추적", 11, MUTED, KR, "middle")

# 2-B. 하단: 스케줄러 & 서브스케줄러 (Scheduler)
SCH_X, SCH_Y, SCH_W, SCH_H = Z2_X + 12, Z2_Y + 160, Z2_W - 24, 112
d.tone(SCH_X, SCH_Y, SCH_W, SCH_H, ACC, 6, "14", 1.4)
d.chip(SCH_X + 26, SCH_Y + 18, "배치", ACC, 11, pad=4)
d.t(SCH_X + 130, SCH_Y + 22, "스케줄러 계층", 12, ACC, KR, "middle", 600)
d.line(SCH_X + 8, SCH_Y + 34, SCH_X + SCH_W - 8, SCH_Y + 34, RULE, 0.5)

d.t(SCH_X + SCH_W / 2, SCH_Y + 50, "중앙 스케줄러: 잡 수신 및 노드 배치 지시", 11, INK, KR, "middle", 600)
d.box(SCH_X + 8, SCH_Y + 62, SCH_W - 16, 42, PAPER, RULE, 0.8)
d.t(SCH_X + SCH_W / 2, SCH_Y + 77, "애플리케이션 서브스케줄러", 11, INK, KR, "middle", 600)
d.t(SCH_X + SCH_W / 2, SCH_Y + 94, "YARN: ApplicationMaster / K8s: Operator", 11, ACC, MONO, "middle")

# 3. 우측 영역: 분산 워커 노드 (Worker Nodes)
Z3_X, Z3_Y, Z3_W, Z3_H = 596, 102, 260, 286
d.box(Z3_X, Z3_Y, Z3_W, Z3_H, PAPER2, RULE, 1.0)
d.t(Z3_X + Z3_W / 2, Z3_Y + 22, "분산 워커 노드 클러스터", 13, INK, KR, "middle", 600)
d.line(Z3_X + 10, Z3_Y + 34, Z3_X + Z3_W - 10, Z3_Y + 34, RULE, 0.6)

# Node 1
N1_X, N1_Y, N1_W, N1_H = Z3_X + 12, Z3_Y + 44, Z3_W - 24, 102
d.box(N1_X, N1_Y, N1_W, N1_H, PAPER, OK, 1.0)
d.chip(N1_X + 28, N1_Y + 16, "Node 1", OK, 11, pad=4)
d.t(N1_X + 140, N1_Y + 20, "태스크 실행기", 12, INK, KR, "middle", 600)
d.t(N1_X + N1_W / 2, N1_Y + 42, "NodeManager / kubelet 데몬", 11, SOFT, KR, "middle")
d.box(N1_X + 8, N1_Y + 52, N1_W - 16, 40, PAPER2, RULE, 0.8)
d.t(N1_X + N1_W / 2, N1_Y + 68, "Task 1 · Task 2 실행", 11, INK, KR, "middle", 600)
d.t(N1_X + N1_W / 2, N1_Y + 84, "cgroups CPU·메모리 격리", 11, OK, KR, "middle")

# Node 2
N2_X, N2_Y, N2_W, N2_H = Z3_X + 12, Z3_Y + 166, Z3_W - 24, 102
d.box(N2_X, N2_Y, N2_W, N2_H, PAPER, OK, 1.0)
d.chip(N2_X + 28, N2_Y + 16, "Node 2", OK, 11, pad=4)
d.t(N2_X + 140, N2_Y + 20, "태스크 실행기", 12, INK, KR, "middle", 600)
d.t(N2_X + N2_W / 2, N2_Y + 42, "NodeManager / kubelet 데몬", 11, SOFT, KR, "middle")
d.box(N2_X + 8, N2_Y + 52, N2_W - 16, 40, PAPER2, RULE, 0.8)
d.t(N2_X + N2_W / 2, N2_Y + 68, "Task 3 · Task 4 실행", 11, INK, KR, "middle", 600)
d.t(N2_X + N2_W / 2, N2_Y + 84, "cgroups CPU·메모리 격리", 11, OK, KR, "middle")

# 직교 연결 화살표 (Rectilinear Paths)
# 1) Client -> Scheduler
d.path("M 238 240 L 274 240", WARN, 1.4, m="warn")
d.t(250, 230, "제출", 11, WARN, KR, "middle", 600)

# 2) Scheduler <-> Resource Manager (직선 수직 연결: 길이 40px)
d.path(f"M {Z2_X + 120} {SCH_Y} L {Z2_X + 120} {RM_Y + RM_H}", INFO, 1.2, m="info")
d.t(Z2_X + 90, Z2_Y + 140, "상태 조회", 11, INFO, KR, "middle")

d.path(f"M {Z2_X + 190} {RM_Y + RM_H} L {Z2_X + 190} {SCH_Y}", ACC, 1.2, m="acc")
d.t(Z2_X + 220, Z2_Y + 140, "자원 할당", 11, ACC, KR, "middle")

# 3) Scheduler -> Node 1 & Node 2 (직교 꺾임 연결)
# Node 1: right -> up -> right
d.path(f"M {Z2_X + Z2_W} {SCH_Y + 30} L 584 {SCH_Y + 30} L 584 {N1_Y + 50} L {Z3_X + 12} {N1_Y + 50}", ACC, 1.3, m="acc")
# Node 2: right -> down -> right
d.path(f"M {Z2_X + Z2_W} {SCH_Y + 60} L 584 {SCH_Y + 60} L 584 {N2_Y + 50} L {Z3_X + 12} {N2_Y + 50}", ACC, 1.3, m="acc")

# 4) Nodes -> Resource Manager (하트비트 직교 연결)
# Node 1 -> RM
d.path(f"M {Z3_X + 12} {N1_Y + 20} L 584 {N1_Y + 20} L 584 {RM_Y + 30} L {RM_X + RM_W} {RM_Y + 30}", OK, 1.2, m="ok", dash="4 3")
# Node 2 -> RM
d.path(f"M {Z3_X + 12} {N2_Y + 20} L 584 {N2_Y + 20} L 584 {RM_Y + 55} L {RM_X + RM_W} {RM_Y + 55}", OK, 1.2, m="ok", dash="4 3")

# 범례
d.legend(LEG, [
    ("스케줄러 (focal)", ACC),
    ("태스크 실행기", OK),
    ("전역 상태 (RM)", INFO),
    ("잡 메타데이터", WARN),
])

d.save("11-03.orchestrator-components.svg")
