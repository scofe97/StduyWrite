# 04-03.label-selector — 같은 네 연산자도 라벨이 없는 Pod 를 다르게 다룬다
# 본문 요구: 「LabelSelector 연산자 넷」 — In·NotIn·Exists·DoesNotExist. NotIn 은 값이 목록 밖인 리소스에 더해 그 키가 없는 리소스도 매칭한다.
# 타입 스펙: type-dp-security-matrix — 행이 연산자 넷, 열이 Pod 둘(A: app=web,tier=frontend / B: app=web). 셀은 매칭 여부와 이유 한 줄.
#           focal 은 NotIn 이 키가 없는 Pod B 를 매칭하는 셀 하나.
import ddx
from dd import D, INK, MUTED, SOFT, RULE, ACC, OK, PAPER, PAPER2, KR, MONO

W, H = 1000, 568
d = D(W, H, "LABELSELECTOR · FOUR OPERATORS",
      "같은 네 연산자도 라벨이 없는 Pod 를 다르게 다룬다",
      "tier 키를 기준으로 In 은 Pod A 만, NotIn 은 값이 목록 밖이거나 키가 없는 Pod B 를, Exists 는 A 만, DoesNotExist 는 B 만 고른다. "
      "In 과 NotIn 은 values 가 비어 있으면 안 되고 Exists 와 DoesNotExist 는 비어 있어야 한다.",
      lead="NotIn 은 키가 없는 Pod 도 고릅니다")

COLS = [(40, 376, "셀렉터 · tier 기준"), (432, 252, "Pod A · app=web, tier=frontend"), (700, 252, "Pod B · app=web")]
HY, RY0, RH, GAP = 136, 152, 72, 12
for x, w, name in COLS:
    d.t(x + w // 2, HY, ddx.fit(name, 12, w - 8, name), 12, SOFT, KR, "middle", 600)

# (연산자 줄, values 규칙, A 셀, B 셀) — 셀 = (매칭 여부, 이유)
ROWS = [
    ("In  tier [frontend]", "values 가 비어 있으면 안 됨",
     (True, "tier=frontend 가 목록 안"), (False, "tier 키가 없음")),
    ("NotIn  tier [frontend]", "values 가 비어 있으면 안 됨",
     (False, "tier=frontend 가 목록 안"), (True, "키가 없어도 매칭")),
    ("Exists  tier", "values 는 비어 있어야 함",
     (True, "tier 키가 있음"), (False, "tier 키가 없음")),
    ("DoesNotExist  tier", "values 는 비어 있어야 함",
     (False, "tier 키가 있음"), (True, "tier 키가 없음")),
]

for r, (op, rule, a, b) in enumerate(ROWS):
    y = RY0 + r * (RH + GAP)
    x, w, _ = COLS[0]
    d.box(x, y, w, RH, PAPER2, RULE, 1.0, 6)
    d.t(x + 20, y + 31, ddx.fit(op, 14, w - 40, op), 14, INK, MONO, "start", 600)
    d.t(x + 20, y + 54, rule, 12, MUTED, KR, "start")
    for ci, (hit, why) in ((1, a), (2, b)):
        x, w, _ = COLS[ci]
        focal = (r == 1 and ci == 2)
        if focal:
            d.tone(x, y, w, RH, ACC, 6, "1F", 1.6)
            tc = ACC
        elif hit:
            d.tone(x, y, w, RH, OK, 6, "14", 1.1)
            tc = OK
        else:
            d.box(x, y, w, RH, PAPER, RULE, 0.9, 6)
            tc = SOFT
        d.t(x + w // 2, y + 31, "매칭" if hit else "불일치", 14, tc, KR, "middle", 600)
        d.t(x + w // 2, y + 54, ddx.fit(why, 12, w - 20, why), 12, ACC if focal else MUTED, KR, "middle")

d.legend(520, [("매칭", OK), ("키가 없어서 매칭", ACC), ("불일치", SOFT)])
d.save("04-03.label-selector.svg")
print("ok label-selector")
