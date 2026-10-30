# 03-05 §5 — Datalog 기본 사실에서 파생 규칙을 거쳐 최종 결과를 도출하는 파생 트리
# 사실 출처: 노트 L177~L201 (Datalog fact, rule 1~4, within_recursive, migrated, us_to_europe)
# 타입 스펙: type-tree
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, RULE, PAPER, PAPER2, KR, MONO

W = 880
H = 504
LEG = 448

d = D(W, H, "03-05 · DATALOG DERIVATION TREE", "Datalog 규칙과 사실의 파생 트리",
      "기본 사실(fact)에서 출발해 재귀 규칙으로 가상 뷰를 합성하고 최종 질의 목표를 도출하는 구조",
      lead="하단의 기본 사실들이 규칙 1·2를 통해 재귀 집합으로 합성되고, 규칙 3·4를 거쳐 최종 결과를 도출합니다.")

# 루트 노드: 최종 질의 목표 us_to_europe (Tier 0, focal ACC)
rx, ry, rw, rh = 340, 96, 200, 48
d.tone(rx, ry, rw, rh, ACC, 6, "18", 1.4)
d.t(rx + rw // 2, ry + 22, 'us_to_europe("Lucy")', 13, ACC, MONO, "middle", 600)
d.t(rx + rw // 2, ry + 38, "최종 질의 목표 · 규칙 4", 12, INK, KR, "middle")

# Root -> Tier 1 연결
d.line(440, ry + rh, 440, 168, RULE, 1.2)

# Tier 1 노드: migrated (규칙 3) — 값은 책 예제 3-11 그대로라 폭을 넓힌다
t1x, t1y, t1w, t1h = 280, 168, 320, 48
d.tone(t1x, t1y, t1w, t1h, INFO, 6, "14", 1.2)
d.t(t1x + t1w // 2, t1y + 22, 'migrated("Lucy", "United States", "Europe")', 12, INK, MONO, "middle", 600)
d.t(t1x + t1w // 2, t1y + 38, "파생 가상 뷰 · 규칙 3", 12, INFO, KR, "middle")

# Tier 1 -> Tier 2 버스 및 수직선
# Tier 2 노드 중심: C0=99, C1=248, C2=446, C3=719
d.line(440, t1y + t1h, 440, 238, RULE, 1.2)
d.line(99, 238, 719, 238, RULE, 1.2)
for cx in [99, 248, 446, 719]:
    d.line(cx, 238, cx, 256, RULE, 1.2)

# Tier 2 노드들 (y = 256, h = 52)
# Node 0: person 사실
d.box(24, 256, 150, 52, PAPER2, RULE, 1.0)
d.t(99, 278, 'person(100, "Lucy")', 12, INK, MONO, "middle")
d.t(99, 296, "기본 사실 (person)", 12, MUTED, KR, "middle")

# Node 1: born_in 사실
d.box(186, 256, 124, 52, PAPER2, RULE, 1.0)
d.t(248, 278, "born_in(100, 3)", 12, INK, MONO, "middle")
d.t(248, 296, "기본 사실 (born_in)", 12, MUTED, KR, "middle")

# Node 2: within_recursive (미국)
d.tone(322, 256, 248, 52, WARN, 6, "14", 1.2)
d.t(446, 278, 'within_recursive(3, "United States")', 11, WARN, MONO, "middle")
d.t(446, 296, "재귀 파생 규칙 2", 12, INK, KR, "middle")

# Node 3: lives_in + within_recursive (유럽)
d.box(582, 256, 274, 52, PAPER2, INFO, 1.0)
d.t(719, 278, 'lives_in + within_recursive', 12, INK, MONO, "middle")
d.t(719, 296, "유럽 거주 파생 조건", 12, MUTED, KR, "middle")


# Node 2 -> Tier 3 버스 및 수직선
# Tier 3 서브노드 중심: S1=370, S2=560
d.line(446, 308, 446, 332, RULE, 1.2)
d.line(370, 332, 560, 332, RULE, 1.2)
d.line(370, 332, 370, 348, RULE, 1.2)
d.line(560, 332, 560, 348, RULE, 1.2)

# Tier 3 노드들 (y = 348, h = 52)
# Subnode 2A: within(3, 2)
d.box(306, 348, 128, 52, PAPER2, RULE, 1.0)
d.t(370, 370, "within(3, 2)", 12, INK, MONO, "middle")
d.t(370, 388, "기본 사실 (within)", 12, MUTED, KR, "middle")

# Subnode 2B: location 기저 사실 (규칙 1)
d.tone(450, 348, 220, 52, OK, 6, "14", 1.2)
d.t(560, 370, 'location(2, "United States", _)', 11, OK, MONO, "middle")
d.t(560, 388, "기저 사실 · 규칙 1 매칭", 12, INK, KR, "middle")


d.legend(LEG, [("질의 목표 (도출 결과)", ACC), ("파생 뷰 (규칙 3)", INFO), ("재귀 규칙 (규칙 2)", WARN), ("기저 앵커 (규칙 1)", OK)])
d.save(str(ASSETS / "03-05.datalog-rules.svg"))
print("ok 03-05.datalog-rules")
