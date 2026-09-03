# 12-01 §5 설치가 붙이는 식별자 셋 — 원문 12.3.4 의 IstioOperator 정의와 네임스페이스 라벨.
# 본문(원문 12.3.4): meshID 는 이 설치가 속한 메시를 식별한다. 쿠버네티스 클러스터는 여러 테넌트와 팀을
#       걸칠 수 있고 Istio 는 한 클러스터 안에 메시를 여럿 설치할 수 있게 하므로, meshID 로 어느 메시인지를
#       가린다. multiCluster.clusterName 은 멀티 클러스터 메시 안에서 클러스터를 식별하고, network 는 이
#       설치가 일어나는 네트워크다. 네트워크 정보는 istio-system 네임스페이스에
#       topology.istio.io/network 라벨로도 붙인다.
# 포함 관계는 *설치 하나를 기준으로* 성립한다 — 한 설치는 메시 하나에 속하고, 클러스터 하나이며, 네트워크 하나 위에 선다.
#       네트워크가 클러스터 안에 갇힌다는 뜻은 아니다. 원문 12.2.3 은 클러스터들이 하나의 네트워크를 공유하는
#       평평한 망(flat network)도 든다. 그 경우 동서 게이트웨이 없이 IP 로 곧장 붙는다.
# 타입 스펙: type-nested — 포함으로 표현하는 계층. 링 3(3~5), 안쪽으로 갈수록 획이 진해지고 채움이 짙어진다.
#           링 라벨은 왼쪽 위 종이색 마스크 위 mono eyebrow, coral 은 가장 안쪽 초점 하나에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, RULE, KR, MONO

W, H = 1160, 640
d = D(W, H, "ISTIO IN ACTION · 12-01 §5",
      "식별자 셋이 어디까지가 한 몸인지를 정한다",
      "같은 meshID 를 가진 설치들이 하나의 메시가 되고, 그 안에서 clusterName 이 클러스터를 가르며, "
      "network 가 어느 망에 있는지를 알린다. 색이 붙은 가장 안쪽이 동서 게이트웨이를 쓸지 정하는 값이다.",
      "network 가 같으면 IP 로 곧장 붙고 다르면 관문을 거칩니다")

def ring(x, y, w, h, tag, sub, stroke, fill, focal=False):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" '
               f'stroke="{stroke}" stroke-width="{1.4 if focal else 1.0}"/>')
    tw = len(tag) * 6 + 16
    d.o.append(f'<rect x="{x + 20}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 28, y + 3, tag, 11, ACC if focal else SOFT, MONO, "start", 600)
    d.t(x + 28, y + 30, sub, 11, ACC if focal else MUTED, KR, "start")

ring(72, 128, 1016, 372, "MESHID = USMESH · 설치 하나 기준", "같은 값을 쓴 설치들이 하나의 메시가 된다", f"{INK}30", f"{INK}04")
ring(116, 184, 928, 280, "CLUSTERNAME = WEST-CLUSTER", "메시 안에서 클러스터를 가른다 · 원격 시크릿의 이름이 된다", MUTED, f"{INK}07")
ring(160, 240, 840, 184, "NETWORK = WEST-NETWORK", "같은 망이면 IP 로, 다르면 동서 게이트웨이로", ACC, f"{ACC}0E", focal=True)

items = [("IstioOperator", "values.global.multiCluster"),
         ("네임스페이스 라벨", "topology.istio.io/network"),
         ("게이트웨이 환경변수", "ISTIO_META_REQUESTED_NETWORK_VIEW")]
for i, (name, sub) in enumerate(items):
    x = 196 + i * 268
    d.o.append(f'<rect x="{x}" y="{316}" width="248" height="64" rx="6" fill="{ACC}10" stroke="{ACC}66" stroke-width="1"/>')
    d.t(x + 124, 342, name, 12, INK, KR, "middle", 600)
    d.t(x + 124, 364, sub, 8, MUTED, MONO)

d.t(32, 528, "east 쪽 설치는 clusterName 과 network 만 바꾸고 meshID 는 그대로 둔다 — 그래야 한 메시가 된다", 11, SOFT, KR, "start")
d.t(32, 552, "네트워크 지형을 MeshNetwork 로도 적을 수 있지만 저자는 드물고 고급인 경우에만 남은 옛 설정이라 적는다", 11, MUTED, KR, "start")
d.t(32, 576, "이 포함은 설치 하나를 기준으로 한 것이다 — 클러스터들이 하나의 평평한 망을 공유하면 network 는 클러스터 밖에서 겹친다", 11, SOFT, KR, "start")
d.legend(600, [("게이트웨이 경유 여부를 정하는 값", ACC), ("그 위를 감싸는 식별자", MUTED)])
d.save("12-01.identity-scopes.svg")
