# 03-02.cni-implementations — 구현체 넷을 판별 축으로 세운다
# 본문 요구: §5 의 표가 `CNI · 접근 · 특징` 3열이라 성격 차이가 산문으로만 읽힌다. 정작 고를 때
#           묻는 것은 "오버레이를 쓰나", "상태를 어디 두나", "정책을 어느 계층까지 거나"다.
#           2026-09-02 사용자 요청 — 이 표를 시각화.
# 타입 스펙: type-dp-security-matrix.md 의 격자를 비교 행렬로 쓴다. 행이 구현체, 오버레이 열이
#           판정 축이라 focal_col 로 그 열을 세운다. 같은 문서의 isolation-spectrum 도 이 타입이지만
#           그쪽은 모드 스펙트럼이고 이쪽은 제품 비교라 대상이 다르다.
# 좌표: ddx.matrix 로 격자를 구현한다. 열 gap 12, 행 stride row_h+gap 하나. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 676
X0, GAP, ROW_H, HDR_Y = 24, 12, 80, 140
COLS = [(176, "구현체"), (232, "접근"), (216, "오버레이를 쓰나"), (292, "상태와 정책")]

ROWS = [
    ([("Flannel", "단순 L3 패브릭"),
      ("네트워킹에만 집중", "정책은 다루지 않는다"),
      ("쓴다", "VXLAN 으로 감싼다"),
      ("클러스터의 기존 etcd 재사용", "저장소를 새로 안 세운다")], WARN),
    ([("Calico", "BGP 라우팅"),
      ("경로를 광고해 L3 로 전달", "책이 드는 기본 지향"),
      ("기본은 안 쓴다", "VXLAN·IP-in-IP 모드도 있다"),
      ("네트워크 정책 완전 지원", "Istio 통합")], OK),
    ([("Cilium", "eBPF"),
      ("커널에 프로그램을 심는다", "L7·HTTP 를 인지한다"),
      ("선택", "주소가 아닌 identity 로 판단"),
      ("L3~L7 정책 강제", "주소가 바뀌어도 정책이 산다")], INFO),
    ([("AWS VPC CNI", "네이티브 VPC"),
      ("VPC 주소를 직접 받는다", "AWS 망 위에 그대로"),
      ("안 쓴다", "감쌀 이유가 없다"),
      ("VPC flow logs · 보안 그룹", "기존 AWS 관행 그대로")], BAD),
]

d = D(W, H, "CNI IMPLEMENTATIONS · WHAT ACTUALLY DIFFERS",
      "구현체 넷 — 고를 때 실제로 묻는 것",
      "CNI 구현체 네 종을 오버레이 사용 여부와 상태·정책 축으로 견준 대조표. "
      "가운데 열이 판정 축이며, 오버레이를 쓰는지가 성능과 물리망 요구를 함께 정한다.",
      lead="같은 인터페이스를 구현하지만 감싸는가·어디에 상태를 두는가·정책을 어디까지 거는가가 갈립니다")

ddx.matrix(d, X0, COLS, ROWS, HDR_Y, row_h=ROW_H, gap=GAP, focal_col=2)

BOTTOM = HDR_Y + 24 + len(ROWS) * (ROW_H + GAP)
d.t(X0, BOTTOM + 32, "감싸면 물리망에 손대지 않아도 되고, 안 감싸면 오버헤드가 없는 대신 물리망이 "
                     "Pod 대역을 알아야 합니다.", 12, MUTED, KR, "start")
d.t(X0, BOTTOM + 56, "Calico 행의 \"안 쓴다\"는 기본 지향이지 절대 조건이 아닙니다 — 서브넷 경계를 넘을 때만 "
                     "감싸는 CrossSubnet 모드가 있습니다.", 12, ACC, KR, "start")
d.legend(BOTTOM + 80, [("절대 조건이 아닌 자리", ACC), ("오버레이 없이 라우팅", OK),
                       ("오버레이로 감쌈", WARN), ("커널 프로그램", INFO), ("클라우드 네이티브", BAD)])
d.save("03-02.cni-implementations.svg")
print("ok cni-implementations")
