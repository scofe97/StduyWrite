# 03-02.cni-implementations — 구현체 넷을 판별 축으로 세운다
# 본문 요구: §5 의 구현체 비교가 산문으로만 읽힌다. 정작 고를 때 묻는 것은 "캡슐화를 쓰나",
#           "상태를 어디 두나", "정책을 어느 계층까지 거나"다.
#           2026-09-02 사용자 요청 — 이 표를 시각화.
# 타입 스펙: type-dp-security-matrix.md 의 격자를 비교 행렬로 쓴다. 행이 구현체, 캡슐화 열이
#           판정 축이라 focal_col 로 그 열을 세운다.
# 근거(버전 고정): flannel v0.28.10 README·Documentation/backends.md, cilium v1.20.5
#       Documentation/network/concepts/routing.rst·overview/intro.rst, Calico 3.33 문서
#       networking/configuring/vxlan-ipip, amazon-vpc-cni-k8s v1.23.3 docs/cni-proposal.md.
# 이력: 2026-11-18 — 칸의 사실을 지금 문서에 맞췄다. Cilium 은 설정이 없으면 캡슐화로 돌고(옛 판 「선택」),
#       Flannel 의 상태 저장소는 Kubernetes API 또는 etcd 이며, Calico 의 Istio 통합은 지금 문서에서
#       확인하지 못해 뺐다. 행을 캡슐화하는 둘 · 안 하는 둘 순으로 다시 놓고 색을 그 축 두 가지로 줄였다.
# 좌표: ddx.matrix 로 격자를 구현한다. 열 gap 12, 행 stride row_h+gap 하나. 전부 4의 배수.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, PAPER2, KR, MONO

W, H = 1000, 604
X0, GAP, ROW_H, HDR_Y = 24, 12, 80, 140
COLS = [(168, "구현체"), (232, "접근"), (236, "노드 사이를 캡슐화하나"), (280, "상태와 정책")]

ROWS = [
    ([("Flannel", "L3 패브릭"),
      ("노드마다 서브넷을 빌려 줌", "노드마다 flanneld 가 실행"),
      ("권장 백엔드가 VXLAN", "host-gw 는 감싸지 않음"),
      ("Kubernetes API 또는 etcd", "정책은 다른 도구를 붙임")], WARN),
    ([("Cilium", "eBPF"),
      ("커널에 eBPF 프로그램 탑재", "HTTP 계층까지 인지"),
      ("설정이 없으면 캡슐화", "native routing 으로 전환 가능"),
      ("identity 기준 L3~L7 정책", "정책이 주소 아닌 identity 에 걸림")], WARN),
    ([("Calico", "L3 라우팅"),
      ("노드가 Pod 경로를 주고받음", "L3 경로로 Pod 에 도달"),
      ("권장은 캡슐화 없음", "VXLAN · IP in IP 는 선택"),
      ("Felix · BIRD 가 경로 관리", "VXLAN 풀은 Felix, 나머지는 BGP")], OK),
    ([("AWS VPC CNI", "네이티브 VPC"),
      ("ENI 의 보조 IP 를 Pod 에", "Pod 가 VPC 주소를 가짐"),
      ("캡슐화 없음", "VPC 가 Pod 주소를 라우팅"),
      ("VPC flow logs · 보안 그룹", "기존 VPC 도구를 그대로 씀")], OK),
]

d = D(W, H, "CNI IMPLEMENTATIONS · WHAT ACTUALLY DIFFERS",
      "구현체 넷은 캡슐화 여부와 상태를 두는 자리에서 갈린다",
      "CNI 구현체 네 종을 노드 사이 캡슐화 여부와 상태·정책 축으로 견준 대조표. "
      "가운데 열이 판정 축이며, 캡슐화를 쓰는지가 MTU 부담과 물리망 요구를 함께 정한다.",
      lead="같은 인터페이스를 구현하지만 노드 사이를 감싸는가 · 상태를 어디 두는가 · 정책을 어디까지 거는가가 갈립니다")

ddx.matrix(d, X0, COLS, ROWS, HDR_Y, row_h=ROW_H, gap=GAP, focal_col=2)

BOTTOM = HDR_Y + 24 + len(ROWS) * (ROW_H + GAP)
# 감쌈의 대가와 Calico CrossSubnet 단서는 본문 §5 산문이 맡는다
d.legend(BOTTOM + 12, [("기본·권장이 캡슐화", WARN), ("캡슐화 없이 라우팅", OK)])
d.save("03-02.cni-implementations.svg")
print("ok cni-implementations")
