# 타입 스펙: type-architecture — 인증서 세 개(내부 CA 서명 cilium-io-cert · 내부 CA 번들 · 공개 CA 번들)가 놓인 자리와 검증 방향.
# 사실 출처: Cilium Up and Running 13장 cil13.txt 줄 948-1004(public-ca-bundle·trust-bundle.pem), 1006-1081(internal-ca·cilium-io-cert), 1085-1156(internal-ca-bundle·ca-certificates.crt), 1158-1210(terminatingTLS·originatingTLS) / github.com/cilium/cilium v1.20.2 pkg/policy/api/l4.go
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, INFO, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 480
d = D(W, H, "CILIUM UP AND RUNNING · 13-03 §2", "인증서 세 개와 검증 방향",
      "Pod 는 내부 CA 번들로 Envoy 의 인증서를 검증하고, Envoy 는 공개 CA 번들로 업스트림의 인증서를 검증한다",
      "Pod 는 내부 CA 번들로 Envoy 의 인증서를 검증하고, Envoy 는 공개 CA 번들로 업스트림의 인증서를 검증한다")

X1, W1 = 24, 232
X2, W2 = 316, 280
X3, W3 = 688, 208
NODE_H = 76

# 열 머리
for x, w, nm in ((X1, W1, "test Pod"), (X2, W2, "노드 Envoy"), (X3, W3, "cilium.io")):
    d.box(x, 100, w, 32, PAPER2, RULE, 1.0)
    d.t(x + w / 2, 121, nm, 13, INK, KR, "middle", 600)

# cilium-secrets 네임스페이스 경계 (노드 Envoy 열)
d.o.append(f'<rect x="{X2 - 12}" y="196" width="{W2 + 24}" height="248" rx="8" fill="none" stroke="{MUTED}" stroke-width="1" stroke-dasharray="5 4"/>')
d.t(X2 + 4, 216, "ns cilium-secrets", 12, MUTED, MONO, "start")

# 발급자 → cilium-io-cert (아래로)
d.box(X2, 148, W2, 32, PAPER2, RULE, 0.9)
d.t(X2 + W2 / 2, 169, "ClusterIssuer internal-ca", 12, INK, MONO)

Y_B1, Y_B2 = 224, 352
# 화살표 먼저 (z-order: 선이 상자 뒤)
XS_ARR = X2 + W2 - 60
d.arrow([(XS_ARR, 184), (XS_ARR, 218)], MUTED, "ar", 1.4)
d.t(XS_ARR + 12, 214, "서명", 12, MUTED, KR, "start")
d.arrow([(X1 + W1 + 6, Y_B1 + NODE_H / 2), (X2 - 6, Y_B1 + NODE_H / 2)], OK, "ok", 1.6)
d.t((X1 + W1 + X2) / 2, Y_B1 + NODE_H / 2 - 10, "검증", 12, OK, KR, "middle", 600)
d.path(f"M {X2 + W2 + 6} {Y_B2 + NODE_H / 2} L 640 {Y_B2 + NODE_H / 2} L 640 {Y_B1 + NODE_H / 2} L {X3 - 6} {Y_B1 + NODE_H / 2}", INFO, 1.6, m="info")
d.t(644, Y_B2 + NODE_H / 2 + 22, "검증", 12, INFO, KR, "start", 600)
d.arrow([(X1 + W1 / 2, Y_B2), (X1 + W1 / 2, Y_B1 + NODE_H + 6)], MUTED, "ar", 1.4)
d.t(X1 + W1 / 2 + 14, (Y_B1 + NODE_H + Y_B2) / 2 + 4, "볼륨 마운트", 12, MUTED, KR, "start")

# Pod 쪽
d.tone(X1, Y_B1, W1, NODE_H, OK, op="12", sw=1.2)
d.t(X1 + W1 / 2, Y_B1 + 32, "ca-certificates.crt", 12, INK, MONO, "middle", 600)
d.t(X1 + W1 / 2, Y_B1 + 54, "/etc/ssl/certs/", 12, MUTED, MONO)
d.box(X1, Y_B2, W1, NODE_H, PAPER2, RULE, 0.9)
d.t(X1 + W1 / 2, Y_B2 + 32, "internal-ca-bundle", 12, INK, MONO, "middle", 600)
d.t(X1 + W1 / 2, Y_B2 + 54, "ConfigMap · ca.crt", 12, MUTED, MONO)

# Envoy 쪽 (Secret 둘)
d.tone(X2, Y_B1, W2, NODE_H, ACC, op="12", sw=1.4)
d.t(X2 + W2 / 2, Y_B1 + 30, "cilium-io-cert", 12, INK, MONO, "middle", 600)
d.t(X2 + W2 / 2, Y_B1 + 50, "terminatingTLS · tls.crt · tls.key", 12, MUTED, MONO)
d.box(X2, Y_B2, W2, NODE_H, PAPER2, RULE, 0.9)
d.t(X2 + W2 / 2, Y_B2 + 30, "public-ca-bundle", 12, INK, MONO, "middle", 600)
d.t(X2 + W2 / 2, Y_B2 + 50, "originatingTLS · trust-bundle.pem", 12, MUTED, MONO)

# 업스트림
d.tone(X3, Y_B1, W3, NODE_H, INFO, op="12", sw=1.2)
d.t(X3 + W3 / 2, Y_B1 + 32, "서버 인증서", 12, INK, KR, "middle", 600)
d.t(X3 + W3 / 2, Y_B1 + 54, "공개 CA 서명", 12, MUTED, KR)

d.save("13-03.certificate-trust-model.svg")
