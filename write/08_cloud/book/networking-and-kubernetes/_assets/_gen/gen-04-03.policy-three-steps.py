# 04-03.policy-three-steps — demo-db 에 정책을 한 단계씩 조일 때 두 방향이 어떻게 닫히고 열리는가
# 본문 요구: "1. 정책이 없으면 둘은 전부 통신 … 2. demo-db 를 선택하고 규칙을 비우면 어떤 트래픽도 주고받지 못합니다 …
#           3. ingress.from.podSelector: app=demo 를 더하면 demo 에서 오는 연결만 받습니다. 나가는 연결은 여전히 차단"
# 타입 스펙: type-state — 주체 하나(demo-db 의 정책 상태)가 세 상태를 차례로 거친다. 같은 두 Pod 와 두 방향을
#           상태마다 다시 그려 무엇이 닫히고 열리는지를 칸 차이로 보인다. 손으로 쓴 SVG 를 2026-09-15 생성기로 옮겼다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, BAD, INFO, PAPER, PAPER2, KR, MONO

W, H = 1000, 592
d = D(W, H, "NETWORKPOLICY · TIGHTENING IN THREE STEPS",
      "정책을 한 단계씩 조이면 무엇이 닫히는가",
      "정책이 없으면 전부 열려 있고, 선택만 하고 규칙을 비우면 양방향이 닫히며, 허용 규칙을 하나 더하면 그 방향만 예외로 열린다.",
      lead="2단계는 규칙 0줄인데 전부 닫힘 · 선택 자체가 차단으로 뒤집는다")

STRIDE, Y0 = 144, 104
DX, DBX, BW, BH = 144, 584, 132, 48
NOTE_X = 764


def pod(x, y, name, c=RULE, tc=INK, sub=None):
    d.box(x, y, BW, BH, PAPER2, c, 1.2, 6)
    if sub:
        d.t(x + BW // 2, y + 20, name, 13, tc, MONO, "middle", 600)
        d.t(x + BW // 2, y + 38, sub, 12, tc, KR)
    else:
        d.t(x + BW // 2, y + 29, name, 13, tc, MONO, "middle", 600)


def links(y, ing, egr):
    (il, ic), (el, ec) = ing, egr
    yi, ye = y + 16, y + 34
    a, b = DX + BW + 8, DBX - 10
    d.arrow([(a, yi), (b, yi)], ic, "ok" if ic == OK else "bad", 1.5, None if ic == OK else "6 5")
    d.arrow([(b + 2, ye), (a + 2, ye)], ec, "ok" if ec == OK else "bad", 1.5, None if ec == OK else "6 5")
    mx = (a + b) // 2
    d.t(mx, yi - 8, il, 12, ic, KR, "middle", 600)
    d.t(mx, ye + 20, el, 12, ec, KR, "middle", 600)


STEPS = [
    ("1 · 정책 없음", OK, None, (("ingress 열림", OK), ("egress 열림", OK)), ["기본 전부 허용"], INK),
    ("2 · demo-db 선택 · 규칙 비움", BAD, "선택됨", (("ingress 막힘", BAD), ("egress 막힘", BAD)), ["규칙 0줄", "DNS 질의도 차단"], BAD),
    ("3 · ingress 에 app=demo 허용 추가", INFO, "선택됨", (("허용된 예외 하나", OK), ("egress 막힘 유지", BAD)), ["허용만 추가 가능", "차단 규칙 표현 불가"], INFO),
]
for i, (title, tc, dbsub, (ing, egr), notes, dbc) in enumerate(STEPS):
    y = Y0 + i * STRIDE
    if i: d.line(32, y - 12, 968, y - 12, RULE, 0.8)
    d.t(52, y + 20, title, 13, tc, KR, "start", 600)
    by = y + 44
    pod(DX, by, "demo")
    pod(DBX, by, "demo-db", RULE if dbc is INK else dbc, dbc, dbsub)
    links(by, ing, egr)
    for k, n in enumerate(notes):
        nc = BAD if "차단" in n and i == 1 else MUTED
        d.t(NOTE_X, by + 20 + k * 24, n, 12, nc, KR, "start")

d.legend(544, [("열린 방향", OK), ("닫힌 방향", BAD), ("허용이 더해진 상태", INFO)])
d.save("04-03.policy-three-steps.svg")
print("ok policy-three-steps")
