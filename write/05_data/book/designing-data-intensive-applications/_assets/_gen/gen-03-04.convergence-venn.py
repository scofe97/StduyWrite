# 03-04 §4 — 관계형 데이터베이스와 문서 데이터베이스의 고유 강점 및 상호 기능 흡수에 따른 수렴 벤 다이어그램.
# 사실 출처: 03-04 본문 §4(L98~L120) — 관계형의 JSON 타입·연산자·속성 인덱싱 흡수, 문서 DB의 조인·보조 인덱스·선언형 쿼리 흡수, 관계형-문서 하이브리드.
# 타입 스펙: type-venn
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, BAD, KR, MONO

W = 880
CY = 295
R = 190
CX1, CX2 = 320, 560
LEG = 506
H = LEG + 56

d = D(W, H, "03-04 · CONVERGENCE", "관계형과 문서 모델의 상호 기능 흡수와 수렴",
      "관계형은 JSON 과 속성 인덱싱을 더하고, 문서는 조인과 보조 인덱스를 더하며 관계형-문서 하이브리드로 수렴한다.",
      "관계형 고유 강점 × 문서 고유 강점 → 상호 기능 흡수와 하이브리드 결합")

# defs 에 클립패스 추가 (중앙 교집합 영역 하이라이트)
d.o.append('<defs>')
d.o.append(f'<clipPath id="clip-c1"><circle cx="{CX1}" cy="{CY}" r="{R}"/></clipPath>')
d.o.append('</defs>')

# 두 원 (배경 틴트 및 테두리)
d.o.append(f'<circle cx="{CX1}" cy="{CY}" r="{R}" fill="{INFO}06" stroke="{INFO}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{CX2}" cy="{CY}" r="{R}" fill="{OK}06" stroke="{OK}" stroke-width="1.2"/>')

# 교집합 영역에 ACC 틴트 (원 2를 원 1 클립패스로 자름)
d.o.append(f'<circle cx="{CX2}" cy="{CY}" r="{R}" fill="{ACC}18" clip-path="url(#clip-c1)"/>')

# 좌측 원 고유 영역 카드 (관계형)
LX = 210
d.box(LX - 100, CY - 120, 200, 240, PAPER2, RULE, 0.9)
d.t(LX, CY - 96, "관계형 데이터베이스", 13, INFO, KR, "middle", 600)
d.t(LX, CY - 78, "정규화 · 스키마 강제", 11, MUTED, KR, "middle")
d.line(LX - 80, CY - 66, LX + 80, CY - 66, RULE, 0.6)

d.t(LX, CY - 44, "schema-on-write", 11, INFO, MONO, "middle", 600)
d.t(LX, CY - 28, "쓸 때 적합성 보장", 11, MUTED, KR, "middle")
d.t(LX, CY - 2, "다대일 · 다대다 조인", 11, INFO, KR, "middle", 600)
d.t(LX, CY + 14, "조인을 더 잘 지원", 11, MUTED, KR, "middle")
d.t(LX, CY + 40, "SQL 표준 선언형 쿼리", 11, INFO, KR, "middle", 600)
d.t(LX, CY + 56, "대부분 SQL 로 쿼리", 11, MUTED, KR, "middle")
d.t(LX, CY + 82, "같은 구조 레코드에 유리", 11, SOFT, KR, "middle", 600)
d.t(LX, CY + 98, "마이그레이션으로 형식 변경", 11, SOFT, KR, "middle")

# 우측 원 고유 영역 카드 (문서 DB)
RX = 670
d.box(RX - 100, CY - 120, 200, 240, PAPER2, RULE, 0.9)
d.t(RX, CY - 96, "문서 데이터베이스", 13, OK, KR, "middle", 600)
d.t(RX, CY - 78, "locality · 스키마 유연성", 11, MUTED, KR, "middle")
d.line(RX - 80, CY - 66, RX + 80, CY - 66, RULE, 0.6)

d.t(RX, CY - 44, "schema-on-read", 11, OK, MONO, "middle", 600)
d.t(RX, CY - 28, "암묵적 스키마 · 동적 유연성", 11, MUTED, KR, "middle")
d.t(RX, CY - 2, "1:N 트리 연속 저장", 11, OK, KR, "middle", 600)
d.t(RX, CY + 14, "단일 문서 로드 locality 이점", 11, MUTED, KR, "middle")
d.t(RX, CY + 40, "앱 객체 모델에 근접", 11, OK, KR, "middle", 600)
d.t(RX, CY + 56, "배열 순서 직접 보존", 11, MUTED, KR, "middle")
d.t(RX, CY + 82, "이질적 데이터 처리 유리", 11, SOFT, KR, "middle", 600)
d.t(RX, CY + 98, "문서 크기 최소화 권고", 11, SOFT, KR, "middle")

# 중앙 교집합 영역 카드 (수렴과 하이브리드)
MX = 440
# 원 테두리가 가운데 글자를 가로지르지 않도록 불투명 바탕을 먼저 깐다
d.box(MX - 95, CY - 130, 190, 260, PAPER, PAPER, 0, 8)
d.tone(MX - 95, CY - 130, 190, 260, ACC, 8, "16", 1.4)
d.t(MX, CY - 106, "상호 기능 흡수", 13, ACC, KR, "middle", 600)
d.chip(MX, CY - 82, "관계형-문서 하이브리드", ACC, 11)

d.line(MX - 76, CY - 66, MX + 76, CY - 66, RULE, 0.8)

# 관계형의 흡수
d.t(MX, CY - 46, "관계형이 흡수한 기능", 11, INK, KR, "middle", 600)
d.t(MX, CY - 28, "JSON 데이터타입 지원", 11, MUTED, KR, "middle")
d.t(MX, CY - 12, "JSON 쿼리 연산자", 11, MUTED, KR, "middle")
d.t(MX, CY + 4, "문서 내부 속성 인덱싱", 11, MUTED, KR, "middle")

d.line(MX - 50, CY + 18, MX + 50, CY + 18, RULE, 0.6)

# 문서 DB의 흡수
d.t(MX, CY + 38, "문서 DB가 흡수한 기능", 11, INK, KR, "middle", 600)
d.t(MX, CY + 56, "문서 간 $lookup 조인", 11, MUTED, KR, "middle")
d.t(MX, CY + 72, "문서 내 필드 보조 인덱스", 11, MUTED, KR, "middle")
d.t(MX, CY + 88, "선언형 집계 파이프라인", 11, MUTED, KR, "middle")

d.chip(MX, CY + 112, "Codd 의 중첩 관계 값", SOFT, 11)

d.legend(LEG, [("수렴 하이브리드 (상호 흡수)", ACC), ("관계형 데이터베이스", INFO), ("문서 데이터베이스", OK)])
d.save("03-04.convergence-venn.svg")
