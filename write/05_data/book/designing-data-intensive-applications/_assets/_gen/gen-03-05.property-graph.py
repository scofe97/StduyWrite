# 03-05 §1 — 속성 그래프의 정점과 간선 실제 구조 및 관계형 테이블 표현
# 사실 출처: 노트 L39~L64 (정점·간선 정의, SQL 스키마, 양방향 인덱스, 실제 레코드 예)
# 타입 스펙: type-architecture
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, INFO, RULE, PAPER, PAPER2, KR, MONO

W = 880
H = 504
LEG = 448

d = D(W, H, "03-05 · PROPERTY GRAPH", "속성 그래프의 정점과 간선 구조",
      "정점과 간선은 고유 ID·label·JSON 속성을 가지며, 간선 테이블의 꼬리·머리 외래 키로 그래프를 연결합니다.",
      lead="윗단은 관계형 테이블 저장 표현, 아랫단은 정점과 간선으로 순회하는 그래프 모델입니다.")

# 윗단: 관계형 저장소 표현 (vertices, edges 테이블)
d.box(24, 96, 832, 172, PAPER, RULE, 1.0)
d.t(40, 120, "관계형 테이블 저장 표현 (PostgreSQL jsonb 스키마)", 13, INK, KR, "start", 600)
d.t(840, 120, "CREATE TABLE vertices · edges", 11, SOFT, MONO, "end")

# vertices 테이블 (x=40, w=380)
d.box(40, 134, 380, 120, PAPER2, RULE, 1.0)
d.t(56, 154, "vertices 테이블 (정점 저장소)", 12, INFO, KR, "start", 600)
# 헤더행
d.box(48, 164, 364, 20, PAPER, RULE, 0.6)
d.t(60, 178, "vertex_id (PK)", 11, SOFT, MONO, "start")
d.t(168, 178, "label", 11, SOFT, MONO, "start")
d.t(248, 178, "properties (jsonb)", 11, SOFT, MONO, "start")
# 데이터행 1
d.t(60, 198, "100", 11, INK, MONO, "start")
d.t(168, 198, "Person", 11, INK, KR, "start")
d.t(248, 198, '{"name": "Lucy"}', 11, MUTED, MONO, "start")
# 데이터행 2
d.t(60, 218, "3", 11, INK, MONO, "start")
d.t(168, 218, "Location", 11, INK, KR, "start")
d.t(248, 218, '{"name": "Idaho"}', 11, MUTED, MONO, "start")
# 데이터행 3
d.t(60, 238, "2", 11, INK, MONO, "start")
d.t(168, 238, "Location", 11, INK, KR, "start")
d.t(248, 238, '{"name": "United States"}', 11, MUTED, MONO, "start")

# edges 테이블 (x=436, w=404)
d.box(436, 134, 404, 120, PAPER2, RULE, 1.0)
d.t(452, 154, "edges 테이블 (간선 저장소 · 인덱스)", 12, ACC, KR, "start", 600)
# 헤더행
d.box(444, 164, 388, 20, PAPER, RULE, 0.6)
d.t(452, 178, "edge_id (PK)", 11, SOFT, MONO, "start")
d.t(536, 178, "tail (FK)", 11, SOFT, MONO, "start")
d.t(600, 178, "head (FK)", 11, SOFT, MONO, "start")
d.t(664, 178, "label", 11, SOFT, MONO, "start")
d.t(736, 178, "properties", 11, SOFT, MONO, "start")
# 데이터행 1
d.t(452, 198, "1", 11, INK, MONO, "start")
d.t(536, 198, "100", 11, OK, MONO, "start")
d.t(600, 198, "3", 11, OK, MONO, "start")
d.t(664, 198, "born_in", 11, ACC, MONO, "start")
d.t(736, 198, '{}', 11, MUTED, MONO, "start")
# 데이터행 2
d.t(452, 218, "2", 11, INK, MONO, "start")
d.t(536, 218, "3", 11, OK, MONO, "start")
d.t(600, 218, "2", 11, OK, MONO, "start")
d.t(664, 218, "within", 11, ACC, MONO, "start")
d.t(736, 218, '{}', 11, MUTED, MONO, "start")
# 인덱스 안내
d.t(452, 240, "인덱스: edges_tails (tail_vertex) · edges_heads (head_vertex)", 11, OK, KR, "start")


# 아랫단: 속성 그래프 모델 뷰
d.box(24, 284, 832, 144, PAPER, RULE, 1.0)
d.t(40, 308, "속성 그래프 표현 뷰 (정점 노드와 방향성 간선)", 13, INK, KR, "start", 600)

# 정점 1: Lucy (x=40, y=328, w=212, h=84)
d.tone(40, 328, 212, 84, INFO, 6, "14", 1.2)
d.t(56, 350, "정점 id: 100 · Person", 13, INK, KR, "start", 600)
d.line(52, 358, 240, 358, RULE, 0.6)
d.t(56, 376, "name: \"Lucy\"", 12, MUTED, MONO, "start")
d.t(56, 396, "나가는 간선: [edge 1]", 12, OK, KR, "start")

# 간선 1: born_in (x=252 to 348)
d.arrow([(252, 370), (344, 370)], ACC, "acc", 1.8)
d.chip(298, 348, "born_in", ACC, 11)
d.t(298, 392, "edge_id: 1", 11, MUTED, MONO, "middle")

# 정점 2: Idaho (x=348, y=328, w=212, h=84)
d.tone(348, 328, 212, 84, INFO, 6, "14", 1.2)
d.t(364, 350, "정점 id: 3 · Location", 13, INK, KR, "start", 600)
d.line(360, 358, 548, 358, RULE, 0.6)
d.t(364, 376, "name: \"Idaho\"", 12, MUTED, MONO, "start")
d.t(364, 396, "type: \"state\"", 12, MUTED, MONO, "start")

# 간선 2: within (x=560 to 656)
d.arrow([(560, 370), (652, 370)], ACC, "acc", 1.8)
d.chip(606, 348, "within", ACC, 11)
d.t(606, 392, "edge_id: 2", 11, MUTED, MONO, "middle")

# 정점 3: United States (x=656, y=328, w=188, h=84)
d.tone(656, 328, 188, 84, INFO, 6, "14", 1.2)
d.t(672, 350, "정점 id: 2 · Location", 13, INK, KR, "start", 600)
d.line(668, 358, 832, 358, RULE, 0.6)
d.t(672, 376, "name: \"United States\"", 12, MUTED, MONO, "start")
d.t(672, 396, "type: \"country\"", 12, MUTED, MONO, "start")


d.legend(LEG, [("간선 · 관계 (꼬리 → 머리)", ACC), ("정점 · 엔티티", INFO), ("외래 키 연결 · 인덱스", OK)])
d.save(str(ASSETS / "03-05.property-graph.svg"))
print("ok 03-05.property-graph")
