# 06-04 §3 「쓸모가 분명한 자리가 하나」 — ClusterIP 서비스의 엔드포인트를 묻는 길이 원서 시점과 지금 어떻게 다른가.
# 본문 근거: 이 노트 §3 — kube-dns 는 A 하나, '*.kube-dns...' 는 원서에서 엔드포인트 레코드 둘(이름은 질의 그대로).
# 릴리스 노트 근거: 1.9.0 "Wildcard queries are no longer supported by the kubernetes plugin."
# 타입 스펙: type-dp-security-matrix — 묻는 방법(행) × 시점(열) 격자에서 어느 칸이 닫혔는가가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 530
d = D(W, H, "LEARNING COREDNS · 06-04 §3",
      "엔드포인트를 묻는 유일한 DNS 길이 닫혔다",
      "ClusterIP 서비스 kube-dns 의 엔드포인트를 알아내는 방법을 원서 시점과 1.9.0 이후로 나눴다. "
      "와일드카드 질의 칸이 닫혀서 지금은 DNS 밖에서 보거나 헤드리스 서비스를 따로 둔다.",
      "주황 칸이 1.9.0 에서 닫힌 길입니다")

COLS = [(20, 300, "묻는 방법"), (330, 260, "원서 시점 · 1.8 까지"), (600, 260, "지금 · 1.9.0 이후")]
rows = [
    (("kube-dns.kube-system", "svc.cluster.local · A"), ("VIP 하나", "ClusterIP 라서", INK), ("VIP 하나", "그대로", INK)),
    (("*.kube-dns.kube-system", "svc.cluster.local · A"), ("엔드포인트 레코드 둘", "이름은 질의 그대로", OK), ("레코드가 오지 않음", "1.9.0 에서 기능 제거", ACC)),
    (("헤드리스 서비스를 따로", "같은 셀렉터 · SRV"), ("엔드포인트별 SRV", "명세 안의 길", INK), ("엔드포인트별 SRV", "명세 안의 길", INK)),
    (("kubectl get endpointslices", "-l kubernetes.io/service-name=kube-dns"), ("Endpoints 로 확인", "DNS 밖", MUTED), ("주소 목록", "DNS 밖", INK)),
]
Y0, PITCH, RH = 132, 78, 68

for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (q, then, now) in enumerate(rows):
    y = Y0 + i * PITCH
    x, w, _ = COLS[0]
    d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 28, q[0], 13 if i < 3 and not q[0].startswith("헤") else 12,
        INK, KR if q[0].startswith("헤") else MONO, "start", 600)
    d.t(x + 12, y + 50, q[1], 12, MUTED, KR if i == 2 else MONO, "start")
    for k, (main, sub, c) in enumerate((then, now), start=1):
        x, w, _ = COLS[k]
        if c == ACC:
            d.tone(x, y, w, RH, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + 28, main, 14, c, KR, "start", 600)
        d.t(x + 12, y + 50, sub, 12, MUTED, KR, "start")

d.t(20, 460, "엔드포인트별 레코드 · 명세가 주는 곳은 헤드리스 서비스뿐", 13, MUTED, KR, "start")

d.legend(482, [("1.9.0 에서 닫힌 칸", ACC), ("원서 시점의 유일한 DNS 길", OK)])
d.save("06-04.wildcard-now.svg")
