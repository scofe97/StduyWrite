# 05-01 §2 네 번째 칸 — 호스트 IP 하나에 컨테이너 둘을 올리면 SRV 가 준 포트가 컨테이너를 가른다.
# 본문 근거: 이 노트 §2 「네 번째 칸」 117~127줄.
# 원서 근거: 원서 3쪽 "An SRV record contains a port as well as another DNS name, which can be resolved to
#            an IP address. Using an SRV record means we do not need to follow ordinary port conventions for
#            services, allowing us to host, for example, multiple HTTP-based microservice APIs on the same
#            IP address. In simple containerized environments, only the host's IP address is reachable on
#            the network, and containers are reached by forwarding ports from the host IP address to the
#            host-local container IP addresses."
# 타입 스펙: type-data-flow — 이름이 SRV·호스트 포트·포워딩을 거쳐 컨테이너에 닿는 단계를 열로 놓았다.
#           users 의 이름·20020·192.0.2.10 은 5절 예제 값(원서 6쪽 Example 5-1, 9쪽 Example 5-7).
# 2026-11-01 검증: 둘째 줄의 cart.services.example.com·20021·172.17.0.x:8080 은 본문·원서에 없는 지어낸 값이라 뺐다.
#           둘째 API 와 컨테이너 주소는 값 없이 이름만 둔다. SRV 의 대상은 IP 가 아니라 이름이므로(원서 3쪽) "대상 이름" 으로 고쳤다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 440
d = D(W, H, "LEARNING COREDNS · 05-01 §2",
      "포트까지 알아야 한 호스트의 컨테이너를 가른다",
      "단순한 컨테이너 환경에서는 호스트 IP 에만 닿고, 컨테이너는 호스트 포트를 거쳐 포워딩된다. "
      "SRV 가 서비스마다 포트를 알려 주므로 같은 IP 위의 HTTP API 둘을 이름으로 가를 수 있다.",
      "주황 열이 A 레코드에는 없는 정보입니다")

COLS = [(20, 220, "이름"), (260, 170, "SRV 응답이 주는 것"),
        (450, 190, "호스트에서 닿는 곳"), (660, 200, "포워딩되는 컨테이너")]
rows = [
    [("users.services.example.com", "사용자 API", MONO), ("포트 20020", "대상 이름 · 192.0.2.10", KR),
     ("192.0.2.10:20020", "호스트 IP 에만 닿음", MONO), ("컨테이너 IP:포트", "users 컨테이너", KR)],
    [("다른 HTTP API", "같은 IP 위의 둘째 API", KR), ("다른 포트", "대상 이름 · 192.0.2.10", KR),
     ("192.0.2.10:다른 포트", "같은 호스트 IP", KR), ("컨테이너 IP:포트", "둘째 컨테이너", KR)],
]

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 12, 118, head, 12, ACC if k == 1 else SOFT, KR, "start", 600)
    if k < 3:
        nx = COLS[k + 1][0]
        for ry in (130, 230):
            d.path(f"M {x + w + 2} {ry + 38} L {nx - 3} {ry + 38}", MUTED, 1.2, m="ar")

for i, cells in enumerate(rows):
    y = 130 + i * 100
    for k, (x, w, _) in enumerate(COLS):
        if k == 1:
            d.tone(x, y, w, 76, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 76, PAPER2, RULE, 1.0, 6)
        main, sub, fam = cells[k]
        d.t(x + 12, y + 32, main, 12 if fam == MONO and k == 0 else 13 if fam == MONO else 14,
            ACC if k == 1 else INK, fam, "start", 600)
        d.t(x + 12, y + 56, sub, 12, MUTED, KR, "start")

d.t(20, 356, "A 레코드만으로는 포트 열 없음 · 컨테이너 하나 또는 정적 포트 매핑", 13, MUTED, KR, "start")
d.t(20, 378, "users 값은 5절 예제 · 둘째 API 와 컨테이너 주소는 값 없이 이름만", 12, SOFT, KR, "start")

d.legend(396, [("SRV 가 더하는 포트", ACC)])
d.save("05-01.host-port.svg")
