# 06-04 §1 「클러스터 밖에서 붙는 셋」 — CoreDNS 가 어디서 도느냐에 따라 API 서버에 붙는 설정 줄과 인증 수단이 갈린다.
# README 근거(master, 2026-10-03 대조): endpoint "If omitted, it will connect to k8s in-cluster using the cluster
#            service account." / tls "CERT KEY CACERT ... ignored if connecting in-cluster" / kubeconfig "It supports TLS,
#            username and password, or token-based authentication. ... The cluster address in the kubeconfig is given preference."
# 타입 스펙: type-dp-security-matrix — 배치(행) × 설정 줄·인증·붙는 곳(열) 격자에서 어느 조합이 쓰이는가가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 06-04 §1",
      "어디서 도느냐가 붙는 설정 줄을 정한다",
      "클러스터 안 파드로 돌면 설정 줄 없이 서비스 어카운트로 API 서버에 붙는다. 클러스터 밖에서 돌면 endpoint 와 tls 로 "
      "URL 과 인증서를 주거나, kubeconfig 하나로 주소와 인증을 함께 준다. 둘 다 적으면 kubeconfig 가 이긴다.",
      "주황 열이 이 소절이 다루는 설정 줄입니다")

COLS = [(20, 160, "CoreDNS 위치"), (190, 250, "kubernetes 블록 안 설정 줄"),
        (450, 210, "인증 수단"), (670, 190, "붙는 API 서버")]
rows = [
    (("클러스터 안 파드", ""), ("(설정 줄 없음)", "기본값"), ("서비스 어카운트", "자동으로 붙는다"), ("in-cluster 주소", "")),
    (("클러스터 밖", "URL 직접"), ("endpoint URL", "tls CERT KEY CACERT"), ("TLS 클라이언트 인증서", ""), ("endpoint 의 URL", "")),
    (("클러스터 밖", "kubeconfig"), ("kubeconfig FILE", "[CONTEXT]"), ("TLS · 사용자·암호 · 토큰", ""), ("컨텍스트의 주소", "endpoint 보다 우선")),
]
Y0, PITCH, RH = 132, 84, 72

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, ACC if k == 1 else SOFT, KR, "start", 600)

d.tone(186, Y0 - 4, 258, PITCH * 2 + RH + 8, ACC, 8, "12", 1.4)

for i, cells in enumerate(rows):
    y = Y0 + i * PITCH
    for k, (x, w, _) in enumerate(COLS):
        main, sub = cells[k]
        if k != 1:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        fam = MONO if (k == 1 and not main.startswith("(")) else KR
        col = ACC if k == 1 else INK
        if sub:
            d.t(x + 12, y + 30, main, 13, col, fam, "start", 600)
            d.t(x + 12, y + 52, sub, 12, MUTED, MONO if (k == 1 and i > 0) else KR, "start")
        else:
            d.t(x + 12, y + 42, main, 13, col, fam, "start", 600)

d.t(20, 404, "원서 · kubeconfig 에 GCP · OpenStack · OIDC 인증 플러그인 · 지금 README 는 셋만 적는다", 13, MUTED, KR, "start")

d.legend(424, [("이 소절의 설정 줄", ACC)])
d.save("06-04.outside-access.svg")
