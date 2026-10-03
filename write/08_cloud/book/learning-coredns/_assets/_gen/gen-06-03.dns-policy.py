# 06-03 §4 — dnsPolicy 에 따라 파드의 nameserver 가 달라지고, 외부 이름이 나가는 길이 갈린다.
# 본문 근거: 이 노트 §4 「가운데 겹」(원서 요지 — Default 는 노드의 DNS 설정, 파드 기본은 ClusterFirst,
#            CoreDNS 는 노드의 상류 네임서버로 외부 이름을 풀어야 한다)과 같은 절의 노트 추론(ClusterFirst 면 자기를 본다).
#            CoreDNS 가 외부 이름을 forward 로 넘기는 것은 06-02 의 기본 Corefile `forward . /etc/resolv.conf`.
# 타입 스펙: type-dp-security-matrix — 파드·정책(행) × nameserver·외부 이름 경로(열) 격자가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 460
d = D(W, H, "LEARNING COREDNS · 06-03 §4",
      "정책 하나가 외부 이름의 출구를 정한다",
      "앱 파드는 기본값 ClusterFirst 로 클러스터 DNS 를 nameserver 로 받는다. CoreDNS 만 Default 로 노드의 resolv.conf 를 받아 "
      "외부 이름을 노드의 상류로 내보낸다. CoreDNS 가 ClusterFirst 라면 자기 자신을 nameserver 로 보게 된다.",
      "주황 행이 CoreDNS 가 Default 를 쓰는 이유입니다")

COLS = [(20, 220, "파드 · 정책"), (250, 250, "resolv.conf 의 nameserver"), (510, 350, "외부 이름이 가는 곳")]
rows = [
    (("앱 파드", "ClusterFirst · 기본값"), ("10.7.240.10", "kube-dns 서비스"), ("CoreDNS 가 받는다", "forward 로 상류에 넘긴다"), None),
    (("CoreDNS 파드", "Default"), ("노드의 nameserver", "노드 /etc/resolv.conf 내용"), ("노드의 상류 네임서버", "클러스터 밖으로 나간다"), ACC),
    (("CoreDNS 파드라면", "ClusterFirst 일 때 · 노트의 추론"), ("10.7.240.10", "자기 자신의 서비스"), ("자기에게 되돌아온다", "상류로 나갈 길이 없다"), BAD),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (c0, c1, c2, mark) in enumerate(rows):
    y = 132 + i * 84
    if mark == ACC:
        d.tone(16, y - 4, 848, 80, ACC, 8, "12", 1.4)
    for k, ((x, w, _), (m, sub)) in enumerate(zip(COLS, (c0, c1, c2))):
        d.box(x, y, w, 72, PAPER2, RULE, 1.0, 6)
        fam = MONO if m.replace(".", "").isdigit() else KR
        col = BAD if (mark == BAD and k == 2) else (ACC if (mark == ACC and k == 0) else INK)
        d.t(x + 12, y + 30, m, 14, col, fam, "start", 600)
        d.t(x + 12, y + 52, sub, 12, MUTED, KR, "start")

d.t(20, 402, "앱 파드는 ClusterFirst 그대로 · CoreDNS 만 Default · 10.7.240.10 은 원서 예제 값", 13, MUTED, KR, "start")

d.legend(418, [("CoreDNS 의 실제 설정", ACC), ("상류로 못 나가는 경우", BAD)])
d.save("06-03.dns-policy.svg")
