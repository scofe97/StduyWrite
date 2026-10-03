# 06-02 §5 — 두 서버 블록 중 질의 이름과 가장 길게 일치하는 블록이 질의를 가져간다.
# 본문 근거: 이 노트 §5 Example 6-13(.:53 블록과 corp.example.com:53 블록, forward . 10.0.0.10:53)과
#            "질의가 가장 길게 일치하는 서버 블록으로 향하기 때문입니다". 최장 일치 규칙은 03-01 노트.
# 타입 스펙: type-flowchart — 질의마다 두 블록 중 하나로 갈리는 분기가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, KR, MONO

W, H = 880, 420
d = D(W, H, "LEARNING COREDNS · 06-02 §5",
      "라벨이 더 길게 맞는 블록이 질의를 가져간다",
      "Example 6-13 의 두 블록에 질의 둘을 넣었다. 클러스터 이름은 루트 블록에만 맞고, 사내 이름은 두 블록 모두에 맞지만 "
      "라벨 셋이 맞는 corp.example.com 블록이 이긴다.",
      "주황 칸이 스텁 도메인이 이기는 자리입니다")

COLS = [(20, 260, "질의"), (290, 180, ".:53 블록"), (480, 210, "corp.example.com:53"), (700, 160, "가는 곳")]
rows = [
    ("orders.default.svc.cluster.local", ("일치 · 라벨 0개", "유일한 후보", OK), ("불일치", "", SOFT), ("kubernetes", "클러스터 이름")),
    ("host.corp.example.com", ("일치 · 라벨 0개", "더 짧아서 진다", MUTED), ("일치 · 라벨 3개", "가장 긴 일치", ACC), ("10.0.0.10:53", "사내 네임서버")),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, MONO if head.startswith(("corp", ".:")) else KR, "start", 600)

for i, (q, b1, b2, dest) in enumerate(rows):
    y = 132 + i * 92
    x0, w0, _ = COLS[0]
    d.box(x0, y, w0, 76, PAPER2, RULE, 1.0, 6)
    d.t(x0 + 12, y + 44, q, 12, INK, MONO, "start", 600)
    for k, (main, sub, c) in ((1, b1), (2, b2)):
        x, w, _ = COLS[k]
        if c == ACC:
            d.tone(x, y, w, 76, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 76, PAPER2, RULE, 1.0, 6)
        d.t(x + 12, y + (32 if sub else 44), main, 14, c if c != SOFT else SOFT, KR, "start", 600)
        if sub:
            d.t(x + 12, y + 56, sub, 12, MUTED, KR, "start")
    x, w, _ = COLS[3]
    d.box(x, y, w, 76, PAPER2, RULE, 1.0, 6)
    d.t(x + 12, y + 32, dest[0], 13, INK, MONO, "start", 600)
    d.t(x + 12, y + 56, dest[1], 12, MUTED, KR, "start")
    # 첫 행은 이긴 칸(.:53)과 가는 곳 사이에 불일치 칸이 끼어 화살표가 글자를 가르므로 둘째 행에만 긋는다
    if i == 1:
        wx, ww, _ = COLS[2]
        d.path(f"M {wx + ww + 2} {y + 38} L {COLS[3][0] - 3} {y + 38}", ACC, 1.3, m="acc")

d.t(20, 338, "스텁 도메인 · 별도 문법 없이 서버 블록 하나 · 최장 일치 규칙이 같은 일을 한다", 13, MUTED, KR, "start")
d.t(20, 362, "블록마다 플러그인 체인이 독립 · 둘째 블록이 cache · loop 를 따로 적는 이유", 13, MUTED, KR, "start")

d.legend(378, [("이긴 블록", ACC), ("유일한 후보", OK)])
d.save("06-02.stub-match.svg")
