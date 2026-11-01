# 06-03 §2 — 네임스페이스 이름 질의에 NXDOMAIN 과 데이터 없는 NOERROR 를 가르려면 네임스페이스를 알아야 한다.
# 본문 근거: 이 노트 §2 「왜 네임스페이스를 읽어야 하는가」 첫째 이유(원서 요지 — 그 네임스페이스에 서비스가 있으면 NXDOMAIN 을 주면 안 된다).
#            질의 이름은 원서·본문의 namespace.svc.cluster.local 하나만 쓴다(구체 네임스페이스 이름은 원서에 없음).
# 원서 근거: 6장 "Kubernetes" p.25("Role-Based Access Control" 안 namespaces 단락, "NXDOMAIN or SUCCESS with no data").
# 타입 스펙: type-dp-security-matrix — 질의(행) × 상태·응답·이유(열) 격자에서 응답 칸의 차이가 논지다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, BAD, KR, MONO

W, H = 880, 390
d = D(W, H, "LEARNING COREDNS · 06-03 §2",
      "없는 이름과 비어 있는 이름을 가른다",
      "네임스페이스 이름만 물으면 그 이름에 붙은 레코드는 없다. 그래도 아래에 서비스 이름이 있으면 없는 이름이 아니므로 "
      "데이터 없는 SUCCESS 로 답하고, 네임스페이스가 없을 때만 NXDOMAIN 을 준다.",
      "주황 칸이 네임스페이스를 알아야 고를 수 있는 답입니다")

COLS = [(20, 250, "질의 이름"), (280, 190, "네임스페이스"), (480, 170, "응답"), (660, 200, "왜")]
rows = [
    ("namespace.svc.cluster.local", ("있음", "서비스 하나 이상"), ("SUCCESS", "데이터 없음"), ("하위 이름 존재", "없는 이름 아님"), True),
    ("namespace.svc.cluster.local", ("없음", ""), ("NXDOMAIN", ""), ("하위 이름 없음", "없는 이름"), False),
]
for x, w, head in COLS:
    d.t(x + 12, 118, head, 12, SOFT, KR, "start", 600)

for i, (q, ns, ans, why, focal) in enumerate(rows):
    y = 132 + i * 84
    for k, (x, w, _) in enumerate(COLS):
        if k == 2 and focal:
            d.tone(x, y, w, 72, ACC, 6, "12", 1.4)
        else:
            d.box(x, y, w, 72, PAPER2, RULE, 1.0, 6)
    d.t(32, y + 41, q, 12, INK, MONO, "start", 600)
    for (x, w, _), (m, sub), c in ((COLS[1], ns, INK), (COLS[2], ans, ACC if focal else BAD), (COLS[3], why, INK)):
        fam = MONO if m.isascii() else KR
        if sub:
            d.t(x + 12, y + 30, m, 14, c, fam, "start", 600)
            d.t(x + 12, y + 52, sub, 12, MUTED, KR, "start")
        else:
            d.t(x + 12, y + 41, m, 14, c, fam, "start", 600)

d.t(20, 324, "둘을 가르는 근거 · 네임스페이스 목록 · namespaces 권한", 13, MUTED, KR, "start")

d.legend(344, [("네임스페이스를 알아야 고르는 답", ACC), ("없는 이름", BAD)])
d.save("06-03.ns-nxdomain.svg")
