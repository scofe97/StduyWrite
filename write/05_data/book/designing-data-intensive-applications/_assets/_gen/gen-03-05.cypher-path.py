# 03-05 §2 — Cypher 가변 길이 경로(*0..)와 그래프 패턴 매칭
# 사실 출처: 노트 L77~L98 (Cypher MATCH 문, WITHIN*0.. 연산자, 미국 출생 및 유럽 거주 조건)
# 타입 스펙: type-data-flow
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, RULE, PAPER, PAPER2, KR, MONO

W = 880
H = 504
LEG = 448

d = D(W, H, "03-05 · CYPHER PATH TRAVERSAL", "가변 길이 경로와 그래프 패턴 매칭",
      "WITHIN*0.. 연산자가 서로 다른 깊이의 위치 계층을 순회해 미국과 유럽 목표 정점을 매칭하는 과정",
      lead="출생지는 1홉, 거주지는 3홉의 WITHIN 간선을 따라가며 동일 정점(Lucy)을 결과로 반환합니다.")

# 배경 컨테이너
d.box(24, 96, 832, 280, PAPER, RULE, 1.0)
d.t(40, 120, "Cypher 패턴 매칭 순회 경로 (MATCH (person)-[:BORN_IN]-> ... / -[:LIVES_IN]-> ...)", 13, INK, KR, "start", 600)

# 시작 정점: person (Lucy) - focal ACC
d.tone(40, 196, 128, 88, ACC, 6, "18", 1.4)
d.t(104, 222, "person 변수", 12, ACC, KR, "middle", 600)
d.t(104, 244, "Lucy", 14, INK, KR, "middle", 600)
d.t(104, 264, "label: Person", 11, MUTED, MONO, "middle")

# 경로 A: 출생지 경로 (상단)
# 직각 화살표: person -> BORN_IN -> Idaho
d.arrow([(168, 220), (208, 220), (208, 160), (244, 160)], ACC, "acc", 1.5)
d.chip(208, 186, "BORN_IN", ACC, 11)

# Idaho (state)
d.box(248, 134, 132, 52, PAPER2, INFO, 1.1)
d.t(314, 155, "Idaho", 13, INK, KR, "middle", 600)
d.t(314, 173, "state (0홉)", 12, MUTED, KR, "middle")

# WITHIN 1홉 화살표
d.arrow([(380, 160), (456, 160)], WARN, "warn", 1.5)
d.chip(418, 144, "WITHIN", WARN, 11)

# United States (매칭 성공!)
d.tone(460, 134, 172, 52, OK, 6, "16", 1.3)
d.t(546, 155, "United States", 13, OK, KR, "middle", 600)
d.t(546, 173, "매칭 완료 (1홉)", 12, OK, KR, "middle")

# 상위 계층 (North America)
d.arrow([(632, 160), (696, 160)], SOFT, "soft", 1.2, dash="3 3")
d.chip(664, 144, "WITHIN", SOFT, 11)
d.box(700, 134, 140, 52, PAPER2, RULE, 0.8)
d.t(770, 155, "North America", 13, MUTED, KR, "middle")
d.t(770, 173, "continent (2홉)", 12, SOFT, KR, "middle")


# 경로 B: 거주지 경로 (하단)
# 직각 화살표: person -> LIVES_IN -> London
d.arrow([(168, 260), (208, 260), (208, 320), (244, 320)], ACC, "acc", 1.5)
d.chip(208, 290, "LIVES_IN", ACC, 11)

# London (city)
d.box(248, 294, 104, 52, PAPER2, INFO, 1.1)
d.t(300, 315, "London", 13, INK, KR, "middle", 600)
d.t(300, 333, "city (0홉)", 12, MUTED, KR, "middle")

# WITHIN 1홉: London -> England
d.arrow([(352, 320), (412, 320)], WARN, "warn", 1.4)
d.chip(382, 304, "WITHIN", WARN, 11)
d.box(416, 294, 104, 52, PAPER2, INFO, 1.1)
d.t(468, 315, "England", 13, INK, KR, "middle", 600)
d.t(468, 333, "country (1홉)", 12, MUTED, KR, "middle")

# WITHIN 2홉: England -> United Kingdom (책 그림 3-6: type country)
d.arrow([(520, 320), (580, 320)], WARN, "warn", 1.4)
d.chip(550, 304, "WITHIN", WARN, 11)
d.box(584, 294, 84, 52, PAPER2, INFO, 1.1)
d.t(626, 315, "United Kingdom", 11, INK, KR, "middle", 600)
d.t(626, 333, "country (2홉)", 12, MUTED, KR, "middle")

# WITHIN 3홉: United Kingdom -> Europe (매칭 성공!)
d.arrow([(668, 320), (744, 320)], WARN, "warn", 1.4)
d.chip(706, 304, "WITHIN", WARN, 11)
d.tone(748, 294, 100, 52, OK, 6, "16", 1.3)
d.t(798, 315, "Europe", 13, OK, KR, "middle", 600)
d.t(798, 333, "매칭 완료 (3홉)", 12, OK, KR, "middle")


# 하단 요약 바 (교집합 결과)
d.box(24, 388, 832, 44, PAPER, RULE, 1.0)
d.t(40, 415, "교집합 평가: BORN_IN 경로(1홉 매칭) ∩ LIVES_IN 경로(3홉 매칭) → RETURN person.name: \"Lucy\"", 12, INK, KR, "start", 600)


d.legend(LEG, [("매칭 대상 (person)", ACC), ("목표 위치 매칭 완료", OK), ("가변 경로 순회 (*0..)", WARN), ("중간 위치 정점", INFO)])
d.save(str(ASSETS / "03-05.cypher-path.svg"))
print("ok 03-05.cypher-path")
