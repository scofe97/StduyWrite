# 13-03 §3 — 검색 인덱스에서 쓰기 경로와 읽기 경로가 만나는 지점 (DDIA 2판 Figure 13-1).
# 사실 출처: 13-03 §3(L42~L53), DDIA 2판 Ch.13 Figure 13-1(PDF p.22) — Update document, Application server,
#   Linguistic analysis, Terms appearing in document, Search index, Query, Search query executor,
#   Expanded search query, Search terms, Posting lists, Search results, Results.
# 2026-10-31 검증: 그림은 PDF p.22 확인. Linguistic analysis 를 "형태소" 없이 "언어 분석"으로, 색인 칸 문구를 원서 p.22~23(모든 단어 항목 갱신, 불리언 논리, 쓰기·읽기 시점 일의 트레이드오프)으로
# 타입 스펙: type-data-flow
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
LEG = 474
H = LEG + 52

d = D(W, H, "13-03 · §3 WRITE PATH AND READ PATH", "검색 인덱스에서 쓰기 경로와 읽기 경로의 수렴",
      "원서 Figure 13-1: 문서 갱신(쓰기 경로)과 질의(읽기 경로)가 파생 데이터셋인 검색 인덱스에서 만난다.",
      "문서 갱신 (사전 계산) · 언어 분석 · 검색 인덱스 (파생 데이터셋) · 질의 실행기 · 질의 결과 (지연 평가)")

# 상단 쓰기 경로 영역 배너
d.tone(24, 104, 550, 30, OK, 4, "12", 0.9)
d.t(299, 123, "쓰기 경로 (Write Path) — 문서 변경 시 사전 계산 · 즉시 평가 (Eager)", 11, OK, KR, "middle", 600)

# 하단 읽기 경로 영역 배너
d.tone(24, 258, 550, 30, INFO, 4, "12", 0.9)
d.t(299, 277, "읽기 경로 (Read Path) — 사용자 요청 시 실행 · 지연 평가 (Lazy)", 11, INFO, KR, "middle", 600)

# -----------------
# 1. 쓰기 경로 (Top Row, y=148)
# -----------------
Y_WRITE = 148
BOX_H = 88

# 1-1. 사용자 (문서 작성자)
d.box(24, Y_WRITE, 106, BOX_H, PAPER2, RULE, 0.9)
d.chip(24 + 53, Y_WRITE + 18, "작성자", OK, 11)
d.t(77, Y_WRITE + 48, "클라이언트", 12, INK, KR, "middle", 600)
d.t(77, Y_WRITE + 68, "문서 갱신 요청", 11, MUTED, KR, "middle")

# 화살표 1: 작성자 -> 앱 서버
d.arrow([(130, Y_WRITE + 44), (186, Y_WRITE + 44)], OK, "ok", 1.4)
d.t(158, Y_WRITE + 32, "문서 갱신", 11, OK, KR, "middle")

# 1-2. 애플리케이션 서버 (쓰기)
d.box(186, Y_WRITE, 134, BOX_H, PAPER2, RULE, 0.9)
d.chip(186 + 67, Y_WRITE + 18, "서버", MUTED, 11)
d.t(253, Y_WRITE + 48, "애플리케이션 서버", 12, INK, KR, "middle", 600)
d.t(253, Y_WRITE + 68, "Application Server", 11, SOFT, MONO, "middle")

# 화살표 2: 앱 서버 -> 형태소 분석
d.arrow([(320, Y_WRITE + 44), (378, Y_WRITE + 44)], OK, "ok", 1.4)
d.t(349, Y_WRITE + 32, "새 문서 버전", 11, OK, KR, "middle")

# 1-3. 형태소/언어 분석
d.box(378, Y_WRITE, 148, BOX_H, PAPER2, RULE, 0.9)
d.chip(378 + 74, Y_WRITE + 18, "분석", OK, 11)
d.t(452, Y_WRITE + 48, "언어 분석", 12, INK, KR, "middle", 600)
d.t(452, Y_WRITE + 68, "Linguistic Analysis", 11, SOFT, MONO, "middle")

# 화살표 3: 형태소 분석 -> 검색 인덱스
d.arrow([(526, Y_WRITE + 44), (590, Y_WRITE + 44)], OK, "ok", 1.4)
d.t(558, Y_WRITE + 32, "출현 단어", 11, OK, KR, "middle")

# -----------------
# 2. 읽기 경로 (Bottom Row, y=302)
# -----------------
Y_READ = 302

# 2-1. 사용자 (질의자)
d.box(24, Y_READ, 106, BOX_H, PAPER2, RULE, 0.9)
d.chip(24 + 53, Y_READ + 18, "질의자", INFO, 11)
d.t(77, Y_READ + 48, "클라이언트", 12, INK, KR, "middle", 600)
d.t(77, Y_READ + 68, "질의 및 수신", 11, MUTED, KR, "middle")

