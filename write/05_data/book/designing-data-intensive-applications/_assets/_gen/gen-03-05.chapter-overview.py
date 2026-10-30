# 03-05 개요 — 속성 그래프·트리플 두 저장 모델과 네 쿼리 언어(Cypher·SQL CTE·SPARQL·Datalog)·GraphQL의 관계
# 사실 출처: 노트 L28~L33(전체 구조), §1 L36~L45, §2 L77~L85, §3 L101~L107, §4 L131~L140, §5 L177~L182, §6 L204~L210
# 타입 스펙: type-architecture
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, RULE, PAPER, PAPER2, KR, MONO

W = 880
H = 504
LEG = 448

d = D(W, H, "03-05 · CHAPTER OVERVIEW", "그래프 데이터 모델과 쿼리 언어 지형",
      "속성 그래프와 트리플 스토어의 두 저장 모델, 그리고 Cypher·SQL CTE·SPARQL·Datalog·GraphQL 다섯 질의 방식의 관계",
      lead="윗단은 저장 모델과 쿼리 언어 대응, 아랫단은 클라이언트 관점의 제한적 쿼리 모델입니다.")

# 좌측 영역: 속성 그래프 계열 (x=24, w=396)
d.box(24, 96, 396, 232, PAPER, RULE, 1.0)
d.t(40, 122, "속성 그래프 계열", 13, INK, KR, "start", 600)
d.t(396, 122, "§1 · §2 · §3", 11, SOFT, MONO, "end")

# §1 속성 그래프 저장 모델
d.tone(40, 138, 364, 48, INFO, 6, "14", 1.1)
d.t(56, 160, "§1 속성 그래프 저장 모델", 13, INK, KR, "start", 600)
d.t(56, 176, "정점(id·label·속성) + 간선(꼬리·머리·label·속성)", 12, MUTED, KR, "start")

# §2 Cypher (focal)
d.tone(40, 196, 364, 48, ACC, 6, "18", 1.4)
d.t(56, 218, "§2 Cypher — 선언형 그래프 쿼리", 13, ACC, KR, "start", 600)
d.t(56, 234, "화살표 표기 · 가변 길이 경로 (*0..)", 12, INK, KR, "start")

# §3 SQL 재귀 CTE
d.box(40, 254, 364, 48, PAPER2, WARN, 1.1)
d.t(56, 276, "§3 SQL 재귀 CTE — 관계형 조인", 13, WARN, KR, "start", 600)
d.t(56, 292, "WITH RECURSIVE · edges 조인 반복 (31줄)", 12, MUTED, KR, "start")


# 우측 영역: 트리플 스토어 및 규칙 계열 (x=460, w=396)
d.box(460, 96, 396, 232, PAPER, RULE, 1.0)
d.t(476, 122, "트리플 스토어 및 규칙 계열", 13, INK, KR, "start", 600)
d.t(832, 122, "§4 · §5", 11, SOFT, MONO, "end")

# §4 트리플 스토어 저장 모델
d.tone(476, 138, 364, 48, INFO, 6, "14", 1.1)
d.t(492, 160, "§4 트리플 스토어 모델", 13, INK, KR, "start", 600)
d.t(492, 176, "(주어, 술어, 목적어) 세 부분 문장 · RDF", 12, MUTED, KR, "start")

# §4 SPARQL
d.box(476, 196, 364, 48, PAPER2, OK, 1.1)
d.t(492, 218, "§4 SPARQL — RDF 선언형 쿼리", 13, OK, KR, "start", 600)
d.t(492, 234, "트리플 패턴 매칭 · Cypher 와 유사한 표현", 12, MUTED, KR, "start")

# §5 Datalog
d.box(476, 254, 364, 48, PAPER2, OK, 1.1)
d.t(492, 276, "§5 Datalog — 규칙 기반 재귀 쿼리", 13, OK, KR, "start", 600)
d.t(492, 292, "기본 사실(fact) → 규칙 정의를 통한 뷰 파생", 12, MUTED, KR, "start")


# 저장 모델 간 동등 연결 (행 1 중앙)
d.line(404, 162, 424, 162, RULE, 1.0, "2 2")
d.line(456, 162, 476, 162, RULE, 1.0, "2 2")
d.box(424, 150, 32, 24, PAPER, RULE, 0.8, r=4)
d.t(440, 166, "동등", 11, MUTED, KR, "middle")


# 하단 영역: §6 GraphQL (x=24, w=832)
d.box(24, 344, 832, 80, PAPER, RULE, 1.0)
d.t(40, 368, "§6 GraphQL — 클라이언트 UI 질의 계층", 13, INK, KR, "start", 600)
d.box(320, 355, 68, 18, PAPER2, WARN, 0.8, r=3)
d.t(354, 368, "의도적 제약", 11, WARN, KR, "middle")

d.t(40, 390, "UI 렌더링에 필요한 필드만 담은 JSON 문서를 요청", 12, MUTED, KR, "start")
d.t(40, 408, "신뢰할 수 없는 클라이언트 보호 목적: 재귀 탐색 차단 · 임의 검색 불가", 12, WARN, KR, "start")

d.box(576, 356, 264, 56, PAPER2, RULE, 1.0)
d.t(708, 378, "모바일 앱 · 웹 프론트엔드용", 12, INK, KR, "middle")
d.t(708, 398, "백엔드 DB 유형(관계형·문서·그래프) 무관", 12, MUTED, KR, "middle")


d.legend(LEG, [("핵심 선언형 언어", ACC), ("저장 모델", INFO), ("재귀 비용·제약", WARN), ("다른 그래프 쿼리 언어", OK)])
d.save(str(ASSETS / "03-05.chapter-overview.svg"))
print("ok 03-05.chapter-overview")
