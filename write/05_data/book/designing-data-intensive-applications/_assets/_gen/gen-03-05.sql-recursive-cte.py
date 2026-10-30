# 03-05 §3 — SQL 재귀 CTE의 단계별 집합 확장 과정
# 사실 출처: 노트 L101~L127 (WITH RECURSIVE in_usa, edges 조인 반복, 고정점 도달, 최종 교집합 조인)
# 타입 스펙: type-process
import sys, pathlib
ASSETS = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ASSETS))
from dd import D, INK, MUTED, SOFT, ACC, OK, WARN, INFO, RULE, PAPER, PAPER2, KR, MONO

W = 880
H = 504
LEG = 448

d = D(W, H, "03-05 · SQL RECURSIVE CTE", "재귀 CTE의 반복별 집합 확장 과정",
      "WITH RECURSIVE in_usa 가 기준 정점부터 시작해 within 간선을 역추적하며 작업 집합을 확장하는 단계",
      lead="초기 앵커 조회에서 출발해, edges 조인을 반복하며 새로운 tail_vertex 가 없을 때까지 집합을 넓힙니다.")

# 4개 단계 컬럼 (x = 24, 236, 448, 660, w = 196)
COLS = [24, 236, 448, 660]
CW = 196

# 단계 1: 기저 쿼리 (반복 0)
d.box(COLS[0], 96, CW, 276, PAPER, RULE, 1.0)
d.box(COLS[0], 96, CW, 40, PAPER2, RULE, 1.0)
d.t(COLS[0] + 12, 120, "1단계 · 기저 쿼리", 12, INFO, KR, "start", 600)
d.t(COLS[0] + CW - 12, 120, "반복 0", 11, SOFT, MONO, "end")

d.t(COLS[0] + 16, 154, "SQL 실행", 12, SOFT, KR, "start")
d.box(COLS[0] + 12, 162, CW - 24, 52, PAPER2, RULE, 0.8)
d.t(COLS[0] + 20, 180, "SELECT vertex_id", 11, INK, MONO, "start")
d.t(COLS[0] + 20, 198, "… name='United States'", 11, MUTED, MONO, "start")

d.t(COLS[0] + 16, 232, "작업 집합 (in_usa)", 12, SOFT, KR, "start")
d.tone(COLS[0] + 12, 240, CW - 24, 56, INFO, 6, "14", 1.1)
d.t(COLS[0] + 20, 262, "{ US }", 12, INK, KR, "start", 600)
d.t(COLS[0] + 20, 282, "vertex_id: 2", 11, MUTED, MONO, "start")

d.t(COLS[0] + 16, 316, "동작 설명", 12, SOFT, KR, "start")
d.t(COLS[0] + 16, 334, "초기 앵커 정점 지정", 12, INK, KR, "start")
d.t(COLS[0] + 16, 352, "재귀 탐색의 기준점 설정", 12, MUTED, KR, "start")

# 화살표 1 -> 2
d.arrow([(COLS[0] + CW, 268), (COLS[1], 268)], WARN, "warn", 1.4)


# 단계 2: 1차 재귀 조인 (반복 1)
d.box(COLS[1], 96, CW, 276, PAPER, RULE, 1.0)
d.box(COLS[1], 96, CW, 40, PAPER2, RULE, 1.0)
d.t(COLS[1] + 12, 120, "2단계 · 1차 조인", 12, WARN, KR, "start", 600)
d.t(COLS[1] + CW - 12, 120, "반복 1", 11, SOFT, MONO, "end")

d.t(COLS[1] + 16, 154, "SQL 실행", 12, SOFT, KR, "start")
d.box(COLS[1] + 12, 162, CW - 24, 52, PAPER2, RULE, 0.8)
d.t(COLS[1] + 20, 180, "JOIN edges head=2", 11, INK, MONO, "start")
d.t(COLS[1] + 20, 198, "WHERE label='within'", 11, MUTED, MONO, "start")

d.t(COLS[1] + 16, 232, "작업 집합 (in_usa)", 12, SOFT, KR, "start")
d.tone(COLS[1] + 12, 240, CW - 24, 56, WARN, 6, "14", 1.1)
d.t(COLS[1] + 20, 262, "{ US, Idaho }", 12, INK, KR, "start", 600)
d.t(COLS[1] + 20, 282, "신규: Idaho (id: 3)", 12, WARN, KR, "start")

