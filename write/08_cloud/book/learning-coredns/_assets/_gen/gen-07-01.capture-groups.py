# 07-01 §1 — template 이 질문 이름을 캡처 그룹으로 쪼개고 answer 템플릿으로 다시 조립하는 과정.
# 본문 근거: 이 노트 §1 의 Corefile(원서 Example 7-1)과 dig 출력(원서 Example 7-2) — 1.2.3.4.in-addr.arpa PTR 이
#            host-4-3-2-1.example.com 을, host-1-2-3-4.example.com A 가 1.2.3.4 를 돌려준다.
# 타입 스펙: type-data-flow — 이름이 match·그룹·answer 를 거쳐 응답이 되는 단계를 열로, 두 질의를 행으로 놓았다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, KR, MONO

W, H = 880, 430
d = D(W, H, "LEARNING COREDNS · 07-01 §1",
      "이름을 쪼개 다시 조립하면 답이 된다",
      "match 정규식의 이름 붙은 그룹이 질문 이름을 조각내고, answer 의 Go 템플릿이 그 조각을 다시 잇는다. "
      "PTR 쪽은 그룹 이름을 d.c.b.a 순으로 붙여 두 템플릿이 서로의 역함수가 된다.",
      "주황 열이 질문 이름에서 떼어 낸 조각입니다")

# answer 템플릿 열이 PTR 줄을 담도록 넓힌다(2026-10-03 첫 렌더에서 넘침)
COLS = [(20, 200, "물은 이름"), (240, 130, "match 가 잡은 그룹"), (390, 290, "answer 템플릿"), (700, 160, "응답")]
rows = [
    (("host-1-2-3-4", ".example.com.  A"), ("a=1  b=2", "c=3  d=4"),
     ("{{ .Group.a }}.{{ .Group.b }}.", "{{ .Group.c }}.{{ .Group.d }}"), ("1.2.3.4", "A 60초")),
    (("1.2.3.4", ".in-addr.arpa.  PTR"), ("d=1  c=2", "b=3  a=4"),
     ("host-{{ .Group.a }}-{{ .Group.b }}-", "{{ .Group.c }}-{{ .Group.d }}..."), ("host-4-3-2-1", ".example.com.")),
]

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 10, 118, head, 12, ACC if k == 1 else SOFT, KR, "start", 600)

for i, cells in enumerate(rows):
    y = 132 + i * 104
    for k, (x, w, _) in enumerate(COLS):
        if k == 1:
            d.tone(x, y, w, 84, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 84, PAPER2, RULE, 1.0, 6)
        a, b = cells[k]
        col = ACC if k == 1 else INK
        size = 12 if k == 2 else 14
        d.t(x + 10, y + 34, a, size, col, MONO, "start", 600)
        d.t(x + 10, y + 60, b, 12 if k == 2 else 13, MUTED if k in (0, 3) else col, MONO, "start")
        if k < 3:
            nx = COLS[k + 1][0]
            d.path(f"M {x + w + 2} {y + 42} L {nx - 3} {y + 42}", MUTED, 1.2, m="ar")

d.t(20, 362, "역방향 이름 1.2.3.4.in-addr.arpa · 주소 4.3.2.1 을 뒤집어 적은 것", 13, MUTED, KR, "start")

d.legend(380, [("질문 이름에서 떼어 낸 조각", ACC)])
d.save("07-01.capture-groups.svg")
