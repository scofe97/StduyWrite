# 타입 스펙: type-sequence
# 03-05 kubeadm join 과 TLS 부트스트래핑 흐름
import sys
sys.path.insert(0, ".")
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 880, 540

d = D(W, H, "KUBERNETES · OPERATIONS · 03-05",
      "kubeadm join 과 TLS 부트스트래핑 흐름",
      "부트스트랩 토큰과 CA 해시로 상호 신뢰를 검증하고 kubelet 인증서를 발급합니다",
      lead="토큰 기반 API 서버 탐색(상단) 및 CSR 발급·자동 승인과 노드 등록(하단)")

# 액터 수직 레인 정의
LX = {"worker": 140, "apiserver": 440, "controller": 740}
LANE_TOP = 110
LANE_BOT = 450

# 액터 헤더 상자
ACTORS = [
    ("worker", "새 워커 노드", "kubeadm · kubelet", INFO),
    ("apiserver", "API 서버", "kube-apiserver (6443)", ACC),
    ("controller", "컨트롤러 매니저", "csrapproving 컨트롤러", OK),
]

for key, title, sub, col in ACTORS:
    x = LX[key]
    d.box(x - 90, LANE_TOP, 180, 44, PAPER2, col, 1.0)
    d.t(x, LANE_TOP + 18, title, 13, INK, KR, "middle", 600)
    d.t(x, LANE_TOP + 34, sub, 12, col, MONO, "middle")
    d.line(x, LANE_TOP + 44, x, LANE_BOT, RULE, 1.0, "3 5")

def msg(from_k, to_k, y, label, sub, col=MUTED, mk="ar", dash=None):
    x1, x2 = LX[from_k], LX[to_k]
    direct = 1 if x2 > x1 else -1
    d.arrow([(x1 + 8 * direct, y), (x2 - 8 * direct, y)], col, mk, 1.4, dash=dash)
    mx = (x1 + x2) / 2
    d.t(mx, y - 9, label, 12, col, KR, "middle", 600)
    if sub:
        d.t(mx, y + 18, sub, 12, SOFT, MONO, "middle")

def selfmsg(k, y, label, sub, col=MUTED):
    x = LX[k]
    d.path(f"M {x + 8} {y - 10} L {x + 50} {y - 10} L {x + 50} {y + 10} L {x + 10} {y + 10}", col, 1.4, m="ar")
    d.t(x + 58, y - 2, label, 12, col, KR, "start", 600)
    if sub:
        d.t(x + 58, y + 14, sub, 12, SOFT, MONO, "start")

# 1. Cluster-info 조회
msg("worker", "apiserver", 185, "1. cluster-info 조회", "kube-public/cluster-info (인증 없음)", INFO, "info")

# 2. CA 인증서 반환
msg("apiserver", "worker", 230, "2. 루트 CA 담은 kubeconfig 응답", "ConfigMap 에 CA·토큰 서명 포함", INFO, "info", dash="3 3")

# 3. CA 해시 검증
selfmsg("worker", 270, "3. 토큰 서명·CA 해시 검증", "SPKI sha256 대조 (가짜 서버 차단)", WARN)

# 4. CSR 요청 생성
msg("worker", "apiserver", 315, "4. 토큰으로 CSR 제출", "signer: kube-apiserver-client-kubelet", INFO, "info")

# 5. CSR 감지 및 자동 승인
msg("controller", "apiserver", 360, "5. CSR 자동 승인", "csrapproving (SubjectAccessReview)", OK, "ok")

# 6. 서명된 인증서 발급
msg("apiserver", "worker", 405, "6. 서명된 인증서 발급", "kubelet 클라이언트 인증서 수신", OK, "ok", dash="3 3")

# 7. 노드 등록 완료
selfmsg("worker", 442, "7. 정식 노드 등록", "kubelet.conf 남김, 임시 파일 삭제", OK)

# 범례
LEG_Y = 485
d.legend(LEG_Y, [
    ("탐색 및 요청", INFO),
    ("해시 검증", WARN),
    ("승인 및 등록", OK),
    ("API 엔드포인트", ACC),
])

d.save("03-05-join-bootstrap.svg")
