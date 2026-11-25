# a0-02 §6 cluster.env 의 값이 가리키는 것.
# 값 근거(본문 §6 · 부록 E · 9장의 SPIFFE 형식):
#   - 13줄 전체: AUTO_REGISTER_GROUP, CLUSTER_ID, DNS_CAPTURE, MESH_ID, NETWORK, WORKLOAD_NAME,
#     ISTIO_NAMESPACE, ISTIO_SERVICE, ISTIO_SERVICE_CIDR, ISTIO_SVC_IP, POD_NAMESPACE, SERVICE_ACCOUNT, TRUST_DOMAIN.
#   - 메시·클러스터·망 식별자 대응: MESH_ID -> meshID, CLUSTER_ID -> clusterName, NETWORK -> network.
#   - DNS_CAPTURE='true' -> DNS 질의를 로컬 DNS 프록시로 돌리는 가로채기.
#   - SPIFFE 형식 spiffe://<trust-domain>/ns/<namespace>/sa/<service-account> 에 TRUST_DOMAIN·POD_NAMESPACE·SERVICE_ACCOUNT 값을 대입한 결과.
# 타입 스펙: type-er — 파일 엔티티가 담는 13개 필드와 외부 메시 식별자 개념의 1:1 매핑.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, PAPER2, RULE, KR, MONO

W, H = 960, 600
d = D(W, H, "ISTIO IN ACTION · A0-02 §6",
      "열세 줄 안에 메시·클러스터·망 식별자와 신원 재료가 있다",
      "cluster.env 하나가 워크로드의 메타데이터를 전부 진다. 그중 셋이 메시·클러스터·망을 "
      "가르는 식별자이고, 세 줄은 신원 URI 의 재료다.",
      lead="점선은 변수와 그 변수가 가리키는 것을 잇습니다.")

EX, EY, EW = 24, 116, 488
# 줄 색: ACC = 원문이 짚은 네 줄, INFO = 식별자 셋 중 나머지(MESH_ID), OK = SPIFFE ID 재료 셋
ROWS = [
    ("ISTIO_META_AUTO_REGISTER_GROUP", "'forum'", ACC),
    ("ISTIO_META_CLUSTER_ID", "'west-cluster'", ACC),
    ("ISTIO_META_DNS_CAPTURE", "'true'", ACC),
    ("ISTIO_META_MESH_ID", "'usmesh'", INFO),
    ("ISTIO_META_NETWORK", "'vm-network'", ACC),
    ("ISTIO_META_WORKLOAD_NAME", "'forum'", None),
    ("ISTIO_NAMESPACE", "'forum-services'", None),
    ("ISTIO_SERVICE", "'forum.forum-services'", None),
    ("ISTIO_SERVICE_CIDR", "'*'", None),
    ("ISTIO_SVC_IP", "'138.91.249.118'", None),
    ("POD_NAMESPACE", "'forum-services'", OK),
    ("SERVICE_ACCOUNT", "'forum-sa'", OK),
    ("TRUST_DOMAIN", "'cluster.local'", OK),
]
HH, RH = 48, 28
EH = HH + RH * len(ROWS) + 12
d.box(EX, EY, EW, EH, PAPER2, RULE, 1.0, 6)
d.line(EX, EY + HH, EX + EW, EY + HH, RULE, 0.9)
d.t(EX + 16, EY + 20, "FILE · VM 로컬", 11, SOFT, MONO, "start", 600)
d.t(EX + 16, EY + 40, "cluster.env", 14, INK, MONO, "start", 600)
for i, (k, v, col) in enumerate(ROWS):
    y = EY + HH + 20 + i * RH
    d.t(EX + 16, y, k, 11, col or MUTED, MONO, "start", 600 if col else 400)
    d.t(EX + 312, y, v, 11, INK if col else MUTED, MONO, "start")

MX, MW, BH = 592, 344, 60
def row_y(i): return EY + HH + 20 + i * RH

d.t(MX, 132, "변수가 가리키는 것", 13, INFO, KR, "start", 600)
# (제목, 설명, 줄 번호, 색, 상자 y, 세로선 x) — 상자는 줄 순서대로 쌓아 선이 서로 가로지르지 않게 한다
MAP = [
    ("clusterName", "메시 안에서 클러스터 구분", 1, INFO, 148, 568),
    ("DNS_CAPTURE = 'true'", "DNS 질의를 로컬 DNS 프록시로 돌림", 2, ACC, 216, 556),
    ("meshID", "하나의 메시로 묶는 값", 3, INFO, 284, 544),
    ("network", "같은 망이면 직접 통신", 4, INFO, 352, 532),
]
for name, sub, src_i, col, y, legx in MAP:
    d.tone(MX, y, MW, BH, col, 6, "12", 1.2)
    d.t(MX + 16, y + 24, name, 13 if col == INFO else 12, col, MONO, "start", 600)
    d.t(MX + 16, y + 47, sub, 13, MUTED, KR, "start")
    sy, ty = row_y(src_i) - 4, y + BH / 2
    d.path(f"M {EX + EW} {sy} L {legx} {sy} L {legx} {ty} L {MX - 2} {ty}",
           col, 1.2, m="info" if col == INFO else "acc", dash="4 3")

# SPIFFE ID 조합: 세 줄에서 모아 상자 하나로
d.tone(MX, 452, MW, 72, OK, 6, "12", 1.2)
d.t(MX + 16, 476, "SPIFFE ID 조합", 13, OK, KR, "start", 600)
d.t(MX + 16, 506, "spiffe://cluster.local/ns/forum-services/sa/forum-sa", 10, INK, MONO, "start")
for i in (10, 11, 12):
    yy = row_y(i) - 4
    d.line(EX + EW, yy, 540, yy, OK, 1.2, "4 3")
d.line(540, row_y(10) - 4, 540, row_y(12) - 4, OK, 1.2, "4 3")
d.arrow([(540, 488), (MX - 2, 488)], OK, "ok", 1.2, "4 3")

d.legend(560, [("원문이 짚은 네 줄", ACC), ("메시·클러스터·망 식별자", INFO), ("SPIFFE ID 재료 셋", OK)])
d.save("a0-02.cluster-env.svg")
print("ok cluster-env")
