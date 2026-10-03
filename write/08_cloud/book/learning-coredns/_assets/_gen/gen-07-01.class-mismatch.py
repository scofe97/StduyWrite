# 07-01 §4 — rewrite continue class CH IN + rewrite stop name 뒤 응답의 Question 과 Answer 가 클래스에서 어긋나는 자리.
# 본문 근거: 이 노트 §4 의 두 줄 규칙(원서 Example 7-11)과 "host 가 잘못된 패킷 경고를 내며 답을 보여 준다"(원서 Example 7-12 요지),
#            출력의 "1.0.1"(원서). 소스 근거: v1.5.0 reverter.go 가 Question 을 원래대로 되돌리고, 정확 일치 name 규칙은 Answer 이름을 되돌린다.
# 타입 스펙: type-data-flow — 같은 질의가 클라이언트 → rewrite 뒤 → 응답의 세 단계를 지나며 섹션마다 값이 바뀐다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, OK, KR, MONO

W, H = 880, 420
d = D(W, H, "LEARNING COREDNS · 07-01 §4",
      "이름은 되돌아오고 클래스는 남는다",
      "CH 클래스로 bind.version 의 TXT 를 물으면 rewrite 가 클래스와 이름을 바꿔 kubernetes 가 답한다. "
      "나갈 때 Question 과 Answer 이름은 되돌아오지만 Answer 의 클래스는 IN 으로 남아 질문의 CH 와 어긋난다.",
      "주황 칸이 되돌릴 옵션이 없는 자리입니다")

COLS = [(20, 110, "섹션"), (140, 230, "클라이언트가 보낸 것"), (390, 240, "rewrite 뒤 · kubernetes 가 본 것"), (650, 210, "응답에 실린 것")]
rows = [
    ("Question", ("bind.version.", "CH  TXT"), ("dns-version.cluster.local.", "IN  TXT"), ("bind.version.", "CH  TXT · 원래대로")),
    ("Answer", ("—", ""), ("dns-version.cluster.local.", "IN  TXT  \"1.0.1\""), ("bind.version.", "IN  TXT  \"1.0.1\"")),
]

for k, (x, w, head) in enumerate(COLS):
    d.t(x + 10, 118, head, 12, SOFT, KR, "start", 600)

for i, (sec, *cells) in enumerate(rows):
    y = 132 + i * 100
    x, w, _ = COLS[0]
    d.box(x, y, w, 82, PAPER2, RULE, 1.0, 6)
    d.t(x + 10, y + 46, sec, 13, INK, MONO, "start", 600)
    for k, (a, b) in enumerate(cells, start=1):
        x, w, _ = COLS[k]
        foc = (i == 1 and k == 3)
        if foc:
            d.tone(x, y, w, 82, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 82, PAPER2, RULE, 1.0, 6)
        d.t(x + 10, y + 34, a, 13 if len(a) < 24 else 12, ACC if foc else (SOFT if a == "—" else INK), MONO, "start", 600)
        if b:
            d.t(x + 10, y + 60, b, 12, BAD if foc else MUTED, KR if "원래" in b else MONO, "start")
        if k < 3:
            nx = COLS[k + 1][0]
            d.path(f"M {x + w + 2} {y + 41} L {nx - 3} {y + 41}", MUTED, 1.2, m="ar")

d.t(20, 354, "host 는 잘못된 패킷 경고와 함께 답을 보여 준다 · 클래스를 대조하는 리졸버라면 버릴 수 있다", 13, MUTED, KR, "start")

d.legend(372, [("되돌릴 옵션이 없는 칸", ACC)])
d.save("07-01.class-mismatch.svg")
