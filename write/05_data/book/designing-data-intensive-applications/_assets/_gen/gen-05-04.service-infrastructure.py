# 05-04 §4 — 서비스 디스커버리·로드 밸런싱·서비스 메시의 결합 구조.
# 사실 출처: 05-04 §4(L82~L94), 원서 Load balancers, service discovery, and service meshes (PDF p.25~26)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
H = 550
LEG = H - 56

d = D(W, H, "05-04 · SERVICE INFRASTRUCTURE", "서비스 디스커버리와 로드 밸런싱 인프라",
      "클라이언트 요청이 서비스 디스커버리·로드 밸런서·서비스 메시를 거쳐 인스턴스로 분산되는 구조.",
      "주소 탐색 · 부하 분산 · 사이드카 프록시 · 가용 인스턴스 풀")

# 1. 좌측: 클라이언트 영역
X_CLI = 24
W_CLI = 180
d.box(X_CLI, 104, W_CLI, 344, PAPER2, RULE, 0.8)
d.t(X_CLI + W_CLI / 2, 128, "클라이언트 영역", 12, SOFT, KR, "middle", 600)

d.box(X_CLI + 16, 210, W_CLI - 32, 110, PAPER, INFO, 1.2)
d.t(X_CLI + W_CLI / 2, 238, "클라이언트", 13, INK, KR, "middle", 600)
d.t(X_CLI + W_CLI / 2, 262, "서비스 요청 발행", 12, INFO, KR, "middle")
d.t(X_CLI + W_CLI / 2, 286, "HTTP · gRPC API 호출", 11, MUTED, MONO, "middle")

# 2. 중앙: 인프라 제어 계층 (디스커버리 & 트래픽 분산)
X_MID = 224
W_MID = 400
d.box(X_MID, 104, W_MID, 344, PAPER2, RULE, 0.8)
d.t(X_MID + W_MID / 2, 128, "인프라 라우팅 및 상태 관리 계층", 12, SOFT, KR, "middle", 600)

# 2-A: 상단 서비스 디스커버리
d.box(X_MID + 16, 142, W_MID - 32, 84, PAPER, WARN, 1.0)
d.t(X_MID + 32, 168, "서비스 디스커버리 (Service Discovery)", 13, WARN, KR, "start", 600)
d.t(X_MID + 32, 192, "중앙 레지스트리 (etcd · ZooKeeper)", 12, INK, KR, "start")
d.t(X_MID + 32, 212, "가용 엔드포인트 추적 · heartbeat 로 갱신", 12, MUTED, KR, "start")

# 2-B: 하단 트래픽 분산 제어 (LB & Service Mesh)
d.box(X_MID + 16, 264, W_MID - 32, 170, PAPER, ACC, 1.0)
d.t(X_MID + 32, 290, "트래픽 분산 계층 (Traffic Routing)", 13, ACC, KR, "start", 600)

# LB 세부 박스
d.box(X_MID + 28, 302, W_MID - 56, 54, PAPER2, RULE, 0.8)
d.t(X_MID + 40, 322, "로드 밸런서 (HW · NGINX · HAProxy · DNS)", 12, INK, KR, "start", 600)
d.t(X_MID + 40, 342, "단일 진입점 제공 · 인스턴스 트래픽 분산", 12, MUTED, KR, "start")

# Service Mesh 세부 박스
d.box(X_MID + 28, 364, W_MID - 56, 56, PAPER2, OK, 0.9)
d.t(X_MID + 40, 384, "서비스 메시 (Istio · Linkerd Sidecar)", 12, OK, KR, "start", 600)
d.t(X_MID + 40, 404, "로컬 프록시 배포 · TLS 암호화 · 호출 관측성", 12, MUTED, KR, "start")

# 3. 우측: 서비스 인스턴스 풀
X_SVC = 644
W_SVC = 212
d.box(X_SVC, 104, W_SVC, 344, PAPER2, RULE, 0.8)
d.t(X_SVC + W_SVC / 2, 128, "서비스 인스턴스 풀", 12, SOFT, KR, "middle", 600)

# 인스턴스 3개
d.box(X_SVC + 16, 142, W_SVC - 32, 80, PAPER, OK, 1.1)
d.t(X_SVC + W_SVC / 2, 168, "서비스 인스턴스 01", 13, INK, KR, "middle", 600)
d.t(X_SVC + W_SVC / 2, 190, "시작 시 호스트·포트 등록", 12, WARN, KR, "middle")
d.t(X_SVC + W_SVC / 2, 210, "비즈니스 로직 서빙", 11, MUTED, KR, "middle")

d.box(X_SVC + 16, 236, W_SVC - 32, 80, PAPER, OK, 1.1)
d.t(X_SVC + W_SVC / 2, 262, "서비스 인스턴스 02", 13, INK, KR, "middle", 600)
d.t(X_SVC + W_SVC / 2, 284, "주기적 heartbeat", 12, OK, KR, "middle")
d.t(X_SVC + W_SVC / 2, 304, "분산 요청 처리", 11, MUTED, KR, "middle")

d.box(X_SVC + 16, 330, W_SVC - 32, 80, PAPER, OK, 1.1)
d.t(X_SVC + W_SVC / 2, 356, "서비스 인스턴스 03", 13, INK, KR, "middle", 600)
d.t(X_SVC + W_SVC / 2, 378, "새로 뜬 인스턴스", 12, ACC, KR, "middle")
d.t(X_SVC + W_SVC / 2, 398, "등록하면 요청을 받음", 11, MUTED, KR, "middle")

# 직교 연결 화살표 (Orthogonal / Manhattan)
# 클라이언트 -> 로드 밸런서
d.arrow([(X_CLI + W_CLI - 16, 265), (X_CLI + W_CLI + 12, 265), (X_CLI + W_CLI + 12, 329), (X_MID + 28, 329)], INFO, "info", 1.4)

# 로드 밸런서 -> 인스턴스 01
d.arrow([(X_MID + W_MID - 28, 320), (X_MID + W_MID + 8, 320), (X_MID + W_MID + 8, 182), (X_SVC + 16, 182)], ACC, "acc", 1.3)

# 로드 밸런서 -> 인스턴스 02 (수평)
d.arrow([(X_MID + W_MID - 28, 329), (X_MID + W_MID + 8, 329), (X_MID + W_MID + 8, 276), (X_SVC + 16, 276)], ACC, "acc", 1.3)

# 로드 밸런서 -> 인스턴스 03
d.arrow([(X_MID + W_MID - 28, 338), (X_MID + W_MID + 8, 338), (X_MID + W_MID + 8, 370), (X_SVC + 16, 370)], ACC, "acc", 1.3)

# 인스턴스 01 -> 서비스 디스커버리 (엔드포인트 등록 & Heartbeat, 수평)
d.arrow([(X_SVC + 16, 172), (X_MID + W_MID - 16, 172)], WARN, "warn", 1.3, dash="4 4")

# 서비스 디스커버리 -> 트래픽 제어 (가용 주소 동기화, 수직)
d.arrow([(X_MID + W_MID / 2, 226), (X_MID + W_MID / 2, 264)], WARN, "warn", 1.3, dash="4 4")

d.legend(LEG, [("클라이언트 요청", INFO), ("트래픽 분산 계층", ACC), ("서비스 인스턴스", OK), ("엔드포인트 등록·감시", WARN)])
d.save("05-04.service-infrastructure.svg")
