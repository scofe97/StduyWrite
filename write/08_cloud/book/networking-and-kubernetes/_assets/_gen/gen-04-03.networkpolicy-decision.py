# 04-03.networkpolicy-decision — 정책 하나가 연결 셋을 판정하는 값 흐름
# 본문 요구: 「선택·잠금 규칙 셋과 오해 둘」 — 격리는 방향마다, 허용 목록은 합집합, 연결은 양쪽 모두 통과해야 한다.
# 타입 스펙: type-flowchart — 정책 패널(값의 출처) 아래에 연결 셋을 행으로 놓고, 행마다 선택·방향 → 허용 목록 대조 → 결과로 흐른다.
#           칸에는 세 단계 조이기 실측의 실제 값(demo-db-allow-demo, app=demo, TCP 80)만 적는다. focal 은 정책 패널 하나.
#           2026-11-08 추상 네 단계 체인에서 값 흐름으로 다시 그렸다.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 604
d = D(W, H, "NetworkPolicy · WHEN IT LOCKS",
      "연결 하나는 선택 · 방향 · 허용 목록 세 관문을 지난다",
      "정책 demo-db-allow-demo 가 걸린 demo-db 에서 연결 셋이 판정된다. demo 에서 오는 80번 연결은 허용 목록과 맞아 통과하고, "
      "other 에서 오는 연결은 목록에 없어 차단되며, demo-db 가 새로 거는 연결은 egress 허용이 없어 차단된다.",
      lead="선택된 방향은 허용 목록에 있는 연결만 통과합니다")

# 값의 출처 — 정책 패널
PX, PY, PW, PH = 24, 104, 952, 76
d.tone(PX, PY, PW, PH, ACC, 8, "1F", 1.6)
d.t(PX + 18, PY + 28, "정책 demo-db-allow-demo", 14, ACC, KR, "start", 600)
d.t(PX + 18, PY + 54, ddx.fit("선택 app=demo-db  ·  방향 Ingress, Egress  ·  ingress 허용 from app=demo, TCP 80  ·  egress 허용 없음",
                              12, PW - 36, "panel"), 12, MUTED, KR, "start")

COLS = [(40, 200, "연결"), (276, 220, "선택 · 방향"), (532, 220, "허용 목록 대조"), (788, 172, "결과")]
HY = 220
for x, w, name in COLS:
    d.t(x + w // 2, HY, name, 12, SOFT, KR, "middle", 600)

NH, Y0, STRIDE = 72, 240, 100
ROWS = [
    ("demo → demo-db", "TCP 80 · 받는 쪽 ingress",
     ("demo-db 선택됨", "Ingress 격리"), ("from app=demo · 80", "라벨 · 포트 일치", OK),
     ("통과", "응답도 함께 통과", OK)),
    ("other → demo-db", "TCP 80 · 받는 쪽 ingress",
     ("demo-db 선택됨", "Ingress 격리"), ("라벨 app=other", "from 목록에 없음", BAD),
     ("차단", "ingress 허용 밖", BAD)),
    ("demo-db → web", "TCP 80 · 보내는 쪽 egress",
     ("demo-db 선택됨", "Egress 격리"), ("egress 규칙 0개", "허용 목록이 비었음", BAD),
     ("차단", "새로 거는 연결", BAD)),
]


def cell(col, y, title, sub, c, mono=False):
    x, w, _ = COLS[col]
    d.box(x, y, w, NH, "#161B22", c or RULE, 1.1, 6)
    tc = c or INK
    d.t(x + w // 2, y + 31, ddx.fit(title, 13, w - 20, title), 13, tc, MONO if mono else KR, "middle", 600)
    d.t(x + w // 2, y + 54, ddx.fit(sub, 12, w - 20, sub), 12, MUTED, KR, "middle")


for i, (ct, cs, (st, ss), (lt, ls, lc), (rt, rs, rc)) in enumerate(ROWS):
    y = Y0 + i * STRIDE
    cell(0, y, ct, cs, None, True)
    cell(1, y, st, ss, INFO)
    cell(2, y, lt, ls, lc)
    cell(3, y, rt, rs, rc)
    cy = y + NH // 2
    d.arrow([(COLS[0][0] + COLS[0][1] + 3, cy), (COLS[1][0] - 5, cy)], SOFT, "soft", 1.4)
    d.arrow([(COLS[1][0] + COLS[1][1] + 3, cy), (COLS[2][0] - 5, cy)], SOFT, "soft", 1.4)
    d.arrow([(COLS[2][0] + COLS[2][1] + 3, cy), (COLS[3][0] - 5, cy)], OK if rc == OK else BAD,
            "ok" if rc == OK else "bad", 1.5, None if rc == OK else "6 5")

d.legend(560, [("정책 값의 출처", ACC), ("선택 · 방향 판정", INFO), ("통과", OK), ("차단", BAD)])
d.save("04-03.networkpolicy-decision.svg")
print("ok networkpolicy-decision")
