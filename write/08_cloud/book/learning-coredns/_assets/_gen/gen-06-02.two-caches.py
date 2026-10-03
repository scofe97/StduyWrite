# 06-02 §2 — 응답 캐시가 아끼는 몫은 이름의 종류에 따라 다르다.
# 본문 근거: 이 노트 §2 — 클러스터 안 이름은 해싱·조회 오버헤드에 이득이 깎이고 빗나가면 순손해, 외부 이름은 네트워크를 타므로 캐시가 값을 한다.
#            kubeadm 판은 cluster.local 을 disable success/denial 로 뺀다(이 노트 §4 버전 차이, manifests.go).
# 타입 스펙: type-dp-security-matrix — 이름 종류(행) × 적중·빗나감·아끼는 것(열) 격자가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 420
d = D(W, H, "LEARNING COREDNS · 06-02 §2",
      "응답 캐시가 아끼는 몫은 이름마다 다르다",
      "클러스터 안 이름은 이미 메모리에 있는 자원에서 만들어지므로 캐시가 아끼는 것이 생성 비용 조금뿐이다. "
      "외부 이름은 빗나가면 상류까지 네트워크를 타므로 캐시가 한 번의 왕복을 아낀다.",
      "주황 칸이 2절이 짚는 자리입니다")

COLS = [(20, 190, "이름의 종류"), (220, 210, "캐시 적중"), (440, 210, "캐시 빗나감"), (660, 200, "캐시가 아끼는 것")]
rows = [
    (("클러스터 안 이름", "orders.default.svc…"), ("해싱 · 조회 후 응답", "메모리에서 메모리로", INK),
     ("해싱 · 조회 + 즉석 생성", "빗나가면 오히려 손해", BAD), ("생성 비용 조금", "오버헤드에 깎임", ACC)),
    (("외부 이름", "www.example.org"), ("네트워크 없이 응답", "", INK),
     ("forward 로 상류 왕복", "네트워크를 탄다", INK), ("상류 왕복 한 번", "캐시가 값을 한다", OK)),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (name, *cells) in enumerate(rows):
    y = 132 + i * 92
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, 76, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 12, y + 32, name[0], 14, INK, KR, "start", 600)
    d.t(x0 + 12, y + 56, name[1], 12, MUTED, MONO, "start")
    for k, (main, sub, c) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        if c == ACC:
            d.tone(x, y, w, 76, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 76, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + (32 if sub else 44), main, 14, c, KR, "start", 600)
        if sub:
            d.t(x + 12, y + 56, sub, 12, MUTED, KR, "start")

d.t(20, 338, "kubeadm 판 · cluster.local 성공 응답은 캐시하지 않음 · 외부 이름만 캐시", 13, MUTED, KR, "start")
d.t(20, 362, "두 캐시 · 쿠버네티스 객체 캐시는 자원을 · cache 플러그인은 DNS 응답을 담는다", 13, MUTED, KR, "start")

d.legend(378, [("클러스터 안에서 아끼는 몫", ACC), ("손해", BAD), ("값을 하는 자리", OK)])
d.save("06-02.two-caches.svg")