d.t(COLS[1] + 16, 316, "동작 설명", 12, SOFT, KR, "start")
d.t(COLS[1] + 16, 334, "within 간선 역추적", 12, INK, KR, "start")
d.t(COLS[1] + 16, 352, "tail 정점 추가 탐색", 12, MUTED, KR, "start")

# 화살표 2 -> 3
d.arrow([(COLS[1] + CW, 268), (COLS[2], 268)], OK, "ok", 1.4)


# 단계 3: 2차 재귀 조인 (반복 2)
d.box(COLS[2], 96, CW, 276, PAPER, RULE, 1.0)
d.box(COLS[2], 96, CW, 40, PAPER2, RULE, 1.0)
d.t(COLS[2] + 12, 120, "3단계 · 고정점 도달", 12, OK, KR, "start", 600)
d.t(COLS[2] + CW - 12, 120, "반복 2", 11, SOFT, MONO, "end")

d.t(COLS[2] + 16, 154, "SQL 실행", 12, SOFT, KR, "start")
d.box(COLS[2] + 12, 162, CW - 24, 52, PAPER2, RULE, 0.8)
d.t(COLS[2] + 20, 180, "JOIN edges head=3", 11, INK, MONO, "start")
d.t(COLS[2] + 20, 198, "추가 행 없음 (0건)", 12, MUTED, KR, "start")

d.t(COLS[2] + 16, 232, "작업 집합 (in_usa)", 12, SOFT, KR, "start")
d.tone(COLS[2] + 12, 240, CW - 24, 56, OK, 6, "14", 1.1)
d.t(COLS[2] + 20, 262, "{ US, Idaho }", 12, INK, KR, "start", 600)
d.t(COLS[2] + 20, 282, "재귀 탐색 종료 · 확정", 12, OK, KR, "start")

d.t(COLS[2] + 16, 316, "동작 설명", 12, SOFT, KR, "start")
d.t(COLS[2] + 16, 334, "더 이상 확장 없음", 12, INK, KR, "start")
d.t(COLS[2] + 16, 352, "in_usa 최종 완성", 12, MUTED, KR, "start")

# 화살표 3 -> 4
d.arrow([(COLS[2] + CW, 268), (COLS[3], 268)], ACC, "acc", 1.5)


# 단계 4: 최종 조인 (교집합 산출) - focal ACC
d.box(COLS[3], 96, CW, 276, PAPER, RULE, 1.0)
d.box(COLS[3], 96, CW, 40, PAPER2, ACC, 1.4)
d.t(COLS[3] + 12, 120, "4단계 · 최종 조인", 12, ACC, KR, "start", 600)
d.t(COLS[3] + CW - 12, 120, "결과", 11, ACC, MONO, "end")

d.t(COLS[3] + 16, 154, "SQL 실행", 12, SOFT, KR, "start")
d.box(COLS[3] + 12, 162, CW - 24, 52, PAPER2, RULE, 0.8)
d.t(COLS[3] + 20, 180, "born_in_usa", 11, INK, MONO, "start")
d.t(COLS[3] + 20, 198, "JOIN lives_in_europe", 11, MUTED, MONO, "start")

d.t(COLS[3] + 16, 232, "결과 레코드", 12, SOFT, KR, "start")
d.tone(COLS[3] + 12, 240, CW - 24, 56, ACC, 6, "18", 1.4)
d.t(COLS[3] + 20, 262, "{ \"Lucy\" }", 13, ACC, KR, "start", 600)
d.t(COLS[3] + 20, 282, "모든 조건 만족 대상", 12, INK, KR, "start")

d.t(COLS[3] + 16, 316, "동작 설명", 12, SOFT, KR, "start")
d.t(COLS[3] + 16, 334, "출생자 ∩ 거주자 교집합", 12, INK, KR, "start")
d.t(COLS[3] + 16, 352, "Cypher 4줄 vs SQL 31줄", 12, WARN, KR, "start")


# 하단 바: 비용 대비 요약
d.box(24, 388, 832, 44, PAPER, RULE, 1.0)
d.t(40, 415, "비용 요약: 가변 길이 경로 순회를 위해 CTE 4개(in_usa, in_europe, born_in_usa, lives_in_europe)와 다중 조인 필요", 12, INK, KR, "start", 600)


d.legend(LEG, [("최종 결과 도출", ACC), ("기저 앵커 (반복 0)", INFO), ("재귀 확장 (반복 1)", WARN), ("고정점 도달 (종료)", OK)])
d.save(str(ASSETS / "03-05.sql-recursive-cte.svg"))
print("ok 03-05.sql-recursive-cte")
