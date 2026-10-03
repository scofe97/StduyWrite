# 07-01 §9 Safe Search — CNAME 으로 답만 돌리는 방식과 질문 이름을 바꾸는 rewrite 를 응답 섹션으로 비교한다.
# 근거: Google 도움말 "Set the DNS entry for www.google.com ... to be a CNAME for forcesafesearch.google.com",
#       이 노트 §3 의 정규식 rewrite(answer name 없을 때 Answer 에 바뀐 이름).
# 타입 스펙: type-dp-security-matrix — 방식(행) × 응답 섹션(열)에서 질문 이름이 남는 칸과 바뀌는 칸이 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, BAD, KR, MONO

W, H = 880, 400
d = D(W, H, "LEARNING COREDNS · 07-01 §9",
      "CNAME 은 질문을 두고 답만 다른 이름을 가리킨다",
      "Safe Search 강제는 www.google.com 을 forcesafesearch.google.com 의 CNAME 으로 둔다. 응답의 첫 레코드 소유자가 물은 이름 그대로라 대응이 지켜진다. "
      "질문 이름 자체를 바꾸는 정규식 rewrite 는 answer name 없이는 Answer 에 다른 이름이 실린다.",
      "주황 칸이 물은 이름이 그대로 남는 자리입니다")

COLS = [(20, 200, "방식"), (230, 240, "Question"), (480, 380, "Answer")]
rows = [
    (("CNAME 으로 돌림", "Safe Search 강제"), ("www.google.com.", OK),
     ("www.google.com. CNAME", "forcesafesearch.google.com.")),
    (("질문 이름을 바꿈", "regex · answer name 없음"), ("www.google.com.", OK),
     ("forcesafesearch.google.com. A", "물은 이름과 다른 소유자")),
]

for x, w, head in COLS:
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (how, q, ans) in enumerate(rows):
    y = 132 + i * 90
    x, w, _ = COLS[0]
    d.box(x, y, w, 72, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 30, how[0], 13, INK, KR, "start", 600)
    d.t(x + 12, y + 52, how[1], 12, MUTED, KR, "start")
    x, w, _ = COLS[1]
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="72" rx="6" fill="{q[1]}14" stroke="{q[1]}" stroke-width="1.0"/>')
    d.t(x + 12, y + 41, q[0], 13, q[1], MONO, "start", 600)
    x, w, _ = COLS[2]
    if i == 0:
        d.tone(x, y, w, 72, ACC, 6, "12", 1.4)
        d.t(x + 12, y + 30, ans[0], 13, ACC, MONO, "start", 600)
        d.t(x + 12, y + 52, ans[1], 12, MUTED, MONO, "start")
    else:
        d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="72" rx="6" fill="{BAD}14" stroke="{BAD}" stroke-width="1.0"/>')
        d.t(x + 12, y + 30, ans[0], 13, BAD, MONO, "start", 600)
        d.t(x + 12, y + 52, ans[1], 12, MUTED, KR, "start")

d.t(20, 344, "둘째 행은 비교를 위한 가정 · 실제 Safe Search 강제는 첫째 행 방식", 13, MUTED, KR, "start")

d.legend(358, [("물은 이름이 남는 칸", ACC), ("물은 이름과 같음", OK), ("물은 이름과 다름", BAD)])
d.save("07-01.safesearch-cname.svg")
