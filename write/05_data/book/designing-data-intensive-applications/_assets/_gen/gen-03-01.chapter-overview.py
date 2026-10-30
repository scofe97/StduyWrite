# 03-01 개요 — 선언형 쿼리·약사·ORM·문서 모델의 여정. 이력서 한 건이 거치는 네 절의 데이터 모델 지도.
# 사실 출처: 03-01 서두(L21~L38), §1(L42~L48), §2(L51~L63), §3(L66~L81), §4(L85~L118)
# 타입 스펙: type-architecture
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER, PAPER2, RULE, INFO, WARN, OK, KR, MONO

W = 880
PY, PH = 104, 268
LEG = PY + PH + 32
H = LEG + 56

d = D(W, H, "03-01 · CHAPTER OVERVIEW", "관계형 대 문서 모델 전체 지도",
      "이력서 한 건의 데이터를 중심으로 네 절이 다루는 쿼리 언어·모델 발전·ORM 계층·저장 구조의 흐름을 조망한다.",
      "질의 표현 · 지배와 공존 · 객체 번역 · 저장 표현")

CW = 196
GAP = 16
X0 = 24

cards = [
    ("§1", "선언형 쿼리", "질의 패턴과 계획",
     [("user_id = 251", "조건 패턴 명시"),
      ("쿼리 옵티마이저", "실행 계획 결정"),
      ("병렬 실행 도입", "쿼리 변경 없는 개선")],
     INFO),
    ("§2", "모델 약사", "지배와 공존의 역사",
     [("1970 관계형", "테이블·튜플 모델"),
      ("2010 NoSQL", "문서 모델 대중화"),
      ("JSON 지원 흡수", "두 모델의 병행")],
     INFO),
    ("§3", "ORM 불일치", "객체 번역과 한계",
     [("Profile 객체", "인메모리 모델"),
      ("ORM 번역 계층", "임피던스 불일치"),
      ("N+1 쿼리 함정", "조인 fetch 필요")],
     WARN),
    ("§4", "1:N 트리", "문서 모델 저장 표현",
     [("테이블 넷 분할", "외래 키 조인 비용"),
      ("JSON 단일 문서", "자족적 1:N 트리"),
      ("관련 정보 집중", "locality 이점")],
     ACC),
]

FOCAL = 3

for i, (sec, title, role, items, card_c) in enumerate(cards):
    x = X0 + i * (CW + GAP)
    is_focal = (i == FOCAL)
    
    # 카드 외곽
    if is_focal:
        d.box(x, PY, CW, PH, PAPER2, ACC, 1.4)
    else:
        d.box(x, PY, CW, PH, PAPER2, RULE, 0.9)
    
    # 절 헤더: 칩(sec) + 제목
    d.chip(x + 28, PY + 22, sec, card_c, 11)
    d.t(x + CW / 2 + 14, PY + 26, title, 13, INK, KR, "middle", 600)
    d.t(x + CW / 2, PY + 46, role, 12, SOFT, KR, "middle")
    d.line(x + 12, PY + 56, x + CW - 12, PY + 56, RULE, 0.8)
    
    # 내부 항목 3개
    for j, (top_txt, bot_txt) in enumerate(items):
        iy = PY + 68 + j * 64
        
        if is_focal and j == 1:
            d.tone(x + 12, iy, CW - 24, 52, ACC, 6, "22", 1.4)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, ACC, KR, "middle")
        elif i == 2 and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, WARN, 6, "1C", 1.2)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, WARN, KR, "middle")
        elif is_focal and j == 2:
            d.tone(x + 12, iy, CW - 24, 52, OK, 6, "18", 1.1)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, OK, KR, "middle")
        else:
            d.box(x + 12, iy, CW - 24, 52, PAPER, RULE, 0.8)
            d.t(x + CW / 2, iy + 22, top_txt, 12, INK, MONO if any(c in top_txt for c in "=_") else KR, "middle", 600)
            d.t(x + CW / 2, iy + 40, bot_txt, 12, MUTED, KR, "middle")

# 카드 간 수평 연결 화살표
for i in range(3):
    x1 = X0 + i * (CW + GAP) + CW
    x2 = x1 + GAP
    y = PY + PH / 2
    d.arrow([(x1 + 2, y), (x2 - 4, y)], SOFT, "soft", 1.3)

d.legend(LEG, [("핵심 저장 모델", ACC), ("데이터 모델·개념", INFO), ("변환 비용·주의", WARN), ("구조적 이점", OK)])
d.save("03-01.chapter-overview.svg")
