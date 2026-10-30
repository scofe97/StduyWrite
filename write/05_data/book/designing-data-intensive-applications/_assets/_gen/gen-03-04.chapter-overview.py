# 03-04 개요 — 모델 선택 기준에서 출발해 스키마 시점과 locality 를 거쳐 두 모델의 수렴으로 이어지는 3-4 편 전체 지도.
# 사실 출처: 03-04 본문 §1(L32~L42), §2(L45~L56), §3(L83~L95), §4(L98~L120)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
PY = 96
LEG = 412
H = LEG + 56

d = D(W, H, "03-04 · CHAPTER OVERVIEW", "모델 선택과 스키마 유연성 전체 지도",
      "문서 모델과 관계형 모델을 선택 기준, 스키마 강제 시점, 저장 locality 세 축으로 평가하고 두 모델의 수렴으로 매듭짓는다.",
      "모델 선택 기준 → 스키마 시점 → locality → 두 모델의 수렴")

# 4개 절 컬럼 x 좌표
COLS = [
    (24, 190, "§1 모델 선택 기준"),
    (234, 190, "§2 스키마 시점"),
    (444, 190, "§3 저장 locality"),
    (654, 202, "§4 수렴과 결합"),
]

# 컬럼 배경 및 헤더
for x, w, header in COLS:
    d.box(x, PY, w, 292, PAPER, RULE, 0.8)
    d.chip(x + w / 2, PY + 20, header, SOFT, 11)

# 상단 레인: 문서 모델
# 하단 레인: 관계형 모델
Y_DOC = PY + 46
Y_REL = PY + 168
BW = 170

# §1 선택 기준
d.box(34, Y_DOC, BW, 92, PAPER2, INFO, 1.2)
d.t(34 + BW / 2, Y_DOC + 24, "문서 모델", 13, INK, KR, "middle", 600)
d.t(34 + BW / 2, Y_DOC + 46, "1:N 트리 구조", 12, INFO, KR, "middle")
d.t(34 + BW / 2, Y_DOC + 68, "전체 일괄 로드", 11, MUTED, KR, "middle")

d.box(34, Y_REL, BW, 92, PAPER2, INFO, 1.2)
d.t(34 + BW / 2, Y_REL + 24, "관계형 모델", 13, INK, KR, "middle", 600)
d.t(34 + BW / 2, Y_REL + 46, "중첩 항목 직접 참조", 12, INFO, KR, "middle")
d.t(34 + BW / 2, Y_REL + 68, "다대일 · 다대다 조인", 11, MUTED, KR, "middle")

# §2 스키마 시점
d.box(244, Y_DOC, BW, 92, PAPER2, INFO, 1.2)
d.t(244 + BW / 2, Y_DOC + 24, "schema-on-read", 13, INK, MONO, "middle", 600)
d.t(244 + BW / 2, Y_DOC + 46, "암묵적 스키마", 12, INFO, KR, "middle")
d.t(244 + BW / 2, Y_DOC + 68, "동적 타입 체크 유사", 11, MUTED, KR, "middle")

d.box(244, Y_REL, BW, 92, PAPER2, INFO, 1.2)
d.t(244 + BW / 2, Y_REL + 24, "schema-on-write", 13, INK, MONO, "middle", 600)
d.t(244 + BW / 2, Y_REL + 46, "명시적 스키마 강제", 12, INFO, KR, "middle")
d.t(244 + BW / 2, Y_REL + 68, "쓸 때 마이그레이션", 11, MUTED, KR, "middle")

# §3 저장 locality
d.box(454, Y_DOC, BW, 92, PAPER2, INFO, 1.2)
d.t(454 + BW / 2, Y_DOC + 24, "연속 문자열 저장", 13, INK, KR, "middle", 600)
d.t(454 + BW / 2, Y_DOC + 46, "전체 로드 성능 이점", 12, OK, KR, "middle")
d.t(454 + BW / 2, Y_DOC + 68, "갱신 시 문서 전체 재작성", 11, WARN, KR, "middle")

d.box(454, Y_REL, BW, 92, PAPER2, INFO, 1.2)
d.t(454 + BW / 2, Y_REL + 24, "테이블 분쇄 (shredding)", 13, INK, KR, "middle", 600)
d.t(454 + BW / 2, Y_REL + 46, "다중 인덱스 조회 비용", 12, WARN, KR, "middle")
d.t(454 + BW / 2, Y_REL + 68, "행 interleave 로 locality", 11, OK, KR, "middle")

# §4 수렴과 결합 (Focal ACC 통합 상자)
d.tone(664, PY + 52, 182, 196, ACC, 6, "16", 1.4)
d.t(664 + 91, PY + 84, "상호 기능 흡수", 14, ACC, KR, "middle", 600)
d.line(676, PY + 98, 834, PY + 98, RULE, 0.8)

d.t(664 + 91, PY + 122, "관계형에 JSON 지원", 12, INK, KR, "middle")
d.t(664 + 91, PY + 142, "JSON 타입 · 속성 인덱싱", 11, MUTED, KR, "middle")

d.t(664 + 91, PY + 174, "문서에 관계형 기능", 12, INK, KR, "middle")
d.t(664 + 91, PY + 194, "조인 · 보조 인덱스 · 선언형 쿼리", 11, MUTED, KR, "middle")

d.chip(664 + 91, PY + 224, "관계형-문서 하이브리드", ACC, 11)

# 화살표 연결 (문서 흐름)
d.arrow([(204, Y_DOC + 46), (240, Y_DOC + 46)], MUTED, "ar", 1.2)
d.arrow([(414, Y_DOC + 46), (450, Y_DOC + 46)], MUTED, "ar", 1.2)
d.arrow([(624, Y_DOC + 46), (644, Y_DOC + 46), (644, PY + 118), (660, PY + 118)], ACC, "acc", 1.3)

# 화살표 연결 (관계형 흐름)
d.arrow([(204, Y_REL + 46), (240, Y_REL + 46)], MUTED, "ar", 1.2)
d.arrow([(414, Y_REL + 46), (450, Y_REL + 46)], MUTED, "ar", 1.2)
d.arrow([(624, Y_REL + 46), (644, Y_REL + 46), (644, PY + 180), (660, PY + 180)], ACC, "acc", 1.3)

d.legend(LEG, [("평가 축 · 구성요소", INFO), ("성능 이점", OK), ("비용 · 한계", WARN), ("수렴 하이브리드", ACC)])
d.save("03-04.chapter-overview.svg")
