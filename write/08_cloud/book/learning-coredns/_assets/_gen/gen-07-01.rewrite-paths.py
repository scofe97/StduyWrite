# 07-01 §3 — rewrite 규칙 구성마다 응답의 Question 섹션과 Answer 이름이 어떻게 나가는가.
# 소스 근거: CoreDNS v1.5.0 plugin/rewrite/reverter.go `res.Question[0] = r.originalQuestion`,
#            plugin/rewrite/rewrite.go — Stop 이면 reverter 를 거치고, 끝까지 continue 이며 ResponseRules 가 비면 원래 writer.
#            plugin/rewrite/name.go — ExactMatch 만 응답 규칙을 스스로 만든다.
# 타입 스펙: type-dp-security-matrix — 규칙 구성(행) × 응답 섹션(열)에서 어느 칸이 어긋나는지가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 470
d = D(W, H, "LEARNING COREDNS · 07-01 §3",
      "Question 은 대개 돌아오고 Answer 이름이 갈린다",
      "api.example.com 을 물었을 때 응답에 실리는 이름이다. stop 경로에서는 Question 섹션이 늘 원래대로 돌아오고, "
      "Answer 이름은 정확 일치이거나 answer name 을 적었을 때만 돌아온다. 끝까지 continue 이고 응답 규칙이 없으면 Question 도 안 돌아온다.",
      "주황 행이 원서가 짚은 경우입니다")

COLS = [(20, 230, "규칙 구성"), (260, 230, "응답의 Question 섹션"), (500, 230, "응답의 Answer 이름"), (740, 120, "저자들 판단")]
G_ = ("api.example.com", OK)
B_ = ("api.example.svc.cluster.local", BAD)
rows = [
    (("name 정확 일치", "기본 stop"), G_, G_, ("받는다", OK)),
    (("name regex 만", "기본 stop"), G_, B_, ("버린다", BAD)),
    (("name regex", "+ answer name"), G_, G_, ("받는다", OK)),
    (("name regex 만", "모두 continue"), B_, B_, ("원서 밖", MUTED)),
]
FOCAL = 1

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (rule, q, a, verdict) in enumerate(rows):
    y = 132 + i * 66
    if i == FOCAL:
        d.tone(16, y - 3, 848, 64, ACC, 8, "12", 1.4)
    x, w, _ = COLS[0]
    if i != FOCAL:
        d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
    d.t(x + 10, y + 25, rule[0], 13, ACC if i == FOCAL else INK, KR, "start", 600)
    d.t(x + 10, y + 45, rule[1], 12, MUTED, KR, "start")
    for k, (txt, c) in ((1, q), (2, a)):
        x, w, _ = COLS[k]
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="58" rx="6" fill="{c}14" stroke="{c}" stroke-width="1.0"/>')
        d.t(x + 10, y + 35, txt, 12, c, MONO, "start", 600)
    x, w, _ = COLS[3]
    d.box(x, y, w, 58, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + 35, verdict[0], 13, verdict[1], KR)

d.t(20, 412, "v1.5.0 코드 기준 · 버린다 = 원서 주장 · 실제 거부는 라이브러리마다 다름", 13, MUTED, KR, "start")

d.legend(426, [("원서가 짚은 경우", ACC), ("물은 이름 그대로", OK), ("바뀐 이름이 나감", BAD)])
d.save("07-01.rewrite-paths.svg")