# 화살표 쌍: 질의자 <-> 앱 서버
d.arrow([(130, Y_READ + 28), (186, Y_READ + 28)], INFO, "info", 1.3)
d.t(158, Y_READ + 18, "검색 질의", 11, INFO, KR, "middle")
d.arrow([(186, Y_READ + 60), (130, Y_READ + 60)], INFO, "info", 1.3)
d.t(158, Y_READ + 76, "최종 결과", 11, MUTED, KR, "middle")

# 2-2. 애플리케이션 서버 (읽기)
d.box(186, Y_READ, 134, BOX_H, PAPER2, RULE, 0.9)
d.chip(186 + 67, Y_READ + 18, "서버", MUTED, 11)
d.t(253, Y_READ + 48, "애플리케이션 서버", 12, INK, KR, "middle", 600)
d.t(253, Y_READ + 68, "Application Server", 11, SOFT, MONO, "middle")

# 화살표 쌍: 앱 서버 <-> 질의 실행기
d.arrow([(320, Y_READ + 28), (378, Y_READ + 28)], INFO, "info", 1.3)
d.t(349, Y_READ + 18, "확장 질의", 11, INFO, KR, "middle")
d.arrow([(378, Y_READ + 60), (320, Y_READ + 60)], INFO, "info", 1.3)
d.t(349, Y_READ + 76, "검색 결과", 11, MUTED, KR, "middle")

# 2-3. 검색 질의 실행기
d.box(378, Y_READ, 148, BOX_H, PAPER2, RULE, 0.9)
d.chip(378 + 74, Y_READ + 18, "질의 실행", INFO, 11)
d.t(452, Y_READ + 48, "검색 질의 실행기", 12, INK, KR, "middle", 600)
d.t(452, Y_READ + 68, "Search Query Executor", 11, SOFT, MONO, "middle")

# 화살표 쌍: 질의 실행기 <-> 검색 인덱스
d.arrow([(526, Y_READ + 28), (590, Y_READ + 28)], INFO, "info", 1.3)
d.t(558, Y_READ + 18, "검색 단어", 11, INFO, KR, "middle")
d.arrow([(590, Y_READ + 60), (526, Y_READ + 60)], INFO, "info", 1.3)
d.t(558, Y_READ + 76, "포스팅 목록", 11, MUTED, KR, "middle")

# -----------------
# 3. 만나는 지점: 검색 인덱스 (Center Right)
# -----------------
d.box(590, 104, 266, 286, PAPER2, ACC, 1.5, r=8)
d.tone(590, 104, 266, 286, ACC, 8, "0d", 1.5)

d.chip(590 + 133, 126, "수렴 지점", ACC, 11)
d.t(723, 156, "검색 인덱스", 15, INK, KR, "middle", 600)
d.t(723, 174, "Search Index (파생 데이터셋)", 11, ACC, KR, "middle")

d.line(604, 186, 842, 186, RULE, 0.8)

# 쓰기 경로 연계 박스
d.box(604, 196, 238, 54, PAPER, OK, 0.8)
d.t(723, 216, "쓰기 경로 수렴 (Eager)", 11, OK, KR, "middle", 600)
d.t(723, 236, "문서의 모든 단어 항목 갱신", 11, MUTED, KR, "middle")

# 읽기 경로 연계 박스
d.box(604, 260, 238, 54, PAPER, INFO, 0.8)
d.t(723, 280, "읽기 경로 수렴 (Lazy)", 11, INFO, KR, "middle", 600)
d.t(723, 300, "단어마다 검색 · 불리언 논리", 11, MUTED, KR, "middle")

# 트레이드오프 박스
d.box(604, 324, 238, 52, PAPER, ACC, 0.8)
d.t(723, 344, "경계 이동 트레이드오프", 11, INK, KR, "middle", 600)
d.t(723, 362, "쓰기 시점 일 ↔ 읽기 시점 일", 11, MUTED, KR, "middle")

# -----------------
# 4. 하단 요약 배너
# -----------------
d.tone(24, 404, W - 48, 38, WARN, 4, "12", 0.9)
d.t(W / 2, 427, "인덱스 없음 = 읽기 때 전체 문서 스캔 ↔ 모든 쿼리 결과 사전 계산 = 쓰기 비용 무한", 11, INK, KR, "middle", 600)

d.legend(LEG, [
    ("파생 데이터셋 (focal)", ACC),
    ("쓰기 경로 파이프라인", OK),
    ("읽기 경로 파이프라인", INFO),
    ("비용 경계 트레이드오프", WARN),
])

d.save("13-03.search-index-write-read-path.svg")
