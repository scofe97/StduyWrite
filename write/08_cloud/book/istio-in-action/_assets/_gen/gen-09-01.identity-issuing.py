# 09-01 §1 istiod 가 발급한 문서로 워크로드가 서로를 알아본다.
# 본문(저자 9.1.5): SPIFFE 신원은 spiffe://trust-domain/path 형식의 URI 이고, path 를 무엇으로 채울지는
#       규격이 열어 두었다. Istio 는 워크로드가 띄워진 서비스 어카운트로 채운다. 그 URI 를 X.509 에 실은 것이 SVID.
# 저자가 openssl 로 확인한 값(SAN 의 URI)과 루트 인증서 경로를 그대로 라벨에 쓴다.
# 타입 스펙: type-architecture — 구성요소(istiod CA · webapp 사이드카 · catalog 사이드카)와 연결.
#           존 2(istio-system · istioinaction), 초점 1(상호 인증 경로).
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, INFO, PAPER, PAPER2, RULE, KR, MONO

W, H = 1200, 620
d = D(W, H, "ISTIO IN ACTION · 09-01 §1",
      "신원이 네트워크 위치에서 문서로 옮겨간다",
      "컨트롤 플레인이 워크로드마다 SVID 를 발급하고, 사이드카끼리 그 문서로 서로를 확인한다. "
      "IP 는 어디에도 쓰이지 않는다. 색이 붙은 경로가 그 확인이 일어나는 자리다.",
      "path 를 무엇으로 채울지는 규격이 열어 두었고 Istio 는 서비스 어카운트를 넣습니다")

def zone(x, y, w, h, label):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{INK}05" '
               f'stroke="{INK}33" stroke-width="1" stroke-dasharray="4 4"/>')
    tw = len(label) * 6 + 12
    d.o.append(f'<rect x="{x + 12}" y="{y - 7}" width="{tw}" height="14" fill="{PAPER}"/>')
    d.t(x + 18, y + 3, label, 8, SOFT, MONO, "start", 600)

def node(x, y, w, h, name, sub, focal=False):
    if focal:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{ACC}12" stroke="{ACC}" stroke-width="1.4"/>')
    else:
        d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 30, name, 13, ACC if focal else INK, KR, "middle", 600)
    d.t(x + w / 2, y + 50, sub, 9, MUTED, MONO)

zone(72, 128, 336, 116, "ISTIO-SYSTEM")
zone(496, 128, 632, 180, "ISTIOINACTION")

node(104, 156, 272, 68, "istiod", "certificate authority")
node(528, 156, 264, 68, "webapp", "sa/webapp")
node(832, 156, 264, 68, "catalog", "sa/catalog")

# 발급 경로 — 컨트롤 플레인에서 두 워크로드로 내려가는 버스
d.path("M 240 224 L 240 280 L 660 280 L 660 226", INFO, 1.2, m="ar")
d.path("M 660 280 L 964 280 L 964 226", INFO, 1.2, m="ar")
d.t(276, 260, "SVID 발급 · 순환", 10, INFO, KR, "start", 600)

# 상호 인증 — 두 사이드카 사이
d.path("M 792 190 L 828 190", ACC, 1.6, m="acc")
d.t(810, 172, "mTLS", 10, ACC, MONO, "middle", 600)

# SVID 의 내용물 — 존 밖으로 내려 둔다
d.box(496, 348, 600, 112, PAPER2, RULE, 1.0, 6)
d.t(516, 374, "catalog 의 X.509 안에 든 것", 11, ACC, KR, "start", 600)
d.t(516, 398, "X509v3 Subject Alternative Name: critical", 10, MUTED, MONO, "start")
d.t(516, 420, "URI:spiffe://cluster.local/ns/istioinaction/sa/catalog", 10, INK, MONO, "start")
# URI 는 trust-domain 과 path 둘로 갈린다. ns/sa 는 path 의 내부 구조이지 세 번째 조각이 아니다.
# 라벨 위치는 mono 10px 문자폭 6px 로 계산했다.
d.t(633, 442, "trust-domain", 9, SOFT, MONO)
d.t(777, 442, "path — Istio 는 서비스 어카운트로 채운다", 9, ACC, KR)
d.line(1040, 224, 1040, 348, MUTED, 1.0, "3 5")

d.t(32, 496, "인증서 발급과 순환을 사람이 하던 시절의 실수가 값비싼 장애로 이어졌다 — 자동화는 편의가 아니다", 11, SOFT, KR, "start")
d.t(32, 520, "검증은 /var/run/secrets/istio/root-cert.pem 으로 하고, 서명이 맞으면 한 줄짜리 확인이 나온다", 11, MUTED, KR, "start")
d.legend(556, [("워크로드끼리 서로를 확인하는 자리", ACC), ("컨트롤 플레인이 내려보내는 것", INFO)])
d.save("09-01.identity-issuing.svg")
