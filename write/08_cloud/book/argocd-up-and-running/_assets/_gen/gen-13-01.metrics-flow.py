# 13-01 §1 — 구성요소 네 곳이 각자 포트로 메트릭을 내고, ServiceMonitor 가 그 Service 를 골라 Prometheus 가 긁고, Grafana 가 조회한다.
# 본문 근거: 이 노트 ### 1 「메트릭과 대시보드」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 install.yaml 을 설치하고 클러스터 안 curl 파드로 다섯 Service 의 /metrics 가 HTTP 200 임을 확인했다. 포트는 install.yaml 의 Service 정의에서 읽었다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/metrics.md (Prometheus Operator 절), manifests/install.yaml.
# 타입 스펙: type-architecture — 왼쪽 구성요소 네 곳에서 오른쪽 조회까지 왼쪽에서 오른쪽 한 방향.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 480
d = D(W, H, "ARGO CD UP AND RUNNING · 13-01 §1",
      "메트릭이 Grafana 에 닿기까지",
      "왼쪽의 대표 구성요소 네 곳이 각자 포트로 /metrics 를 내보낸다(알림 컨트롤러 등 나머지도 같은 방식). ServiceMonitor 는 라벨로 그 Service 들을 골라 Prometheus 에 알리고, Prometheus 가 주기적으로 긁어 저장한다. "
      "Grafana 는 Prometheus 를 조회해 Argo CD 대시보드를 그린다.",
      "구성요소마다 다른 포트를 Service 가 열어 둡니다")

X, BW, BH = 24, 300, 64
ys = [110, 188, 266, 344]
rows = [("application-controller", "Service argocd-metrics", "8082"),
        ("argocd-server", "Service argocd-server-metrics", "8083"),
        ("repo-server", "Service argocd-repo-server", "8084"),
        ("applicationset-controller", "Service argocd-applicationset-controller", "8080")]
for y, (name, svc, port) in zip(ys, rows):
    d.tone(X, y, BW, BH, INFO, 6, "14", 1.1)
    d.t(X + 16, y + 26, name, 12.5, INK, KR, "start", 600)
    d.t(X + 16, y + 48, svc, 11, MUTED, MONO, "start")
    d.t(X + BW - 16, y + 26, port, 12.5, INK, MONO, "end", 600)

SM_X, SM_W = 372, 140
SM_Y, SM_H = 150, 242
d.box(SM_X, SM_Y, SM_W, SM_H, PAPER2, RULE, 1.0)
d.t(SM_X + SM_W / 2, SM_Y + 36, "ServiceMonitor", 12.5, INK, KR, "middle", 600)
d.t(SM_X + SM_W / 2, SM_Y + 62, "구성요소마다 하나", 12, MUTED)
d.t(SM_X + SM_W / 2, SM_Y + 118, "selector 로", 12, MUTED)
d.t(SM_X + SM_W / 2, SM_Y + 138, "Service 선택", 12, MUTED)
d.t(SM_X + SM_W / 2, SM_Y + 194, "release 라벨", 11.5, MUTED, MONO)
BUS = SM_X - 24
for y in ys:
    d.path(f"M {X + BW + 2} {y + BH / 2} L {BUS} {y + BH / 2}", MUTED, 1.3)
d.path(f"M {BUS} {ys[0] + BH / 2} L {BUS} {ys[-1] + BH / 2}", MUTED, 1.3)
d.path(f"M {BUS} {SM_Y + SM_H / 2} L {SM_X - 2} {SM_Y + SM_H / 2}", MUTED, 1.3, m="ar")

P_X, P_W = 556, 132
d.tone(P_X, SM_Y + 72, P_W, 98, ACC, 6, "14", 1.4)
d.t(P_X + P_W / 2, SM_Y + 108, "Prometheus", 12.5, INK, KR, "middle", 600)
d.t(P_X + P_W / 2, SM_Y + 134, "긁어서 저장", 12, MUTED)
d.path(f"M {SM_X + SM_W + 2} {SM_Y + 121} L {P_X - 2} {SM_Y + 121}", MUTED, 1.4, m="ar")

G_X, G_W = 744, 112
d.tone(G_X, SM_Y + 72, G_W, 98, OK, 6, "14", 1.2)
d.t(G_X + G_W / 2, SM_Y + 108, "Grafana", 12.5, INK, KR, "middle", 600)
d.t(G_X + G_W / 2, SM_Y + 134, "대시보드", 12, MUTED)
d.path(f"M {P_X + P_W + 2} {SM_Y + 121} L {G_X - 2} {SM_Y + 121}", MUTED, 1.4, m="ar")

d.legend(440, [("메트릭 노출", INFO), ("선택", PAPER2), ("수집", ACC), ("시각화", OK)])
d.save("13-01.metrics-flow.svg")
