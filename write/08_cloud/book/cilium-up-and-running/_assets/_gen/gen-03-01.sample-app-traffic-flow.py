# 타입 스펙: type-data-flow — netshoot-client 의 요청이 서비스 IP 에서 백엔드 Pod 로 나뉘고, 응답 출발지가 서비스 IP 로 돌아오는 경로.
# 사실 출처: cil3.txt 줄 463~705 (netshoot-client 10.244.1.67 kind-worker, nginx 10.244.2.127·10.244.2.189 kind-worker2, nginx-service 10.96.242.74, EndpointSlice nginx-service-66q4l, kube-proxy DaemonSet 3/3), docs.cilium.io/en/stable/network/kubernetes/kubeproxy-free/ (kubeProxyReplacement 기본 false).
import sys
sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, SOFT, MUTED, INK, PAPER, PAPER2, RULE, KR, MONO

W, H = 920, 376
d = D(W, H, "CILIUM UP AND RUNNING · 03-01 §4", "서비스 IP 로 보낸 요청이 Pod 로 나뉜다",
      "클라이언트는 ClusterIP 만 알고 Cilium 이 백엔드를 고른다",
      "응답의 출발지는 서비스 IP 로 되돌려진다")

Y0, HN = 104, 240
# 왼쪽 노드
XL, WL = 24, 364
d.box(XL, Y0, WL, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XL + 14, Y0 + 24, "kind-worker", 12, INFO, MONO, "start", 600)
d.tone(XL + 14, Y0 + 40, WL - 28, 64, INFO, r=6, op="10", sw=1.0)
d.t(XL + 26, Y0 + 62, "netshoot-client", 12, INK, MONO, "start", 600)
d.t(XL + 26, Y0 + 84, "10.244.1.67", 11, INFO, MONO, "start")
d.tone(XL + 14, Y0 + 120, WL - 28, 100, ACC, r=6, op="12", sw=1.4)
d.t(XL + 26, Y0 + 142, "Cilium eBPF", 12, ACC, KR, "start", 600)
d.t(XL + 26, Y0 + 168, "10.96.242.74:80", 11, INK, MONO, "start", 600)
d.t(XL + 26, Y0 + 192, "→ 10.244.2.127 · 10.244.2.189", 11, MUTED, MONO, "start")
d.t(XL + WL - 26, Y0 + 142, "kube-proxy 3/3 · 미사용", 12, SOFT, KR, "end")
# 오른쪽 노드
XR, WR = 532, 364
d.box(XR, Y0, WR, HN, PAPER2, RULE, sw=0.9, r=8)
d.t(XR + 14, Y0 + 24, "kind-worker2", 12, OK, MONO, "start", 600)
d.t(XR + WR - 14, Y0 + 24, "nginx-service", 11, MUTED, MONO, "end")
for j, ip in enumerate(["10.244.2.127", "10.244.2.189"]):
    yy = Y0 + 40 + j * 92
    d.tone(XR + 36, yy, WR - 50, 80, OK, r=6, op="10", sw=1.0)
    d.t(XR + 48, yy + 28, "nginx-deployment Pod", 12, INK, KR, "start", 600)
    d.t(XR + 48, yy + 52, ip, 11, OK, MONO, "start")
    d.t(XR + 48, yy + 70, ["최초 1개", "scale 로 추가"][j], 12, MUTED, KR, "start")
    d.arrow([(XR + 6, yy + 40), (XR + 34, yy + 40)], ACC, "acc", 1.4)
# 노드 사이 경로: 요청은 줄기에서 두 Pod 로 갈라지고 응답은 Pod 에서 돌아온다
ym_req, ym_res = Y0 + 150, Y0 + 190
d.arrow([(XL + WL - 14, ym_req), (XR + 6, ym_req)], ACC, "acc", 1.6)
d.line(XR + 6, Y0 + 80, XR + 6, Y0 + 172, ACC, 1.4)
d.arrow([(XR + 36, ym_res), (XL + WL - 14, ym_res)], OK, "ok", 1.4, "5 4")
d.t((XL + WL + XR) / 2, ym_req - 12, "VXLAN", 11, ACC, MONO, "middle", 600)
d.t((XL + WL + XR) / 2, ym_res + 22, "src 10.96.242.74", 10, OK, MONO, "middle")

d.save("03-01.sample-app-traffic-flow.svg")
