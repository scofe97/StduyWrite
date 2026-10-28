# 03-04 §2 — schema-on-read 와 schema-on-write 를 쓰기·저장·읽기 순서로 나란히 놓고, 구조를 다루는 시점을 강조한다.
# 옛 도식의 장단점 격자는 뺐다. §2 본문 산문과 §1 표가 맡는다.
# 타입 스펙: type-timeline
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY, PH = 100, 252
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-04 · SCHEMA ON READ VS WRITE", "구조를 다루는 시점",
      "schema-on-read 는 읽을 때 구조를 해석하고 schema-on-write 는 쓸 때 데이터베이스가 적합성을 보장한다.",
      "쓰기 · 저장 · 읽기 순서의 비교")

LANES = [
    (104, "schema-on-read", "동적(런타임) 타입 체크와 유사",
     [("쓰기", "임의의 키·값 추가", False), ("저장", "암묵적 스키마", False), ("읽기", "읽을 때 구조 해석", True)]),
    (232, "schema-on-write", "정적(컴파일 타임) 타입 체크와 유사",
     [("쓰기", "적합성 보장", True), ("저장", "명시적 스키마", False), ("읽기", "스키마에 맞는 데이터", False)]),
]
XS = [304, 504, 704]
for y, name, hint, nodes in LANES:
    d.box(16, y, 848, 116, PAPER, RULE, 0.9)
    d.t(32, y + 52, name, 14, INK, MONO, "start", 600)
    d.t(32, y + 76, hint, 12, MUTED, KR, "start")
    for x, (a, b, hot) in zip(XS, nodes):
        d.box(x, y + 24, 144, 68, PAPER2, ACC if hot else INFO, 1.6 if hot else 1.2)
        d.t(x + 72, y + 52, a, 14, INK, KR, "middle", 600)
        d.t(x + 72, y + 76, b, 12, ACC if hot else MUTED, KR)
    for x in XS[:2]:
        d.arrow([(x + 148, y + 58), (x + 196, y + 58)], MUTED, "ar", 1.4)

d.legend(LEG, [("구조를 다루는 시점", ACC), ("단계", INFO)])
d.save("03-04.schema-on-read-write.svg")
