# 타입 스펙: type-swimlane — 새 노드 합류 시 Cilium Operator 와 Agent 간 PodCIDR 할당 스윔레인.
# 사실 출처: Cilium Up and Running 2장 The Cilium Operator (§Figure 2-4).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 02-01 §4", "새 노드 합류 시 PodCIDR 할당 스윔레인",
      "클러스터 전역 오퍼레이터와 노드별 에이전트 간 비동기 조율 및 주소 블록 배분",
      "오퍼레이터가 중복 없는 IP 풀을 배분하고 에이전트는 로컬 데이터패스에 적용합니다")

Y_OP = 106
H_LANE = 130
Y_AG = 276

# 상단 레인: CILIUM OPERATOR
# 좌측 레이블 컬럼
d.box(24, Y_OP, 126, H_LANE, PAPER2, RULE, sw=0.9, r=6)
d.t(87, Y_OP + 52, "OPERATOR", 11, INFO, MONO, "middle", 600)
d.t(87, Y_OP + 74, "클러스터 컨트롤", 11, INK, KR, "middle")
d.t(87, Y_OP + 92, "Deployment", 10, MUTED, MONO, "middle")

# 메인 작업 레인
d.box(154, Y_OP, 742, H_LANE, PAPER2, RULE, sw=0.9, r=6)


# 하단 레인: CILIUM AGENT
# 좌측 레이블 컬럼
d.box(24, Y_AG, 126, H_LANE, PAPER2, RULE, sw=0.9, r=6)
d.t(87, Y_AG + 52, "AGENT", 11, ACC, MONO, "middle", 600)
d.t(87, Y_AG + 74, "노드 데몬", 11, INK, KR, "middle")
d.t(87, Y_AG + 92, "DaemonSet", 10, MUTED, MONO, "middle")

# 메인 작업 레인
d.box(154, Y_AG, 742, H_LANE, PAPER2, RULE, sw=0.9, r=6)


# 선행: (Agent 레인) 신규 노드 기동 및 등록
X0 = 170
d.box(X0, Y_AG + 30, 110, 70, PAPER, SOFT, sw=0.9, r=4)
d.t(X0 + 55, Y_AG + 52, "신규 노드 기동", 11, INK, KR, "middle", 600)
d.t(X0 + 55, Y_AG + 70, "kubelet 부팅", 11, SOFT, KR, "middle")
d.t(X0 + 55, Y_AG + 88, "Node 객체 등록", 11, MUTED, KR, "middle")

# 핸드오프: K8s API 등록 -> 오퍼레이터 감지 (상향 점선 화살표)
d.arrow([(X0 + 55, Y_AG + 30), (X0 + 55, Y_OP + 65), (292, Y_OP + 65)], INFO, "info", sw=1.3, dash="3 3")
d.t(X0 + 46, 256, "API 서버 등록", 11, INFO, KR, "end")


# 단계 1: (Operator 레인) 신규 노드 감지
X1 = 292
d.box(X1, Y_OP + 30, 116, 70, PAPER, INFO, sw=0.9, r=4)
d.t(X1 + 58, Y_OP + 52, "1. 노드 감지", 11, INFO, KR, "middle", 600)
d.t(X1 + 58, Y_OP + 70, "API 서버 이벤트", 11, INK, KR, "middle")
d.t(X1 + 58, Y_OP + 88, "새 Node 등록 포착", 11, MUTED, KR, "middle")

# 내부 이동 1 -> 2
d.arrow([(X1 + 116, Y_OP + 65), (X1 + 148, Y_OP + 65)], INFO, "info", sw=1.3)


# 단계 2: (Operator 레인) 전역 IP 풀 대조 및 대역 선점
X2 = 440
d.tone(X2, Y_OP + 30, 120, 70, WARN, r=4, op="18", sw=1.2)
d.t(X2 + 60, Y_OP + 52, "2. IP 풀 대조", 11, WARN, KR, "middle", 600)
d.t(X2 + 60, Y_OP + 70, "ClusterPool 모드", 11, INK, KR, "middle")
d.t(X2 + 60, Y_OP + 88, "중복 없는 CIDR 선점", 11, MUTED, KR, "middle")

# 내부 이동 2 -> 3
d.arrow([(X2 + 120, Y_OP + 65), (X2 + 152, Y_OP + 65)], INFO, "info", sw=1.3)


# 단계 3: (Operator 레인) CiliumNode 생성
X3 = 592
d.box(X3, Y_OP + 30, 126, 70, PAPER, OK, sw=0.9, r=4)
d.t(X3 + 63, Y_OP + 52, "3. CiliumNode 생성", 11, OK, KR, "middle", 600)
d.t(X3 + 63, Y_OP + 70, "10.244.1.0/24", 11, OK, MONO, "middle", 600)
d.t(X3 + 63, Y_OP + 88, "spec.ipam 기재", 11, MUTED, KR, "middle")

# 핸드오프 3 -> 4: 오퍼레이터 CRD 생성 -> 에이전트 Watch 감지 (하향 화살표)
d.arrow([(X3 + 63, Y_OP + 100), (X3 + 63, Y_AG + 30)], ACC, "acc", sw=1.4)
d.t(X3 + 73, (Y_OP + 100 + Y_AG + 30)/2 + 4, "CiliumNode Watch", 11, ACC, KR, "start", 600)


# 단계 4: (Agent 레인) CiliumNode 감시 및 대역 수신
X4 = 592
d.box(X4, Y_AG + 30, 126, 70, PAPER, ACC, sw=0.9, r=4)
d.t(X4 + 63, Y_AG + 52, "4. 할당 대역 수신", 11, ACC, KR, "middle", 600)
d.t(X4 + 63, Y_AG + 70, "CiliumNode 감시", 11, INK, KR, "middle")
d.t(X4 + 63, Y_AG + 88, "자기 노드 CIDR 확인", 11, MUTED, KR, "middle")

# 내부 이동 4 -> 5
d.arrow([(X4 + 126, Y_AG + 65), (X4 + 158, Y_AG + 65)], ACC, "acc", sw=1.3)


# 단계 5: (Agent 레인) 로컬 eBPF 주소 풀 구성
X5 = 750
d.tone(X5, Y_AG + 30, 132, 70, ACC, r=4, op="18", sw=1.2)
d.t(X5 + 66, Y_AG + 52, "5. 로컬 IPAM 구성", 11, ACC, KR, "middle", 600)
d.t(X5 + 66, Y_AG + 70, "eBPF 맵 초기화", 11, INK, KR, "middle")
d.t(X5 + 66, Y_AG + 88, "Pod IP 발급 준비", 11, MUTED, KR, "middle")


# 하단 범례
d.legend(430, [
    ("노드 이벤트", SOFT),
    ("클러스터 조율", INFO),
    ("CIDR 선점", WARN),
    ("CRD 동기화 (핵심)", ACC),
    ("로컬 적용 완료", OK),
])

d.save("02-01.operator-node-cidr.svg")
