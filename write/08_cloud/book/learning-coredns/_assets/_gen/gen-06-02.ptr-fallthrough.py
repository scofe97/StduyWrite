# 06-02 §4 — 역방향 존을 in-addr.arpa 전체로 잡았을 때 fallthrough 가 있고 없음에 따라 PTR 질의가 갈린다.
# 소스 근거: kubernetes README fallthrough — "If a query for a record in the zones for which the plugin is authoritative
#            results in NXDOMAIN, normally that is what the response will be. However, if you specify this option,
#            the query will instead be passed on down the plugin chain".
# 본문 근거: 이 노트 §4 「kubernetes 블록 안의 세 줄」. 10.7.240.10 은 원서의 서비스 CIDR 예 10.7.240.0/20 안의 주소다.
# 타입 스펙: type-dp-security-matrix — 질의(행) × fallthrough 유무(열) 2×2 격자에서 한 칸만 결과가 갈린다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 420
d = D(W, H, "LEARNING COREDNS · 06-02 §4",
      "fallthrough 가 없으면 모르는 IP 의 PTR 을 삼킨다",
      "kubernetes 블록이 in-addr.arpa 전체를 맡으면 모든 PTR 질의가 이 플러그인을 지난다. 서비스 IP 는 어느 쪽이든 답이 같지만, "
      "클러스터와 무관한 IP 는 fallthrough 가 있어야 forward 로 내려간다.",
      "주황 칸이 이 줄을 지웠을 때 깨지는 자리입니다")

COLS = [(20, 230, "PTR 질의"), (260, 290, "fallthrough 있음"), (560, 300, "fallthrough 없음")]
rows = [
    (("10.7.240.10 의 PTR", "서비스 CIDR 안"), ("서비스 이름으로 응답", "kubernetes 가 답함", False),
     ("서비스 이름으로 응답", "결과가 같음", False)),
    (("8.8.8.8 의 PTR", "클러스터와 무관"), ("forward 가 상류에 물음", "kubernetes 가 넘김", False),
     ("NXDOMAIN", "kubernetes 가 삼킴", True)),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (q, *cells) in enumerate(rows):
    y = 132 + i * 92
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, 76, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 12, y + 32, q[0], 14, INK, KR, "start", 600)
    d.t(x0 + 12, y + 56, q[1], 12, MUTED, KR, "start")
    for k, (main, sub, focal) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if focal:
            d.tone(x, y, w, 76, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 76, PAPER2, RULE, 1.0, 6)
        fm = MONO if main == "NXDOMAIN" else KR
        d.t(x + 12, y + 32, main, 14, ACC if focal else INK, fm, "start", 600)
        d.t(x + 12, y + 56, sub, 12, MUTED, KR, "start")

d.t(20, 338, "존 인자에 in-addr.arpa · ip6.arpa 전체를 줬을 때의 이야기", 13, MUTED, KR, "start")
d.t(20, 362, "역방향 CIDR 만 적었다면 · 8.8.8.8 은 처음부터 이 플러그인의 존 밖", 13, MUTED, KR, "start")

d.legend(378, [("fallthrough 를 지우면 깨지는 칸", ACC)])
d.save("06-02.ptr-fallthrough.svg")
