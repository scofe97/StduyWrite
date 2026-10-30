# 03-01 §1 — 명령형 루프와 선언형 쿼리(SQL → 옵티마이저 → 실행 계획)의 처리 흐름 비교.
# 사실 출처: 03-01 §1(L42~L48), 원서 Ch.3 Relational Versus Document Models §Declarative Queries on the Web
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
Y1, Y2 = 128, 276
BH = 104
LEG = Y2 + BH + 32
H = LEG + 56

d = D(W, H, "03-01 · DECLARATIVE QUERY", "명령형 루프 대 선언형 쿼리 파이프라인",
      "선언형은 결과 조건만 명시하고 옵티마이저가 인덱스와 조인 순서를 결정해, 쿼리 수정 없이 병렬 실행과 최적화를 얻는다.",
      "명령형 알고리즘 고정 · 선언형 쿼리 옵티마이저 · 자동 병렬 실행")

# 트랙 머리 라벨
d.tone(24, 96, 192, 24, WARN, 4, "18", 1.0)
d.t(120, 112, "명령형 · Python / Java", 12, WARN, KR, "middle", 600)

d.tone(24, 244, 192, 24, ACC, 4, "1F", 1.2)
d.t(120, 260, "선언형 · SQL / Cypher", 12, ACC, KR, "middle", 600)

# 단계 컬럼 좌표: 3개 열 (w=236, gap=60)
# col0: 24 ~ 260, col1: 320 ~ 556, col2: 616 ~ 856
col_x = [24, 320, 616]
col_w = [236, 236, 240]

# --- 1. 명령형 트랙 ---
# 1-1. 질의 작성
d.box(col_x[0], Y1, col_w[0], BH, PAPER2, RULE, 0.9)
d.t(col_x[0] + col_w[0] / 2, Y1 + 24, "프로그래머 알고리즘 명시", 13, INK, KR, "middle", 600)
d.t(col_x[0] + col_w[0] / 2, Y1 + 46, "연산 순서와 제어 흐름 직접 지시", 12, MUTED, KR, "middle")
d.box(col_x[0] + 16, Y1 + 60, col_w[0] - 32, 28, PAPER, RULE, 0.8)
d.t(col_x[0] + col_w[0] / 2, Y1 + 78, "for · if 반복문", 12, MUTED, KR, "middle")

# 1-2. 처리 엔진
d.box(col_x[1], Y1, col_w[1], BH, PAPER2, RULE, 0.9)
d.t(col_x[1] + col_w[1] / 2, Y1 + 24, "고정 순차 처리", 13, INK, KR, "middle", 600)
d.t(col_x[1] + col_w[1] / 2, Y1 + 46, "작성된 반복문대로 순차 실행", 12, MUTED, KR, "middle")
d.box(col_x[1] + 16, Y1 + 60, col_w[1] - 32, 28, PAPER, RULE, 0.8)
d.t(col_x[1] + col_w[1] / 2, Y1 + 78, "연산 순서 = 코드 순서", 12, MUTED, KR, "middle")

# 1-3. 실행과 확장
d.tone(col_x[2], Y1, col_w[2], BH, WARN, 6, "18", 1.2)
d.t(col_x[2] + col_w[2] / 2, Y1 + 24, "최적화 도입의 한계", 13, WARN, KR, "middle", 600)
d.t(col_x[2] + col_w[2] / 2, Y1 + 46, "다중 코어 병렬화 수동 구현 필요", 12, MUTED, KR, "middle")
d.box(col_x[2] + 16, Y1 + 60, col_w[2] - 32, 28, PAPER, WARN, 0.8)
d.t(col_x[2] + col_w[2] / 2, Y1 + 78, "코드 수정 없는 성능 개선 불가", 12, WARN, KR, "middle")

# 명령형 화살표
y_mid1 = Y1 + BH / 2
d.arrow([(col_x[0] + col_w[0], y_mid1), (col_x[1], y_mid1)], SOFT, "soft", 1.3)
d.arrow([(col_x[1] + col_w[1], y_mid1), (col_x[2], y_mid1)], SOFT, "soft", 1.3)

# --- 2. 선언형 트랙 (FOCAL) ---
# 2-1. 패턴 명시
d.tone(col_x[0], Y2, col_w[0], BH, ACC, 6, "18", 1.3)
d.t(col_x[0] + col_w[0] / 2, Y2 + 24, "목표 데이터 패턴 명시", 13, ACC, KR, "middle", 600)
d.t(col_x[0] + col_w[0] / 2, Y2 + 46, "충족할 조건과 변환 명세", 12, MUTED, KR, "middle")
d.box(col_x[0] + 16, Y2 + 60, col_w[0] - 32, 28, PAPER, ACC, 0.8)
d.t(col_x[0] + col_w[0] / 2, Y2 + 78, "WHERE · ORDER BY · GROUP BY", 11, INK, MONO, "middle")

# 2-2. 쿼리 옵티마이저
d.tone(col_x[1], Y2, col_w[1], BH, INFO, 6, "18", 1.2)
d.t(col_x[1] + col_w[1] / 2, Y2 + 24, "쿼리 옵티마이저", 13, INK, KR, "middle", 600)
d.t(col_x[1] + col_w[1] / 2, Y2 + 46, "실행 방법을 대신 결정", 12, MUTED, KR, "middle")
d.box(col_x[1] + 16, Y2 + 60, col_w[1] - 32, 28, PAPER, INFO, 0.8)
d.t(col_x[1] + col_w[1] / 2, Y2 + 78, "인덱스 · 조인 알고리즘 · 순서", 12, INFO, KR, "middle")

# 2-3. 실행과 확장
d.tone(col_x[2], Y2, col_w[2], BH, OK, 6, "18", 1.2)
d.t(col_x[2] + col_w[2] / 2, Y2 + 24, "자동 병렬 실행과 성능 개선", 13, OK, KR, "middle", 600)
d.t(col_x[2] + col_w[2] / 2, Y2 + 46, "다중 코어·머신 병렬 실행 지원", 12, MUTED, KR, "middle")
d.box(col_x[2] + 16, Y2 + 60, col_w[2] - 32, 28, PAPER, OK, 0.8)
d.t(col_x[2] + col_w[2] / 2, Y2 + 78, "쿼리 변경 없는 엔진 개선 흡수", 12, OK, KR, "middle")

# 선언형 화살표
y_mid2 = Y2 + BH / 2
d.arrow([(col_x[0] + col_w[0], y_mid2), (col_x[1], y_mid2)], ACC, "acc", 1.4)
d.arrow([(col_x[1] + col_w[1], y_mid2), (col_x[2], y_mid2)], OK, "ok", 1.4)

d.legend(LEG, [("선언형 쿼리 (focal)", ACC), ("명령형 실행", WARN), ("최적화·병렬 실행", OK), ("옵티마이저 계획", INFO)])
d.save("03-01.declarative-query.svg")
