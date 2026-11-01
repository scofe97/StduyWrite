# 타입 스펙: type-swimlane — 새 노드 합류 시 Cilium Operator 와 Agent 간 PodCIDR 할당 스윔레인.
# 사실 출처: 《Cilium: Up and Running》 Ch.2 p.8 (Figure 2-4 "The Cilium operator manages IP address allocation") 및 본문 §4 L161~165.
# 단계 번호는 본문 목록 1~5 와 같다. 10.1.1.0/24 는 원서 Figure 2-4 (p.8) 의 podCIDRs 예 값이다(본문에는 값이 없다).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 02-01 §4", "새 노드 합류 시 PodCIDR 할당 스윔레인",
      "클러스터 전역 오퍼레이터와 노드별 에이전트 간 조율과 주소 블록 배분",
      "오퍼레이터의 중복 없는 IP 풀 배분과 에이전트의 로컬 데이터패스 반영 흐름")

Y_OP = 106
H_LANE = 130
Y_AG = 276

# 상단 레인: CILIUM OPERATOR
# 좌측 레이블 컬럼
d.box(24, Y_OP, 126, H_LANE, PAPER2, RULE, sw=0.9, r=6)
d.t(87, Y_OP + 52, "OPERATOR", 11, INK, MONO, "middle", 600)
d.t(87, Y_OP + 74, "클러스터 컨트롤", 11, INK, KR, "middle")
d.t(87, Y_OP + 92, "Deployment", 10, MUTED, MONO, "middle")

# 메인 작업 레인
d.box(154, Y_OP, 742, H_LANE, PAPER2, RULE, sw=0.9, r=6)


# 하단 레인: 워커 노드 (노드 등록 + cilium-agent)
# 좌측 레이블 컬럼
d.box(24, Y_AG, 126, H_LANE, PAPER2, RULE, sw=0.9, r=6)
d.t(87, Y_AG + 52, "NODE", 11, INK, MONO, "middle", 600)
d.t(87, Y_AG + 74, "워커 노드", 11, INK, KR, "middle")
d.t(87, Y_AG + 92, "cilium-agent", 10, MUTED, MONO, "middle")

# 메인 작업 레인
d.box(154, Y_AG, 742, H_LANE, PAPER2, RULE, sw=0.9, r=6)


# 단계 1: (노드 레인) 신규 워커 노드 기동과 등록
X0 = 170
d.box(X0, Y_AG + 30, 120, 70, PAPER, SOFT, sw=0.9, r=4)
d.t(X0 + 60, Y_AG + 52, "1. 신규 노드 기동", 11, INK, KR, "middle", 600)
d.t(X0 + 60, Y_AG + 70, "API 서버에", 11, SOFT, KR, "middle")
d.t(X0 + 60, Y_AG + 88, "노드 등록 이벤트", 11, MUTED, KR, "middle")

# 핸드오프 1 -> 2: 노드 등록 이벤트 -> 오퍼레이터 감지 (상향 점선 화살표)
X2 = 344
d.arrow([(X0 + 60, Y_AG + 30), (X0 + 60, Y_OP + 65), (X2, Y_OP + 65)], SOFT, "ar", sw=1.3, dash="3 3")


# 단계 2: (Operator 레인) 노드 추가 감지와 PodCIDR 블록 선점
d.tone(X2, Y_OP + 30, 180, 70, WARN, r=4, op="18", sw=1.2)
d.t(X2 + 90, Y_OP + 52, "2. 노드 감지 · 선점", 11, WARN, KR, "middle", 600)
d.t(X2 + 90, Y_OP + 70, "클러스터 풀에서", 11, INK, KR, "middle")
d.t(X2 + 90, Y_OP + 88, "중복 없는 PodCIDR 블록", 11, MUTED, KR, "middle")

# 내부 이동 2 -> 3
X3 = 576
d.arrow([(X2 + 180, Y_OP + 65), (X3, Y_OP + 65)], WARN, "warn", sw=1.3)


# 단계 3: (Operator 레인) CiliumNode 생성과 대역 기록
d.box(X3, Y_OP + 30, 150, 70, PAPER, ACC, sw=0.9, r=4)
d.t(X3 + 75, Y_OP + 52, "3. CiliumNode 생성", 11, ACC, KR, "middle", 600)
d.t(X3 + 75, Y_OP + 70, "spec.ipam.podCIDRs", 10, INK, MONO, "middle")
d.t(X3 + 75, Y_OP + 88, "10.1.1.0/24", 11, ACC, MONO, "middle", 600)

# 핸드오프 3 -> 4: 에이전트가 CiliumNode 를 감시 (하향 화살표)
d.arrow([(X3 + 75, Y_OP + 100), (X3 + 75, Y_AG + 30)], ACC, "acc", sw=1.4)
d.t(X3 + 85, (Y_OP + 100 + Y_AG + 30)/2 + 4, "CiliumNode 감시", 11, ACC, KR, "start", 600)


# 단계 4: (노드 레인) 에이전트가 자기 노드 CIDR 수신
X4 = X3
d.box(X4, Y_AG + 30, 150, 70, PAPER, ACC, sw=0.9, r=4)
d.t(X4 + 75, Y_AG + 52, "4. 할당 대역 수신", 11, ACC, KR, "middle", 600)
d.t(X4 + 75, Y_AG + 70, "10.1.1.0/24", 11, ACC, MONO, "middle", 600)
d.t(X4 + 75, Y_AG + 88, "자기 노드 CIDR", 11, MUTED, KR, "middle")

# 내부 이동 4 -> 5
X5 = 752
d.arrow([(X4 + 150, Y_AG + 65), (X5, Y_AG + 65)], OK, "ok", sw=1.3)


# 단계 5: (노드 레인) 로컬 IPAM 주소 풀 초기화와 eBPF 라우팅 맵 갱신
d.tone(X5, Y_AG + 30, 132, 70, OK, r=4, op="18", sw=1.2)
d.t(X5 + 66, Y_AG + 52, "5. 로컬 IPAM 구성", 11, OK, KR, "middle", 600)
d.t(X5 + 66, Y_AG + 70, "주소 풀 초기화", 11, INK, KR, "middle")
d.t(X5 + 66, Y_AG + 88, "eBPF 라우팅 맵 갱신", 11, MUTED, KR, "middle")


# 하단 범례
d.legend(430, [
    ("노드 등록 이벤트", SOFT),
    ("감지 · 대역 선점", WARN),
    ("CiliumNode 동기화 (핵심)", ACC),
    ("로컬 주소 풀 적용", OK),
])

d.save("02-01.operator-node-cidr.svg")
