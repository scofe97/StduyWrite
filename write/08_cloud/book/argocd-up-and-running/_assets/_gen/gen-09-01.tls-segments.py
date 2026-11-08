# 09-01 §1~2 — 이 편이 다루는 TLS 연결은 두 구간이다. 브라우저·CLI 가 argocd-server 로 가는 구간은 argocd-server-tls Secret 이 인증서를 내고, repo-server 가 Git 서버로 가는 구간은 argocd-tls-certs-cm 이 믿을 인증서를 정한다.
# 본문 근거: 이 노트 ### 1 「서버 인증서」와 ### 2 「저장소 서버 인증서」.
# 검증 근거: kind v0.31.0 에 Argo CD v3.6.1 을 설치하고 두 구간을 따로 확인했다.
#            argocd-server 는 argocd-server-tls Secret 이 없으면 자체 서명 인증서를 내고, 라벨(app.kubernetes.io/part-of=argocd)을 단 Secret 을 만들면 재시작 없이 바꿔 냈다.
#            사설 CA 가 서명한 Git 서버에는 argocd-tls-certs-cm 에 호스트 이름 키로 CA 인증서를 넣기 전까지 x509 오류로 실패했고, 넣은 뒤에는 성공했다.
# 공식 근거: argo-cd v3.6.1 docs/operator-manual/tls.md("Certificate Priority", "Configuring inbound TLS for argocd-server"),
#            docs/operator-manual/declarative-setup.md("Repositories using self-signed TLS certificates"), docs/user-guide/private-repositories.md("Self-signed & Untrusted TLS Certificates").
# 타입 스펙: type-architecture — 왼쪽 시점(연결하는 쪽, 클라이언트)에서 오른쪽(연결을 받는 쪽, 서버)으로 가는 한 방향 흐름, 줄마다 하나의 구간.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 432
d = D(W, H, "ARGO CD UP AND RUNNING · 09-01 §1~2",
      "TLS 연결 두 구간과 인증서를 두는 곳",
      "위쪽 줄은 브라우저와 명령줄 도구가 argocd-server 에 연결하는 구간이다. 연결을 받는 쪽(서버)인 argocd-server 는 argocd-server-tls Secret 의 인증서를 내고 연결하는 쪽(클라이언트)은 운영체제 신뢰 저장소로 그 인증서를 믿는다. "
      "아래쪽 줄은 argocd-repo-server 가 Git 서버에 HTTPS 로 연결하는 구간이다. 믿을 인증서는 연결하는 쪽(클라이언트)인 Argo CD 의 argocd-tls-certs-cm 에 호스트 이름별로 넣는다.",
      "구간마다 믿음을 정하는 곳이 다르다")

C1X, C1W = 24, 330
C2X, C2W = 526, 330
YS = [124, 262]
RH = 108

for cx, label in ((C1X + C1W / 2, "연결하는 쪽(클라이언트) — 믿음을 정하는 곳"), (C2X + C2W / 2, "연결을 받는 쪽(서버) — 인증서를 내는 곳")):
    d.t(cx, 108, label, 12, MUTED, KR, "middle", 600)

rows = [
    ("구간 1", ("브라우저 · argocd CLI", KR), ("운영체제 신뢰 저장소", KR),
     ("argocd-server", MONO), ("argocd-server-tls Secret", MONO)),
    ("구간 2", ("argocd-repo-server", MONO), ("argocd-tls-certs-cm", MONO),
     ("Git 서버 (HTTPS)", KR), ("사설 CA 가 서명한 서버 인증서", KR)),
]

for y, (seg, (a1, f1), (a2, f2), (b1, g1), (b2, g2)) in zip(YS, rows):
    cy = y + RH / 2
    d.tone(C1X, y, C1W, RH, INFO, 6, "14", 1.1)
    d.t(C1X + C1W / 2, y + 46, a1, 12.5, INK, f1, "middle", 600)
    d.t(C1X + C1W / 2, y + 72, a2, 12, MUTED, f2)
    d.tone(C2X, y, C2W, RH, ACC, 6, "14", 1.4)
    d.t(C2X + C2W / 2, y + 46, b1, 12.5, INK, g1, "middle", 600)
    d.t(C2X + C2W / 2, y + 72, b2, 12, MUTED, g2)
    d.t((C1X + C1W + C2X) / 2, cy - 10, seg + " · TLS", 12, MUTED, KR, "middle", 600)
    d.path(f"M {C1X + C1W + 2} {cy} L {C2X - 2} {cy}", MUTED, 1.4, m="ar")

d.legend(392, [("연결하는 쪽(클라이언트)", INFO), ("연결을 받는 쪽(서버)", ACC)])
d.save("09-01.tls-segments.svg")
