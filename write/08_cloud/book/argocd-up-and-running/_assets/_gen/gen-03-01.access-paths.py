# 03-01 §2 — 브라우저·argocd CLI·REST 클라이언트는 Ingress 를 지나 같은 API server 에 닿고, API server 는 클러스터 리소스를 읽고 쓴다.
# 본문 근거: 이 노트 ### 1 「UI 를 Ingress 로 노출하기」, ### 2 「CLI 와 REST API」.
# 검증 근거: kind v0.31.0(Kubernetes v1.35.0)에 Traefik 차트 42.3.0 과 argo-cd 차트 10.14.0 을 설치하고
#            https://argocd.127.0.0.1.nip.io:8443 으로 UI(HTTP 200), argocd login --insecure --grpc-web 성공, POST /api/v1/session 으로 받은 토큰의 Bearer 호출 성공을 확인.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/architecture.md(API server 는 Web UI·CLI·CI/CD 시스템이 쓰는 gRPC/REST API 를 연다),
#            ingress.md(TLS 를 Ingress 에서 끝내려면 server.insecure), argo-helm argo-cd-10.14.0 templates/argocd-server/ingress.yaml(insecure 일 때 백엔드 포트 80).
# 타입 스펙: type-architecture — 입구 셋이 한 서버로 모이는 수렴형.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 440
d = D(W, H, "ARGO CD UP AND RUNNING · 03-01 §2",
      "UI·CLI·REST API 가 같은 API server 로 모이는 길",
      "왼쪽의 세 입구인 브라우저, argocd CLI, REST 클라이언트가 가운데의 Ingress 컨트롤러를 지나 하나의 API server 에 닿는 구성도다. "
      "API server 는 오른쪽의 클러스터 리소스인 Application, ConfigMap, Secret 을 읽고 쓴다.",
      "세 입구는 프로토콜만 다르고 닿는 서버는 하나입니다")

ROW_Y = (110, 198, 286)
EB_X, EB_W, EB_H = 24, 190, 74
ING_X, ING_W = 290, 150
API_X, API_W = 510, 150
RES_X, RES_W = 730, 138
TOP, BOT = 110, 360


def tall(x, w, c, title, subs, op="14", sw=1.2):
    d.tone(x, TOP, w, BOT - TOP, c, 6, op, sw)
    d.t(x + w / 2, TOP + 34, title, 13, INK, KR, "middle", 600)
    for i, s in enumerate(subs):
        d.t(x + w / 2, TOP + 60 + i * 22, s, 11.5, MUTED, KR)


entrances = [
    ("브라우저", "UI · HTTPS"),
    ("argocd CLI", "gRPC-web"),
    ("REST 클라이언트", "REST · Bearer 토큰"),
]
for y, (title, sub) in zip(ROW_Y, entrances):
    d.tone(EB_X, y, EB_W, EB_H, INFO, 6, "14", 1.1)
    d.t(EB_X + EB_W / 2, y + 31, title, 12.5, INK, KR, "middle", 600)
    d.t(EB_X + EB_W / 2, y + 54, sub, 11.5, MUTED, KR)
    d.path(f"M {EB_X + EB_W + 2} {y + EB_H / 2} L {ING_X - 2} {y + EB_H / 2}", MUTED, 1.4, m="ar")

tall(ING_X, ING_W, SOFT, "Ingress 컨트롤러", ["TLS 종료", "Host 헤더로 라우팅"])
d.path(f"M {ING_X + ING_W + 2} {(TOP + BOT) / 2} L {API_X - 2} {(TOP + BOT) / 2}", MUTED, 1.4, m="ar")
d.t((ING_X + ING_W + API_X) / 2, (TOP + BOT) / 2 - 10, "포트 80", 11.5, MUTED, KR)

tall(API_X, API_W, ACC, "API server", ["gRPC · REST", "웹 UI 서빙"], "14", 1.4)
d.path(f"M {API_X + API_W + 2} {(TOP + BOT) / 2} L {RES_X - 2} {(TOP + BOT) / 2}", MUTED, 1.4, m="ar")

d.tone(RES_X, TOP, RES_W, BOT - TOP, SOFT, 6, "14", 1.1)
d.t(RES_X + RES_W / 2, TOP + 34, "클러스터 리소스", 13, INK, KR, "middle", 600)
for i, n in enumerate(["Application", "ConfigMap", "Secret"]):
    y = TOP + 62 + i * 52
    d.box(RES_X + 14, y, RES_W - 28, 38, PAPER2, RULE, 1.0)
    d.t(RES_X + RES_W / 2, y + 24, n, 12, INK, MONO)

d.legend(392, [("입구", INFO), ("서버", ACC), ("경유 · 저장", SOFT)])
d.save("03-01.access-paths.svg")
