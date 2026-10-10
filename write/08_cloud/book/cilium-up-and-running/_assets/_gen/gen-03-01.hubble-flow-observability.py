# 타입 스펙: type-data-flow — 노드별 Hubble 서버의 흐름이 Relay 로 모여 hubble observe·UI 로 나가고, 같은 흐름 한 줄이 끝까지 따라간다.
# 사실 출처: cil3.txt 줄 957~1110 (cilium hubble port-forward 127.0.0.1:4245, hubble list nodes 1.05·1.06·4.32 flows/s, policy-verdict:none INGRESS DENIED ID:8087→ID:5834), cil3.txt 줄 1160 (UI localhost:12000), docs.cilium.io/en/stable/observability/hubble/setup/ (Relay Service :80, 노드 :4244).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 484
d = D(W, H, "CILIUM UP AND RUNNING · 03-01 §6", "노드의 흐름이 Relay 를 거쳐 한 화면으로 모인다",
      "Hubble 서버가 노드마다 흐름을 쥐고 Relay 가 세 노드를 묶는다",
      "정책 판정은 흐름 한 줄에 verdict 로 남는다")

Y0 = 104
# 노드별 Hubble 서버
nodes = [("kind-control-plane", "1.05"), ("kind-worker", "1.06"), ("kind-worker2", "4.32")]
XN, WN = 24, 232
for i, (name, rate) in enumerate(nodes):
    y = Y0 + i * 88
    d.box(XN, y, WN, 72, PAPER2, RULE, sw=0.9, r=6)
    d.t(XN + 14, y + 26, name, 12, INK, MONO, "start", 600)
    d.t(XN + 14, y + 50, f"{rate} flows/s", 11, MUTED, MONO, "start")
    d.chip(XN + WN - 44, y + 46, ":4244", INFO, size=11)
# Relay
XR, WR = 340, 232
d.tone(XR, Y0, WR, 240, INFO, r=6, op="10", sw=1.2)
d.t(XR + WR / 2, Y0 + 32, "hubble-relay", 13, INFO, MONO, "middle", 600)
d.t(XR + WR / 2, Y0 + 56, "Deployment", 12, MUTED, KR, "middle")
d.line(XR + 14, Y0 + 72, XR + WR - 14, Y0 + 72, RULE, 0.6)
d.chip(XR + WR / 2, Y0 + 104, "Service :80", INFO, size=11)
d.chip(XR + WR / 2, Y0 + 140, "Pod :4245", INFO, size=11)
d.t(XR + WR / 2, Y0 + 184, "Connected Nodes", 11, MUTED, MONO, "middle")
d.t(XR + WR / 2, Y0 + 208, "3/3", 13, OK, MONO, "middle", 600)
# 클라이언트
XC, WC = 656, 240
d.box(XC, Y0, WC, 112, PAPER2, RULE, sw=0.9, r=6)
d.t(XC + 14, Y0 + 28, "hubble observe", 12, WARN, MONO, "start", 600)
d.t(XC + 14, Y0 + 56, "127.0.0.1:4245", 11, INK, MONO, "start")
d.t(XC + 14, Y0 + 84, "cilium hubble port-forward", 11, MUTED, MONO, "start")
d.box(XC, Y0 + 128, WC, 112, PAPER2, RULE, sw=0.9, r=6)
d.t(XC + 14, Y0 + 156, "Hubble UI", 12, OK, MONO, "start", 600)
d.t(XC + 14, Y0 + 184, "localhost:12000", 11, INK, MONO, "start")
d.t(XC + 14, Y0 + 212, "cilium hubble ui", 11, MUTED, MONO, "start")
# 연결선
for i in range(3):
    y = Y0 + i * 88 + 36
    d.arrow([(XN + WN, y), (XR, y)], INFO, "info", 1.3)
d.arrow([(XR + WR, Y0 + 56), (XC, Y0 + 56)], WARN, "warn", 1.4)
d.arrow([(XR + WR, Y0 + 184), (XC, Y0 + 184)], OK, "ok", 1.4)

# 흐름 한 줄
yf = Y0 + 240 + 32
d.arrow([(XR + WR / 2, Y0 + 240), (XR + WR / 2, yf - 2)], ACC, "acc", 1.4, "4 4")
d.tone(XN, yf, 872, 80, ACC, r=6, op="12", sw=1.4)
d.t(XN + 14, yf + 26, "default/unauthorized-client:41212 (ID:8087) <> default/nginx-deployment-979f5455f-bnxh7:80 (ID:5834)", 11, INK, MONO, "start")
d.t(XN + 14, yf + 56, "policy-verdict:none INGRESS DENIED (TCP Flags: SYN)", 11, BAD, MONO, "start", 600)

d.save("03-01.hubble-flow-observability.svg")
