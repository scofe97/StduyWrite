# 12-01 §4 공통 루트에서 갈라진 중간 CA — 원문 그림 12.8 · 12.10.
# 본문(원문 12.2.4 · 12.3.3): Istio 는 설치할 때 CA 를 만들어 istio-ca-secret 이라는 시크릿으로 두는데,
#       설치 네임스페이스에 cacerts 라는 시크릿을 두면 그것을 대신 집어 쓴다. cacerts 는 네 파일로 이루어진다 —
#       ca-cert.pem(중간 CA 인증서), ca-key.pem(중간 CA 개인키), root-cert.pem(그 중간 CA 를 발급한 루트 CA 의
#       인증서), cert-chain.pem(중간 CA 인증서와 루트 인증서를 이어 붙인 신뢰 사슬). 루트 CA 는 자기 중간 CA 가
#       발급한 인증서를 검증해 주므로 클러스터 사이 상호 신뢰의 열쇠가 된다.
#       루트 CA 의 개인키는 클러스터 밖에 안전하게 둔다.
# 타입 스펙: type-tree — 뿌리 하나(루트 CA)에서 중간 CA 둘로 갈라지고 그 아래 시크릿 내용이 잎이 된다.
#           깊이 3, 최대 폭 2, 연결선은 직각 엘보(대각선 금지), coral 은 한 곳에만.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 1160, 640
d = D(W, H, "ISTIO IN ACTION · 12-01 §4",
      "같은 뿌리에서 갈라져야 서로를 알아본다",
      "두 클러스터에 각자 다른 중간 CA 를 꽂되 같은 루트가 서명한 것으로 둔다. 색이 붙은 뿌리가 "
      "양쪽 워크로드 인증서를 함께 검증해 주는 자리이고, 그 개인키만 클러스터 밖에 남는다.",
      "쉬운 방법이지만 중간 CA 가 새면 탐지될 때까지 서명이 통합니다")

NW, NH = 380, 56
def node(x, y, name, sub, focal=False, w=NW, h=NH):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 24, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 44, sub, 9, MUTED, MONO)

ROOT_X, ROOT_Y = 390, 112
node(ROOT_X, ROOT_Y, "루트 CA", "개인키는 클러스터 밖에 둔다", focal=True)

BUS_Y = 216
XS = [88, 692]
MID_Y, LEAF_Y = 256, 372
d.line(ROOT_X + NW / 2, ROOT_Y + NH, ROOT_X + NW / 2, BUS_Y, ACC, 1.4)
d.line(XS[0] + NW / 2, BUS_Y, XS[1] + NW / 2, BUS_Y, ACC, 1.4)
for x in XS:
    d.line(x + NW / 2, BUS_Y, x + NW / 2, MID_Y, ACC, 1.4)
    d.line(x + NW / 2, MID_Y + NH, x + NW / 2, LEAF_Y, MUTED, 1.0)

node(XS[0], MID_Y, "west 의 중간 CA", "cacerts · istio-system")
node(XS[1], MID_Y, "east 의 중간 CA", "cacerts · istio-system")

def leaf(x, y, lines):
    h = 24 + len(lines) * 22
    d.box(x, y, NW, h, PAPER2, RULE, 1.0, 6)
    for j, ln in enumerate(lines):
        d.t(x + 16, y + 30 + j * 22, ln, 10, MUTED, MONO, "start")

files = ["ca-cert.pem      중간 CA 인증서",
         "ca-key.pem       중간 CA 개인키",
         "root-cert.pem    루트 CA 인증서",
         "cert-chain.pem   둘을 이은 신뢰 사슬"]
leaf(XS[0], LEAF_Y, files)
leaf(XS[1], LEAF_Y, files)

d.t(32, 512, "cacerts 를 두지 않으면 Istio 가 스스로 CA 를 만들어 istio-ca-secret 에 넣고, 그러면 두 클러스터의 뿌리가 달라진다", 11, SOFT, KR, "start")
d.t(32, 536, "더 안전한 쪽은 외부 CA 를 붙이는 것이다 — istiod 가 등록 기관이 되어 CSR 을 승인만 한다", 11, MUTED, KR, "start")
d.legend(560, [("양쪽을 함께 검증하는 뿌리", ACC), ("클러스터마다 다른 중간 CA", MUTED)])
d.save("12-01.common-trust.svg")
