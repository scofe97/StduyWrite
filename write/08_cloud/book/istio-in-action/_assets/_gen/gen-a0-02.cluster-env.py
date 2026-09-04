# a0-02 §6 cluster.env 의 값이 가리키는 것.
# 본문(부록 E 의 출력 그대로): 13 줄. 저자가 주석으로 짚는 넷은 자동 등록 그룹 · 인증 대상 클러스터 ·
#       DNS 가로채기 · 소속 망. 12 장의 meshID · clusterName · network 가 여기 환경변수로 내려온다.
# 타입 스펙: type-er — 파일 하나가 필드 묶음을 담고 그 필드가 바깥 개념과 짝을 이루는 것이 논점이다.
#           엔티티 상자에 필드를 나열하고 관계선으로 대응을 잇는다.
#           축약: 13 줄 전부를 적되 저자가 주석을 단 넷만 색으로 가른다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER2, RULE, KR, MONO

W, H = 1000, 620
d = D(W, H, "ISTIO IN ACTION · A0-02 §6",
      "열세 줄 안에 12 장의 식별자 셋이 들어 있다",
      "파일 하나가 워크로드의 메타데이터를 전부 진다. 그중 셋이 12 장에서 메시와 클러스터와 망을 "
      "가르던 식별자이고, 색이 붙은 줄이 저자가 주석으로 짚은 넷이다.",
      "TRUST_DOMAIN 과 네임스페이스와 서비스 어카운트를 붙이면 9 장의 SPIFFE ID 가 됩니다")

EX, EY, EW = 28, 128, 500
ROWS = [
    ("ISTIO_META_AUTO_REGISTER_GROUP", "'forum'", True),
    ("ISTIO_META_CLUSTER_ID", "'west-cluster'", True),
    ("ISTIO_META_DNS_CAPTURE", "'true'", True),
    ("ISTIO_META_MESH_ID", "'usmesh'", False),
    ("ISTIO_META_NETWORK", "'vm-network'", True),
    ("ISTIO_META_WORKLOAD_NAME", "'forum'", False),
    ("ISTIO_NAMESPACE", "'forum-services'", False),
    ("ISTIO_SERVICE", "'forum.forum-services'", False),
    ("ISTIO_SERVICE_CIDR", "'*'", False),
    ("ISTIO_SVC_IP", "'138.91.249.118'", False),
    ("POD_NAMESPACE", "'forum-services'", False),
    ("SERVICE_ACCOUNT", "'forum-sa'", False),
    ("TRUST_DOMAIN", "'cluster.local'", False),
]
HH, RH = 44, 24
EH = HH + RH * len(ROWS) + 12
d.box(EX, EY, EW, EH, PAPER2, RULE, 1.0, 6)
d.line(EX, EY + HH, EX + EW, EY + HH, RULE, 0.9)
d.t(EX + 16, EY + 20, "FILE · VM 로컬", 11, SOFT, MONO, "start", 600)
d.t(EX + 16, EY + 38, "cluster.env", 13, INK, MONO, "start", 600)
for i, (k, v, marked) in enumerate(ROWS):
    y = EY + HH + 18 + i * RH
    d.t(EX + 16, y, k, 11, ACC if marked else MUTED, MONO, "start", 600 if marked else 400)
    d.t(EX + 316, y, v, 11, INK if marked else MUTED, MONO, "start")

# 대응선은 출발 줄의 실제 y 에서 뽑는다. 임의의 y 로 그으면 이 도식의 논점인
# "어느 줄이 어느 식별자인가" 가 틀린 채로 그려진다. 줄 y = EY + HH + 18 + i * RH.
# 오른쪽 상자는 출발 줄 순서(CLUSTER_ID 1 · MESH_ID 3 · NETWORK 4)대로 놓아 선이 꼬이지 않게 한다.
MX, MW = 620, 352
def row_y(i): return EY + HH + 18 + i * RH
MAP = [
    ("clusterName", "메시 안에서 클러스터를 가른다", 1, 176, 552),
    ("meshID", "메시 하나로 묶는 값", 3, 272, 568),
    ("network", "같은 망이면 IP 로 곧장 붙는다", 4, 368, 584),
]
for name, sub, src_i, y, legx in MAP:
    d.o.append(f'<rect x="{MX}" y="{y}" width="{MW}" height="64" rx="6" '
               f'fill="{INFO}12" stroke="{INFO}" stroke-width="1.2"/>')
    d.t(MX + 16, y + 26, name, 12, INFO, MONO, "start", 600)
    d.t(MX + 16, y + 46, sub, 11, MUTED, KR, "start")
    sy, ty = row_y(src_i) - 4, y + 32
    d.path(f"M {EX + EW} {sy} L {legx} {sy} L {legx} {ty} L {MX - 2} {ty}",
           INFO, 1.2, m="info", dash="4 3")

d.t(MX, 152, "12 장이 세운 식별자 셋", 12, INFO, KR, "start", 600)
d.t(MX, 460, "DNS_CAPTURE 가 참인 것은 13 장 §5 의", 11, ACC, KR, "start", 600)
d.t(MX, 482, "가로채기를 켜는 스위치다", 11, MUTED, KR, "start")

d.t(28, 540, "저자가 주석으로 짚은 넷 — 자동 등록 그룹 · 인증 대상 클러스터 · DNS 가로채기 · 소속 망", 11, SOFT, KR, "start")
d.legend(560, [("저자가 주석을 단 줄", ACC), ("12 장의 식별자와 짝", INFO)])
d.save("a0-02.cluster-env.svg")
