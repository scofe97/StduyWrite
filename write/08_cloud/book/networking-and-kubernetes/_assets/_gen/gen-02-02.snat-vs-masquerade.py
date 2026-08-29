# 02-02.snat-vs-masquerade — 주소를 언제 아는가가 두 타깃을 가른다
# 본문 요구(§3 MASQUERADE 절): "SNAT 가 '출발지를 이 주소로 바꿔라'라고 값을 직접 적는 것이라면,
#           MASQUERADE 는 '출발지를 나가는 인터페이스의 주소로 바꿔라'라고 자리를 가리킵니다."
#           + "실제 값은 패킷이 나갈 때 커널이 그 인터페이스에서 읽어 채웁니다."
#           + "DHCP 로 주소를 받는 회선이나 노드가 뜰 때마다 IP 가 달라지는 클라우드에서는
#             규칙을 쓰는 시점에 넣을 값이 없습니다."
#           + "값이 고정이라면 매번 인터페이스를 조회하지 않는 SNAT 가 약간 더 빠릅니다."
#           + "나가는 인터페이스가 정해진 뒤라야 '그 인터페이스의 주소'를 알 수 있으므로
#             POSTROUTING 체인 전용입니다."
# 타입 스펙: type-flowchart.md — 조건 하나(규칙을 쓰는 시점에 넣을 주소를 아는가)에서 두 갈래로
#           갈리는 판단 논리. 갈래마다 규칙에 적는 것 · 값이 정해지는 시점 · 그래서 언제 쓰는지가
#           따라 나온다. 같은 장 01-03.local-or-gateway 와 같은 문법이라 읽는 법을 다시 배우지
#           않는다. 갈림목에 focal 하나.
# 이력: 2026-08-29 신설. 이 소절만 §3 에서 자기 도식이 없었고, 여덟 문단 위의 H2 도식을
#           "위 그림"으로 되짚고 있었다. nat-table-traverse 가 이미 그리는 mark 0x4000 · Pod/노드
#           분기는 여기서 다시 그리지 않는다.
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, PAPER2, KR, MONO

W, H = 1000, 608
X0, X1, GAP = 12, 972, 32
COLW = (X1 - X0 - GAP) / 2      # 464 — 갈래 둘이 반씩 쓴다
CX = W / 2
LEFT, RIGHT = X0, X0 + COLW + GAP

d = D(W, H, "BRANCH · 02-02 SNAT TARGETS",
      "주소를 언제 아는가 — SNAT 와 MASQUERADE 가 갈리는 곳",
      "출발지를 바꾸는 두 타깃은 규칙을 쓰는 시점에 넣을 주소를 아느냐로 갈린다. 알면 SNAT 가 값을 "
      "그대로 적고, 모르면 MASQUERADE 가 자리만 가리킨 뒤 패킷이 나갈 때 커널이 인터페이스에서 "
      "읽어 채운다. MASQUERADE 가 POSTROUTING 전용인 것도 나가는 인터페이스가 정해진 뒤라야 그 "
      "주소를 알 수 있기 때문이다.",
      lead="규칙을 쓰는 시점에 주소를 모르면 값을 적을 수 없습니다.")

# 갈림목 — focal 1곳
d.tone(CX - 176, 112, 352, 64, ACC, 6, "14", 1.4)
d.t(CX, 139, "규칙을 쓰는 시점에", 12, ACC, KR, "middle", 600)
d.t(CX, 160, "넣을 주소를 아는가?", 11, INK)

BRANCHES = [
    (LEFT,  OK,   "ok",   "안다", "주소가 고정이다",
     "값을 적는다",       "-j SNAT --to-source <주소>",
     "규칙을 쓸 때",      "값이 규칙 안에 박힌다",
     "값이 고정일 때",    "인터페이스를 조회하지 않아 약간 빠르다"),
    (RIGHT, WARN, "warn", "모른다", "DHCP 회선 · 뜰 때마다 IP 가 달라지는 클라우드",
     "자리를 가리킨다",   "-j MASQUERADE",
     "패킷이 나갈 때",    "커널이 그 인터페이스에서 읽어 채운다",
     "값이 바뀔 때",      "POSTROUTING 체인 전용"),
]

ROWS = (308, 372, 436)          # stride 64, 높이 56
LABELS = ("규칙에 적는 것", "값이 정해지는 시점", "언제 쓰나")

for x, c, mk, head, sub, *cells in BRANCHES:
    cx = x + COLW / 2
    d.arrow([(CX, 178), (CX, 204), (cx, 204), (cx, 229)], c, mk, 1.5)
    d.tone(x, 232, COLW, 60, c, 6, "14", 1.3)
    d.t(cx, 257, head, 12, c, KR, "middle", 600)
    d.t(cx, 278, sub, 10, INK)
    for i, y in enumerate(ROWS):
        top, val = cells[i * 2], cells[i * 2 + 1]
        d.box(x, y, COLW, 56, PAPER2, RULE, 0.9)
        d.t(x + 12, y + 20, LABELS[i], 9, SOFT, KR, "start")
        d.t(cx, y + 24, top, 12, c, KR, "middle", 600)
        mono = val.startswith("-j ")
        d.t(cx, y + 44, val, 11 if not mono else 10, INK if not mono else MUTED,
            KR if not mono else MONO)

d.t(CX, 524, "POSTROUTING 전용인 것도 같은 이유입니다 — 나가는 인터페이스가 정해진 뒤라야 그 주소를 알 수 있습니다.",
    10, ACC)
d.legend(544, [("SNAT — 값을 적는다", OK), ("MASQUERADE — 자리를 가리킨다", WARN)])
d.save("02-02.snat-vs-masquerade.svg")
print("ok snat-vs-masquerade")
