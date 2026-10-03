# 06-03 §3 — Prometheus 는 Service 에서 포트 이름과 번호를 찾고, 메트릭은 파드마다 직접 긁는다.
# 본문 근거: 이 노트 §3 「메트릭 포트가 서비스에 있는 이유」(원서 요지 — 서비스는 포트의 이름표, 실제 메트릭은 각 파드에서).
# 매니페스트 근거: kubeadm manifests.go 의 Service ports dns 53/UDP · dns-tcp 53/TCP · metrics 9153/TCP.
#            파드 IP 는 설명용 예시 값이다.
# 타입 스펙: type-architecture — 구성요소 셋 사이에서 어느 화살표가 실제 데이터를 나르는지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 06-03 §3",
      "포트는 서비스에서 찾고 메트릭은 파드에서 긁는다",
      "서비스로 긁으면 요청마다 다른 파드가 답해 값이 섞인다. 그래서 Prometheus 는 서비스에 적힌 metrics 포트로 "
      "어느 포트를 볼지만 알아내고, 실제 스크레이프는 파드마다 따로 한다.",
      "주황 화살표가 실제로 메트릭이 오가는 길입니다")

d.box(20, 200, 180, 80, PAPER2, RULE, 1.0, 8)
d.t(110, 236, "Prometheus", 14, INK, KR, "middle", 600)
d.t(110, 260, "스크레이프", 12, MUTED, KR)

d.box(300, 104, 260, 136, PAPER2, RULE, 1.0, 8)
d.t(316, 130, "Service kube-dns", 14, INK, KR, "start", 600)
for j, txt in enumerate(["dns 53/UDP", "dns-tcp 53/TCP", "metrics 9153/TCP"]):
    d.t(316, 156 + j * 22, txt, 12, INK if j == 2 else MUTED, MONO, "start", 600 if j == 2 else 400)
d.t(316, 226, "포트의 이름표 노릇", 12, MUTED, KR, "start")
d.path("M 202 222 L 250 222 L 250 186 L 296 186", SOFT, 1.2, m="soft", dash="4 4")

pods = [("coredns 파드 1", "10.244.0.2:9153", 104), ("coredns 파드 2", "10.244.1.3:9153", 196), ("coredns 파드 3", "10.244.2.4:9153", 288)]
for name, ep, y in pods:
    d.box(640, y, 220, 72, PAPER2, RULE, 1.0, 8)
    d.t(656, y + 28, name, 13, INK, KR, "start", 600)
    d.t(656, y + 52, ep, 12, MUTED, MONO, "start")
    d.path(f"M 202 258 L 610 258 L 610 {y + 36} L 636 {y + 36}", ACC, 1.4, m="acc")
d.t(406, 280, "파드마다 직접 긁는다", 13, ACC, KR, "middle", 600)

d.t(20, 392, "서비스로 긁으면 매번 다른 파드가 답한다 · 그래서 파드마다 긁는다", 13, MUTED, KR, "start")
d.t(20, 414, "파드 IP 는 예시 값", 12, SOFT, KR, "start")

d.legend(426, [("실제 스크레이프", ACC)])
d.save("06-03.metrics-port.svg")
